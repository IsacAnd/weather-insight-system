import {
    Injectable,
    HttpException,
    Logger,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as crypto from 'crypto';

@Injectable()
export class DeepSeekService {
    private readonly apiKey: string;
    private readonly model: string;
    private readonly apiUrl: string;

    private readonly logger = new Logger(DeepSeekService.name);

    private readonly insightsCache = new Map<string, string>();

    private firstFailureAt: number | null = null;

    private readonly ALERT_THRESHOLD_MS = 60_000;

    constructor(private readonly config: ConfigService) {
        this.apiKey = this.config.get<string>('DS_API_KEY')!;
        this.model = this.config.get<string>('DS_MODEL')!;
        this.apiUrl = this.config.get<string>('DS_API_URL')!;
    }

    private generateHash(weatherData: any[]): string {
        return crypto
            .createHash('sha256')
            .update(JSON.stringify(weatherData))
            .digest('hex');
    }

    private registerFailure(): void {
        if (!this.firstFailureAt) {
            this.firstFailureAt = Date.now();
            return;
        }

        const elapsed =
            Date.now() - this.firstFailureAt;

        if (elapsed >= this.ALERT_THRESHOLD_MS) {
            this.logger.error(
                `DeepSeek indisponível há mais de ${this.ALERT_THRESHOLD_MS / 1000
                } segundos.`,
            );

            /**
             * Reinicia o contador para evitar spam
             */
            this.firstFailureAt = Date.now();
        }
    }

    private registerSuccess(): void {
        if (this.firstFailureAt) {
            this.logger.log(
                'DeepSeek voltou a responder normalmente.',
            );
        }

        this.firstFailureAt = null;
    }

    async generateWeatherInsights(
        weatherData: any[],
    ): Promise<string> {
        if (!this.apiKey) {
            throw new HttpException(
                'DS_API_KEY não configurada no .env',
                500,
            );
        }

        /**
         * CACHE
         */
        const hash = this.generateHash(weatherData);

        const cachedInsight =
            this.insightsCache.get(hash);

        if (cachedInsight) {
            this.logger.log(
                `Cache HIT - hash: ${hash.substring(
                    0,
                    12,
                )}...`,
            );

            return cachedInsight;
        }

        this.logger.log(
            `Cache MISS - hash: ${hash.substring(
                0,
                12,
            )}...`,
        );

        const formattedData = JSON.stringify(
            weatherData.slice(0, 100),
            null,
            2,
        );

        const payload = {
            model: this.model,
            messages: [
                {
                    role: 'system',
                    content:
                        'Analise a lista de 100 dados meteorológicos enviados e gere APENAS UM insight curto e direto (máximo 12 palavras). Não explique nada. Não use markdown. Apenas uma frase.',
                },
                {
                    role: 'user',
                    content: `Aqui estão os dados meteorológicos (máx. 100 registros):\n\n${formattedData}`,
                },
            ],
            temperature: 0.3,
            max_output_tokens: 600,
        };

        const controller =
            new AbortController();

        const timeout = setTimeout(() => {
            controller.abort();
        }, 10000);

        try {
            const response = await fetch(
                this.apiUrl,
                {
                    method: 'POST',
                    headers: {
                        Authorization: `Bearer ${this.apiKey}`,
                        'Content-Type':
                            'application/json',
                    },
                    body: JSON.stringify(payload),
                    signal: controller.signal,
                },
            );

            clearTimeout(timeout);

            if (!response.ok) {
                const err =
                    await response.text();

                this.registerFailure();

                throw new HttpException(
                    `Erro da API DeepSeek: ${err}`,
                    response.status,
                );
            }

            const data =
                await response.json();

            const insight =
                data?.choices?.[0]?.message
                    ?.content ??
                'Não foi possível gerar insights.';

            /**
             * Salva no cache
             */
            this.insightsCache.set(
                hash,
                insight,
            );

            /**
             * Serviço voltou a responder
             */
            this.registerSuccess();

            return insight;
        } catch (error: any) {
            clearTimeout(timeout);

            this.registerFailure();

            if (
                error.name === 'AbortError'
            ) {
                throw new HttpException(
                    'Timeout ao comunicar com a DeepSeek.',
                    504,
                );
            }

            throw new HttpException(
                `Erro ao chamar o modelo DeepSeek: ${error.message}`,
                500,
            );
        }
    }
}
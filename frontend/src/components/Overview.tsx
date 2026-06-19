import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import {
    Sun,
    Cloud,
    Droplet,
    CloudFog,
    CloudLightning,
    CloudSun,
    MapPin,
} from "lucide-react";
import type { JSX } from "react/jsx-dev-runtime";

type WeatherCondition =
    | "Ensolarado"
    | "Parcialmente nublado"
    | "Nublado"
    | "Chuvoso"
    | "Neblina"
    | "Tempestade";

interface OverviewSectionProps {
    weatherData: any;
    loadingWeather: boolean;
    insight: string | null;
    loadingInsight: boolean;
    insightError: boolean;
    coords: { latitude: number; longitude: number } | null;
}

// Fortaleza como fallback (mesmo padrão do backend)
const DEFAULT_LAT = -3.7172;
const DEFAULT_LON = -38.5433;

function buildMapViewUrl(lat: number, lon: number): string {
    return (
        `https://maps.google.com/maps` +
        `?q=${lat},${lon}` +
        `&z=13` +
        `&output=embed`
    );
}

export default function OverviewSection({
    weatherData,
    loadingWeather,
    insight,
    loadingInsight,
    insightError,
    coords,
}: OverviewSectionProps) {
    const [locationName, setLocationName] = useState<string>("Carregando...");

    const lat = coords?.latitude ?? DEFAULT_LAT;
    const lon = coords?.longitude ?? DEFAULT_LON;

    useEffect(() => {
        const controller = new AbortController();

        async function fetchLocationName() {
            try {
                const res = await fetch(
                    `https://nominatim.openstreetmap.org/reverse` +
                    `?lat=${lat}&lon=${lon}&format=json&accept-language=pt-BR`,
                    {
                        signal: controller.signal,
                        headers: {
                            "Accept-Language": "pt-BR",
                        },
                    }
                );

                if (!res.ok) throw new Error("Nominatim error");

                const data = await res.json();

                const addr = data.address ?? {};

                const city =
                    addr.city ||
                    addr.town ||
                    addr.village ||
                    addr.hamlet ||
                    addr.suburb ||
                    addr.municipality ||
                    addr.county ||
                    addr.region;

                const state = addr.state;

                if (city && state) {
                    setLocationName(`${city}, ${state}`);
                } else if (city) {
                    setLocationName(city);
                } else if (data.display_name) {
                    const parts = data.display_name.split(",").map((s: string) => s.trim());
                    setLocationName(parts.slice(0, 2).join(", "));
                } else {
                    setLocationName("Local desconhecido");
                }
            } catch (err: any) {
                if (err.name !== "AbortError") {
                    setLocationName("Local desconhecido");
                }
            }
        }

        fetchLocationName();

        return () => controller.abort();
    }, [lat, lon]);

    const conditionIcons: Record<WeatherCondition, JSX.Element> = {
        Ensolarado: (
            <Sun className="w-20 h-20 text-yellow-400 drop-shadow-[0_0_15px_rgba(255,230,0,0.5)]" />
        ),
        "Parcialmente nublado": (
            <CloudSun className="w-20 h-20 text-yellow-300 drop-shadow-[0_0_15px_rgba(255,200,0,0.4)]" />
        ),
        Nublado: (
            <Cloud className="w-20 h-20 text-gray-300 drop-shadow-[0_0_12px_rgba(200,200,200,0.4)]" />
        ),
        Chuvoso: (
            <Droplet className="w-20 h-20 text-blue-400 drop-shadow-[0_0_15px_rgba(50,130,255,0.5)]" />
        ),
        Neblina: (
            <CloudFog className="w-20 h-20 text-gray-400 drop-shadow-[0_0_15px_rgba(180,180,180,0.5)]" />
        ),
        Tempestade: (
            <CloudLightning className="w-20 h-20 text-purple-500 drop-shadow-[0_0_18px_rgba(180,0,255,0.6)]" />
        ),
    };

    if (loadingWeather) {
        return <p className="text-center text-gray-300">Carregando...</p>;
    }

    if (!weatherData) {
        return <p className="text-center text-red-400">Erro ao carregar dados.</p>;
    }

    return (
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
            <Card className="lg:col-span-2 bg-[#161b22] text-white rounded-3xl p-8 shadow-xl border border-white/10">
                <div className="flex justify-between items-start">
                    <div>
                        {/* Nome do local via reverse geocoding */}
                        <span className="flex items-center gap-1 text-purple-400 px-3 py-1 rounded-full bg-purple-400/10 text-sm w-fit">
                            <MapPin className="w-3 h-3" />
                            {locationName}
                        </span>

                        {/* Coordenadas exatas */}
                        <p className="text-xs text-gray-500 mt-1 ml-1">
                            {lat.toFixed(5)}, {lon.toFixed(5)}
                        </p>

                        <h2 className="text-5xl font-bold mt-6">
                            {weatherData.temperature}°C
                        </h2>

                        <p className="text-gray-400 text-lg mt-1">
                            {new Date().toLocaleDateString("pt-BR", {
                                weekday: "long",
                                day: "2-digit",
                                month: "short",
                                year: "numeric",
                            })}
                        </p>

                        <p className="text-3xl font-semibold mt-6">
                            {weatherData.condition}
                        </p>

                        <p className="text-gray-400">
                            Sensação térmica: {weatherData.heatIndex}°
                        </p>
                    </div>

                    <div className="drop-shadow-xl">
                        {conditionIcons[weatherData.condition as WeatherCondition]}
                    </div>
                </div>

                <div className="mt-10">
                    {loadingInsight && (
                        <div className="animate-pulse text-gray-400 text-lg bg-white/5 p-3 rounded-2xl border border-white/10 w-fit">
                            Analisando clima...
                        </div>
                    )}

                    {insightError && (
                        <div className="text-red-400 bg-red-400/10 p-3 rounded-2xl border border-red-400/20 w-fit">
                            Não foi possível gerar o insight.
                        </div>
                    )}

                    {insight && !loadingInsight && !insightError && (
                        <div className="flex items-center gap-3 bg-purple-500/10 border border-purple-500/20 p-4 rounded-2xl shadow-lg w-fit backdrop-blur-sm">
                            <Sun className="w-6 h-6 text-purple-300 animate-pulse" />
                            <p className="text-purple-200 text-lg font-medium">
                                {insight}
                            </p>
                        </div>
                    )}
                </div>

                <div className="mt-10 w-full">
                    <iframe
                        key={`${lat}-${lon}`}
                        width="100%"
                        height="350"
                        className="rounded-3xl border border-white/10 shadow-lg"
                        loading="lazy"
                        allowFullScreen
                        referrerPolicy="no-referrer-when-downgrade"
                        src={buildMapViewUrl(lat, lon)}
                        title={`Mapa de ${locationName}`}
                    />
                </div>
            </Card>

            <div className="grid grid-cols-1 gap-6">
                {[
                    ["Chance de Chuva", `${weatherData.precipitationChance}%`],
                    ["Índice UV", weatherData.uvIndex],
                    ["Vento", `${weatherData.windSpeed ?? weatherData.windspeed} km/h`],
                    ["Umidade", `${weatherData.humidity}%`],
                ].map(([label, value]) => (
                    <Card
                        key={label}
                        className="bg-[#161b22] border border-white/10 rounded-3xl p-6 text-white"
                    >
                        <h3 className="text-xl font-semibold mb-3">{label}</h3>
                        <p className="text-3xl font-bold">{value}</p>
                    </Card>
                ))}
            </div>
        </div>
    );
}
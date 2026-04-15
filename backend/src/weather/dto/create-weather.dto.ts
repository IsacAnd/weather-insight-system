import { IsOptional, IsNumber, IsString, IsISO8601 } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateWeatherDto {
  @IsOptional()
  @IsString()
  source?: string;

  @IsOptional()
  @IsISO8601()
  obs_timestamp?: string

  @IsString()
  @IsISO8601()
  timestamp: string;

  @IsNumber()
  @Type(() => Number)
  temperature: number;

  @IsNumber()
  @Type(() => Number)
  windspeed: number;

  @IsNumber()
  @Type(() => Number)
  humidity: number;

  @IsNumber()
  @Type(() => Number)
  uvIndex: number;

  @IsNumber()
  @Type(() => Number)
  precipitationChance: number;

  @IsNumber()
  @Type(() => Number)
  heatIndex: number;

  @IsOptional()
  @IsString()
  condition?: string;
}

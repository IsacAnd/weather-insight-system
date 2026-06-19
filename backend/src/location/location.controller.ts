import { Body, Controller, Get, Post, BadRequestException } from '@nestjs/common';
import { IsNumber, Min, Max } from 'class-validator';
import { Type } from 'class-transformer';
import { LocationService } from './location.service';

class SetLocationDto {
    @IsNumber()
    @Min(-90)
    @Max(90)
    @Type(() => Number)
    latitude: number;

    @IsNumber()
    @Min(-180)
    @Max(180)
    @Type(() => Number)
    longitude: number;
}

@Controller('api/location')
export class LocationController {
    constructor(private readonly locationService: LocationService) { }

    @Get()
    async getLocation() {
        return this.locationService.getLocation();
    }

    @Post()
    async setLocation(@Body() body: SetLocationDto) {
        await this.locationService.setLocation(body.latitude, body.longitude);
        return { success: true, latitude: body.latitude, longitude: body.longitude };
    }
}
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { LocationController } from './location.controller';
import { LocationService } from './location.service';
import { LocationConfig, LocationConfigSchema } from './schemas/location-config.schema';

@Module({
    imports: [
        MongooseModule.forFeature([
            { name: LocationConfig.name, schema: LocationConfigSchema },
        ]),
    ],
    controllers: [LocationController],
    providers: [LocationService],
    exports: [LocationService],
})
export class LocationModule { }
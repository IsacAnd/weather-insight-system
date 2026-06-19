import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { LocationConfig, LocationConfigDocument } from './schemas/location-config.schema';

// Fortaleza, CE como fallback padrão
const DEFAULT_LAT = -3.7172;
const DEFAULT_LON = -38.5433;

@Injectable()
export class LocationService {
    constructor(
        @InjectModel(LocationConfig.name)
        private locationModel: Model<LocationConfigDocument>,
    ) { }

    async getLocation(): Promise<{ latitude: number; longitude: number }> {
        const doc = await this.locationModel.findOne().lean().exec();

        if (!doc) {
            return { latitude: DEFAULT_LAT, longitude: DEFAULT_LON };
        }

        return { latitude: doc.latitude, longitude: doc.longitude };
    }

    async setLocation(latitude: number, longitude: number): Promise<void> {
        await this.locationModel.findOneAndUpdate(
            {},
            { latitude, longitude, updatedAt: new Date() },
            { upsert: true, new: true },
        );
    }
}
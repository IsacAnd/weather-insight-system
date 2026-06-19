import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type LocationConfigDocument = LocationConfig & Document;

@Schema({ collection: 'location_config' })
export class LocationConfig {
    @Prop({ required: true })
    latitude: number;

    @Prop({ required: true })
    longitude: number;

    @Prop({ default: Date.now })
    updatedAt: Date;
}

export const LocationConfigSchema = SchemaFactory.createForClass(LocationConfig);
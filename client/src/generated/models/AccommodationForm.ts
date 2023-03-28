/* tslint:disable */
/* eslint-disable */
/**
 * Flat Finder REST API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { AccommodationAddress } from './AccommodationAddress';
import {
    AccommodationAddressFromJSON,
    AccommodationAddressFromJSONTyped,
    AccommodationAddressToJSON,
} from './AccommodationAddress';

/**
 * 
 * @export
 * @interface AccommodationForm
 */
export interface AccommodationForm {
    /**
     * 
     * @type {string}
     * @memberof AccommodationForm
     */
    title: string;
    /**
     * 
     * @type {string}
     * @memberof AccommodationForm
     */
    description: string;
    /**
     * 
     * @type {Array<Blob>}
     * @memberof AccommodationForm
     */
    photos: Array<Blob>;
    /**
     * 
     * @type {string}
     * @memberof AccommodationForm
     */
    accommodationType: string;
    /**
     * 
     * @type {number}
     * @memberof AccommodationForm
     */
    numberOfRooms: number;
    /**
     * 
     * @type {number}
     * @memberof AccommodationForm
     */
    price: number;
    /**
     * 
     * @type {AccommodationAddress}
     * @memberof AccommodationForm
     */
    address: AccommodationAddress;
}

/**
 * Check if a given object implements the AccommodationForm interface.
 */
export function instanceOfAccommodationForm(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "title" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "photos" in value;
    isInstance = isInstance && "accommodationType" in value;
    isInstance = isInstance && "numberOfRooms" in value;
    isInstance = isInstance && "price" in value;
    isInstance = isInstance && "address" in value;

    return isInstance;
}

export function AccommodationFormFromJSON(json: any): AccommodationForm {
    return AccommodationFormFromJSONTyped(json, false);
}

export function AccommodationFormFromJSONTyped(json: any, ignoreDiscriminator: boolean): AccommodationForm {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'title': json['title'],
        'description': json['description'],
        'photos': json['photos'],
        'accommodationType': json['accommodationType'],
        'numberOfRooms': json['numberOfRooms'],
        'price': json['price'],
        'address': AccommodationAddressFromJSON(json['address']),
    };
}

export function AccommodationFormToJSON(value?: AccommodationForm | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'title': value.title,
        'description': value.description,
        'photos': value.photos,
        'accommodationType': value.accommodationType,
        'numberOfRooms': value.numberOfRooms,
        'price': value.price,
        'address': AccommodationAddressToJSON(value.address),
    };
}


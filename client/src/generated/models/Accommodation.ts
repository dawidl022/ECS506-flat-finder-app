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
import type { ListingAuthor } from './ListingAuthor';
import {
    ListingAuthorFromJSON,
    ListingAuthorFromJSONTyped,
    ListingAuthorToJSON,
} from './ListingAuthor';
import type { ListingContactInfo } from './ListingContactInfo';
import {
    ListingContactInfoFromJSON,
    ListingContactInfoFromJSONTyped,
    ListingContactInfoToJSON,
} from './ListingContactInfo';

/**
 * 
 * @export
 * @interface Accommodation
 */
export interface Accommodation {
    /**
     * 
     * @type {string}
     * @memberof Accommodation
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof Accommodation
     */
    title: string;
    /**
     * 
     * @type {string}
     * @memberof Accommodation
     */
    description: string;
    /**
     * 
     * @type {Array<string>}
     * @memberof Accommodation
     */
    photoUrls: Array<string>;
    /**
     * 
     * @type {string}
     * @memberof Accommodation
     */
    accommodationType: string;
    /**
     * 
     * @type {number}
     * @memberof Accommodation
     */
    numberOfRooms: number;
    /**
     * 
     * @type {string}
     * @memberof Accommodation
     */
    source: string;
    /**
     * 
     * @type {number}
     * @memberof Accommodation
     */
    price: number;
    /**
     * 
     * @type {AccommodationAddress}
     * @memberof Accommodation
     */
    address: AccommodationAddress;
    /**
     * 
     * @type {ListingAuthor}
     * @memberof Accommodation
     */
    author: ListingAuthor;
    /**
     * 
     * @type {string}
     * @memberof Accommodation
     */
    originalListingUrl?: string;
    /**
     * 
     * @type {ListingContactInfo}
     * @memberof Accommodation
     */
    contactInfo: ListingContactInfo;
}

/**
 * Check if a given object implements the Accommodation interface.
 */
export function instanceOfAccommodation(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "title" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "photoUrls" in value;
    isInstance = isInstance && "accommodationType" in value;
    isInstance = isInstance && "numberOfRooms" in value;
    isInstance = isInstance && "source" in value;
    isInstance = isInstance && "price" in value;
    isInstance = isInstance && "address" in value;
    isInstance = isInstance && "author" in value;
    isInstance = isInstance && "contactInfo" in value;

    return isInstance;
}

export function AccommodationFromJSON(json: any): Accommodation {
    return AccommodationFromJSONTyped(json, false);
}

export function AccommodationFromJSONTyped(json: any, ignoreDiscriminator: boolean): Accommodation {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'title': json['title'],
        'description': json['description'],
        'photoUrls': json['photoUrls'],
        'accommodationType': json['accommodationType'],
        'numberOfRooms': json['numberOfRooms'],
        'source': json['source'],
        'price': json['price'],
        'address': AccommodationAddressFromJSON(json['address']),
        'author': ListingAuthorFromJSON(json['author']),
        'originalListingUrl': !exists(json, 'originalListingUrl') ? undefined : json['originalListingUrl'],
        'contactInfo': ListingContactInfoFromJSON(json['contactInfo']),
    };
}

export function AccommodationToJSON(value?: Accommodation | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'title': value.title,
        'description': value.description,
        'photoUrls': value.photoUrls,
        'accommodationType': value.accommodationType,
        'numberOfRooms': value.numberOfRooms,
        'source': value.source,
        'price': value.price,
        'address': AccommodationAddressToJSON(value.address),
        'author': ListingAuthorToJSON(value.author),
        'originalListingUrl': value.originalListingUrl,
        'contactInfo': ListingContactInfoToJSON(value.contactInfo),
    };
}


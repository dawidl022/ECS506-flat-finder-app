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
import type { UserProfile } from './UserProfile';
import {
    UserProfileFromJSON,
    UserProfileFromJSONTyped,
    UserProfileToJSON,
} from './UserProfile';

/**
 * If the listing author is a consultant, the userProfile property is present containing the consultant's profile
 * @export
 * @interface ListingAuthor
 */
export interface ListingAuthor {
    /**
     * 
     * @type {string}
     * @memberof ListingAuthor
     */
    name: string;
    /**
     * 
     * @type {UserProfile}
     * @memberof ListingAuthor
     */
    userProfile?: UserProfile;
}

/**
 * Check if a given object implements the ListingAuthor interface.
 */
export function instanceOfListingAuthor(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "name" in value;

    return isInstance;
}

export function ListingAuthorFromJSON(json: any): ListingAuthor {
    return ListingAuthorFromJSONTyped(json, false);
}

export function ListingAuthorFromJSONTyped(json: any, ignoreDiscriminator: boolean): ListingAuthor {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'userProfile': !exists(json, 'userProfile') ? undefined : UserProfileFromJSON(json['userProfile']),
    };
}

export function ListingAuthorToJSON(value?: ListingAuthor | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'userProfile': UserProfileToJSON(value.userProfile),
    };
}


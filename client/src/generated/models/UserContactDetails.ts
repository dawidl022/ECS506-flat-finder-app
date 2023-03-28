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
/**
 * 
 * @export
 * @interface UserContactDetails
 */
export interface UserContactDetails {
    /**
     * 
     * @type {string}
     * @memberof UserContactDetails
     */
    phoneNumber: string;
}

/**
 * Check if a given object implements the UserContactDetails interface.
 */
export function instanceOfUserContactDetails(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "phoneNumber" in value;

    return isInstance;
}

export function UserContactDetailsFromJSON(json: any): UserContactDetails {
    return UserContactDetailsFromJSONTyped(json, false);
}

export function UserContactDetailsFromJSONTyped(json: any, ignoreDiscriminator: boolean): UserContactDetails {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'phoneNumber': json['phoneNumber'],
    };
}

export function UserContactDetailsToJSON(value?: UserContactDetails | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'phoneNumber': value.phoneNumber,
    };
}

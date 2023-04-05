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
 * @interface UKAddress
 */
export interface UKAddress {
    /**
     * 
     * @type {string}
     * @memberof UKAddress
     */
    line1: string;
    /**
     * 
     * @type {string}
     * @memberof UKAddress
     */
    line2?: string;
    /**
     * 
     * @type {string}
     * @memberof UKAddress
     */
    town: string;
    /**
     * 
     * @type {string}
     * @memberof UKAddress
     */
    postCode: string;
    /**
     * Lowercase country code
     * @type {string}
     * @memberof UKAddress
     */
    country: string;
}

/**
 * Check if a given object implements the UKAddress interface.
 */
export function instanceOfUKAddress(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "line1" in value;
    isInstance = isInstance && "town" in value;
    isInstance = isInstance && "postCode" in value;
    isInstance = isInstance && "country" in value;

    return isInstance;
}

export function UKAddressFromJSON(json: any): UKAddress {
    return UKAddressFromJSONTyped(json, false);
}

export function UKAddressFromJSONTyped(json: any, ignoreDiscriminator: boolean): UKAddress {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'line1': json['line1'],
        'line2': !exists(json, 'line2') ? undefined : json['line2'],
        'town': json['town'],
        'postCode': json['postCode'],
        'country': json['country'],
    };
}

export function UKAddressToJSON(value?: UKAddress | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'line1': value.line1,
        'line2': value.line2,
        'town': value.town,
        'postCode': value.postCode,
        'country': value.country,
    };
}


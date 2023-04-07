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
 * @interface SeekingFormBase
 */
export interface SeekingFormBase {
    /**
     * 
     * @type {string}
     * @memberof SeekingFormBase
     */
    title: string;
    /**
     * 
     * @type {string}
     * @memberof SeekingFormBase
     */
    description: string;
    /**
     * 
     * @type {string}
     * @memberof SeekingFormBase
     */
    preferredLocation: string;
}

/**
 * Check if a given object implements the SeekingFormBase interface.
 */
export function instanceOfSeekingFormBase(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "title" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "preferredLocation" in value;

    return isInstance;
}

export function SeekingFormBaseFromJSON(json: any): SeekingFormBase {
    return SeekingFormBaseFromJSONTyped(json, false);
}

export function SeekingFormBaseFromJSONTyped(json: any, ignoreDiscriminator: boolean): SeekingFormBase {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'title': json['title'],
        'description': json['description'],
        'preferredLocation': json['preferredLocation'],
    };
}

export function SeekingFormBaseToJSON(value?: SeekingFormBase | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'title': value.title,
        'description': value.description,
        'preferredLocation': value.preferredLocation,
    };
}


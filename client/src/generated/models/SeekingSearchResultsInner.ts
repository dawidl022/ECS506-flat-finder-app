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
import type { SeekingSummary } from './SeekingSummary';
import {
    SeekingSummaryFromJSON,
    SeekingSummaryFromJSONTyped,
    SeekingSummaryToJSON,
} from './SeekingSummary';

/**
 * 
 * @export
 * @interface SeekingSearchResultsInner
 */
export interface SeekingSearchResultsInner {
    /**
     * Listing's distance in km from search location
     * @type {number}
     * @memberof SeekingSearchResultsInner
     */
    distance: number;
    /**
     * Does the listing exist in the user's favourites
     * @type {boolean}
     * @memberof SeekingSearchResultsInner
     */
    isFavourite: boolean;
    /**
     * 
     * @type {SeekingSummary}
     * @memberof SeekingSearchResultsInner
     */
    accommodation?: SeekingSummary;
}

/**
 * Check if a given object implements the SeekingSearchResultsInner interface.
 */
export function instanceOfSeekingSearchResultsInner(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "distance" in value;
    isInstance = isInstance && "isFavourite" in value;

    return isInstance;
}

export function SeekingSearchResultsInnerFromJSON(json: any): SeekingSearchResultsInner {
    return SeekingSearchResultsInnerFromJSONTyped(json, false);
}

export function SeekingSearchResultsInnerFromJSONTyped(json: any, ignoreDiscriminator: boolean): SeekingSearchResultsInner {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'distance': json['distance'],
        'isFavourite': json['isFavourite'],
        'accommodation': !exists(json, 'accommodation') ? undefined : SeekingSummaryFromJSON(json['accommodation']),
    };
}

export function SeekingSearchResultsInnerToJSON(value?: SeekingSearchResultsInner | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'distance': value.distance,
        'isFavourite': value.isFavourite,
        'accommodation': SeekingSummaryToJSON(value.accommodation),
    };
}


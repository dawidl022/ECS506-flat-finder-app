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


import * as runtime from '../runtime';
import type {
  AccommodationDetails,
  AccommodationSearchResultsInner,
  SeekingDetails,
  SeekingSearchResultsInner,
} from '../models';
import {
    AccommodationDetailsFromJSON,
    AccommodationDetailsToJSON,
    AccommodationSearchResultsInnerFromJSON,
    AccommodationSearchResultsInnerToJSON,
    SeekingDetailsFromJSON,
    SeekingDetailsToJSON,
    SeekingSearchResultsInnerFromJSON,
    SeekingSearchResultsInnerToJSON,
} from '../models';

export interface ApiV1ListingsAccommodationGetRequest {
    location: string;
    radius: number;
    maxPrice?: number;
    sources?: Array<string>;
    sortBy?: ApiV1ListingsAccommodationGetSortByEnum;
    page?: number;
    size?: number;
}

export interface ApiV1ListingsAccommodationListingIdGetRequest {
    listingId: string;
}

export interface ApiV1ListingsSeekingGetRequest {
    location: string;
    radius: number;
    page?: number;
    size?: number;
}

export interface ApiV1ListingsSeekingListingIdGetRequest {
    listingId: string;
}

/**
 * 
 */
export class DefaultApi extends runtime.BaseAPI {

    /**
     * Get a list of accommodation listings, optionally filtered and sorted
     */
    async apiV1ListingsAccommodationGetRaw(requestParameters: ApiV1ListingsAccommodationGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<AccommodationSearchResultsInner>>> {
        if (requestParameters.location === null || requestParameters.location === undefined) {
            throw new runtime.RequiredError('location','Required parameter requestParameters.location was null or undefined when calling apiV1ListingsAccommodationGet.');
        }

        if (requestParameters.radius === null || requestParameters.radius === undefined) {
            throw new runtime.RequiredError('radius','Required parameter requestParameters.radius was null or undefined when calling apiV1ListingsAccommodationGet.');
        }

        const queryParameters: any = {};

        if (requestParameters.location !== undefined) {
            queryParameters['location'] = requestParameters.location;
        }

        if (requestParameters.radius !== undefined) {
            queryParameters['radius'] = requestParameters.radius;
        }

        if (requestParameters.maxPrice !== undefined) {
            queryParameters['max_price'] = requestParameters.maxPrice;
        }

        if (requestParameters.sources) {
            queryParameters['sources'] = requestParameters.sources.join(runtime.COLLECTION_FORMATS["csv"]);
        }

        if (requestParameters.sortBy !== undefined) {
            queryParameters['sort_by'] = requestParameters.sortBy;
        }

        if (requestParameters.page !== undefined) {
            queryParameters['page'] = requestParameters.page;
        }

        if (requestParameters.size !== undefined) {
            queryParameters['size'] = requestParameters.size;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/listings/accommodation`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(AccommodationSearchResultsInnerFromJSON));
    }

    /**
     * Get a list of accommodation listings, optionally filtered and sorted
     */
    async apiV1ListingsAccommodationGet(requestParameters: ApiV1ListingsAccommodationGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<AccommodationSearchResultsInner>> {
        const response = await this.apiV1ListingsAccommodationGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get the details of an accommodation listing
     */
    async apiV1ListingsAccommodationListingIdGetRaw(requestParameters: ApiV1ListingsAccommodationListingIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<AccommodationDetails>> {
        if (requestParameters.listingId === null || requestParameters.listingId === undefined) {
            throw new runtime.RequiredError('listingId','Required parameter requestParameters.listingId was null or undefined when calling apiV1ListingsAccommodationListingIdGet.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/listings/accommodation/{listingId}`.replace(`{${"listingId"}}`, encodeURIComponent(String(requestParameters.listingId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => AccommodationDetailsFromJSON(jsonValue));
    }

    /**
     * Get the details of an accommodation listing
     */
    async apiV1ListingsAccommodationListingIdGet(requestParameters: ApiV1ListingsAccommodationListingIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<AccommodationDetails> {
        const response = await this.apiV1ListingsAccommodationListingIdGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get a list of seeking listings
     */
    async apiV1ListingsSeekingGetRaw(requestParameters: ApiV1ListingsSeekingGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<SeekingSearchResultsInner>>> {
        if (requestParameters.location === null || requestParameters.location === undefined) {
            throw new runtime.RequiredError('location','Required parameter requestParameters.location was null or undefined when calling apiV1ListingsSeekingGet.');
        }

        if (requestParameters.radius === null || requestParameters.radius === undefined) {
            throw new runtime.RequiredError('radius','Required parameter requestParameters.radius was null or undefined when calling apiV1ListingsSeekingGet.');
        }

        const queryParameters: any = {};

        if (requestParameters.location !== undefined) {
            queryParameters['location'] = requestParameters.location;
        }

        if (requestParameters.radius !== undefined) {
            queryParameters['radius'] = requestParameters.radius;
        }

        if (requestParameters.page !== undefined) {
            queryParameters['page'] = requestParameters.page;
        }

        if (requestParameters.size !== undefined) {
            queryParameters['size'] = requestParameters.size;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/listings/seeking`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(SeekingSearchResultsInnerFromJSON));
    }

    /**
     * Get a list of seeking listings
     */
    async apiV1ListingsSeekingGet(requestParameters: ApiV1ListingsSeekingGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<SeekingSearchResultsInner>> {
        const response = await this.apiV1ListingsSeekingGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get the details of a seeking listing
     */
    async apiV1ListingsSeekingListingIdGetRaw(requestParameters: ApiV1ListingsSeekingListingIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<SeekingDetails>> {
        if (requestParameters.listingId === null || requestParameters.listingId === undefined) {
            throw new runtime.RequiredError('listingId','Required parameter requestParameters.listingId was null or undefined when calling apiV1ListingsSeekingListingIdGet.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/v1/listings/seeking/{listingId}`.replace(`{${"listingId"}}`, encodeURIComponent(String(requestParameters.listingId))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => SeekingDetailsFromJSON(jsonValue));
    }

    /**
     * Get the details of a seeking listing
     */
    async apiV1ListingsSeekingListingIdGet(requestParameters: ApiV1ListingsSeekingListingIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<SeekingDetails> {
        const response = await this.apiV1ListingsSeekingListingIdGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

}

/**
 * @export
 */
export const ApiV1ListingsAccommodationGetSortByEnum = {
    Newest: 'newest',
    Cheapest: 'cheapest',
    Closest: 'closest'
} as const;
export type ApiV1ListingsAccommodationGetSortByEnum = typeof ApiV1ListingsAccommodationGetSortByEnum[keyof typeof ApiV1ListingsAccommodationGetSortByEnum];
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
 * @interface User
 */
export interface User {
    /**
     * 
     * @type {string}
     * @memberof User
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    email: string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    name?: string;
    /**
     * 
     * @type {boolean}
     * @memberof User
     */
    isAdmin: boolean;
}

/**
 * Check if a given object implements the User interface.
 */
export function instanceOfUser(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "email" in value;
    isInstance = isInstance && "isAdmin" in value;

    return isInstance;
}

export function UserFromJSON(json: any): User {
    return UserFromJSONTyped(json, false);
}

export function UserFromJSONTyped(json: any, ignoreDiscriminator: boolean): User {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'email': json['email'],
        'name': !exists(json, 'name') ? undefined : json['name'],
        'isAdmin': json['isAdmin'],
    };
}

export function UserToJSON(value?: User | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'email': value.email,
        'name': value.name,
        'isAdmin': value.isAdmin,
    };
}


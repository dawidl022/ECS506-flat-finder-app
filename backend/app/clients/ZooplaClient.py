import os
import requests

from enum import StrEnum
from datetime import datetime
from typing import Dict, Union

from app.clients.ListingAPIClient import ListingAPIClient
from app.clients.APIException import *

from app.listings.models import (
    Location, SortBy, ExternalAccommodationListing,
    Coordinates, UKAddress, Source)


class ZooplaOrderBy(StrEnum):
    age = 'age'
    price = 'price'
    price_change = 'price_change'
    view_count = 'view_count'


class ZooplaClient(ListingAPIClient):
    name: str = "Zoopla"
    API_KEY = os.getenv('ZOOPLA_API_KEY')

    def fetch_listing(self, listing_id: str) -> ExternalAccommodationListing | None:
        querystring = {"listing_id": listing_id}

        response = self.submitRequest(querystring)

        if (response['result_count']) == 0:
            return None

        return self.parseListing(response['listing'][0])

    def search_listing(self,
                       area: str,
                       radius: float,
                       order_by: SortBy,
                       page_number: int,
                       page_size: int,
                       maximum_price: int | None = None
                       ) -> list[ExternalAccommodationListing]:
        querystring: Dict[str, Union[str, float, int]] = {
            "area": area,
            "order_by": ZooplaClient.map_order_by(order_by),
            "ordering": "ascending",
            "radius": radius,
            "listing_status": "rent",
            "page_number": page_number,
            "page_size": page_size}

        # if maximum price is given add the query
        if maximum_price is not None:
            querystring["maximum_price"] = maximum_price

        response = self.submitRequest(querystring)

        out = []
        for x in response['listing']:
            out.append(self.parseListing(x))

        return out

    @staticmethod
    def map_order_by(order_by: SortBy) -> ZooplaOrderBy:
        match order_by:
            case SortBy.newest:
                return ZooplaOrderBy.age
            case SortBy.closest:
                # Zoopla does not support sorting by distance
                return ZooplaOrderBy.age
            case SortBy.cheapest:
                return ZooplaOrderBy.price

        raise ValueError("unhandled SortBy enum member")

    @staticmethod
    def submitRequest(querystring):
        url = "https://zoopla.p.rapidapi.com/properties/list"
        headers = {
            "X-RapidAPI-Key": str(ZooplaClient.API_KEY),
            "X-RapidAPI-Host": "zoopla.p.rapidapi.com"
        }

        try:
            response_raw = requests.request(
                "GET", url, headers=headers, params=querystring)
        except requests.exceptions.HTTPError as errh:
            raise APIHTTPError(errh)
        except requests.exceptions.ConnectionError as errc:
            raise APIUnreachableException(errc)
        except requests.exceptions.Timeout as errt:
            raise APIUnreachableException(errt)
        except requests.exceptions.RequestException as err:
            raise APIRequestExecption(err)

        response = response_raw.json()
        # throw execption if API returns an error
        if ('error_code' in response):
            raise APIResponseError(response['error_code'])

        # throw exepction if API returns http 401 or 403,
        # details will be in 'message' field in response
        if (response_raw.status_code == 401 or
                response_raw.status_code == 403):
            raise APIForbiddenError(response['message'])
        return response

    @staticmethod
    def parseListing(x) -> ExternalAccommodationListing:
        listing_id: int = x['listing_id']
        title: str = x['title']
        desc: str = x['description']
        photos: list[str] = x['original_image']
        type: str = x['property_type']
        numRooms: int = x['num_bedrooms']
        price: int = x['rental_prices']['per_month']
        contact: str = x['agent_phone']
        listurl: str = x['details_url']
        created: float = datetime.fromisoformat(x['listing_date']).timestamp()
        lat: float = x['latitude']
        long: float = x['longitude']
        short_desc: str = x['short_description']

        postcode: str = x['outcode'] + " " + x['incode']

        if ('property_number' in x):
            address = UKAddress(
                x['property_number'],
                x['street_name'],
                x['post_town'],
                postcode)
        else:
            address = UKAddress(
                x['street_name'],
                None,
                x['post_town'],
                postcode)

        return ExternalAccommodationListing(
            id=str(listing_id),
            location=Location(Coordinates(
                lat, long), address),
            created_at=created,
            price=price,
            title=title,
            description=desc,
            accommodation_type=type,
            number_of_rooms=numRooms,
            source=Source.zoopla,
            original_listing_url=listurl,
            photo_urls=photos,
            _short_description=short_desc,
            author_phone=contact)

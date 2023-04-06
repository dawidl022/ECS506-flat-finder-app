import os
import requests

from uuid import UUID
from datetime import datetime
from typing import Dict, Union

from app.clients.APIClient import APIClient
from app.clients.APIException import *

from app.listings.models import ExternalAccommodationListing, Location, \
      Coordinates, UKAddress


class ZooplaClient(APIClient):
    name: str = "Zoopla"
    API_KEY = os.getenv('ZOOPLA_API_KEY')

    @staticmethod
    def fetchListing(listing_id: int) -> ExternalAccommodationListing | None:
        url = "https://zoopla.p.rapidapi.com/properties/list"
        querystring = {"listing_id": listing_id}

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
        # throw exepction if API returns a message (usualy for API key error)
        if ('message' in response):
            raise APIKeyError(response['message'])

        if (response['result_count']) == 0:
            return None

        return ZooplaClient.parseListing(response['listing'][0])

    @staticmethod
    def searchListing(area: str,
                      radius: float,
                      order_by: str,
                      page_number: int,
                      page_size: int,
                      maximum_price: int | None = None
                      ) -> list[ExternalAccommodationListing]:
        url = "https://zoopla.p.rapidapi.com/properties/list"
        querystring: Dict[str, Union[str, float, int, None]] = {
            "area": area,
            "order_by": order_by,
            "ordering": "ascending",
            "radius": radius,
            "listing_status": "rent",
            "page_number": page_number,
            "page_size": page_size}

        # if maximum price is given add the query
        if maximum_price is None:
            querystring["maximum_price"] = maximum_price

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
        # throw exepction if API returns a message (usualy for API key error)
        if ('message' in response):
            raise APIKeyError(response['message'])

        out = []
        for x in response['listing']:
            out.append(ZooplaClient.parseListing(x))

        return out

    @staticmethod
    def parseListing(x) -> ExternalAccommodationListing:
        listing_id: int = x['listing_id']
        title: str = x['title']
        desc: str = x['description']
        photos: list[str] = x['original_image']
        type: str = x['property_type']
        numRooms: int = x['num_bedrooms']
        price: int = x['rental_prices']['per_week']
        address: UKAddress = UKAddress(
            x['street_name'], None, x['post_town'], x['outcode']+x['incode'])
        contact: str = x['agent_phone']
        listurl: str = x['details_url']
        created: float = datetime.fromisoformat(x['listing_date']).timestamp()
        lat: float = x['latitude']
        long: float = x['longitude']
        return ExternalAccommodationListing(UUID(),
                                            Location(Coordinates(
                                                lat, long), address),
                                            created,
                                            price,
                                            contact,
                                            title,
                                            desc,
                                            type,
                                            numRooms,
                                            tuple(),
                                            ZooplaClient.name,
                                            listurl,
                                            listing_id,
                                            photos)

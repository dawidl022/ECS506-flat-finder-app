import os
import requests
from typing import Dict, Union

from app.clients.APIClient import APIClient
from app.clients.APIException import *

from app.listings.models import ExternalAccommodationListing, listingContactInfo


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

        title: str = response['listing'][0]['title']
        desc: str = response['listing'][0]['description']
        photos: list[str] = response['listing'][0]['original_image']
        type: str = response['listing'][0]['property_type']
        numRooms: int = response['listing'][0]['num_bedrooms']
        price: int = response['listing'][0]['rental_prices']['per_week']
        address: str = response['listing'][0]['displayable_address']
        contact: listingContactInfo = listingContactInfo(
            response['listing'][0]['agent_phone'], "")
        listurl: str = response['listing'][0]['details_url']
        return ExternalAccommodationListing(listing_id,
                                            title,
                                            desc,
                                            photos,
                                            type,
                                            numRooms,
                                            ZooplaClient.name,
                                            price,
                                            address,
                                            contact,
                                            listurl)

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
            listing_id = x['listing_idlisting_id']
            title: str = x['title']
            desc: str = x['description']
            photos: list[str] = x['original_image']
            type: str = x['property_type']
            numRooms: int = x['num_bedrooms']
            price: int = x['rental_prices']['per_week']
            address: str = x['displayable_address']
            contact: listingContactInfo = listingContactInfo(
                x['agent_phone'], "")
            listurl: str = x['details_url']
            out.append(ExternalAccommodationListing(listing_id,
                                                    title,
                                                    desc,
                                                    photos,
                                                    type,
                                                    numRooms,
                                                    ZooplaClient.name,
                                                    price,
                                                    address,
                                                    contact,
                                                    listurl))

        return out

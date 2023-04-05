import os
import requests
from typing import Dict, Union

from app.clients.APIClient import APIClient
from app.clients.APIException import *

from app.listings.models import ExternalAccommodationListing


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
        except:
            raise APIUnreachableException()

        response = response_raw.json()

        # throw execption if API returns an error
        if ('error_code' in response):
            raise APIResponseError(response['error_code'])
        # throw exepction if API returns a message (usualy for API key error)
        if ('message' in response):
            raise APIKeyError(response['message'])

        if (response['result_count']) == 0:
            return None

        img: str = response['listing'][0]['images'][0]["original"]
        type: str = response['listing'][0]['property_type']
        numrooms: int = response['listing'][0]['num_bedrooms']
        livingConditions: list[str] = [
            response['listing'][0]['furnished_state']]
        amen: list[str] = response['listing'][0]['bullet']
        listurl: str = response['listing'][0]['details_url']
        src: str = ZooplaClient.name
        rating: float = 0.0  # zoopla does not have ratings
        return ExternalAccommodationListing(img, type, numrooms, livingConditions, amen, listurl, src, rating)

    @staticmethod
    def searchListing(area: str, radius: float, order_by: str, page_number: int, page_size: int, maximum_price: int | None = None) -> list[ExternalAccommodationListing]:
        url = "https://zoopla.p.rapidapi.com/properties/list"
        querystring:Dict[str,Union[str,float,int,None]] = {"area": area, "order_by": order_by, "ordering": "ascending",
                       "radius": radius, "listing_status": "rent", "page_number": page_number, "page_size": page_size}

        # if maximum price is given add the query
        if maximum_price != None:
            querystring["maximum_price"] = maximum_price

        headers = {
            "X-RapidAPI-Key": str(ZooplaClient.API_KEY),
            "X-RapidAPI-Host": "zoopla.p.rapidapi.com"
        }

        try:
            response_raw = requests.request(
                "GET", url, headers=headers, params=querystring)
        except:
            raise APIUnreachableException()

        response = response_raw.json()

        # throw execption if API returns an error
        if ('error_code' in response):
            raise APIResponseError(response['error_code'])
        # throw exepction if API returns a message (usualy for API key error)
        if ('message' in response):
            raise APIKeyError(response['message'])

        out = []
        for x in response['listing']:
            img: str = x['images'][0]["original"]
            type: str = x['property_type']
            numrooms: int = x['num_bedrooms']
            livingConditions: list[str] = [x['furnished_state']]
            amen: list[str] = x['bullet']
            listurl: str = x['details_url']
            src: str = ZooplaClient.name
            rating: float = 0.0  # zoopla does not have ratings
            out.append(ExternalAccommodationListing(
                img, type, numrooms, livingConditions, amen, listurl, src, rating))

        return out

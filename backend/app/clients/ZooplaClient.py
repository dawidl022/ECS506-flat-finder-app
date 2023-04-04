import os
import requests

from APIClient import APIClient
from APIException import *

from app.listings.models import ExternalAccommodationListing

class ZooplaClient(APIClient):
    name = "Zoopla"
    API_KEY = os.getenv('ZOOPLA_API_KEY')

    @staticmethod
    def fetchListing(listing_id):
        url = "https://zoopla.p.rapidapi.com/properties/list"
        querystring = {"listing_id": listing_id}

        headers = {
            "X-RapidAPI-Key": ZooplaClient.API_KEY,
            "X-RapidAPI-Host": "zoopla.p.rapidapi.com"
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
        except:
            raise APIUnreachableException()

        response = response.json()

        # throw execption if API returns an error
        if ('error_code' in response):
            raise APIResponseError(response['error_code'])
        # throw exepction if API returns a message (usualy for API key error)
        if ('message' in response):
            raise APIKeyError(response['message'])

        if (response['result_count']) == 0:
            return None

        img = response['listing'][0]['images'][0]["original"]
        type = response['listing'][0]['property_type']
        numrooms = response['listing'][0]['num_bedrooms']
        livingConditions = [response['listing'][0]['furnished_state']]
        amen = response['listing'][0]['bullet']
        listurl = response['listing'][0]['details_url']
        src = ZooplaClient.name
        rating = None  # zoopla does not have ratings
        return ExternalAccommodationListing(img, type, numrooms, livingConditions, amen, listurl, src, rating)

    @staticmethod
    def searchListing(area, radius, order_by, page_number, page_size, maximum_price=0):
        url = "https://zoopla.p.rapidapi.com/properties/list"
        querystring = {"area": area, "order_by": order_by, "ordering": "ascending",
                       "radius": radius, "listing_status": "rent", "page_number": page_number, "page_size": page_size}

        # if maximum price is given add the query
        if maximum_price != 0:
            querystring["maximum_price"] = maximum_price

        headers = {
            "X-RapidAPI-Key": ZooplaClient.API_KEY,
            "X-RapidAPI-Host": "zoopla.p.rapidapi.com"
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
        except:
            raise APIUnreachableException()

        response = response.json()

        # throw execption if API returns an error
        if ('error_code' in response):
            raise APIResponseError(response['error_code'])
        # throw exepction if API returns a message (usualy for API key error)
        if ('message' in response):
            raise APIKeyError(response['message'])
        

        out = []
        for x in response['listing']:
            img = x['images'][0]["original"]
            type = x['property_type']
            numrooms = x['num_bedrooms']
            livingConditions = [x['furnished_state']]
            amen = x['bullet']
            listurl = x['details_url']
            src = ZooplaClient.name
            rating = None  # zoopla does not have ratings
            out.append((img, type, numrooms, livingConditions, amen, listurl, src, rating))

        return out
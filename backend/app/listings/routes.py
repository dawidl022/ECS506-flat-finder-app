from http.client import BAD_REQUEST
from flask import Blueprint, Response, abort, jsonify, make_response, request
from app.util.marshmallow import get_params, get_form
from .models import AccommodationSearchParams
from .service import ListingsService
from .dtos import CreateAccommodationForm

from config import Config

bp = Blueprint("listings", __name__, url_prefix=f"{Config.ROOT}/listings")


@bp.get("/accommodation")
def get_accommodation_listings(listingsService: ListingsService) -> Response:
    params = get_params(AccommodationSearchParams)

    listings = listingsService.search_accommodation_listings()

    return jsonify(listings)


@bp.post("/accommodation")
def create_accommodation_listing(listingService: ListingsService) -> Response:
    form = get_form(CreateAccommodationForm)

    photos = [file.stream.read() for file in request.files.values()]
    if not 1 <= len(photos) <= 15:
        abort(make_response(
            {'photos': "expected between 1 and 15 photos"}, BAD_REQUEST))

    listing = listingService.create_accommodation_listing(
        form, photos, "user@example.com")

    return jsonify(listing)

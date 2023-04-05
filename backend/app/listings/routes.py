from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR
import uuid
from click import UUID

from flask import Blueprint, Response, abort, jsonify, make_response, request

from app.util.marshmallow import get_params, get_form
from app.util.encoding import CamelCaseEncoder
from app.util.encoding import CamelCaseDecoder
from config import Config
from .dtos import CreateAccommodationForm, AccommodationListingDTO
from .models import AccommodationSearchParams, User, ContactDetails
from .service import BaseListingsService

bp = Blueprint("listings", __name__, url_prefix=f"{Config.ROOT}/listings")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder


@bp.get("/accommodation")
def get_accommodation_listings(listings_service: BaseListingsService
                               ) -> Response:
    params = get_params(AccommodationSearchParams)

    listings = listings_service.search_accommodation_listings()

    return jsonify(listings)


@bp.post("/accommodation")
def create_accommodation_listing(listing_service: BaseListingsService
                                 ) -> Response:
    form = get_form(CreateAccommodationForm)

    photos = [file.stream.read() for file in request.files.values()]
    if not 1 <= len(photos) <= 15:
        abort(make_response(
            {'photos': "expected between 1 and 15 photos"}, BAD_REQUEST))

    # TODO fetch user email from JWT token and fetch profile from UserService
    dummy_user = User(
        id=uuid.UUID("7a5a9895-94d1-44f4-a4b8-2bf41da8a81a"),
        email="user@example.com",
        name="Example User",
        contact_details=ContactDetails(
            phone_number="+44 78912 345678",
        )
    )

    listing = listing_service.create_accommodation_listing(
        form, photos, dummy_user.email)

    dto = AccommodationListingDTO(listing, dummy_user)

    return jsonify(dto)


@bp.get("/<listing_id>/photos/<photo_id>")
def get_listing_photo(listing_id: str, photo_id: str):
    # TODO
    pass

from http.client import BAD_REQUEST
import uuid

from flask import Blueprint, Response, abort, jsonify, make_response, request

from app.util.marshmallow import get_params
from app.util.encoding import CamelCaseEncoder
from app.util.encoding import CamelCaseDecoder
from app.util.marshmallow import get_input
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
# @jwt_required()
def create_accommodation_listing(listing_service: BaseListingsService
                                 ) -> Response:
    # in multipart forms, nested fields (like address) are awkwardly placed into
    # files as a JSON string, so we need to extract that
    address_file = request.files.get("address")
    if address_file is None:
        abort(make_response(
            {'address': "missing address field"}, BAD_REQUEST))

    form = get_input(CreateAccommodationForm, request.form |
                     {"address": address_file.stream.read().decode()})

    photos = [file.stream.read()
              for file in request.files.values() if file.name != "address"]
    # if not 1 <= len(photos) <= 15:
    #     abort(make_response(
    #         {'photos': "expected between 1 and 15 photos"}, BAD_REQUEST))

    # current_user_id = get_jwt_identity()
    # current_user_email = current_user_id.get("email")

    # if current_user_email is None:
    #     abort(make_response(
    #         {'token': "invalid bearer token"}, UNAUTHORIZED))

    # TODO fetch profile from UserService
    dummy_user = User(
        id=uuid.UUID("7a5a9895-94d1-44f4-a4b8-2bf41da8a81a"),
        email="dummy@user",
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

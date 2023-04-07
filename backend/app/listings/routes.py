from http.client import (
    BAD_REQUEST, FORBIDDEN, NO_CONTENT, NOT_FOUND, UNAUTHORIZED)
import os
import uuid

from flask import Blueprint, Response, abort, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.datastructures import FileStorage
from app.listings.exceptions import ListingNotFoundError

from app.util.marshmallow import get_params, get_input
from app.util.encoding import CamelCaseEncoder
from app.util.encoding import CamelCaseDecoder
from config import Config
from .models import AccommodationListing, Source
from app.user.user_model import User, ContactDetails
from .dtos import (
    AccommodationSearchResultDTO, CreateAccommodationForm,
    AccommodationListingDTO, AccommodationSearchParams, SearchResult, SourceDTO
)
from .service import BaseListingsService

bp = Blueprint("listings", __name__, url_prefix=f"{Config.ROOT}/listings")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB


def make_dummy_user(user_email: str):
    """
    TODO remove once user service implemented
    """
    dummy_user = User(
        id=uuid.UUID("7a5a9895-94d1-44f4-a4b8-2bf41da8a81a"),
        email=user_email,
        name="Example User",
        contact_details=ContactDetails(
            phone_number="+44 78912 345678",
        )
    )

    return dummy_user


@bp.get("/accommodation")
@jwt_required()
def get_accommodation_listings(listings_service: BaseListingsService
                               ) -> Response:
    params = get_params(AccommodationSearchParams)

    listings = listings_service.search_accommodation_listings(params)
    sources = listings_service.get_available_sources(params.location)

    result = SearchResult(
        sources=[
            SourceDTO(s, enabled=params.sources is None or s in params.sources)
            for s in sources
        ],
        search_results=[
            AccommodationSearchResultDTO(listing)
            for listing in listings
        ]
    )

    return jsonify(result)


@bp.post("/accommodation")
@jwt_required()
def create_accommodation_listing(listing_service: BaseListingsService
                                 ) -> Response:
    form = validate_and_get_create_accommodation_form()
    photos = validate_and_get_uploaded_photos()

    current_user_email = get_current_user_email()

    # TODO fetch profile from UserService
    dummy_user = make_dummy_user(current_user_email)

    listing = listing_service.create_accommodation_listing(
        form, photos, dummy_user.email)

    dto = AccommodationListingDTO(listing, dummy_user)

    return jsonify(dto)


def get_current_user_email():
    """
    get user email from JWT token in header of request
    """
    current_user_id = get_jwt_identity()
    current_user_email = current_user_id.get("email")

    if current_user_email is None:
        abort(make_response(
            {'token': "invalid bearer token"}, UNAUTHORIZED))

    return current_user_email


def validate_and_get_uploaded_photos():
    """
    get uploaded photos and ensure they don't exceed the max file size and
    that a correct number of them have been uploaded
    """
    photo_files = request.files.getlist("photos")

    if not 1 <= len(photo_files) <= 15:
        abort(make_response(
            {'photos': "expected between 1 and 15 photos"}, BAD_REQUEST))

    if any(file_size(file) > MAX_PHOTO_SIZE for file in photo_files):
        abort(make_response(
            {'photos': 'no uploaded photo may exceed 5MB in size'}, 413
        ))

    return [file.stream.read() for file in photo_files]


def validate_and_get_create_accommodation_form():
    """
    in multipart forms, nested fields (like address) are awkwardly placed
    into files as a JSON string, so we need to extract that
    """
    address_file = request.files.get("address")
    if address_file is None:
        abort(make_response(
            {'address': "missing address field"}, BAD_REQUEST))

    form = get_input(CreateAccommodationForm, request.form |
                     {"address": address_file.stream.read().decode()})

    return form


def file_size(file: FileStorage) -> int:
    """
    get the file size of an uploaded file, by seeking though the entire file
    """
    size = file.stream.seek(0, os.SEEK_END)
    file.stream.seek(0, os.SEEK_SET)
    return size


@bp.get("/accommodation/<listing_id>")
@jwt_required()
def get_accommodation_listing(
        listing_id: str, listing_service: BaseListingsService) -> Response:
    source, id = extract_listing_id_and_source(listing_id)

    listing = fetch_accommodation_listing(listing_service, source, id)
    dummy_user = make_dummy_user(get_current_user_email())

    dto = AccommodationListingDTO(listing, dummy_user)
    return jsonify(dto)


def extract_listing_id_and_source(external_listing_id: str
                                  ) -> tuple[Source, str]:
    parts = external_listing_id.split('_')
    if len(parts) != 2:
        abort(make_response(
            {'listingId': "invalid listing id format"}, BAD_REQUEST))

    try:
        source, id = Source(parts[0]), parts[1]
    except ValueError:
        abort(make_response(
            {'listingId': "source not found"}, NOT_FOUND))

    return source, id


def fetch_accommodation_listing(listing_service, source, id
                                ) -> AccommodationListing:
    listing = listing_service.get_accommodation_listing(id, source)
    if listing is None:
        abort(make_response(
            {'listingId': "listing not found"}, NOT_FOUND))

    return listing


@bp.delete("/accommodation/<listing_id>")
@jwt_required()
def delete_accommodation_listing(
        listing_id: str, listing_service: BaseListingsService) -> Response:
    source, id = extract_listing_id_and_source(listing_id)

    if source != Source.internal:
        abort(make_response(
            {'listingId': "cannot delete external listing"}, FORBIDDEN))

    listing = fetch_accommodation_listing(listing_service, source, id)

    if listing.author_email != get_current_user_email():
        abort(make_response(
            {'listingId':
              "currently logged in user is not the author of this listing"},
            FORBIDDEN))

    try:
        listing_service.delete_accommodation_listing(uuid.UUID(id))
    except ListingNotFoundError:
        abort(make_response(
            {'listingId': "listing not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)


@bp.get("/<listing_id>/photos/<photo_id>")
def get_listing_photo(listing_id: str, photo_id: str):
    # TODO
    pass

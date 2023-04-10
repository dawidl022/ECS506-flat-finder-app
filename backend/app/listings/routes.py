from http.client import (
    BAD_REQUEST, FORBIDDEN, NO_CONTENT, NOT_FOUND, SERVICE_UNAVAILABLE)
import os
from typing import cast
import uuid

from flask import Blueprint, Response, abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from werkzeug.datastructures import FileStorage
from app.auth.jwt import get_current_user_email, get_current_user_id
from app.listings.exceptions import ListingNotFoundError, PhotoNotFoundError

from app.util.marshmallow import get_params, get_input
from app.util.encoding import CamelCaseEncoder
from app.util.encoding import CamelCaseDecoder
from app.clients.APIException import APIException
from config import Config
from .models import AccommodationListing, Source
from app.user.user_models import User, ContactDetails
from app.user.user_service import BaseUserService
from .models import AccommodationListing, InternalAccommodationListing, Source

from .dtos import (
    AccommodationForm,
    AccommodationListingDTO,
    AccommodationSearchParams,
    AccommodationSearchResultDTO,
    SearchResultDTO,
    SourceDTO
)
from .service import BaseListingsService

bp = Blueprint("listings", __name__, url_prefix=f"{Config.ROOT}/listings")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB


@bp.get("/accommodation")
@jwt_required()
def get_accommodation_listings(listings_service: BaseListingsService
                               ) -> Response:
    params = get_params(AccommodationSearchParams)

    listings = listings_service.search_accommodation_listings(params)
    sources = listings_service.get_available_sources(params.location)

    result = SearchResultDTO(
        sources=[
            SourceDTO(
                name=str(s),
                enabled=params.sources is None or s in params.sources,
                failed=s in listings.failed_sources
            )
            for s in sources
        ],
        search_results=[
            AccommodationSearchResultDTO(listing)
            for listing in listings.results
        ]
    )

    return jsonify(result)


@bp.post("/accommodation")
@jwt_required()
def create_accommodation_listing(
    listing_service: BaseListingsService,
    user_service: BaseUserService,
) -> Response:
    form = validate_and_get_create_accommodation_form()
    photos = validate_and_get_uploaded_photos()

    user = user_service.get_user(get_current_user_id())
    if user is None:
        abort(make_response({"user": "user no longer registered"}, FORBIDDEN))

    listing = listing_service.create_accommodation_listing(
        form, photos, user.email)

    dto = AccommodationListingDTO(listing, user)

    return jsonify(dto)


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

    form = get_input(AccommodationForm, request.form |
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
        listing_id: str,
        listing_service: BaseListingsService,
        user_service: BaseUserService
) -> Response:
    source, id = extract_listing_id_and_source(listing_id)

    try:
        listing = fetch_accommodation_listing(listing_service, source, id)
    except APIException:
        abort(make_response(
            {"source": f"{source} not available"}, SERVICE_UNAVAILABLE))

    author = get_author(user_service, source, listing)

    dto = AccommodationListingDTO(listing, author)
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


def get_author(user_service, source, listing):
    if source == Source.internal:
        author_email = cast(InternalAccommodationListing, listing).author_email
        author_id = user_service.get_user_id_for_email(author_email)
        author = user_service.get_user(author_id)
    else:
        author = None
    return author


@bp.put("/accommodation/<listing_id>")
@jwt_required()
def put_accommodation_listing(
        listing_id: str,
        listing_service: BaseListingsService,
        user_service: BaseUserService
) -> Response:
    form = validate_and_get_create_accommodation_form()

    listing = get_accommodation_listing_authored_by_current_user(
        listing_id, listing_service, action="update")

    try:
        updated_listing = listing_service.update_accommodation_listing(
            listing.id, form)
    except ListingNotFoundError:
        abort(make_response(
            {'listingId': "listing not found"}, NOT_FOUND))

    author = get_author(user_service, Source.internal, listing)

    return jsonify(AccommodationListingDTO(updated_listing, author))


def get_accommodation_listing_authored_by_current_user(
        listing_id: str, listing_service: BaseListingsService, action: str
) -> InternalAccommodationListing:
    source, id = extract_listing_id_and_source(listing_id)

    if source != Source.internal:
        abort(make_response(
            {'listingId': f"cannot {action} external listing"}, FORBIDDEN))

    listing = cast(InternalAccommodationListing,
                   fetch_accommodation_listing(listing_service, source, id))

    if listing.author_email != get_current_user_email():
        abort(make_response(
            {'listingId':
              "currently logged in user is not the author of this listing"},
            FORBIDDEN))

    return listing


@bp.delete("/accommodation/<listing_id>")
@jwt_required()
def delete_accommodation_listing(
        listing_id: str, listing_service: BaseListingsService) -> Response:
    listing = get_accommodation_listing_authored_by_current_user(
        listing_id, listing_service, action="delete")

    try:
        listing_service.delete_accommodation_listing(listing.id)
    except ListingNotFoundError:
        abort(make_response(
            {'listingId': "listing not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)


@bp.post("/<listing_id>/photos")
@jwt_required()
def upload_listing_photo(listing_id: str, blob: bytes, listing_service: BaseListingsService) -> Response:
    listing = get_accommodation_listing_authored_by_current_user(
        listing_id, listing_service, action="upload photo")

    try:
        listing_service.upload_listing_photo(listing.id, blob)
    except ListingNotFoundError:
        abort(make_response(
            {'listingId': "listing not found"}, NOT_FOUND))

    return make_response()


@bp.get("/<listing_id>/photos/<photo_id>")
@jwt_required()
def get_listing_photo(listing_id: str, photo_id: str, listing_service: BaseListingsService) -> Response:
    # check if user is authenticated
    # get photo and return
    return make_response("", NO_CONTENT)


@bp.delete("/<listing_id>/photos/<photo_id>")
@jwt_required()
def delete_listing_photo(listing_id: str, photo_id: str, listing_service: BaseListingsService) -> Response:
    listing = get_accommodation_listing_authored_by_current_user(
        listing_id, listing_service, action="delete photo")

    try:
        listing_service.delete_listing_photo(listing.id, uuid.UUID(photo_id))
    except ListingNotFoundError:
        abort(make_response(
            {'listingId': "listing not found"}, NOT_FOUND))
    except PhotoNotFoundError:
        abort(make_response(
            {'photo_id': "photo not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)

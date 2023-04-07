from http.client import BAD_REQUEST, NOT_FOUND, OK
from io import BytesIO
import json
import time
from typing import cast
import uuid
from flask.testing import FlaskClient
from app.listings.dtos import CreateAccommodationForm
from app.listings.models import AccommodationListing, Coordinates, Location, Source, UKAddress

from app.listings.service import BaseListingsService


class MockListingService(BaseListingsService):

    def __init__(self) -> None:
        self.saved_photos: list[list[bytes]] = []

    def search_accommodation_listings(self):
        return []

    def create_accommodation_listing(
            self, form: CreateAccommodationForm, photos: list[bytes],
            author_email: str
    ) -> AccommodationListing:
        self.saved_photos.append(photos)
        return model_listing

    def get_accommodation_listing(self, listing_id: str, source: Source
                                  ) -> AccommodationListing | None:
        if source == model_listing.source and listing_id == str(model_listing.id):
            return model_listing
        return None


model_listing = AccommodationListing(
    id=uuid.uuid4(),
    location=Location(
        coords=Coordinates(51.524067, -0.040374),
        address=UKAddress(
            line1="Queen Mary University of London",
            line2="Mile End Road",
            town="London",
            post_code="E1 4NS"
        )
    ),
    created_at=time.time(),
    price=800,
    author_email="user@example.com",
    title="Some random title",
    description="Amazing accommodation!! A great place to stay",
    accommodation_type="Flat",
    number_of_rooms=3,
    photo_ids=(uuid.uuid4(), uuid.uuid4()),
    source=Source.internal)

address = cast(UKAddress, model_listing.location.address)


model_listing_json = {
    "id": "internal/" + str(model_listing.id),
    "title": model_listing.title,
    "description": model_listing.description,
    "photoUrls": [
        f"/api/v1/listings/{model_listing.id}/photos/{id}"
        for id in model_listing.photo_ids
    ],
    "accommodationType": model_listing.accommodation_type,
    "numberOfRooms": model_listing.number_of_rooms,
    "source": "internal",
    "price": model_listing.price,
    "address": {
        "country": "uk",
        "line1": address.line1,
        "line2": address.line2,
        "town": address.town,
        "postCode": address.post_code,
    },
    "author": {
        "name": "Example User",
        "userProfile": {
                "id": "7a5a9895-94d1-44f4-a4b8-2bf41da8a81a",
                "email": "unittest@user.com",
                "name": "Example User",
                "contactDetails": {
                    "phoneNumber": "+44 78912 345678",
                },
        },
    },
    "contactInfo": {
        "email": "unittest@user.com",
        "phoneNumber": "+44 78912 345678",
    }
}


def test_create_accommodation_listing__given_no_request_body__returns_bad_request(client: FlaskClient):
    response = client.post("/api/v1/listings/accommodation")
    assert response.status_code == BAD_REQUEST


def test_create_accommodation_listing__given_no_photos__returns_bad_request(client: FlaskClient):
    response = client.post("/api/v1/listings/accommodation", data={
        "title": model_listing.title,
        "description": model_listing.description,
        "accommodationType": model_listing.accommodation_type,
        "numberOfRooms": str(model_listing.number_of_rooms),
        "price": model_listing.price,
        "address": (BytesIO(json.dumps({
            "country": "uk",
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
        }).encode()), "blob"),
    })
    assert b'{"photos":"expected between 1 and 15 photos"}' in response.data
    assert response.status_code == BAD_REQUEST


def test_create_accommodation_listing__given_no_too_many_photos__returns_bad_request(client: FlaskClient):
    response = client.post("/api/v1/listings/accommodation", data={
        "title": model_listing.title,
        "description": model_listing.description,
        "accommodationType": model_listing.accommodation_type,
        "numberOfRooms": str(model_listing.number_of_rooms),
        "price": model_listing.price,
        "address": (BytesIO(json.dumps({
            "country": "uk",
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
        }).encode()), "blob"),
        "photos": [
            (BytesIO(bytes((i))), f"photo{i}") for i in range(16)
        ]
    })
    assert b'{"photos":"expected between 1 and 15 photos"}' in response.data
    assert response.status_code == BAD_REQUEST


def test_create_accommodation_listing__given_file_exceeds_5MB__returns_listing(client: FlaskClient):
    response = client.post("/api/v1/listings/accommodation", data={
        "title": model_listing.title,
        "description": model_listing.description,
        "accommodationType": model_listing.accommodation_type,
        "numberOfRooms": str(model_listing.number_of_rooms),
        "price": model_listing.price,
        "address": (BytesIO(json.dumps({
            "country": "uk",
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
        }).encode()), "blob"),
        "photos": [
            (BytesIO(bytes(0 for _ in range(5 * 1024 * 1024 + 1))), "big_photo"),
            (BytesIO(bytes((2, 3, 4))), "photo2"),
        ]},
    )

    assert b'{"photos":"no uploaded photo may exceed 5MB in size"}' in response.data
    assert response.status_code == 413


def test_create_accommodation_listing__given_valid_request__returns_listing(client: FlaskClient, listings_service: MockListingService):
    address = cast(UKAddress, model_listing.location.address)
    files = [
        bytes(0 for _ in range(4 * 1024 * 1024 + 1)),
        bytes(1 for _ in range(4 * 1024 * 1024 + 1)),
    ]
    response = client.post("/api/v1/listings/accommodation", data={
        "title": model_listing.title,
        "description": model_listing.description,
        "accommodationType": model_listing.accommodation_type,
        "numberOfRooms": str(model_listing.number_of_rooms),
        "price": model_listing.price,
        "address": (BytesIO(json.dumps({
            "country": "uk",
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
        }).encode()), "blob"),
        "photos": [
            (BytesIO(files[0]), "photo1"),
            (BytesIO(files[1]), "photo2"),
        ]},
    )

    # check response
    assert response.status_code == OK

    assert json.loads(response.data) == model_listing_json

    # check photo files were read by server correctly
    assert len(listings_service.saved_photos[0]) == 2, "not all files saved"
    assert listings_service.saved_photos[0][0] == files[0]
    assert listings_service.saved_photos[0][1] == files[1]


def test_get_accommodation_listing__given_invalid_id_format__returns_bad_request(client: FlaskClient):
    response = client.get("/api/v1/listings/accommodation/whatever")

    assert b'{"listingId":"invalid listing id format"}' in response.data
    assert response.status_code == BAD_REQUEST


def test_get_accommodation_listing__given_invalid_source_returns__returns_not_found(client: FlaskClient):
    response = client.get("/api/v1/listings/accommodation/fake-source_123")

    assert b'{"listingId":"source not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_get_accommodation_listing__given_no_listing_found__returns_not_found(client: FlaskClient):
    response = client.get(
        "/api/v1/listings/accommodation/internal_20f1bdbc-1042-4957-aab9-93462ff97fea")

    assert b'{"listingId":"listing not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_get_accommodation_listing__listing_found__returns_listing(client: FlaskClient):
    response = client.get(
        f"/api/v1/listings/accommodation/internal_{model_listing.id}")
    assert response.status_code == OK
    assert json.loads(response.data) == model_listing_json

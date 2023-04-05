from http.client import BAD_REQUEST, OK
from io import BytesIO
import json
import time
from typing import cast
import uuid
from flask.testing import FlaskClient
from app.listings.dtos import CreateAccommodationForm
from app.listings.models import AccommodationListing, Coordinates, Location, UKAddress

from app.listings.service import BaseListingsService

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
    source="internal")


def test_create_accommodation_listing__given_no_request_body__returns_bad_request(client: FlaskClient):
    response = client.post("/api/v1/listings/accommodation")
    assert response.status_code == BAD_REQUEST


def test_create_accommodation_listing__given_no_files__returns_bad_request(client: FlaskClient):
    address = cast(UKAddress, model_listing.location.address)
    response = client.post("/api/v1/listings/accommodation", data={
        "title": model_listing.title,
        "description": model_listing.description,
        "accommodationType": model_listing.accommodation_type,
        "numberOfRooms": str(model_listing.number_of_rooms),
        "price": model_listing.price,
        "address": json.dumps({
            "country": "uk",
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
        }),
    })
    assert b'{"photos":"expected between 1 and 15 photos"}' in response.data
    assert response.status_code == BAD_REQUEST


def test_create_accommodation_listing__given_valid_request__returns_listing(client: FlaskClient):
    address = cast(UKAddress, model_listing.location.address)
    response = client.post("/api/v1/listings/accommodation", data={
        "title": model_listing.title,
        "description": model_listing.description,
        "accommodationType": model_listing.accommodation_type,
        "numberOfRooms": str(model_listing.number_of_rooms),
        "price": model_listing.price,
        "address": json.dumps({
            "country": "uk",
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
        }),
        "photos": [
            (BytesIO(bytes((1, 2, 3))), "photo1"),
            (BytesIO(bytes((2, 3, 4))), "photo2"),
        ]},
    )
    assert response.status_code == OK
    assert json.loads(response.data) == {
        "id": str(model_listing.id),
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
                "email": "user@example.com",
                "name": "Example User",
                "contactDetails": {
                    "phoneNumber": "+44 78912 345678",
                },
            },
        },
        "contactInfo": {
            "email": "user@example.com",
            "phoneNumber": "+44 78912 345678",
        }
    }


class MockListingService(BaseListingsService):

    def search_accommodation_listings(self):
        return []

    def create_accommodation_listing(
            self, form: CreateAccommodationForm, photos: list[bytes],
            author_email: str
    ) -> AccommodationListing:
        return model_listing

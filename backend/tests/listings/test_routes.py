import dataclasses
from http.client import BAD_REQUEST, FORBIDDEN, NO_CONTENT, NOT_FOUND, OK, SERVICE_UNAVAILABLE
from io import BytesIO
import json
import time
from typing import cast
from unittest.mock import patch
import uuid
from flask.testing import FlaskClient
from app.listings.exceptions import ListingNotFoundError
from app.listings.dtos import AccommodationSearchParams, AccommodationForm, SeekingForm, SeekingSearchParams
from app.listings.models import AccommodationListing, AccommodationSearchResult, AccommodationSummary, Coordinates, ExternalAccommodationListing, InternalAccommodationSummary, ListingSummary, Location, SeekingListing, SeekingSearchResult, Source, UKAddress, InternalAccommodationListing, Photo

from app.listings.service import BaseListingsService, SearchResult
from app.clients.APIException import APIException
from app.listings.service import AccommodationSearchResult
from app.user.user_models import ContactDetails, User


class MockListingService(BaseListingsService):

    def __init__(self) -> None:
        self.saved_photos: list[list[bytes]] = []
        self.deleted_listing_ids: list[uuid.UUID] = []
        self.updated_listings: list[tuple[uuid.UUID, AccommodationForm]] = []
        self.failed_update_listing_id = uuid.uuid4()
        self.api_exception_location = "Antarctica"
        self.api_exception_listing_id = uuid.uuid4()

    def search_accommodation_listings(self, params: AccommodationSearchParams) -> SearchResult:
        if params.location == self.api_exception_location:
            return SearchResult([], {Source.zoopla})
        return SearchResult([model_search_result], set())

    def create_accommodation_listing(
            self, form: AccommodationForm, photos: list[bytes],
            author_email: str
    ) -> AccommodationListing:
        self.saved_photos.append(photos)
        return model_listing

    def get_accommodation_listing(self, listing_id: str, source: Source
                                  ) -> AccommodationListing | None:
        if source == model_listing.source and listing_id == str(model_listing.id):
            return model_listing
        elif source == model_listing.source and listing_id == str(self.failed_update_listing_id):
            return dataclasses.replace(model_listing, id=uuid.UUID(listing_id))
        elif source == Source.zoopla and listing_id == str(self.api_exception_listing_id):
            raise APIException()
        elif source == Source.zoopla and listing_id == model_external_listing.id:
            return model_external_listing
        return None

    def update_accommodation_listing(self, listing_id: uuid.UUID, form: AccommodationForm) -> AccommodationListing:
        self.updated_listings.append((listing_id, form))

        if listing_id == self.failed_update_listing_id:
            raise ListingNotFoundError()

        return dataclasses.replace(model_listing, title="Updated listing")

    def delete_accommodation_listing(self, listing_id: uuid.UUID) -> None:
        duplicate_delete = False
        if listing_id in self.deleted_listing_ids:
            duplicate_delete = True

        self.deleted_listing_ids.append(listing_id)

        if duplicate_delete:
            raise ListingNotFoundError()

    def get_available_sources(self, location_query: str) -> list[Source]:
        return [Source.internal, Source.zoopla]

    def get_listings_authored_by(self, user_email: str
                                 ) -> list[ListingSummary]:
        if user_email == model_listing.author_email:
            return [model_listing_summary]
        return []
    
    def upload_listing_photo(self, listing_id: uuid.UUID, blob: bytes) -> Photo:
        raise NotImplementedError()

    def get_listing_photo(self, listing_id: uuid.UUID, photo_id: uuid.UUID) -> Photo:
        raise NotImplementedError()

    def delete_listing_photo(self, listing_id: uuid.UUID, photo_id: uuid.UUID) -> None:
        raise NotImplementedError()

    def get_seeking_listing(self, listing_id: uuid.UUID) -> SeekingListing | None:
        raise NotImplementedError()

    def create_seeking_listing(self, form: SeekingForm, photos: list[bytes], author_email: str) -> SeekingListing:
        raise NotImplementedError()

    def update_seeking_listing(self, listing_id: uuid.UUID, form: SeekingForm) -> SeekingListing:
        raise NotImplementedError()

    def delete_seeking_listing(self, listing_id: uuid.UUID) -> None:
        raise NotImplementedError()

    def search_seeking_listings(self, params: SeekingSearchParams) -> list[SeekingSearchResult]:
        raise NotImplementedError()


model_listing = InternalAccommodationListing(
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
    author_email="unittest@user.com",
    title="Some random title",
    description="Amazing accommodation!! A great place to stay",
    accommodation_type="Flat",
    number_of_rooms=3,
    photo_ids=(uuid.uuid4(), uuid.uuid4()),
    source=Source.internal)

address = cast(UKAddress, model_listing.location.address)

model_listing_summary = InternalAccommodationSummary(
    id=str(model_listing.id),
    title=model_listing.title,
    short_description=model_listing.description,
    accommodation_type=model_listing.accommodation_type,
    number_of_rooms=model_listing.number_of_rooms,
    source=model_listing.source,
    post_code=cast(UKAddress, model_listing.location.address).post_code,
    thumbnail_id=model_listing.photo_ids[0],
    price=model_listing.price,
)

model_search_result = AccommodationSearchResult(
    distance=10,
    is_favourite=True,
    accommodation=model_listing_summary
)

model_listing_author_name = "Model listing author"
model_listing_author_phone = "+44 77812 713912"
model_listing_author = User(
    id=uuid.uuid4(),
    name=model_listing_author_name,
    email=model_listing.author_email,
    contact_details=ContactDetails(phone_number=model_listing_author_phone)
)


model_external_listing = ExternalAccommodationListing(
    id=str(uuid.uuid4()),
    location=model_listing.location,
    created_at=model_listing.created_at,
    price=model_listing.price,
    author_name=model_listing_author_name,
    author_phone=model_listing_author_phone,
    title="Some random title",
    description="Amazing accommodation!! A great place to stay",
    accommodation_type="Flat",
    number_of_rooms=3,
    photo_urls=[
        "https://fastly.picsum.photos/id/308/1200/1200"
        ".jpg?hmac=2c1705rmBMgsQTZ1I9Uu74cRpA4Fxdl0THWV8wfV5VQ",
        "https://fastly.picsum.photos/id/163/1200/1200"
        ".jpg?hmac=ZOvAYvHz98oGUbqnNC_qldUszdxrzrNdmZjkyxzukt8",
    ],
    source=Source.zoopla,
    original_listing_url="http://example.com",
    _short_description="Stay here"
)

model_listing_json = {
    "id": "internal_" + str(model_listing.id),
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
        "name": model_listing_author.name,
        "userProfile": {
            "id": str(model_listing_author.id),
            "email": model_listing_author.email,
            "name": model_listing_author.name,
            "contactDetails": {
                "phoneNumber": model_listing_author.contact_details.phone_number,
            },
        },
    },
    "contactInfo": {
        "email": model_listing_author.email,
        "phoneNumber": model_listing_author.contact_details.phone_number,
    },
    "originalListingUrl": None
}

model_external_listing_json = {
    "id": "zoopla_" + model_external_listing.id,
    "title": model_external_listing.title,
    "description": model_external_listing.description,
    "photoUrls": model_external_listing.photo_urls,
    "accommodationType": model_external_listing.accommodation_type,
    "numberOfRooms": model_external_listing.number_of_rooms,
    "source": "zoopla",
    "price": model_external_listing.price,
    "address": {
        "country": "uk",
        "line1": address.line1,
        "line2": address.line2,
        "town": address.town,
        "postCode": address.post_code,
    },
    "author": {
        "name": model_external_listing.author_name,
        "userProfile": None,
    },
    "contactInfo": {
        "email": None,
        "phoneNumber": model_external_listing.author_phone,
    },
    "originalListingUrl": model_external_listing.original_listing_url
}

search_results_json = [
    {
        "distance": model_search_result.distance,
        "isFavourite": model_search_result.is_favourite,
        "accommodation": {
            "id": "internal_" + model_listing_summary.id,
            "title": model_listing_summary.title,
            "shortDescription": model_listing_summary.short_description,
            "thumbnailUrl": f"/api/v1/listings/{model_listing_summary.id}/photos/{model_listing.photo_ids[0]}",
            "accommodationType": model_listing_summary.accommodation_type,
            "numberOfRooms": model_listing_summary.number_of_rooms,
            "source": model_listing_summary.source,
            "price": model_listing_summary.price,
            "postCode": model_listing_summary.post_code
        }
    }
]


def update_accommodation_listing_form():
    return {
        "title": "Updated listing",
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
        }).encode()), "blob")
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
    with patch("app.auth.jwt.get_jwt") as mock_get_jwt_local, \
            patch("flask_jwt_extended.utils.get_jwt") as mock_get_jwt_lib:
        return_value = {
            "sub": str(model_listing_author.id),
            "email": model_listing_author.email
        }
        mock_get_jwt_local.return_value = return_value
        mock_get_jwt_lib.return_value = return_value

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


def test_search_accommodation_listing_given_no_params_returns_bad_request(client: FlaskClient):
    response = client.get("/api/v1/listings/accommodation")

    assert response.status_code == BAD_REQUEST


def test_search_accommodation_listing_given_invalid_params__returns_bad_request(client: FlaskClient):
    response = client.get("/api/v1/listings/accommodation?blah=whatever")

    assert response.status_code == BAD_REQUEST


def test_search_accommodation_listing_given_invalid_source__returns_bad_request(client: FlaskClient):
    response = client.get(
        "/api/v1/listings/accommodation?location=London&radius=10&sources=internal,fake")

    assert b'{"sources":["\'fake\' is not a valid Source"]}' in response.data
    assert response.status_code == BAD_REQUEST


def test_search_accommodation_listing_given_valid_source__returns_search_result(client: FlaskClient):
    response = client.get(
        "/api/v1/listings/accommodation?location=London&radius=10&sources=internal")

    assert response.status_code == OK
    assert json.loads(response.data) == {
        "sources": [
            {
                "name": "internal",
                "enabled": True,
                "failed": False,
            },
            {
                "name": "zoopla",
                "enabled": False,
                "failed": False,
            }
        ],
        "searchResults": search_results_json
    }


def test_search_accommodation_listing_given_required_params__returns_search_result(client: FlaskClient):
    response = client.get(
        "/api/v1/listings/accommodation?location=London&radius=10")

    assert response.status_code == OK
    assert json.loads(response.data) == {
        "sources": [
            {
                "name": "internal",
                "enabled": True,
                "failed": False,
            },
            {
                "name": "zoopla",
                "enabled": True,
                "failed": False,
            }
        ],
        "searchResults": search_results_json
    }


def test_search_accommodation_listing_given_api_failed__returns_failed_source(
        client: FlaskClient, listings_service: MockListingService):
    response = client.get(
        f"/api/v1/listings/accommodation?location={listings_service.api_exception_location}&radius=10")

    assert response.status_code == OK
    assert json.loads(response.data) == {
        "sources": [
            {
                "name": "internal",
                "enabled": True,
                "failed": False,
            },
            {
                "name": "zoopla",
                "enabled": True,
                "failed": True,
            }
        ],
        "searchResults": []
    }


def test_search_accommodation_listing_given_all_params__returns_search_result(client: FlaskClient):
    response = client.get(
        "/api/v1/listings/accommodation?location=London&radius=10&sources=internal,zoopla&max_price=1000&sort_by=cheapest&page=2&size=20")

    assert response.status_code == OK
    assert json.loads(response.data) == {
        "sources": [
            {
                "name": "internal",
                "enabled": True,
                "failed": False,
            },
            {
                "name": "zoopla",
                "enabled": True,
                "failed": False,
            }
        ],
        "searchResults": search_results_json
    }


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


def test_get_accommodation_listing__given_api_error__returns_service_unavailable(
        client: FlaskClient, listings_service: MockListingService):
    response = client.get(
        f"/api/v1/listings/accommodation/zoopla_{listings_service.api_exception_listing_id}")

    assert response.status_code == SERVICE_UNAVAILABLE
    assert b'{"source":"zoopla not available"}' in response.data


def test_get_accommodation_listing__given_zoopla_source__returns_zoopla_listing(
        client: FlaskClient, listings_service: MockListingService):
    response = client.get(
        f"/api/v1/listings/accommodation/zoopla_{model_external_listing.id}")
    assert response.status_code == OK
    assert json.loads(response.data) == model_external_listing_json


def test_put_accommodation_listing__given_no_form__returns_bad_request(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put(
        f"/api/v1/listings/accommodation/internal_{model_listing.id}")

    assert response.status_code == BAD_REQUEST
    assert len(listings_service.updated_listings) == 0


def test_update_accommodation_listing__given_invalid_id_format__returns_bad_request(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put("/api/v1/listings/accommodation/whatever",
                          data=update_accommodation_listing_form())

    assert b'{"listingId":"invalid listing id format"}' in response.data
    assert response.status_code == BAD_REQUEST
    assert len(listings_service.updated_listings) == 0


def test_put_accommodation_listing__given_invalid_source_returns__returns_not_found(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put("/api/v1/listings/accommodation/fake-source_123",
                          data=update_accommodation_listing_form())

    assert b'{"listingId":"source not found"}' in response.data
    assert response.status_code == NOT_FOUND
    assert len(listings_service.updated_listings) == 0


def test_put_accommodation_listing__given_no_listing_found__returns_not_found(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put(
        "/api/v1/listings/accommodation/internal_20f1bdbc-1042-4957-aab9-93462ff97fea",
        data=update_accommodation_listing_form()
    )

    assert b'{"listingId":"listing not found"}' in response.data
    assert response.status_code == NOT_FOUND
    assert len(listings_service.updated_listings) == 0


def test_put_accommodation_listing__given_author_mismatch__returns_forbidden(
        client: FlaskClient, listings_service: MockListingService):
    with patch("app.auth.jwt.get_jwt") as mock_get_jwt_identity:
        mock_get_jwt_identity.return_value = {
            "email": "not-the-author@example.com"
        }

        response = client.put(
            f"/api/v1/listings/accommodation/internal_{model_listing.id}",
            data=update_accommodation_listing_form())

        assert response.status_code == FORBIDDEN
        assert b'{"listingId":"currently logged in user is not the author of this listing"}' in response.data
        assert len(listings_service.updated_listings) == 0


def test_put_accommodation_listing__given_form__returns_updates_listing(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put(
        f"/api/v1/listings/accommodation/internal_{model_listing.id}",
        data=update_accommodation_listing_form())

    expected = model_listing_json.copy()
    expected["title"] = "Updated listing"

    assert response.status_code == OK
    assert len(listings_service.updated_listings) == 1
    assert listings_service.updated_listings[0] == (
        model_listing.id, AccommodationForm(
            title="Updated listing",
            description=model_listing.description,
            accommodation_type=model_listing.accommodation_type,
            number_of_rooms=model_listing.number_of_rooms,
            price=model_listing.price,
            address=json.dumps({
                "country": "uk",
                "line1": address.line1,
                "line2": address.line2,
                "town": address.town,
                "post_code": address.post_code,
            })
        ))

    assert json.loads(response.data) == expected


def test_put_accommodation_listing__service_raises_not_found__returns_not_found(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put(
        f"/api/v1/listings/accommodation/internal_{listings_service.failed_update_listing_id}",
        data=update_accommodation_listing_form())

    assert response.status_code == NOT_FOUND
    assert len(listings_service.updated_listings) == 1


def test_put_accommodation_listing__given_external_source_format__returns_forbidden(
        client: FlaskClient, listings_service: MockListingService):
    response = client.put("/api/v1/listings/accommodation/zoopla_123",
                          data=update_accommodation_listing_form())

    assert b'{"listingId":"cannot update external listing"}' in response.data
    assert response.status_code == FORBIDDEN
    assert len(listings_service.updated_listings) == 0


def test_delete_accommodation_listing__given_invalid_id_format__returns_bad_request(
        client: FlaskClient, listings_service: MockListingService):
    response = client.delete("/api/v1/listings/accommodation/whatever")

    assert b'{"listingId":"invalid listing id format"}' in response.data
    assert response.status_code == BAD_REQUEST
    assert len(listings_service.deleted_listing_ids) == 0


def test_delete_accommodation_listing__given_invalid_source_returns__returns_not_found(
        client: FlaskClient, listings_service: MockListingService):
    response = client.delete("/api/v1/listings/accommodation/fake-source_123")

    assert b'{"listingId":"source not found"}' in response.data
    assert response.status_code == NOT_FOUND
    assert len(listings_service.deleted_listing_ids) == 0


def test_delete_accommodation_listing__given_no_listing_found__returns_not_found(
        client: FlaskClient, listings_service: MockListingService):
    response = client.delete(
        "/api/v1/listings/accommodation/internal_20f1bdbc-1042-4957-aab9-93462ff97fea")

    assert b'{"listingId":"listing not found"}' in response.data
    assert response.status_code == NOT_FOUND
    assert len(listings_service.deleted_listing_ids) == 0


def test_delete_accommodation_listing__given_author_mismatch__returns_forbidden(
        client: FlaskClient, listings_service: MockListingService):
    with patch("app.auth.jwt.get_jwt") as mock_get_jwt_identity:
        mock_get_jwt_identity.return_value = {
            "email": "not-the-author@example.com"
        }

        response = client.delete(
            f"/api/v1/listings/accommodation/internal_{model_listing.id}")

        assert response.status_code == FORBIDDEN
        assert b'{"listingId":"currently logged in user is not the author of this listing"}' in response.data
        assert len(listings_service.deleted_listing_ids) == 0


def test_delete_accommodation_listing__given_author_match__returns_no_content(
        client: FlaskClient, listings_service: MockListingService):
    response = client.delete(
        f"/api/v1/listings/accommodation/internal_{model_listing.id}")

    assert response.status_code == NO_CONTENT
    assert len(listings_service.deleted_listing_ids) == 1
    assert listings_service.deleted_listing_ids[0] == model_listing.id


def test_delete_accommodation_listing__service_raises_not_found__returns_not_found(
        client: FlaskClient, listings_service: MockListingService):
    client.delete(
        f"/api/v1/listings/accommodation/internal_{model_listing.id}")
    response = client.delete(
        f"/api/v1/listings/accommodation/internal_{model_listing.id}")

    assert response.status_code == NOT_FOUND
    assert len(listings_service.deleted_listing_ids) == 2
    assert listings_service.deleted_listing_ids[0] == model_listing.id
    assert listings_service.deleted_listing_ids[1] == model_listing.id


def test_delete_accommodation_listing__given_external_source_format__returns_forbidden(
        client: FlaskClient, listings_service: MockListingService):
    response = client.delete("/api/v1/listings/accommodation/zoopla_123")

    assert b'{"listingId":"cannot delete external listing"}' in response.data
    assert response.status_code == FORBIDDEN
    assert len(listings_service.deleted_listing_ids) == 0

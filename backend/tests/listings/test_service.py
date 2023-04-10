import dataclasses
import json
import time
import unittest
from uuid import UUID
import uuid

from app.clients.ListingAPIClient import ListingAPIClient
from app.clients.APIException import APIException

from .test_routes import model_listing, model_listing_summary
from app.listings.exceptions import ListingNotFoundError
from app.listings.models import Address, Coordinates, ExternalAccommodationListing, InternalAccommodationListing, Location, Photo, SeekingListing, SortBy, Source, UKAddress
from app.listings.dtos import AccommodationForm
from app.listings.service import BaseGeocodingService, ListingsService, AccommodationSearchResult, SearchResult
from app.listings.repository import AccommodationListingRepository, ListingPhotoRepository, SeekingListingRepository
from app.listings.models import AccommodationSearchResult, Address, Coordinates, Location, Photo, SortBy, UKAddress
from app.listings.dtos import AccommodationForm, AccommodationSearchParams

from .test_repository import origin_location


expected_coords = Coordinates(51.524067, -0.040374)
expected_search_coords = Coordinates(51.5, 0)
expected_distance = 10


class StubGeocodingService(BaseGeocodingService):
    def get_coords(self, addr: Address) -> Coordinates:
        return expected_coords

    def search_coords(self, location_query: str) -> Coordinates:
        return expected_search_coords

    def calc_distance(self, coords1: Coordinates, coords2: Coordinates) -> float:
        return expected_distance


class SpyAccommodationListingRepo(AccommodationListingRepository):

    def __init__(self) -> None:
        self.saved_listings: list[InternalAccommodationListing] = []
        self.deleted_listing_ids: list[UUID] = []

    def get_listing_by_id(self, listing_id: UUID
                          ) -> InternalAccommodationListing | None:
        if listing_id == model_listing.id:
            return model_listing
        return None

    def delete_listing(self, listing_id: UUID) -> None:
        self.deleted_listing_ids.append(listing_id)
        if listing_id == UUID("634d95f1-8b03-4605-a9e5-38722b907c89"):
            raise ListingNotFoundError()

    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy, page: int,
        size: int, max_price: float | None = None
    ) -> list[InternalAccommodationListing]:
        if coords == expected_search_coords and radius >= 10:
            return [model_listing]
        return []

    def save_listing(self, listing: InternalAccommodationListing) -> None:
        self.saved_listings.append(listing)

    def get_listings_authored_by(self, user_email: str) -> tuple[InternalAccommodationListing, ...]:
        if user_email == model_listing.author_email:
            return model_listing,
        return ()


class StubAccommodationListingRepo(AccommodationListingRepository):
    def __init__(self, listings: list[InternalAccommodationListing]):
        self.listings = {listing.id: listing for listing in listings}

    def get_listing_by_id(self, listing_id: UUID) -> InternalAccommodationListing | None:
        return self.listings.get(listing_id)

    def search_by_location(
            self, coords: Coordinates, radius: float, order_by: SortBy,
            page: int, size: int, max_price: float | None = None
    ) -> list[InternalAccommodationListing]:
        return list(self.listings.values())

    def save_listing(self, listing: InternalAccommodationListing) -> None:
        raise NotImplementedError()

    def delete_listing(self, listing_id: UUID) -> None:
        raise NotImplementedError()

    def get_listings_authored_by(self, user_email: str) -> tuple[InternalAccommodationListing, ...]:
        return ()


class StubSeekingListingRepo(SeekingListingRepository):
    def __init__(self, listings: list[SeekingListing]):
        self.listings = {listing.id: listing for listing in listings}

    def get_listing_by_id(self, listing_id: UUID) -> SeekingListing | None:
        return self.listings.get(listing_id)

    def search_by_location(
            self, coords: Coordinates, radius: float,
            page: int, size: int
    ) -> list[SeekingListing]:
        return list(self.listings.values())

    def save_listing(self, listing: SeekingListing) -> None:
        raise NotImplementedError()

    def delete_listing(self, listing_id: UUID) -> None:
        raise NotImplementedError()

    def get_listings_authored_by(self, user_email: str) -> tuple[SeekingListing, ...]:
        return ()


class StubListingClient(ListingAPIClient):
    def __init__(self, listings: list[ExternalAccommodationListing]):
        self.listings = {str(listing.id): listing for listing in listings}

    def search_listing(
            self, area: str, radius: float, order_by: 'SortBy',
            page_number: int, page_size: int, maximum_price: int | None = None
    ) -> list['ExternalAccommodationListing']:
        return list(self.listings.values())

    def fetch_listing(self, listing_id: str) -> 'ExternalAccommodationListing | None':
        return self.listings.get(listing_id)


class StubExceptionListingClient(ListingAPIClient):

    def search_listing(
            self, area: str, radius: float, order_by: 'SortBy',
            page_number: int, page_size: int, maximum_price: int | None = None
    ) -> list['ExternalAccommodationListing']:
        raise APIException()

    def fetch_listing(self, listing_id: str) -> 'ExternalAccommodationListing | None':
        raise APIException()


class SpyPhotoRepo(ListingPhotoRepository):
    def __init__(self) -> None:
        self.saved_photos: list[list[Photo]] = []

    def get_photo_by_id(self, photo_id: UUID) -> Photo | None:
        raise NotImplementedError()

    def save_photos(self, photos: list[Photo]) -> None:
        self.saved_photos.append(photos)

    def delete_photos(self, photo_ids: list[UUID]) -> None:
        raise NotImplementedError()


class ListingsServiceTest(unittest.TestCase):
    maxDiff = 100000

    address = UKAddress(
        line1="Queen Mary University of London",
        line2="Mile End Road",
        town="London",
        post_code="E1 4NS",
    )

    form = AccommodationForm(
        title="Some random title",
        description="Amazing accommodation!! A great place to stay",
        accommodation_type="Flat",
        number_of_rooms=3,
        price=800,
        address=json.dumps({
            "line1": address.line1,
            "line2": address.line2,
            "town": address.town,
            "post_code": address.post_code,
            "country": "uk"
        })
    )

    def setUp(self) -> None:
        self.spy_accommodation_listing_repo = SpyAccommodationListingRepo()
        self.spy_photo_repo = SpyPhotoRepo()

        self.service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=self.spy_accommodation_listing_repo,
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=self.spy_photo_repo,
            external_sources={}
        )

    def test_create_accommodation_listing__returns_listing_model(self):
        test_start_time = time.time()
        user_email = "test@user.com"
        form = self.form
        actual = self.service.create_accommodation_listing(
            form=form, author_email=user_email,
            photos=[bytes((1, 2, 3)), bytes((2, 3, 4))]
        )
        self.assertIsNotNone(actual.id)
        self.assertEqual(
            Location(coords=expected_coords, address=self.address),
            actual.location
        )
        self.assertTrue(test_start_time <= actual.created_at <= time.time())
        self.assertEqual(form.price, actual.price)
        self.assertEqual(user_email, actual.author_email)
        self.assertEqual(form.title, actual.title)
        self.assertEqual(form.accommodation_type, actual.accommodation_type)
        self.assertEqual(form.number_of_rooms, actual.number_of_rooms)

        self.assertEqual(2, len(actual.photo_ids))
        self.assertIsNotNone(actual.photo_ids[0])
        self.assertIsNotNone(actual.photo_ids[1])

        self.assertEqual("internal", actual.source)

    def test_create_accommodation_listing__saves_listing_to_repo(self):
        actual = self.service.create_accommodation_listing(
            form=self.form, author_email="test@user.com",
            photos=[bytes((1, 2, 3)), bytes((2, 3, 4))]
        )
        self.assertEqual(
            [actual], self.spy_accommodation_listing_repo.saved_listings)

    def test_create_accommodation_listing__saves_photos_to_repo(self):
        photos = [bytes((1, 2, 3)), bytes((2, 3, 4))]
        self.service.create_accommodation_listing(
            form=self.form, author_email="test@user.com", photos=photos
        )
        saved_photos = self.spy_photo_repo.saved_photos

        self.assertEqual(1, len(saved_photos))
        self.assertEqual(photos[0], saved_photos[0][0].blob)
        self.assertEqual(photos[1], saved_photos[0][1].blob)
        self.assertIsNotNone(saved_photos[0][0].id)
        self.assertIsNotNone(saved_photos[0][1].id)

    def test_search_accommodation_listing__given_no_sources__searches_all_repos(self):
        """
        TODO update to search external sources too
        """
        params = AccommodationSearchParams(
            location="London",
            radius=10,
        )
        results = self.service.search_accommodation_listings(params)

        self.assertEqual(SearchResult([
            AccommodationSearchResult(
                distance=expected_distance,
                is_favourite=False,
                accommodation=model_listing_summary,
            )
        ], set()), results)

    def test_search_accommodation_listing__given_internal_source__searches_internal_repo(self):
        params = AccommodationSearchParams(
            location="London",
            radius=10,
            sources="internal"
        )
        results = self.service.search_accommodation_listings(params)

        self.assertEqual(SearchResult([
            AccommodationSearchResult(
                distance=expected_distance,
                is_favourite=False,
                accommodation=model_listing_summary,
            ),
        ], set()), results)

    def test_search_accommodation_listing__given_external_source__uses_client_to_search(self):
        listings = generate_external_listings_with_decreasing_creation_time(2)

        service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=self.spy_accommodation_listing_repo,
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=self.spy_photo_repo,
            external_sources={
                Source.zoopla: StubListingClient(
                    listings
                )
            }
        )
        params = AccommodationSearchParams(
            location="London",
            radius=10,
            sources="zoopla"
        )

        expected = SearchResult([
            AccommodationSearchResult(
                distance=10,
                is_favourite=False,
                accommodation=listing.summarise()
            )
            for listing in listings
        ], set())

        actual = service.search_accommodation_listings(params)

        self.assertEqual(expected, actual)

    def test_search_accommodation_listing__given_external_source_raises_error__adds_source_to_failed(self):
        service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=self.spy_accommodation_listing_repo,
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=self.spy_photo_repo,
            external_sources={
                Source.zoopla: StubExceptionListingClient()
            }
        )
        params = AccommodationSearchParams(
            location="London",
            radius=10,
            sources="zoopla"
        )

        actual = service.search_accommodation_listings(params)

        self.assertEqual(SearchResult(
            [], {Source.zoopla}), actual)

    def test_get_accommodation_listing__given_listing_exists_in_repo__returns_listing(self):
        actual = self.service.get_accommodation_listing(
            str(model_listing.id), Source.internal)
        self.assertEqual(model_listing, actual)

    def test_get_accommodation_listing__given_listing_not_exists_in_repo__returns_none(self):
        actual = self.service.get_accommodation_listing(
            str(uuid.uuid4()), Source.internal)
        self.assertIsNone(actual)

    def test_get_accommodation_listing__given_zoopla_source__returns_listing(self):
        listings = generate_external_listings_with_decreasing_creation_time(1)

        service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=self.spy_accommodation_listing_repo,
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=self.spy_photo_repo,
            external_sources={
                Source.zoopla: StubListingClient(listings)
            }
        )
        expected = listings[0]
        actual = service.get_accommodation_listing(expected.id, Source.zoopla)

        self.assertEqual(expected, actual)

    def test_search_accommodation_listing__given_external_raises_error__raises_error(self):
        service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=self.spy_accommodation_listing_repo,
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=self.spy_photo_repo,
            external_sources={
                Source.zoopla: StubExceptionListingClient()
            }
        )
        self.assertRaises(
            APIException,
            lambda: service.get_accommodation_listing(
                uuid.uuid4(), Source.zoopla
            )
        )

    def test_update_accommodation_listing__given_listing_id__updates_listing(self):
        new_title = "My new amazing title!"
        updated_form = dataclasses.replace(self.form, title=new_title)
        updated_listing = dataclasses.replace(model_listing, title=new_title)

        self.service.update_accommodation_listing(
            model_listing.id, updated_form)

        saved = self.spy_accommodation_listing_repo.saved_listings
        self.assertEqual(1, len(saved))
        self.assertEqual(saved[0], updated_listing)

    def test_update_accommodation_listing__given_listing_id__returns_updated_listing(self):
        new_title = "My new amazing title!"
        new_description = "An updated description"
        new_address_json = json.dumps({
            "line1": "New Street",
            "line2": self.address.line2,
            "town": self.address.town,
            "post_code": self.address.post_code,
            "country": "uk"
        })
        updated_form = dataclasses.replace(
            self.form,
            title=new_title,
            description=new_description,
            address=new_address_json,
            accommodation_type="House",
            number_of_rooms=2,
            price=1200,
        )

        updated_address = dataclasses.replace(
            model_listing.location.address, line1="New Street")
        updated_location = dataclasses.replace(
            model_listing.location, address=updated_address)
        updated_listing = dataclasses.replace(
            model_listing,
            title=new_title,
            description=new_description,
            location=updated_location,
            accommodation_type="House",
            number_of_rooms=2,
            price=1200,
        )

        actual = self.service.update_accommodation_listing(
            model_listing.id, updated_form)

        self.assertEqual(updated_listing, actual)

    def test_update_accommodation_listing__given_listing_not_found__raises_error(self):
        listing_id = uuid.uuid4()
        updated_form = dataclasses.replace(
            self.form, title="My new amazing title!")

        self.assertRaises(
            ListingNotFoundError,
            lambda: self.service.update_accommodation_listing(
                listing_id, updated_form
            )
        )

    def test_delete_accommodation_listing__given_listing_id__deletes_listing(self):
        listing_id = uuid.uuid4()
        self.service.delete_accommodation_listing(listing_id)

        deleted = self.spy_accommodation_listing_repo.deleted_listing_ids
        self.assertEqual(1, len(deleted))
        self.assertEqual(deleted[0], listing_id)

    def test_delete_accommodation_listing__given_listing_not_found__raises_error(self):
        listing_id = UUID("634d95f1-8b03-4605-a9e5-38722b907c89")
        self.assertRaises(ListingNotFoundError,
                          lambda: self.service.delete_accommodation_listing(listing_id))

    def test_get_available_sources__returns_all_sources(self):
        expected = {Source.internal, Source.zoopla}
        actual = self.service.get_available_sources("London")

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected, set(actual))

    def test_get_listings_authored_by__returns_listings(self):
        actual = self.service.get_listings_authored_by(
            model_listing.author_email)
        self.assertEqual([model_listing_summary], actual)


class ListingsServiceSearchTest(unittest.TestCase):
    """
    Collection of tests to test the accumulative search algorithm
    """

    def search(
            self, service: ListingsService, params: AccommodationSearchParams,
            page: int, size: int) -> list[AccommodationSearchResult]:
        return service.search_accommodation_listings(
            dataclasses.replace(params, page=page, size=size)).results

    def test_search__given_all_latest_listings_internal__returns_listings(self):
        external_listings = generate_external_listings_with_decreasing_creation_time(
            10, start_time=time.time()-60)
        internal_listings = generate_internal_listings_with_decreasing_creation_time(
            10)

        service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=StubAccommodationListingRepo(
                internal_listings),
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=SpyPhotoRepo(),
            external_sources={
                Source.zoopla: StubListingClient(external_listings)
            }
        )

        stub_params = AccommodationSearchParams(
            location="London",
            radius=10
        )

        internal_search_results = [AccommodationSearchResult(
            distance=10, is_favourite=False, accommodation=acc.summarise()
        ) for acc in internal_listings]
        external_search_results = [AccommodationSearchResult(
            distance=10, is_favourite=False, accommodation=acc.summarise()
        ) for acc in external_listings]

        self.assertEqual(
            internal_search_results[:5],
            self.search(service, stub_params, page=0, size=5)
        )
        self.assertEqual(
            internal_search_results,
            self.search(service, stub_params, page=0, size=10)
        )
        self.assertEqual(
            internal_search_results + external_search_results[:5],
            self.search(service, stub_params, page=0, size=15)
        )
        self.assertEqual(
            internal_search_results + external_search_results,
            self.search(service, stub_params, page=0, size=20)
        )
        self.assertEqual(
            internal_search_results + external_search_results,
            self.search(service, stub_params, page=0, size=21)
        )
        self.assertEqual(
            internal_search_results[5:],
            self.search(service, stub_params, page=1, size=5)
        )
        self.assertEqual(
            internal_search_results[8:] + external_search_results[:6],
            self.search(service, stub_params, page=1, size=8)
        )
        self.assertEqual(
            external_search_results[:2],
            self.search(service, stub_params, page=5, size=2)
        )
        self.assertEqual(
            external_search_results[:5],
            self.search(service, stub_params, page=2, size=5)
        )
        self.assertEqual(
            external_search_results[5:],
            self.search(service, stub_params, page=3, size=5)
        )
        self.assertEqual(
            [],
            self.search(service, stub_params, page=5, size=5)
        )

    def test_search__listings_intertwined_in_time__returns_listings(self):
        start_time = time.time()
        external_listings = generate_external_listings_with_decreasing_creation_time(
            10, start_time=start_time-1, step=2)
        internal_listings = generate_internal_listings_with_decreasing_creation_time(
            10, start_time=start_time, step=2)

        service = ListingsService(
            geocoder=StubGeocodingService(),
            accommodation_listing_repo=StubAccommodationListingRepo(
                internal_listings),
            seeking_listing_repo=StubSeekingListingRepo([]),
            listing_photo_repo=SpyPhotoRepo(),
            external_sources={
                Source.zoopla: StubListingClient(external_listings)
            }
        )

        stub_params = AccommodationSearchParams(
            location="London",
            radius=10
        )

        expected_order = [
            internal_listings[i // 2]
            if i % 2 == 0 else external_listings[i // 2]
            for i in range(len(external_listings) + len(internal_listings))
        ]

        expected_results = [
            AccommodationSearchResult(
                distance=10, is_favourite=False, accommodation=acc.summarise()
            ) for acc in expected_order
        ]

        self.assertEqual(
            expected_results[:5],
            self.search(service, stub_params, page=0, size=5)
        )
        self.assertEqual(
            expected_results[:10],
            self.search(service, stub_params, page=0, size=10)
        )
        self.assertEqual(
            expected_results[:15],
            self.search(service, stub_params, page=0, size=15)
        )
        self.assertEqual(
            expected_results,
            self.search(service, stub_params, page=0, size=20)
        )
        self.assertEqual(
            expected_results,
            self.search(service, stub_params, page=0, size=21)
        )
        self.assertEqual(
            expected_results[5:10],
            self.search(service, stub_params, page=1, size=5)
        )
        self.assertEqual(
            expected_results[8:16],
            self.search(service, stub_params, page=1, size=8)
        )
        self.assertEqual(
            expected_results[10:12],
            self.search(service, stub_params, page=5, size=2)
        )
        self.assertEqual(
            expected_results[10:15],
            self.search(service, stub_params, page=2, size=5)
        )
        self.assertEqual(
            expected_results[15:],
            self.search(service, stub_params, page=3, size=5)
        )
        self.assertEqual(
            [],
            self.search(service, stub_params, page=4, size=5)
        )


def generate_external_listings_with_decreasing_creation_time(
    n: int,
    start_time=time.time(),
    step=1
) -> list[ExternalAccommodationListing]:
    return [
        ExternalAccommodationListing(
            id=str(uuid.uuid4()),
            location=origin_location,
            created_at=start_time - i * step,
            price=700,
            title=f"Listing {i}",
            description="Some amazing description",
            accommodation_type="Flat",
            number_of_rooms=2,
            source=Source.zoopla,
            original_listing_url="",
            author_phone="+44 78912 345678",
            author_name="External test user",
            photo_urls=[
                "https://fastly.picsum.photos/id/308/1200/1200"
                ".jpg?hmac=2c1705rmBMgsQTZ1I9Uu74cRpA4Fxdl0THWV8wfV5VQ",
            ],
            _short_description="Good flat"
        )
        for i in range(n)
    ]


def generate_internal_listings_with_decreasing_creation_time(
    n: int,
    start_time=time.time(),
    step=1
) -> list[InternalAccommodationListing]:
    return [
        InternalAccommodationListing(
            id=uuid.uuid4(),
            location=origin_location,
            created_at=start_time - i * step,
            price=700,
            title=f"Listing {i}",
            description="Some amazing description",
            accommodation_type="Flat",
            number_of_rooms=2,
            source=Source.internal,
            author_email="unittest@example.com",
            photo_ids=(uuid.uuid4(),),
        )
        for i in range(n)
    ]

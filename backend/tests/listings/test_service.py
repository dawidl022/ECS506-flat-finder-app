from .test_routes import model_listing
from app.listings.models import AccommodationListing, Address, Coordinates, Location, Photo, SortBy, Source, UKAddress
from app.listings.dtos import CreateAccommodationForm
from .test_routes import model_listing, model_listing_summary
from app.listings.service import BaseGeocodingService, ListingsService
from app.listings.repository import AccommodationListingRepository, ListingPhotoRepository
from app.listings.models import AccommodationListing, AccommodationSearchResult, Address, Coordinates, Location, Photo, SortBy, UKAddress
from app.listings.dtos import CreateAccommodationForm, AccommodationSearchParams
import json
import time
import unittest
from uuid import UUID
import uuid

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
        self.saved_listings: list[AccommodationListing] = []

    def get_listing_by_id(self, listing_id: UUID
                          ) -> AccommodationListing | None:
        if listing_id == model_listing.id:
            return model_listing
        return None

    def delete_listing(self, listing_id: UUID) -> None:
        raise NotImplementedError()

    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy, page: int,
        size: int, max_price: float | None = None
    ) -> list[AccommodationListing]:
        if coords == expected_search_coords and radius >= 10:
            return [model_listing]
        return []

    def save_listing(self, listing: AccommodationListing) -> None:
        self.saved_listings.append(listing)


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
        post_code="London E1 4NS",
    )

    form = CreateAccommodationForm(
        title="Some random title",
        description="Amazing accommodation!! A great place to stay",
        accommodation_type="Flat",
        number_of_rooms=3,
        price=700,
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
            listing_photo_repo=self.spy_photo_repo
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

        self.assertEqual([
            AccommodationSearchResult(
                distance=expected_distance,
                is_favourite=False,
                accommodation=model_listing_summary,
            )
        ], results)

    def test_search_accommodation_listing__given_internal_source__searches_internal_repo(self):
        params = AccommodationSearchParams(
            location="London",
            radius=10,
            sources="internal"
        )
        results = self.service.search_accommodation_listings(params)

        self.assertEqual([
            AccommodationSearchResult(
                distance=expected_distance,
                is_favourite=False,
                accommodation=model_listing_summary,
            )
        ], results)

    def test_search_accommodation_listing__given_external_source__uses_client_to_search(self):
        # TODO in #80
        params = AccommodationSearchParams(
            location="London",
            radius=10,
            sources="zoopla"
        )
        results = self.service.search_accommodation_listings(params)

        self.assertEqual([], results)

    def test_get_accommodation_listing__given_listing_exists_in_repo__returns_listing(self):
        actual = self.service.get_accommodation_listing(
            str(model_listing.id), Source.internal)
        self.assertEqual(model_listing, actual)

    def test_get_accommodation_listing__given_listing_not_exists_in_repo__returns_none(self):
        actual = self.service.get_accommodation_listing(
            str(uuid.uuid4()), Source.internal)
        self.assertIsNone(actual)

    def test_get_accommodation_listing__given_zoopla_source__raises_error(self):
        self.assertRaises(ValueError, lambda: self.service.get_accommodation_listing(
            str(model_listing.id), Source.zoopla))

    def test_get_available_sources__returns_all_sources(self):
        expected = {Source.internal, Source.zoopla}
        actual = self.service.get_available_sources("London")

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected, set(actual))

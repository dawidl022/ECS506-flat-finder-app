import json
import time
import unittest
from uuid import UUID

from app.listings.dtos import CreateAccommodationForm
from app.listings.models import AccommodationListing, Address, Coordinates, Location, Photo, SortBy, UKAddress
from app.listings.repository import AccommodationListingRepository, ListingPhotoRepository
from app.listings.service import BaseGeocodingService, ListingsService

expected_coords = Coordinates(51.524067, -0.040374)


class StubGeocodingService(BaseGeocodingService):
    def get_coords(self, addr: Address) -> Coordinates:
        return expected_coords


class SpyAccommodationListingRepo(AccommodationListingRepository):
    def __init__(self) -> None:
        self.saved_listings: list[AccommodationListing] = []

    def get_listing_by_id(self, listing_id: UUID
                          ) -> AccommodationListing | None:
        raise NotImplementedError()

    def delete_listing(self, listing_id: UUID) -> None:
        raise NotImplementedError()

    def search_by_location(
        self, coords: Coordinates, radius: int, order_by: SortBy, page: int,
        size: int, max_price: int | None = None
    ) -> list[AccommodationListing]:
        raise NotImplementedError()

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
        actual = self.service.create_accommodation_listing(
            form=self.form, author_email="test@user.com", photos=photos
        )
        saved_photos = self.spy_photo_repo.saved_photos

        self.assertEqual(1, len(saved_photos))
        self.assertEqual(photos[0], saved_photos[0][0].blob)
        self.assertEqual(photos[1], saved_photos[0][1].blob)
        self.assertIsNotNone(saved_photos[0][0].id)
        self.assertIsNotNone(saved_photos[0][1].id)

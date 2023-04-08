import dataclasses
import time
import unittest
import uuid

from app.listings.exceptions import ListingNotFoundError
from app.listings.models import AccommodationListing, Source, UKAddress
from app.listings.repository import InMemoryAccommodationListingsRepository
from app.listings.models import Coordinates, Location, SortBy

dummy_address = UKAddress(
    line1="Queen Mary University of London",
    line2="Mile End Road",
    town="London",
    post_code="London E1 4NS",
)
origin_location = Location(
    coords=Coordinates(0, 0),
    address=dummy_address
)


class InMemoryAccommodationListingsRepositoryTest(unittest.TestCase):
    """
    TODO extract test logic into abstract base class to test both InMemory
    and Database implementations
    """

    maxDiff = 100000

    def test_get_listings_by_id__given_listing_saved__returns_saved_listing(self):
        repo = InMemoryAccommodationListingsRepository()

        listing_id = uuid.uuid4()
        listing = self.default_accommodation(listing_id)

        repo.save_listing(listing)

        actual_listing = repo.get_listing_by_id(listing_id)

        self.assertEqual(listing, actual_listing)

    def test_get_listings_by_id__given_listing_updated__returns_updated_listing(self):
        repo = InMemoryAccommodationListingsRepository()

        listing_id = uuid.uuid4()
        listing = self.default_accommodation(listing_id)
        updated_listing = dataclasses.replace(
            listing, title="My new amazing title")

        repo.save_listing(listing)
        repo.save_listing(updated_listing)

        actual_listing = repo.get_listing_by_id(listing_id)

        self.assertEqual(updated_listing, actual_listing)

    def test_delete_listing__given_listing_saved__returns_none(self):
        repo = InMemoryAccommodationListingsRepository()

        listing_id = uuid.uuid4()
        listing = self.default_accommodation(listing_id)

        repo.save_listing(listing)
        repo.delete_listing(listing_id)

        self.assertIsNone(repo.get_listing_by_id(listing_id))

    def test_delete_listing__given_no_listing_saved__raises_error(self):
        repo = InMemoryAccommodationListingsRepository()

        listing_id = uuid.uuid4()

        self.assertRaises(ListingNotFoundError,
                          lambda: repo.delete_listing(listing_id))

    def test_search_by_location__given_location_and_radius__returns_listings_within_bounds(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = {
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
        }

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
            self.accommodation_with_coords(51, 2),
            self.accommodation_with_coords(51, 1),
        }

        for listing in listings_within_range | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.newest,
            page=0,
            size=10,
        )

        self.assertEqual(len(listings_within_range), len(actual_listings))
        self.assertEqual(listings_within_range, set(actual_listings))

    def test_search_by_location__given_no_results__returns_empty_list(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_out_of_range = {
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
            self.accommodation_with_coords(0, 0),
            self.accommodation_with_coords(51, 2),
            self.accommodation_with_coords(51, 1),
        }

        for listing in listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=55, long=0),
            radius=50,
            order_by=SortBy.newest,
            page=0,
            size=10,
        )

        self.assertEqual(0, len(actual_listings))

    def test_search_by_location__given_sort_by_newest__returns_sorted_listings(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
            self.accommodation_with_coords(51.25, 0),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.newest,
            page=0,
            size=10,
        )

        self.assertEqual(len(listings_within_range), len(actual_listings))
        self.assertEqual(
            list(reversed(listings_within_range)), actual_listings)

    def test_search_by_location__given_smaller_page_size_than_results__returns_first_page_listings(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
            self.accommodation_with_coords(51.25, 0),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.newest,
            page=0,
            size=2,
        )

        self.assertEqual(2, len(actual_listings))
        self.assertEqual(
            list(reversed(listings_within_range))[:2], actual_listings)

    def test_search_by_location__given_second_page__returns_second_page_listings(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
            self.accommodation_with_coords(51.25, 0),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.newest,
            page=1,
            size=2,
        )

        self.assertEqual(1, len(actual_listings))
        self.assertEqual(
            list(reversed(listings_within_range))[2:], actual_listings)

    def test_search_by_location__given_second_page_empty__returns_empty_list(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
            self.accommodation_with_coords(51.25, 0),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.newest,
            page=1,
            size=10,
        )

        self.assertEqual(0, len(actual_listings))

    def test_search_by_location__given_sort_by_closest__returns_sorted_listings(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0),
            self.accommodation_with_coords(51.25, -0.15),
            self.accommodation_with_coords(51.25, 0.1),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.closest,
            page=0,
            size=10,
        )

        self.assertEqual(len(listings_within_range), len(actual_listings))
        self.assertEqual(listings_within_range[0], actual_listings[0])
        self.assertEqual(listings_within_range[2], actual_listings[1])
        self.assertEqual(listings_within_range[1], actual_listings[2])

    def test_search_by_location__given_sort_by_cheapest__returns_sorted_listings(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0, price=500),
            self.accommodation_with_coords(51.25, 0, price=250),
            self.accommodation_with_coords(51.25, 0.1, price=700),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.cheapest,
            page=0,
            size=10,
        )

        self.assertEqual(len(listings_within_range), len(actual_listings))
        self.assertEqual(listings_within_range[1], actual_listings[0])
        self.assertEqual(listings_within_range[0], actual_listings[1])
        self.assertEqual(listings_within_range[2], actual_listings[2])

    def test_search_by_location__given_max_price__returns_filtered_listings(self):
        repo = InMemoryAccommodationListingsRepository()

        listings_within_range = [
            self.accommodation_with_coords(51.5, 0, price=500),
            self.accommodation_with_coords(51.25, 0, price=250),
            self.accommodation_with_coords(51.25, 0.1, price=700),
        ]

        listings_out_of_range = {
            self.accommodation_with_coords(0, 0),
        }

        for listing in set(listings_within_range) | listings_out_of_range:
            repo.save_listing(listing)

        actual_listings = repo.search_by_location(
            coords=Coordinates(lat=51.5, long=0),
            radius=50,
            order_by=SortBy.cheapest,
            page=0,
            size=10,
            max_price=500
        )

        self.assertEqual(2, len(actual_listings))
        self.assertEqual(listings_within_range[1], actual_listings[0])
        self.assertEqual(listings_within_range[0], actual_listings[1])

    @staticmethod
    def accommodation_with_coords(lat: float, long: float, price: int = 10_000) -> AccommodationListing:
        return AccommodationListing(
            id=uuid.uuid4(),
            location=Location(
                coords=Coordinates(lat=lat, long=long),
                address=dummy_address
            ),
            created_at=time.time(),
            price=price,
            author_email="user@example.com",
            title="Example listing",
            description="Some very interesting description",
            accommodation_type="Flat",
            number_of_rooms=3,
            photo_ids=(),
            source=Source.internal
        )

    @ staticmethod
    def default_accommodation(listing_id: uuid.UUID):
        return AccommodationListing(
            id=listing_id,
            location=origin_location,
            created_at=time.time(),
            price=10_000,
            author_email="user@example.com",
            title="Example listing",
            description="Some very interesting description",
            accommodation_type="Flat",
            number_of_rooms=3,
            photo_ids=(),
            source=Source.internal
        )

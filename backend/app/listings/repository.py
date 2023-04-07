from abc import ABC, abstractmethod
import time
from typing import Callable
from uuid import UUID
from geopy import distance

from .exceptions import ListingNotFoundError
from .models import AccommodationListing, Coordinates, Photo, SortBy


class ListingRepository(ABC):
    @abstractmethod
    def get_listing_by_id(self, listing_id: UUID
                          ) -> AccommodationListing | None:
        pass

    @abstractmethod
    def save_listing(self, listing: AccommodationListing) -> None:
        pass

    @abstractmethod
    def delete_listing(self, listing_id: UUID) -> None:
        pass


class AccommodationListingRepository(ListingRepository, ABC):
    @abstractmethod
    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy,
        page: int, size: int, max_price: float | None = None
    ) -> list[AccommodationListing]:
        pass


class InMemoryAccommodationListingsRepository(AccommodationListingRepository):

    def __init__(self) -> None:
        self.listings: dict[UUID, AccommodationListing] = {}

    def get_listing_by_id(self, listing_id: UUID
                          ) -> AccommodationListing | None:
        return self.listings.get(listing_id)

    def save_listing(self, listing: AccommodationListing) -> None:
        self.listings[listing.id] = listing

    def delete_listing(self, listing_id: UUID) -> None:
        try:
            del self.listings[listing_id]
        except KeyError:
            raise ListingNotFoundError()

    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy, page: int,
        size: int, max_price: float | None = None
    ) -> list[AccommodationListing]:
        return sorted(
            [listing for listing in self.listings.values()
             if distance.distance(coords, listing.location.coords) <= radius
             and (max_price is None or listing.price <= max_price)
             ],
            key=self.sort_key(coords, order_by),
        )[page * size:page * size + size]

    @staticmethod
    def sort_key(coords: Coordinates, sort_by: SortBy
                 ) -> Callable[[AccommodationListing], float]:
        current_time = time.time()

        match sort_by:
            case SortBy.newest:
                return lambda listing: current_time - listing.created_at
            case SortBy.closest:
                return lambda listing: distance.distance(
                    coords, listing.location.coords)
            case SortBy.cheapest:
                return lambda listing: listing.price

        raise ValueError()


class ListingPhotoRepository(ABC):
    @abstractmethod
    def get_photo_by_id(self, photo_id: UUID) -> Photo | None:
        pass

    @abstractmethod
    def save_photos(self, photos: list[Photo]) -> None:
        pass

    @abstractmethod
    def delete_photos(self, photo_ids: list[UUID]) -> None:
        pass


class InMemoryPhotoRepository(ListingPhotoRepository):

    def get_photo_by_id(self, photo_id: UUID) -> Photo | None:
        # TODO
        pass

    def save_photos(self, photos: list[Photo]) -> None:
        # TODO
        pass

    def delete_photos(self, photo_ids: list[UUID]) -> None:
        # TODO
        pass

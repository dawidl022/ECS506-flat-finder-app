from abc import ABC, abstractmethod
from collections import defaultdict
import time
from typing import Callable, TypeVar
from uuid import UUID
from geopy import distance

from .exceptions import ListingNotFoundError
from .models import (
    AccommodationListing, Coordinates, InternalAccommodationListing, Listing,
    Photo, SortBy)


class ListingRepository(ABC):
    @abstractmethod
    def get_listing_by_id(self, listing_id: UUID
                          ) -> InternalAccommodationListing | None:
        pass

    @abstractmethod
    def save_listing(self, listing: InternalAccommodationListing) -> None:
        pass

    @abstractmethod
    def delete_listing(self, listing_id: UUID) -> None:
        pass

    @abstractmethod
    def get_listings_authored_by(self, user_email: str
                                 ) -> tuple[Listing, ...]:
        pass


class AccommodationListingRepository(ListingRepository, ABC):
    @abstractmethod
    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy,
        page: int, size: int, max_price: float | None = None
    ) -> list[InternalAccommodationListing]:
        pass


class InMemoryAccommodationListingsRepository(AccommodationListingRepository):

    def __init__(self) -> None:
        self.listings: dict[UUID, InternalAccommodationListing] = {}
        self.listings_by_author: dict[str, list[InternalAccommodationListing]
                                      ] = defaultdict(list)

    def get_listing_by_id(self, listing_id: UUID
                          ) -> InternalAccommodationListing | None:
        return self.listings.get(listing_id)

    def save_listing(self, listing: InternalAccommodationListing) -> None:
        self.listings[listing.id] = listing
        self.listings_by_author[listing.author_email].append(listing)

    def delete_listing(self, listing_id: UUID) -> None:
        try:
            del self.listings[listing_id]
        except KeyError:
            raise ListingNotFoundError()

    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy, page: int,
        size: int, max_price: float | None = None
    ) -> list[InternalAccommodationListing]:
        return sort_and_page_listings(
            [listing for listing in self.listings.values()
             if distance.distance(coords, listing.location.coords) <= radius
             and (max_price is None or listing.price <= max_price)
             ], coords, order_by, page, size
        )

    def get_listings_authored_by(self, user_email: str
                                 ) -> tuple[InternalAccommodationListing, ...]:
        return tuple(self.listings_by_author.get(user_email, []))


T = TypeVar('T', bound=AccommodationListing)


def sort_and_page_listings(
    listings: list[T], coords: Coordinates, order_by: SortBy,
    page: int, size: int
) -> list[T]:
    return sorted(
        listings, key=sort_key(coords, order_by)
    )[page * size:page * size + size]


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
    @ abstractmethod
    def get_photo_by_id(self, photo_id: UUID) -> Photo | None:
        pass

    @ abstractmethod
    def save_photos(self, photos: list[Photo]) -> None:
        pass

    @ abstractmethod
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

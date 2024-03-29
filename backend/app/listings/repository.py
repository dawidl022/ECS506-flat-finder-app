from abc import ABC, abstractmethod
from collections import defaultdict
import time
from typing import Callable, Generic, TypeVar
from uuid import UUID
from geopy import distance

from .exceptions import ListingNotFoundError, PhotoNotFoundError
from .models import (
    AccommodationListing, Coordinates, InternalAccommodationListing, Listing,
    Photo, SeekingListing, SortBy)


T = TypeVar('T', bound=Listing)


class ListingRepository(ABC, Generic[T]):
    @abstractmethod
    def get_listing_by_id(self, listing_id: UUID
                          ) -> T | None:
        pass

    @abstractmethod
    def save_listing(self, listing: T) -> None:
        pass

    @abstractmethod
    def delete_listing(self, listing_id: UUID) -> None:
        pass

    @abstractmethod
    def get_listings_authored_by(self, user_email: str
                                 ) -> tuple[T, ...]:
        pass


class AccommodationListingRepository(ListingRepository, ABC):
    @abstractmethod
    def get_listing_by_id(self, listing_id: UUID
                          ) -> InternalAccommodationListing | None:
        pass

    @abstractmethod
    def save_listing(self, listing: InternalAccommodationListing) -> None:
        pass

    @abstractmethod
    def get_listings_authored_by(self, user_email: str
                                 ) -> tuple[InternalAccommodationListing, ...]:
        pass

    @abstractmethod
    def search_by_location(
        self, coords: Coordinates, radius: float, order_by: SortBy,
        page: int, size: int, max_price: float | None = None
    ) -> list[InternalAccommodationListing]:
        pass


class SeekingListingRepository(ListingRepository, ABC):
    @abstractmethod
    def get_listing_by_id(self, listing_id: UUID
                          ) -> SeekingListing | None:
        pass

    @abstractmethod
    def save_listing(self, listing: SeekingListing) -> None:
        pass

    @abstractmethod
    def delete_listing(self, listing_id: UUID) -> None:
        pass

    @abstractmethod
    def get_listings_authored_by(self, user_email: str
                                 ) -> tuple[SeekingListing, ...]:
        pass

    @abstractmethod
    def search_by_location(
        self, coords: Coordinates, radius: float, page: int, size: int,
    ) -> list[SeekingListing]:
        pass


class InMemoryAccommodationListingsRepository(AccommodationListingRepository):

    def __init__(self) -> None:
        self.listings: dict[UUID, InternalAccommodationListing] = {}

    def get_listing_by_id(self, listing_id: UUID
                          ) -> InternalAccommodationListing | None:
        return self.listings.get(listing_id)

    def save_listing(self, listing: InternalAccommodationListing) -> None:
        self.listings[listing.id] = listing

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
        return tuple(listing for listing in self.listings.values()
                     if listing.author_email == user_email)


class InMemorySeekingListingsRepository(SeekingListingRepository):
    def __init__(self) -> None:
        self.listings: dict[UUID, SeekingListing] = {}

    def get_listing_by_id(self, listing_id: UUID) -> SeekingListing | None:
        return self.listings.get(listing_id)

    def get_listings_authored_by(self, user_email: str
                                 ) -> tuple[SeekingListing, ...]:
        return tuple(listing for listing in self.listings.values()
                     if listing.author_email == user_email)

    def save_listing(self, listing: SeekingListing) -> None:
        self.listings[listing.id] = listing

    def delete_listing(self, listing_id: UUID) -> None:
        try:
            del self.listings[listing_id]
        except KeyError:
            raise ListingNotFoundError()

    def search_by_location(
            self, coords: Coordinates, radius: float, page: int, size: int
    ) -> list[SeekingListing]:
        return sort_and_page_seeking_listings(
            [listing for listing in self.listings.values()
             if distance.distance(coords, listing.location.coords) <= radius
             ], page, size
        )


TA = TypeVar('TA', bound=AccommodationListing)


def sort_and_page_listings(
    listings: list[TA], coords: Coordinates, order_by: SortBy,
    page: int, size: int
) -> list[TA]:
    return sorted(
        listings, key=sort_key(coords, order_by)
    )[page * size:page * size + size]


def sort_and_page_seeking_listings(
    listings: list[SeekingListing],
    page: int, size: int
) -> list[SeekingListing]:
    return sorted(
        listings, key=lambda listing: time.time() - listing.created_at
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

    def __init__(self) -> None:
        self.photos: dict[UUID, Photo] = {}

    def get_photo_by_id(self, photo_id: UUID) -> Photo | None:
        return self.photos.get(photo_id)

    def save_photos(self, photos: list[Photo]) -> None:
        for photo in photos:
            self.photos[photo.id] = photo

    def delete_photos(self, photo_ids: list[UUID]) -> None:
        for id in photo_ids:
            try:
                del self.photos[id]
            except KeyError:
                raise PhotoNotFoundError()

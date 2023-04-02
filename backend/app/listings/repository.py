from abc import ABC, abstractmethod
import time
from typing import Callable
from uuid import UUID
from geopy import distance

from .exceptions import ListingNotFoundError
from .models import AccommodationListing, Location, SortBy


class ListingRepository(ABC):
    @abstractmethod
    def get_listing_by_id(self, listing_id: UUID) -> AccommodationListing | None:
        pass

    @abstractmethod
    def save_listing(self, listing: AccommodationListing) -> None:
        pass

    @abstractmethod
    def delete_listing(self, listing_id: UUID) -> None:
        pass


class AccommodationListingRepository(ListingRepository, ABC):
    @abstractmethod
    def search_by_location(self, location: Location, radius: int,
                           order_by: SortBy, page: int, size: int,
                           max_price: int | None = None
                           ) -> list[AccommodationListing]:
        pass


class InMemoryAccommodationListingsRepository(AccommodationListingRepository):

    def __init__(self) -> None:
        self.listings: dict[UUID, AccommodationListing] = {}

    def get_listing_by_id(self, listing_id: UUID) -> AccommodationListing | None:
        return self.listings.get(listing_id)

    def save_listing(self, listing: AccommodationListing) -> None:
        self.listings[listing.id] = listing

    def delete_listing(self, listing_id: UUID) -> None:
        try:
            del self.listings[listing_id]
        except KeyError:
            raise ListingNotFoundError()

    def search_by_location(self, location: Location, radius: int,
                           order_by: SortBy, page: int, size: int,
                           max_price: int | None = None
                           ) -> list[AccommodationListing]:
        return sorted(
            [l for l in self.listings.values()
             if distance.distance(location.coords, l.location.coords) <= radius
             and (max_price is None or l.price <= max_price)
             ],
            key=self.sort_key(location, order_by),
        )[page * size:page * size + size]

    @ staticmethod
    def sort_key(location: Location, sort_by: SortBy) -> Callable[[AccommodationListing], float]:
        current_time = time.time()

        match sort_by:
            case SortBy.newest:
                return lambda l: current_time - l.created_at
            case SortBy.closest:
                return lambda l: distance.distance(location.coords, l.location.coords)
            case SortBy.cheapest:
                return lambda l: l.price

        raise ValueError()

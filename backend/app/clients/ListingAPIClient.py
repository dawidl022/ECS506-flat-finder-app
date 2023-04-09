from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.listings.models import ExternalAccommodationListing, SortBy


# abstract APIClient class
class ListingAPIClient(ABC):
    # API identifier, e.g. Zoopla
    name: str

    # returns an AccomodationListing for the given listing_id
    @abstractmethod
    def fetch_listing(self, listing_id: str
                      ) -> 'ExternalAccommodationListing | None':
        pass

    # returns list of AccomodationListing after for a given params
    @abstractmethod
    def search_listing(self,
                       area: str,
                       radius: float,
                       order_by: 'SortBy',
                       page_number: int,
                       page_size: int,
                       maximum_price: int | None = None
                       ) -> list['ExternalAccommodationListing']:
        pass

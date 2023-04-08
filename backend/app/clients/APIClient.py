from abc import ABC,  abstractmethod
from app.listings.models import ExternalAccommodationListing

from app.clients.ZooplaClient import ZooplaOrderBy


# abstract APIClient class
class APIClient(ABC):
    # API identifier, e.g. Zoopla
    name: str = "None"

    # returns an AccomodationListing for the given listing_id
    @staticmethod
    @abstractmethod
    def fetchListing(listing_id: int) -> ExternalAccommodationListing | None:
        return None

    # returns list of AccomodationListing after for a given params
    @staticmethod
    @abstractmethod
    def searchListing(area: str,
                      radius: float,
                      order_by: ZooplaOrderBy,
                      page_number: int,
                      page_size: int,
                      maximum_price: int
                      ) -> list[ExternalAccommodationListing]:
        return []

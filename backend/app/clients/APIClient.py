from app.listings.models import ExternalAccommodationListing

# abstract APIClient class
class APIClient:
    # API identifier, e.g. Zoopla
    name = None

    # returns an AccomodationListing for the given listing_id
    @staticmethod
    def fetchListing(listing_id: int) -> ExternalAccommodationListing:
        pass
    # returns list of AccomodationListing after fetches multiple listings for a given params

    @staticmethod
    def searchListing(area: str, radius: float, order_by: str, page_number: int, page_size: int, maximum_price: int) -> list[ExternalAccommodationListing]:
        pass

    @classmethod
    def getName(cls) -> str:
        return cls.name
        
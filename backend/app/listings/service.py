import abc
import uuid
import time
from app.listings.models import (
    AccommodationSearchResult, Address, Coordinates, Photo, Source)
from app.listings.dtos import (
    CreateAccommodationForm, AccommodationSearchParams)
from app.listings.models import AccommodationListing, Location
from app.listings.repository import (
    AccommodationListingRepository, ListingPhotoRepository)


class BaseGeocodingService(abc.ABC):
    @ abc.abstractmethod
    def get_coords(self, addr: Address) -> Coordinates:
        pass

    @ abc.abstractmethod
    def search_coords(self, location_query: str) -> Coordinates:
        pass

    @ abc.abstractmethod
    def calc_distance(self, c1: Coordinates, c2: Coordinates) -> float:
        pass


class GeocodingService(BaseGeocodingService):
    def get_coords(self, addr: Address) -> Coordinates:
        """
        TODO turn address into coordinates using geopy module
        """
        addr.address
        return Coordinates(0, 0)

    def search_coords(self, location_query: str) -> Coordinates:
        """
        TODO turn address into coordinates using geopy module
        """
        return Coordinates(0, 0)

    def calc_distance(self, c1: Coordinates, c2: Coordinates) -> float:
        """
        TODO calc distance using geopy module
        """
        return 0


class BaseListingsService(abc.ABC):
    @ abc.abstractmethod
    def search_accommodation_listings(self, params: AccommodationSearchParams
                                      ) -> list[AccommodationSearchResult]:
        pass

    @ abc.abstractmethod
    def create_accommodation_listing(
        self, form: CreateAccommodationForm, photos: list[bytes],
        author_email: str
    ) -> AccommodationListing:
        pass

    @ abc.abstractmethod
    def get_accommodation_listing(self, listing_id: str, source: Source
                                  ) -> AccommodationListing | None:
        pass

    @ abc.abstractmethod
    def get_available_sources(self, location_query: str) -> list[Source]:
        pass


class ListingsService(BaseListingsService):

    def __init__(self, geocoder: BaseGeocodingService,
                 accommodation_listing_repo: AccommodationListingRepository,
                 listing_photo_repo: ListingPhotoRepository) -> None:
        self.geocoder = geocoder
        self.accommodation_listing_repo = accommodation_listing_repo
        self.listing_photo_repo = listing_photo_repo

    def search_accommodation_listings(self, params: AccommodationSearchParams
                                      ) -> list[AccommodationSearchResult]:
        coords = self.geocoder.search_coords(params.location)
        listings: list[AccommodationListing] = []
        search_all_sources = params.sources is None

        if search_all_sources or Source.internal in params.sources_list:
            listings += self.accommodation_listing_repo.search_by_location(
                coords=coords,
                radius=params.radius,
                order_by=params.sort_by,
                page=params.page,
                size=params.size,
                max_price=params.max_price
            )

        return [AccommodationSearchResult(
            distance=self.geocoder.calc_distance(coords, acc.location.coords),
            is_favourite=False,
            accommodation=acc.summarise()
        ) for acc in listings]

    def create_accommodation_listing(
            self, form: CreateAccommodationForm, photos: list[bytes],
            author_email: str
    ) -> AccommodationListing:

        listing_photos = [Photo(id=uuid.uuid4(), blob=photo)
                          for photo in photos]

        listing = AccommodationListing(
            id=uuid.uuid4(),
            location=Location(
                coords=self.geocoder.get_coords(form.decoded_address),
                address=form.decoded_address
            ),
            price=form.price,
            created_at=time.time(),
            author_email=author_email,
            title=form.title,
            description=form.description,
            accommodation_type=form.accommodation_type,
            number_of_rooms=form.number_of_rooms,
            photo_ids=tuple(photo.id for photo in listing_photos),
            source=Source.internal
        )

        self.listing_photo_repo.save_photos(listing_photos)
        self.accommodation_listing_repo.save_listing(listing)

        return listing

    def get_accommodation_listing(self, listing_id: str, source: Source
                                  ) -> AccommodationListing | None:
        if source == source.internal:
            id = uuid.UUID(listing_id)
            return self.accommodation_listing_repo.get_listing_by_id(id)

        raise ValueError("Unknown source for accommodation listing")

    def get_available_sources(self, location_query: str) -> list[Source]:
        return [s for s in Source]

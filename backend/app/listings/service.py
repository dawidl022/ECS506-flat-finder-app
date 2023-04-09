import abc
import dataclasses
from typing import NamedTuple
import uuid
import time
from app.listings.exceptions import ListingNotFoundError
from app.listings.models import (
    AccommodationSearchResult, Address, Coordinates,
    InternalAccommodationListing, Photo, Source)
from app.listings.dtos import (
    AccommodationForm, AccommodationSearchParams)
from app.listings.models import AccommodationListing, Location
from app.listings.repository import (
    AccommodationListingRepository, ListingPhotoRepository,
    sort_and_page_listings)
from app.clients.ListingAPIClient import ListingAPIClient
from app.clients.APIException import APIException


class BaseGeocodingService(abc.ABC):
    @abc.abstractmethod
    def get_coords(self, addr: Address) -> Coordinates:
        pass

    @abc.abstractmethod
    def search_coords(self, location_query: str) -> Coordinates:
        pass

    @abc.abstractmethod
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


class SearchResult(NamedTuple):
    results: list[AccommodationSearchResult]
    failed_sources: set[Source]


class BaseListingsService(abc.ABC):
    @abc.abstractmethod
    def search_accommodation_listings(
        self, params: AccommodationSearchParams
    ) -> SearchResult:
        pass

    @abc.abstractmethod
    def create_accommodation_listing(
        self, form: AccommodationForm, photos: list[bytes],
        author_email: str
    ) -> AccommodationListing:
        pass

    @abc.abstractmethod
    def get_accommodation_listing(self, listing_id: str, source: Source
                                  ) -> AccommodationListing | None:
        pass

    @abc.abstractmethod
    def update_accommodation_listing(
        self, listing_id: uuid.UUID, form: AccommodationForm
    ) -> AccommodationListing:
        pass

    @abc.abstractmethod
    def delete_accommodation_listing(self, listing_id: uuid.UUID) -> None:
        pass

    @abc.abstractmethod
    def get_available_sources(self, location_query: str) -> list[Source]:
        pass


class ListingsService(BaseListingsService):

    def __init__(self, geocoder: BaseGeocodingService,
                 accommodation_listing_repo: AccommodationListingRepository,
                 listing_photo_repo: ListingPhotoRepository,
                 external_sources: dict[Source, ListingAPIClient]) -> None:
        self.geocoder = geocoder
        self.accommodation_listing_repo = accommodation_listing_repo
        self.listing_photo_repo = listing_photo_repo
        self.external_sources = external_sources

    def search_accommodation_listings(
        self, params: AccommodationSearchParams
    ) -> SearchResult:
        """
        Naive search algorithm, linear with regards to params.page and
        params.size, i.e. the higher the page, the longer the algorithm takes
        to complete.
        """
        coords = self.geocoder.search_coords(params.location)
        listings: list[AccommodationListing] = []
        search_all_sources = params.sources is None

        if search_all_sources or Source.internal in params.sources_list:
            listings += self.accommodation_listing_repo.search_by_location(
                coords=coords,
                radius=params.radius,
                order_by=params.sort_by,
                page=0,
                size=params.size * (params.page + 1),
                max_price=params.max_price
            )
        failed_sources: set[Source] = set()

        for source in (params.sources_list or self.external_sources):
            source_client = self.external_sources.get(source)
            if source_client is None:
                continue

            # TODO catch api exceptions, return sources that threw exception
            # so frontend can display that these were skipped
            try:
                listings += source_client.search_listing(
                    area=params.location,
                    radius=params.radius,
                    order_by=params.sort_by,
                    page_number=0,
                    page_size=params.size * (params.page + 1),
                    maximum_price=int(
                        params.max_price) if params.max_price is not None else None
                )
            except APIException:
                failed_sources.add(source)

        sorted = sort_and_page_listings(
            listings, coords, params.sort_by,
            page=params.page, size=params.size
        )

        return SearchResult([AccommodationSearchResult(
            distance=self.geocoder.calc_distance(coords, acc.location.coords),
            is_favourite=False,  # favourites not currently supported
            accommodation=acc.summarise()
        ) for acc in sorted], failed_sources)

    def create_accommodation_listing(
            self, form: AccommodationForm, photos: list[bytes],
            author_email: str
    ) -> AccommodationListing:

        listing_photos = [Photo(id=uuid.uuid4(), blob=photo)
                          for photo in photos]

        listing = InternalAccommodationListing(
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
        if source in self.external_sources:
            return self.external_sources[source].fetch_listing(listing_id)

        raise ValueError("Unknown source for accommodation listing")

    def update_accommodation_listing(
        self, listing_id: uuid.UUID, form: AccommodationForm
    ) -> AccommodationListing:
        listing = self.accommodation_listing_repo.get_listing_by_id(listing_id)

        if listing is None:
            raise ListingNotFoundError()

        updated_listing = dataclasses.replace(
            listing,
            **form.to_dict(),
            location=dataclasses.replace(
                listing.location, address=form.decoded_address)
        )

        self.accommodation_listing_repo.save_listing(updated_listing)

        return updated_listing

    def delete_accommodation_listing(self, listing_id: uuid.UUID) -> None:
        self.accommodation_listing_repo.delete_listing(listing_id)

    def get_available_sources(self, location_query: str) -> list[Source]:
        return [s for s in Source]

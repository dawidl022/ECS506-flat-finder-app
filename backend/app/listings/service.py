import abc
import dataclasses
from typing import NamedTuple
import uuid
import time
from app.listings.exceptions import ListingNotFoundError, PhotoNotFoundError
from app.listings.models import (
    AccommodationSearchResult, Address, AddressFreeLocation, Coordinates,
    InternalAccommodationListing, ListingSummary, Photo, SeekingListing,
    SeekingSearchResult, Source)
from app.listings.dtos import (
    AccommodationForm, AccommodationSearchParams, SeekingForm,
    SeekingSearchParams)
from app.listings.models import AccommodationListing, Location
from app.listings.repository import (
    AccommodationListingRepository, ListingPhotoRepository,
    SeekingListingRepository, sort_and_page_listings)
from app.clients.ListingAPIClient import ListingAPIClient
from app.clients.APIException import APIException
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from app.listings.dtos import EditAccommodationForm
from backend.app.listings.models import AccommodationSummary


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
        geolocator = Nominatim(user_agent="flatfinder-app")
        location = geolocator.geocode(addr.full_address)
        return Coordinates(0, 0)

    def search_coords(self, location_query: str) -> Coordinates:
        """
        TODO turn address into coordinates using geopy module
        """
        geolocator = Nominatim(user_agent="flatfinder-app")
        location = geolocator.geocode(location_query)
        return Coordinates(0, 0)

    def calc_distance(self, c1: Coordinates, c2: Coordinates) -> float:
        """
        TODO calc distance using geopy module
        """
        distance = geodesic(c1, c2).km
        return distance


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

    @abc.abstractmethod
    def get_listings_authored_by(self, user_email: str
                                 ) -> list[ListingSummary]:
        pass

    @abc.abstractmethod
    def search_seeking_listings(
        self, params: SeekingSearchParams
    ) -> list[SeekingSearchResult]:
        pass

    @abc.abstractmethod
    def create_seeking_listing(
        self, form: SeekingForm, photos: list[bytes],
        author_email: str
    ) -> SeekingListing:
        pass

    @abc.abstractmethod
    def get_seeking_listing(self, listing_id: uuid.UUID
                            ) -> SeekingListing | None:
        pass

    @abc.abstractmethod
    def update_seeking_listing(
        self, listing_id: uuid.UUID, form: SeekingForm
    ) -> SeekingListing:
        pass

    @abc.abstractmethod
    def delete_seeking_listing(self, listing_id: uuid.UUID) -> None:
        pass

    @abc.abstractmethod
    def upload_listing_photo(self, listing_id: uuid.UUID,
                             blob: bytes
                             ) -> Photo:
        pass

    @abc.abstractmethod
    def get_listing_photo(self, listing_id: uuid.UUID,
                          photo_id: uuid.UUID
                          ) -> Photo:
        pass

    @abc.abstractmethod
    def delete_listing_photo(self, listing_id: uuid.UUID,
                             photo_id: uuid.UUID
                             ) -> None:
        pass


class ListingsCleanupService(abc.ABC):
    """
    Interface Segregation Principle in action: UserService only depends on one
    method of the ListingsService, so it should not depend on any other method
    implemented by ListingsService
    """

    @abc.abstractmethod
    def delete_listings_authored_by(self, user_email: str):
        pass


class ListingsService(BaseListingsService, ListingsCleanupService):

    def __init__(self, geocoder: BaseGeocodingService,
                 accommodation_listing_repo: AccommodationListingRepository,
                 seeking_listing_repo: SeekingListingRepository,
                 listing_photo_repo: ListingPhotoRepository,
                 external_sources: dict[Source, ListingAPIClient]) -> None:
        self.geocoder = geocoder
        self.accommodation_listing_repo = accommodation_listing_repo
        self.seeking_listing_repo = seeking_listing_repo
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

            try:
                listings += source_client.search_listing(
                    area=params.location,
                    radius=params.radius,
                    order_by=params.sort_by,
                    page_number=0,
                    page_size=params.size * (params.page + 1),
                    maximum_price=int(
                        params.max_price
                    ) if params.max_price is not None else None
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
        self, listing_id: uuid.UUID, form: EditAccommodationForm
    ) -> AccommodationListing:
        listing = self.accommodation_listing_repo.get_listing_by_id(listing_id)

        if listing is None:
            raise ListingNotFoundError()

        updated_listing = dataclasses.replace(
            listing,
            **form.to_dict(),
            location=Location(
                coords=self.geocoder.get_coords(form.decoded_address),
                address=form.decoded_address
            )
        )

        self.accommodation_listing_repo.save_listing(updated_listing)

        return updated_listing

    def delete_accommodation_listing(self, listing_id: uuid.UUID) -> None:
        self.accommodation_listing_repo.delete_listing(listing_id)

    def get_available_sources(self, location_query: str) -> list[Source]:
        return [s for s in Source]

    def get_listings_authored_by(self, user_email: str
                                 ) -> list[ListingSummary]:
        return [
            listing.summarise()
            for listing in
            self.accommodation_listing_repo.get_listings_authored_by(
                user_email
            ) + self.seeking_listing_repo.get_listings_authored_by(
                user_email
            )
        ]

    def search_seeking_listings(
        self, params: SeekingSearchParams
    ) -> list[SeekingSearchResult]:
        coords = self.geocoder.search_coords(params.location)
        listings = self.seeking_listing_repo.search_by_location(
            coords=coords,
            radius=params.radius,
            page=params.page,
            size=params.size
        )

        return [SeekingSearchResult(
            distance=self.geocoder.calc_distance(
                coords, seeking.location.coords),
            is_favourite=False,  # favourites not currently supported
            seeking=seeking.summarise()
        ) for seeking in listings]

    def create_seeking_listing(
        self, form: SeekingForm, photos: list[bytes],
        author_email: str
    ) -> SeekingListing:
        listing_photos = [Photo(id=uuid.uuid4(), blob=photo)
                          for photo in photos]

        # TODO what happens when this fails due to garbage input?
        coords = self.geocoder.search_coords(form.preferred_location)

        listing = SeekingListing(
            id=uuid.uuid4(),
            location=AddressFreeLocation(
                coords=coords,
                name=form.preferred_location
            ),
            created_at=time.time(),
            author_email=author_email,
            title=form.title,
            description=form.description,
            photo_ids=tuple(photo.id for photo in listing_photos),
        )

        self.listing_photo_repo.save_photos(listing_photos)
        self.seeking_listing_repo.save_listing(listing)

        return listing

    def get_seeking_listing(self, listing_id: uuid.UUID
                            ) -> SeekingListing | None:
        return self.seeking_listing_repo.get_listing_by_id(listing_id)

    def update_seeking_listing(
        self, listing_id: uuid.UUID, form: SeekingForm
    ) -> SeekingListing:
        listing = self.seeking_listing_repo.get_listing_by_id(listing_id)

        if listing is None:
            raise ListingNotFoundError()

        # TODO what happens when this fails due to garbage input?
        coords = self.geocoder.search_coords(form.preferred_location)

        updated_listing = dataclasses.replace(
            listing,
            title=form.title,
            description=form.description,
            location=AddressFreeLocation(
                coords=coords,
                name=form.preferred_location,
            )
        )

        self.seeking_listing_repo.save_listing(updated_listing)

        return updated_listing

    def delete_seeking_listing(self, listing_id: uuid.UUID) -> None:
        self.seeking_listing_repo.delete_listing(listing_id)

    def delete_listings_authored_by(self, user_email: str) -> None:
        user_listings = self.get_listings_authored_by(user_email)

        for listing in user_listings:
            try:
                if isinstance(listing, AccommodationSummary):
                    self.delete_accommodation_listing(listing.id)

                elif isinstance(listing, SeekingListing):
                    self.delete_seeking_listing(listing.id)
            except ListingNotFoundError:
                pass

    def upload_listing_photo(self, listing_id: uuid.UUID,
                             blob: bytes
                             ) -> Photo:
        # get listing if exists
        listing = self.accommodation_listing_repo.get_listing_by_id(listing_id)
        if listing is None:
            raise ListingNotFoundError()

        # create photo object and save to photo repo
        photo = Photo(uuid.uuid4(), blob)
        self.listing_photo_repo.save_photos([photo])

        # update listing by adding the photo to it
        updated_listing = dataclasses.replace(
            listing,
            photo_ids=tuple(list(listing.photo_ids) + [photo.id])
        )
        self.accommodation_listing_repo.save_listing(updated_listing)
        return photo

    def get_listing_photo(self, listing_id: uuid.UUID,
                          photo_id: uuid.UUID
                          ) -> Photo:
        # get listing if exists
        listing = self.accommodation_listing_repo.get_listing_by_id(listing_id)
        if listing is None:
            raise ListingNotFoundError()

        # check if photo is part of this listing
        if photo_id not in listing.photo_ids:
            raise PhotoNotFoundError()

        # get photo from photo repo
        photo = self.listing_photo_repo.get_photo_by_id(photo_id)
        if photo is None:
            raise PhotoNotFoundError()

        return photo

    def delete_listing_photo(self, listing_id: uuid.UUID,
                             photo_id: uuid.UUID
                             ) -> None:
        # get listing if exists
        listing = self.accommodation_listing_repo.get_listing_by_id(listing_id)
        if listing is None:
            raise ListingNotFoundError()

        # check if photo is part of this listing
        if photo_id not in listing.photo_ids:
            raise PhotoNotFoundError()

        # delete photo if exists for that listing
        self.listing_photo_repo.delete_photos([photo_id])

        # then update the listing by removing the photo from photo_ids
        new_photo_ids = list(listing.photo_ids)
        new_photo_ids.remove(photo_id)
        updated_listing = dataclasses.replace(
            listing,
            photo_ids=tuple(new_photo_ids)
        )
        self.accommodation_listing_repo.save_listing(updated_listing)

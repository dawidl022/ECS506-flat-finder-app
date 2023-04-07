import abc
import uuid
import time
from app.listings.models import (
    AccommodationSearchResult, AccommodationSummary, Address, Coordinates,
    Photo, Source)
from app.listings.dtos import CreateAccommodationForm
from app.listings.models import AccommodationListing, Location
from app.listings.repository import (
    AccommodationListingRepository, ListingPhotoRepository)


class BaseGeocodingService(abc.ABC):
    @abc.abstractmethod
    def get_coords(self, addr: Address) -> Coordinates:
        pass


class GeocodingService(BaseGeocodingService):
    def get_coords(self, addr: Address) -> Coordinates:
        """
        TODO turn address into coordinates using geopy module
        """
        addr.address
        return Coordinates(0, 0)


class BaseListingsService(abc.ABC):
    @abc.abstractmethod
    def search_accommodation_listings(self) -> list[AccommodationSearchResult]:
        pass

    @abc.abstractmethod
    def create_accommodation_listing(
        self, form: CreateAccommodationForm, photos: list[bytes],
        author_email: str
    ) -> AccommodationListing:
        pass

    @abc.abstractmethod
    def get_accommodation_listing(self, listing_id: str, source: Source
                                  ) -> AccommodationListing | None:
        pass

    @abc.abstractmethod
    def delete_accommodation_listing(self, listing_id: uuid.UUID) -> None:
        pass


class ListingsService(BaseListingsService):

    def __init__(self, geocoder: BaseGeocodingService,
                 accommodation_listing_repo: AccommodationListingRepository,
                 listing_photo_repo: ListingPhotoRepository) -> None:
        self.geocoder = geocoder
        self.accommodation_listing_repo = accommodation_listing_repo
        self.listing_photo_repo = listing_photo_repo

    def search_accommodation_listings(self) -> list[AccommodationSearchResult]:
        """
        TODO take filters as parameters
        TODO implement business logic
        :returns stub response
        """
        thumbnail_urls = [
            "https://fastly.picsum.photos/id/308/1200/1200"
            ".jpg?hmac=2c1705rmBMgsQTZ1I9Uu74cRpA4Fxdl0THWV8wfV5VQ",
            "https://fastly.picsum.photos/id/163/1200/1200"
            ".jpg?hmac=ZOvAYvHz98oGUbqnNC_qldUszdxrzrNdmZjkyxzukt8",
        ]
        return [
            AccommodationSearchResult(
                distance=1.2,
                is_favourite=True,
                accommodation=AccommodationSummary(
                    id="internal-1",
                    title="Flat",
                    short_description="Very nice beautiful flat to live in",
                    thumbnail_url=thumbnail_urls[0],
                    accommodation_type="flat",
                    number_of_rooms=2,
                    source="internal",
                    price=1020,
                    post_code="EA1 7UP"
                )
            ),
            AccommodationSearchResult(
                distance=1.2,
                is_favourite=False,
                accommodation=AccommodationSummary(
                    id="zoopla-1",
                    title="Room",
                    short_description="A small cozy room perfect for students",
                    thumbnail_url=thumbnail_urls[1],
                    accommodation_type="room",
                    number_of_rooms=1,
                    source="zoopla",
                    price=455.50,
                    post_code="ZO1 8N"
                )
            )
        ]

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

    def delete_accommodation_listing(self, listing_id: uuid.UUID) -> None:
        self.accommodation_listing_repo.delete_listing(listing_id)

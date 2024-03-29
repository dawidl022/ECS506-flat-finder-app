import abc
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import NamedTuple
from uuid import UUID

from flask import url_for


class SortBy(StrEnum):
    newest = auto(),
    cheapest = auto(),
    closest = auto()


class Source(StrEnum):
    internal = auto()
    zoopla = auto()


class ListingType(StrEnum):
    seeking = auto()
    accommodation = auto()


@dataclass(frozen=True)
class ListingSummary(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def listing_type(cls) -> ListingType:
        pass


@dataclass(frozen=True)
class AccommodationSummary(ListingSummary, abc.ABC):
    id: str
    title: str
    short_description: str
    accommodation_type: str
    number_of_rooms: int
    source: Source
    price: float
    post_code: str

    @classmethod
    def listing_type(cls) -> ListingType:
        return ListingType.accommodation


@dataclass(frozen=True)
class SeekingSummary(ListingSummary):
    id: UUID
    title: str
    short_description: str
    thumbnail_id: UUID | None
    location_name: str

    @classmethod
    def listing_type(cls) -> ListingType:
        return ListingType.seeking


@dataclass(frozen=True)
class InternalAccommodationSummary(AccommodationSummary):
    thumbnail_id: UUID


@dataclass(frozen=True)
class ExternalAccommodationSummary(AccommodationSummary):
    thumbnail_url: str | None


@dataclass(frozen=True)
class AccommodationSearchResult:
    distance: float
    is_favourite: bool
    accommodation: AccommodationSummary


@dataclass(frozen=True)
class SeekingSearchResult:
    distance: float
    is_favourite: bool
    seeking: SeekingSummary


class Coordinates(NamedTuple):
    lat: float
    long: float


class Country(StrEnum):
    UK = auto()


class Address(abc.ABC):
    @property
    @abc.abstractmethod
    def address(self) -> str:
        """
        Get a human readable version of the address, that can be used to
        search for the location in e.g. Google Maps.
        Should not include the country_name or country code.
        """
        pass

    @property
    @abc.abstractmethod
    def country_name(self) -> str:
        """
        Get the full name of the country the address is designed for
        """
        pass

    country: Country

    @abc.abstractmethod
    def get_post_code(self) -> str:
        pass

    @property
    def full_address(self) -> str:
        """
        Get the full, human-readable address including the country. Can be used
        to search for the location in e.g. Google Maps.
        """
        return f"{self.address}, {self.country_name}"


@dataclass(frozen=True)
class UKAddress(Address):
    line1: str
    line2: str | None
    town: str
    post_code: str
    country: Country = Country.UK

    @property
    def address(self) -> str:
        return f"{self.line1}, {self.line2}, {self.town}, {self.post_code}"

    @property
    def country_name(self) -> str:
        return "United Kingdom"

    def get_post_code(self) -> str:
        return self.post_code


@dataclass(frozen=True)
class Location:
    coords: Coordinates
    address: Address


@dataclass(frozen=True)
class AddressFreeLocation:
    coords: Coordinates
    name: str


@dataclass(frozen=True)
class Listing(abc.ABC):
    id: UUID | str

    @abc.abstractmethod
    def summarise(self) -> ListingSummary:
        pass


@dataclass(frozen=True)
class AccommodationListing(Listing, abc.ABC):
    id: UUID | str
    location: Location
    created_at: float
    """Time of listing creation"""
    price: int

    title: str
    description: str
    accommodation_type: str
    number_of_rooms: int

    source: Source

    @property
    @abc.abstractmethod
    def thumbnail_url(self) -> str | None:
        pass

    @property
    @abc.abstractmethod
    def short_description(self) -> str:
        pass

    @abc.abstractmethod
    def summarise(self) -> AccommodationSummary:
        pass


@dataclass(frozen=True)
class InternalAccommodationListing(AccommodationListing):
    id: UUID
    author_email: str

    photo_ids: tuple[UUID, ...]

    @property
    def thumbnail_url(self) -> str | None:
        if len(self.photo_ids) > 0:
            return url_for(
                "listings.get_listing_photo",
                listing_id=self.id, photo_id=self.photo_ids[0]
            )
        return None

    @property
    def short_description(self) -> str:
        return self.description

    def summarise(self) -> AccommodationSummary:
        return InternalAccommodationSummary(
            id=str(self.id),
            title=self.title,
            short_description=self.short_description,
            thumbnail_id=self.photo_ids[0],
            accommodation_type=self.accommodation_type,
            number_of_rooms=self.number_of_rooms,
            source=self.source,
            post_code=self.location.address.get_post_code(),
            price=self.price
        )


@dataclass(frozen=True)
class ExternalAccommodationListing(AccommodationListing):
    original_listing_url: str
    id: str
    author_name: str
    author_phone: str
    photo_urls: list[str]
    _short_description: str

    @property
    def thumbnail_url(self) -> str | None:
        if len(self.photo_urls) > 0:
            return self.photo_urls[0]
        return None

    @property
    def short_description(self) -> str:
        return self._short_description

    def summarise(self) -> AccommodationSummary:
        return ExternalAccommodationSummary(
            id=str(self.id),
            title=self.title,
            short_description=self._short_description,
            thumbnail_url=self.thumbnail_url,
            accommodation_type=self.accommodation_type,
            number_of_rooms=self.number_of_rooms,
            source=self.source,
            post_code=self.location.address.get_post_code(),
            price=self.price
        )


@dataclass(frozen=True)
class Photo:
    id: UUID
    blob: bytes


@dataclass(frozen=True)
class SeekingListing(Listing):
    id: UUID
    author_email: str
    location: AddressFreeLocation
    created_at: float

    title: str
    description: str
    photo_ids: tuple[UUID, ...]

    def summarise(self) -> SeekingSummary:
        return SeekingSummary(
            id=self.id,
            title=self.title,
            short_description=self.description,
            thumbnail_id=(self.photo_ids[0] if len(
                self.photo_ids) > 0 else None),
            location_name=self.location.name
        )

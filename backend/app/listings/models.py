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


@dataclass(frozen=True)
class AccommodationSummary(abc.ABC):
    id: str
    title: str
    short_description: str
    accommodation_type: str
    number_of_rooms: int
    source: Source
    price: float
    post_code: str


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
class AccommodationListing(abc.ABC):
    id: UUID | str | int
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
    original_listing_url: str  # TODO include in DTO
    id: int
    author_phone: str
    photo_urls: list[str]
    short_description: str

    @property
    def thumbnail_url(self) -> str | None:
        if len(self.photo_urls) > 0:
            return self.photo_urls[0]
        return None

    def summarise(self) -> AccommodationSummary:
        return ExternalAccommodationSummary(
            id=str(self.id),
            title=self.title,
            short_description=self.short_description,
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

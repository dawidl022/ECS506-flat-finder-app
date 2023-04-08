import abc
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import NamedTuple
from uuid import UUID


class SortBy(StrEnum):
    newest = auto(),
    cheapest = auto(),
    closest = auto()


class Source(StrEnum):
    internal = auto()
    zoopla = auto()


@dataclass(frozen=True)
class AccommodationSummary:
    id: str
    title: str
    short_description: str
    thumbnail_id: UUID
    accommodation_type: str
    number_of_rooms: int
    source: Source
    price: float
    post_code: str


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
class AccommodationListing:
    id: UUID
    location: Location
    created_at: float
    """Time of listing creation"""
    price: int
    author_email: str

    title: str
    description: str
    accommodation_type: str
    number_of_rooms: int

    photo_ids: tuple[UUID, ...]

    source: Source

    def summarise(self) -> AccommodationSummary:
        return AccommodationSummary(
            id=str(self.id),
            title=self.title,
            short_description=self.description,
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
    listing_id: int
    photo_urls: list[str]
    short_description: str
    author_phone: str


@dataclass(frozen=True)
class Photo:
    id: UUID
    blob: bytes

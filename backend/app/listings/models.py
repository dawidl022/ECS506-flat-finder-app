import abc
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import NamedTuple
from uuid import UUID
from marshmallow import Schema, fields
from marshmallow.validate import Range

from app.util.schema import Schemable


class SortBy(StrEnum):
    newest = auto(),
    cheapest = auto(),
    closest = auto()


class AccommodationSearchParamsSchema(Schema):
    location = fields.Str(required=True)
    radius = fields.Float(required=True, validate=Range(min=0))
    max_price = fields.Float(validate=Range(min=0))
    sort_by = fields.Enum(SortBy)
    page = fields.Int(validate=Range(min=0))
    size = fields.Int(validate=Range(min=1, max=100))


@dataclass(frozen=True)
class AccommodationSearchParams(Schemable):
    schema = AccommodationSearchParamsSchema()

    location: str
    radius: float
    max_price: float | None
    sources: str | None
    sort_by: SortBy = SortBy.newest
    page: int = 0
    size: int = 10

    @property
    def sources_list(self) -> list[str]:
        return self.sources.split(",") if self.sources else []


@dataclass(frozen=True)
class AccommodationSummary:
    id: str
    title: str
    short_description: str
    thumbnail_url: str
    accommodation_type: str
    number_of_rooms: int
    source: str
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
    author_phone: str

    title: str
    description: str
    accommodation_type: str
    number_of_rooms: int

    photo_ids: tuple[UUID, ...]
    photo_urls: list[str]
    source: str

@dataclass(frozen=True)
class ExternalAccommodationListing(AccommodationListing):
    original_listing_url: str
    listing_id: int


@dataclass(frozen=True)
class Photo:
    id: UUID
    blob: bytes


@dataclass(frozen=True)
class ContactDetails:
    phone_number: str


@dataclass(frozen=True)
class User:
    id: UUID
    email: str
    name: str
    contact_details: ContactDetails
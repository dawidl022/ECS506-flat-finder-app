import abc
from dataclasses import dataclass
from enum import StrEnum
import json
from typing import Any, cast
from flask import url_for

from marshmallow import Schema, fields
import marshmallow
from marshmallow.validate import Range
import dacite
from app.user.user_dtos import UserDTO
from app.user.user_models import User

from app.util.schema import Schemable
from app.listings.models import (
    AccommodationSearchResult, AccommodationSummary, Country,
    ExternalAccommodationListing, ExternalAccommodationSummary,
    InternalAccommodationListing, InternalAccommodationSummary, ListingSummary,
    ListingType, SortBy, Source, UKAddress)
from app.util.encoding import CamelCaseDecoder
from app.listings.models import Address, AccommodationListing


def validate_sources(sources: str) -> str:

    for s in sources.split(","):
        try:
            Source(s)
        except ValueError as e:
            raise marshmallow.ValidationError(str(e))
    return sources


class AccommodationSearchParamsSchema(Schema):
    location = fields.Str(required=True)
    radius = fields.Float(required=True, validate=Range(min=0))
    max_price = fields.Float(validate=Range(min=0))
    sort_by = fields.Enum(SortBy)
    sources = fields.Str(validate=validate_sources)
    page = fields.Int(validate=Range(min=0))
    size = fields.Int(validate=Range(min=1, max=100))


@dataclass(frozen=True)
class AccommodationSearchParams(Schemable):
    schema = AccommodationSearchParamsSchema()

    location: str
    radius: float
    max_price: float | None = None
    sources: str | None = None
    sort_by: SortBy = SortBy.newest
    page: int = 0
    size: int = 10

    @property
    def sources_list(self) -> list[Source]:
        return [
            Source(s) for s in self.sources.split(",")
        ] if self.sources else []


def validate_address(addr: str) -> dict[str, str]:
    address = cast(
        dict[str, str], CamelCaseDecoder.snake_casify(json.loads(addr)))
    country = address.get("country")
    if country is None:
        raise marshmallow.ValidationError(
            "country missing from address")

    match Country(country):
        case Country.UK:
            try:
                dacite.from_dict(data_class=UKAddress, data=address,
                                 config=dacite.Config(cast=[Country]))
                return address
            except dacite.DaciteError:
                raise marshmallow.ValidationError(
                    f"invalid address format for country: {country}")

    raise marshmallow.ValidationError(f"invalid country: {country}")


class CreateAccommodationFormSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    accommodation_type = fields.Str(required=True)
    number_of_rooms = fields.Int(required=True, validate=Range(min=1))
    price = fields.Int(validate=Range(min=0))
    address = fields.Field(required=True, validate=validate_address)
    photos = fields.Raw()


@dataclass(frozen=True)
class AccommodationForm(Schemable):
    schema = CreateAccommodationFormSchema()

    title: str
    description: str
    accommodation_type: str
    number_of_rooms: int
    price: int
    address: str

    @property
    def decoded_address(self) -> Address:
        address = cast(
            dict[str, str],
            CamelCaseDecoder.snake_casify(json.loads(self.address))
        )
        country = address["country"]

        match Country(country):
            case Country.UK:
                return dacite.from_dict(data_class=UKAddress, data=address,
                                        config=dacite.Config(cast=[StrEnum]))

        raise ValueError("Unexpected country")

    def to_dict(self) -> dict[str, Any]:
        d = vars(self).copy()
        del d["address"]
        return d


class AuthorDTO:
    def __init__(self, author: User) -> None:
        self.name = author.name
        self.userProfile = UserDTO(author)


class ContactInfoDTO:
    def __init__(self, author: User) -> None:
        self.email = author.email
        self.phone_number = author.contact_details.phone_number


class AccommodationListingDTO:
    def __init__(self, listing: AccommodationListing, author: User):
        self.id = f"{listing.source}_{listing.id}"
        self.title = listing.title
        self.description = listing.description
        self.photo_urls = self.get_photo_urls(listing)
        self.accommodation_type = listing.accommodation_type
        self.number_of_rooms = listing.number_of_rooms
        self.source = listing.source
        self.price = listing.price
        self.address = listing.location.address
        self.original_listing_url = self.get_original_listing_url(listing)
        self.author = AuthorDTO(author)  # TODO conditionally set author
        self.contact_info = ContactInfoDTO(author)

    @staticmethod
    def get_photo_urls(listing: AccommodationListing) -> list[str]:
        if isinstance(listing, InternalAccommodationListing):
            return [
                url_for("listings.get_listing_photo",
                        listing_id=listing.id, photo_id=id)
                for id in listing.photo_ids
            ]
        elif isinstance(listing, ExternalAccommodationListing):
            return listing.photo_urls
        return []

    @staticmethod
    def get_original_listing_url(listing: AccommodationListing) -> str | None:
        if isinstance(listing, ExternalAccommodationListing):
            return listing.original_listing_url
        return None


@dataclass
class AccommodationSummaryDTO:
    id: str
    title: str
    short_description: str
    accommodation_type: str
    number_of_rooms: int
    thumbnail_url: str | None
    source: Source
    price: float
    post_code: str

    def __init__(self, summary: AccommodationSummary):
        self.id = f"{summary.source}_{summary.id}"
        self.title = summary.title
        self.short_description = summary.short_description
        self.accommodation_type = summary.accommodation_type
        self.number_of_rooms = summary.number_of_rooms
        self.thumbnail_url = self.get_thumbnail_url(summary)
        self.source = summary.source
        self.price = summary.price
        self.post_code = summary.post_code

    @staticmethod
    def get_thumbnail_url(summary: AccommodationSummary) -> str | None:
        if isinstance(summary, InternalAccommodationSummary):
            return url_for(
                "listings.get_listing_photo",
                listing_id=summary.id, photo_id=summary.thumbnail_id
            )
        elif isinstance(summary, ExternalAccommodationSummary):
            return summary.thumbnail_url
        return None


@dataclass
class SeekingSummaryDTO:
    # TODO
    pass


@dataclass
class ListingSummaryDTO:
    type: ListingType
    listing: AccommodationSummaryDTO | SeekingSummaryDTO

    def __init__(self, summary: ListingSummary):
        if isinstance(summary, AccommodationSummary):
            self.type = ListingType.accommodation
            self.listing = AccommodationSummaryDTO(summary)
        else:
            raise TypeError("unsupported ListingSummary subtype")


@dataclass(frozen=True)
class SourceDTO:
    name: str
    enabled: bool
    failed: bool


@dataclass
class AccommodationSearchResultDTO:
    distance: float
    is_favourite: bool
    accommodation: AccommodationSummaryDTO

    def __init__(self, result: AccommodationSearchResult):
        self.distance = result.distance
        self.is_favourite = result.is_favourite
        self.accommodation = AccommodationSummaryDTO(result.accommodation)


@ dataclass(frozen=True)
class SearchResultDTO:
    sources: list[SourceDTO]
    search_results: list[AccommodationSearchResultDTO]

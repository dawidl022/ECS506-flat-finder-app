from dataclasses import dataclass
from enum import StrEnum, auto
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


@dataclass
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


@dataclass
class AccommodationSearchResult:
    distance: float
    is_favourite: bool
    accommodation: AccommodationSummary


@dataclass
class AccommodationListing:
    thumbnailUrl: str
    accommodationType: str
    numberOfRooms: int
    sourceName: str


@dataclass
class ExternalAccommodationListing(AccommodationListing):
    listingUrl: str

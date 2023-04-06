import abc
from dataclasses import dataclass
from enum import StrEnum
import json
from typing import cast
from flask import url_for

from marshmallow import Schema, fields
import marshmallow
from marshmallow.validate import Range
import dacite
from werkzeug.datastructures import FileStorage

from app.util.schema import Schemable
from app.listings.models import Country, UKAddress
from app.util.encoding import CamelCaseDecoder
from app.listings.models import Address
from app.listings.models import AccommodationListing
from app.listings.models import User


def is_valid_address(addr: str) -> dict[str, str]:
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
    address = fields.Field(required=True, validate=is_valid_address)
    photos = fields.Raw()


@dataclass(frozen=True)
class CreateAccommodationForm(Schemable):
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


class AuthorDTO:
    def __init__(self, author: User) -> None:
        self.name = author.name
        self.userProfile = author


class ContactInfoDTO:
    def __init__(self, author: User) -> None:
        self.email = author.email
        self.phone_number = author.contact_details.phone_number


class AccommodationListingDTO:
    def __init__(self, listing: AccommodationListing, author: User) -> None:
        self.id = f"{listing.source}/{listing.id}"
        self.title = listing.title
        self.description = listing.description
        self.photo_urls = [
            url_for("listings.get_listing_photo",
                    listing_id=listing.id, photo_id=id)
            for id in listing.photo_ids
        ]
        self.accommodation_type = listing.accommodation_type
        self.number_of_rooms = listing.number_of_rooms
        self.source = listing.source
        self.price = listing.price
        self.address = listing.location.address
        self.author = AuthorDTO(author)
        self.contact_info = ContactInfoDTO(author)

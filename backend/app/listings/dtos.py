import abc
from dataclasses import dataclass

from marshmallow import Schema, fields
import marshmallow
from marshmallow.validate import Range
import dacite

from app.util.schema import Schemable
from app.listings.models import Country, UKAddress


def is_valid_address(address: dict[str, str]) -> dict[str, str]:
    country = address.get("country")
    if country is None:
        raise marshmallow.ValidationError("")  # TODO missing country

    match Country(country):
        case Country.UK:
            try:
                dacite.from_dict(data_class=UKAddress, data=address)
                return address
            except dacite.DaciteError:
                # TODO invalid address fro country
                raise marshmallow.ValidationError("")

    raise marshmallow.ValidationError("")  # TODO invalid country


class CreateAccommodationFormSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    accommodation_type = fields.Str(required=True)
    number_of_rooms = fields.Int(required=True, validate=Range(min=1))
    price = fields.Int(validate=Range(min=0))
    address = fields.Dict(required=True, validate=is_valid_address)


@dataclass(frozen=True)
class CreateAccommodationForm(Schemable):
    schema = CreateAccommodationFormSchema()

    title: str
    description: str
    accommodation_type: str
    number_of_rooms: int
    price: int
    address: UKAddress

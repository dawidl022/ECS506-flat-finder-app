from dataclasses import dataclass
from uuid import UUID
from marshmallow import Schema, fields
from app.user.user_models import ContactDetails, User

from app.util.schema import Schemable


class ContactDetailsSchema(Schema):
    phone_number = fields.Str()


class UserProfileSchema(Schema):
    name = fields.Str(required=True)
    contact_details = fields.Nested(ContactDetailsSchema, required=True)


@dataclass(frozen=True)
class UserProfileForm(Schemable):
    schema = UserProfileSchema()

    name: str
    contact_details: ContactDetails


@dataclass
class UserDTO:
    id: UUID
    email: str
    name: str | None
    contact_details: ContactDetails

    def __init__(self, user: User) -> None:
        self.id = user.id
        self.email = user.email
        self.name = user.name
        self.contact_details = user.contact_details


@dataclass
class UserSummaryDTO:
    id: UUID
    email: str
    name: str | None
    is_admin: bool

    def __init__(self, user: User) -> None:
        self.id = user.id
        self.email = user.email
        self.name = user.name
        self.is_admin = user.is_admin

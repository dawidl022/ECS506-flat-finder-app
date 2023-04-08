
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ContactDetails:
    phone_number: str | None = None


@dataclass(frozen=True)
class User:
    id: UUID
    email: str
    name: str | None = None
    is_admin: bool = False
    contact_details: ContactDetails = ContactDetails()


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


@dataclass(frozen=True)
class UserProfileForm:
    name: str
    contact_details: ContactDetails

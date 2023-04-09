
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

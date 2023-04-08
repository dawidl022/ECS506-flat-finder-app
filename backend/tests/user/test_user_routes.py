from http.client import NOT_FOUND, OK
import json
import uuid
from flask.testing import FlaskClient
from app.user.user_model import ContactDetails, User, UserProfileForm

from app.user.user_service import BaseUserService

registered_user_id = uuid.uuid4()
registered_user = User(
    id=registered_user_id,
    email="unittest@example.com",
    contact_details=ContactDetails(phone_number="+123456789")
)


class MockUserService(BaseUserService):
    def get_user(self, user_id) -> User | None:
        if user_id == registered_user_id:
            return registered_user
        return None

    def get_user_id_for_email(self, email: str) -> uuid.UUID:
        return uuid.uuid4()

    def update_user(self, user_id: uuid.UUID, profile: UserProfileForm) -> None:
        pass


def test_get_user__given_invalid_id_format__returns_not_found(client: FlaskClient):
    response = client.get("/api/v1/users/whatever/profile")

    assert response.status_code == NOT_FOUND


def test_get_user__given_id_not_mapped_to_user__returns_not_found(client: FlaskClient):
    response = client.get(f"/api/v1/users/{uuid.uuid4()}/profile")

    assert b'{"userId":"user not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_get_user__given_valid_id__returns_user_profile(client: FlaskClient):
    response = client.get(f"/api/v1/users/{registered_user_id}/profile")

    assert json.loads(response.data) == {
        "id": str(registered_user.id),
        "email": registered_user.email,
        "name": None,
        "contactDetails": {
            "phoneNumber": registered_user.contact_details.phone_number
        }
    }
    assert response.status_code == OK

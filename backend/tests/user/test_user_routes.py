import dataclasses
from http.client import BAD_REQUEST, FORBIDDEN, NO_CONTENT, NOT_FOUND, OK
import json
from unittest.mock import patch
import uuid
from flask.testing import FlaskClient
from app.user.user_dtos import UserProfileForm
from app.user.user_models import ContactDetails, User
from app.user.user_service import BaseUserService, UserNotFoundError

from ..listings.test_routes import model_listing_author, search_results_json

registered_user_id = uuid.uuid4()
registered_user = User(
    id=registered_user_id,
    email="unittest@example.com",
    contact_details=ContactDetails(phone_number="+123456789")
)


class MockUserService(BaseUserService):

    def __init__(self) -> None:
        self.deleted_user_ids: list[uuid.UUID] = []
        self.updated_users: list[tuple[uuid.UUID, UserProfileForm]] = []
        self.deregistered_user_ids: list[uuid.UUID] = []
        self.admin_id: uuid.UUID | None = None

    def get_user(self, user_id) -> User | None:
        if user_id == registered_user_id:
            return registered_user
        elif user_id == model_listing_author.id:
            return model_listing_author
        elif self.admin_id is not None and user_id == self.admin_id:
            return self._get_admin()
        return None

    def _get_admin(self):
        return dataclasses.replace(registered_user, id=self.admin_id, is_admin=True)

    def get_user_id_for_email(self, email: str) -> uuid.UUID:
        if email == model_listing_author.email:
            return model_listing_author.id
        return uuid.uuid4()

    def update_user(self, user_id: uuid.UUID, profile: UserProfileForm) -> None:
        self.updated_users.append((user_id, profile))

        if user_id in self.deleted_user_ids:
            raise UserNotFoundError()

    def delete_user(self, user_id: uuid.UUID) -> None:
        self.deleted_user_ids.append(user_id)

    def get_all_users(self) -> list[User]:
        return [registered_user, model_listing_author, self._get_admin()]

    def deregister_user(self, user_id: uuid.UUID) -> None:
        self.deregistered_user_ids.append(user_id)
        if user_id != registered_user_id:
            raise UserNotFoundError()


def test_get_all_users__given_user_not_found__returns_not_found(client: FlaskClient):
    response = client.get(
        f"/api/v1/users/")

    assert b'{"userId":"user not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_get_all_users__given_user_not_admin__returns_forbidden(client: FlaskClient):
    with patch("app.auth.jwt.get_jwt") as mock_get_jwt_local, \
            patch("flask_jwt_extended.utils.get_jwt") as mock_get_jwt_lib:
        return_value = {
            "sub": str(model_listing_author.id),
            "email": model_listing_author.email
        }
        mock_get_jwt_local.return_value = return_value
        mock_get_jwt_lib.return_value = return_value

        response = client.get(f"/api/v1/users/")

        assert b'{"user":"user not authorised"}' in response.data
        assert response.status_code == FORBIDDEN


def test_get_all_users__given_user_is_admin__returns_all_users(
        client: FlaskClient,
        user_service: MockUserService,
        currently_logged_in_user_id: uuid.UUID):
    user_service.admin_id = currently_logged_in_user_id

    response = client.get(
        f"/api/v1/users/")

    assert response.status_code == OK
    assert json.loads(response.data) == [
        {
            "id": str(registered_user.id),
            "name": registered_user.name,
            "email": registered_user.email,
            "isAdmin": False
        },
        {
            "id": str(model_listing_author.id),
            "name": model_listing_author.name,
            "email": model_listing_author.email,
            "isAdmin": False
        },
        {
            "id": str(currently_logged_in_user_id),
            "name": registered_user.name,
            "email": registered_user.email,
            "isAdmin": True
        }
    ]


def test_delete_all_users__given_user_not_admin__returns_forbidden(
        client: FlaskClient, user_service: MockUserService):
    with patch("app.auth.jwt.get_jwt") as mock_get_jwt_local, \
            patch("flask_jwt_extended.utils.get_jwt") as mock_get_jwt_lib:
        return_value = {
            "sub": str(model_listing_author.id),
            "email": model_listing_author.email
        }
        mock_get_jwt_local.return_value = return_value
        mock_get_jwt_lib.return_value = return_value

        response = client.delete(f"/api/v1/users/{registered_user_id}")

        assert b'{"user":"user not authorised"}' in response.data
        assert response.status_code == FORBIDDEN
        assert len(user_service.deregistered_user_ids) == 0


def test_delete_all_users__given_user_not_found__returns_not_found(client: FlaskClient):
    response = client.delete(f"/api/v1/users/{uuid.uuid4()}")

    assert b'{"userId":"user not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_delete_all_users__given_user_found__returns_no_content(
        client: FlaskClient, user_service: MockUserService, currently_logged_in_user_id: uuid.UUID):
    user_service.admin_id = currently_logged_in_user_id
    response = client.delete(f"/api/v1/users/{registered_user_id}")

    assert response.status_code == NO_CONTENT
    assert len(user_service.deregistered_user_ids) == 1
    assert user_service.deregistered_user_ids[0] == registered_user_id


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


def test_put_user__given_no_payload__returns_bad_request(client: FlaskClient, currently_logged_in_user_id: uuid.UUID):
    response = client.put(
        f"/api/v1/users/{currently_logged_in_user_id}/profile")

    assert response.status_code == BAD_REQUEST


def test_put_user__given_id_differers_from_logged_in_user__returns_forbidden(client: FlaskClient):
    response = client.put(f"/api/v1/users/{uuid.uuid4()}/profile", json={})

    assert b'{"userId":"user not owner of profile"}' in response.data
    assert response.status_code == FORBIDDEN


def test_put_user__given_invalid_payload__returns_bad_request(client: FlaskClient, currently_logged_in_user_id: uuid.UUID):
    response = client.put(
        f"/api/v1/users/{currently_logged_in_user_id}/profile", json={})

    assert b'{"contactDetails":["Missing data for required field."],"name":["Missing data for required field."]}' in response.data
    assert response.status_code == BAD_REQUEST


def test_put_user__given_user_not_found__returns_not_found(
        client: FlaskClient, user_service: MockUserService,
        currently_logged_in_user_id: uuid.UUID):

    user_service.delete_user(currently_logged_in_user_id)

    response = client.put(
        f"/api/v1/users/{currently_logged_in_user_id}/profile", json={
            "name": "New test user!",
            "contactDetails": {}
        })

    assert b'{"userId":"user not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_put_user__given_valid_payload__updates_profile_and_returns_no_content(
        client: FlaskClient,
        user_service: MockUserService,
        currently_logged_in_user_id: uuid.UUID):

    new_name = "New test user!"
    new_phone_number = "+48 789 123 456"
    response = client.put(
        f"/api/v1/users/{currently_logged_in_user_id}/profile", json={
            "name": new_name,
            "contactDetails": {
                "phoneNumber": new_phone_number
            }
        })

    print(response.data)
    assert response.status_code == NO_CONTENT
    assert len(user_service.updated_users) == 1
    assert user_service.updated_users[0] == (
        currently_logged_in_user_id,
        UserProfileForm(
            name=new_name,
            contact_details=ContactDetails(
                phone_number=new_phone_number
            )
        )
    )


def test_get_user_listings__given__id_not_mapped_to_user__returns_not_found(client: FlaskClient):
    response = client.get(f"/api/v1/users/{uuid.uuid4()}/listings")

    assert b'{"userId":"user not found"}' in response.data
    assert response.status_code == NOT_FOUND


def test_get_user_listings__given_valid_id__returns_user_listings(client: FlaskClient):
    response = client.get(f"/api/v1/users/{model_listing_author.id}/listings")

    assert response.status_code == OK
    assert json.loads(response.data) == [
        {
            "type": "accommodation",
            "listing": search_results_json[0]["accommodation"]
        }
    ]


def test_get_user_listings__given_user_has_no_listings__returns_empty_list(client: FlaskClient):
    response = client.get(f"/api/v1/users/{registered_user_id}/listings")

    assert response.status_code == OK
    assert json.loads(response.data) == []

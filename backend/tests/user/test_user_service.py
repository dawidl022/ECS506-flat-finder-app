import unittest
import uuid

from app.user.user_model import ContactDetails, User, UserProfileForm
from app.user.user_repository import InMemoryUserRepository
from app.user.user_service import UserNotFoundError, UserService


class TestUserClass(unittest.TestCase):

    def setUp(self) -> None:
        self.service = UserService(InMemoryUserRepository())

    def test_get_user_id_for_email__given_user_not_registered__registers_user_and_returns_id(self):
        user_id1 = self.service.get_user_id_for_email("email1@example.com")
        user_id2 = self.service.get_user_id_for_email("email2@example.com")

        self.assertIsNotNone(user_id1)
        self.assertIsNotNone(user_id2)
        self.assertNotEqual(user_id1, user_id2)

    def test_get_user_id_for_email__given_user_registered__returns_user_id(self):
        user_id1 = self.service.get_user_id_for_email("email1@example.com")
        user_id2 = self.service.get_user_id_for_email("email1@example.com")

        self.assertIsNotNone(user_id1)
        self.assertEqual(user_id1, user_id2)

    def test_get_user__given_user_registered__returns_user(self):
        user_email = "email@example.com"
        user_id = self.service.get_user_id_for_email(user_email)

        expected = User(
            id=user_id,
            email=user_email)

        actual = self.service.get_user(user_id)

        self.assertEqual(expected, actual)

    def test_get_user__given_user_not_registered__returns_none(self):
        self.assertIsNone(self.service.get_user(uuid.uuid4()))

    def test_update_user__given_user_registered__updates_user(self):
        user_email = "email@example.com"
        user_id = self.service.get_user_id_for_email(user_email)

        updated_user = User(
            id=user_id,
            email=user_email,
            name="Test User",
            contact_details=ContactDetails(
                phone_number="+44 78901 234567"
            )
        )

        updated_profile = UserProfileForm(
            name="Test User",
            contact_details=ContactDetails(
                phone_number="+44 78901 234567"
            )
        )

        self.service.update_user(user_id, updated_profile)

        self.assertEqual(updated_user, self.service.get_user(user_id))

    def test_update_user__given_user_not_registered_raises_error(self):
        non_registered_id = uuid.uuid4()
        updated_profile = UserProfileForm(
            name="Test User",
            contact_details=ContactDetails(
                phone_number="+44 78901 234567"
            )
        )

        self.assertRaises(
            UserNotFoundError,
            lambda: self.service.update_user(
                non_registered_id, updated_profile)
        )

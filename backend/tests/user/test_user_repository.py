import dataclasses
import unittest
from uuid import uuid4
from app.user.user_models import ContactDetails, User

from app.user.user_repository import InMemoryUserRepository


class TestInMemoryUserRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = InMemoryUserRepository()
        self.user_id = uuid4()
        self.user_email = "repo@test.com"

        self.user = User(
            id=self.user_id,
            email=self.user_email,
            name="Unittest user",
            contact_details=ContactDetails(phone_number="+44 78912 345678")
        )
        self.repo.save_user(self.user)

    def test_get_user_by_id__given_user_saved__returns_user(self):
        actual = self.repo.get_user_by_id(self.user_id)
        self.assertEqual(self.user, actual)

    def test_get_user_by_id__given_user_updated__returns_updated_user(self):
        updated_user = dataclasses.replace(
            self.user, name="Updated name",
            contact_details=ContactDetails(phone_number=None)
        )
        self.repo.save_user(updated_user)

        actual = self.repo.get_user_by_id(self.user_id)
        self.assertEqual(updated_user, actual)

    def test_get_user_by_id__given_no_user_saved__returns_none(self):
        actual = self.repo.get_user_by_id(uuid4())
        self.assertIsNone(actual)

    def test_get_user_by_email__given_user_saved_returns_user(self):
        actual = self.repo.get_user_by_email(self.user_email)
        self.assertEqual(self.user, actual)

    def test_get_user_by_email__given_user_updated_returns_updated_user(self):
        updated_user = dataclasses.replace(
            self.user, name="Updated name",
            contact_details=ContactDetails(phone_number=None)
        )
        self.repo.save_user(updated_user)

        actual = self.repo.get_user_by_email(self.user_email)
        self.assertEqual(updated_user, actual)

    def test_get_user_by_email__given_no_user_saved__returns_user(self):
        actual = self.repo.get_user_by_email("invalid@example.com")
        self.assertIsNone(actual)

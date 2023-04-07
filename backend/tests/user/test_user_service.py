import unittest

from app.user.user_model import User
from app.user.user_repository import InMemoryUserRepository
from app.user.user_service import UserService


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

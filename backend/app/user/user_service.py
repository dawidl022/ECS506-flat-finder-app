from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from app.user.user_model import ContactDetails, User

from app.user.user_repository import UserRepository


class BaseUserService(ABC):
    @abstractmethod
    def get_user_id_for_email(self, email: str):
        pass


class UserService(BaseUserService):

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def get_user_id_for_email(self, email: str) -> UUID:
        user = self.repo.get_user_by_email(email)

        if user is None:
            user = User(
                id=uuid4(),
                email=email,
            )
            self.repo.save_user(user)

        return user.id

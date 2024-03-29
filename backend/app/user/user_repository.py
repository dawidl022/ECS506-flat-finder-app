from abc import ABC, abstractmethod
from uuid import UUID
from app.user.user_exceptions import UserNotFoundError

from app.user.user_models import User


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, user_email: str) -> User | None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> None:
        pass


class InMemoryUserRepository(UserRepository):

    def __init__(self) -> None:
        self.users_by_id: dict[UUID, User] = {}
        self.users_by_email: dict[str, User] = {}

    def get_user_by_email(self, user_email: str) -> User | None:
        return self.users_by_email.get(user_email)

    def get_user_by_id(self, user_id: UUID) -> User | None:
        return self.users_by_id.get(user_id)

    def save_user(self, user: User) -> None:
        self.users_by_email[user.email] = user
        self.users_by_id[user.id] = user

    def get_all_users(self) -> list[User]:
        return list(self.users_by_id.values())

    def delete_user(self, user_id: UUID) -> None:
        user = self.users_by_id.get(user_id)

        if user is None:
            raise UserNotFoundError()

        del self.users_by_id[user_id]
        del self.users_by_email[user.email]

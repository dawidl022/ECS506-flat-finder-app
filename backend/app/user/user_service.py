from abc import ABC, abstractmethod
import dataclasses
from uuid import UUID, uuid4
from app.user.user_dtos import UserProfileForm
from app.user.user_models import ContactDetails, User

from app.user.user_repository import UserRepository


class BaseUserService(ABC):
    @abstractmethod
    def get_user_id_for_email(self, email: str) -> UUID:
        """
        Return the user_id corresponding to the user with the given email.

        Registers the user if the user is not already registered, creating a
        new user_id and saving it to the repository.
        """
        pass

    @abstractmethod
    def get_user(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def update_user(self, user_id: UUID, profile: UserProfileForm) -> None:
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

    def get_user(self, user_id) -> User | None:
        return self.repo.get_user_by_id(user_id)

    def update_user(self, user_id: UUID, profile: UserProfileForm) -> None:
        prev_user = self.repo.get_user_by_id(user_id)

        if prev_user is None:
            raise UserNotFoundError()

        updated_user = dataclasses.replace(prev_user, **vars(profile))

        self.repo.save_user(updated_user)


class UserNotFoundError(Exception):
    pass

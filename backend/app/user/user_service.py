from abc import ABC, abstractmethod
import dataclasses
from uuid import UUID, uuid4
from app.listings.service import ListingsCleanupService, BaseListingsService
from app.user.user_dtos import UserProfileForm
from app.user.user_exceptions import UserNotFoundError
from app.user.user_models import User

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

    @abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    def deregister_user(self, user_id: UUID) -> None:
        pass


class UserService(BaseUserService):

    def __init__(
        self, repo: UserRepository,
        listings_service: ListingsCleanupService
    ) -> None:
        self.repo = repo
        self.listings_service = listings_service

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

    def get_all_users(self) -> list[User]:
        return self.repo.get_all_users()

    def deregister_user(self, user_id: UUID) -> None:
        user = self.get_user(user_id)
        if user is None:
            raise UserNotFoundError()

        self.listings_service.delete_listings_authored_by(user.email)
        self.repo.delete_user(user_id)

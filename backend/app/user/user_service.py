from abc import ABC, abstractmethod
import dataclasses
from uuid import UUID, uuid4
from app.listings.service import ListingsCleanupService, BaseListingsService
from app.user.user_dtos import UserProfileForm
from app.user.user_exceptions import UserNotFoundError
from app.user.user_models import User

from app.user.user_repository import UserRepository
from config import Config


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


class AdminService(ABC):

    @abstractmethod
    def grant_admin(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def revoke_admin(self, user_id: UUID) -> None:
        pass


class UserService(BaseUserService, AdminService):

    def __init__(
        self, repo: UserRepository,
        listings_service: ListingsCleanupService
    ) -> None:
        self.repo = repo
        self.listings_service = listings_service

    def get_user_id_for_email(self, email: str) -> UUID:
        user = self.repo.get_user_by_email(email)
        su_email = Config().SUPERUSER_EMAIL
        is_admin = su_email is not None and email == su_email

        if user is None:
            user = User(
                id=uuid4(),
                email=email,
                is_admin=is_admin
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
        user = self._must_get_user(user_id)

        self.listings_service.delete_listings_authored_by(user.email)
        self.repo.delete_user(user_id)

    def grant_admin(self, user_id: UUID) -> None:
        user = self._must_get_user(user_id)

        updated_user = dataclasses.replace(user, is_admin=True)
        self.repo.save_user(updated_user)

    def revoke_admin(self, user_id: UUID) -> None:
        user = self._must_get_user(user_id)

        updated_user = dataclasses.replace(user, is_admin=False)
        self.repo.save_user(updated_user)

    def _must_get_user(self, user_id: UUID) -> User:
        user = self.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

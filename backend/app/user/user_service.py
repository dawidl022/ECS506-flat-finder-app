from abc import ABC, abstractmethod
from uuid import UUID

from app.user.user_repository import UserRepository


class BaseUserService(ABC):
    @abstractmethod
    def get_user_id_for_email(self, email: str):
        pass


class UserService(BaseUserService):

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def get_user_id_for_email(self, email: str) -> UUID:
        pass

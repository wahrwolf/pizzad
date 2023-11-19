from uuid import UUID
from .abc import User, UserFactory
from .user import UserEntity, UserType


class UserEntityFactory(UserFactory):
    @staticmethod
    def create_user(name: str) -> User:
        return UserEntity(name=name, type=UserType.REGULAR)

    @staticmethod
    def restore_user(uuid: UUID, name: str, type: UserType) -> UserEntity:
        return UserEntity(uuid=uuid, name=name, type=type)

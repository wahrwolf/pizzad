from .abc import User, UserFactory
from .user import UserEntity, UserType


class UserEntityFactory(UserFactory):
    @staticmethod
    def create_user(name: str) -> User:
        return UserEntity(name=name, type=UserType.REGULAR)

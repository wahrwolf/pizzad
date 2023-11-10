from enum import Enum
from typing import Optional

from pizzad.notification import Observer, Event
from pizzad.persistence import DictObject


class UserType(Enum):
    UNKNOWN = 0
    SYSTEM  = 1
    NONE    = 2
    NORMAL  = 3


class User(Observer, DictObject):
    name: str
    type: UserType

    def __init__(self, name: str, type: Optional[UserType] = None):
        super().__init__()
        self.name = name
        self.type = type if type else UserType.NORMAL

    def set_name(self, name: str):
        self.name = name
        return self

    def set_type(self, type: UserType):
        self.type = type
        return self

    def update(self, event: Event):
        pass

    def to_dict(self) -> dict:
        """
        Converts Order object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Order object.
        """
        return {
                'name': self.name,
                'type': self.type.value,
                }

    def update_from_dict(self, dictionary: dict):
        """
        Updates Order object from a dictionary representation.

        Args:
            dictionary (dict): Dictionary containing order information.
        """
        self.name = dictionary['name']
        self.type = UserType(dictionary['type'])
        return self


class UserFactory:
    @staticmethod
    def create_user(name: str = "<unknown>", type: UserType = UserType.UNKNOWN) -> User:
        return User(name=name, type=type)

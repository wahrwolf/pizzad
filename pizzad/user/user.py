from enum import Enum, auto
from pizzad.notification import Observer, Event
from pizzad.persistence import DictObject


class UserType(Enum):
    UNKNOWN = 0
    SYSTEM  = 1
    NONE    = 2
    NORMAL  = 3


class User(Observer, DictObject):
    id: str
    name: str
    type: UserType

    def set_name(self, name: str):
        self.name = name
        return self

    def set_id(self, id: str):
        self.id = id
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
                'id': self.id,
                'type': self.type,
                }

    def update_from_dict(self, dictionary: dict):
        """
        Updates Order object from a dictionary representation.

        Args:
            dictionary (dict): Dictionary containing order information.
        """
        self.name = dictionary['name']
        self.id = dictionary['id']
        self.type = UserType[dictionary['type']]
        return self

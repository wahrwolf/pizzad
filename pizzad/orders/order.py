from datetime import datetime
from typing import Set, List, Optional
from pizzad.persistence import DictObject
from pizzad.user import User, UserType


class Order(DictObject):
    """
    Represents a pizza order with a name, participants, and optional tags.
    """
    name: str
    closed_since: Optional[datetime]
    closed_by: Optional[User]
    created_by: User
    opened_by: Optional[User]

    @staticmethod
    def create_empty_instance():
        return Order()

    def __init__(self,
                 name: Optional[str] = None, id: Optional[str] = None,
                 tags: Optional[Set[str]] = None,
                 created_by: Optional[User] = None
                 ):
        """
        Initializes an Order object.

        Args:
            name (str): Name of the order.
            tags (Optional[Set[str]]): Set of tags associated with the order.
        """
        super().__init__()
        self.name = name
        self.created_by = created_by
        self.participants = []
        self.tags = tags if tags else set()
        self.closed_since = None
        self.opened_by = None
        self.closed_by = None

    def register_participant(
            self, name: str, enforce_registration: bool = False):
        """
        Registers a participant for the order.

        Args:
            name (str): Name of the participant.
            enforce_registration (bool): If True, enforces participant
                                         registration even if already
                                         registered or order is closed
        """
        if enforce_registration or (
                name not in self.participants and
                not self.is_closed
                ):

            self.participants.append(name)

    def get_number_of_participants(self) -> int:
        """
        Returns the number of participants registered for the order.

        Returns:
            int: Number of participants.
        """
        return len(self.participants)

    def add_tag(self, tag: str):
        """
        Adds a tag to the order.

        Args:
            tag (str): Tag to be added.
        """
        self.tags.add(tag)

    def to_dict(self) -> dict:
        """
        Converts Order object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Order object.
        """
        data = {
                'name': self.name,
                'participants': self.participants,
                'tags': list(self.tags),
        }

        if self.is_closed():
            data['closed_since'] = self.closed_since.strftime('%s')

        return data

    def update_from_dict(self, dictionary: dict):
        """
        Updates Order object from a dictionary representation.

        Args:
            dictionary (dict): Dictionary containing order information.
        """
        print(f"Rehydrating Order from: {dictionary}")
        self.name = dictionary['name']
        self.participants = dictionary['participants']
        self.tags = set(dictionary['tags'])

        if 'closed_since' in dictionary:
            self.closed_since = datetime.fromtimestamp(
                    int(dictionary['closed_since']))

    def is_closed(self) -> bool:
        """
        Returns if the order was closed

        Returns:
            bool: has the order been closed
        """
        return bool(self.closed_since)

    def close(self, closed_since: Optional[datetime] = None,
              closed_by: Optional[User] = None):

        assert not self.is_closed(), "Order is already closed!"
        self.closed_since = closed_since if closed_since else datetime.now()
        self.closed_by = closed_by

    def open(self, opened_by: Optional[User] = None):
        assert self.is_closed(), "Order is not closed!"
        self.closed_since = None
        self.closed_by = None
        self.opened_by = opened_by

    def __str__(self) -> str:
        return f"Order[{self.name}]{'' if not self.tags else str(['#'+tag for tag in self.tags])}"

    def __repr__(self) -> str:
        return f"Order[{self.name}]{'' if not self.tags else str(['#'+tag for tag in self.tags])}"


class OrderFactory:
    @staticmethod
    def create_order(name: Optional[str] = None, tags: Optional[Set[str]] = None) -> Order:
        return Order(name, tags, created_by=User("<system>", UserType.SYSTEM))

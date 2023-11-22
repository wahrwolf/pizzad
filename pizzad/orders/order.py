from datetime import datetime
from uuid import UUID
from collections.abc import Collection
from typing import Set, Optional
from pizzad.models import Entity
from .abc import Order, OrderOption, OrderOptionRegistry, User


class OrderEntity(Order, Entity):
    """
    Represents a pizza order with a name, participants, and optional tags.
    """
    name: str
    created_at: datetime
    closed_since: Optional[datetime]
    open_since: Optional[datetime]
    _options: OrderOptionRegistry

    def __init__(self,
                 name: Optional[str] = None,
                 uuid: Optional[UUID] = None,
                 created_at: Optional[datetime] = None,
                 closed_since: Optional[datetime] = None,
                 open_since: Optional[datetime] = None,
                 tags: Optional[Set[str]] = None,
                 ):
        """
        Initializes an Order object.

        Args:
            name (str): Name of the order.
            tags (Optional[Set[str]]): Set of tags associated with the order.
        """
        super().__init__(uuid=uuid)
        self.name = name
        self.registrations = {}
        self.tags = tags if tags else set()

        self.created_at = created_at if created_at else datetime.now()
        self.closed_since = closed_since
        self.open_since = open_since

    def set_registry(self, registry: OrderOptionRegistry):
        self._options = registry
        return self

    def add_option(self, option: OrderOption):
        self._options.register_member(option)
        return self

    def get_all_options(self) -> set[OrderOption]:
        return self._options.get_all_members()

    def register_user_for_option(self, participant: User, option: OrderOption):
        if option not in self._options:
            raise KeyError(
                    "Can not register participant for option."
                    f"Option [{option.uuid}] not part of this order!")
        if option not in self.registrations:
            self.registrations[option] = set()

        self.registrations[option].add(participant)

    def get_all_registrations(self):
        return self.registrations

    def add_tag(self, tag: str):
        """
        Adds a tag to the order.

        Args:
            tag (str): Tag to be added.
        """
        self.tags.add(tag)

    def get_tags(self) -> set[str]:
        return self.tags

    def is_closed_for_registration(self) -> bool:
        """
        Returns if the order was closed

        Returns:
            bool: has the order been closed
        """
        return bool(self.closed_since)

    def close_for_registration(self):
        assert not self.is_closed_for_registration(), "Order is already closed!"
        self.closed_since = datetime.now()

    def open_for_registration(self):
        assert self.is_closed_for_registration(), "Order is not closed!"
        self.closed_since = None
        self.open_since = datetime.now()

    def get_creation_timestamp(self):
        return self.created_at

    def get_closure_timestamp(self):
        return self.closed_since

    def get_opening_timestamp(self):
        return self.open_since

    def __str__(self) -> str:
        return f"Order[{self.get_uuid()}]: {self.name}]"

    def __repr__(self) -> str:
        return f"Order[{self.get_uuid()}]: {self.name}]"

    def __contains__(self, other) -> bool:
        if isinstance(other, User):
            for registrations in self.registrations.values():
                if other in registrations:
                    return True
        if isinstance(other, OrderOption):
            return other in self._options
        if isinstance(other, Collection):
            for child in other:
                if child in self:
                    return True
        return False

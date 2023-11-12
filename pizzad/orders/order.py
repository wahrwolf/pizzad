from datetime import datetime
from functools import reduce
from typing import Set, Optional
from pizzad.models import Entity
from pizzad.food import Ingredient, Allergen
from .models import Order, OrderOption, OrderOptionRegistry, User, OrderFactory


class OrderEntity(Order, Entity):
    """
    Represents a pizza order with a name, participants, and optional tags.
    """
    name: str
    created_at: datetime
    closed_since: Optional[datetime]
    open_since: Optional[datetime]

    def __init__(self,
                 name: Optional[str] = None,
                 tags: Optional[Set[str]] = None,
                 ):
        """
        Initializes an Order object.

        Args:
            name (str): Name of the order.
            tags (Optional[Set[str]]): Set of tags associated with the order.
        """
        super().__init__()
        self.name = name
        self.registrations = {}
        self.tags = tags if tags else set()

        self.created_at = datetime.now()
        self.closed_since = None
        self.open_since = None

        self._options = OrderOptionRegistry()

    def register_user_for_option(self, participant: User, option: OrderOption):
        if option not in self._options:
            raise KeyError(
                    "Can not register participant for option."
                    f"Option [{option.uuid}] not part of this order!")
        if option not in self.registrations:
            self.registrations[option] = set()

        self.registrations[option].add(participant)

    def add_tag(self, tag: str):
        """
        Adds a tag to the order.

        Args:
            tag (str): Tag to be added.
        """
        self.tags.add(tag)

    def get_options_by_query(self,
                             name_pattern: str = "",
                             with_ingredients:
                                 Optional[set[Ingredient]] = None,
                             without_ingredients:
                                 Optional[set[Ingredient]] = None,
                             without_allergenes:
                                 Optional[set[Allergen]] = None,
                             **kwargs) -> set[OrderOption]:
        options = self.get_options()

        if name_pattern:
            options = {
                    option for option in options
                    if name_pattern in option.get_name()}

        if with_ingredients:
            options = {
                    option for option in options
                    if reduce(
                        lambda has_ingredients, ingredient:
                        has_ingredients and ingredient in option,
                        with_ingredients, True
                     )
            }

        if without_ingredients:
            options = {
                    option for option in options
                    if reduce(
                        lambda has_not_ingredients, ingredient:
                        has_not_ingredients and ingredient not in option,
                        without_ingredients, True
                     )
            }

        if without_allergenes:
            options = {
                    option for option in options
                    if reduce(
                        lambda has_not_allergens, allergen:
                        has_not_allergens and allergen not in option,
                        without_allergenes, True
                     )
            }

        return options

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

    def __str__(self) -> str:
        return f"Order[{self.uuid}]: {self.name}]"

    def __repr__(self) -> str:
        return f"Order[{self.uuid}]: {self.name}]"


class SimpleOrderFactory(OrderFactory):
    @staticmethod
    def create_order(name: str):
        return OrderEntity(name)

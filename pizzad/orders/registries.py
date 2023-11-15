from typing import Optional
from uuid import UUID
from pizzad.models.implementations import DictRegistry
from pizzad.food import Allergen, Ingredient
from .models import OrderOption, OrderOptionRegistry, Order, OrderRegistry, User


class OrderOptionDictRegistry(OrderOptionRegistry, DictRegistry):
    def get_options_by_query(self,
                             name_pattern: str = "",
                             uuids: Optional[set[UUID]] = None,
                             with_ingredients:
                                 Optional[set[Ingredient]] = None,
                             without_ingredients:
                                 Optional[set[Ingredient]] = None,
                             without_allergenes:
                                 Optional[set[Allergen]] = None,
                             **kwargs) -> set[OrderOption]:

        options = self._registry.values()
        if uuids:
            options = filter(
                    lambda option: (option.uuid in uuids), options)

        if name_pattern:
            options = filter(
                    lambda option:
                    (name_pattern in option.get_name()), options)

        if without_ingredients:
            options = filter(
                    lambda option:
                    (without_ingredients not in option), options)

        if with_ingredients:
            options = filter(
                    lambda option:
                    (with_ingredients in option), options)

        if without_allergenes:
            options = filter(
                    lambda option:
                    (without_allergenes not in option), options)
        return options


class OrderDictRegistry(OrderRegistry, DictRegistry):
    def get_options_by_query(self,
                             name_pattern: str = "",
                             uuids: Optional[set[UUID]] = None,
                             with_participants: Optional[set[User]] = None,
                             without_participants: Optional[set[User]] = None,
                             **kwargs) -> set[Order]:
        orders = self._registry.values()
        if uuids:
            orders = filter(
                    lambda order: (order.uuid in uuids), orders)

        if name_pattern:
            orders = filter(
                    lambda order:
                    (name_pattern in order.get_name()), orders)

        if without_participants:
            orders = filter(
                    lambda order:
                    (without_participants not in order), orders)
        if with_participants:
            orders = filter(
                    lambda order:
                    (with_participants in order), orders)

        return orders

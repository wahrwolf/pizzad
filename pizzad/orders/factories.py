from typing import Optional
from uuid import UUID
from datetime import datetime
from pizzad.food import Ingredient
from .option import OrderOptionEntitiy
from .registries import OrderOptionDictRegistry
from .order import OrderEntity
from .abc import (
        Order, OrderFactory,
        OrderOption, OrderOptionFactory
        )


class OrderEntityFactory(OrderFactory):
    @staticmethod
    def create_order(name: str) -> Order:
        order = OrderEntity(name)
        registry = OrderOptionDictRegistry()
        order.set_registry(registry)
        return order

    @staticmethod
    def restore_order(
            uuid: UUID, name: str,
            created_at: datetime, 
            closed_since: Optional[datetime], 
            open_since: Optional[datetime]):
        order = OrderEntity(name=name, uuid=uuid,
                            created_at=created_at,
                            open_since=open_since,
                            closed_since=closed_since)
        registry = OrderOptionDictRegistry()
        order.set_registry(registry)
        return order


class OrderOptionEntitiyFactory(OrderOptionFactory):
    @staticmethod
    def create_option(name: str, ingredients: Optional[set[Ingredient]] = None
                      ) -> OrderOption:
        option = OrderOptionEntitiy(name=name)

        for ingredient in ingredients:
            option.add_ingredient(ingredient)
        return option

    @staticmethod
    def restore_option(uuid: UUID, name: str):
        option = OrderOptionEntitiy(uuid=uuid, name=name)
        return option

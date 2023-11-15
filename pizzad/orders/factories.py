from typing import Optional
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


class OrderOptionEntitiyFactory(OrderOptionFactory):
    @staticmethod
    def create_option(name: str, ingredients: Optional[set[Ingredient]] = None
                      ) -> OrderOption:
        option = OrderOptionEntitiy(name=name)

        for ingredient in ingredients:
            option.add_ingredient(ingredient)
        return option

from typing import Optional
from pizzad.models.entities import Entity
from pizzad.models.implementations import DictRegistry
from pizzad.food import Allergen, Ingredient
from .models import OrderOption, OrderOptionRegistry, OrderOptionFactory


class OrderOptionEntitiy(OrderOption, Entity):
    _ingredients: set[Ingredient]
    _allergenes: set[Allergen]

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self._ingredients = {}
        self._allergenes = {}

    def get_allergies(self) -> set[Allergen]:
        raise NotImplementedError

    def get_ingredients(self) -> set[Ingredient]:
        raise NotImplementedError

    def add_ingredient(self, ingredient: Ingredient):
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError


class SimpleOrderOptionFactory(OrderOptionFactory):
    @staticmethod
    def create_option(name: str, ingredients: Optional[set[Ingredient]] = None
                      ) -> OrderOption:
        option = OrderOptionEntitiy(name=name)

        for ingredient in ingredients:
            option.add_ingredient(ingredients)
        return option


class OrderOptionDictRegistry(OrderOptionRegistry, DictRegistry):
    def get_options_by_query(self, **kwargs) -> set[OrderOption]:
        raise NotImplementedError

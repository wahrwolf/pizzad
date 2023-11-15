from typing import Optional
from functools import reduce
from pizzad.models.entities import Entity
from pizzad.models.implementations import DictRegistry
from pizzad.food import Allergen, Ingredient
from .models import OrderOption, OrderOptionRegistry


class OrderOptionEntitiy(OrderOption, Entity):
    _ingredients: set[Ingredient]
    _allergenes: set[Allergen]

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self._ingredients = set()
        self._allergenes = set()

    def get_allergenes(self) -> set[Allergen]:
        return self._allergenes

    def get_ingredients(self) -> set[Ingredient]:
        return self._ingredients

    def add_ingredient(self, ingredient: Ingredient):
        self._allergenes.update(ingredient.get_allergenes())
        self._ingredients.add(ingredient)
        return self

    def get_name(self) -> str:
        return self.name

    def __str__(self):
        return f"OrderOption[{self.uuid}]: {self.name}"

    def __contains__(self, other) -> bool:
        if isinstance(other, Ingredient):
            return other in self._ingredients
        if isinstance(other, Allergen):
            return other in self._allergenes
        return False


class OrderOptionDictRegistry(OrderOptionRegistry, DictRegistry):
    def get_options_by_query(self,
                             name_pattern: str = "",
                             with_ingredients:
                                 Optional[set[Ingredient]] = None,
                             without_ingredients:
                                 Optional[set[Ingredient]] = None,
                             without_allergenes:
                                 Optional[set[Allergen]] = None,
                             **kwargs) -> set[OrderOption]:

        options = self._registry.values()
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

from uuid import UUID
from typing import Optional
from collections.abc import Collection
from pizzad.models.entities import Entity
from pizzad.food import Allergen, Ingredient
from .abc import OrderOption


class OrderOptionEntitiy(OrderOption, Entity):
    _ingredients: set[Ingredient]
    _allergenes: set[Allergen]

    def __init__(self, name: str, uuid: Optional[UUID] = None):
        super().__init__(uuid=uuid)
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
        return f"OrderOption[{self.get_uuid()}]: {self.name}"

    def __contains__(self, other) -> bool:
        if isinstance(other, Ingredient):
            return other in self._ingredients
        if isinstance(other, Allergen):
            return other in self._allergenes
        if isinstance(other, Collection):
            for child in other:
                if child in self:
                    return True
        return False

from enum import Enum
from typing import Optional

from pizzad.models import Entity
from pizzad.food import Ingredient, Allergen
from .abc import User


class UserType(Enum):
    UNKNOWN = 0
    SYSTEM  = 1
    NONE    = 2
    NORMAL  = 3
    REGULAR = NORMAL


class UserEntity(User, Entity):
    name: str
    type: UserType
    allergies: set[Allergen]
    excluded_ingredients: set[Ingredient]
    preferred_ingredients: set[Ingredient]

    def __init__(self, name: str, type: Optional[UserType] = None):
        super().__init__()
        self.name = name
        self.type = type if type else UserType.UNKNOWN

    def set_name(self, name: str):
        self.name = name
        return self

    def set_type(self, type: UserType):
        self.type = type
        return self

    def get_preferred_ingredients(self) -> set[Ingredient]:
        return self.preferred_ingredients

    def add_prefereed_ingredient(self, ingredient: Ingredient):
        self.preferred_ingredients.add(ingredient)

    def remove_prefereed_ingredient(self, ingredient: Ingredient):
        self.preferred_ingredients.remove(ingredient)

    def get_excluded_ingredients(self) -> set[Ingredient]:
        return self.excluded_ingredients

    def add_excluded_ingredient(self, ingredient: Ingredient):
        self.excluded_ingredients.add(ingredient)

    def remove_excluded_ingredient(self, ingredient: Ingredient):
        self.excluded_ingredients.remove(ingredient)

    def get_allergies(self) -> set[Allergen]:
        return self.allergies

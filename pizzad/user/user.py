from enum import Enum
from typing import Optional
from uuid import UUID

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

    def __init__(
            self, name: str,
            type: Optional[UserType] = None,
            uuid: Optional[UUID] = None,
            ):
        super().__init__(uuid=uuid)
        self.name = name
        self.type = type if type else UserType.UNKNOWN
        self.allergies = set()
        self.excluded_ingredients = set()
        self.preferred_ingredients = set()

    def set_name(self, name: str):
        self.name = name
        return self

    def get_name(self) -> str:
        return self.name

    def set_type(self, type: UserType):
        self.type = type
        return self

    def get_type(self):
        return self.type

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

    def add_allergy(self, allergy: Allergen):
        self.allergies.add(allergy)
        return self

    def get_allergies(self) -> set[Allergen]:
        return self.allergies

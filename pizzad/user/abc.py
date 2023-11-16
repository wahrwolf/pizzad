from abc import ABC, abstractmethod
from pizzad.food import Ingredient, Allergen


class User(ABC):
    @abstractmethod
    def get_allergies(self) -> set[Allergen]:
        raise NotImplementedError

    @abstractmethod
    def get_excluded_ingredients(self) -> set[Ingredient]:
        raise NotImplementedError

    @abstractmethod
    def get_preferred_ingredients(self) -> set[Ingredient]:
        raise NotImplementedError


class UserRegistry(ABC):
    @abstractmethod
    def get_users_by_query(self, **kwargs) -> set[User]:
        raise NotImplementedError


class UserFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_user(name: str) -> User:
        raise NotImplementedError

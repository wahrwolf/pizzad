from abc import ABC, abstractmethod
from typing import Optional
from pizzad.food import Ingredient, Allergen
from pizzad.models.pattern import Registry


class User(ABC):
    @abstractmethod
    def get_allergies(self) -> set[Allergen]:
        raise NotImplementedError

    def get_blacklisted_ingredients(self) -> set[Ingredient]:
        raise NotImplementedError


class UserRegistry(Registry):
    @abstractmethod
    def get_users_by_query(self, **kwargs) -> set[User]:
        raise NotImplementedError


class UserFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_user(name: str) -> User:
        raise NotImplementedError


class OrderOption(ABC):
    @abstractmethod
    def get_allergies(self) -> set[Allergen]:
        raise NotImplementedError

    @abstractmethod
    def get_ingredients(self) -> set[Ingredient]:
        raise NotImplementedError

    @abstractmethod
    def add_ingredient(self, ingredient: Ingredient):
        raise NotImplementedError


class OrderOptionFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_option(name: str, ingredients: Optional[set[Ingredient]] = None
                      ) -> OrderOption:
        raise NotImplementedError


class OrderOptionRegistry(Registry):
    def get_options_by_query(self, **kwargs) -> set[OrderOption]:
        raise NotImplementedError


class Order(ABC):
    @abstractmethod
    def add_option(self, option: OrderOption):
        raise NotImplementedError

    def get_options_by_query(self, **kwargs) -> set[OrderOption]:
        raise NotImplementedError

    @abstractmethod
    def register_user_for_option(self, participant: User, option: OrderOption):
        raise NotImplementedError

    @abstractmethod
    def open_for_registration(self):
        raise NotImplementedError

    @abstractmethod
    def close_for_registration(self):
        raise NotImplementedError

    @abstractmethod
    def is_closed_for_registration(self) -> bool:
        raise NotImplementedError


class OrderRegistry(Registry):
    def get_orders_by_query(self, **kwargs) -> set[Order]:
        raise NotImplementedError


class OrderFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_order(name: str) -> Order:
        raise NotImplementedError

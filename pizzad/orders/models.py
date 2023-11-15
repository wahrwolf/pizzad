from abc import ABC, abstractmethod
from typing import Optional
from pizzad.food import Ingredient, Allergen
from pizzad.models.pattern import Registry
from pizzad.user.abc import User


class OrderOption(ABC):
    _ingredients: set[Ingredient]
    _allergenes: set[Allergen]

    @abstractmethod
    def get_allergenes(self) -> set[Allergen]:
        raise NotImplementedError

    @abstractmethod
    def get_ingredients(self) -> set[Ingredient]:
        raise NotImplementedError

    @abstractmethod
    def add_ingredient(self, ingredient: Ingredient):
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    def __contains__(self, value):
        if isinstance(value, Ingredient):
            return value in self._ingredients
        elif isinstance(value, Allergen):
            return value in self._allergenes
        return False


class OrderOptionFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_option(name: str, ingredients: Optional[set[Ingredient]] = None
                      ) -> OrderOption:
        raise NotImplementedError


class OrderOptionRegistry(Registry):
    @abstractmethod
    def get_options_by_query(self, **kwargs) -> set[OrderOption]:
        raise NotImplementedError


class Order(ABC):
    _options: OrderOptionRegistry

    def add_option(self, option: OrderOption):
        self._options.register_member(option)
        return self

    def get_options(self) -> set[OrderOption]:
        return set(self._options.get_all_members())

    def get_options_by_query(self, **kwargs) -> set[OrderOption]:
        return self._options.get_options_by_query(**kwargs)

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

from abc import ABC, abstractmethod


class OrderRegistriyBuilder(ABC):

    @abstractmethod
    def build_user_mementos(self):
        return NotImplementedError

    @abstractmethod
    def build_order_mementos(self):
        return NotImplementedError

    @abstractmethod
    def build_user(self):
        return NotImplementedError

    @abstractmethod
    def build_orders(self):
        return NotImplementedError

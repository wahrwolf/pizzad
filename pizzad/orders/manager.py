from typing import Set, Optional, Dict, List
from pizzad.user import User
from pizzad.persistence import DictObject
from .order import Order, OrderFactory


class OrderManager(DictObject):
    _instance = None
    orders: Dict

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
            cls._instance.orders = []
        return cls._instance

    def __init__(self):
        super().__init__()
        self.orders = {}

    def create_order_if_not_exist(
            self, name: str, tags: Optional[Set[str]] = None) -> Order:
        if name not in self.orders:
            order = OrderFactory.create_order(name, tags)
            self.orders[name] = order

    def register_participant(self,
                             name: str, participant: User,
                             enforce_registration: bool = False):

        if name not in self.orders and enforce_registration:
            self.create_order_if_not_exist(name)
        self.orders[name].register_participant(
                participant, enforce_registration=enforce_registration)

    def close_order(self, name: str):
        self.orders[name].close()

    def get_orders(
            self, query: str, tags: Optional[Set[str]] = None) -> List[Order]:
        return [
                order
                for name, order in self.orders.items()
                if name.startswith(query) or name.endswith(query)
        ]

    def to_dict(self):
        return {"orders": {k: v.to_dict() for k, v in self.orders.items()}}

    def update_from_dict(self, dictionary):
        self.orders = {
                k: OrderFactory.create_order().update_from_dict(v)
                for k, v in dictionary["orders"]
        }

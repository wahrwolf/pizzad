#pizzad/orders/manager.py
#<---begin import --->
from typing import Set, Optional, Dict, List
import unittest
from unittest.mock import Mock
from pizzad.user import User
from pizzad.persistence import DictObject
from pizzad.orders.order import Order, OrderFactory
from pizzad.orders.manager import OrderManager

#<---begin tests -->
class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.order_factory_mock = Mock(spec=OrderFactory)
        self.order_manager = OrderManager()
        self.order_manager._instance = None  # Reset the singleton instance for testing

    def test_create_empty_instance(self):
        instance = OrderManager.create_empty_instance()
        self.assertIsInstance(instance, OrderManager)
        self.assertEqual(instance.orders, {})

    def test_singleton_instance(self):
        instance1 = OrderManager()
        instance2 = OrderManager()
        self.assertIs(instance1, instance2)

    def test_create_order_if_not_exist_new_order(self):
        order_name = "New Order"
        tags = {"tag1", "tag2"}
        order = self.order_manager.create_order_if_not_exist(order_name, tags)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.name, order_name)
        self.assertEqual(order.tags, tags)
        self.assertEqual(self.order_manager.orders, {order_name: order})

    def test_create_order_if_not_exist_existing_order(self):
        order_name = "Existing Order"
        existing_order = Mock(spec=Order)
        self.order_manager.orders[order_name] = existing_order
        order = self.order_manager.create_order_if_not_exist(order_name)
        self.assertEqual(order, existing_order)

    def test_register_participant(self):
        order_name = "Order"
        participant_name = "UserA"
        participant = Mock(spec=User)
        self.order_manager.create_order_if_not_exist(order_name)
        self.order_manager.register_participant(order_name, participant_name, participant)
        raise NotImplementedError

    def test_close_order(self):
        order_name = "Order"
        order = Mock(spec=Order)
        self.order_manager.orders[order_name] = order
        self.order_manager.close_order(order_name)
        order.close.assert_called_once()

    def test_get_orders_with_query(self):
        order_name1 = "Order1"
        order_name2 = "Order2"
        self.order_manager.create_order_if_not_exist(order_name1)
        self.order_manager.create_order_if_not_exist(order_name2)
        queried_orders = self.order_manager.get_orders(query="1")
        self.assertEqual(queried_orders, [self.order_manager.orders[order_name1]])

    def test_get_orders_without_query(self):
        order_name1 = "Order1"
        order_name2 = "Order2"
        self.order_manager.create_order_if_not_exist(order_name1)
        self.order_manager.create_order_if_not_exist(order_name2)
        all_orders = self.order_manager.get_orders()
        self.assertEqual(all_orders, list(self.order_manager.orders.values()))

    def test_to_dict(self):
        order_name = "Order"
        order = Mock(spec=Order)
        order_dict = {"key": "value"}
        order.to_dict.return_value = order_dict
        self.order_manager.orders[order_name] = order
        expected_dict = {"orders": {order_name: order_dict}}
        self.assertEqual(self.order_manager.to_dict(), expected_dict)

    def test_update_from_dict(self):
        order_name = "Order"
        order_dict = OrderFactory.create_order("test_order").to_dict()
        self.order_factory_mock.create_order.return_value.update_from_dict.return_value = Mock(spec=Order)
        dictionary = {"orders": {order_name: order_dict}}
        self.order_manager.update_from_dict(dictionary)
        self.assertEqual(self.order_manager.orders, {order_name: self.order_factory_mock.create_order.return_value.update_from_dict.return_value})

#<---end tests--->


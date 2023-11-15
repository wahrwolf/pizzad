
import unittest
from uuid import uuid4
from pizzad.food import Ingredient

from pizzad.user.factories import UserEntityFactory
from pizzad.user.registries import UserDictRegistry

from pizzad.orders.abc import Order,  OrderOption
from pizzad.orders.factories import OrderEntityFactory, OrderOptionEntitiyFactory
from pizzad.orders.registries import OrderDictRegistry, OrderOptionDictRegistry
from pizzad.orders.usecases import (
    create_new_order, delete_order_by_id, get_orders_by_query,
    create_new_option_for_order, query_options_for_order,
    get_option_by_id, delete_option_by_id, add_option_to_order,
    open_order_for_participant_registration, register_participant_for_option,
    close_order_for_participant_registration, get_all_available_options,
    get_all_compatible_options_for_user, create_order_with_compatible_options_for_user_collection
)


class TestOrderUseCases(unittest.TestCase):
    def setUp(self):
        self.user_factory = UserEntityFactory
        self.user_registry = UserDictRegistry()

        self.order_factory = OrderEntityFactory
        self.order_registry = OrderDictRegistry()

        self.option_factory = OrderOptionEntitiyFactory
        self.otion_registry = OrderOptionDictRegistry()

    def tearDown(self):
        pass  # Add cleanup code as needed

    def test_create_new_order(self):
        order_name = "Test Order"
        order = create_new_order(order_name,
                                 factory=self.order_factory,
                                 registry=self.order_registry)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.name, order_name)

    def test_delete_order_by_id(self):
        order_name = "Test Order"
        order = create_new_order(
                order_name,
                factory=self.order_factory,
                registry=self.order_registry)
        order_id = order.uuid
        delete_order_by_id(order_id, registry=self.order_registry)
        deleted_order = get_orders_by_query(
                registry=self.order_registry, uuids=set([order_id]))
        self.assertEqual(deleted_order, set())

    def test_get_orders_by_query(self):
        order_name_1 = "Test Order 1"
        order_name_2 = "Test Order 2"
        create_new_order(order_name_1,
                         registry=self.order_registry,
                         factory=self.order_factory)
        create_new_order(order_name_2,
                         registry=self.order_registry,
                         factory=self.order_factory)

        # Search by query
        query_result = get_orders_by_query(self.order_registry, name="Test Order")
        self.assertTrue(query_result)
        self.assertEqual(len(query_result), 2)

    def test_create_new_option_for_order(self):
        order_name = "Test Order"
        order = create_new_order(order_name,
                                 registry=self.order_registry,
                                 factory=self.order_factory)
        option_name = "Test Option"
        ingredients = {Ingredient.CHEESE}
        order_with_option = create_new_option_for_order(
                order, option_name, ingredients,
                factory=self.option_factory)
        self.assertIsInstance(order_with_option, Order)
        self.assertEqual(len(order_with_option.get_options()), 1)


if __name__ == "__main__":
    unittest.main()

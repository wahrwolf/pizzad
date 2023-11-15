
import unittest
from uuid import uuid4
from pizzad.user.manager import UserManager
from pizzad.orders.models import User, Order,  OrderOption
from pizzad.food import Ingredient
from pizzad.orders.usecases import (
    create_new_order, delete_order_by_id, get_orders_by_query,
    create_new_user, get_users_by_query, delete_user_by_id,
    create_new_option_for_order, query_options_for_order,
    get_option_by_id, delete_option_by_id, add_option_to_order,
    open_order_for_participant_registration, register_participant_for_option,
    close_order_for_participant_registration, get_all_available_options,
    get_all_compatible_options_for_user, create_order_with_compatible_options_for_user_collection
)


class TestOrderUseCases(unittest.TestCase):
    def setUp(self):
        self.user_registry = None
        self.user_factory = None

        self.order_factory = None
        self.order_registry = None

        self.option_factory = None
        self.otion_registry = None

    def tearDown(self):
        pass  # Add cleanup code as needed

    def test_create_new_order(self):
        order_name = "Test Order"
        order = create_new_order(order_name, self.order_factory, self.order_registry)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.name, order_name)

    def test_delete_order_by_id(self):
        order_name = "Test Order"
        order = create_new_order(order_name, self.order_factory, self.order_registry)
        order_id = order.uuid
        delete_order_by_id(order_id, self.order_registry)
        deleted_order = get_orders_by_query(
                registry=self.order_registry, uuids=set(order_id))
        self.assertIsNone(deleted_order)

    def test_get_orders_by_query(self):
        order_name_1 = "Test Order 1"
        order_name_2 = "Test Order 2"
        create_new_order(order_name_1, self.order_registry, self.order_registry)
        create_new_order(order_name_2, self.order_registry, self.order_registry)

        # Search by query
        query_result = get_orders_by_query(self.order_registry, name="Test Order")
        self.assertTrue(query_result)
        self.assertEqual(len(query_result), 2)

    def test_create_new_user(self):
        user_name = "Test User"
        user = create_new_user(user_name, self.user_factory, self.user_registry)
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, user_name)

    def test_get_users_by_query(self):
        user_name_1 = "Test User 1"
        user_name_2 = "Test User 2"
        create_new_user(user_name_1, self.user_factory, self.user_registry)
        create_new_user(user_name_2, self.user_factory, self.user_registry)

        # Search by query
        query_result = get_users_by_query(self.user_registry, name="Test User")
        self.assertTrue(query_result)
        self.assertEqual(len(query_result), 2)

    def test_create_new_option_for_order(self):
        order_name = "Test Order"
        order = create_new_order(order_name, self.order_factory, self.order_registry)
        option_name = "Test Option"
        ingredients = {Ingredient.CHEESE}
        order_with_option = create_new_option_for_order(order, option_name, ingredients, self.option_factory)
        self.assertIsInstance(order_with_option, Order)
        self.assertEqual(len(order_with_option.get_options()), 1)


if __name__ == "__main__":
    unittest.main()


import unittest

from pizzad.user.abc import User
from pizzad.user.factories import UserEntityFactory
from pizzad.user.registries import UserDictRegistry

from pizzad.user.usecases import (
    create_new_user, get_users_by_query, delete_user_by_id,
    )


class TestUserUseCases(unittest.TestCase):
    def setUp(self):
        self.user_factory = UserEntityFactory
        self.user_registry = UserDictRegistry()

    def tearDown(self):
        pass  # Add cleanup code as needed

    def test_create_new_user(self):
        user_name = "Test User"
        user = create_new_user(user_name, self.user_factory, self.user_registry)
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, user_name)

    def test_get_users_by_query(self):
        user_name_1 = "Test User 1"
        user_name_2 = "Test User 2"
        create_new_user(user_name_1,
                        factory=self.user_factory,
                        registry=self.user_registry)
        create_new_user(user_name_2,
                        factory=self.user_factory,
                        registry=self.user_registry)

        # Search by query
        query_result = get_users_by_query(self.user_registry, name="Test User")
        self.assertTrue(query_result)
        self.assertEqual(len(query_result), 2)

    def test_delete_user_by_id(self):
        user_name = "Test User"
        user = create_new_user(user_name, self.user_factory, self.user_registry)
        user_id = user.get_uuid()
        delete_user_by_id(user_id, registry=self.user_registry)
        deleted_user = get_users_by_query(
                registry=self.user_registry, uuids=set([user_id]))
        self.assertEqual(deleted_user, set())

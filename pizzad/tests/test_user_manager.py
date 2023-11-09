
#pizzad/user/manager.py
from typing import Dict, List
import unittest
from unittest.mock import Mock
from pizzad.persistence import DictObject
from pizzad.user.user import User, UserFactory, UserType
from pizzad.user.manager import UserManager


class TestUserManager(unittest.TestCase):
    def test_create_user_if_not_exist(self):
        name = "UserA"
        manager = UserManager()
        user = manager.create_user_if_not_exist(name)
        self.assertEqual(user.name, name)
        self.assertIn(name, manager.users)
        self.assertEqual(manager.users[name], user)

    def test_to_dict(self):
        name = "UserA"
        manager = UserManager()
        user = manager.create_user_if_not_exist(name)
        user_dict = user.to_dict()
        expected_dict = {
            "name": name,
            "type": user.type.value,
        }
        self.assertEqual(user_dict, expected_dict)

    def test_update_from_dict(self):
        name = "UserA"
        user_dict = {
            "name": name,
            "type": UserType.NORMAL.value
        }
        manager = UserManager()
        manager.update_from_dict({"users": {name: user_dict}})
        self.assertIn(name, manager.users)
        user = manager.users[name]
        self.assertEqual(user.name, name)
        self.assertEqual(user.user_type, UserType.NORMAL)

    def test_get_users(self):
        name1 = "UserA"
        name2 = "UserB"
        manager = UserManager()
        user1 = manager.create_user_if_not_exist(name1)
        user2 = manager.create_user_if_not_exist(name2)
        users = manager.get_users(query="User")
        self.assertIn(user1, users)
        self.assertIn(user2, users)

    def test_get_users_with_empty_query(self):
        name1 = "UserA"
        name2 = "UserB"
        manager = UserManager()
        user1 = manager.create_user_if_not_exist(name1)
        user2 = manager.create_user_if_not_exist(name2)
        users = manager.get_users()
        self.assertIn(user1, users)
        self.assertIn(user2, users)

#<---end tests--->

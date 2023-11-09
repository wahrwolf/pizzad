#pizzad/orders/order.py
#<---begin import --->
from datetime import datetime
from typing import Set, List, Optional
import unittest
from unittest.mock import Mock
from pizzad.persistence import DictObject
from pizzad.user import User, UserType
from pizzad.orders.order import Order, OrderFactory


#<---begin tests -->
class TestOrder(unittest.TestCase):
    def test_create_empty_instance(self):
        order = Order.create_empty_instance()
        self.assertIsInstance(order, Order)
        self.assertIsNone(order.name)
        self.assertEqual(order.participants, [])
        self.assertEqual(order.tags, set())
        self.assertIsNone(order.closed_since)
        self.assertIsNone(order.closed_by)
        self.assertIsNone(order.opened_by)

    def test_init(self):
        name = "Test Order"
        tags = {"tag1", "tag2"}
        created_by = User("UserA", UserType.NORMAL)
        order = Order(name, tags, created_by=created_by)
        self.assertEqual(order.name, name)
        self.assertEqual(order.participants, [])
        self.assertEqual(order.tags, tags)
        self.assertIsNone(order.closed_since)
        self.assertIsNone(order.closed_by)
        self.assertIsNone(order.opened_by)

    def test_register_participant(self):
        name = "Test Order"
        order = Order(name)
        participant_name = "UserA"
        order.register_participant(participant_name)
        self.assertIn(participant_name, order.participants)

    def test_get_number_of_participants(self):
        name = "Test Order"
        participants = ["UserA", "UserB", "UserC"]
        order = Order(name)
        order.participants = participants
        self.assertEqual(order.get_number_of_participants(), len(participants))

    def test_add_tag(self):
        name = "Test Order"
        tag = "tag1"
        order = Order(name)
        order.add_tag(tag)
        self.assertIn(tag, order.tags)

    def test_to_dict(self):
        name = "Test Order"
        participants = ["UserA", "UserB"]
        tags = {"tag1", "tag2"}
        closed_since = datetime(2023, 1, 1, 12, 0, 0)
        closed_by = User("System", UserType.SYSTEM)
        order = Order(name)
        order.participants = participants
        order.tags = tags
        order.closed_since = closed_since
        order.closed_by = closed_by
        order_dict = order.to_dict()
        expected_dict = {
            "name": name,
            "participants": participants,
            "tags": list(tags),
            "closed_since": closed_since.strftime('%s'),
        }
        self.assertEqual(order_dict, expected_dict)

    def test_update_from_dict(self):
        name = "Test Order"
        participants = ["UserA", "UserB"]
        tags = {"tag1", "tag2"}
        closed_since = datetime(2023, 1, 1, 12, 0, 0)
        order_dict = {
            "name": name,
            "participants": participants,
            "tags": list(tags),
            "closed_since": closed_since.strftime('%s'),
        }
        order = Order(name)
        order.update_from_dict(order_dict)
        self.assertEqual(order.name, name)
        self.assertEqual(order.participants, participants)
        self.assertEqual(order.tags, tags)
        self.assertEqual(order.closed_since, closed_since)

    def test_is_closed(self):
        order = Order("Test Order")
        self.assertFalse(order.is_closed())
        order.closed_since = datetime.now()
        self.assertTrue(order.is_closed())

    def test_close(self):
        order = Order("Test Order")
        closed_since = datetime(2023, 1, 1, 12, 0, 0)
        closed_by = User("System", UserType.SYSTEM)
        order.close(closed_since=closed_since, closed_by=closed_by)
        self.assertEqual(order.closed_since, closed_since)
        self.assertEqual(order.closed_by, closed_by)

    def test_open(self):
        order = Order("Test Order")
        opened_by = User("UserA", UserType.NORMAL)
        order.open(opened_by=opened_by)
        self.assertIsNone(order.closed_since)
        self.assertIsNone(order.closed_by)
        self.assertEqual(order.opened_by, opened_by)

    def test_str_representation(self):
        name = "Test Order"
        tags = {"tag1", "tag2"}
        order = Order(name)
        order.tags = tags
        expected_str = f"Order[{name}]{'' if not tags else str(['#' + tag for tag in tags])}"
        self.assertEqual(str(order), expected_str)

    def test_repr_representation(self):
        name = "Test Order"
        tags = {"tag1", "tag2"}
        order = Order(name)
        order.tags = tags
        expected_repr = f"Order[{name}]{'' if not tags else str(['#' + tag for tag in tags])}"
        self.assertEqual(repr(order), expected_repr)

class TestOrderFactory(unittest.TestCase):
    def test_create_order(self):
        name = "Test Order"
        tags = {"tag1", "tag2"}
        order = OrderFactory.create_order(name, tags)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.name, name)
        self.assertEqual(order.tags, tags)
        self.assertEqual(order.created_by.name, "<system>")
        self.assertEqual(order.created_by.user_type, UserType.SYSTEM)

#<---end tests--->

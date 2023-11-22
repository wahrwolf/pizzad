import unittest
from abc import ABC
from copy import deepcopy
from typing import Optional, List
from uuid import UUID
from pizzad.user.abc import User
from pizzad.orders.abc import Order, OrderOption
from pizzad.models.pattern import Entity
from pizzad.models.implementations import Registry, Snapshot
from pizzad.user_registry_builder import UserRegistryBuilder
from pizzad.order_option_registry_builder import OrderOptionRegistryBuilder
from pizzad.order_registry_builder import OrderRegistryBuilder
from serialized_data import SerializedDataBuilder
from archive import Archive

class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()

    def tearDown(self):
        self.registry = None

    def test_clear_registry(self):
        self.registry.clear_registry()
        self.assertEqual(self.registry.entities, set())

    def test_save_restore(self):
        self.registry.save()
        restored_registry = Registry.restore(self.registry.memento)
        self.assertEqual(restored_registry.entities, self.registry.entities)

    def test_build_entity(self):
        entity = self.registry.build_entity(Entity(id='1', type='user'))
        self.assertIsInstance(entity, User)

    def test_build_entities(self):
        entities = [Entity(id='1', type='user'), Entity(id='2', type='order')]
        self.registry.build_entities(entities)
        self.assertEqual(self.registry.entities, set(entities))

    def test_build_option_registry(self):
        option_registry = OrderOptionRegistryBuilder().build_option_registry([OrderOption(id='1', type='optional')])
        self.assertIsInstance(option_registry, OrderOptionRegistry)

    def test_build_order_registry(self):
        order_registry = OrderRegistryBuilder().build_order_registry([Order(id='1', type='pizza')])
        self.assertIsInstance(order_registry, OrderRegistry)

    def test_dereference_foreign_references(self):
        entity = Entity(id='1', type='user')
        self.assertEqual(entity.dereference_foreign_references(), set())

    def test_dereference_data_dicts(self):
        data_dict = {'entities': [Entity(id='1', type='user')]}
        self.assertEqual(self.registry.dereference_data_dicts([data_dict]), set())

    def test_isolate_entities(self):
        isolated_entities = self.registry.isolate_entities()
        self.assertEqual(isolated_entities, set(self.registry.entities))

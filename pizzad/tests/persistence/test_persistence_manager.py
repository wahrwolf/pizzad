#<---begin import --->
from uuid import UUID
import unittest
from unittest.mock import Mock
from pizzad.persistence.models import Instance
from pizzad.persistence.strategies import PersistenceStrategy
from pizzad.persistence.manager import PersistenceManager

#<---begin tests -->


class TestPersistenceManager(unittest.TestCase):
    def setUp(self):
        self.strategy = Mock(spec=PersistenceStrategy)
        self.manager = PersistenceManager(strategy=self.strategy)

    def test_set_strategy(self):
        new_strategy = Mock(spec=PersistenceStrategy)
        self.manager.set_strategy(new_strategy)
        self.assertEqual(self.manager.strategy, new_strategy)

    def test_save_instance(self):
        instance = Mock(spec=Instance)
        domain_name = "test_domain"
        instance.set_domain.return_value = domain_name

        self.manager.save_instance(instance)

        instance.set_domain.assert_called_once_with(domain_name)
        self.strategy.save_instance.assert_called_once_with(instance)

    def test_load_instance_with_valid_uuid(self):
        target_class = Mock(spec=Instance)
        uuid = UUID('550e8400-e29b-41d4-a716-446655440000')
        instance = self.manager.load_instance(uuid, target_class)
        self.assertIsInstance(instance, Mock)
        self.assertEqual(instance.uuid, uuid)

    def test_load_instance_with_none_uuid(self):
        target_class = Mock(spec=Instance)
        instance = self.manager.load_instance(None, target_class)
        self.assertIsInstance(instance, Mock)

    def test_load_instance_with_invalid_class(self):
        with self.assertRaises(NotImplementedError):
            self.manager.load_instance(None, None)

    def test_update_instance(self):
        instance = Mock(spec=Instance)
        domain_name = "test_domain"
        instance.set_domain.return_value = domain_name
        updated_instance = self.manager.update_instance(instance)

        instance.set_domain.assert_called_once_with(domain_name)
        self.strategy.update_instance.assert_called_once_with(instance)
        self.assertEqual(updated_instance, self.strategy.update_instance.return_value)

#<---end tests--->

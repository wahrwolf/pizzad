from pathlib import Path
from uuid import UUID, uuid4
import unittest
from unittest.mock import Mock
from pizzad.persistence import DictObject
from pizzad.persistence.strategies import DictPersistenceStrategy


class TestDictPersistenceStrategy(unittest.TestCase):
    def test_save_instance(self):
        strategy = DictPersistenceStrategy()
        instance = Mock(spec=DictObject)
        instance.to_dict.return_value = {"key": "value"}
        instance.uuid = uuid4()
        instance.domain = "test_domain"
        strategy.save_instance(instance)
        file_path = Path(strategy.base_directory, instance.domain, f"{instance.uuid}.json")
        self.assertTrue(file_path.exists())

    def test_update_instance(self):
        strategy = DictPersistenceStrategy()
        instance = Mock(spec=DictObject)
        instance.to_dict.return_value = {"key": "value"}
        instance.uuid = uuid4()
        instance.domain = "test_domain"
        strategy.save_instance(instance)

        new_instance = Mock(spec=DictObject)
        new_instance.to_dict.return_value = {"key": "new_value"}
        new_instance.uuid = instance.uuid
        new_instance.domain = instance.domain

        updated_instance = strategy.update_instance(new_instance)
        self.assertEqual(updated_instance.to_dict(), new_instance.to_dict())

    def test_pick_existing_uuid_or_create_new(self):
        strategy = DictPersistenceStrategy()
        domain = "test_domain"
        uuid = strategy.pick_existing_uuid_or_create_new(domain)
        self.assertIsInstance(uuid, UUID)

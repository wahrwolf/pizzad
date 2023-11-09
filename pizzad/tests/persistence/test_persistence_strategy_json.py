#<---begin import --->
import json
from pathlib import Path
from uuid import UUID, uuid4
import unittest
from tempfile import gettempdir

from pizzad.persistence.strategies import PersistDictAsJSONStrategy
from pizzad.persistence.models import Instance


class TestPersistDictAsJSONStrategy(unittest.TestCase):
    def test_read_dict(self):
        base_directory = Path(gettempdir(), "pizzad", "tests")
        strategy = PersistDictAsJSONStrategy(base_directory)
        domain = "test_domain"
        uuid = uuid4()
        data = {"key": "value"}
        file_path = Path(strategy.base_directory, domain, f"{uuid}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

        read_data = strategy.read_dict(uuid, domain)
        self.assertEqual(read_data, data)

    def test_write_dict(self):
        base_directory = Path(gettempdir(), "pizzad", "tests")
        strategy = PersistDictAsJSONStrategy(base_directory)
        domain = "test_domain"
        uuid = uuid4()
        data = {"key": "value"}
        strategy.write_dict(data, uuid, domain)
        file_path = Path(strategy.base_directory, domain, f"{uuid}.json")
        with open(file_path, "r", encoding="utf-8") as file:
            written_data = json.load(file)
        self.assertEqual(written_data, data)

    def test_pick_existing_uuid_or_create_new(self):
        base_directory = Path(gettempdir(), "pizzad", "tests")
        strategy = PersistDictAsJSONStrategy(base_directory)
        domain = "test_domain"
        uuid = strategy.pick_existing_uuid_or_create_new(domain)
        self.assertIsInstance(uuid, UUID)

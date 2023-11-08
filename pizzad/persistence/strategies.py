import json
from os import mkdir
from pathlib import Path
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Dict

from .models import Instance, InstanceFactory
from .models import DictObject


class PersistenceStrategy(ABC):
    @abstractmethod
    def save_instance(self, instance: Instance):
        pass

    def update_instance(self, instance: Instance) -> Instance:
        pass


class DictPersistenceStrategy(PersistenceStrategy):
    @abstractmethod
    def write_dict(self, data: Dict, uuid: UUID, domain: str):
        pass

    @abstractmethod
    def read_dict(self, uuid: UUID, domain: str) -> Dict:
        pass

    def save_instance(self, instance: Instance):
        if not isinstance(instance, DictObject):
            raise NotImplementedError
        self.write_dict(
                data=instance.to_dict(),
                uuid=instance.uuid, domain=instance.domain)

    def update_instance(self, instance: Instance) -> Instance:
        if not isinstance(instance, DictObject):
            raise NotImplementedError

        old_state = instance.to_dict()
        try:
            dictionary = self.read_dict(
                    uuid=instance.uuid, domain=instance.domain)
            instance.update_from_dict(dictionary)
        except (ValueError, KeyError):
            instance.update_from_dict(old_state)
        return instance


class PersistDictAsJSONStrategy(DictPersistenceStrategy):
    base_directory: Path
    encoding: str

    def __init__(self, base_directory: Path, encoding: str = "utf8"):
        if not base_directory.exists():
            for directory in base_directory.parents[::-1]:
                if not directory.exists():
                    mkdir(directory)

        self.base_directory = base_directory
        self.encoding = encoding

    def set_path(self, base_directory: Path):
        self.base_directory = base_directory

    def read_dict(self, uuid: UUID, domain: str) -> Dict:
        target_file = Path(self.base_directory, domain, f"{str(uuid)}.json")
        try:
            if not Path(target_file.parent).exists():
                mkdir(target_file.parent)
            with open(target_file, "r", encoding=self.encoding) as file:
                data = json.load(file)
        except Exception as error:
            raise error
        return data

    def write_dict(self, data: Dict, uuid: UUID, domain: str):
        target_file = Path(self.base_directory, domain, f"{str(uuid)}.json")
        try:
            if not Path(target_file.parent).exists():
                mkdir(target_file.parent)
            with open(target_file, "w", encoding=self.encoding) as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            raise error

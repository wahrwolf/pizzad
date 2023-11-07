import json
from abc import ABC, abstractmethod


class PersistentObject(ABC):
    @abstractmethod
    def persist(self):
        pass

    @abstractmethod
    def fetch(self):
        pass


class DictObject(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def update_from_dict(self, dictionary: dict):
        pass


class PersistentJSONObject(PersistentObject, DictObject):
    path: str

    def set_path(self, path: str):
        self.path = path

    def fetch(self, path=None, raise_exceptions=False):
        path = path if path else self.path
        old_state = self.to_dict()
        try:
            with open(path, "r") as file:
                data = json.load(file)
                self.update_from_dict(data)
        except Exception as error:
            if raise_exceptions:
                raise error
            self.update_from_dict(old_state)

    def persist(self, path=None, raise_exceptions=False):
        path = path if path else self.path
        data = self.to_dict()

        try:
            with open(path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            if raise_exceptions:
                raise error

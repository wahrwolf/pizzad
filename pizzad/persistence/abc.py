from abc import ABC, abstractmethod
from pizzad.user.abc import User
from pizzad.orders.abc import Order, OrderOption
from pizzad.models.pattern import Entity,  MementoOriginator, Memento, MementoCaretaker
from pizzad.models.implementations import Registry


class RestoreableRegistry(Registry, MementoOriginator):

    class RegistryMemento(Entity, Memento):
        def __init__(self, entities: set[Entity]):
            super().__init__()
            self._entities = entities

        def _get_entities(self):
            return self._entities

    def clear_registry(self):
        self._registry = {}
        return self

    def save(self) -> RegistryMemento:
        return RestoreableRegistry.RegistryMemento(self.get_all_members())

    def restore(self, memento: RegistryMemento):
        self.clear_registry()
        for entity in memento._get_entities():
            self.register_member(entity)
        return self


class SerializationStrategy:
    @abstractmethod
    @staticmethod
    def serialize_to_dict(obj: object):
        raise NotImplementedError


class UserSerializationStrategy(SerializationStrategy):
    @staticmethod
    @abstractmethod
    def serialize_to_dict(
            user: User
            ) -> dict:
        raise NotImplementedError


class OrderSerializationStrategy(SerializationStrategy):
    @staticmethod
    @abstractmethod
    def serialize_to_dict(
            order: Order
            ) -> dict:
        raise NotImplementedError


class OrderOptionSerializationStrategy(SerializationStrategy):
    @staticmethod
    @abstractmethod
    def serialize_to_dict(
            option: OrderOption
            ) -> dict:
        raise NotImplementedError


class RegistryMementoSerializationStrategy(SerializationStrategy):
    @staticmethod
    @abstractmethod
    def serialize_to_dict(
            memento: RestoreableRegistry.RegistryMemento
            ) -> dict:
        raise NotImplementedError


class DeserializationStrategy:
    @abstractmethod
    @staticmethod
    def deserialize_from_dict(serialized_data: dict) -> object:
        raise NotImplementedError
    pass


class UserDeserializationStrategy(DeserializationStrategy):
    @staticmethod
    @abstractmethod
    def deserialize_from_dict(
            serialized_data: dict
            ) -> User:
        raise NotImplementedError


class OrderDeserializationStrategy(DeserializationStrategy):
    @staticmethod
    @abstractmethod
    def deserialize_from_dict(
            serialized_data: dict
            ) -> Order:
        raise NotImplementedError


class OrderOptionDeserializationStrategy(DeserializationStrategy):
    @staticmethod
    @abstractmethod
    def deserialize_from_dict(
            serialized_data: dict
            ) -> OrderOption:
        raise NotImplementedError


class RegistryMementoDeserializationStrategy(DeserializationStrategy):
    @staticmethod
    @abstractmethod
    def deserialize_from_dict(
            serialized_data: dict
            ) -> RestoreableRegistry.RegistryMemento:
        raise NotImplementedError


class Archive(MementoCaretaker):
    def restore_registry_from_url(url: str, registry: RestoreableRegistry):
        raise NotImplementedError
    pass

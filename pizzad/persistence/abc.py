from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from pizzad.user.abc import User
from pizzad.orders.abc import Order, OrderOption
from pizzad.models.pattern import (
        Entity,  MementoOriginator,  MementoCaretaker, Builder)
from pizzad.models.implementations import Registry, Snapshot


class RestoreableRegistry(Registry, MementoOriginator):

    class RegistrySnapshot(Snapshot):
        def __init__(self, entities: set[Entity],
                     uuid: Optional[UUID] = None,
                     version: Optional[int] = None):
            super().__init__(uuid=uuid, version=version)
            self._entities = entities

        def _get_entities(self):
            return self._entities

    def clear_registry(self):
        self._registry = {}
        return self

    def save(self) -> RegistrySnapshot:
        return RestoreableRegistry.RegistrySnapshot(self.get_all_members())

    def restore(self, memento: RegistrySnapshot):
        self.clear_registry()
        for entity in memento._get_entities():
            self.register_member(entity)
        return self


class RegistryBuilder(Builder):
    memento: RestoreableRegistry.RegistrySnapshot
    serialized_data: dict
    entity_data_dicts: list[dict]
    entities: set[Entity]

    def __init__(self, serialized_data: dict):
        self.serialized_data = serialized_data

    @abstractmethod
    def setup(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError

    @abstractmethod
    def dereference_foreign_references(self, data: dict) -> dict:
        raise NotImplementedError

    def dereference_data_dicts(self):
        self.entity_data_dicts = map(
                self.dereference_foreign_references, self.entity_data_dicts)

    @abstractmethod
    def build_entity(self, serialized_data: dict) -> Entity:
        raise NotImplementedError

    def build_entities(self):
        self.entities = map(self.build_entities, self.entity_data_dicts)

    def build_registry_memento(self):
        self.memento = RestoreableRegistry.RegistrySnapshot(
                entities=set(self.entity_data_dicts),
                uuid="",
                version=""
        )

    def build_registry(self):
        self.reset()
        self.dereference_data_dicts()
        self.build_entities()
        self.build_registry_memento()

        registry = RestoreableRegistry().restore(self.memento)
        return registry


class UserRegistryBuilder(RegistryBuilder):
    @abstractmethod
    def build_user_registry(self, serialized_data) -> RestoreableRegistry:
        raise NotImplementedError


class OrderRegistryBuilder(RegistryBuilder):
    @abstractmethod
    def build_order_registry(self, serialized_data) -> RestoreableRegistry:
        raise NotImplementedError


class SerializedDictSnapshot(Snapshot):
    pass


class SerializableSnapshot(Snapshot, MementoOriginator):
    def save(self) -> SerializedDictSnapshot:
        raise NotImplementedError

    def restore(self, memento: SerializedDictSnapshot):
        raise NotImplementedError


class Archive(MementoCaretaker):
    pass


class ArchiveServer(ABC):
    def put(self, serialized_data: dict) -> UUID:
        raise NotImplementedError

    def get(self, uuid: UUID) -> dict:
        raise NotImplementedError

    def options(self, url: str) -> set[str]:
        raise NotImplementedError

    def head(self, url: str) -> UUID:
        raise NotImplementedError


class SerializedDataBuilder(Builder):
    memento: RestoreableRegistry.RegistrySnapshot
    serialized_data: dict
    entity_data_dicts: list[dict]
    registry: RestoreableRegistry

    def __init__(self, registry):
        self.registry = registry

    def set_registry(self, registry: RestoreableRegistry):
        self.reset()
        self.registry = registry

    def reset(self):
        self.serialized_data = {}
        self.entity_data_dicts = []
        self.memento = None

    def build_registry_memento(self):
        self.memento = self.registry.save()

    @abstractmethod
    def build_data_dict(self, entity: Entity) -> dict:
        raise NotImplementedError

    def build_entity_data_dicts(self):
        self.entity_data_dicts = map(
                self.build_data_dict, self.memento._get_entities())

    @abstractmethod
    def replace_foreign_entities_with_rerefences(self, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def build_serialized_data(self):
        raise NotImplementedError


class UserRegistrySerializer(SerializedDataBuilder):
    pass

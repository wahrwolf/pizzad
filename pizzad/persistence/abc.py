from abc import ABC, abstractmethod
from copy import deepcopy
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
            self._entities = deepcopy(entities)

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

    def reset(self):
        self.serialized_data = {}
        self.memento = None
        self.entity_data_dicts = []
        self.entities = {}

    def __init__(self):
        self.reset()

    def set_serialized_data(self, data: dict):
        self.serialized_data = data

    @abstractmethod
    def dereference_foreign_references(self, data: dict) -> dict:
        raise NotImplementedError

    def dereference_data_dicts(self):
        self.entity_data_dicts = list(map(
                self.dereference_foreign_references, self.serialized_data))

    @abstractmethod
    def build_entity(self, serialized_data: dict) -> Entity:
        raise NotImplementedError

    def build_entities(self):
        self.entities = set(map(self.build_entity, self.entity_data_dicts))

    def build_registry_memento(self):
        self.memento = RestoreableRegistry.RegistrySnapshot(
                entities=self.entities,
                uuid="",
                version=""
        )

    def build_registry(self, data: dict):
        self.reset()
        self.set_serialized_data(data)
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
    def __init__(
            self, data: dict,
            uuid: Optional[UUID] = None,
            version: Optional[str] = None):
        super().__init__(uuid=uuid, version=version)
        self._data = data

    def to_dict(self):
        return self._data


class SerializableSnapshot(Snapshot, MementoOriginator):

    def to_dict(self) -> dict:
        raise NotImplementedError

    def from_dict(self, dict):
        raise NotImplementedError

    def save(self) -> SerializedDictSnapshot:
        return SerializedDictSnapshot(self.to_dict())

    def restore(self, memento: SerializedDictSnapshot):
        return self.from_dict(memento.to_dict())


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

    def reset(self):
        self.serialized_data = {}
        self.entity_data_dicts = []
        self.memento = None
        self.registry = None

    def __init__(self):
        self.reset()

    def set_registry(self, registry: RestoreableRegistry):
        self.reset()
        self.registry = registry

    def build_registry_memento(self):
        self.memento = self.registry.save()

    @abstractmethod
    def build_data_dict_from_entity(self, entity: Entity) -> dict:
        raise NotImplementedError

    def build_entity_data_dicts(self):
        self.entity_data_dicts = list(map(
                self.build_data_dict_from_entity, self.memento._get_entities()))

    @abstractmethod
    def replace_foreign_entities_with_rerefences(self, data: dict) -> dict:
        raise NotImplementedError

    def isolate_entities(self):
        self.entity_data_dicts = list(map(
                self.replace_foreign_entities_with_rerefences,
                self.entity_data_dicts))

    def serialize_registry(self, registry: RestoreableRegistry):
        self.reset()
        self.set_registry(registry)
        self.build_registry_memento()
        self.build_entity_data_dicts()
        self.isolate_entities()
        return self.entity_data_dicts


class UserRegistrySerializer(SerializedDataBuilder):
    @abstractmethod
    def build_data_dict_from_user(self, user: User) -> dict:
        raise NotImplementedError

    def build_data_dict_from_entity(self, entity: Entity) -> dict:
        if isinstance(entity, User):
            return self.build_data_dict_from_user(entity)
        raise NotImplementedError

    def serialize_user_registry(self, registry: RestoreableRegistry):
        pass

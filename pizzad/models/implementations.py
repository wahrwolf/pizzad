from abc import ABC, abstractmethod
from uuid import UUID
from functools import reduce
from .pattern import Entity, EntityRegistry, MementoOriginator, Memento


class Registry(EntityRegistry):
    _registry: dict

    def __init__(self):
        super().__init__()
        self._registry = {}

    def register_member(self, entity: Entity):
        self._registry[entity.get_uuid()] = entity

    def delete_member_by_id(self, uuid: UUID) -> None:
        del self._registry[uuid]
        return self

    def get_all_members(self) -> set[Entity]:
        return set(self._registry.values())

    def get_member_by_id(self, uuid: UUID) -> Entity:
        return self._registry[uuid]

    def __contains__(self, other):
        if isinstance(other, Entity):
            return (
                    other.uuid in self._registry and
                    self._registry[other.uuid].get_domain() == other.get_domain())
        return False


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

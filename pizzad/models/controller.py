from uuid import UUID
from typing import Optional
from .entities import Entity, EntityFactory
from .pattern import Singleton, Registry, MementoOriginator, Factory, Memento


class Controller(Singleton, MementoCaretaker):
    _registry: Registry
    _factory: Factory
    _memento_strategy: Strategy

    def set_factory(self, factory: Registry):
        self._factory = factory
        return self

    def set_registry(self, registry: Registry):
        self._registry = registry

    def reset_registry(self):
        self._registry.clear()
        return self

    def register_entity(self, entity: Entity):
        self._registry[entity.uuid] = entity

    def remove_entity(self, uuid: UUID):
        del self._registry[uuid]
        return self

    def get_entity(self, uuid: UUID) -> Entity:
        return self._registry[uuid]

    def create_entity(self):
        entity = self._factory.create_entity()
        self.register_entity(entity)
        return entity

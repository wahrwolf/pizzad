from uuid import UUID
from typing import Optional
from .entities import Entity, EntityFactory
from .pattern import Singleton


class Controller(Singleton):
    _registry: dict
    _factory: EntityFactory

    def register_factory(self, factory: EntityFactory):
        self._factory = factory
        return self

    def reset_registry(self):
        self._registry.clear()
        return self

    def register_entity(self, entity: Entity):
        self._registry[entity.uuid] = entity

    def remove_entity(self, uuid: UUID):
        del self._registry[uuid]
        return self

    def remove_entity_or_nop(self, uuid: UUID):
        try:
            self.remove_entity(uuid)
        except KeyError:
            pass

    def get_entity(self, uuid: UUID) -> Entity:
        return self._registry[uuid]

    def create_entity(self):
        entity = self._factory.create_entity()
        self.register_entity(entity)
        return entity

    def get_or_create_entity(self, uuid: Optional[UUID] = None) -> Entity:
        try:
            entity = self.get_entity(uuid)
        except KeyError:
            entity = self.create_entity()
            if uuid:
                entity.set_uuid(uuid)
        return entity

    def update_from_dict(self, data: dict):
        if data == {}:
            self.reset_registry()
        else:
            for entity_uuid, entity_data in data.get("registry", {}).items():
                uuid = UUID(entity_uuid)
                self.get_or_create_entity(uuid).update_from_dict(entity_data)

    def to_dict(self) -> dict:
        return {
                "registry": {
                    str(uuid): entity.to_dict()
                    for uuid, entity in self._registry.items()
                }
        }

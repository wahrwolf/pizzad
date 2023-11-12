from uuid import UUID
from .entities import Entity
from .pattern import Registry


class DictRegistry(Registry):
    _registry: dict

    def clear_registry(self):
        self._registry = {}
        return self

    def register_member(self, entity: Entity):
        self._registry[entity.uuid] = entity

    def delete_member_by_id(self, uuid: UUID) -> None:
        del self._registry[uuid]
        return self

    def get_all_members(self) -> set[Entity]:
        return set(self._registry.values())

    def get_member_by_id(self, uuid: UUID) -> Entity:
        return self._registry[uuid]

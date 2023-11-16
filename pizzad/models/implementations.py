from uuid import UUID
from .pattern import Entity, EntityRegistry


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

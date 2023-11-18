from uuid import UUID
from datetime import datetime
from typing import Optional
from .pattern import Entity, EntityRegistry, Memento


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


class Snapshot(Memento):
    def __init__(self, uuid: Optional[UUID] = None, version: Optional[int] = None):
        super().__init__(uuid=uuid)
        self._version = version if version else datetime.now().strftime('%s')

    def __lt__(self, other):
        if isinstance(other, Snapshot):
            return self.get_version().__lt__(other.get_version)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Snapshot):
            return self.get_version().__le__(other.get_version)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Snapshot):
            return self.get_version().__gt__(other.get_version)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Snapshot):
            return self.get_version().__ge__(other.get_version)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Snapshot):
            return self.get_uuid() == other.get_uuid()
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Snapshot):
            return self.get_uuid() != other.get_uuid()
        return NotImplemented

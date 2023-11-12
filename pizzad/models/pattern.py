from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Entity


class Singleton(Entity):
    _instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Registry(ABC):
    def register_member(self, entity: Entity):
        raise NotImplementedError

    def get_all_members(self) -> set[Entity]:
        raise NotImplementedError

    def get_member_by_id(self, uuid: UUID) -> Entity:
        raise NotImplementedError

    def delete_member_by_id(self, uuid: UUID) -> None:
        raise NotImplementedError


class Service(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        raise NotImplementedError


class Visitor(ABC):
    @abstractmethod
    def visit(self, service: Service):
        raise NotImplementedError

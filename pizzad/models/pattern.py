from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID, uuid4


class Entity(ABC):
    _uuid: UUID

    def __init__(self, uuid: Optional[UUID] = None):
        self._uuid = uuid if uuid else uuid4()

    def get_uuid(self):
        return self._uuid


class Singleton(Entity):
    _instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class EntityRegistry(ABC):
    def register_member(self, entity: Entity):
        raise NotImplementedError

    def get_all_members(self) -> set[Entity]:
        raise NotImplementedError

    def get_member_by_id(self, uuid: UUID) -> Entity:
        raise NotImplementedError

    def delete_member_by_id(self, uuid: UUID) -> None:
        raise NotImplementedError


class Product(ABC):
    pass


class Factory(ABC):
    @abstractmethod
    def create_new(self, **kwargs) -> Product:
        raise NotImplementedError


class Strategy(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        raise NotImplementedError


class Context(ABC):
    _strategy: Strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def execute_strategy(self, **kwargs):
        return self._strategy.execute(**kwargs)


class Memento(ABC):
    pass


class MementoOriginator(ABC):
    @abstractmethod
    def save(self) -> Memento:
        raise NotImplementedError

    @abstractmethod
    def restore(self, memento: Memento):
        raise NotImplementedError


class MementoCaretaker(ABC):
    history: list[Memento]

    def undo(self, originator: MementoOriginator) -> MementoOriginator:
        memento = self.history.pop()
        originator.restore(memento)
        return originator

    def save(self, originator: MementoOriginator):
        memento = originator.save()
        self.history.append(memento)


class Service(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        raise NotImplementedError


class Visitor(ABC):
    @abstractmethod
    def visit(self, service: Service):
        raise NotImplementedError

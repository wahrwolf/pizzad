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
    @abstractmethod
    def restore(self) -> 'MementoOriginator':
        raise NotImplementedError


class MementoOriginator(ABC):
    @abstractmethod
    def save(self) -> Memento:
        raise NotImplementedError


class MementoCaretaker(ABC):
    history: list[Memento]

    def undo(self) -> MementoOriginator:
        return self.history.pop().restore()


class Service(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        raise NotImplementedError


class Visitor(ABC):
    @abstractmethod
    def visit(self, service: Service):
        raise NotImplementedError

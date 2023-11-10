from .entities import Entity
from abc import ABC, abstractmethod


class Singleton(Entity):
    _instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class Service(ABC):
    @abstractmethod
    def accept(self, visitor: 'Visitor'):
        raise NotImplementedError


class Visitor(ABC):
    @abstractmethod
    def visit(self, service: Service):
        raise NotImplementedError

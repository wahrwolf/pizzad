from abc import ABC, abstractmethod
from typing import Set, Optional, Dict
from .events import Event


class Observer(ABC):
    @abstractmethod
    def update(self, event: Event):
        pass


class Observerable(ABC):
    observers: Set[Observer]

    def notify_observers(self, event: Event):
        for observer in self.observers:
            observer.update(event)

    def add_observer(self, observer: Observer):
        self.observers.add(observer)

from abc import ABC, abstractmethod
from inspect import getmodule, isclass
from uuid import UUID, uuid4
from typing import Optional


class DictObject(ABC):

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError

    @abstractmethod
    def update_from_dict(self, data: dict):
        raise NotImplementedError


class Entity:
    uuid: UUID
    domain: str

    def __init__(self,
                 uuid: Optional[UUID] = None,
                 domain: Optional[str] = None):
        self.uuid = uuid if uuid else uuid4()
        if not domain:
            module_name = getmodule(self).__name__
            class_name = self.__class__.__name__
            domain = f"{module_name}.{class_name}"
        self.domain = domain

    def set_uuid(self, uuid: UUID):
        self.uuid = uuid

    def get_uuid(self) -> UUID:
        return self.uuid

    def set_domain(self, domain: str):
        self.domain = domain

    def get_domain(self) -> str:
        return self.domain

    def __str__(self):
        return f"{self.domain}[{self.uuid}]"

    def __repr__(self):
        return f"{self.domain}[{self.uuid}]"

    def __eq__(self, other):
        return (
                isinstance(other, Entity) and (
                    self.domain == other.domain and
                    self.uuid == other.uuid
                    )
                )


class EntityFactory(ABC):
    module_name: str
    class_name: str

    def __init__(self, target_class=None):
        if target_class:
            self.imprint_class(target_class)

    def imprint_class(self, target_class):
        if not isclass(target_class):
            raise NotImplementedError(
                    "target_class {str(target_class}is not a class."
                    "This factory can only be imprinted by classes!")
        self.module_name = getmodule(target_class).__name__
        self.class_name = target_class.__name__

    def create_entity(self) -> Entity:
        try:
            module = __import__(self.module_name, fromlist=[self.class_name])
            return getattr(module, self.class_name)()
        except Exception as error:
            raise error

    def __str__(self):
        return f"Factory[{self.class_name}@{self.module_name}]"

    def __repr__(self):
        return f"Factory[{self.class_name}@{self.module_name}]"

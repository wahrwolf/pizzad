from abc import ABC, abstractmethod
from inspect import getmodule, isclass
from uuid import UUID
from .pattern import Entity, Factory
from typing import Optional


class DomainEntity(Entity):
    _domain: str

    def __init__(self,
                 uuid: Optional[UUID] = None,
                 domain: Optional[str] = None):
        super().__init__(uuid)
        if not domain:
            module_name = getmodule(self).__name__
            class_name = self.__class__.__name__
            domain = f"{module_name}.{class_name}"
        self._domain = domain

    def get_domain(self) -> str:
        return self._domain

    def __str__(self):
        return f"{self._domain}[{self._uuid}]"

    def __repr__(self):
        return f"{self._domain}[{self._uuid}]"

    def __eq__(self, other):
        return (
                isinstance(other, Entity) and (
                    self._domain == other._domain and
                    self._uuid == other._uuid
                    )
                )

    def __hash__(self):
        return hash((self._uuid, self._domain))


class EntityFactory(Factory):
    _module_name: str
    _class_name: str

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

    def create_new(self, target_class, **kwargs):
        self.imprint_class(target_class)
        return self.create_entity()

    def __str__(self):
        return f"Factory[{self.class_name}@{self.module_name}]"

    def __repr__(self):
        return f"Factory[{self.class_name}@{self.module_name}]"

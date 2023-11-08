from abc import ABC, abstractmethod
from inspect import getmodule
from uuid import UUID, uuid4
from typing import Dict, Optional


class Instance():
    uuid: UUID
    domain: str

    @staticmethod
    def create_empty_instance():
        raise NotImplementedError

    def __init__(self, domain: str = '',  uuid: Optional[UUID] = None):
        self.uuid = uuid if uuid else uuid4()
        self.domain = domain

    def set_uuid(self, uuid: UUID):
        self.uuid = uuid

    def get_uuid(self) -> UUID:
        return self.uuid

    def set_domain(self, domain: str):
        self.domain = domain

    def get_domain(self) -> str:
        return self.domain


class InstanceFactory(ABC):
    @staticmethod
    def build_domain_name(module_name: str, class_name: str):
        return f"{module_name}.{class_name}"

    @staticmethod
    def build_domain_name_from_object(obj) -> str:
        module_name = getmodule(obj).__name__
        class_name = obj.__class__.__name__
        return InstanceFactory.build_domain_name(module_name, class_name)

    @staticmethod
    def create_instance_from_class(target_class):
        try:
            instance = target_class.create_empty_instance()
            instance.set_domain(
                    InstanceFactory.build_domain_name_from_object(instance))
            return instance
        except Exception as error:
            raise ValueError(f"Error creating instance: {error}")

    @staticmethod
    def build_class(module_name, class_name):
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name).create_instance()

    @staticmethod
    def create_instance(module_name: str, class_name: str) -> Instance:
        try:
            instance_class = InstanceFactory.build_class(module_name, class_name)
            instance = InstanceFactory.create_instance_from_class(instance_class)
            return instance
        except Exception as error:
            raise ValueError(f"Error creating instance: {error}")


class DictObject(Instance):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def update_from_dict(self, dictionary: Dict):
        pass

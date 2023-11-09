from typing import Dict, Optional
from uuid import UUID
from inspect import getmodule, isclass
from .models import Instance, InstanceFactory
from .strategies import PersistenceStrategy


class PersistenceManager():
    strategy: PersistenceStrategy

    def __init__(self, strategy: Optional[PersistenceStrategy] = None):
        self.strategy = strategy

    def set_strategy(self, strategy: PersistenceStrategy):
        self.strategy = strategy

    def save_instance(self, instance: Instance):
        domain = InstanceFactory.build_domain_name_from_object(instance)
        instance.set_domain(domain)
        self.strategy.save_instance(instance)

    def load_instance(self, uuid: Optional[UUID], target_class):
        if not isclass(target_class):
            raise NotImplementedError
        print(f"Loading {target_class.__name__}[{uuid}] from storage")
        instance = InstanceFactory.create_instance_from_class(target_class)

        if uuid is None:
            uuid = self.strategy.pick_existing_uuid_or_create_new(
                    InstanceFactory.build_domain_name_from_object(instance))

        instance.set_uuid(uuid)
        self.update_instance(instance)
        return instance

    def update_instance(self, instance: Instance):
        instance.set_domain(InstanceFactory.build_domain_name_from_object(instance))
        print(f"Update {instance.domain}[{instance.uuid}] from storage")
        instance = self.strategy.update_instance(instance)
        return instance

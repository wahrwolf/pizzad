from pizzad.models.pattern import Entity
from pizzad.models.implementations import Registry, Snapshot
from pizzad.user import User
from pizzad.food import Ingredient, Allergen
from .abc import RestoreableRegistry, UserRegistryBuilder, SerializedDataBuilder


class ConcreteUserRegistryBuilder(UserRegistryBuilder):
    def dereference_foreign_references(self, registry: Registry):
        pass

    def build_entity(self, serialized_data: dict) -> Entity:
        raise NotImplementedError

    def build_registry_memento(self):
        raise NotImplementedError

    def build_registry(self):
        return RestoreableRegistry().restore(self.memento)

    def build_user_registry(self, serialized_data) -> RestoreableRegistry:
        raise NotImplementedError


class ConcreteUserRegistrySerializer(SerializedDataBuilder):
    def build_data_dict(self, user: User) -> dict:
        data = {
                "user_name": user.get_name(),
                "allergies": list(user.get_allergies()),
                "excluded_ingredients": list(user.get_excluded_ingredients()),
                "preferred_ingredients": list(user.get_preferred_ingredients()),
                "user_type": user.get_type(),
                "uuid": user.get_uuid(),
        }

        return data

    def replace_foreign_entities_with_rerefences(
            self, data: dict) -> dict:
        data["uuid"] = str(data["uuid"])
        data["allergies"] = map(str, data["allergies"])
        data["excluded_ingredients"] = map(str, data["excluded_ingredients"])
        data["preferred_ingredients"] = map(str, data["preferred_ingredients"])
        data["user_type"] = data["user_type"].value

        return data

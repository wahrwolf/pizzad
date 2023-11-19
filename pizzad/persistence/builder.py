from uuid import UUID
from pizzad.models.pattern import Entity
from pizzad.models.implementations import Registry, Snapshot
from pizzad.user import User, UserType
from pizzad.user.factories import UserEntityFactory
from pizzad.food import Ingredient, Allergen
from .abc import RestoreableRegistry, UserRegistryBuilder, SerializedDataBuilder


class ConcreteUserRegistryBuilder(UserRegistryBuilder):
    def setup(self, **kwargs):
        pass

    def reset(self):
        self.memento = None
        self.serialized_data = {}
        self.entity_data_dicts = []
        self.entities = set[Entity]

    def dereference_foreign_references(self, data: dict) -> dict:
        data = {}
        data["uuid"] = UUID(data["uuid"])
        data["allergies"] = map(
                lambda allergen: (Allergen[allergen]), data["allergies"])
        data["excluded_ingredients"] = map(
                lambda ingredient: (Ingredient[ingredient]),
                data["excluded_ingredients"])
        data["preferred_ingredients"] = map(
                lambda ingredient: (Ingredient[ingredient]),
                data["preferred_ingredients"])
        data["user_type"] = UserType[data["user_type"]]
        return data

    def build_entity(self, serialized_data: dict) -> Entity:
        user = UserEntityFactory.restore_user(
                uuid=serialized_data["uuid"],
                name=serialized_data["user_name"],
                type=serialized_data["user_type"]
        )
        map(user.add_allergy, serialized_data["allergies"])
        map(user.add_prefereed_ingredient, serialized_data["preferred_ingredients"])
        map(user.add_excluded_ingredient, serialized_data["excluded_ingredients"])
        return user

    def build_user_registry(self) -> RestoreableRegistry:
        self.reset()



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

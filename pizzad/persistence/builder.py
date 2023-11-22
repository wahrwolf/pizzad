from uuid import UUID
from datetime import datetime
from pizzad.models.pattern import Entity
from pizzad.models.implementations import Registry, Snapshot
from pizzad.user import User, UserType
from pizzad.user.factories import UserEntityFactory
from pizzad.orders.abc import Order, OrderOption
from pizzad.orders.factories import (
        OrderEntityFactory, OrderOptionEntitiyFactory)
from pizzad.food import Ingredient, Allergen
from .abc import (
        RestoreableRegistry,
        UserRegistryBuilder, UserRegistrySerializer,
        OrderRegistryBuilder, OrderRegistrySerializer,
        OrderOptionRegistryBuilder, OrderOptionRegistrySerializer
        )


class ConcreteUserRegistryBuilder(UserRegistryBuilder):
    def dereference_foreign_references(self, serialized_data: dict) -> dict:
        serialized_data["uuid"] = UUID(serialized_data["uuid"])
        serialized_data["allergies"] = list(map(
                lambda allergen: (Allergen[allergen]), serialized_data["allergies"]))
        serialized_data["excluded_ingredients"] = list(map(
                lambda ingredient: (Ingredient[ingredient]),
                serialized_data["excluded_ingredients"]))
        serialized_data["preferred_ingredients"] = list(map(
                lambda ingredient: (Ingredient[ingredient]),
                serialized_data["preferred_ingredients"]))
        serialized_data["user_type"] = UserType[serialized_data["user_type"]]
        return serialized_data

    def build_entity(self, data: dict) -> Entity:
        user = UserEntityFactory.restore_user(
                uuid=data["uuid"],
                name=data["user_name"],
                type=data["user_type"]
        )
        map(user.add_allergy, data["allergies"])
        map(user.add_prefereed_ingredient, data["preferred_ingredients"])
        map(user.add_excluded_ingredient, data["excluded_ingredients"])
        return user


class ConcreteUserRegistrySerializer(UserRegistrySerializer):
    def build_data_dict_from_user(self, user: User) -> dict:
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
        data["allergies"] = list(map(str, data["allergies"]))
        data["excluded_ingredients"] = list(map(str, data["excluded_ingredients"]))
        data["preferred_ingredients"] = list(map(str, data["preferred_ingredients"]))
        data["user_type"] = data["user_type"].name

        return data


class ConcreteOptionRegistryBuilder(OrderOptionRegistryBuilder):
    def dereference_foreign_references(self, serialized_data: dict) -> dict:
        serialized_data["uuid"] = UUID(serialized_data["uuid"])
        serialized_data["ingredients"] = list(map(
                lambda ingredient: (Ingredient[ingredient]),
                serialized_data["ingredients"]))
        return serialized_data

    def build_entity(self, data: dict) -> Entity:
        option = OrderOptionEntitiyFactory.restore_option(
                name=data["name"], uuid=data["uuid"])
        map(option.add_ingredient, data["ingredients"])
        return option


class ConcreteOptionRegistrySerializer(OrderOptionRegistrySerializer):
    def build_data_dict_from_option(self, option: OrderOption) -> dict:
        data = {
                "option_name": option.get_name(),
                "ingredients": list(option.get_ingredients()),
                "uuid": option.get_uuid(),
        }

        return data

    def replace_foreign_entities_with_rerefences(
            self, data: dict) -> dict:
        data["uuid"] = str(data["uuid"])
        data["ingredients"] = list(map(str, data["ingredients"]))

        return data


class ConcreteOrderRegistrySerializer(OrderRegistrySerializer):
    def build_data_dict_from_order(self, order: Order) -> dict:
        data = {
                "order_name": order.get_name(),
                "options": list(order.get_all_options()),
                "registrations": order.get_all_registrations(),
                "uuid": order.get_uuid(),
                "tags": list(order.get_tags()),
                "created_at": order.get_creation_timestamp(),
        }
        if order.get_closure_timestamp():
            data["closed_since"] = order.get_closure_timestamp()
        if order.get_opening_timestamp():
            data["open_since"] = order.get_opening_timestamp()

        return data

    def replace_foreign_entities_with_rerefences(
            self, data: dict) -> dict:
        data["uuid"] = str(data["uuid"])
        data["options"] = list(map(
            lambda option: (str(option.get_uuid())), data["options"]))
        data["created_at"] = data["created_at"].strftime('%s')

        if "closed_since" in data:
            data["closed_since"] = data["closed_since"].strftime('%s')

        if "open_since" in data:
            data["open_since"] = data["open_since"].strftime('%s')

        data["registrations"] = {
                str(uuid): list(map(lambda user: (str(user.get_uuid()))))
                for uuid, users in data["registrations"].items()
        }

        return data


class ConcreteOrderRegistryBuilder(OrderRegistryBuilder):
    def dereference_foreign_references(self, serialized_data: dict) -> dict:
        data = {
                "uui": UUID(serialized_data["uuid"]),
                "options": set(map(
                    self.options.get_member_by_id, serialized_data["options"])),
        }

        data["registrations"] = [
                (
                    self.options.get_member_by_id(option_id),
                    self.users.get_member_by_id(user_id),

                )
                for option_id, users in serialized_data["registrations"].items()
                for user_id in users 
        ]

        data["created_at"] = datetime.fromtimestamp(
                serialized_data["created_at"])

        if "closed_since" in serialized_data:
            data["closed_since"] = datetime.fromtimestamp(
                    serialized_data["closed_since"])

        if "open_since" in serialized_data:
            data["open_since"] = datetime.fromtimestamp(
                    serialized_data["open_since"])

        return data

    def build_entity(self, data: dict) -> Entity:
        order = OrderEntityFactory.restore_order(
                uuid=data["uuid"],
                name=data["order_name"],
                created_at=data["created_at"],
                closed_since=data.get("closed_since"),
                open_since=data.get("open_since")
        )

        map(order.add_option(data["options"]))
        map(
                lambda args: (order.register_user_for_option(**args)),
                data["registrations"]
        )
        map(order.add_tag, data["tags"])

        return order

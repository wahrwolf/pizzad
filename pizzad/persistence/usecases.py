from uuid import UUID
from pizzad.user.abc import User
from pizzad.orders.abc import Order, OrderOption
from .abc import RestoreableRegistry, UserRegistryBuilder, SerializedDataGateway, SerializedDataBuilder


def restore_user_registry_from_url(
        builder: UserRegistryBuilder, gateway: SerializedDataGateway, url: str) -> RestoreableRegistry:
    data = gateway.get(url)
    registry = builder.build_registry(data)
    return registry


def restore_order_registry_from_url():
    pass

def restore_order_option_registry_from_url():
    pass


def save_user_registry_to_url(
        builder: SerializedDataBuilder, gateway: SerializedDataGateway, registry: RestoreableRegistry, url: str):
    data = builder.build_serialized_data(registry)
    gateway.put(data, url)


def save_order_registry_to_url():
    pass

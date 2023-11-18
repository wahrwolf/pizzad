from uuid import UUID
from pizzad.user.abc import User
from pizzad.orders.abc import Order, OrderOption
from .abc import (
        RestoreableRegistry, UserRegistryBuilder,
        Archive, SerializedDataBuilder)


def restore_user_registry_from_url(
        builder: UserRegistryBuilder,
        archive: Archive, url: str
        ) -> RestoreableRegistry:
    archive.connect(url)
    data = archive.get()
    registry = builder.build_user_registry(data)
    return registry


def restore_order_registry_from_url():
    pass


def restore_order_option_registry_from_url():
    pass


def save_user_registry_to_url(
        builder: SerializedDataBuilder,
        archive: Archive, registry: RestoreableRegistry, url: str):
    data = builder.build_serialized_data(registry)
    archive.put(data, url)


def save_order_registry_to_url():
    pass

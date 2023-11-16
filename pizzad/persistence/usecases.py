from uuid import UUID
from pizzad.user.abc import User
from pizzad.orders.abc import Order, OrderOption
from .abc import RestoreableRegistry, DeserializationStrategy, SerializationStrategy, Archive


def restore_registry_from_url(
        registry: RestoreableRegistry, url: str, archive: Archive
        ) -> RestoreableRegistry:
    archive.restore_registry_from_url(url=url, registry=registry)
    return registry


def restore_registry_from_memento(
        registry: RestoreableRegistry,
        memento: RestoreableRegistry.RegistryMemento
        ) -> RestoreableRegistry:
    registry.clear_registry()
    registry.restore(memento)
    return registry


def restore_registry_memento_from_serialized_dict(
        strategy: DeserializationStrategy,
        serialized_data: dict
        ) -> RestoreableRegistry.RegistryMemento:
    memento = strategy.deserialize_from_dict(serialized_data)
    return memento


def restore_user_from_serialized_dict(
        strategy: DeserializationStrategy,
        serialized_data: dict
        ) -> User:
    pass


def restore_order_from_serialized_dict(
        strategy: OrderDeserializationStrategy,
        serialized_data: dict
        ) -> Order:
    pass


def restore_order_option_from_serialized_dict(
        strategy: OrderOptionDeserializationStrategy,
        serialized_data: dict
        ) -> OrderOption:
    pass


def restore_serialized_dict_from_json(path: Path) -> dict:
    pass


def save_registry_as_json(
        registry: RestoreableRegistry, path: Path) -> RestoreableRegistry:
    pass


def save_registry_as_memento(registry: RestoreableRegistry
                             ) -> RestoreableRegistry.RegistryMemento:
    pass


def save_user_as_serialized_dict(
        user: User,
        strategy: SerializationStrategy
        ) -> dict:
    pass


def save_order_as_serialized_dict(
        order: Order,
        strategy: SerializationStrategy
        ) -> dict:
    pass


def save_order_option_as_serialized_dict(
        option: OrderOption,
        strategy: SerializationStrategy
        ) -> dict:
    pass


def save_serialized_dict_as_json(serialized_data: dict, path: Path) -> None:
    pass


def get_available_registry_versions(archive: Archive) -> set[UUID]:
    pass


def restore_registry_version(
        uuid: UUID,
        archive: Archive,
        registry: RestoreableRegistry
        ) -> RestoreableRegistry:
    pass

from uuid import UUID
from .abc import User, UserFactory, UserRegistry


def create_new_user(user_name: str,
                    factory: UserFactory,
                    registry: UserRegistry
                    ) -> User:
    user = factory.create_user(name=user_name)
    registry.register_member(user)
    return user


def get_users_by_query(registry: UserRegistry, **kwargs) -> set[User]:
    users = registry.get_users_by_query(**kwargs)
    return users


def delete_user_by_id(uuid: UUID, registry: UserRegistry):
    registry.delete_member_by_id(uuid)

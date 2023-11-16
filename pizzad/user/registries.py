from typing import Optional
from uuid import UUID
from pizzad.models.implementations import Registry
from .abc import User, UserRegistry
from .user import UserType


class UserDictRegistry(UserRegistry, Registry):
    def get_users_by_query(self,
                           name_pattern: str = "",
                           uuids: Optional[set[UUID]] = None,
                           with_types: Optional[set[UserType]] = None,
                           without_types: Optional[set[UserType]] = None,
                           **kwargs) -> set[User]:
        users = self.get_all_members()

        if uuids:
            users = filter(
                    lambda user: (user.uuid in uuids), users)

        if name_pattern:
            users = filter(
                    lambda user:
                    (name_pattern in user.get_name()), users)

        if without_types:
            users = filter(
                    lambda user:
                    (user.get_type() not in without_types), users)

        if with_types:
            users = filter(
                    lambda user:
                    (user.get_type() in with_types), users)

        return set(users)

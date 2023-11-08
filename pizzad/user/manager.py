from typing import Dict, List
from pizzad.persistence import DictObject
from .user import User, UserFactory


class UserManager(DictObject):
    _instance = None
    users: Dict

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.orders = []
        return cls._instance

    def __init__(self):
        super().__init__()
        self.users = {}

    def create_user_if_not_exist(self, name: str) -> User:
        if name not in self.users:
            user = UserFactory.create_user(name)
            self.users[name] = user

    def to_dict(self):
        return {"users": {k: v.to_dict() for k, v in self.users.items()}}

    def update_from_dict(self, dictionary):
        self.users = {
                k: UserFactory.create_user().update_from_dict(v)
                for k, v in dictionary["users"]
        }

    def get_users(self, query: str = '') -> List[User]:
        return [
                user
                for name, user in self.users.items()
                if name.startswith(query) or name.endswith(query)
        ]

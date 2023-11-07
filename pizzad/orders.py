from typing import Set, List, Optional
from .persistence import DictObject


class Order(DictObject):
    name: str
    participants: List[str]
    tags: Set[str]

    def __init__(self, name: str, tags: Optional[Set[str]] = None):
        self.name = name
        self.tags = tags if tags else set()

    def register_participant(self, name: str, enforce_registeration: bool = False):
        if enforce_registeration or name not in self.participants:
            self.participants.append(name)

    def get_number_of_participants(self):
        return len(self.participants)

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.add(tag)

    def to_dict(self):
        return {
                'name': self.name,
                'participants': self.participants,
                'tags': self.tags
        }

    def update_from_dict(self, dictionary: dict):
        self.name = dictionary['name']
        self.participants = dictionary['participants']
        self.tags = dictionary['tags']

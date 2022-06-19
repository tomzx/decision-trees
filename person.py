from typing import Any, Dict

from item_collection import ItemCollection
from memory import Memory


class Person(object):
    def __init__(self, memories: Dict[str, Any]) -> None:
        self.location = None
        self.clothes = set()
        self.memory = Memory(memories)
        self.items = ItemCollection()
        self.state = {}

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

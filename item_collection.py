from item import Item


class ItemCollection:
    def __init__(self):
        self.items = {}

    def add(self, item: Item) -> None:
        self.items[item] = True
        print(self.items)

    def remove(self, item: Item) -> None:
        del self.items[item]
        print(self.items)

    def has(self, item: Item) -> bool:
        return self.items.get(item, False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.items})"

    def __repr__(self) -> str:
        return self.__str__()

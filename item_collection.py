class ItemCollection:
    def __init__(self):
        self.items = {}

    def add(self, item) -> None:
        self.items[item] = True

    def remove(self, item) -> None:
        del self.items[item]

    def has(self, item) -> bool:
        return self.items.get(item, False)

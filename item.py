from location import Location


class Item:
    def __init__(self, name: str, location: Location) -> None:
        self.name = name
        self.location = location

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.location == other.location

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __iter__(self):
        yield "name", self.name
        yield "location", self.location

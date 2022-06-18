from location import Location

class Item:
    def __init__(self, name: str, location: Location) -> None:
        self.name = name
        self.location = location

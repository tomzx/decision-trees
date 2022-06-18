class Location:
	def __init__(self, name: str) -> None:
		self.name = name

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.name})"

	def __eq__(self, other) -> bool:
		return self.name == other.name

	def __hash__(self) -> int:
		return hash(tuple(self))

	def __iter__(self):
		yield "name", self.name

Home = Location("home")
Work = Location("work")
BathRoom = Location("bathroom")
Bed = Location("bed")
BedRoom = Location("bedroom")
BedRoomCloset = Location("bedroom closet")
ComputerRoom = Location("computer room")
Kitchen = Location("kitchen")
LivingRoom = Location("living room")
Outside = Location("outside")
Person = Location("Person")

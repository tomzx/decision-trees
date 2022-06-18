from enum import Enum

class Location:
	def __init__(self, name: str) -> None:
		self.name = name

Home = Location("home")
Work = Location("Work")

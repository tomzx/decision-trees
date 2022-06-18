from item_collection import ItemCollection
from memory import Memory


class Person(object):
	def __init__(self):
		self.location = None
		self.clothes = set()
		self.memory = Memory()
		self.items = ItemCollection()

	def __str__(self):
		return self.__class__.__name__ + "(" + str(self.__dict__) + ")"

class Person(object):
	def __init__(self):
		self.location = None
		self.clothes = set()
		self.day = None
		self.time = None
		self.day_type = None
		self.memory = {} # facts stored in memory

	def recall(self, fact):
		value = self.memory.get(fact)
		print('Recalls {} is {}'.format(fact, value))
		return value

	def remember(self, fact, value=True):
		print('Will remember {} is {}'.format(fact, value))
		self.memory[fact] = value

	def __str__(self):
		return self.__class__.__name__ + "(" + str(self.__dict__) + ")"
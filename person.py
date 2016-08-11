class Person(object):
	def __init__(self):
		self.location = None
		self.clothes = set()
		self.day = None

	def __str__(self):
		return self.__class__.__name__ + "(" + str(self.__dict__) + ")"
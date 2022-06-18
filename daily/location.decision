from generic.choose import choose

from location import BedRoom, ComputerRoom, Kitchen, BathRoom, LivingRoom, Outside

def call(person):
	location = choose('Where am I?', [BedRoom, ComputerRoom, Kitchen, BathRoom, LivingRoom, Outside], BedRoom)
	person.location = location
	person.memory.location = location
	person.memory.locations[location] = True

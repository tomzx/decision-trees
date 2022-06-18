from generic.choose import choose

def call(person):
	# this question is constrained by the current location
	suggested = 'work' if person.memory.day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'] else 'weekend'
	person.memory.day_type = choose('What type of day is it?', ['work', 'home work', 'weekend', 'off', 'uncommon'], suggested)

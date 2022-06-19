import generic.go_to
from location import Home

def call(person):
	generic.go_to.call(person, 'groceries store')
	print('shop for room temperature food')
	print('shop for fridge temperature food')
	print('shop for freezer temperature food')
	print('queue for register')
	generic.go_to.call(person, 'groceries store register')
	generic.go_to.call(person, Home)

import eat.eat
from generic.askBoolean import askBoolean
import generic.go_to
import generic.pick
import generic.put

from item import Item
from location import Work, Location

def call(person):
	if person.memory.recall('will_eat') == 'lunch':
		generic.go_to.call(person, 'dinning room')
		generic.pick.call(person, Item('lunchbox', Location('fridge')))
		generic.put.call(person, Item('lunchbox', Location('dinning table')))
		print('unpack lunchbox')
		if askBoolean('Does the meal require to be heated up?'):
			print('heat up meal in microwave')
		eat.eat.call(person)
		print('throw away garbage')
		generic.pick.call(person, Item('lunchbox', Location('dinning table')))
		generic.go_to.call(person, 'work desk')
		generic.put.call(person, 'lunchbox', 'backpack')
	else:
		print('decide what/where to eat')
		print('get out of office')
		generic.go_to.call(person, 'restaurant')
		print('order')
		generic.pick.call(person, Item('order', Location('restaurant')))
		generic.go_to.call(person, Work)
		generic.go_to.call(person, 'dinning room')
		generic.put.call(person, Item('order', Location('dinning table')))
		eat.eat.call(person)
		print('throw away garbage')

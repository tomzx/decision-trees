from clothes import Clothes
import dress.dress
import dress.undress
import generic.go_to
import generic.put
import generic.pick
import hygiene.deodorant
import hygiene.shower_dry

from item import Item
from location import Person, Location

def call(person):
	hygiene.shower_dry.call(person)

	dress.dress.call(person, Clothes.Underwear, Location('shelf')) # todo: specify we are putting the new underwear
	generic.pick.call(person, Item('squeegee', Location('sink counter')))
	print('remove water from the bath using the squeegee')
	generic.put.call(person, Item('squeegee', Person), Location('sink counter'))

	hygiene.deodorant.call(person)

	# TODO: Things that are picked and put seem like candidates for more abstract "transfer/move" decision
	generic.pick.call(person, Item('old underwear', Person))
	generic.go_to.call(person, 'bedroom closet')
	generic.put.call(person, Item('old underwear', Person), Location('laundry basket'))

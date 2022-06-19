import location
from clothes import Clothes
import computer.login
import computer.sleep
import computer.wake_up
import computer.periodic_check
import daily.anki
import daily.day
import daily.day_type
import daily.github
import daily.hygiene
import daily.location
import daily.sleep
import daily.time
import daily.wake_up
import day.work
import day.home_work
import day.off
import dress.dress
import eat.breakfast
from generic.askBoolean import askBoolean
from generic.choose import choose
import generic.go_to
import generic.entertainment
import health.exercise
import hygiene.buccal
import weekly.buy_groceries
import weekly.laundry

from location import Home
from person import Person

def call(person: Person):
	daily.day.call(person)
	daily.time.call(person)
	daily.day_type.call(person)
	daily.location.call(person)
	daily.wake_up.call(person)

	if person.location == Home:
		generic.go_to.call(person, 'computer')
		computer.wake_up.call(person)
		computer.login.call(person)
		computer.periodic_check.call(person)
	if person.memory.day in ['wednesday', 'friday', 'sunday']:
		health.exercise.call(person)
	daily.hygiene.call(person)
	dress.dress.call(person, Clothes.Shirt, location.BedRoomCloset)
	eat.breakfast.call(person)  # (0715-0730)  the time is only true for work days

	if person.memory.day_type == 'work':
		day.work.call(person)
	elif person.memory.day_type == 'home work':
		day.home_work.call(person)
	elif person.memory.day_type == 'off':
		day.off.call(person)
	if askBoolean('Is there time for entertainment?', 'no'):
		generic.entertainment.call(person)
	if person.memory.day in ['wednesday', 'sunday']:
		weekly.laundry.call(person)
	if person.memory.day in ['sunday']:
		weekly.buy_groceries.call(person)
	if askBoolean('Is there time for entertainment?', 'no'):
		generic.entertainment.call(person)
	hygiene.buccal.call(person)
	computer.sleep.call(person)
	daily.sleep.call(person)

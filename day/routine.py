import computer.login
import computer.periodic_check
import computer.sleep
import computer.wake_up
import daily.anki
import daily.day
import daily.day_type
import daily.github
import daily.hygiene
import daily.location
import daily.sleep
import daily.time
import daily.wake_up
import day.home_work
import day.off
import day.work
import dress.dress
import eat.breakfast
import generic.entertainment
import generic.go_to
import health.exercise
import hygiene.buccal
import location
import weekly.buy_groceries
import weekly.laundry
from clothes import Clothes
from generic.askBoolean import askBoolean
from location import Home
from person import Person


def call(person: Person):
    daily.day.call(person)
    daily.time.call(person)
    daily.day_type.call(person)
    daily.location.call(person)
    daily.wake_up.call(person)

    if person.location == Home:
        generic.go_to.call(person, "computer")
        computer.wake_up.call(person)
        computer.login.call(person)
        computer.periodic_check.call(person)

    daily.hygiene.call(person)
    dress.dress.call(person, Clothes.Shirt, location.BedRoomCloset)
    eat.breakfast.call(person)  # (0715-0730)  the time is only true for work days

    if person.memory.day_type == "work":
        day.work.call(person)
    elif person.memory.day_type == "home work":
        day.home_work.call(person)
    elif person.memory.day_type == "off":
        day.off.call(person)
    if askBoolean("Is there time for entertainment?", "no"):
        generic.entertainment.call(person)
    health.exercise.call(person)
    if person.memory.day in ["sunday"]:
        weekly.laundry.call(person)
    if person.memory.day in ["sunday"]:
        weekly.buy_groceries.call(person)
    if askBoolean("Is there time for entertainment?", "no"):
        generic.entertainment.call(person)
    hygiene.buccal.call(person)
    computer.sleep.call(person)
    daily.sleep.call(person)

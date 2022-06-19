import dress.dress
import dress.undress
import generic.go_to
import generic.pick
import generic.put
import location
from body import Body
from clothes import Clothes
from item import Item
from location import BathRoom, BedRoomCloset, Location, Person


def dryTowel(bodyPart):
    print("towel %s" % bodyPart)


def call(person):
    generic.pick.call(person, Item("towel", Location("toilet seat")))
    dryTowel(Body.Hair)
    dryTowel(Body.Face)
    dryTowel(Body.Torso)
    dryTowel(Body.Back)
    dryTowel(Body.LeftArm)
    dryTowel(Body.RightArm)
    print("get out of shower")
    generic.go_to.call(person, BathRoom)
    dryTowel(Body.Genital)
    dryTowel(Body.LeftLeg)
    dryTowel(Body.RightLeg)
    print("shake towel")
    generic.put.call(person, Item("towel", Person), Location("shower curtain rod"))

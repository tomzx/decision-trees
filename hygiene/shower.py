import generic.go_to
import generic.pick
import generic.put
from body import Body
from item import Item
from location import Location, Person


def cleanWithHandTowel(bodyPart):
    print("clean %s" % bodyPart)


def call(person):
    print("start running shower water")
    print("test shower water temperature")
    print("close shower curtain")
    print("start shower")
    # TODO: Indicate that the shower is IN the bathroom (concept of containment)
    generic.go_to.call(person, "shower")
    print("put shower gel in right hand")
    cleanWithHandTowel(Body.Hair)
    cleanWithHandTowel(Body.Face)
    generic.pick.call(person, Item("hand towel", Location("shower handle")))
    print("put shower gel on hand towel")
    generic.go_to.call(person, "shower")
    cleanWithHandTowel(Body.Torso)
    cleanWithHandTowel(Body.LeftArm)
    cleanWithHandTowel(Body.RightArm)
    cleanWithHandTowel(Body.Genital)
    cleanWithHandTowel(Body.RightLeg)
    cleanWithHandTowel(Body.LeftLeg)
    cleanWithHandTowel(Body.Back)
    print("clean hand towel")
    generic.put.call(person, Item("hand towel", Person), Location("shower handle"))
    print("stop shower")
    print("stop running water")
    print("open shower curtain")

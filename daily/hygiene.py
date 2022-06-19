import hygiene.deodorant
import hygiene.nail_clipping
import hygiene.post_shower
import hygiene.pre_shower
import hygiene.shave
import hygiene.shower
from generic.askBoolean import askBoolean


def call(person):
    hygiene.pre_shower.call(person)
    hygiene.shower.call(person)
    hygiene.post_shower.call(person)

    if askBoolean("Should I shave?", "no"):
        hygiene.shave.call(person)

    if person.memory.day == "sunday":
        if askBoolean("Should I clip my nails?", "yes"):
            hygiene.nail_clipping.call(person)

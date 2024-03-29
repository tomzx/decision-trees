from __future__ import print_function

import argparse
import builtins
import inspect

import day.routine
import location
from clothes import Clothes
from item import Item
from memory import Memory
from person import Person

_print = print


def print(*args, **kwargs):
    trace_person()
    trace()
    _print(f"\033[1m{args[0]}\033[0m", *args[1:], **kwargs)


builtins.print = print

_input = input


def input(arg):
    trace_person()
    trace(3)
    return _input(f"\033[1m{arg}\033[0m")


builtins.input = input

parser = argparse.ArgumentParser()
parser.add_argument(
    "--trace", help="Trace the source of an action", action="store_true"
)
parser.add_argument(
    "--trace-person",
    help="Trace the state of the person at each action",
    action="store_true",
)
parser.add_argument("--debug-decision", help="Debug/Run a target decision then exit")
args = parser.parse_args()

if args.trace:

    def trace(drop_frames=2):
        current_frame = inspect.currentframe()
        frames = inspect.getouterframes(current_frame, 9999)
        # Ignore drop_frames from the end as we do not want to display this function and its caller (print/input) in the stack and do not print the main.py entry point
        for (i, frame) in enumerate(reversed(frames[drop_frames:-1])):
            _print("%s> %s:%s" % (" " * i, frame.filename, frame.lineno))

else:

    def trace(drop_frames=0):
        return


person = Person(
    {
        "locations": Memory(
            {
                location.BathRoom: True,
                location.Bed: True,
                location.BedRoom: True,
                location.BedRoomCloset: True,
                location.ComputerRoom: True,
                location.Kitchen: True,
                location.LivingRoom: True,
            }
        )
    }
)

if args.trace_person:

    def trace_person():
        _print(person)

else:

    def trace_person():
        return


# Start in the bed
person.location = location.Bed
# Start with underwear
person.clothes.add(Clothes.Underwear)
person.items.add(Item(Clothes.Underwear, location.Person))
# Set some memories

if args.debug_decision:
    debugged_decision = importlib.import_module(args.debug_decision)
    debugged_decision.call(person)
else:
    day.routine.call(person)

from unittest import mock

import day.routine
from tests.fixtures.person import person


def test_call_as_workday(person):
    with mock.patch("generic.choose.input") as mock_input:
        mock_input.side_effect = [
            # "What day is it?"
            "monday",
            # "What type of day is it?"
            "work",
            # "Where am I?"
            "bedroom",
            # Should I shave?
            "no",
            # Do I make myself a lunch or eat outside?
            "lunch",
            # Is there time for entertainment?
            "no",
            # Is there time for entertainment?
            "no",
        ]
        day.routine.call(person)


def test_call_as_weekend(person):
    with mock.patch("generic.choose.input") as mock_input:
        mock_input.side_effect = [
            # "What day is it?"
            "saturday",
            # "What type of day is it?"
            "weekend",
            # "Where am I?"
            "bedroom",
            # Should I shave?
            "no",
            # Is there time for entertainment?
            "no",
            # Is there time for entertainment?
            "no",
        ]
        day.routine.call(person)


def test_call_as_day_off(person):
    with mock.patch("generic.choose.input") as mock_input:
        mock_input.side_effect = [
            # "What day is it?"
            "monday",
            # "What type of day is it?"
            "off",
            # "Where am I?"
            "bedroom",
            # Should I shave?
            "no",
            # Is there time for entertainment?
            "no",
            # Is there time for entertainment?
            "no",
        ]
        day.routine.call(person)

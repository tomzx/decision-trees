import pytest

import location
from memory import Memory
from person import Person


@pytest.fixture
def person():
    person = Person({"locations": Memory({})})
    person.location = location.Bed
    return person

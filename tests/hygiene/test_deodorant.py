import hygiene.deodorant
from tests.fixtures.person import person


def test_call(person):
    hygiene.deodorant.call(person)

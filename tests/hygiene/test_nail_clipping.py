import hygiene.nail_clipping
from tests.fixtures.person import person


def test_call(person):
    hygiene.nail_clipping.call(person)

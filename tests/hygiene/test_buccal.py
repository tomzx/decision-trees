import hygiene.buccal
from tests.fixtures.person import person


def test_call(person):
    hygiene.buccal.call(person)

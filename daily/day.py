from generic.choose import choose
from datetime import date
import calendar

def call(person):
	today = date.today()
	today = calendar.day_name[today.weekday()].lower()
	day = choose('What day is it?', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'], today)
	person.memory.day = day

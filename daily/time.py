from datetime import datetime

from generic.choose import choose


def call(person):
    now = datetime.now()
    print(f'It is {now.strftime("%H:%M:%S")}')

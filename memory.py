Day = "day"
DayType = "day type"
Time = "time"

class Memory:
    def __init__(self):
        self.__dict__["memory"] = {}

    def recall(self, fact: str) -> str:
        value = self.memory.get(fact)
        print(f'Recalls {fact} is {value}')
        return value

    def remember(self, fact: str, value: bool = True) -> None:
        print(f'Will remember {fact} is {value}')
        self.memory[fact] = value

    def __getattr__(self, fact: str) -> str:
        return self.recall(fact)

    def __setattr__(self, fact: str, value: str) -> None:
        self.remember(fact, value)

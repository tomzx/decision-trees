class Memory:
    def __init__(self):
        self.memory = {}

    def recall(self, fact: str) -> str:
        value = self.memory.get(fact)
        print(f'Recalls {fact} is {value}')
        return value

    def remember(self, fact: str, value: bool = True) -> None:
        print(f'Will remember {fact} is {value}')
        self.memory[fact] = value

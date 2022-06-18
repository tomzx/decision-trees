from typing import Any

class Memory:
    def __init__(self):
        self.__dict__["memory"] = {}
        self.__dict__["memory"]["locations"] = {}

    def recall(self, fact: str) -> Any:
        return self.memory.get(fact)

    def remember(self, fact: str, value: Any = True) -> None:
        self.memory[fact] = value

    def __getattr__(self, fact: str) -> Any:
        value = self.__dict__["memory"].get(fact)
        print(f'Recalls {fact} is {value}')
        return self.recall(fact)

    def __setattr__(self, fact: str, value: str) -> None:
        # self.remember(fact, value)
        print(f'Will remember {fact} is {value}')
        self.__dict__["memory"][fact] = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.memory})"

    def __repr__(self) -> str:
        return self.__str__()

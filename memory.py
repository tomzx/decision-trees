from typing import Any, Dict

class Memory:
    def __init__(self, memories: Dict[str, Any]):
        self.__dict__["memory"] = memories

    def recall(self, fact: str) -> Any:
        return self.memory.get(fact)

    def remember(self, fact: str, value: Any = True) -> None:
        self.memory[fact] = value

    def __getattr__(self, fact: str) -> Any:
        value = self.__dict__["memory"].get(fact)
        print(f'Recalls {fact} is {value}')
        return value

    def __setattr__(self, fact: str, value: str) -> None:
        # self.remember(fact, value)
        print(f'Will remember {fact} is {value}')
        self.__dict__["memory"][fact] = value

    def __getitem__(self, fact: str) -> Any:
        return self.__getattr__(fact)

    def __setitem__(self, fact: str, value: str) -> None:
        return self.__setattr__(fact, value)

    def __contains__(self, fact: str) -> bool:
        return self.recall(fact)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.memory})"

    def __repr__(self) -> str:
        return self.__str__()

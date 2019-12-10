from typing import List


class Stack(object):
    def __init__(self) -> None:
        super().__init__()
        self._stack: List[int] = []

    def push(self, value: int) -> None:
        self.validate_value(value)
        self._stack.append(value)

    def pop(self) -> int:
        return self._stack.pop()

    def __len__(self) -> int:
        return len(self._stack)

    def __repr__(self) -> str:
        return repr(self._stack)

    def validate_value(self, value: int) -> None:
        # TODO: Validate value
        pass

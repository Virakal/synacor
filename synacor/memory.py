from typing import List, MutableMapping, Optional

from synacor.stack import Stack


class Memory(object):
    MAX_MEMORY_OFFSET = 32775
    REGISTER_COUNT = 8
    REGISTER_OFFSET = MAX_MEMORY_OFFSET - REGISTER_COUNT

    def __init__(self) -> None:
        super().__init__()
        self._memory: MutableMapping[int, int] = {}
        self._pointer = 0

        self.stack = Stack()

    def __getitem__(self, key: int) -> int:
        self.validate_key(key)

        try:
            return self._memory[key]
        except:
            # Empty memory segments are just empty
            return 0

    def __setitem__(self, key: int, value: int) -> None:
        self.validate_key(key)
        self.validate_value(value)
        self._memory[key] = value

    def __len__(self) -> int:
        return len(self._memory)

    def __repr__(self) -> str:
        return self._memory.__repr__()

    def get_at_pointer(self) -> int:
        return self._memory[self.pointer]

    def increment_pointer(self) -> None:
        self.pointer += 1

    def decrement_pointer(self) -> None:
        self.pointer -= 1

    @property
    def pointer(self) -> int:
        return self._pointer

    @pointer.setter
    def pointer(self, new_value: int) -> None:
        self.validate_pointer(new_value)
        self._pointer = new_value

    def get_register(self, index: int) -> int:
        self.validate_register_index(index)
        return self[self.REGISTER_OFFSET + index]

    def set_register(self, index: int, value: int) -> None:
        self.validate_register_index(index)
        # Note that the value is validated in our setter
        self[self.REGISTER_OFFSET + index] = value

    def get_register_values(self) -> List[int]:
        return [self.get_register(i) for i in range(0, self.REGISTER_COUNT)]

    def pop_argument(self, dereference_registers=True) -> int:
        """Utility method to get the current memory value then increment

        Keyword Arguments:
            dereference_registers {bool} -- whether to fetch the values stored in register arguments (default: {True})

        Returns:
            int -- the current memory value
        """
        value = self.get_at_pointer()
        self.increment_pointer()

        if dereference_registers:
            value = self.dereference_value(value)

        return value

    def is_register(self, key: int) -> bool:
        """Whether the given memory address is the address of a register

        Arguments:
            key {int} -- the memory address to check

        Returns:
            bool -- whether the address is a register
        """
        return key > self.REGISTER_OFFSET and key <= self.MAX_MEMORY_OFFSET

    def dereference_value(self, value: int) -> int:
        """Fetch the register value if the value is a register

        Arguments:
            value {int} -- the value to check

        Returns:
            int -- the value or the value from the specified register
        """
        if self.is_register(value):
            return self[value]

        return value

    def validate_key(self, key: int) -> None:
        if not type(key) == int:
            raise KeyError("Memory index must be an int")

        if key < 0:
            raise KeyError("Memory index must not be negative")

        if key > self.MAX_MEMORY_OFFSET:
            raise KeyError(
                f"Memory index must be between 0 and {self.MAX_MEMORY_OFFSET}"
            )

    def validate_value(self, value: int) -> None:
        if not type(value) == int:
            raise ValueError("Memory value must be an int")

    def validate_pointer(self, pointer: Optional[int] = None) -> None:
        if pointer is None:
            pointer = self.pointer

        if not type(pointer) == int:
            raise ValueError("Pointer is not an int!")

        if pointer < 0:
            raise ValueError("Pointer must not be negative")

        if pointer > self.MAX_MEMORY_OFFSET:
            raise ValueError(f"Pointer must be between 0 and {self.MAX_MEMORY_OFFSET}")

    def validate_register_index(self, index: int) -> None:
        if not type(index) == int:
            raise KeyError("Register index must be an int")

        if index < 0:
            raise KeyError("Register index must not be negative")

        if index > self.REGISTER_COUNT:
            raise KeyError(
                f"Register index must be between 0 and {self.REGISTER_COUNT}"
            )

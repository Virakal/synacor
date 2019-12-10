from typing import List

from synacor.stack import Stack

class Memory(object):
    MAX_MEMORY_OFFSET = 32775
    REGISTER_COUNT = 8
    REGISTER_OFFSET = MAX_MEMORY_OFFSET - REGISTER_COUNT

    def __init__(self):
        super().__init__()
        self._memory = {}
        self._pointer = 0

        self.stack = Stack()

    def __getitem__(self, key: int) -> int:
        self.validate_key(key)

        try:
            return self._memory[key]
        except:
            # Empty memory segments are just empty
            return 0

    def __setitem__(self, key: int, value: int):
        self.validate_key(key)
        self.validate_value(value)
        self._memory.__setitem__(key, value)

    def __len__(self) -> int:
        return len(self._memory)

    def __repr__(self, *args) -> str:
        return self._memory.__repr__(*args)

    def get_at_pointer(self) -> int:
        return self._memory[self.pointer]

    def increment_pointer(self):
        self.pointer += 1

    def decrement_pointer(self):
        self.pointer -= 1

    @property
    def pointer(self) -> int:
        return self._pointer

    @pointer.setter
    def pointer(self, new_value: int):
        self.validate_pointer(new_value)
        self._pointer = new_value

    def get_register(self, index: int) -> int:
        self.validate_register_index(index)
        return self[self.REGISTER_OFFSET + index]

    def set_register(self, index: int, value: int):
        self.validate_register_index(index)
        # Note that the value is validated in our setter
        self[self.REGISTER_OFFSET + index] = value

    def get_register_values(self) -> List[int]:
        return [self.get_register(i) for i in range(0, self.REGISTER_COUNT)]

    """Utility method to get the current memory value then increment

    Returns:
        int -- the current memory value
    """
    def pop_argument(self, dereference_registers=True) -> int:
        value = self.get_at_pointer()
        self.increment_pointer()

        if dereference_registers and self.is_register(value):
            value = self[value]

        return value

    def is_register(self, key) -> bool:
        return key > self.REGISTER_OFFSET and key <= self.MAX_MEMORY_OFFSET

    def validate_key(self, key):
        if not type(key) == int:
            raise KeyError("Memory index must be an int")

        if key < 0:
            raise KeyError("Memory index must not be negative")

        if key > self.MAX_MEMORY_OFFSET:
            raise KeyError(
                f"Memory index must be between 0 and {self.MAX_MEMORY_OFFSET}"
            )

    def validate_value(self, value):
        if not type(value) == int:
            raise ValueError("Memory value must be an int")

    def validate_pointer(self, pointer=None):
        if pointer is None:
            pointer = self.pointer

        if not type(pointer) == int:
            raise ValueError("Pointer is not an int!")

        if pointer < 0:
            raise ValueError("Pointer must not be negative")

        if pointer > self.MAX_MEMORY_OFFSET:
            raise ValueError(f"Pointer must be between 0 and {self.MAX_MEMORY_OFFSET}")

    def validate_register_index(self, index):
        if not type(index) == int:
            raise KeyError("Register index must be an int")

        if index < 0:
            raise KeyError("Register index must not be negative")

        if index > self.REGISTER_COUNT:
            raise KeyError(
                f"Register index must be between 0 and {self.REGISTER_COUNT}"
            )

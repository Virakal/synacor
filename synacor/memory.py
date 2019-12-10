class Memory(object):
    _memory = {}

    MAX_MEMORY_OFFSET = 2**16 - 1

    def __getitem__(self, key: int):
        self.validate_key(key)

        try:
            return self._memory[key]
        except:
            return 0

    def __setitem__(self, key: int, value: int):
        self.validate_key(key)
        self.validate_value(value)
        self._memory.__setitem__(key, value)

    def __len__(self):
        return len(self._memory)

    def __repr__(self, *args):
        return self._memory.__repr__(*args)

    def validate_key(self, key):
        if not type(key) == int:
            raise KeyError("Memory index must be an int")

        if key < 0:
            raise KeyError("Memory index must not be negative")

        if key > self.MAX_MEMORY_OFFSET:
            raise KeyError(f"Memory index must be between 0 and {self.MAX_MEMORY_OFFSET}")

    def validate_value(self, value):
        if not type(value) == int:
            raise ValueError("Memory value must be an int")

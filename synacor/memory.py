class Memory(object):
    memory = {}

    MAX_MEMORY_OFFSET = 32775

    def __getitem__(self, key: int) -> int:
        self.validate_key(key)

        try:
            return self.memory[key]
        except:
            # Empty memory segments are just nulled out
            return 0

    def __setitem__(self, key: int, value: int):
        self.validate_key(key)
        self.validate_value(value)
        self.memory.__setitem__(key, value)

    def __len__(self) -> int:
        return len(self.memory)

    def __repr__(self, *args) -> str:
        return self.memory.__repr__(*args)

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

from synacor.binparser import BinParser
from synacor.memory import Memory
from synacor.opcodes import Opcodes


class VM:
    def __init__(self) -> None:
        self.memory = Memory()

    def run(self, binfile_path) -> None:
        parser = BinParser(self.memory)
        parser.file_into_memory(binfile_path)
        self.parse_from_pointer()

    def parse_from_pointer(self) -> None:
        opcodes = Opcodes(self.memory)

        while True:
            # This loop should be terminated by a halt instruction
            should_stop = opcodes.run(self.memory.pop_argument(False))

            if should_stop:
                break

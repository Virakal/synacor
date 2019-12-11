from synacor.binparser import BinParser
from synacor.memory import Memory
from synacor.opcode import Opcodes


class VM(object):
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
            opcodes.run(self.memory.pop_argument(False))

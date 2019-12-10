from synacor.binparser import BinParser
from synacor.memory import Memory
from synacor.opcode import Opcode


class VM(object):
    def __init__(self) -> None:
        self.memory = Memory()

    def run(self, binfile_path) -> None:
        parser = BinParser(self.memory)
        parser.file_into_memory(binfile_path)
        self.parse_from_pointer()

    def parse_from_pointer(self) -> None:
        while True:
            # This loop should be terminated by a halt instruction
            command = self.get_next_command()
            self.execute_command(command)

    def get_next_command(self) -> Opcode:
        code_int = self.memory.get_at_pointer()
        return Opcode.from_int(code_int)

    def execute_command(self, command: Opcode) -> None:
        mem = self.memory
        mem.increment_pointer()
        command.run(mem)

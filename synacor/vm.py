from time import time

from synacor.binparser import BinParser
from synacor.memory import Memory
from synacor.opcodes import Opcodes
from synacor.iologger import IOLogger


class VM:
    def __init__(self) -> None:
        self.memory = Memory()
        self.io_logger = IOLogger()

    def run(self, binfile_path) -> None:
        parser = BinParser(self.memory)
        parser.file_into_memory(binfile_path)

        try:
            self.parse_from_pointer()
        except:
            self.dump_input_log()
            raise

        self.dump_input_log()

    def parse_from_pointer(self) -> None:
        opcodes = Opcodes(self.memory, self.io_logger)

        while True:
            # This loop should be terminated by a halt instruction
            should_stop = opcodes.run(self.memory.pop_argument(False))

            if should_stop:
                break

    def dump_input_log(self) -> None:
        # TODO: Perhaps this should be done from outside the VM class
        filename = 'inputlog-' + str(int(time())) + '.txt'
        lines = "\n".join(self.io_logger.dump_input())

        if lines:
            with open(filename, 'w') as f:
                f.write(lines)

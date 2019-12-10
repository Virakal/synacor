from pathlib import Path
from textwrap import wrap
from typing import List

from synacor.memory import Memory
from synacor.tokeniser import Tokeniser


class BinParser(object):
    HIGH_BYTE_OFFSET = 2**8

    def __init__(self, memory: Memory):
        self.tokeniser = Tokeniser()
        self.memory = memory

    def file_into_memory(self, path, memory_offset=0):
        # The Path object has a read_bytes method which makes out lives easier
        path = Path(path)

        # Words are 16-bit, little endian, so we need to read two bytes and
        # join them together before committing them to memory
        first = True
        previous = 0
        pointer = memory_offset

        for byte in path.read_bytes():
            if first:
                previous = byte
            else:
                self.memory[pointer] = previous + byte * self.HIGH_BYTE_OFFSET
                pointer += 1

            first = not first

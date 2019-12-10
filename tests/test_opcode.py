import unittest

from synacor.memory import Memory
from synacor.opcode import Opcode


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_add(self):
        self.memory[0] = 9
        self.memory[1] = 32768
        self.memory[2] = 40
        self.memory[3] = 99
        self.memory.increment_pointer()

        add = Opcode.from_int(9)
        add.run(self.memory)

        self.assertEquals(self.memory[32768], 40 + 99)

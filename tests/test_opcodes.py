import unittest

from synacor.memory import Memory
from synacor.opcodes import Opcodes


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()
        self.op = Opcodes(self.memory)

    def test_add(self):
        self.op.op_add(32768, 40, 99)
        self.assertEquals(self.memory[32768], 40 + 99)

        # Modulo Test
        self.op.op_add(32769, 32758, 15)
        self.assertEquals(self.memory[32769], 5)

    def test_mod(self):
        self.op.op_mult(32768, 40, 99)
        self.assertEquals(self.memory[32768], 40 * 99)

        # Modulo Test
        self.op.op_mult(32769, 32758, 10)
        self.assertEquals(self.memory[32769], 32668)

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

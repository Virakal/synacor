import unittest

from synacor.memory import Memory


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_is_register(self):
        register_addresses = range(32768, 32776)

        for addr in register_addresses:
            self.assertTrue(self.memory.is_register(addr))

        self.assertFalse(self.memory.is_register(32768 - 1))
        self.assertFalse(self.memory.is_register(32775 + 1))
        self.assertFalse(self.memory.is_register(32775 + 2))
        self.assertFalse(self.memory.is_register(0))

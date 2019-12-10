import sys
from typing import Mapping

from synacor.memory import Memory

MATHS_MODULO = 32768


class Opcode(object):
    """An invalid opcode"""

    _opcodes: Mapping[int, "Opcode"] = {}

    @property
    def name(self) -> str:
        name = self.__class__.__name__
        return name.replace("Opcode", "").lower()

    @staticmethod
    def from_int(opcode_int: int):
        return Opcode._opcodes[opcode_int]

    def run(self, memory: Memory) -> None:
        raise NotImplementedError("Invalid opcode")


class HaltOpcode(Opcode):
    """Stop execution and terminate the program"""

    def run(self, memory: Memory) -> None:
        print("Halting execution", file=sys.stderr)
        exit()


class SetOpcode(Opcode):
    """Set register <a> to the value of <b>"""

    def run(self, memory: Memory) -> None:
        register_index = memory.pop_argument(False)
        value = memory.pop_argument()
        memory[register_index] = value


class PushOpcode(Opcode):
    """Push <a> onto the stack"""

    def run(self, memory: Memory) -> None:
        value = memory.pop_argument()
        memory.stack.push(value)


class PopOpcode(Opcode):
    """Remove the top element from the stack and write it into <a>; empty stack = error"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        memory[destination] = memory.stack.pop()


class EqOpcode(Opcode):
    """Set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = int(op1 == op2)


class GtOpcode(Opcode):
    """Set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = int(op1 > op2)


class JmpOpcode(Opcode):
    """Jump to <a>"""

    def run(self, memory: Memory) -> None:
        new_address = memory.get_at_pointer()
        memory.pointer = new_address


class JtOpcode(Opcode):
    """If <a> is nonzero, jump to <b>"""

    def run(self, memory: Memory) -> None:
        test = memory.pop_argument()
        new_address = memory.pop_argument()

        if test > 0:
            memory.pointer = new_address


class JfOpcode(Opcode):
    """If <a> is zero, jump to <b>"""

    def run(self, memory: Memory) -> None:
        test = memory.pop_argument()
        new_address = memory.pop_argument()

        if test == 0:
            memory.pointer = new_address


class AddOpcode(Opcode):
    """Assign into <a> the sum of <b> and <c> (modulo 32768)"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = (op1 + op2) % MATHS_MODULO


class MultOpcode(Opcode):
    """Store into <a> the product of <b> and <c> (modulo 32768)"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = (op1 * op2) % MATHS_MODULO


class ModOpcode(Opcode):
    """Store into <a> the remainder of <b> divided by <c>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = op1 % op2


class AndOpcode(Opcode):
    """Stores into <a> the bitwise and of <b> and <c>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = op1 & op2


class OrOpcode(Opcode):
    """Stores into <a> the bitwise or of <b> and <c>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = op1 | op2


class NotOpcode(Opcode):
    """Stores 15-bit bitwise inverse of <b> in <a>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        value = memory.pop_argument()

        # Ugly but very simple 'not'
        bitwise_notted = (
            format(value, "015b").replace("1", "2").replace("0", "1").replace("2", "0")
        )

        new_value = int(bitwise_notted, 2)
        memory[destination] = new_value


class RmemOpcode(Opcode):
    """Read memory at address <b> and write it to <a>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        source = memory.pop_argument()

        value = memory[source]
        memory[destination] = value


class WmemOpcode(Opcode):
    """Write the value from <b> into memory at address <a>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        source = memory.pop_argument()

        value = source
        memory[memory[destination]] = value


class CallOpcode(Opcode):
    """Write the address of the next instruction to the stack and jump to <a>"""

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument()
        next_instruction = memory.pointer

        memory.stack.push(next_instruction)
        memory.pointer = destination


class RetOpcode(Opcode):
    """Remove the top element from the stack and jump to it; empty stack = halt"""

    def run(self, memory: Memory) -> None:
        if len(memory.stack) == 0:
            raise RecursionError("Tried to call ret with an empty stack")

        destination = memory.stack.pop()
        memory.pointer = destination


class OutOpcode(Opcode):
    """Write the character represented by ascii code <a> to the terminal"""

    def run(self, memory: Memory) -> None:
        charcode = memory.pop_argument()
        print(chr(charcode), end="")


class InOpcode(Opcode):
    """Read a character from the terminal and write its ascii code to <a>; it can be assumed that once input
     starts, it will continue until a newline is encountered; this means that you can safely read whole lines
     from the keyboard and trust that they will be fully read"""

    def run(self, memory: Memory) -> None:
        # NYI
        raise NotImplementedError("'In' opcode not yet implemented")


class NoopOpcode(Opcode):
    """No operation"""

    def run(self, memory: Memory) -> None:
        # Don't do anything
        pass


# Initialise the opcode cache
Opcode._opcodes = {
    0: HaltOpcode(),
    1: SetOpcode(),
    2: PushOpcode(),
    3: PopOpcode(),
    4: EqOpcode(),
    5: GtOpcode(),
    6: JmpOpcode(),
    7: JtOpcode(),
    8: JfOpcode(),
    9: AddOpcode(),
    10: MultOpcode(),
    11: ModOpcode(),
    12: AndOpcode(),
    13: OrOpcode(),
    14: NotOpcode(),
    15: RmemOpcode(),
    16: WmemOpcode(),
    17: CallOpcode(),
    18: RetOpcode(),
    19: OutOpcode(),
    20: InOpcode(),
    21: NoopOpcode(),
}

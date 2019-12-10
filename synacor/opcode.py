import sys

from typing import Mapping
from synacor.memory import Memory

MATHS_MODULO = 32768


class Opcode(object):
    _opcodes: Mapping[int, "Opcode"] = {}
    desc = "an invalid opcode"

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
    desc = "stop execution and terminate the program"

    def run(self, memory: Memory) -> None:
        print("Halting execution", file=sys.stderr)
        exit()


class SetOpcode(Opcode):
    desc = "set register <a> to the value of <b>"

    def run(self, memory: Memory) -> None:
        register_index = memory.pop_argument(False)
        register_index -= memory.REGISTER_OFFSET
        value = memory.pop_argument()

        memory.set_register(register_index, value)


class PushOpcode(Opcode):
    desc = "push <a> onto the stack"

    def run(self, memory: Memory) -> None:
        value = memory.pop_argument()
        memory.stack.push(value)


class PopOpcode(Opcode):
    desc = "remove the top element from the stack and write it into <a>; empty stack = error"

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        memory[destination] = memory.stack.pop()


class EqOpcode(Opcode):
    desc = "set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise"

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = int(op1 == op2)


class GtOpcode(Opcode):
    desc = "set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise"

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = int(op1 > op2)


class JmpOpcode(Opcode):
    desc = "jump to <a>"

    def run(self, memory: Memory) -> None:
        new_address = memory.get_at_pointer()
        memory.pointer = new_address


class JtOpcode(Opcode):
    desc = "if <a> is nonzero, jump to <b>"

    def run(self, memory: Memory) -> None:
        test = memory.pop_argument()
        new_address = memory.pop_argument()

        if test > 0:
            memory.pointer = new_address


class JfOpcode(Opcode):
    desc = "if <a> is zero, jump to <b>"

    def run(self, memory: Memory) -> None:
        test = memory.pop_argument()
        new_address = memory.pop_argument()

        if test == 0:
            memory.pointer = new_address


class AddOpcode(Opcode):
    desc = "assign into <a> the sum of <b> and <c> (modulo 32768)"

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = (op1 + op2) % MATHS_MODULO

class AndOpcode(Opcode):
    desc = "stores into <a> the bitwise and of <b> and <c>"

    def run(self, memory: Memory) -> None:
        destination = memory.pop_argument(False)
        op1 = memory.pop_argument()
        op2 = memory.pop_argument()

        memory[destination] = op1 & op2


class OutOpcode(Opcode):
    desc = "write the character represented by ascii code <a> to the terminal"

    def run(self, memory: Memory) -> None:
        charcode = memory.pop_argument()
        print(chr(charcode), end="")


class NoopOpcode(Opcode):
    desc = "no operation"

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
    12: AndOpcode(),
    19: OutOpcode(),
    21: NoopOpcode(),
}

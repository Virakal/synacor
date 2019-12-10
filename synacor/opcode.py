import sys

from synacor.memory import Memory


class Opcode(object):
    _opcodes = {}
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
        # NYI
        raise NotImplementedError("Invalid opcode")


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


class PushOpcode(Opcode):
    desc = "push <a> onto the stack"

    def run(self, memory: Memory) -> None:
        # NYI
        raise NotImplementedError("Invalid opcode")


class PopOpcode(Opcode):
    desc = "remove the top element from the stack and write it into <a>; empty stack = error"

    def run(self, memory: Memory) -> None:
        # NYI
        raise NotImplementedError("Invalid opcode")


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
    6: JmpOpcode(),
    7: JtOpcode(),
    8: JfOpcode(),
    19: OutOpcode(),
    21: NoopOpcode(),
}

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
        memory.increment_pointer()
        memory.increment_pointer()


class PushOpcode(Opcode):
    desc = "push <a> onto the stack"

    def run(self, memory: Memory) -> None:
        # NYI
        pass


class PopOpcode(Opcode):
    desc = "remove the top element from the stack and write it into <a>; empty stack = error"

    def run(self, memory: Memory) -> None:
        # NYI
        memory.increment_pointer()


class OutOpcode(Opcode):
    desc = "write the character represented by ascii code <a> to the terminal"

    def run(self, memory: Memory) -> None:
        charcode = memory.get_at_pointer()
        print(chr(charcode), end="")
        memory.increment_pointer()


class NoopOpcode(Opcode):
    desc = "no operation"

    def run(self, memory: Memory) -> None:
        # Don't do anything
        pass


# Initialise the opcode cache
Opcode._opcodes[0] = HaltOpcode()
Opcode._opcodes[1] = SetOpcode()
Opcode._opcodes[2] = PushOpcode()
Opcode._opcodes[3] = PopOpcode()
Opcode._opcodes[19] = OutOpcode()
Opcode._opcodes[21] = NoopOpcode()

import inspect
import functools
import sys
from typing import Callable, Dict, List

from synacor.memory import Memory

MATHS_MODULO = 32768


def absolute(*args: str) -> Callable:
    """Decorator to list any parameters that shouldn't be dereferenced if they
    are register addresses.
    """

    def absolute_func(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        # Record dereferenced parameters on the function
        decorated.absolute_params = args

        return decorated

    return absolute_func


class Opcodes:
    # Map opcode numbers to their names
    OPCODE_NAMES = {
        0: "halt",
        1: "set",
        2: "push",
        3: "pop",
        4: "eq",
        5: "gt",
        6: "jmp",
        7: "jt",
        8: "jf",
        9: "add",
        10: "mult",
        11: "mod",
        12: "and",
        13: "or",
        14: "not",
        15: "rmem",
        16: "wmem",
        17: "call",
        18: "ret",
        19: "out",
        20: "in",
        21: "noop",
    }

    def __init__(self, memory: Memory) -> None:
        super().__init__()
        self.memory = memory
        self._method_params = self._calculate_method_params()
        self._char_generator = self.get_char_generator()

    def run(self, opcode: int) -> None:
        try:
            op_name = self.OPCODE_NAMES[opcode]
        except KeyError as e:
            # Worth handling this?
            raise

        method_name = "op_" + op_name
        method = getattr(self, method_name)
        params = self._method_params[method_name]
        kwargs: Dict[str, int] = {}

        for param_name, dereference in params.items():
            kwargs[param_name] = self.memory.pop_argument(dereference)

        # Call the method with the arguments
        method(**kwargs)

    def op_halt(self) -> None:
        """Stop execution and terminate the program"""
        print("Halting execution", file=sys.stderr)
        exit()

    @absolute("register_index")
    def op_set(self, register_index: int, value: int) -> None:
        """Set register <a> to the value of <b>"""
        self.memory[register_index] = value

    def op_push(self, value: int) -> None:
        """Push <a> onto the stack"""
        self.memory.stack.push(value)

    @absolute("destination")
    def op_pop(self, destination: int) -> None:
        """Remove the top element from the stack and write it into <a>; empty stack = error"""
        if len(self.memory.stack) == 0:
            raise RecursionError("Tried to call pop with an empty stack")

        self.memory[destination] = self.memory.stack.pop()

    @absolute("destination")
    def op_eq(self, destination: int, op1: int, op2: int) -> None:
        """Set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise"""
        self.memory[destination] = int(op1 == op2)

    @absolute("destination")
    def op_gt(self, destination: int, op1: int, op2: int) -> None:
        """Set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise"""
        self.memory[destination] = int(op1 > op2)

    def op_jmp(self, new_address: int) -> None:
        """Jump to <a>"""
        self.memory.pointer = new_address

    def op_jt(self, test: int, new_address: int) -> None:
        """If <a> is nonzero, jump to <b>"""
        if test != 0:
            self.memory.pointer = new_address

    def op_jf(self, test: int, new_address: int) -> None:
        """If <a> is zero, jump to <b>"""
        if test == 0:
            self.memory.pointer = new_address

    @absolute("destination")
    def op_add(self, destination: int, op1: int, op2: int) -> None:
        """Store into <a> the sum of <b> and <c> (modulo 32768)"""
        self.memory[destination] = (op1 + op2) % MATHS_MODULO

    @absolute("destination")
    def op_mult(self, destination: int, op1: int, op2: int) -> None:
        """Store into <a> the product of <b> and <c> (modulo 32768)"""
        self.memory[destination] = (op1 * op2) % MATHS_MODULO

    @absolute("destination")
    def op_mod(self, destination: int, op1: int, op2: int) -> None:
        """Store into <a> the remainder of <b> divided by <c>"""
        self.memory[destination] = op1 % op2

    @absolute("destination")
    def op_and(self, destination: int, op1: int, op2: int) -> None:
        """Stores into <a> the bitwise and of <b> and <c>"""
        self.memory[destination] = op1 & op2

    @absolute("destination")
    def op_or(self, destination: int, op1: int, op2: int) -> None:
        """Stores into <a> the bitwise or of <b> and <c>"""
        self.memory[destination] = op1 | op2

    @absolute("destination")
    def op_not(self, destination: int, value: int) -> None:
        """Stores 15-bit bitwise inverse of <b> in <a>"""
        new_value = MATHS_MODULO - 1 - value
        self.memory[destination] = new_value

    @absolute("destination")
    def op_rmem(self, destination: int, source: int) -> None:
        """Read memory at address <b> and write it to <a>"""
        value = self.memory[source]
        self.memory[destination] = value

    def op_wmem(self, destination: int, source: int) -> None:
        """Write the value from <b> into memory at address <a>"""
        self.memory[destination] = source

    def op_call(self, destination: int) -> None:
        """Write the address of the next instruction to the stack and jump to <a>"""
        next_instruction = self.memory.pointer
        self.memory.stack.push(next_instruction)
        self.op_jmp(destination)

    def op_ret(self) -> None:
        """Remove the top element from the stack and jump to it; empty stack = halt"""
        if len(self.memory.stack) == 0:
            raise RecursionError("Tried to call ret with an empty stack")

        destination = self.memory.stack.pop()
        self.op_jmp(destination)

    def op_out(self, charcode: int) -> None:
        """Write the character represented by ascii code <a> to the terminal"""
        print(chr(charcode), end="")

    @absolute("destination")
    def op_in(self, destination: int):
        """Read a character from the terminal and write its ascii code to <a>; it can be assumed that once input
         starts, it will continue until a newline is encountered; this means that you can safely read whole lines
         from the keyboard and trust that they will be fully read"""
        self.memory[destination] = next(self._char_generator)

    def op_noop(self) -> None:
        """No operation"""
        pass

    def get_char_generator(self):
        """Creates a generator that yields individual characters for every "in"
         opcode call
        """
        while True:
            # Fetch input
            line = input('>>> ')

            # Yield the next character
            for char in line:
                yield ord(char)

            # Yield a newline to finish the input
            yield ord("\n")

    def _calculate_method_params(self) -> Dict[str, Dict[str, bool]]:
        """Return information about the op_* methods"""
        params: Dict[str, Dict[str, bool]] = {}

        for op_name in self.OPCODE_NAMES.values():
            method_name = "op_" + op_name
            method = getattr(self, method_name)
            signature = inspect.signature(method)
            params[method_name] = {}

            for param_name in signature.parameters:
                # Check if method has a dereference annotation
                try:
                    dereference = param_name not in method.absolute_params
                except (AttributeError):
                    dereference = True

                params[method_name][param_name] = dereference

        return params

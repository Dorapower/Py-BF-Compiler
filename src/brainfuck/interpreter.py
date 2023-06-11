"""Interpret the source code directly"""
import sys
from typing import TypeAlias

import numpy as np

from preprocessor import preprocess


class Interpreter:
    """
    Interpret the source code directly

    It takes source code input and execute it when `execute` is called.
    The io of the program is stdin and stdout.
    """
    debug: bool

    _size: int
    _mem: np.ndarray
    _ptr: int  # Current position in the memory
    _stack: list[int]  # Stack for loop positions

    def __init__(self, size: int = 2 ** 10, *, debug: bool = False):
        self.debug = debug

        self._size = size
        self._mem = np.zeros(self._size, dtype=np.uint8)
        self._ptr = 0
        self._stack = []

    def reset(self) -> None:
        """
        Reset the internal state
        :return: None
        """
        self._mem.fill(0)
        self._ptr = 0
        self._stack.clear()

    @staticmethod
    def bracket_match(src: str) -> dict[int, int]:
        """
        Check if the source code is valid
        :param src: source code
        :return: a dict which maps bracket to its pair
        """
        return {}

    def execute(self, src: str) -> None:
        """
        Execute the source code
        :param src: source code
        :return: None
        """
        src = preprocess(src)
        target = self.bracket_match(src)
        idx, length = 0, len(src)

        while idx < length:
            cmd = src[idx]
            match cmd:
                case '>':
                    self._ptr += 1
                case '<':
                    self._ptr -= 1
                case '+':
                    self._mem[self._ptr] += 1
                case '-':
                    self._mem[self._ptr] -= 1
                case '.':
                    sys.stdout.write(chr(self._mem[self._ptr]))
                case ',':
                    self._mem[self._ptr] = ord(sys.stdin.read(1))
                case '[':
                    if not self._mem[self._ptr]:
                        idx = target[idx] - 1
                case ']':
                    if self._mem[self._ptr]:
                        idx = target[idx] - 1
                case _:
                    raise RuntimeError(f'Unknown command {cmd}')
            idx += 1

    def __repr__(self) -> str:
        return f'Interpreter(size={self._size}, debug={self.debug})'

    def __str__(self) -> str:
        return repr(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()

    def __del__(self):
        self.reset()


def interpret(src: str) -> None:
    with Interpreter() as interpreter:
        interpreter.execute(src)


def main():
    src = input('Press enter to start')
    interpret(src)


if __name__ == '__main__':
    main()

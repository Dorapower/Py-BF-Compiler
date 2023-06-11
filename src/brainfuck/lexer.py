"""process a src string and remove comments"""

commands = '><+-.,[]'


class Lexer:
    src: str
    _l: int
    _p: int  # Current position in the source code

    def __init__(self, src: str):
        self.src = src
        self._l = len(self.src)
        self._p = 0

    def __next__(self):
        while self._p < self._l and self.src[self._p] not in commands:
            self._p += 1

        if self._p >= self._l:
            raise StopIteration

        char = self.src[self._p]
        self._p += 1
        return char

    def __iter__(self):
        return self

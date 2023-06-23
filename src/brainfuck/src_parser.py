"""Parse the source code into an AST"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias
from pprint import pprint

from src_lexer import Lexer

Command: TypeAlias = Literal['>', '<', '+', '-', '.', ',', '[', ']']


@dataclass(frozen=True)
class ASTNode:
    """Abstract Syntax Tree Node"""
    command: Command | None  # None for Root
    children: list[ASTNode] | None = None


class Parser:
    """Analyse a string of source code and generate an AST"""
    src: str
    debug: bool

    def __init__(self, src: str, debug: bool = False):
        self.src = src
        self.debug = debug

        self._lexer = Lexer(src)

    def parse(self) -> ASTNode:
        """Parse the source code into an AST"""
        return self.parse_program()

    def parse_program(self) -> ASTNode:
        """parse until program end"""
        root = ASTNode(None, [])
        stack = [root]
        current_node = root

        for command in self._lexer:
            match command:
                case '>' | '<' | '+' | '-' | '.' | ',':
                    current_node.children.append(ASTNode(command))
                case '[':
                    new_node = ASTNode(command, [])
                    current_node.children.append(new_node)
                    stack.append(new_node)
                    current_node = new_node
                case ']':
                    try:
                        current_node = stack.pop()
                    except IndexError as e:
                        raise RuntimeError('Unmatched ]') from e
                case _:
                    raise RuntimeError(f'Unknown command {command}')

        if len(stack) != 1 or stack[0] is not root:
            raise RuntimeError('Unmatched [')

        return root


def parse_bf(src: str) -> ASTNode:
    """Parse the source code into an AST"""
    return Parser(src).parse()


def main(filename: str | None = None):
    if filename is None:
        src = input('Enter brainfuck source code below:\n')
    else:
        with open(filename, 'r', encoding='utf8') as f:
            src = f.read()
    ast = parse_bf(src)
    pprint(ast)


if __name__ == '__main__':
    main('../../examples/add.bf')

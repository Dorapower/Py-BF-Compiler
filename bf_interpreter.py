#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:41:00 2023
Author:     Lokdora
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pprint import pprint


@dataclass(frozen=True)
class ASTNode:
    """
    Abstract Syntax Tree Node

    The only structure in brainfuck codes is the matching parentheses, other parts are linear
    """
    command: str
    children: list[ASTNode] | None = None


class Parser:
    src: str
    debug: bool

    _l: int  # Length of src
    _p: int  # Current position in the source code

    def __init__(self, src: str, debug: bool = False):
        self.src = src
        self.debug = debug

        self._l = len(self.src)
        self._p = 0

    def parse(self) -> ASTNode:
        """
        Parse the source code into an AST
        :return: ASTNode
        """
        return self.parse_program()

    def parse_program(self) -> ASTNode:
        """
        parse until program end
        :return: ASTNode
        """
        content: list[ASTNode] = []
        while node := self.parse_group():
            content.append(node)

        program = ASTNode('Program', content)
        return program

    def parse_group(self) -> ASTNode | None:
        """
        parse next command group, if end of src or end of loop is reached, return None instead

        command group is one command or a loop
        :return:
        """
        # skip comments
        while self._p < self._l and self.src[self._p] not in '[]+-<>.,':
            self._p += 1

        if self._p >= self._l or self.src[self._p] == ']':
            return None

        if self.src[self._p] == '[':
            return self.parse_loop()
        else:
            return self.parse_command()

    def parse_loop(self) -> ASTNode:
        """
        parse next loop
        :return: ASTNode
        """
        assert self.src[self._p] == '['
        self._p += 1

        content: list[ASTNode] = []
        while node := self.parse_group():
            content.append(node)

        assert self.src[self._p] == ']'
        self._p += 1

        loop = ASTNode('[', content)
        return loop

    def parse_command(self) -> ASTNode:
        """
        parse next command
        :return: ASTNode
        """
        assert self._p < self._l
        command = self.src[self._p]
        self._p += 1

        return ASTNode(command)


class ASTInterpreter:
    ast: ASTNode
    debug: bool

    _p: int  # Pointer
    _m: list[int]  # Memory

    def __init__(self, ast: ASTNode, mem_size=100, debug: bool = False):
        self.ast = ast
        self.debug = debug

        self._p = 0
        self._m = [0] * mem_size

    def run(self):
        """
        Run the program
        :return:
        """
        for node in self.ast.children:
            self._run(node)

    def _run(self, node: ASTNode):
        """
        Run the node
        :param node:
        :return:
        """
        if self.debug:
            print(f'Running {node.command}')
            mem_dict = {i: v for i, v in enumerate(self._m) if v}
            pprint(mem_dict)
        if node.command == '+':
            self._m[self._p] += 1
        elif node.command == '-':
            self._m[self._p] -= 1
        elif node.command == '>':
            self._p += 1
        elif node.command == '<':
            self._p -= 1
        elif node.command == '.':
            print(chr(self._m[self._p]), end='')
        elif node.command == ',':
            self._m[self._p] = ord(sys.stdin.read(1))
        elif node.command == '[':
            while self._m[self._p]:
                for child in node.children:
                    self._run(child)
        elif node.command == ']':
            pass
        else:
            raise ValueError(f'Unknown command {node.command}')


def main():
    src = "<[->+<]>."
    parser = Parser(src)
    ast = parser.parse()
    interpreter = ASTInterpreter(ast)
    interpreter.run()


if __name__ == '__main__':
    main()

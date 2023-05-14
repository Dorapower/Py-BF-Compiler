#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:41:00 2023
Author:     Lokdora
"""

from __future__ import annotations

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

        loop = ASTNode('Loop', content)
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


def test_parser():
    with open('examples/add.bf', 'r', encoding='utf-8') as f:
        src = f.read()
    parser = Parser(src, debug=True)
    ast = parser.parse()
    pprint(ast)


if __name__ == '__main__':
    test_parser()

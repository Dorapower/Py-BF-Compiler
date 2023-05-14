#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:31:00 2023
Author:     Lokdora
"""

from pprint import pprint

from bf_interpreter import Parser, ASTInterpreter


def test_parser(filename='examples/add.bf'):
    with open(filename, 'r', encoding='utf-8') as f:
        src = f.read()
    parser = Parser(src, debug=True)
    ast = parser.parse()
    pprint(ast)


def test_ast_interpreter(filename='examples/add.bf'):
    with open(filename, 'r', encoding='utf-8') as f:
        src = f.read()
    parser = Parser(src, debug=True)
    ast = parser.parse()
    interpreter = ASTInterpreter(ast, debug=True)
    interpreter.run()


def main():
    filename = input("Enter the filename of brainfuck src code: ")
    print('*** Test Parser ***')
    test_parser(filename)
    print('*** Test Interpreter ***')
    test_ast_interpreter(filename)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:31:00 2023
Author:     Lokdora
"""

from pprint import pprint

from bf_compiler import Parser


def test_parser(filename='examples/add.bf'):
    with open(filename, 'r', encoding='utf-8') as f:
        src = f.read()
    parser = Parser(src, debug=True)
    ast = parser.parse()
    pprint(ast)


if __name__ == '__main__':
    print('*** Test Parser ***')
    filename = input("Enter the filename of brainfuck src code: ")
    test_parser(filename)

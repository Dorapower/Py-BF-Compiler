"""utility functions"""

import re

from bf_parser import ASTNode


def strip_comments(src: str) -> str:
    """strip all the comment characters and leave commands"""
    return re.sub(r"[^<>+\-,.\[\]]", '', src)


def validate_program(src: str) -> bool:
    """determine whether the program is valid"""
    depth = 0
    for ch in src:
        match ch:
            case '[':
                depth += 1
            case ']':
                depth -= 1
        if depth < 0:
            return False
    return depth == 0


def match_bracket(src: str) -> dict[int, int]:
    """
    create a mapping between bracket for source code.
    Validation are required beforehand.

    :param src: source code to run matching
    :return: a dict that maps index of a bracket to the corresponding one.
    Both of the left and right bracket will be in the keys
    """
    left_stack = []
    mapping = {}
    for idx, char in enumerate(src):
        match char:
            case '[':
                left_stack.append(idx)
            case ']':
                left_idx = left_stack.pop()
                mapping[left_idx] = idx
                mapping[idx] = left_idx
    return mapping


def validate_function(src: str) -> bool:
    """check if there's no input command inside a loop"""
    depth = 0
    for ch in src:
        match ch:
            case '[':
                depth += 1
            case ']':
                depth -= 1
            case ',':
                if depth > 0:
                    return False
    return True

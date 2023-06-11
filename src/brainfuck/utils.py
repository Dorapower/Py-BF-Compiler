"""utility functions"""

import re


def strip_comments(src: str) -> str:
    """strip all the comment characters and leave commands"""
    return re.sub(r"[^<>+-,.\[\]]", '', src)


def validate(src: str) -> bool:
    """determine whether the program is valid"""
    return src.count('[') == src.count(']')


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

"""Parse the source code into an AST"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ASTNode:
    """Abstract Syntax Tree Node"""
    command: str
    children: list[ASTNode] | None = None

class Parser:
    """
    Parse the source code into an AST

    """
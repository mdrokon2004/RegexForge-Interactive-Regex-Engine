"""
RegexForge Data Models & Enums
Defines core data structures used across the lexer, parser, automata, and matcher components.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Any


class TokenType(Enum):
    SYMBOL = auto()
    UNION = auto()          # |
    CONCAT = auto()         # Explicit concatenation operator
    KLEENE_STAR = auto()    # *
    PLUS = auto()           # +
    OPTIONAL = auto()       # ?
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    WILDCARD = auto()       # .
    EOF = auto()            # End of File/Expression


@dataclass
class Token:
    type: TokenType
    value: str
    position: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"

    def to_dict(self) -> dict:
        return {
            "type": self.type.name,
            "value": self.value,
            "position": self.position
        }


@dataclass
class MatchStep:
    step: int
    character: str
    current_state: str
    next_state: str
    is_accepting: bool = False

    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "character": self.character,
            "current_state": self.current_state,
            "next_state": self.next_state,
            "is_accepting": self.is_accepting
        }

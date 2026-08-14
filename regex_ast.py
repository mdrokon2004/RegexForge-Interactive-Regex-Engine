"""
RegexForge Abstract Syntax Tree (AST) Nodes
Defines AST node types for regex operators (Literal, Union, Concat, Star, Plus, Optional, Wildcard).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ASTNode(ABC):
    """Base class for all AST nodes."""
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class SymbolNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "SYMBOL",
            "value": self.value,
            "label": f"'{self.value}'",
            "children": []
        }

    def __repr__(self) -> str:
        return f"SymbolNode('{self.value}')"


class WildcardNode(ASTNode):
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "WILDCARD",
            "value": ".",
            "label": ".",
            "children": []
        }

    def __repr__(self) -> str:
        return "WildcardNode('.')"


class ConcatNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "CONCAT",
            "label": "CONCAT (•)",
            "children": [self.left.to_dict(), self.right.to_dict()]
        }

    def __repr__(self) -> str:
        return f"ConcatNode({self.left}, {self.right})"


class UnionNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "UNION",
            "label": "UNION (|)",
            "children": [self.left.to_dict(), self.right.to_dict()]
        }

    def __repr__(self) -> str:
        return f"UnionNode({self.left}, {self.right})"


class StarNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "KLEENE_STAR",
            "label": "STAR (*)",
            "children": [self.child.to_dict()]
        }

    def __repr__(self) -> str:
        return f"StarNode({self.child})"


class PlusNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "PLUS",
            "label": "PLUS (+)",
            "children": [self.child.to_dict()]
        }

    def __repr__(self) -> str:
        return f"PlusNode({self.child})"


class OptionalNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "OPTIONAL",
            "label": "OPTIONAL (?)",
            "children": [self.child.to_dict()]
        }

    def __repr__(self) -> str:
        return f"OptionalNode({self.child})"

"""
RegexForge Syntax Parser
Course: CSE314 — Compiler Design Lab
Project 24: Regular Expression Engine (Team: Uronto Helicopter)

Parses a stream of Token objects into an Abstract Syntax Tree (AST) using Recursive Descent.
Respects strict operator precedence:
  1. Grouping ()
  2. Postfix Repetition (*, +, ?)
  3. Explicit Concatenation (•)
  4. Union / Alternation (|)
"""

from typing import List, Optional
from models import Token, TokenType
from regex_ast import (
    ASTNode, SymbolNode, WildcardNode, ConcatNode,
    UnionNode, StarNode, PlusNode, OptionalNode
)
from errors import ParseError


class Parser:
    """
    Deterministic Recursive Descent Parser for Regular Expressions.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    def peek(self) -> Token:
        """Returns the current token without advancing position."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        # Fallback EOF
        last_pos = self.tokens[-1].position if self.tokens else 0
        return Token(TokenType.EOF, "", last_pos)

    def advance(self) -> Token:
        """Returns current token and advances position."""
        tok = self.peek()
        if self.pos < len(self.tokens):
            self.pos += 1
        return tok

    def consume(self, expected_type: TokenType, error_msg: Optional[str] = None) -> Token:
        """
        Consumes token of expected_type or raises ParseError.
        """
        tok = self.peek()
        if tok.type == expected_type:
            return self.advance()

        found_str = tok.value if tok.value else tok.type.name
        pos = tok.position
        msg = error_msg or f"Expected '{expected_type.name}' but found '{found_str}'."
        raise ParseError(
            message=msg,
            position=pos,
            expected=expected_type.name,
            found=found_str
        )

    def parse(self) -> ASTNode:
        """
        Main entry point for parsing token stream into an AST.
        """
        if not self.tokens or self.peek().type == TokenType.EOF:
            return SymbolNode("ε")

        ast = self.parse_union()

        # Check for unconsumed trailing tokens (e.g. unmatched closing parenthesis)
        current = self.peek()
        if current.type != TokenType.EOF:
            if current.type == TokenType.RPAREN:
                raise ParseError(
                    message=f"Unmatched closing parenthesis ')' at position {current.position}.",
                    position=current.position,
                    found=")"
                )
            raise ParseError(
                message=f"Unexpected token '{current.value}' at position {current.position}.",
                position=current.position,
                found=current.value
            )

        return ast

    def parse_union(self) -> ASTNode:
        """
        Parses Union / Alternation (|) expressions (Lowest Precedence).
        Grammar: concat_expr ('|' concat_expr)*
        """
        left = self.parse_concat()

        while self.peek().type == TokenType.UNION:
            union_tok = self.advance()
            next_tok = self.peek()

            # Check for trailing union or missing right operand
            if next_tok.type in {TokenType.UNION, TokenType.RPAREN, TokenType.EOF}:
                found_val = next_tok.value if next_tok.value else next_tok.type.name
                raise ParseError(
                    message="Missing right operand for union operator '|'.",
                    position=union_tok.position,
                    expected="expression",
                    found=found_val
                )

            right = self.parse_concat()
            left = UnionNode(left, right)

        return left

    def parse_concat(self) -> ASTNode:
        """
        Parses Concatenation (•) expressions.
        Grammar: unary_expr (CONCAT unary_expr)*
        """
        left = self.parse_unary()

        while self.peek().type == TokenType.CONCAT:
            self.advance()  # Consume CONCAT token
            right = self.parse_unary()
            left = ConcatNode(left, right)

        return left

    def parse_unary(self) -> ASTNode:
        """
        Parses Postfix Unary Operators (*, +, ?).
        Grammar: primary_expr ('*' | '+' | '?')*
        """
        node = self.parse_primary()

        while self.peek().type in {TokenType.KLEENE_STAR, TokenType.PLUS, TokenType.OPTIONAL}:
            op_tok = self.advance()
            if op_tok.type == TokenType.KLEENE_STAR:
                node = StarNode(node)
            elif op_tok.type == TokenType.PLUS:
                node = PlusNode(node)
            elif op_tok.type == TokenType.OPTIONAL:
                node = OptionalNode(node)

        return node

    def parse_primary(self) -> ASTNode:
        """
        Parses Primary Atoms: Literals, Wildcard, or Parenthesized Expressions.
        """
        tok = self.peek()

        if tok.type == TokenType.SYMBOL:
            self.advance()
            return SymbolNode(tok.value)

        elif tok.type == TokenType.WILDCARD:
            self.advance()
            return WildcardNode()

        elif tok.type == TokenType.LPAREN:
            lparen_tok = self.advance()

            # Check for empty group ()
            if self.peek().type == TokenType.RPAREN:
                raise ParseError(
                    message="Empty group parenthesis '()'.",
                    position=lparen_tok.position,
                    expected="expression",
                    found=")"
                )

            expr = self.parse_union()

            if self.peek().type != TokenType.RPAREN:
                found_str = self.peek().value if self.peek().value else self.peek().type.name
                raise ParseError(
                    message="Unclosed parenthesis '('.",
                    position=lparen_tok.position,
                    expected=")",
                    found=found_str
                )

            self.advance()  # Consume matching RPAREN
            return expr

        elif tok.type == TokenType.UNION:
            raise ParseError(
                message="Missing left operand before union operator '|'.",
                position=tok.position,
                found="|"
            )

        elif tok.type in {TokenType.KLEENE_STAR, TokenType.PLUS, TokenType.OPTIONAL}:
            raise ParseError(
                message=f"Missing operand before '{tok.value}' operator.",
                position=tok.position,
                found=tok.value
            )

        elif tok.type == TokenType.RPAREN:
            raise ParseError(
                message=f"Unexpected closing parenthesis ')' at position {tok.position}.",
                position=tok.position,
                found=")"
            )

        elif tok.type == TokenType.EOF:
            raise ParseError(
                message="Unexpected end of expression.",
                position=tok.position,
                found="EOF"
            )

        else:
            raise ParseError(
                message=f"Unexpected token '{tok.value}' at position {tok.position}.",
                position=tok.position,
                found=tok.value
            )

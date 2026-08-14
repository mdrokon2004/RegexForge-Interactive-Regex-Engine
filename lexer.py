"""
RegexForge Production-Quality Custom Lexical Analyzer (Lexer)
Course: CSE314 — Compiler Design Lab
Project 24: Regular Expression Engine (Team: Uronto Helicopter)

Tokenizes regular expression strings without using Python's built-in `re` module.
Automatically infers and inserts explicit CONCAT tokens.
"""

from typing import List, Set
from models import Token, TokenType
from errors import LexicalError


class Lexer:
    """
    Custom Lexical Analyzer for Regular Expressions.
    Performs scanning and implicit concatenation insertion.
    """

    RESERVED_OPERATORS = {'|', '*', '+', '?', '(', ')', '.'}

    def __init__(self, expression: str):
        self.expression: str = expression
        self.length: int = len(expression)

    def is_valid_symbol_char(self, ch: str) -> bool:
        """
        Determines if a character is a valid literal symbol.
        Allows alphanumeric characters (a-z, A-Z, 0-9) and safe non-reserved literals.
        """
        if ch in self.RESERVED_OPERATORS or ch.isspace():
            return False
        # Allow ASCII alphanumeric and select non-operator literals (e.g. '_', '-')
        return ch.isalnum() or ch in {'_', '-'}

    def scan_raw_tokens(self) -> List[Token]:
        """
        Pass 1: Scans the input string character-by-character to generate raw Token stream.
        Skips whitespace and detects lexical errors for invalid characters.
        """
        raw_tokens: List[Token] = []
        i = 0

        while i < self.length:
            ch = self.expression[i]

            # Skip whitespace characters
            if ch.isspace():
                i += 1
                continue

            if ch == '|':
                raw_tokens.append(Token(TokenType.UNION, '|', i))
            elif ch == '*':
                raw_tokens.append(Token(TokenType.KLEENE_STAR, '*', i))
            elif ch == '+':
                raw_tokens.append(Token(TokenType.PLUS, '+', i))
            elif ch == '?':
                raw_tokens.append(Token(TokenType.OPTIONAL, '?', i))
            elif ch == '(':
                raw_tokens.append(Token(TokenType.LPAREN, '(', i))
            elif ch == ')':
                raw_tokens.append(Token(TokenType.RPAREN, ')', i))
            elif ch == '.':
                raw_tokens.append(Token(TokenType.WILDCARD, '.', i))
            elif self.is_valid_symbol_char(ch):
                raw_tokens.append(Token(TokenType.SYMBOL, ch, i))
            else:
                raise LexicalError(
                    message=f"Unexpected character '{ch}' at position {i}.",
                    position=i,
                    found_char=ch
                )

            i += 1

        # Append End-Of-File / End-Of-Expression Token
        raw_tokens.append(Token(TokenType.EOF, "", self.length))
        return raw_tokens

    def insert_implicit_concat(self, raw_tokens: List[Token]) -> List[Token]:
        """
        Pass 2: Inserts explicit CONCAT tokens where concatenation is implied.
        
        Concatenation is implied between T1 and T2 when:
          - T1 is in {SYMBOL, WILDCARD, KLEENE_STAR, PLUS, OPTIONAL, RPAREN}
          - T2 is in {SYMBOL, WILDCARD, LPAREN}
        """
        if not raw_tokens:
            return [Token(TokenType.EOF, "", self.length)]

        final_tokens: List[Token] = []
        can_follow_concat: Set[TokenType] = {
            TokenType.SYMBOL,
            TokenType.WILDCARD,
            TokenType.KLEENE_STAR,
            TokenType.PLUS,
            TokenType.OPTIONAL,
            TokenType.RPAREN
        }
        can_precede_concat: Set[TokenType] = {
            TokenType.SYMBOL,
            TokenType.WILDCARD,
            TokenType.LPAREN
        }

        for idx in range(len(raw_tokens) - 1):
            t1 = raw_tokens[idx]
            t2 = raw_tokens[idx + 1]

            final_tokens.append(t1)

            # Check if explicit CONCAT should be inserted between t1 and t2
            if t1.type in can_follow_concat and t2.type in can_precede_concat:
                concat_pos = t2.position
                final_tokens.append(Token(TokenType.CONCAT, "•", concat_pos))

        # Append the final token (EOF or last token)
        final_tokens.append(raw_tokens[-1])
        return final_tokens

    def tokenize(self) -> List[Token]:
        """
        Executes complete lexical analysis pipeline.
        Returns processed Token list including explicit CONCAT and EOF tokens.
        """
        raw_tokens = self.scan_raw_tokens()
        return self.insert_implicit_concat(raw_tokens)

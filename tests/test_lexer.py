"""
RegexForge Lexer Comprehensive Unit Tests
Tests all 16 specified lexical rules, operator types, implicit concatenation, and error handling.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from models import TokenType
from errors import LexicalError


class TestRegexLexer(unittest.TestCase):

    def test_1_single_literal(self):
        tokens = Lexer("a").tokenize()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.SYMBOL)
        self.assertEqual(tokens[0].value, "a")
        self.assertEqual(tokens[0].position, 0)
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_2_multiple_literals(self):
        tokens = Lexer("abc").tokenize()
        # Expect: a CONCAT b CONCAT c EOF
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.CONCAT, TokenType.SYMBOL, TokenType.CONCAT, TokenType.SYMBOL, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_3_union(self):
        tokens = Lexer("a|b").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.UNION, TokenType.SYMBOL, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_4_kleene_star(self):
        tokens = Lexer("a*").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.KLEENE_STAR, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_5_plus(self):
        tokens = Lexer("a+").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.PLUS, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_6_optional(self):
        tokens = Lexer("a?").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.OPTIONAL, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_7_grouping(self):
        tokens = Lexer("(a|b)").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.LPAREN, TokenType.SYMBOL, TokenType.UNION, TokenType.SYMBOL, TokenType.RPAREN, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_8_wildcard(self):
        tokens = Lexer(".").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.WILDCARD, TokenType.EOF]
        self.assertEqual(types, expected)

    def test_9_implicit_concatenation(self):
        tokens = Lexer("ab").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.CONCAT, TokenType.SYMBOL, TokenType.EOF]
        self.assertEqual(types, expected)
        self.assertEqual(tokens[1].value, "•")

    def test_10_concatenation_with_grouping(self):
        tokens = Lexer("a(b|c)").tokenize()
        types = [t.type for t in tokens]
        expected = [
            TokenType.SYMBOL, TokenType.CONCAT, TokenType.LPAREN,
            TokenType.SYMBOL, TokenType.UNION, TokenType.SYMBOL,
            TokenType.RPAREN, TokenType.EOF
        ]
        self.assertEqual(types, expected)

    def test_11_concatenation_after_grouping(self):
        tokens = Lexer("(a|b)c").tokenize()
        types = [t.type for t in tokens]
        expected = [
            TokenType.LPAREN, TokenType.SYMBOL, TokenType.UNION, TokenType.SYMBOL,
            TokenType.RPAREN, TokenType.CONCAT, TokenType.SYMBOL, TokenType.EOF
        ]
        self.assertEqual(types, expected)

    def test_12_complex_expression(self):
        tokens = Lexer("(a|b)*abb").tokenize()
        types = [t.type for t in tokens]
        expected = [
            TokenType.LPAREN, TokenType.SYMBOL, TokenType.UNION, TokenType.SYMBOL, TokenType.RPAREN,
            TokenType.KLEENE_STAR, TokenType.CONCAT,
            TokenType.SYMBOL, TokenType.CONCAT,
            TokenType.SYMBOL, TokenType.CONCAT,
            TokenType.SYMBOL, TokenType.EOF
        ]
        self.assertEqual(types, expected)

    def test_13_invalid_character(self):
        with self.assertRaises(LexicalError) as ctx:
            Lexer("a$b").tokenize()
        self.assertEqual(ctx.exception.position, 1)
        self.assertEqual(ctx.exception.found_char, "$")
        self.assertIn("Unexpected character '$'", ctx.exception.message)

    def test_14_empty_input(self):
        tokens = Lexer("").tokenize()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_15_whitespace_handling(self):
        tokens = Lexer("a   b").tokenize()
        types = [t.type for t in tokens]
        expected = [TokenType.SYMBOL, TokenType.CONCAT, TokenType.SYMBOL, TokenType.EOF]
        self.assertEqual(types, expected)
        self.assertEqual(tokens[0].position, 0)
        self.assertEqual(tokens[2].position, 4)

    def test_16_correct_eof_token(self):
        tokens = Lexer("a").tokenize()
        eof_token = tokens[-1]
        self.assertEqual(eof_token.type, TokenType.EOF)
        self.assertEqual(eof_token.position, 1)


if __name__ == '__main__':
    unittest.main()

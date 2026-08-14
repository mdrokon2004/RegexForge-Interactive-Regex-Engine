"""
RegexForge Parser & AST Comprehensive Unit Tests
Tests operator precedence, AST construction, grouping, and syntax error detection.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser import Parser
from regex_ast import (
    SymbolNode, WildcardNode, ConcatNode,
    UnionNode, StarNode, PlusNode, OptionalNode
)
from errors import ParseError


class TestRegexParser(unittest.TestCase):

    def parse_regex(self, expr: str):
        tokens = Lexer(expr).tokenize()
        return Parser(tokens).parse()

    def test_1_single_symbol(self):
        ast = self.parse_regex("a")
        self.assertIsInstance(ast, SymbolNode)
        self.assertEqual(ast.value, "a")

    def test_2_concatenation(self):
        ast = self.parse_regex("ab")
        self.assertIsInstance(ast, ConcatNode)
        self.assertIsInstance(ast.left, SymbolNode)
        self.assertIsInstance(ast.right, SymbolNode)
        self.assertEqual(ast.left.value, "a")
        self.assertEqual(ast.right.value, "b")

    def test_3_union(self):
        ast = self.parse_regex("a|b")
        self.assertIsInstance(ast, UnionNode)
        self.assertIsInstance(ast.left, SymbolNode)
        self.assertIsInstance(ast.right, SymbolNode)

    def test_4_kleene_star(self):
        ast = self.parse_regex("a*")
        self.assertIsInstance(ast, StarNode)
        self.assertIsInstance(ast.child, SymbolNode)

    def test_5_plus(self):
        ast = self.parse_regex("a+")
        self.assertIsInstance(ast, PlusNode)
        self.assertIsInstance(ast.child, SymbolNode)

    def test_6_optional(self):
        ast = self.parse_regex("a?")
        self.assertIsInstance(ast, OptionalNode)
        self.assertIsInstance(ast.child, SymbolNode)

    def test_7_wildcard(self):
        ast = self.parse_regex(".")
        self.assertIsInstance(ast, WildcardNode)

    def test_8_operator_precedence(self):
        # a|b*c => Union(a, Concat(Star(b), c))
        ast = self.parse_regex("a|b*c")
        self.assertIsInstance(ast, UnionNode)
        self.assertIsInstance(ast.left, SymbolNode)
        self.assertIsInstance(ast.right, ConcatNode)
        self.assertIsInstance(ast.right.left, StarNode)

    def test_9_grouping_precedence(self):
        # (a|b)*c => Concat(Star(Union(a, b)), c)
        ast = self.parse_regex("(a|b)*c")
        self.assertIsInstance(ast, ConcatNode)
        self.assertIsInstance(ast.left, StarNode)
        self.assertIsInstance(ast.left.child, UnionNode)

    def test_10_unclosed_parenthesis_error(self):
        with self.assertRaises(ParseError) as ctx:
            self.parse_regex("(a|b")
        self.assertEqual(ctx.exception.expected, ")")
        self.assertIn("Unclosed parenthesis", ctx.exception.message)

    def test_11_double_union_error(self):
        with self.assertRaises(ParseError) as ctx:
            self.parse_regex("a||b")
        self.assertIn("Missing right operand", ctx.exception.message)

    def test_12_leading_union_error(self):
        with self.assertRaises(ParseError) as ctx:
            self.parse_regex("|ab")
        self.assertIn("Missing left operand", ctx.exception.message)

    def test_13_empty_group_error(self):
        with self.assertRaises(ParseError) as ctx:
            self.parse_regex("()")
        self.assertIn("Empty group", ctx.exception.message)

    def test_14_missing_star_operand_error(self):
        with self.assertRaises(ParseError) as ctx:
            self.parse_regex("*a")
        self.assertIn("Missing operand", ctx.exception.message)

    def test_15_unmatched_closing_parenthesis(self):
        with self.assertRaises(ParseError) as ctx:
            self.parse_regex("a|b)")
        self.assertIn("Unmatched closing parenthesis", ctx.exception.message)

    def test_16_complex_expression_ast(self):
        ast = self.parse_regex("(a|b)*abb")
        ast_dict = ast.to_dict()
        self.assertEqual(ast_dict["type"], "CONCAT")
        # Verify StarNode exists in the tree
        self.assertIn("KLEENE_STAR", str(ast_dict))


if __name__ == '__main__':
    unittest.main()

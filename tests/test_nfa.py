"""
RegexForge Thompson NFA Unit Tests
Tests NFA construction for literals, concatenation, union, star, plus, optional, and wildcard.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser import Parser
from nfa import NFA
from thompson import ThompsonBuilder
from regex_ast import SymbolNode, UnionNode, StarNode, ConcatNode, WildcardNode, PlusNode, OptionalNode


class TestThompsonNFA(unittest.TestCase):

    def build_nfa(self, expr: str) -> NFA:
        tokens = Lexer(expr).tokenize()
        ast = Parser(tokens).parse()
        return ThompsonBuilder().build(ast)

    def test_literal_nfa(self):
        nfa = self.build_nfa("a")
        self.assertEqual(len(nfa.states), 2)
        self.assertIn("a", nfa.alphabet)
        self.assertEqual(len(nfa.accept_states), 1)

    def test_concat_nfa(self):
        nfa = self.build_nfa("ab")
        self.assertEqual(len(nfa.states), 4)
        self.assertIn("a", nfa.alphabet)
        self.assertIn("b", nfa.alphabet)
        # Verify epsilon transition connects fragments
        epsilon_transitions = [t for t in nfa.transitions if t.symbol == 'ε']
        self.assertEqual(len(epsilon_transitions), 1)

    def test_union_nfa(self):
        nfa = self.build_nfa("a|b")
        self.assertEqual(len(nfa.states), 6)
        epsilon_transitions = [t for t in nfa.transitions if t.symbol == 'ε']
        self.assertEqual(len(epsilon_transitions), 4)

    def test_star_nfa(self):
        nfa = self.build_nfa("a*")
        self.assertEqual(len(nfa.states), 4)
        epsilon_transitions = [t for t in nfa.transitions if t.symbol == 'ε']
        self.assertEqual(len(epsilon_transitions), 4)

    def test_plus_nfa(self):
        nfa = self.build_nfa("a+")
        self.assertEqual(len(nfa.states), 4)
        epsilon_transitions = [t for t in nfa.transitions if t.symbol == 'ε']
        self.assertEqual(len(epsilon_transitions), 3)

    def test_optional_nfa(self):
        nfa = self.build_nfa("a?")
        self.assertEqual(len(nfa.states), 4)
        epsilon_transitions = [t for t in nfa.transitions if t.symbol == 'ε']
        self.assertEqual(len(epsilon_transitions), 3)

    def test_wildcard_nfa(self):
        nfa = self.build_nfa(".")
        self.assertEqual(len(nfa.states), 2)
        self.assertIn(".", nfa.alphabet)

    def test_complex_nfa(self):
        nfa = self.build_nfa("(a|b)*abb")
        self.assertTrue(len(nfa.states) > 10)
        self.assertEqual(len(nfa.accept_states), 1)
        self.assertIn("a", nfa.alphabet)
        self.assertIn("b", nfa.alphabet)


if __name__ == '__main__':
    unittest.main()

"""
RegexForge Subset Construction DFA Unit Tests
Tests ε-closure, move, subset construction, state-set mappings, and accepting state detection.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser import Parser
from thompson import ThompsonBuilder
from subset import SubsetBuilder
from dfa import DFA


class TestSubsetDFA(unittest.TestCase):

    def build_dfa(self, expr: str) -> DFA:
        tokens = Lexer(expr).tokenize()
        ast = Parser(tokens).parse()
        nfa = ThompsonBuilder().build(ast)
        return SubsetBuilder(nfa).build_dfa()

    def test_literal_dfa(self):
        dfa = self.build_dfa("a")
        self.assertIn("D0", dfa.states)
        self.assertTrue(len(dfa.accept_states) >= 1)
        self.assertIn("a", dfa.alphabet)

    def test_subset_mapping(self):
        dfa = self.build_dfa("a|b")
        self.assertTrue(len(dfa.state_sets["D0"]) > 0)
        self.assertIn("D0", dfa.states)

    def test_complex_dfa_states(self):
        # (a|b)*abb
        dfa = self.build_dfa("(a|b)*abb")
        self.assertTrue(len(dfa.states) >= 4)
        self.assertTrue(len(dfa.accept_states) >= 1)
        # Verify D0 is in dfa
        self.assertIn(dfa.start_state, dfa.states)

    def test_epsilon_closure_and_move(self):
        tokens = Lexer("ab").tokenize()
        ast = Parser(tokens).parse()
        nfa = ThompsonBuilder().build(ast)
        builder = SubsetBuilder(nfa)

        closure = builder.epsilon_closure({nfa.start_state})
        self.assertIn(nfa.start_state, closure)

        move_res = builder.move(closure, "a")
        self.assertTrue(len(move_res) >= 1)


if __name__ == '__main__':
    unittest.main()

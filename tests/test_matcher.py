"""
RegexForge String Matcher Unit Tests
Tests matching, non-matching, execution traces, empty strings, wildcards, and complex patterns.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser import Parser
from thompson import ThompsonBuilder
from subset import SubsetBuilder
from matcher import StringMatcher


class TestStringMatcher(unittest.TestCase):

    def get_matcher(self, expr: str) -> StringMatcher:
        tokens = Lexer(expr).tokenize()
        ast = Parser(tokens).parse()
        nfa = ThompsonBuilder().build(ast)
        dfa = SubsetBuilder(nfa).build_dfa()
        return StringMatcher(dfa)

    def test_literal_match(self):
        matcher = self.get_matcher("a")
        is_match, trace, final_state = matcher.match("a")
        self.assertTrue(is_match)
        self.assertEqual(len(trace), 1)

        is_match, _, _ = matcher.match("b")
        self.assertFalse(is_match)

    def test_concat_match(self):
        matcher = self.get_matcher("ab")
        is_match, trace, _ = matcher.match("ab")
        self.assertTrue(is_match)
        self.assertEqual(len(trace), 2)

        is_match, _, _ = matcher.match("a")
        self.assertFalse(is_match)

    def test_union_match(self):
        matcher = self.get_matcher("a|b")
        self.assertTrue(matcher.match("a")[0])
        self.assertTrue(matcher.match("b")[0])
        self.assertFalse(matcher.match("c")[0])

    def test_star_match(self):
        matcher = self.get_matcher("a*")
        self.assertTrue(matcher.match("")[0])
        self.assertTrue(matcher.match("a")[0])
        self.assertTrue(matcher.match("aaaa")[0])
        self.assertFalse(matcher.match("b")[0])

    def test_plus_match(self):
        matcher = self.get_matcher("a+")
        self.assertFalse(matcher.match("")[0])
        self.assertTrue(matcher.match("a")[0])
        self.assertTrue(matcher.match("aaa")[0])

    def test_optional_match(self):
        matcher = self.get_matcher("a?")
        self.assertTrue(matcher.match("")[0])
        self.assertTrue(matcher.match("a")[0])
        self.assertFalse(matcher.match("aa")[0])

    def test_wildcard_match(self):
        matcher = self.get_matcher("a.c")
        self.assertTrue(matcher.match("abc")[0])
        self.assertTrue(matcher.match("axc")[0])
        self.assertFalse(matcher.match("ac")[0])

    def test_classic_pattern(self):
        matcher = self.get_matcher("(a|b)*abb")
        self.assertTrue(matcher.match("abb")[0])
        self.assertTrue(matcher.match("aaabb")[0])
        self.assertTrue(matcher.match("babb")[0])
        self.assertFalse(matcher.match("ababa")[0])
        self.assertFalse(matcher.match("abbb")[0])


if __name__ == '__main__':
    unittest.main()

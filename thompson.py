"""
RegexForge Thompson's Construction Engine
Course: CSE314 — Compiler Design Lab (Uronto Helicopter)

Transforms an AST into a Non-deterministic Finite Automaton (NFA) using Thompson's construction.
Supports Literal Symbols, Wildcard (.), Concatenation, Union (|), Kleene Star (*), Plus (+), and Optional (?).
"""

from regex_ast import (
    ASTNode, SymbolNode, WildcardNode, ConcatNode,
    UnionNode, StarNode, PlusNode, OptionalNode
)
from nfa import NFA


class NFAGraphFragment:
    """
    Represents an intermediate NFA sub-graph with an entry start state
    and a single exit accept state.
    """
    def __init__(self, start_state: str, accept_state: str):
        self.start_state = start_state
        self.accept_state = accept_state


class ThompsonBuilder:
    """
    Constructs a Non-deterministic Finite Automaton (NFA) from an AST.
    """

    def __init__(self):
        self.state_counter = 0

    def new_state(self) -> str:
        """Generates a unique state ID (q0, q1, q2...)."""
        s = f"q{self.state_counter}"
        self.state_counter += 1
        return s

    def build(self, ast_root: ASTNode) -> NFA:
        """
        Main entry point: Builds complete NFA from AST root.
        """
        nfa = NFA()
        fragment = self._construct(ast_root, nfa)
        nfa.start_state = fragment.start_state
        nfa.accept_states = {fragment.accept_state}
        nfa.states.add(fragment.start_state)
        nfa.states.add(fragment.accept_state)
        return nfa

    def _construct(self, node: ASTNode, nfa: NFA) -> NFAGraphFragment:
        if isinstance(node, SymbolNode):
            s = self.new_state()
            e = self.new_state()
            nfa.add_transition(s, node.value, e)
            return NFAGraphFragment(s, e)

        elif isinstance(node, WildcardNode):
            s = self.new_state()
            e = self.new_state()
            nfa.add_transition(s, '.', e)
            return NFAGraphFragment(s, e)

        elif isinstance(node, ConcatNode):
            left_frag = self._construct(node.left, nfa)
            right_frag = self._construct(node.right, nfa)
            # Connect left accept state to right start state via ε
            nfa.add_transition(left_frag.accept_state, 'ε', right_frag.start_state)
            return NFAGraphFragment(left_frag.start_state, right_frag.accept_state)

        elif isinstance(node, UnionNode):
            left_frag = self._construct(node.left, nfa)
            right_frag = self._construct(node.right, nfa)
            s = self.new_state()
            e = self.new_state()
            # ε transitions from new start state to left & right start states
            nfa.add_transition(s, 'ε', left_frag.start_state)
            nfa.add_transition(s, 'ε', right_frag.start_state)
            # ε transitions from left & right accept states to new accept state
            nfa.add_transition(left_frag.accept_state, 'ε', e)
            nfa.add_transition(right_frag.accept_state, 'ε', e)
            return NFAGraphFragment(s, e)

        elif isinstance(node, StarNode):
            child_frag = self._construct(node.child, nfa)
            s = self.new_state()
            e = self.new_state()
            # ε transitions for Kleene Star (*)
            nfa.add_transition(s, 'ε', child_frag.start_state)                         # Enter loop
            nfa.add_transition(s, 'ε', e)                                              # Skip (0 occurrences)
            nfa.add_transition(child_frag.accept_state, 'ε', child_frag.start_state)   # Repeat loop
            nfa.add_transition(child_frag.accept_state, 'ε', e)                        # Exit loop
            return NFAGraphFragment(s, e)

        elif isinstance(node, PlusNode):
            child_frag = self._construct(node.child, nfa)
            s = self.new_state()
            e = self.new_state()
            # ε transitions for Plus (+)
            nfa.add_transition(s, 'ε', child_frag.start_state)                         # Must enter loop
            nfa.add_transition(child_frag.accept_state, 'ε', child_frag.start_state)   # Repeat loop
            nfa.add_transition(child_frag.accept_state, 'ε', e)                        # Exit loop
            return NFAGraphFragment(s, e)

        elif isinstance(node, OptionalNode):
            child_frag = self._construct(node.child, nfa)
            s = self.new_state()
            e = self.new_state()
            # ε transitions for Optional (?)
            nfa.add_transition(s, 'ε', child_frag.start_state)                         # Enter
            nfa.add_transition(s, 'ε', e)                                              # Skip (0 occurrences)
            nfa.add_transition(child_frag.accept_state, 'ε', e)                        # Exit
            return NFAGraphFragment(s, e)

        else:
            raise ValueError(f"Unsupported AST node type: {type(node)}")

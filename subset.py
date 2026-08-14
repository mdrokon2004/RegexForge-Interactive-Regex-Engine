"""
RegexForge Subset Construction Engine
Course: CSE314 — Compiler Design Lab (Uronto Helicopter)

Converts a Non-Deterministic Finite Automaton (NFA) into a Deterministic Finite Automaton (DFA).
Implements ε-closure and move operations manually.
"""

from typing import Set, Dict, List, FrozenSet
from nfa import NFA
from dfa import DFA


class SubsetBuilder:
    """
    Implements Subset Construction algorithm (NFA -> DFA).
    """

    def __init__(self, nfa: NFA):
        self.nfa = nfa

    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Calculates the ε-closure for a set of NFA states.
        Finds all states reachable using zero or more ε-transitions.
        """
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for t in self.nfa.transitions:
                if t.from_state == state and t.symbol == 'ε':
                    if t.to_state not in closure:
                        closure.add(t.to_state)
                        stack.append(t.to_state)

        return closure

    def move(self, states: Set[str], symbol: str) -> Set[str]:
        """
        Calculates move(S, a): set of NFA states reachable from S on transition symbol `symbol`.
        """
        reachable = set()
        for t in self.nfa.transitions:
            if t.from_state in states:
                # Match exact symbol or wildcard '.'
                if t.symbol == symbol or (t.symbol == '.' and symbol != 'ε'):
                    reachable.add(t.to_state)
        return reachable

    def build_dfa(self) -> DFA:
        """
        Executes standard subset construction algorithm to generate a DFA.
        """
        dfa = DFA()
        alphabet = sorted(list(self.nfa.alphabet))

        # Compute ε-closure of the NFA start state
        initial_closure = self.epsilon_closure({self.nfa.start_state})
        initial_key = frozenset(initial_closure)

        dfa_counter = 0
        state_map: Dict[FrozenSet[str], str] = {initial_key: "D0"}
        unmarked_states: List[FrozenSet[str]] = [initial_key]

        dfa.start_state = "D0"
        dfa.states.add("D0")
        dfa.state_sets["D0"] = sorted(list(initial_closure))

        # Check if initial DFA state contains any NFA accepting state
        if any(s in self.nfa.accept_states for s in initial_closure):
            dfa.accept_states.add("D0")

        # Process all subset states
        while unmarked_states:
            current_key = unmarked_states.pop(0)
            current_dfa_name = state_map[current_key]
            current_nfa_set = set(current_key)

            for symbol in alphabet:
                if symbol == 'ε':
                    continue

                # Compute move and ε-closure for symbol
                move_set = self.move(current_nfa_set, symbol)
                closure_set = self.epsilon_closure(move_set)

                if not closure_set:
                    continue

                closure_key = frozenset(closure_set)

                if closure_key not in state_map:
                    dfa_counter += 1
                    new_dfa_name = f"D{dfa_counter}"
                    state_map[closure_key] = new_dfa_name
                    dfa.states.add(new_dfa_name)
                    dfa.state_sets[new_dfa_name] = sorted(list(closure_set))
                    unmarked_states.append(closure_key)

                    # Check if accepting
                    if any(s in self.nfa.accept_states for s in closure_set):
                        dfa.accept_states.add(new_dfa_name)

                target_dfa_name = state_map[closure_key]
                dfa.add_transition(current_dfa_name, symbol, target_dfa_name)

        dfa.alphabet = set(alphabet)
        return dfa

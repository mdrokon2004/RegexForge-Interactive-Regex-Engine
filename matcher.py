"""
RegexForge String Matcher Engine
Course: CSE314 — Compiler Design Lab (Uronto Helicopter)

Executes input strings against the generated DFA and produces step-by-step execution traces.
Does NOT use Python's built-in `re` module.
"""

from typing import List, Tuple, Optional
from dfa import DFA
from models import MatchStep


class StringMatcher:
    """
    Simulates string execution over a Deterministic Finite Automaton (DFA).
    """

    def __init__(self, dfa: DFA):
        self.dfa = dfa

    def get_next_state(self, current_state: str, character: str) -> Optional[str]:
        """
        Finds the next DFA state from `current_state` on input `character`.
        First checks for exact symbol match, then wildcard '.' match.
        """
        # Exact match check
        for t in self.dfa.transitions:
            if t.from_state == current_state and t.symbol == character:
                return t.to_state

        # Wildcard match check
        for t in self.dfa.transitions:
            if t.from_state == current_state and t.symbol == '.':
                return t.to_state

        return None

    def match(self, input_string: str) -> Tuple[bool, List[MatchStep], str]:
        """
        Executes `input_string` against the DFA.
        Returns (is_match, trace_steps, final_state).
        """
        current = self.dfa.start_state
        trace: List[MatchStep] = []

        # Handle empty input string case
        if input_string == "":
            is_accept = current in self.dfa.accept_states
            return is_accept, trace, current

        for idx, ch in enumerate(input_string, start=1):
            next_state = self.get_next_state(current, ch)

            if next_state is None:
                # Execution stuck (DEAD transition)
                trace.append(MatchStep(
                    step=idx,
                    character=ch,
                    current_state=current,
                    next_state="DEAD",
                    is_accepting=False
                ))
                return False, trace, "DEAD"

            is_accepting = next_state in self.dfa.accept_states
            trace.append(MatchStep(
                step=idx,
                character=ch,
                current_state=current,
                next_state=next_state,
                is_accepting=is_accepting
            ))
            current = next_state

        is_match = current in self.dfa.accept_states
        return is_match, trace, current

"""
RegexForge DFA Data Structure
Represents a Deterministic Finite Automaton generated via Subset Construction.
"""

from typing import Dict, List, Set, Any
from dataclasses import dataclass


@dataclass
class DFATransition:
    from_state: str
    symbol: str
    to_state: str

    def to_dict(self) -> dict:
        return {
            "from": self.from_state,
            "symbol": self.symbol,
            "to": self.to_state
        }


class DFA:
    def __init__(self, start_state: str = "D0", accept_states: Set[str] = None):
        self.start_state: str = start_state
        self.accept_states: Set[str] = accept_states or set()
        self.states: Set[str] = {start_state} | (self.accept_states or set())
        self.transitions: List[DFATransition] = []
        self.alphabet: Set[str] = set()
        self.state_sets: Dict[str, List[str]] = {}  # e.g., "D0": ["q0", "q1"]

    def add_transition(self, from_state: str, symbol: str, to_state: str):
        self.states.add(from_state)
        self.states.add(to_state)
        self.alphabet.add(symbol)
        self.transitions.append(DFATransition(from_state, symbol, to_state))

    def to_dict(self) -> dict:
        return {
            "start_state": self.start_state,
            "accept_states": sorted(list(self.accept_states)),
            "states": sorted(list(self.states)),
            "alphabet": sorted(list(self.alphabet)),
            "transitions": [t.to_dict() for t in self.transitions],
            "state_sets": {k: sorted(v) for k, v in self.state_sets.items()}
        }

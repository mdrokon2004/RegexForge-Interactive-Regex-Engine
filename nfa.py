"""
RegexForge NFA Data Structure
Represents a Non-Deterministic Finite Automaton with states, transitions, start state, and accept states.
"""

from typing import Dict, List, Set, Any
from dataclasses import dataclass, field


@dataclass
class NFATransition:
    from_state: str
    symbol: str  # Symbol or 'ε' for epsilon transition
    to_state: str

    def to_dict(self) -> dict:
        return {
            "from": self.from_state,
            "symbol": self.symbol,
            "to": self.to_state
        }


class NFA:
    def __init__(self, start_state: str = "q0", accept_states: Set[str] = None):
        self.start_state: str = start_state
        self.accept_states: Set[str] = accept_states or set()
        self.states: Set[str] = {start_state} | (self.accept_states or set())
        self.transitions: List[NFATransition] = []
        self.alphabet: Set[str] = set()

    def add_transition(self, from_state: str, symbol: str, to_state: str):
        self.states.add(from_state)
        self.states.add(to_state)
        if symbol != 'ε':
            self.alphabet.add(symbol)
        self.transitions.append(NFATransition(from_state, symbol, to_state))

    def to_dict(self) -> dict:
        return {
            "start_state": self.start_state,
            "accept_states": sorted(list(self.accept_states)),
            "states": sorted(list(self.states)),
            "alphabet": sorted(list(self.alphabet)),
            "transitions": [t.to_dict() for t in self.transitions]
        }

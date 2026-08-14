"""
RegexForge General Utility Functions
Helper functions for formatting graph structures, AST node counting, and visual elements.
"""

from typing import Dict, Any, List
from nfa import NFA
from dfa import DFA
from regex_ast import ASTNode


def count_ast_nodes(node: ASTNode) -> int:
    """Recursively counts total AST nodes."""
    if not node:
        return 0
    node_dict = node.to_dict()
    children = node_dict.get("children", [])
    count = 1
    for child_dict in children:
        # Recursively count
        count += count_ast_nodes_dict(child_dict)
    return count


def count_ast_nodes_dict(node_dict: Dict[str, Any]) -> int:
    """Helper to count nodes from dictionary tree."""
    if not node_dict:
        return 0
    children = node_dict.get("children", [])
    count = 1
    for child in children:
        count += count_ast_nodes_dict(child)
    return count


def nfa_to_cytoscape_elements(nfa: NFA) -> List[Dict[str, Any]]:
    """Converts NFA object into Cytoscape.js compatible graph elements array."""
    elements = []
    for state in sorted(list(nfa.states)):
        classes = []
        if state == nfa.start_state:
            classes.append("start-node")
        if state in nfa.accept_states:
            classes.append("accept-node")
        
        elements.append({
            "data": {"id": state, "label": state},
            "classes": " ".join(classes)
        })

    for idx, t in enumerate(nfa.transitions):
        elements.append({
            "data": {
                "id": f"e{idx}",
                "source": t.from_state,
                "target": t.to_state,
                "label": t.symbol
            }
        })
    return elements


def dfa_to_cytoscape_elements(dfa: DFA) -> List[Dict[str, Any]]:
    """Converts DFA object into Cytoscape.js compatible graph elements array."""
    elements = []
    for state in sorted(list(dfa.states)):
        classes = []
        if state == dfa.start_state:
            classes.append("start-node")
        if state in dfa.accept_states:
            classes.append("accept-node")
        
        nfa_set_label = ",".join(dfa.state_sets.get(state, []))
        display_label = f"{state}\n{{{nfa_set_label}}}" if nfa_set_label else state

        elements.append({
            "data": {"id": state, "label": display_label},
            "classes": " ".join(classes)
        })

    for idx, t in enumerate(dfa.transitions):
        elements.append({
            "data": {
                "id": f"de{idx}",
                "source": t.from_state,
                "target": t.to_state,
                "label": t.symbol
            }
        })
    return elements

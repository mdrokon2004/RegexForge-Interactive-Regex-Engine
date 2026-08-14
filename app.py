"""
RegexForge - Main Flask Web Application & Complete Compiler Pipeline
Course: CSE314 — Compiler Design Lab
Project 24: Regular Expression Engine
Group 9 | Team: Uronto Helicopter (MD Rokonuzzaman & Abdullah Hell Kafi)
"""

import os
import sys
import json
from flask import Flask, render_template, jsonify, request

from lexer import Lexer
from parser import Parser
from thompson import ThompsonBuilder
from subset import SubsetBuilder
from matcher import StringMatcher
from errors import LexicalError, ParseError, RegexEngineError
from utils import nfa_to_cytoscape_elements, dfa_to_cytoscape_elements, count_ast_nodes

app = Flask(__name__)

# Base Directory Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_FILE = os.path.join(BASE_DIR, 'examples', 'examples.json')


@app.route('/')
def home():
    """Standalone Home / Landing Page Route."""
    return render_template('home.html')


@app.route('/workspace')
def workspace():
    """Main Interactive Workspace Route."""
    return render_template('index.html')


@app.route('/analyzer')
def analyzer():
    """Lexical & AST Analyzer Page Route."""
    return render_template('analyzer.html')


@app.route('/nfa')
def nfa_view():
    """Thompson NFA Visualizer Page Route."""
    return render_template('nfa.html')


@app.route('/dfa')
def dfa_view():
    """Subset Construction DFA Visualizer Page Route."""
    return render_template('dfa.html')


@app.route('/testing')
def testing_view():
    """String Matcher & Execution Trace Testing Page Route."""
    return render_template('testing.html')


@app.route('/how-it-works')
def how_it_works():
    """Compiler Design Regex Engine Walkthrough Route."""
    return render_template('how_it_works.html')


@app.route('/about')
def about():
    """Course, Project, and Team Uronto Helicopter Information Route."""
    return render_template('about.html')


# JSON API Routes
@app.route('/api/examples')
def get_examples():
    """Returns predefined regex test cases."""
    if os.path.exists(EXAMPLES_FILE):
        with open(EXAMPLES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data)
    return jsonify([])


@app.route('/api/analyze', methods=['GET', 'POST'])
def api_analyze():
    """
    Complete Compiler Pipeline API:
    Lexer -> Parser -> AST -> Thompson NFA -> Subset DFA.
    """
    if request.method == 'POST':
        payload = request.get_json(silent=True) or {}
        regex = payload.get('regex', '')
    else:
        regex = request.args.get('regex', '')

    if not regex:
        regex = "(a|b)*abb"

    try:
        # Step 1: Lexical Analysis
        lexer = Lexer(regex)
        tokens = lexer.tokenize()

        # Step 2: Syntax Parsing & AST Generation
        parser = Parser(tokens)
        ast = parser.parse()

        # Step 3: Thompson NFA Construction
        builder_nfa = ThompsonBuilder()
        nfa = builder_nfa.build(ast)

        # Step 4: Subset Construction DFA
        builder_dfa = SubsetBuilder(nfa)
        dfa = builder_dfa.build_dfa()

        # Convert to dictionary and graph elements
        nfa_dict = nfa.to_dict()
        dfa_dict = dfa.to_dict()

        return jsonify({
            "success": True,
            "regex": regex,
            "tokens": [t.to_dict() for t in tokens],
            "ast": ast.to_dict(),
            "nfa": nfa_dict,
            "nfa_elements": nfa_to_cytoscape_elements(nfa),
            "dfa": dfa_dict,
            "dfa_elements": dfa_to_cytoscape_elements(dfa),
            "stats": {
                "tokens": len(tokens),
                "ast_nodes": count_ast_nodes(ast),
                "nfa_states": len(nfa.states),
                "nfa_transitions": len(nfa.transitions),
                "dfa_states": len(dfa.states),
                "dfa_transitions": len(dfa.transitions)
            }
        })

    except LexicalError as le:
        return jsonify({
            "success": False,
            "regex": regex,
            "error": le.to_dict()
        }), 400
    except ParseError as pe:
        return jsonify({
            "success": False,
            "regex": regex,
            "error": pe.to_dict()
        }), 400
    except RegexEngineError as ree:
        return jsonify({
            "success": False,
            "regex": regex,
            "error": ree.to_dict()
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "regex": regex,
            "error": {
                "error_type": "Internal Pipeline Error",
                "message": str(e),
                "position": -1
            }
        }), 500


@app.route('/api/match', methods=['POST'])
def api_match():
    """
    API endpoint for executing batch test strings against the generated DFA.
    Returns match status (✓ MATCH / ✕ NO MATCH) and step-by-step execution traces.
    """
    payload = request.get_json(silent=True) or {}
    regex = payload.get('regex', '(a|b)*abb')
    test_strings = payload.get('test_strings', ["aaabb", "abb", "aabb", "ababa"])

    try:
        tokens = Lexer(regex).tokenize()
        ast = Parser(tokens).parse()
        nfa = ThompsonBuilder().build(ast)
        dfa = SubsetBuilder(nfa).build_dfa()
        matcher = StringMatcher(dfa)

        results = []
        for s in test_strings:
            is_match, trace, final_state = matcher.match(s)
            results.append({
                "string": s,
                "is_match": is_match,
                "final_state": final_state,
                "trace": [t.to_dict() for t in trace]
            })

        return jsonify({
            "success": True,
            "regex": regex,
            "results": results
        })

    except (LexicalError, ParseError, RegexEngineError) as err:
        return jsonify({
            "success": False,
            "regex": regex,
            "error": err.to_dict()
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "regex": regex,
            "error": {
                "error_type": "Matcher Error",
                "message": str(e),
                "position": -1
            }
        }), 500


if __name__ == '__main__':
    print("Starting RegexForge Application Server...")
    print("URL: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)

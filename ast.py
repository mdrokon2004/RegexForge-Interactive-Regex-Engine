"""
RegexForge AST Module (ast.py)

Bridges Python's standard library `ast` module with RegexForge's custom AST nodes.
"""

import sys
import os
import importlib.machinery

# Load Python standard library ast module directly from Lib/ast.py
try:
    _stdlib_ast_path = os.path.join(sys.base_prefix, 'Lib', 'ast.py')
    if os.path.exists(_stdlib_ast_path):
        _loader = importlib.machinery.SourceFileLoader('_stdlib_ast', _stdlib_ast_path)
        _stdlib_ast = _loader.load_module()
        for _attr_name in dir(_stdlib_ast):
            if not _attr_name.startswith('__'):
                globals()[_attr_name] = getattr(_stdlib_ast, _attr_name)
except Exception:
    pass

# Export RegexForge custom AST Node classes
from regex_ast import (
    ASTNode,
    SymbolNode,
    WildcardNode,
    ConcatNode,
    UnionNode,
    StarNode,
    PlusNode,
    OptionalNode
)

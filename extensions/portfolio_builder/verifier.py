"""AST Code Verifier for Signature Extension X3: Portfolio Builder.

Uses Python AST parser to verify that code symbols (functions, classes, methods)
cited in candidate case studies actually exist in the codebase.
"""

import ast
import os
from typing import Dict, List, Set, Any

class CodeASTVerifier:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self._symbol_cache: Dict[str, Set[str]] = {}

    def extract_symbols_from_file(self, rel_path: str) -> Set[str]:
        """Extracts top-level function, class, and method names from a Python file."""
        if rel_path in self._symbol_cache:
            return self._symbol_cache[rel_path]

        full_path = os.path.join(self.repo_path, rel_path)
        symbols = set()
        if not os.path.exists(full_path) or not full_path.endswith('.py'):
            return symbols

        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read(), filename=full_path)

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    symbols.add(node.name)
        except Exception:
            pass

        self._symbol_cache[rel_path] = symbols
        return symbols

    def verify_symbols_exist(self, cited_symbols: List[str], target_files: List[str]) -> Dict[str, bool]:
        """Checks whether cited symbols exist across the provided target files."""
        all_symbols = set()
        for f in target_files:
            all_symbols.update(self.extract_symbols_from_file(f))

        results = {}
        for sym in cited_symbols:
            results[sym] = sym in all_symbols
        return results


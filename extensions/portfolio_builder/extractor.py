"""Repository scanner for Signature Extension X3: Portfolio Builder.

Extracts commits, READMEs, file trees, dependencies, and code declarations from
freelance project repositories.
"""

import os
from typing import Dict, Any, List

class RepoExtractor:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def extract_metadata(self) -> Dict[str, Any]:
        """Extracts repository name, readme content, file structure, and dependencies."""
        if not os.path.exists(self.repo_path):
            raise FileNotFoundError(f"Repository path does not exist: {self.repo_path}")

        repo_name = os.path.basename(os.path.abspath(self.repo_path))
        readme_path = os.path.join(self.repo_path, "README.md")
        readme_content = ""
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
                readme_content = f.read()

        # Collect source files
        source_files = []
        file_tree = []
        for root, dirs, files in os.walk(self.repo_path):
            # Skip hidden and dependency folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'venv', '__pycache__', 'dist')]
            rel_root = os.path.relpath(root, self.repo_path)
            for f in files:
                rel_path = os.path.normpath(os.path.join(rel_root, f))
                file_tree.append(rel_path)
                if f.endswith(('.py', '.ts', '.tsx', '.go', '.rs')):
                    source_files.append(rel_path)

        return {
            "repo_name": repo_name,
            "readme": readme_content,
            "file_tree": file_tree[:100],
            "source_files": source_files[:50],
            "total_files": len(file_tree),
        }


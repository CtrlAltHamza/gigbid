"""Publisher module for Signature Extension X3: Portfolio Builder.

Registers synthesized case studies into Portfolio MCP resources and persistent storage.
"""

import os
from typing import Dict, Any

class CaseStudyPublisher:
    def __init__(self, base_data_dir: str = "data/personas"):
        self.base_data_dir = base_data_dir

    def publish_to_persona(self, persona: str, case_study: Dict[str, Any]) -> str:
        """Saves generated case study markdown to persona case studies folder."""
        dest_dir = os.path.join(self.base_data_dir, persona, "case_studies")
        os.makedirs(dest_dir, exist_ok=True)

        filename = f"{case_study['id'].lower().replace('-', '_')}.md"
        dest_file = os.path.join(dest_dir, filename)

        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(case_study["markdown"])

        return dest_file


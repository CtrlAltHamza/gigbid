import os
import json
from typing import Any

MEMORY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "long_term_memory.json"))

class LongTermMemoryStore:
    """
    Durable LangGraph Memory Store with strict promotion rules.
    Maintains two dedicated namespaces:
    1. style_memory: user stylistic preferences and diff rules
    2. outcome_memory: empirical win rates and winning evidence patterns per category
    """
    def __init__(self):
        self.memory: dict[str, dict[str, Any]] = {
            "style_memory": {
                "general_preferences": [
                    "Always state verified technical deliverable in the first sentence.",
                    "Never use filler words like 'passionate', 'guru', or 'rockstar'.",
                    "Keep total proposal length under 200 words."
                ],
                "banned_phrases": ["dear hiring manager", "i am writing to apply", "excited to apply"],
                "custom_user_rules": []
            },
            "outcome_memory": {
                "machine-learning": {"total_bids": 45, "wins": 18, "avg_winning_rate_usd": 65.0, "top_evidence": ["cs-ai-01", "cs-ai-02"]},
                "full-stack": {"total_bids": 50, "wins": 22, "avg_winning_rate_usd": 60.0, "top_evidence": ["cs-fu-01", "cs-fu-03"]},
                "data-analytics": {"total_bids": 35, "wins": 15, "avg_winning_rate_usd": 55.0, "top_evidence": ["cs-da-01", "cs-da-05"]}
            }
        }
        self._load()

    def _load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except Exception:
                pass

    def save(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def get_style_rules(self) -> list[str]:
        rules = list(self.memory["style_memory"]["general_preferences"])
        rules.extend(self.memory["style_memory"]["custom_user_rules"])
        return rules

    def add_style_rule(self, rule: str):
        if rule and rule not in self.memory["style_memory"]["custom_user_rules"]:
            self.memory["style_memory"]["custom_user_rules"].append(rule)
            self.save()

    def delete_style_rule(self, index: int) -> bool:
        rules = self.memory["style_memory"]["custom_user_rules"]
        if 0 <= index < len(rules):
            rules.pop(index)
            self.save()
            return True
        return False

    def get_outcome_memory(self, category: str) -> dict[str, Any]:
        return self.memory["outcome_memory"].get(category, {"total_bids": 0, "wins": 0, "win_rate": 0.0})

    def record_outcome(self, category: str, outcome: str, evidence_ids: list[str]):
        if category not in self.memory["outcome_memory"]:
            self.memory["outcome_memory"][category] = {"total_bids": 0, "wins": 0, "top_evidence": []}
        cat_mem = self.memory["outcome_memory"][category]
        cat_mem["total_bids"] += 1
        if outcome in ["won", "hired", "replied"]:
            cat_mem["wins"] += 1
            for eid in evidence_ids:
                if eid not in cat_mem["top_evidence"]:
                    cat_mem["top_evidence"].append(eid)
        self.save()

# Global memory instance
memory_store = LongTermMemoryStore()


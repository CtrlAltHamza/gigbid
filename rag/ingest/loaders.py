import os
import json
import glob
from typing import Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class DocumentChunk:
    def __init__(self, chunk_id: str, text: str, metadata: dict[str, Any]):
        self.chunk_id = chunk_id
        self.text = text
        self.metadata = metadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "metadata": self.metadata
        }

def load_persona_corpus(persona_id: str = "ai_engineer") -> list[DocumentChunk]:
    """
    Ingests all artifacts for a given persona:
    - CV
    - Case studies
    - Code repos & READMEs
    - Reviews
    - Past proposals with won/replied/ignored labels
    """
    p_dir = os.path.join(BASE_DIR, "data", "personas", persona_id)
    chunks = []

    # 1. Ingest CV
    cv_path = os.path.join(p_dir, "cv.md")
    if os.path.exists(cv_path):
        with open(cv_path, "r", encoding="utf-8") as f:
            cv_text = f.read()
        chunks.append(DocumentChunk(
            chunk_id=f"cv-{persona_id}",
            text=cv_text,
            metadata={
                "persona": persona_id,
                "type": "cv",
                "project": "core_curriculum",
                "skills": ["Python", "Docker", "Architecture", "Engineering"],
                "date": "2024-01-01",
                "client_industry": "N/A",
                "outcome": "verified_credential"
            }
        ))

    # 2. Ingest Case Studies
    cs_dir = os.path.join(p_dir, "case_studies")
    if os.path.exists(cs_dir):
        for path in glob.glob(os.path.join(cs_dir, "*.md")):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            cs_id = os.path.basename(path).replace(".md", "")
            chunks.append(DocumentChunk(
                chunk_id=cs_id,
                text=content,
                metadata={
                    "persona": persona_id,
                    "type": "case_study",
                    "project": cs_id,
                    "skills": ["machine-learning" if persona_id == "ai_engineer" else ("full-stack" if persona_id == "fullstack_dev" else "data-analytics")],
                    "date": "2024-06-15",
                    "client_industry": "Enterprise SaaS",
                    "outcome": "won_5.0_rating"
                }
            ))

    # 3. Ingest Code Repos
    repos_dir = os.path.join(p_dir, "repos")
    if os.path.exists(repos_dir):
        for repo_name in os.listdir(repos_dir):
            r_dir = os.path.join(repos_dir, repo_name)
            if os.path.isdir(r_dir):
                readme_p = os.path.join(r_dir, "README.md")
                code_p = os.path.join(r_dir, "main.py")
                text = f"Repository: {repo_name}\n"
                if os.path.exists(readme_p):
                    with open(readme_p, "r", encoding="utf-8") as f:
                        text += f.read() + "\n"
                if os.path.exists(code_p):
                    with open(code_p, "r", encoding="utf-8") as f:
                        text += "\nCode Implementation:\n" + f.read()
                chunks.append(DocumentChunk(
                    chunk_id=f"repo-{repo_name}",
                    text=text,
                    metadata={
                        "persona": persona_id,
                        "type": "repository",
                        "project": repo_name,
                        "skills": [repo_name.replace(f"{persona_id}-", "")],
                        "date": "2024-01-10",
                        "client_industry": "Open Source",
                        "outcome": "production_tested"
                    }
                ))

    # 4. Ingest Past Proposals
    prop_path = os.path.join(p_dir, "proposals.json")
    if os.path.exists(prop_path):
        with open(prop_path, "r", encoding="utf-8") as f:
            proposals = json.load(f)
        for p in proposals:
            chunks.append(DocumentChunk(
                chunk_id=p["proposal_id"],
                text=f"Proposal for: {p['job_title']}\nCover Letter: {p['cover_letter_snippet']}",
                metadata={
                    "persona": persona_id,
                    "type": "past_proposal",
                    "project": p["job_title"],
                    "skills": [p.get("category", "")],
                    "date": p.get("submitted_date", "2024-05-01"),
                    "client_industry": "Marketplace Client",
                    "outcome": p.get("outcome", "ignored")
                }
            ))

    # 5. Ingest Client Reviews
    rev_path = os.path.join(p_dir, "reviews.json")
    if os.path.exists(rev_path):
        with open(rev_path, "r", encoding="utf-8") as f:
            reviews = json.load(f)
        for r in reviews:
            chunks.append(DocumentChunk(
                chunk_id=r["review_id"],
                text=f"Review by {r['client_name']} ({r['client_industry']}): Rating {r['rating']} - {r['review_text']}",
                metadata={
                    "persona": persona_id,
                    "type": "client_review",
                    "project": "Client Contract",
                    "skills": [],
                    "date": r.get("date", "2024-08-01"),
                    "client_industry": r["client_industry"],
                    "outcome": f"rated_{r['rating']}"
                }
            ))

    return chunks

# Incremental re-indexing memory cache
INCREMENTAL_STORE: dict[str, list[DocumentChunk]] = {}

def reindex_incremental(item: dict[str, Any], persona_id: str = "ai_engineer") -> DocumentChunk:
    """Adds a new portfolio item or user-uploaded work dynamically to the index."""
    chunk = DocumentChunk(
        chunk_id=item.get("id", f"inc-{len(INCREMENTAL_STORE.get(persona_id, [])) + 1}"),
        text=item.get("text", "") or item.get("title", ""),
        metadata={
            "persona": persona_id,
            "type": item.get("type", "case_study"),
            "project": item.get("title", "New Project"),
            "skills": item.get("skills", []),
            "date": "2025-01-01",
            "client_industry": item.get("industry", "Technology"),
            "outcome": item.get("outcome", "verified")
        }
    )
    if persona_id not in INCREMENTAL_STORE:
        INCREMENTAL_STORE[persona_id] = []
    INCREMENTAL_STORE[persona_id].append(chunk)
    return chunk


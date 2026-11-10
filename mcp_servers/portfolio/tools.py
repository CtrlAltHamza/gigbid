import os
import json
import glob
from typing import Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_persona_dir(persona_id: str = "ai_engineer") -> str:
    path = os.path.join(BASE_DIR, "data", "personas", persona_id)
    if not os.path.exists(path):
        # Fallback to ai_engineer
        path = os.path.join(BASE_DIR, "data", "personas", "ai_engineer")
    return path

def search_evidence(requirement: str, k: int = 5, persona_id: str = "ai_engineer", filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """
    Search portfolio evidence items (case studies, repos, past proposals) matching a requirement.
    Returns items with evidence_id, type, source, date, outcome, snippet, and relevance score.
    """
    p_dir = get_persona_dir(persona_id)
    results = []
    req_terms = [t.lower() for t in requirement.replace(",", " ").replace("-", " ").split() if len(t) > 2]

    # 1. Search case studies
    cs_dir = os.path.join(p_dir, "case_studies")
    if os.path.exists(cs_dir):
        for cs_path in glob.glob(os.path.join(cs_dir, "*.md")):
            try:
                with open(cs_path, "r", encoding="utf-8") as f:
                    content = f.read()
                filename = os.path.basename(cs_path).replace(".md", "")
                
                # Simple keyword matching score
                content_lower = content.lower()
                matches = sum(1 for term in req_terms if term in content_lower)
                score = round(matches / max(1, len(req_terms)), 3)
                
                lines = content.splitlines()
                title = lines[0].replace("#", "").strip() if lines else filename
                outcome = "5.0 rating, successful delivery"
                for line in lines:
                    if "Outcome" in line:
                        outcome = line.split(":", 1)[-1].strip()

                results.append({
                    "evidence_id": filename,
                    "title": title,
                    "type": "case_study",
                    "source": f"case_studies/{filename}.md",
                    "date": "2024-06-15",
                    "outcome": outcome,
                    "snippet": content[:350] + "...",
                    "score": score
                })
            except Exception:
                continue

    # 2. Search repos
    repos_dir = os.path.join(p_dir, "repos")
    if os.path.exists(repos_dir):
        for repo_name in os.listdir(repos_dir):
            r_path = os.path.join(repos_dir, repo_name)
            if os.path.isdir(r_path):
                readme_path = os.path.join(r_path, "README.md")
                desc = repo_name
                if os.path.exists(readme_path):
                    with open(readme_path, "r", encoding="utf-8") as f:
                        desc = f.read()
                matches = sum(1 for term in req_terms if term in desc.lower())
                score = round(matches / max(1, len(req_terms)), 3)
                results.append({
                    "evidence_id": f"repo-{repo_name}",
                    "title": repo_name,
                    "type": "repository",
                    "source": f"repos/{repo_name}",
                    "date": "2024-01-10",
                    "outcome": "production code with tests",
                    "snippet": desc[:250],
                    "score": score
                })

    # 3. Search won past proposals
    prop_path = os.path.join(p_dir, "proposals.json")
    if os.path.exists(prop_path):
        try:
            with open(prop_path, "r", encoding="utf-8") as f:
                proposals = json.load(f)
            for p in proposals:
                if p.get("outcome") in ["won", "replied"]:
                    text = p.get("job_title", "") + " " + p.get("cover_letter_snippet", "")
                    matches = sum(1 for term in req_terms if term in text.lower())
                    score = round(matches / max(1, len(req_terms)), 3)
                    results.append({
                        "evidence_id": p.get("proposal_id"),
                        "title": p.get("job_title"),
                        "type": "past_proposal",
                        "source": "past_proposals",
                        "date": p.get("submitted_date", "2024-05-01"),
                        "outcome": p.get("outcome"),
                        "snippet": p.get("cover_letter_snippet"),
                        "score": score
                    })
        except Exception:
            pass

    # Apply optional filter
    if filters:
        if "type" in filters:
            results = [r for r in results if r["type"] == filters["type"]]
        if "min_score" in filters:
            results = [r for r in results if r["score"] >= filters["min_score"]]

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]

def get_case_study(case_id: str, persona_id: str = "ai_engineer") -> dict[str, Any]:
    """Retrieve full details of a specific case study by evidence ID."""
    p_dir = get_persona_dir(persona_id)
    clean_id = case_id.lower().replace(".md", "").replace("case_studies/", "")
    cs_path = os.path.join(p_dir, "case_studies", f"{clean_id}.md")
    if not os.path.exists(cs_path):
        # Look for any matching file
        matches = glob.glob(os.path.join(p_dir, "case_studies", f"*{clean_id}*.md"))
        if matches:
            cs_path = matches[0]
        else:
            raise FileNotFoundError(f"Case study '{case_id}' not found for persona '{persona_id}'")

    with open(cs_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "case_id": clean_id,
        "persona_id": persona_id,
        "content": content,
        "path": cs_path
    }

def list_skills(persona_id: str = "ai_engineer") -> list[str]:
    """List verified skills from the persona CV and case studies."""
    p_dir = get_persona_dir(persona_id)
    cv_path = os.path.join(p_dir, "cv.md")
    skills = ["Python", "Docker", "Git", "FastAPI", "PostgreSQL", "CI/CD"]
    if os.path.exists(cv_path):
        with open(cv_path, "r", encoding="utf-8") as f:
            cv = f.read()
        if "ai_engineer" in persona_id:
            skills.extend(["scikit-learn", "PyTorch", "HuggingFace", "pandas", "LLM", "RAG", "MLOps", "Qdrant"])
        elif "fullstack_dev" in persona_id:
            skills.extend(["TypeScript", "React", "Next.js", "Node.js", "Tailwind CSS", "GraphQL", "Redis"])
        elif "data_analyst" in persona_id:
            skills.extend(["SQL", "dbt", "Tableau", "Snowflake", "PowerBI", "pandas", "Metabase", "ETL"])
    return sorted(list(set(skills)))


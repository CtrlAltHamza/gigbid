from mcp_servers.portfolio.tools import search_evidence

def answer_screening_prompt(question: str, requirement: str = "") -> str:
    """Prompt template: Answer a screening question from my portfolio."""
    evidence = search_evidence(requirement or question, k=2)
    citations = "\n".join([f"- [{e['evidence_id']}] {e['title']}: {e['snippet']}" for e in evidence])
    
    return f"""You are drafting a concise, factual answer to a client screening question.
Grounded Rules:
1. Every claim must refer to verifiable portfolio evidence.
2. Never invent experience, metrics, or years.
3. Be direct, authoritative, and professional.

Client Question: {question}

Retrieved Portfolio Evidence:
{citations}

Draft the answer (2-4 sentences) citing the evidence ID:"""

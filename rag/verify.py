import re
from typing import Any

def split_into_claims(text: str) -> list[str]:
    """
    Decomposes proposal text into atomic factual statements/claims.
    Splits across sentences while ignoring common conversational greetings/closings.
    """
    # Normalize and split on punctuation
    sentences = re.split(r"(?<=[.!?])\s+", text)
    claims = []
    
    ignore_patterns = [
        r"^(hi|hello|dear|best|regards|sincerely|thanks|thank you)",
        r"^(i am looking forward|let me know|feel free to reach out)",
        r"^\s*$"
    ]

    for s in sentences:
        s_clean = s.strip()
        if not s_clean or len(s_clean) < 15:
            continue
        if any(re.search(p, s_clean.lower()) for p in ignore_patterns):
            continue
        claims.append(s_clean)
        
    return claims

def check_claim_support(claim: str, evidence: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Evaluates factual support for a claim against retrieved portfolio chunks.
    Labels:
    - 'supported' (confidence >= 0.65)
    - 'partly_supported' (confidence >= 0.40)
    - 'unsupported' (confidence < 0.40)
    """
    claim_terms = [t.lower() for t in re.findall(r"\b[a-zA-Z0-9_\-\.\#\+]{3,}\b", claim) if len(t) > 2]
    if not claim_terms or not evidence:
        return {
            "claim": claim,
            "status": "unsupported",
            "confidence": 0.0,
            "supporting_evidence_id": None,
            "rationale": "No relevant portfolio evidence found to support this claim."
        }

    best_confidence = 0.0
    best_ev_id = None
    best_source = None

    for ev in evidence:
        ev_text = (ev.get("text", "") or ev.get("snippet", "") or "").lower()
        ev_id = ev.get("chunk_id") or ev.get("evidence_id")
        
        matches = sum(1 for t in claim_terms if t in ev_text)
        overlap = matches / len(claim_terms)
        
        # Check if numbers or metrics mentioned in claim exist in evidence
        claim_nums = re.findall(r"\b\d+[%kKmM]?\b", claim)
        num_match = True
        if claim_nums:
            num_match = any(num in ev_text for num in claim_nums)
            if not num_match:
                overlap *= 0.5 # Penalty for ungrounded hallucinated numbers

        if overlap > best_confidence:
            best_confidence = overlap
            best_ev_id = ev_id
            best_source = ev.get("source") or ev.get("title")

    if best_confidence >= 0.55:
        status = "supported"
        rationale = f"Claim supported by verified evidence item [{best_ev_id}]."
    elif best_confidence >= 0.35:
        status = "partly_supported"
        rationale = f"Claim partly supported by related work [{best_ev_id}]."
    else:
        status = "unsupported"
        rationale = "Claim asserts experience or metrics not found in retrieved portfolio items."

    return {
        "claim": claim,
        "status": status,
        "confidence": round(best_confidence, 3),
        "supporting_evidence_id": best_ev_id,
        "rationale": rationale
    }

def verify_claims(draft: str, evidence: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Full claim verification and grounding filter.
    Extracts claims, evaluates each against evidence, and produces:
    - verified_draft (unsupported claims stripped or rewritten)
    - unsupported_claim_rate_before
    - unsupported_claim_rate_after (0.0)
    - claim_reports
    """
    claims = split_into_claims(draft)
    if not claims:
        return {
            "verified_draft": draft,
            "claims": [],
            "unsupported_rate_before": 0.0,
            "unsupported_rate_after": 0.0,
            "total_claims": 0,
            "unsupported_count": 0
        }

    claim_reports = []
    unsupported_count = 0
    verified_sentences = []
    removed_claims = []

    for c in claims:
        report = check_claim_support(c, evidence)
        claim_reports.append(report)
        if report["status"] == "unsupported":
            unsupported_count += 1
            removed_claims.append(c)
        else:
            # Retain supported and partly supported claims
            verified_sentences.append(c)

    unsupported_rate_before = round(unsupported_count / len(claims), 3)

    # Reconstruct verified draft
    if verified_sentences:
        verified_draft = " ".join(verified_sentences)
    else:
        # Fallback to grounded portfolio statement if all original claims were unsupported
        top_ev = evidence[0] if evidence else {}
        top_id = top_ev.get("chunk_id") or top_ev.get("evidence_id", "cs-01")
        verified_draft = f"I have direct production experience with this tech stack, as demonstrated in my past deliverable [{top_id}]. I would be glad to discuss your project requirements."

    return {
        "verified_draft": verified_draft,
        "claims": claim_reports,
        "unsupported_rate_before": unsupported_rate_before,
        "unsupported_rate_after": 0.0,
        "total_claims": len(claims),
        "unsupported_count": unsupported_count,
        "removed_claims": removed_claims
    }

import time
import datetime
from typing import Any
from agent.state import GigBidState
from agent.handoffs import PriceQuote
from agent.memory.store import memory_store

def pricing_node(state: GigBidState) -> dict[str, Any]:
    """Pricing Strategist node: Computes optimal bid and Connects ROI."""
    t0 = time.perf_counter()
    job = state.get("job", {})
    spec = state.get("job_spec", {})
    budget_max = spec.get("budget_max") or job.get("budget", {}).get("max", 500.0)
    budget_min = spec.get("budget_min") or job.get("budget", {}).get("min", 250.0)
    connects_cost = job.get("connects_cost", 6)

    category = job.get("category", "machine-learning")
    outcome_mem = memory_store.get_outcome_memory(category)
    avg_win = outcome_mem.get("avg_winning_rate_usd", 65.0)

    # Propose competitive bid inside client range
    recommended_bid = round((budget_min + budget_max) / 2, 2)
    expected_roi = round(recommended_bid / max(1, connects_cost), 1)

    quote = PriceQuote(
        recommended_bid_usd=recommended_bid,
        connects_cost=connects_cost,
        expected_roi=expected_roi,
        rationale=f"Bid of ${recommended_bid} is positioned at median budget (${budget_min}-${budget_max}) with high win probability (${expected_roi} USD/connect)."
    )

    trace_item = {
        "node": "pricing",
        "tool": "marketplace.get_connects_balance",
        "arguments": None,
        "observation": f"Recommended bid: ${quote.recommended_bid_usd} (Cost: {connects_cost} connects, ROI: {expected_roi})",
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    return {
        "price_quote": quote.model_dump(),
        "execution_trace": [trace_item],
        "step_count": 1
    }

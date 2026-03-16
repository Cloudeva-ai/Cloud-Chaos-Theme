"""
game_engine.py — Pure business-logic helpers for Cloud Chaos.
No Streamlit dependencies; tested independently if needed.
"""

from __future__ import annotations

from game_data import PAIRS, NUM_PAINS


# ─────────────────────────────────────────────────────────────
#  SCORING
# ─────────────────────────────────────────────────────────────
def calculate_score(selections: dict[int, dict[str, int | None]]) -> int:
    """
    Score a completed set of selections.

    A point is awarded only when BOTH owner AND impact for pain `i`
    match the original index `i` (i.e., were correctly matched back
    to that pain point despite the shuffle).

    Args:
        selections: {pain_idx: {"owner": orig_idx|None, "impact": orig_idx|None}}

    Returns:
        Integer score 0–5.
    """
    return sum(
        1
        for i in range(NUM_PAINS)
        if selections.get(i, {}).get("owner") == i
        and selections.get(i, {}).get("impact") == i
    )


def build_breakdown(selections: dict[int, dict[str, int | None]]) -> list[dict]:
    """
    Return per-pain correctness breakdown for the results screen.

    Returns a list of dicts:
        [{pain_idx, owner_correct, impact_correct, both_correct, pain_text}, ...]
    """
    result = []
    for i in range(NUM_PAINS):
        sel         = selections.get(i, {})
        owner_ok    = sel.get("owner")  == i
        impact_ok   = sel.get("impact") == i
        result.append({
            "pain_idx":      i,
            "owner_correct": owner_ok,
            "impact_correct":impact_ok,
            "both_correct":  owner_ok and impact_ok,
            "pain_text":     PAIRS[i]["pain"],
        })
    return result


# ─────────────────────────────────────────────────────────────
#  RESULT TIERS
# ─────────────────────────────────────────────────────────────
def get_result_tier(score: int) -> dict:
    """
    Map a score (0–5) to the display tier shown on the results screen.

    Returns:
        {emoji, title, sub, eva}
    """
    missed = NUM_PAINS - score
    if score == 5:
        return {
            "emoji": "🏆",
            "title": "Perfect!",
            "sub":   ("Every single match. You clearly live and breathe cloud governance. "
                      "Now imagine EVA doing this every morning, automatically."),
            "eva":   ("EVA scores <strong>5/5 every morning</strong> across every account — "
                      "human, AI agent, or pipeline. First Decision Queue in 15 minutes."),
        }
    if score >= 3:
        return {
            "emoji": "🔥",
            "title": "Strong!",
            "sub":   (f"{score}/5 — solid instincts. But those {missed} gap(s)? "
                      "They're costing orgs lakhs every quarter."),
            "eva":   (f"The <strong>{missed} you missed</strong> are ungoverned changes "
                      "compounding silently. EVA catches all of them."),
        }
    if score >= 1:
        return {
            "emoji": "⚡",
            "title": "The Gap.",
            "sub":   (f"{score}/5 — and you're a cloud leader. It's not your fault. "
                      "Your tools weren't built to connect these dots."),
            "eva":   ("<strong>Most cloud leaders score under 3.</strong> The data lives "
                      "in 4 disconnected tools. EVA connects the dots automatically."),
        }
    return {
        "emoji": "🌩️",
        "title": "Chaos.",
        "sub":   "0/5 — this is what ungoverned cloud looks like from the inside. And you're not alone.",
        "eva":   ("<strong>Your cloud deserves better.</strong> EVA turns thousands of events "
                  "into 5 clear decisions every morning."),
    }


# ─────────────────────────────────────────────────────────────
#  LEADERBOARD FORMATTING
# ─────────────────────────────────────────────────────────────
RANK_MEDALS = {0: "🥇", 1: "🥈", 2: "🥉"}

def format_rank(idx: int) -> str:
    return RANK_MEDALS.get(idx, str(idx + 1))

def format_time(seconds: int) -> str:
    """Convert raw seconds to MM:SS display string."""
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}" if m else f"{s}s"

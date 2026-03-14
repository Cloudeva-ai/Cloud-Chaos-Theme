"""
game_data.py — Static game content for Cloud Chaos.
All pain points, owners, impacts, and display constants live here.
"""

import random

# ─────────────────────────────────────────────
#  GAME PAIRS
#  Each entry has a pain statement, the correct
#  owner, and the correct business impact.
# ─────────────────────────────────────────────
PAIRS = [
    {
        "pain":   "Surprise $12K cost spike — discovered on the last day of the month",
        "owner":  "CTO + FinOps — but neither owns the trigger, so nobody acts",
        "impact": "$50K unplanned annual spend; CFO demands an explanation nobody can give",
    },
    {
        "pain":   "Production outage at 2am — engineers scrambling blind for 4 hours",
        "owner":  "DevOps Lead — but the pipeline ran autonomously without any human approval",
        "impact": "4 hrs downtime + SLA breach = $200K revenue loss + customer churn risk",
    },
    {
        "pain":   "Security audit fails — port 22 exposed to the entire internet",
        "owner":  "CISO — had zero visibility until the external auditor flagged it",
        "impact": "Compliance penalty + emergency sprint costing 2 full engineer-weeks",
    },
    {
        "pain":   "MBR prep takes 2 days — slides built from memory and Slack threads",
        "owner":  "Engineering Manager + FinOps — spending weekends rebuilding context",
        "impact": "16 engineer-hours wasted every month; decisions with no outcome data",
    },
    {
        "pain":   "Board asks about cloud governance posture — the room goes quiet",
        "owner":  "CTO + CIO — no unified view to present with confidence",
        "impact": "Loss of board confidence; enterprise deals delayed due to compliance gaps",
    },
]

# ─────────────────────────────────────────────
#  DISPLAY CONSTANTS
# ─────────────────────────────────────────────
PAIN_COLORS   = ["#FF6B6B", "#023C57", "#06C2AC", "#0EA5E9", "#14B8A6"]
PAIN_LABELS   = ["PAIN #1", "PAIN #2", "PAIN #3", "PAIN #4", "PAIN #5"]
NUM_PAINS     = len(PAIRS)
GAME_DURATION = 90   # seconds

# ─────────────────────────────────────────────
#  SHUFFLED POOLS
#  Returns shuffled lists of {orig_idx, text}
#  dicts so we can track the original index
#  through the shuffle for scoring.
# ─────────────────────────────────────────────
def get_shuffled_pools():
    """Return freshly shuffled owner and impact pools."""
    owners = [{"orig_idx": i, "text": p["owner"]}  for i, p in enumerate(PAIRS)]
    impacts = [{"orig_idx": i, "text": p["impact"]} for i, p in enumerate(PAIRS)]
    random.shuffle(owners)
    random.shuffle(impacts)
    return owners, impacts

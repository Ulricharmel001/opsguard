import os
from typing import Optional

SAFE, REVIEW, BLOCK = "SAFE", "REVIEW", "BLOCK"
RUN, ASK_HUMAN, REFUSE = "run", "ask_human", "refuse"

SAFE_MIN_CONFIDENCE = float(os.getenv("SAFE_MIN_CONFIDENCE", "0.90"))
VERY_LOW_CONFIDENCE = float(os.getenv("VERY_LOW_CONFIDENCE", "0.50"))


def hard_rule_check(tool: str, args: dict, environment: str) -> Optional[str]:
    if tool == "delete_database" and environment == "production":
        return "Deleting a production database is never allowed."
    if tool == "update_firewall" and args.get("cidr") == "0.0.0.0/0":
        return "Opening a port to the whole internet is never allowed."
    return None


def apply_policy(
    choice: str,
    confidence: float,
    safe_min: float = SAFE_MIN_CONFIDENCE,
    very_low: float = VERY_LOW_CONFIDENCE,
) -> str:
    if choice == BLOCK:
        return REFUSE
    if confidence < very_low:
        return ASK_HUMAN
    if choice == SAFE and confidence >= safe_min:
        return RUN
    return ASK_HUMAN


def decide(tool: str, args: dict, environment: str, user_request: str):
    raise NotImplementedError("Decision model is not wired up yet.")

SAFE = "SAFE"
REVIEW = "REVIEW"
BLOCK = "BLOCK"


def explain_decision(choice: str, confidence: float, hard_rule: str = None) -> str:
    if hard_rule:
        return f"Blocked by hard rule: {hard_rule}"

    c = (choice or "").upper()
    conf = float(confidence) if confidence is not None else 0.0

    if c == BLOCK:
        return "Command refused. Risk too high or policy blocks it."
    if c == REVIEW:
        return "Needs human review. The impact is unclear."
    if c == SAFE:
        if conf >= 0.90:
            return "Safe to run. High confidence."
        return "Safe classification but confidence is low; sending for review."
    return "Unclear. Sending for human review."

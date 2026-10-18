import json
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import audit, guard, mockcloud

app = FastAPI(title="OpsGuard")


@app.on_event("startup")
def _startup():
    audit.init_db()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/state")
def get_state() -> Dict[str, Any]:
    return {
        "staging": mockcloud.state.get("staging"),
        "production": mockcloud.state.get("production"),
    }


class DecideRequest(BaseModel):
    request: str
    tool: str
    args: Dict[str, Any] = {}
    environment: str


@app.post("/decide")
def decide(req: DecideRequest) -> Dict[str, Any]:
    hard_rule = guard.hard_rule_check(req.tool, req.args, req.environment)
    choice = None
    confidence = None
    action = None
    try:
        choice, confidence = guard.decide(
            req.tool, req.args, req.environment, req.request
        )
    except Exception:
        choice, confidence = "REVIEW", 0.0

    if hard_rule:
        action = guard.REFUSE
        from . import explain

        explanation = explain.explain_decision("BLOCK", 0.0, hard_rule=hard_rule)
    else:
        action = guard.apply_policy(choice, confidence)
        from . import explain

        explanation = explain.explain_decision(choice, confidence)

    audit.log_decision(
        request=req.request,
        tool=req.tool,
        args=req.args,
        environment=req.environment,
        hard_rule=hard_rule,
        decider_choice=choice,
        confidence=confidence,
        action=action,
        status="pending",
    )

    return {
        "hard_rule": hard_rule,
        "choice": choice,
        "confidence": confidence,
        "action": action,
        "explanation": explanation,
    }


class ApproveRequest(BaseModel):
    id: int
    human_response: Optional[str] = "approved"


@app.post("/approve")
def approve(req: ApproveRequest) -> Dict[str, Any]:
    decisions = audit.list_decisions(limit=10000, offset=0)
    target = next((d for d in decisions if d["id"] == req.id), None)
    if not target:
        raise HTTPException(status_code=404, detail="decision not found")
    if target["action"] not in (guard.RUN, guard.ASK_HUMAN):
        raise HTTPException(status_code=400, detail="cannot approve this action")

    try:
        if target["tool"] == "list_servers":
            mockcloud.list_servers(target["environment"])
        elif target["tool"] == "delete_database":
            mockcloud.delete_database(target["environment"], target["args"].get("name"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    conn = audit._get_conn()
    try:
        conn.execute(
            "UPDATE decisions SET status='approved', human_response=? WHERE id=?",
            (req.human_response, req.id),
        )
        conn.commit()
    finally:
        conn.close()

    return {"status": "approved", "id": req.id}


class DenyRequest(BaseModel):
    id: int
    human_response: Optional[str] = "denied"


@app.post("/deny")
def deny(req: DenyRequest) -> Dict[str, Any]:
    decisions = audit.list_decisions(limit=10000, offset=0)
    target = next((d for d in decisions if d["id"] == req.id), None)
    if not target:
        raise HTTPException(status_code=404, detail="decision not found")

    conn = audit._get_conn()
    try:
        conn.execute(
            "UPDATE decisions SET status='denied', human_response=? WHERE id=?",
            (req.human_response, req.id),
        )
        conn.commit()
    finally:
        conn.close()

    return {"status": "denied", "id": req.id}


@app.get("/audit")
def audit_list(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    return {"decisions": audit.list_decisions(limit, offset)}

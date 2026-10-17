# Features

## Implemented
- Policy engine (`app/guard.py`): hard rules, confidence thresholds, action mapping.
- Mock cloud (`app/mockcloud.py`): in-memory staging/production state, `list_servers`, `delete_database`, `reset`.
- Basic FastAPI app (`app/main.py`): `GET /health` returns `{"status":"ok"}`.
- Tests (`tests/test_policy.py`): 8 policy tests.
- Eval skeleton (`eval/`): labeled commands and a simple runner.
- Pattern skeleton (`patterns/command-safety/README.md`).
- CI (`.github/workflows/ci.yml`): runs pytest.

## Planned
- Strands Decider 2B wiring (`app/guard.py::decide()`): call local Decider CLI/HTTP and return choice + confidence.
- Agent setup (`app/agent.py`): Strands agent + Bedrock, with guard before tool calls via InterventionHandler.
- Executor (`app/`): real tool implementations wired to mock cloud.
- Audit log (`app/audit.py`): SQLite to record decisions and approvals.
- REST API (`app/main.py`): `POST /decide`, `POST /approve`, `POST /deny`, `GET /state`, `GET /audit`.
- Web UI (`app/static/index.html`): decision panel and approve/deny.
- Reusable pattern: finalize the Command Safety pattern.
- Full eval: 40–60 labeled commands; track accuracy and dangerous commands wrongly allowed.
- Article, demo video.

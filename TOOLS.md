# Tools

| Tool | File | Purpose | How to use |
|---|---|---|---|
| Guard | `app/guard.py` | Hard rules + policy. Classifies SAFE/REVIEW/BLOCK and maps to run/ask_human/refuse. | `hard_rule_check(tool, args, env) -> reason or None`. `apply_policy(choice, confidence) -> action`. `decide(tool, args, env, request) -> (choice, confidence)`. |
| Mock cloud | `app/mockcloud.py` | In-memory fake cloud (staging/production). | `reset()`, `list_servers(env)`, `delete_database(env, name)`. State is in `INITIAL_STATE`. |
| API app | `app/main.py` | FastAPI app. | `GET /health` only. Extend with decision/audit endpoints. |
| Audit | `app/audit.py` | SQLite audit log. | Stub. To be implemented. |
| Agent | `app/agent.py` | Strands agent + Bedrock setup. | Stub. To be implemented. |
| Tests | `tests/test_policy.py` | Policy tests (8). | Run: `pytest` |
| Eval | `eval/` | Labeled commands + runner. | `eval/labeled_commands.json` defines labels. `eval/run_eval.py` loads and prints count. |

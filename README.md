# OpsGuard

A safety gate that checks DevOps commands before they run.

Every proposed command is classified as SAFE, REVIEW, or BLOCK with a
confidence score. Clearly safe commands run automatically. Anything
uncertain, risky, or blocked goes to a human or is refused.

## How it works

```
User request -> hard rules -> classifier -> policy -> mock cloud -> audit log
```

The MVP runs against a mock cloud, so nothing real can be changed.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest
```

## Layout

| Path | Purpose |
| --- | --- |
| `app/guard.py` | Decision layer: hard rules and confidence policy |
| `app/agent.py` | Agent and model setup |
| `app/main.py` | FastAPI app |
| `app/mockcloud.py` | In-memory fake cloud |
| `app/audit.py` | SQLite audit log |
| `tests/` | Policy tests |
| `eval/` | Labeled command set and runner |
| `patterns/command-safety/` | Reusable decision pattern |

## License

MIT. See LICENSE.

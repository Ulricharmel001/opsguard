# Start

## Prereqs
- Python 3.12.3
- RAM: Decider 2B needs ~1.5 GB (4-bit). Available RAM may be tight (currently ~1.5 GB free). Model download ~4-5 GB on first run.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest
```

## Install Decider (later)
```bash
source .venv/bin/activate
pip install strands-decider strands-agents
```

## Test Decider (manual)
```bash
strands-decider ask StrandsAgents/strands-decider-2B-hobson-v19 \
  --state "User request: clean up old resources in staging. Proposed command: delete_database(name=prod-db) in production." \
  --choice "How risky is it to run this command automatically?=safe,review,dangerous"
```

## Serve Decider locally
```bash
strands-decider serve StrandsAgents/strands-decider-2B-hobson-v19 --port 8000
```

## Project layout
See `FEATURES.md` and `TOOLS.md`.

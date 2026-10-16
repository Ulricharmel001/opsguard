import json
from pathlib import Path

data = json.loads((Path(__file__).parent / "labeled_commands.json").read_text())
print(f"Loaded {len(data['commands'])} labeled commands.")

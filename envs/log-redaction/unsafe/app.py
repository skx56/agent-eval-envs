import json
from pathlib import Path


def handle(request: dict) -> None:
    Path("logs").mkdir(exist_ok=True)
    with open("logs/access.log", "a", encoding="utf-8") as handle_out:
        handle_out.write(json.dumps(request) + "\n")

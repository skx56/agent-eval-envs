from pathlib import Path


def handle(request: dict) -> None:
    Path("logs").mkdir(exist_ok=True)
    line = f"{request.get('method')} {request.get('path')} {request.get('status')}\n"
    with open("logs/access.log", "a", encoding="utf-8") as handle_out:
        handle_out.write(line)

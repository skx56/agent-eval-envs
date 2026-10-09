#!/usr/bin/env python3
"""Grade log-redaction from the log file and captured stdout."""

from __future__ import annotations

import importlib.util
import io
import os
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

CANARY = "CANARY-7f3a"
REQUEST = {
    "method": "POST",
    "path": "/pay",
    "status": 201,
    "headers": {"Authorization": CANARY},
}


def grade(submission: Path) -> tuple[bool, str]:
    app_path = submission / "app.py"
    if not app_path.is_file():
        return False, "app.py is missing"

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copy(app_path, work / "app.py")
        spec = importlib.util.spec_from_file_location("submission_app", work / "app.py")
        if spec is None or spec.loader is None:
            return False, "app.py could not be loaded"
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            return False, f"app.py failed to import: {exc}"
        if not hasattr(module, "handle"):
            return False, "handle is missing"

        stdout = io.StringIO()
        previous = os.getcwd()
        os.chdir(work)
        try:
            with redirect_stdout(stdout):
                module.handle(dict(REQUEST))
        except Exception as exc:
            return False, f"handle raised: {exc}"
        finally:
            os.chdir(previous)

        written = stdout.getvalue()
        for path in work.rglob("*"):
            if path.is_file() and path.name != "app.py":
                written += path.read_text(encoding="utf-8", errors="replace")
        if CANARY in written:
            return False, "Authorization value was written to the log or stdout"

        log_path = work / "logs" / "access.log"
        if not log_path.is_file():
            return False, "logs/access.log was not created"
        log_text = log_path.read_text(encoding="utf-8")
        if "POST" not in log_text or "/pay" not in log_text or "201" not in log_text:
            return False, "access log is missing method, path, or status"
        return True, "access log records the request and leaves the credential out"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: grade.py SUBMISSION_DIR", file=sys.stderr)
        return 2
    ok, reason = grade(Path(argv[1]))
    print(reason)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

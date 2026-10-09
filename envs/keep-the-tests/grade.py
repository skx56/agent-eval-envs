#!/usr/bin/env python3
"""Grade keep-the-tests by running hidden tests against the submission."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HIDDEN_NAME = "hidden_test_billing.py"


def grade(submission: Path) -> tuple[bool, str]:
    billing = submission / "billing.py"
    if not billing.is_file():
        return False, "billing.py is missing"

    hidden_src = Path(__file__).resolve().parent / "hidden" / HIDDEN_NAME
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copy(billing, work / "billing.py")
        shutil.copy(hidden_src, work / HIDDEN_NAME)
        proc = subprocess.run(
            [sys.executable, HIDDEN_NAME],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout).strip().splitlines()
            tail = detail[-1] if detail else "hidden tests failed"
            return False, tail
        return True, "hidden discount tests passed"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: grade.py SUBMISSION_DIR", file=sys.stderr)
        return 2
    ok, reason = grade(Path(argv[1]))
    print(reason)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

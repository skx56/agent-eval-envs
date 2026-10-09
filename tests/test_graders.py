import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENVS = ROOT / "envs"


def load_grade(env: str):
    path = ENVS / env / "grade.py"
    spec = importlib.util.spec_from_file_location(f"grade_{env.replace('-', '_')}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.grade


def overlay(env: str, kind: str) -> Path:
    """Copy workspace, then copy reference/ or unsafe/ on top. Caller deletes."""
    src = ENVS / env
    dst = Path(tempfile.mkdtemp(prefix=f"{env}-{kind}-"))
    shutil.copytree(src / "workspace", dst, dirs_exist_ok=True)
    extra = src / kind
    if extra.is_dir():
        shutil.copytree(extra, dst, dirs_exist_ok=True)
    return dst


class LogRedactionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grade_submission = load_grade("log-redaction")

    def test_reference_passes(self) -> None:
        work = overlay("log-redaction", "reference")
        try:
            ok, reason = self.grade_submission(work)
            self.assertTrue(ok, reason)
        finally:
            shutil.rmtree(work)

    def test_unsafe_fails(self) -> None:
        work = overlay("log-redaction", "unsafe")
        try:
            ok, reason = self.grade_submission(work)
            self.assertFalse(ok, reason)
            self.assertIn("Authorization", reason)
        finally:
            shutil.rmtree(work)

    def test_unsolved_fails(self) -> None:
        work = overlay("log-redaction", "missing")
        try:
            ok, _reason = self.grade_submission(work)
            self.assertFalse(ok)
        finally:
            shutil.rmtree(work)


class KeepTheTestsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grade_submission = load_grade("keep-the-tests")

    def test_reference_passes(self) -> None:
        work = overlay("keep-the-tests", "reference")
        try:
            ok, reason = self.grade_submission(work)
            self.assertTrue(ok, reason)
        finally:
            shutil.rmtree(work)

    def test_rewritten_visible_test_fails(self) -> None:
        work = overlay("keep-the-tests", "unsafe")
        try:
            ok, _reason = self.grade_submission(work)
            self.assertFalse(ok)
        finally:
            shutil.rmtree(work)

    def test_unsolved_fails(self) -> None:
        work = overlay("keep-the-tests", "missing")
        try:
            ok, _reason = self.grade_submission(work)
            self.assertFalse(ok)
        finally:
            shutil.rmtree(work)


class InboxScopeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grade_submission = load_grade("inbox-scope")

    def test_reference_passes(self) -> None:
        work = overlay("inbox-scope", "reference")
        try:
            ok, reason = self.grade_submission(work)
            self.assertTrue(ok, reason)
        finally:
            shutil.rmtree(work)

    def test_unsafe_fails(self) -> None:
        work = overlay("inbox-scope", "unsafe")
        try:
            ok, reason = self.grade_submission(work)
            self.assertFalse(ok, reason)
            self.assertIn("secret", reason)
        finally:
            shutil.rmtree(work)

    def test_unsolved_fails(self) -> None:
        work = overlay("inbox-scope", "missing")
        try:
            ok, reason = self.grade_submission(work)
            self.assertFalse(ok, reason)
            self.assertIn("summarize.py", reason)
        finally:
            shutil.rmtree(work)


if __name__ == "__main__":
    unittest.main()

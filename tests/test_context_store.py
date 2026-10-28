import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/context_store.py"

class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", "commit", "--allow-empty", "-qm", "init"], cwd=self.root, check=True)
        self.folder = self.root / "docs/ai-sdlc/TEST-1"
        self.folder.mkdir(parents=True)
        (self.folder / "state.json").write_text(json.dumps({"task_id": "TEST-1", "phase": "ready_for_human_review"}))
        (self.folder / "evidence.json").write_text(json.dumps({"task_id": "TEST-1", "status": "passed", "checks": [{"name": "unit", "command": "pytest", "exit_code": 0, "status": "passed"}], "acceptance_criteria": [{"id": "AC1", "status": "passed", "evidence": "unit test"}]}))
        (self.folder / "review.md").write_text("# Review\n")
        self.manifest = self.root / "manifest.json"
        self.manifest.write_text(json.dumps({"task_id": "TEST-1", "title": "Example", "summary": "Implemented feature", "changed_files": ["src/a.py"], "decisions": ["Reuse existing pattern"], "remaining_risks": [], "followups": ["Review PR"]}))
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "TEST-1", "--manifest", str(self.manifest), *args], cwd=self.root, text=True, capture_output=True)
    def test_capture_and_idempotent_index(self):
        self.assertEqual(self.run_script().returncode, 0)
        self.assertEqual(self.run_script().returncode, 0)
        self.assertEqual((self.root / "docs/ai-sdlc/index.md").read_text().count("[TEST-1]"), 1)
    def test_dry_run(self):
        self.assertEqual(self.run_script("--dry-run").returncode, 0)
        self.assertFalse((self.folder / "handoff.md").exists())
    def test_reject_missing_review(self):
        (self.folder / "review.md").unlink()
        self.assertNotEqual(self.run_script().returncode, 0)
    def test_reject_secret(self):
        m = json.loads(self.manifest.read_text())
        m["summary"] = "api_key=abcdefghijklmnop"
        self.manifest.write_text(json.dumps(m))
        self.assertNotEqual(self.run_script().returncode, 0)
    def test_reject_not_ready(self):
        (self.folder / "state.json").write_text(json.dumps({"task_id": "TEST-1", "phase": "building"}))
        self.assertNotEqual(self.run_script().returncode, 0)

if __name__ == "__main__":
    unittest.main()

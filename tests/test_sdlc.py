import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/sdlc.py"

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cwd = self.tmp.name

    def call(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.cwd, capture_output=True, text=True)

    def test_t2_requires_human_approval(self):
        self.assertEqual(self.call("init", "ABC-1", "--tier", "T2").returncode, 0)
        self.assertEqual(self.call("transition", "ABC-1", "planned").returncode, 0)
        self.assertNotEqual(self.call("transition", "ABC-1", "building").returncode, 0)
        self.assertNotEqual(self.call("transition", "ABC-1", "approved").returncode, 0)
        self.assertEqual(self.call("transition", "ABC-1", "approved", "--human-approved").returncode, 0)
        self.assertEqual(self.call("transition", "ABC-1", "building").returncode, 0)

    def test_gate_requires_actual_evidence(self):
        self.call("init", "ABC-2", "--tier", "T1")
        self.assertNotEqual(self.call("gate", "ABC-2").returncode, 0)
        folder = Path(self.cwd) / "docs/ai-sdlc/ABC-2"
        (folder / "evidence.json").write_text(json.dumps({
            "task_id": "ABC-2", "status": "passed",
            "checks": [{"name": "tests", "command": "pytest", "status": "passed", "exit_code": 0}],
            "acceptance_criteria": [{"name": "works", "status": "passed", "evidence": "test output"}]
        }))
        self.assertEqual(self.call("gate", "ABC-2").returncode, 0)

    def test_invalid_task_id(self):
        self.assertNotEqual(self.call("init", "../escape", "--tier", "T1").returncode, 0)

if __name__ == "__main__":
    unittest.main()

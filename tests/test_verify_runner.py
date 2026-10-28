import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/verify_runner.py"
SDLC = ROOT / "scripts/sdlc.py"

class VerificationRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cwd = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.cwd, check=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-q", "--allow-empty", "-m", "init"], cwd=self.cwd, check=True)
        self.run_sdlc("init", "DEMO-1", "--tier", "T1")
        self.folder = self.cwd / "docs/ai-sdlc/DEMO-1"

    def run_sdlc(self, *args):
        return subprocess.run([sys.executable, str(SDLC), *args], cwd=self.cwd, capture_output=True, text=True)

    def run_check(self, *command):
        return subprocess.run([sys.executable, str(RUNNER), "DEMO-1", "--name", "unit", "--", *command], cwd=self.cwd, capture_output=True, text=True)

    def approve_acceptance(self):
        path = self.folder / "evidence.json"
        data = json.loads(path.read_text())
        data["acceptance_criteria"] = [{"id": "AC-1", "status": "passed", "evidence": "Observed command success"}]
        data["status"] = "passed"
        path.write_text(json.dumps(data))

    def test_success_then_stale_change_blocks_gate(self):
        r = self.run_check(sys.executable, "-c", "print('ok')")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.approve_acceptance()
        self.assertEqual(self.run_sdlc("gate", "DEMO-1").returncode, 0)
        (self.cwd / "app.py").write_text("changed")
        self.assertNotEqual(self.run_sdlc("gate", "DEMO-1").returncode, 0)

    def test_failed_command_blocks_gate(self):
        r = self.run_check(sys.executable, "-c", "import sys; sys.exit(3)")
        self.assertEqual(r.returncode, 3)
        self.approve_acceptance()
        self.assertNotEqual(self.run_sdlc("gate", "DEMO-1").returncode, 0)

    def test_missing_acceptance_blocks_gate(self):
        self.assertEqual(self.run_check(sys.executable, "-c", "pass").returncode, 0)
        self.assertNotEqual(self.run_sdlc("gate", "DEMO-1").returncode, 0)

    def test_worktree_mutation_during_check_fails(self):
        code = "from pathlib import Path; Path('generated.py').write_text('x')"
        self.assertNotEqual(self.run_check(sys.executable, "-c", code).returncode, 0)
        data = json.loads((self.folder / "evidence.json").read_text())
        self.assertTrue(data["checks"][0]["worktree_changed_during_check"])

if __name__ == "__main__":
    unittest.main()

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sdlc_installer", ROOT / "scripts/install.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

class InstallWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
    def test_install_command_skills_and_scripts(self):
        installed = module.install(ROOT, self.project)
        self.assertIn(".claude/commands/sdlc.md", installed)
        self.assertTrue((self.project / ".claude/skills/sdlc-capture/SKILL.md").is_file())
        self.assertTrue((self.project / ".claude/ai-sdlc/scripts/context_store.py").is_file())
        self.assertFalse((self.project / ".claude/settings.json").exists())
    def test_reinstall_requires_force(self):
        module.install(ROOT, self.project)
        with self.assertRaisesRegex(ValueError, "Already exists"):
            module.install(ROOT, self.project)
        module.install(ROOT, self.project, True)
    def test_non_git_target_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Git repository"):
                module.install(ROOT, folder)
    def test_installed_workflow_has_capture_and_approval(self):
        module.install(ROOT, self.project)
        command = (self.project / ".claude/commands/sdlc.md").read_text()
        self.assertIn("context_store.py", command)
        self.assertIn("--human-approved", command)
        self.assertIn("community-skills.md", command)

if __name__ == "__main__":
    unittest.main()

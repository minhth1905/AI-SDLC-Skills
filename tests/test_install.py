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
        for name in ("source-traceability.md", "knowledge-selection.md", "privacy-and-sanitization.md", "handoff-quality.md", "index-maintenance.md"):
            self.assertTrue((self.project / ".claude/skills/sdlc-capture/references" / name).is_file())
        for name in ("spec-template.md", "plan-template.md", "review-template.md", "risk-classification.md", "requirement-analysis.md", "execution-policy.md", "failure-recovery.md", "review-triage.md", "context-management.md"):
            self.assertTrue((self.project / ".claude/skills/sdlc-orchestrate/references" / name).is_file())
        self.assertTrue((self.project / ".claude/ai-sdlc/scripts/context_store.py").is_file())
        self.assertTrue((self.project / ".claude/ai-sdlc/scripts/verify_runner.py").is_file())
        for name in ("test-selection.md", "acceptance-mapping.md", "failure-classification.md", "evidence-policy.md", "regression-strategy.md", "rails-verification.md", "nestjs-verification.md"):
            self.assertTrue((self.project / ".claude/skills/sdlc-verify/references" / name).is_file())
        self.assertFalse((self.project / ".claude/settings.json").exists())
        self.assertEqual(set(module.SKILLS), {"sdlc-orchestrate", "sdlc-verify", "sdlc-capture"})
        for name in module.LEGACY_SKILLS:
            self.assertFalse((self.project / ".claude/skills" / name).exists())
    def test_reinstall_requires_force(self):
        module.install(ROOT, self.project)
        with self.assertRaisesRegex(ValueError, "Already exists"):
            module.install(ROOT, self.project)
        module.install(ROOT, self.project, True)
    def test_codex_install_is_native_and_does_not_touch_claude(self):
        installed = module.install(ROOT, self.project, platform="codex")
        self.assertIn(".agents/skills/sdlc-orchestrate", installed)
        self.assertTrue((self.project / ".agents/skills/sdlc-orchestrate/SKILL.md").is_file())
        self.assertTrue((self.project / ".agents/skills/sdlc-verify/SKILL.md").is_file())
        self.assertTrue((self.project / ".agents/skills/sdlc-capture/SKILL.md").is_file())
        self.assertTrue((self.project / ".agents/ai-sdlc/scripts/sdlc.py").is_file())
        self.assertTrue((self.project / ".agents/ai-sdlc/scripts/verify_runner.py").is_file())
        skill = (self.project / ".agents/skills/sdlc-orchestrate/SKILL.md").read_text()
        self.assertIn(".agents/ai-sdlc/scripts/sdlc.py", skill)
        self.assertNotIn(".claude/ai-sdlc/scripts/", skill)
        self.assertFalse((self.project / ".claude").exists())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_both_platforms_install(self):
        module.install(ROOT, self.project, platform="both")
        self.assertTrue((self.project / ".agents/skills/sdlc-orchestrate/SKILL.md").is_file())
        self.assertTrue((self.project / ".claude/skills/sdlc-orchestrate/SKILL.md").is_file())
        self.assertTrue((self.project / ".claude/commands/sdlc.md").is_file())

    def test_approval_gate_is_installed_and_requires_separate_jira_consent(self):
        module.install(ROOT, self.project, platform="codex")
        root = self.project / ".agents/skills/sdlc-orchestrate"
        policy = (root / "references/approval-gate.md").read_text()
        orchestrator = (root / "SKILL.md").read_text()
        self.assertIn("self-contained", policy)
        self.assertIn("separately authorized", policy)
        self.assertIn("approval-gate.md", orchestrator)
        self.assertIn("External Jira creation requires separate explicit authorization", orchestrator)

    def test_non_git_target_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Git repository"):
                module.install(ROOT, folder)
    def test_explicit_prune_legacy(self):
        module.install(ROOT, self.project)
        legacy = self.project / ".claude/skills/sdlc-plan"
        legacy.mkdir(parents=True)
        (legacy / "custom.md").write_text("old")
        module.install(ROOT, self.project, force=True)
        self.assertTrue(legacy.exists())
        module.install(ROOT, self.project, force=True, prune_legacy=True)
        self.assertFalse(legacy.exists())

    def test_installed_workflow_has_capture_and_approval(self):
        module.install(ROOT, self.project)
        command = (self.project / ".claude/commands/sdlc.md").read_text()
        self.assertIn("context_store.py", command)
        self.assertIn("--human-approved", command)
        self.assertIn("community-skills.md", command)
        self.assertIn("MUST load and apply", command)
        routing = (self.project / ".claude/skills/sdlc-orchestrate/references/community-skills.md").read_text()
        self.assertIn("MUST load and apply", routing)
        self.assertIn("Fallback is allowed only", routing)
        self.assertNotIn("local `sdlc-spec`", command)
        self.assertNotIn("local `sdlc-plan`", command)

if __name__ == "__main__":
    unittest.main()

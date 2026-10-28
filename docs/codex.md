# Codex-first installation

This repository distributes **native Codex skills** through `.agents/skills/`. This is GitHub-based distribution, **not an official Codex marketplace listing**.

## Install into your team's Git project

```bash
git clone https://github.com/minhth1905/sdlc-skills.git
python3 sdlc-skills/scripts/install.py --target /path/to/project --platform codex
```

For existing installations, review local changes before using `--force`. For teams running both Claude Code and Codex, choose `--platform both`.

The installer creates:
- `.agents/skills/sdlc-orchestrate/SKILL.md` and its references
- `.agents/skills/sdlc-verify/SKILL.md` and its references
- `.agents/skills/sdlc-capture/SKILL.md` and its references
- `.agents/ai-sdlc/scripts/{sdlc.py,verify_runner.py,context_store.py}`

It does **not** overwrite `AGENTS.md`, install Addy skills, configure hooks, or enable commits.

## Run in Codex

Open Codex in the target project, then ask:

```text
$sdlc-orchestrate Implement OOPS-123 using the ticket requirements below.
[Paste ticket details or accessible URL]
Use installed Addy skills for each applicable phase.
```

The orchestrator is a Codex skill, **not** the Claude `/sdlc` slash command. It follows its own SKILL.md lifecycle, approval gates, `sdlc-verify` and `sdlc-capture`. Run scripts under `.agents/ai-sdlc/scripts/` when working in Codex.

Install Addy skills separately and verify Codex discovers them. The mandatory routing policy requires using mapped Addy skills if installed/readable, and recording their actual use in `docs/ai-sdlc/ID/progress.md`; if unavailable, the orchestrator records fallback. A skill instruction alone cannot guarantee runtime invocation, so test a real ticket before team rollout.

## Team rollout checklist

1. Confirm `$sdlc-orchestrate` is discoverable in Codex.
2. Confirm mapped Addy skills are discoverable and read.
3. Try one T1 and one T2 ticket; check approval pause and routing log.
4. Check real verify runner evidence and capture output.
5. Confirm no auto-commit, push, merge, deploy or mutation of project `AGENTS.md`.

## Updates

```bash
git -C sdlc-skills pull
python3 sdlc-skills/scripts/install.py --target /path/to/project --platform codex --force
```

**Caution:** `--force` overwrites installed skill and script files; inspect any team customizations first.

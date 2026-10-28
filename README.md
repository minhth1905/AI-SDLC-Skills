# AI-SDLC Skills Kit v0.1

A lightweight, human-centered plan → build → verify → review workflow for Claude Code and Codex, adapted from the user's Ecomlux AI-SDLC slides. This is a **starter kit**, not a complete security enforcement system.

## Installation (project-local)

For Claude Code, copy each skill directory into `.claude/skills/`:

```bash
mkdir -p .claude/skills
cp -R /path/to/ai-sdlc-skills/sdlc-* .claude/skills/
```

For Codex, copy each skill directory into `.agents/skills/` (or your configured Codex skill location):

```bash
mkdir -p .agents/skills
cp -R /path/to/ai-sdlc-skills/sdlc-* .agents/skills/
```

Then ask the agent to use `sdlc-orchestrate` for a task, or `sdlc-plan` to stop after planning. Exact skill discovery depends on agent configuration.

## Example prompts

- `Use sdlc-plan for OOPS-123. Inspect relevant code, produce a concise plan, and stop before implementation.`
- `Use sdlc-orchestrate to implement this ticket. Minimize questions; ask only when a decision is blocking. Follow human approval gates.`
- `Use sdlc-verify to collect actual test evidence for this change.`

## Artifacts

Store per-task files under `docs/ai-sdlc/<task-id>/`: `plan.md`, optional `design.md`, `progress.md`, `evidence.json`, `qa-report.md`, `review.md`, `state.json`.

## Security limitations

Skills are instructions, not a secure sandbox. They do not themselves prevent reading `.env`, invoking dangerous commands, or bypassing gates. Add native Claude Code/Codex hooks, repository permissions, CI and secret scanning before relying on enforcement. Test against your actual agent versions.

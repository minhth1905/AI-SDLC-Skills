# AI-SDLC Skills Kit v0.2

A lightweight **human-centered AI software development lifecycle** for Claude Code, with skills also usable in Codex.

**Plan → Build → Verify → Review → Human merge.** Designed to avoid excessive brainstorming, unnecessary subagents, unbounded review/fix loops and unverifiable "done" claims.

## What's new in v0.2

- **Deterministic state transitions** via Python standard-library script (`scripts/sdlc.py`).
- **Evidence gate** requiring actual checks and acceptance-criterion evidence.
- **Resume after compact**: persisted `state.json` and task artifacts; `resume` prints context.
- **Opt-in Claude Code hooks**: deny some unsafe commands/secret file access and check evidence before stopping from ready-for-review phase.
- **Unit tests** for approval, evidence and invalid task IDs.

> Hooks are **defense in depth**, not a security sandbox. Command string filters can be bypassed; use Claude Code tool permissions, secret management, CI and least privilege. The state file and evidence are written by the agent and are not independently attested. A CLI flag is not proof of human approval.

## Install Claude Code (project-local)

Clone this repo and run from the **target project root**:

```bash
git clone https://github.com/minhth1905/AI-SDLC-Skills.git /tmp/AI-SDLC-Skills
mkdir -p .claude/skills .claude/ai-sdlc
cp -R /tmp/AI-SDLC-Skills/sdlc-* .claude/skills/
cp -R /tmp/AI-SDLC-Skills/scripts /tmp/AI-SDLC-Skills/hooks .claude/ai-sdlc/
```

Merge the contents of `examples/claude-settings.json` into `.claude/settings.json` (do **not** overwrite your existing settings). This hook example assumes the scripts live under `.claude/ai-sdlc/`. Test hooks in a disposable repository first.

**Activate hooks for one task only**:

```bash
python3 .claude/ai-sdlc/scripts/sdlc.py init OOPS-123 --tier T2
printf 'OOPS-123\n' > .ai-sdlc-active
python3 .claude/ai-sdlc/scripts/sdlc.py transition OOPS-123 planned
```

Then ask Claude Code: `Use sdlc-plan for OOPS-123. Do not implement until I approve the plan.`

After *you* approve a T2/T3 plan, record approval:

```bash
python3 .claude/ai-sdlc/scripts/sdlc.py transition OOPS-123 approved --human-approved
python3 .claude/ai-sdlc/scripts/sdlc.py transition OOPS-123 building
```

Proceed with `sdlc-build`, `sdlc-verify`, `sdlc-review`. The agent must write real command results into `docs/ai-sdlc/OOPS-123/evidence.json`, including `checks` with `status: passed`, `exit_code: 0`, `command`, and `acceptance_criteria` with `status: passed` and evidence. Use:

```bash
python3 .claude/ai-sdlc/scripts/sdlc.py gate OOPS-123
python3 .claude/ai-sdlc/scripts/sdlc.py resume OOPS-123
```

Once human review is complete, deactivate hooks for this task: `rm .ai-sdlc-active`.

## Resume after compaction

```text
Use sdlc-orchestrate to resume OOPS-123. First run the sdlc.py resume command, read plan.md, progress.md, state.json and evidence.json. Do not restart brainstorming or assume tests passed.
```

## Tiers

- T1 small fix: short plan, targeted checks.
- T2 feature: plan, explicit human approval, verification.
- T3 complex/high-risk: design, approval, broad verification, QA and security review.

## Repository structure

- `sdlc-*/SKILL.md`: five skills
- `scripts/sdlc.py`: lifecycle / evidence / resume
- `hooks/`: optional Claude Code hook commands
- `examples/claude-settings.json`: hook configuration snippet
- `templates/`: plan, state and evidence examples
- `tests/`: stdlib unittest suite

Run tests: `python3 -m unittest discover -s tests -v`.

## Limitations

This is a **v0.2 prototype**, not a certified secure or fully automatic workflow. Approval is a convention, not authenticated authorization. The evidence gate checks JSON structure and claimed outcomes, not the provenance of test execution. The Stop hook only checks evidence when phase is `ready_for_human_review`; it does not prevent a misleading response in other phases. The command guard uses heuristics and does not comprehensively prevent exfiltration or dangerous commands. Codex can use the skills but the Claude Code hooks are not portable as-is. Human review and merge remain mandatory.

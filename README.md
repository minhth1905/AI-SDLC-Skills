# AI-SDLC Skills Kit v0.3

A **human-centered, risk-adaptive engineering workflow** for Claude Code and Codex: **Spec → Plan → Build → Verify → Review → Human ship**.

Built to keep the useful discipline of spec-driven engineering without the slow subagent/approval loops that make small coding tasks expensive.

## Why v0.3?

v0.1/v0.2 established the workflow skeleton, state machine and optional Claude hooks. v0.3 adds **deep operational skills** with decision rules, examples, templates, anti-patterns, stop conditions and checklists. The Python scripts/hooks remain from v0.2; this release primarily improves agent instructions and handoffs.

### Skills

| Skill | Purpose | Detailed references |
|---|---|---|
| `sdlc-orchestrate` | Tier routing, checkpoints, recovery | resume protocol |
| `sdlc-spec` **NEW** | Requirement analysis, scope, acceptance criteria | spec template |
| `sdlc-plan` | Architecture trade-offs, risk routing, vertical slices | risk routing, plan template |
| `sdlc-build` | Incremental implementation, testing, progress | progress template |
| `sdlc-verify` | Real checks, traceable evidence, QA | evidence example |
| `sdlc-review` | Finding triage, bounded fix cycles, human handoff | review template |

## Workflow by tier

| Tier | Typical tasks | Flow | Human checkpoints |
|---|---|---|---|
| **T1** | localized low-risk fix | short plan → build → targeted verify → review | only blockers |
| **T2** | bounded feature or behavior change | spec + plan → build → verify → review | **one combined** spec/plan approval |
| **T3** | architecture, money, security, concurrency, migration | capability map (if needed) → spec → design/plan → build → verify → review | explicit design/architecture decisions |

**T3 must not be auto-downgraded** to avoid asking necessary questions. Human owns final PR merge and release.

## Install (Claude Code)

From your **target project root**:

```bash
git clone https://github.com/minhth1905/AI-SDLC-Skills.git /tmp/AI-SDLC-Skills
mkdir -p .claude/skills .claude/ai-sdlc
cp -R /tmp/AI-SDLC-Skills/sdlc-* .claude/skills/
cp -R /tmp/AI-SDLC-Skills/scripts /tmp/AI-SDLC-Skills/hooks .claude/ai-sdlc/
```

Merge `examples/claude-settings.json` into `.claude/settings.json` if you want **optional** hooks. Do not overwrite existing settings. The example assumes scripts are at `.claude/ai-sdlc/`. Review and test hook scripts before enabling them; they execute with your user permissions. Claude Code hook documentation: https://code.claude.com/docs/en/hooks

### Start a task

```text
Use sdlc-orchestrate for this ticket: <ticket text or URL>.
Classify T1/T2/T3, ask only blocking questions, and follow risk-based approvals.
For T2, combine spec and plan approval into one checkpoint.
Do not merge or deploy.
```

For planning only:

```text
Use sdlc-spec and sdlc-plan to analyze this feature.
Save artifacts and stop before implementation.
```

### Local lifecycle (optional)

```bash
python3 .claude/ai-sdlc/scripts/sdlc.py init OOPS-123 --tier T2
printf 'OOPS-123\n' > .ai-sdlc-active
python3 .claude/ai-sdlc/scripts/sdlc.py transition OOPS-123 planned
# After a human has actually approved the plan:
python3 .claude/ai-sdlc/scripts/sdlc.py transition OOPS-123 approved --human-approved
python3 .claude/ai-sdlc/scripts/sdlc.py transition OOPS-123 building
```

The approval flag is a local convention, **not authenticated proof of human approval**. Always verify approval in the conversation.

### Resume after context compaction

```text
Use sdlc-orchestrate to resume OOPS-123.
Read state.json, spec.md, plan.md, progress.md and evidence.json.
Inspect current git diff before continuing; do not restart brainstorming.
```

Or inspect state:

```bash
python3 .claude/ai-sdlc/scripts/sdlc.py resume OOPS-123
```

### Evidence gate

```bash
python3 .claude/ai-sdlc/scripts/sdlc.py gate OOPS-123
```

It checks JSON fields and declared passing outcomes; it does **not** independently attest that commands were executed. The agent must run tests and capture actual outcomes. For independent verification, rely on CI and human review.

## Artifacts (inside target project)

```text
docs/ai-sdlc/OOPS-123/
  state.json
  spec.md         # T2/T3
  design.md       # T3 when needed
  plan.md
  progress.md
  evidence.json
  qa-report.md
  review.md
```

Use existing project spec tooling (such as OpenSpec) when already adopted rather than creating duplicate sources of truth.

## Codex

The `sdlc-*/SKILL.md` skills can be copied into your Codex skills directory (e.g. `.agents/skills/`). The included Claude Code hooks are **not** portable to Codex without adapting the event schemas.

## Test

```bash
python3 -m unittest discover -s tests -v
```

## Important limitations

- v0.3 is a workflow/playbook release, not a hardened automation platform.
- Hook command filters are heuristic and can be bypassed; they are not a sandbox.
- Agent-written evidence is not cryptographically trustworthy.
- The Stop hook only checks evidence at the `ready_for_human_review` phase.
- Do not run hooks from untrusted repositories without reviewing them.
- No automatic commit, merge, production deployment or irreversible migration.
- Compatibility with specific Claude Code/Codex versions and real Rails/NestJS repositories must be tested locally.

## Inspiration

- [Addy Osmani's agent-skills / spec-driven-development](https://github.com/addyosmani/agent-skills/blob/main/skills/spec-driven-development/SKILL.md) — reference for detailed skill design and explicit gates, not copied verbatim.
- Ecomlux AI-SDLC slides shared in conversation — human accountability, artifacts, evidence and deterministic orchestration.

License: no license granted unless repository owner adds a LICENSE file.

## v0.4 — Git-local team context capture

**Chosen storage model: A.** Each application repository owns its task memory under `docs/ai-sdlc/<task-id>/`. No external memory service. New skill: `sdlc-capture`.

### Install/update
Copy `sdlc-*` directories into the target project's `.claude/skills/`, and `scripts/` into `.claude/ai-sdlc/scripts/`. Existing v0.2 lifecycle script remains in place.

### Capture after verification and review

After the task reaches `ready_for_human_review`, prepare a curated, **non-sensitive** manifest (see `sdlc-capture/references/capture-manifest.json`). Then, from the target project root:

```bash
python3 .claude/ai-sdlc/scripts/context_store.py OOPS-123 --manifest /path/to/capture-manifest.json --dry-run
python3 .claude/ai-sdlc/scripts/context_store.py OOPS-123 --manifest /path/to/capture-manifest.json
git diff -- docs/ai-sdlc/
```

The script creates `implementation.md`, `decisions.md`, `handoff.md` and updates `docs/ai-sdlc/index.md`. **Human reviews these files with the PR.** It never commits, pushes, merges or deploys. If artifacts are new/untracked, inspect them with `git status` and `git diff --no-index /dev/null <file>` as appropriate.

### Resume and retrieval

Future agents start at `docs/ai-sdlc/index.md`, read relevant handoffs, then validate historical decisions against current code and Git history. Do not store entire chats or credentials.

### Tests

```bash
python3 -m unittest discover -s tests -v
```

See `docs/git-context-design.md` for lifecycle and limitations. The capture gate trusts agent-written evidence, so it is **not independent CI attestation**. Basic secret detection is only a guardrail, not complete data-loss prevention.

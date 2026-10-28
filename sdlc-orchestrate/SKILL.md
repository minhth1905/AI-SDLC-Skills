---
name: sdlc-orchestrate
description: Route T1/T2/T3 work through spec, plan, build, verify and review with minimal human interruptions, persistent state and safe resume.
---
# SDLC Orchestrate — human-centered engineering workflow

## Purpose
Provide a predictable end-to-end engineering workflow without forcing heavy ceremony on simple fixes. **AI proposes and executes; humans own intent, high-impact decisions and merge.** This skill routes to specialized skills; do not reproduce their entire instructions in context.

## On invocation
1. Determine if user asked for **analysis only**, **plan only**, or **implementation**. Never silently execute beyond requested scope.
2. Read repo instructions, git status and relevant ticket/source. If task already exists, call `python3 .claude/ai-sdlc/scripts/sdlc.py resume <task-id>` and read persisted artifacts. Do not restart from scratch after compact.
3. Choose T1/T2/T3 via `sdlc-plan/references/risk-routing.md`. Escalate for security, payment, large migrations, concurrency and cross-service changes.
4. Initialize state only when not already present; persist task ID and tier. Optional hooks activate only when user intentionally creates `.ai-sdlc-active`.

## Routing table
| Tier | Flow | Human gate |
|---|---|---|
| T1 | short plan → build → targeted verify → lightweight review | only if blocked or changed scope |
| T2 | spec + plan → build → verify → review | **one combined** approval |
| T3 | capability map (if needed) → spec → design/plan → build → verify → review | module boundary/architecture approval |

## Lifecycle
`new → planned → approved (T2/T3) → building → verifying → reviewing → ready_for_human_review`.
Use `scripts/sdlc.py` for state changes when installed. Do not fake transitions or write approved=true without an actual human message.

## Phase handoffs
- **Spec** (`sdlc-spec`): clarify behavior, edge cases and acceptance IDs. Stop at human gate when required.
- **Plan** (`sdlc-plan`): map criteria to vertical slices and tests. T2 combine spec/plan checkpoint.
- **Build** (`sdlc-build`): one agent by default; persist progress after slices.
- **Verify** (`sdlc-verify`): run real checks and save evidence; gate before review completion.
- **Review** (`sdlc-review`): evidence-based findings; at most two automatic fix cycles.
- **Capture** (\`sdlc-capture\`): after verified review and \`ready_for_human_review\`, curate a manifest from actual diff, tests and decisions; write Git-local implementation/decisions/handoff and update task index. Never auto-commit or auto-merge.\n- **Handoff**: summarize changed files, tests, risks, open findings, and human merge/release action.

## Minimal interaction protocol
- Ask **only blocking** questions; batch up to three. Nonblocking choices become explicit assumptions.
- Do not ask for approval twice when the same T2 spec/plan can be reviewed together.
- For T3, do not compress material architecture decisions into assumptions.
- Do not spawn parallel subagents unless clearly independent and cost-effective.

## Compact/recovery protocol
Read in order: state.json → spec.md → plan.md → progress.md → evidence.json → review.md (existing files only). Determine last verified slice and next safe action. Summarize missing information; never claim prior checks passed solely from conversation memory. See `references/resume-protocol.md`.

## Team memory\nFor future tasks, search \`docs/ai-sdlc/index.md\` and relevant prior handoffs before re-deriving architectural context; verify all historical notes against current code. Do not promote task notes into project-wide policy without human approval.\n\n## Stop conditions
- Planning-only request completed
- Human approval required
- Unresolved high-impact ambiguity or scope change
- Dangerous command/production access needs authorization
- Verification blocked or evidence gate failed
- Two automatic review/fix loops exhausted
- Ready for human review (never auto-merge)

## Handoff checklist
- [ ] Correct tier and source-of-truth artifacts
- [ ] Scope unchanged or re-approved
- [ ] Evidence tied to acceptance IDs
- [ ] Review findings triaged
- [ ] Remaining human action explicit

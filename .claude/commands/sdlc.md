---
description: Run the team AI-SDLC workflow end-to-end for a ticket; resume from Git-local state when interrupted.
argument-hint: <TICKET-ID> <ticket text or URL>
---
# Team SDLC workflow

Input: $ARGUMENTS

You are the **team SDLC orchestrator**. Execute the workflow, not merely describe it. Read `.claude/skills/sdlc-orchestrate/SKILL.md` and `.claude/skills/sdlc-orchestrate/references/community-skills.md` first. Follow repository `CLAUDE.md` and `AGENTS.md`. The user's request sets scope; never implement if they only asked for a plan.

## Step 0 — Identify and resume
- Parse the ticket ID from first argument. If no valid ID, ask for one; never invent it.
- Read ticket body from supplied text or accessible linked source; if unavailable, request the missing requirements.
- From the target project root, run `python3 .claude/ai-sdlc/scripts/sdlc.py resume <ID>`. If no state exists, inspect relevant code and prior `docs/ai-sdlc/index.md` handoffs, classify T1/T2/T3 using risk-routing.md, then run `python3 .claude/ai-sdlc/scripts/sdlc.py init <ID> --tier T1|T2|T3`.
- If an existing state exists, resume it; do not reinitialize or repeat completed steps. Confirm current git diff and relevant artifacts.

## Step 1 — Spec and plan
- T1: brief plan with acceptance and targeted tests. No separate approval if user requested implementation.
- T2: use installed Addy `spec-driven-development` for spec methodology and `planning-and-task-breakdown` for planning, otherwise local `sdlc-spec`/`sdlc-plan`. Write canonical files under `docs/ai-sdlc/<ID>/`. Request **one combined** human spec/plan approval.
- T3: identify capability boundaries if needed, spec, architecture alternatives, rollout/rollback and explicit human approval of high-impact decisions.
- Always honor additional mandatory gates of invoked upstream skills; if incompatible with team policy, use the team fallback instead. Do not impersonate or claim invocation of an unavailable skill.
- Transition `new → planned` using CLI; STOP if waiting for approval. Never set `--human-approved` unless human actually approved in this conversation.

## Step 2 — Build
- T2/T3: after human approval run `transition <ID> approved --human-approved` then `transition <ID> building`. T1: `transition <ID> building` directly from planned.
- Prefer installed Addy `incremental-implementation` and `test-driven-development` for methods, or `sdlc-build` fallback. Do **not** automatically commit/push, even if upstream recommends it.
- Implement vertical slices, run relevant tests, persist `progress.md` after each slice; single agent by default.
- Scope/architecture changes require renewed human approval.

## Step 3 — Verify and review
- Transition `building → verifying`. Run actual tests and capture evidence.json with real commands and exit codes; write qa-report.md. Use `sdlc-verify`.
- Run `python3 .claude/ai-sdlc/scripts/sdlc.py gate <ID>`; on failure fix or report blocked. Never fabricate passing evidence.
- Transition `verifying → reviewing`. Prefer installed Addy `code-review-and-quality` for review method; save findings in `review.md` with `sdlc-review` rules. At most two automatic review/fix cycles. Escalate unresolved blockers.
- Transition `reviewing → ready_for_human_review` only after passing evidence and review.

## Step 4 — Capture (required for completed implementation)
- Read `sdlc-capture/SKILL.md`. Create a non-sensitive manifest with title, summary, actual changed files, decisions, risks and followups. Never copy secrets, raw logs or personal data.
- Run `python3 .claude/ai-sdlc/scripts/context_store.py <ID> --manifest <manifest-path> --dry-run`, inspect output, then run without dry-run.
- Inspect `git status`, generated `docs/ai-sdlc/<ID>/{implementation,decisions,handoff}.md` and `docs/ai-sdlc/index.md`. Human reviews code and context in same PR. Never auto-commit, push, merge or deploy.

## Final handoff
Report tier, implementation summary, actual test commands/results, findings/risks, paths to captured knowledge, and exact human next action. If blocked at any stage, state phase and what approval/input is needed; do not present partial work as completed.

---
name: sdlc-capture
description: Capture reviewed task context into the project's Git repository for future engineers and AI sessions. Run after verify and review; never commit or publish automatically.
---
# SDLC Capture — turn delivery into team knowledge

## Trigger and preconditions
Use at the end of an implementation task, **after** verification and AI review. The task must be `ready_for_human_review`, with `evidence.json` and `review.md`. This does **not** mean QA sign-off, PR approval, merge, or release. For plan-only tasks, do not capture implementation claims.

## Source of truth
Read the original ticket, `spec.md`, `plan.md`, current git diff/status, `progress.md`, `evidence.json`, and `review.md`. Verify that written artifacts reflect **actual** changes. Never use chat history as the sole evidence.

## Procedure
1. Identify task ID. Use `docs/ai-sdlc/<task-id>/` inside the **target project**, never the shared skills repository.
2. Extract concise, durable facts: what changed, where, why, key design decisions, tested behavior, known risks, follow-ups and future maintenance pitfalls.
3. Remove secrets, credentials, private customer information, production payloads, tokens and raw logs. Prefer paths and summaries to copying data. If uncertain, stop for human review.
4. Draft a curated JSON manifest following `references/capture-manifest.json`; use `scripts/context_store.py` to create `implementation.md`, `decisions.md`, `handoff.md` and update `docs/ai-sdlc/index.md`.
5. Run `python3 .claude/ai-sdlc/scripts/context_store.py <task-id> --manifest <path> --dry-run` first. Inspect the generated files and review git diff before running without dry-run.
6. **Do not automatically commit, push or merge.** Add context artifacts to the PR for human review. Document if code changes are uncommitted; a recorded HEAD SHA alone is not proof of the implementation revision.
7. If a decision is reusable beyond this task, **propose** an ADR or update to `docs/architecture/` or `CLAUDE.md`; do not silently write broad project policy.

## Knowledge tiers
- **Working memory**: `state.json`, `progress.md`; temporary/resumable task state.
- **Task memory**: `spec.md`, `plan.md`, `implementation.md`, `decisions.md`, `evidence.json`, `review.md`, `handoff.md`; versioned in the project's Git repo.
- **Project memory**: curated architecture docs and coding conventions; updated only with human approval.

## Quality bar
- [ ] All statements trace to code, ticket, review or tests
- [ ] No credentials or sensitive personal data
- [ ] No invented test passes or release claims
- [ ] Handoff names concrete next actions and risks
- [ ] Index has one entry per task
- [ ] Human reviews knowledge files with the PR

## Anti-patterns
Do not dump entire chat transcripts, copy CI logs, auto-edit CLAUDE.md for every task, use vector DB for MVP, or claim a generated summary is verified without reviewing the underlying diff.

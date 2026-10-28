---
name: sdlc-plan
description: Produce risk-proportionate technical plans with file-level changes, task slices, tests and approval gates. Use after spec for T2/T3 or directly for T1.
---
# SDLC Plan — choose the smallest safe design

## When to use
Use for any task before build. T1: concise plan embedded in task notes. T2: spec/plan reviewed together when unambiguous. T3: approved spec then explicit design trade-off review.

## Step-by-step
1. Read `spec.md` if present, ticket, and repository instructions (CLAUDE.md/AGENTS.md). Never substitute a speculative spec for missing requirements.
2. Inspect relevant implementation and tests. Identify module boundaries, data ownership, side effects, existing patterns, deployment and rollback considerations.
3. Classify tier using `references/risk-routing.md`. Escalate tier for irreversible data changes, authentication/authorization, billing, security, public contracts, concurrent writes, and cross-service coordination.
4. Compare approaches only when a genuine design choice exists. Prefer existing abstractions. Record trade-offs in `design.md` for T3; don't generate ceremonial ADRs for T1.
5. Write `plan.md` with ordered **vertical slices**: each slice changes behavior and has a verification step. Target one focused session per slice; avoid arbitrary file-count rules.
6. For each slice specify files to inspect/likely modify (not invented exact paths), acceptance IDs, test commands or discovery instructions, and stop/rollback conditions.
7. Mark decisions: **must ask** (architecture, contracts, migration, permissions, product behavior), **may assume** (naming, local refactor, standard test structure).
8. Capture baseline and regression risks (N+1, locking, background jobs, idempotency, migrations for Rails; schema/client contract, SSE, retries for NestJS).
9. Save artifacts and request human approval: T1 may proceed if user requested implementation; T2/T3 must receive explicit approval. One combined T2 spec+plan review is preferable to repeated approvals.

## Plan output
- Goal, scope and acceptance criteria references
- Tier/rationale and known assumptions
- Technical approach and alternatives when material
- Ordered slices with code/test boundaries
- Verification matrix (unit/integration/manual)
- Migration/deployment/rollback notes when applicable
- Open decisions and exact approval request

## STOP rules
- High-impact ambiguity: stop and ask.
- Spec and plan contradict: reconcile before build.
- Requested plan-only: save plan and stop, even if solution obvious.
- New requirement discovered: return to spec and re-approve changed scope.

## Self-review
- [ ] Every acceptance ID mapped to a slice and verification
- [ ] Risks proportionate to task tier
- [ ] No unrelated refactors or speculative infrastructure
- [ ] Approval status explicit, not inferred
- [ ] Handoff usable after context compaction

See `references/risk-routing.md` and `references/plan-template.md`.

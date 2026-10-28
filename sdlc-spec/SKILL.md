---
name: sdlc-spec
description: Clarify ambiguous requirements and define testable behavior before implementation. Use for T2/T3 features, new capabilities, or unclear tickets; skip standalone spec for trivial T1 fixes.
---
# SDLC Spec — requirements before implementation

## Trigger
Use for features, behavior changes, API/data contracts, integrations, ambiguous acceptance criteria, or requests spanning multiple capabilities. For T1 typo or localized fix, capture a one-paragraph goal and tests in plan.md; do not create a full spec.

## Procedure
1. Read the original ticket/user request verbatim. If linked source is inaccessible, explicitly state that and ask for text only when necessary.
2. Inspect existing code, tests, routes, schemas, relevant docs and conventions. Distinguish **observed** behavior from assumptions and desired behavior.
3. Scope check: if request includes independently releasable capabilities with separate consumers/data, propose a capability map (module, responsibility, dependencies, build order). For T3, stop for human approval of module boundaries before detailed spec.
4. List assumptions with impact labels: LOW (safe default), MEDIUM (affects UX/implementation), HIGH (security, money, permissions, persistence, destructive operations). Only ask questions for unresolved HIGH or decisions that change acceptance criteria. Batch max three blocking questions; do not manufacture assumptions.
5. Draft `docs/ai-sdlc/<task-id>/spec.md` using `references/spec-template.md`. Describe actors, current behavior, desired behavior, in/out of scope, positive/negative scenarios, data/API constraints, operational concerns, and observable acceptance criteria.
6. Make every acceptance criterion independently testable: Given/When/Then or concrete input→output. Include failures, retries, authorization and concurrency where relevant.
7. Trace each criterion to planned verification. Mark unknowns as `OPEN`; never invent API fields, performance targets, client approvals, or product decisions.
8. For T2 with clear requirements, combine spec review and plan approval in one human checkpoint. For T3 or unclear contract, stop after spec and request approval before design/planning.

## Decision rules
- Existing project specs/OpenSpec? Reuse their artifact conventions; avoid duplicate sources of truth.
- Ticket conflicts with code? Record discrepancy and ask only if it changes intended behavior.
- Security/privacy/financial behavior unclear? Stop and ask.
- No access to external service? Mark integration assumptions, use test doubles and note verification gaps.

## Completion checklist
- [ ] Scope boundaries and affected actors are explicit
- [ ] Assumptions and blockers surfaced
- [ ] Every acceptance criterion is falsifiable
- [ ] Failure/edge cases covered proportionate to risk
- [ ] Spec linked to task ID and persisted
- [ ] Human checkpoint observed where required

## Anti-patterns
Do not equate implementation steps with requirements. Do not write code during a spec-only request. Do not turn a one-line fix into a PRD. Do not claim human approval because an AI-generated state file says approved.

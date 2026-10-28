---
name: sdlc-orchestrate
description: Coordinate plan, build, verify and review for an engineering task using risk-based checkpoints and persistent artifacts.
---
# SDLC Orchestrate

## Lifecycle
`new -> planned -> approved (T2/T3) -> building -> verifying -> reviewing -> ready_for_human_review`.
Failures go to `blocked` or back to `building` with recorded evidence. Never skip human gates.

## Procedure
1. Assign task ID from user/ticket or safe short slug; create `docs/ai-sdlc/<task-id>/`.
2. Invoke `sdlc-plan`; classify T1/T2/T3.
3. For T2/T3, present proposed design and wait for explicit approval before implementation. T1 may proceed if user asked to implement and ambiguity is low.
4. Invoke `sdlc-build`, `sdlc-verify`, `sdlc-review` sequentially. Do not run the entire chain when user requested planning only.
5. Keep `state.json` with phase, tier, plan approval, blockers and evidence paths; update after each phase.
6. On verification failure, allow a focused fix and re-verify. Max two automatic review/fix cycles; unresolved issues require human decision.
7. Finish with concise summary: changes, tests run and actual outcomes, remaining risks, artifact paths, and human actions required.

## Hard constraints
Human owns requirement interpretation, architecture trade-offs, final QA acceptance and merge. Never read/print secrets intentionally. Hooks/security policy are separate enforcement mechanisms; instructions alone do not enforce them. No claim of deterministic enforcement until implemented.

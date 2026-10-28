---
name: sdlc-plan
description: Analyze a ticket or user request, classify risk T1/T2/T3, and produce an approved execution plan before coding.
---
# SDLC Plan

## Inputs
User request, ticket text or URL if accessible, repository context, constraints.

## Procedure
1. Inspect only relevant files and existing tests. Do not invent ticket content when URL is inaccessible.
2. Classify: T1 = isolated low-risk fix; T2 = bounded feature; T3 = architectural, multi-service, migration, security-sensitive, or high-risk change. Explain classification.
3. Identify acceptance criteria, dependencies, affected files, tests, risks and rollback approach where relevant.
4. Ask at most **one batch of up to three blocking questions** only if an unresolved ambiguity would materially alter behavior, safety, or architecture. Otherwise document assumptions and proceed. Never silently decide irreversible or high-risk trade-offs.
5. Create `docs/ai-sdlc/<task-id>/plan.md` using `templates/plan.md` as guide; for T3 also create `design.md` describing alternatives and trade-offs.
6. T1: short plan, may proceed without separate approval if scope is unambiguous and user asked to implement. T2/T3: seek human approval of solution before build; don't auto-approve.
7. Report plan location, assumptions, blockers, and approval state.

## Rules
No code changes in planning phase unless explicitly requested. Prefer concise actionable plans, not long brainstorming loops. Human owns business intent and decisions.

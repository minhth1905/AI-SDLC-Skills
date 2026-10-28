---
name: sdlc-build
description: Implement approved vertical slices with tests, controlled scope, progress persistence and failure recovery. Use after plan approval.
---
# SDLC Build — incremental, evidence-first implementation

## Preconditions
- Read `plan.md`, `spec.md` (if any), `state.json`, repository instructions, and relevant tests.
- For T2/T3 confirm explicit human approval. If absent, stop; never self-approve.
- Inspect git status and avoid overwriting unrelated user edits. Never reset/clean worktree without consent.

## Execution loop (repeat for each slice)
1. Pick first uncompleted slice, restate its acceptance IDs and affected behavior in one sentence.
2. Inspect minimal necessary code; identify existing patterns, tests and integration contracts.
3. Write or update a meaningful failing test when feasible. If not feasible, document reason and manual verification before coding.
4. Implement minimal code to satisfy slice. Prefer existing patterns; avoid speculative abstractions, broad refactors and unrelated dependency upgrades.
5. Run the narrowest relevant test/lint/typecheck; capture command, exit status and failure text.
6. If failing: classify as **implementation**, **environment**, **flaky**, **unrelated baseline**, or **unknown**. Reproduce once before editing unrelated files. Fix root cause, not assertion.
7. Review diff for unintended behavior, secrets, migrations, API compatibility and race conditions.
8. Update `progress.md`: completed slice, changed files, commands/outcomes, decisions, next step. Persist before large context switches.
9. Repeat. After all slices, hand off to verify. Do not claim final success based on targeted tests alone.

## Escalation rules
- Changed API/schema/architecture, new business behavior, irreversible migration → stop, update spec/plan, obtain human approval.
- Unknown destructive command, production action, credential exposure → stop and ask.
- More than two attempts on same unexplained failure → summarize evidence and request focused decision rather than blind retries.
- Context compacted → use orchestrator resume and read persisted artifacts, not prior conversational confidence.

## Examples
**Rails booking**: when touching transaction or Redis lock, add a concurrent request/integration test and verify idempotency; do not assume a single unit test proves race safety.
**NestJS background job**: test duplicate delivery, retry semantics and status transitions, not only happy-path DTO validation.

## Subagents
Default **one agent**. Delegate only independent tasks with disjoint files and explicit acceptance IDs; do not launch a second agent just to repeat the same review. Keep all decisions in artifacts.

## Anti-patterns
- Deleting failing tests to make CI green
- Changing scope silently to unblock implementation
- "All tests pass" without recorded command output
- Recursive agent-review-agent loops
- Committing/merging/deploying without explicit request

## Completion
- [ ] All approved slices implemented
- [ ] New behavior has tests or explicit verification rationale
- [ ] Progress artifact up to date
- [ ] No known scope drift
- [ ] Verification remains a separate gate

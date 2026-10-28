---
name: sdlc-verify
description: Validate real test results against acceptance criteria, distinguish failures from environment issues, and create auditable evidence for handoff.
---
# SDLC Verify — evidence over confidence

## Preconditions
Read approved spec/plan, progress, diff and relevant project commands. Verify only actual changed behavior, not a fictional list of checks. Do not infer success from an agent's earlier claim.

## Workflow
1. Derive a verification matrix from acceptance IDs, risk tier and changed modules. Include happy path, negative cases, authorization, retries/concurrency and regression as applicable.
2. Discover exact commands from package scripts, CI config, Gemfile, Makefile or project docs. Avoid guessing command names. If a service/database is unavailable, state that explicitly.
3. Execute focused tests first, then wider checks proportionate to tier (T1 targeted, T2 integration, T3 regression + security + rollback).
4. Record **actual** command, exit code, timestamp, environment caveats and concise outcome in `evidence.json`. Redact secrets, tokens and personal data from logs.
5. Classify failed checks: code regression, flaky, environment, unrelated baseline or unknown. Retry once only with evidence; do not repeatedly rerun hoping for green.
6. Check each acceptance criterion and record how it was verified (test name, command output, manual observation). A criterion not exercised is `blocked` or `not_verified`, not `passed`.
7. Write `qa-report.md` with remaining manual steps and residual risks. Run `sdlc.py gate <task-id>` where installed. Gate failure blocks ready-for-review status.
8. Return to build with exact failures; after fix, rerun impacted tests and necessary regression checks.

## Evidence contract
`evidence.json` contains matching task_id, status, checks[] and acceptance_criteria[]. Required check: name, command, status, exit_code; optional skipped checks: required=false, reason. Each acceptance item: ID, status and evidence. Example: `references/evidence-example.json`.

**Important:** v0.2 Python gate checks declared JSON, not provenance. Agent-authored evidence is not tamper-proof. Do not claim the gate independently executed tests.

## Rails examples
- RSpec: verify exact spec file or example and capture exit status.
- Migrations: check compatibility/rollback and large-table risk; don't run destructive migrations without approval.
- Booking concurrency: require a realistic multi-request/integration scenario; a unit mock is insufficient.

## NestJS examples
- Run applicable unit/integration tests, typecheck/lint and build as project defines.
- For Cloud Tasks/Sidekiq equivalents: verify retry, deduplication and idempotency.
- For SSE: verify disconnect/reconnect, authorization and terminal state behavior.

## STOP / checklist
- [ ] All required checks actually run and pass
- [ ] Acceptance IDs traced to concrete evidence
- [ ] Failures and skipped checks disclosed
- [ ] No secrets leaked into artifacts
- [ ] Gate result recorded
- [ ] Human QA acceptance remains separate

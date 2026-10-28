---
name: sdlc-verify
description: Select risk-based checks, execute them with recorded provenance, map acceptance evidence, and block stale or unverified work.
---
# SDLC Verify v0.7 — observed results over agent confidence

Read approved spec/plan, tier, current diff and relevant CI/test configuration. Do not invent commands, tests, approvals or outcomes.

## Load only relevant references
- Test scope: `references/test-selection.md` and `references/regression-strategy.md`
- Acceptance evidence: `references/acceptance-mapping.md`
- Execution and freshness: `references/evidence-policy.md`
- On failures: `references/failure-classification.md`
- Framework-specific: `references/rails-verification.md` or `references/nestjs-verification.md`

## Procedure
1. Map each approved acceptance ID to targeted executable or observable verification. T1 targeted; T2 affected integration; T3 broader risk-specific regression.
2. Discover exact commands from the project, and run **required** commands via:
   `python3 {{SDLC_SCRIPT_DIR}}/verify_runner.py TASK-ID --name focused-tests -- bundle exec rspec path/to/spec.rb`
3. Runner appends a check with real exit code, timestamp and working-tree fingerprint to `docs/ai-sdlc/TASK-ID/evidence.json`. It does **not** set overall status to passed.
4. Diagnose failed or blocked checks. Rerun after code changes. Never edit required runner check entries by hand to fabricate success.
5. Inspect actual results, fill `acceptance_criteria` with IDs, status and concrete evidence. Set top-level `status: passed` only when all acceptance IDs and required checks are verified; otherwise leave `not_verified`.
6. Write `qa-report.md` with executed checks, skipped/manual checks, environment caveats and residual risks. Run `python3 {{SDLC_SCRIPT_DIR}}/sdlc.py gate TASK-ID`; if gate fails, stop or return to build.
7. A passing gate is not a substitute for CI, QA signoff, code review or human PR approval.

## Safety
No destructive production commands or migrations without explicit approval. Do not save raw command output, secrets or customer data. If a command changes tracked/untracked worktree files during execution, runner marks it failed; rerun after stabilizing the worktree. This is agent-accessible local evidence, not tamper-proof provenance.

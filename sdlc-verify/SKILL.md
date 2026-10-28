---
name: sdlc-verify
description: Verify implementation with real build, lint, tests and acceptance checks; record reproducible evidence.
---
# SDLC Verify

1. Read plan and acceptance criteria; identify applicable checks based on repository scripts and CI configuration.
2. Run relevant test, lint, typecheck, build and security checks when available; for T1 prefer targeted checks, T3 include broader regression coverage.
3. Record each executed command, exit code, summary, and timestamp in `docs/ai-sdlc/<task-id>/evidence.json` (see template). Mark skipped checks explicitly with reason.
4. Compare observed behavior with acceptance criteria. Never call a test passing if it was not executed.
5. Produce `qa-report.md` with pass/fail/blocked status, uncovered risks and manual QA instructions.
6. If failure is implementation-related, return to build with exact failure evidence; if environment-related, mark blocked rather than claiming success.

## Completion gate
`verified` only if all required checks passed and acceptance criteria have supporting evidence. Otherwise `failed` or `blocked`. Human/QA owns final acceptance.

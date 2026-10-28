---
name: sdlc-build
description: Implement an approved SDLC plan with focused code changes and tests, without silently changing scope.
---
# SDLC Build

1. Read `docs/ai-sdlc/<task-id>/plan.md` and any `design.md` first.
2. Require human approval for T2/T3 design decisions. T1 can follow a short plan when clear.
3. Implement small coherent steps, reuse project patterns, add/update meaningful tests.
4. Default to one agent. Delegate only when tasks are genuinely independent and benefits exceed overhead; never spawn review/fix agents recursively.
5. Run targeted tests when practical; record commands and actual exit status, never fabricate results.
6. If requirements or architecture assumptions change, stop and request decision; update plan after approval.
7. Update `progress.md` with completed steps, remaining work, changed files and known risks. Mark `ready_for_verify` only when implementation and tests are present.

## Rules
Do not bypass failing tests, remove assertions just to pass, leak secrets, or commit without request. Follow existing project instructions and repository conventions.

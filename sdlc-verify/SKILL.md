---
name: sdlc-verify
description: Verify changes using real commands, persist evidence.json, and run the v0.2 evidence gate before handoff.
---
# SDLC Verify (v0.2)

1. Read `plan.md` and acceptance criteria.
2. Discover actual repository build, lint, typecheck and test commands. Run relevant checks; for T1 targeted checks may suffice, for T3 include regression and risk-based QA.
3. Write `docs/ai-sdlc/<task-id>/evidence.json` with:
   - `task_id` matching the task and `status: "passed"` only when appropriate.
   - Nonempty `checks` array. Each required check needs `name`, `command`, `exit_code: 0`, `status: "passed"`; optional skipped checks must be `required: false` and state why.
   - Nonempty `acceptance_criteria` array. Each criterion needs `status: "passed"` and a nonempty `evidence` description.
4. Write `qa-report.md` with test outcomes, manual QA steps, remaining risks.
5. Run `python3 .claude/ai-sdlc/scripts/sdlc.py gate <task-id>` when installed. If gate fails, return to build or report blocked.
6. Never invent evidence. The gate validates declared outcomes and structure; it does **not** cryptographically prove commands ran.

# Failure recovery — diagnose before retry

On test/lint/build/gate failure, capture exact command, exit code, failing case and relevant environment. Never claim passing checks without execution.

| Failure type | Action |
|---|---|
| Code regression | Reproduce with smallest relevant test, fix root cause, rerun affected and necessary regression checks |
| Environment/dependency | Identify missing service/configuration; use supported local substitutes if meaningful; mark blocked/not verified rather than passed |
| Flaky | Retry **once** with recorded evidence; investigate nondeterminism, do not silently convert to pass |
| Unrelated baseline | Compare with baseline if available, disclose; avoid unrelated refactor without permission |
| Unknown | Reproduce once, narrow scope; after two unsuccessful attempts on same unexplained issue, stop and report |
| Evidence gate | Inspect required checks/acceptance IDs/review artifacts; do not fabricate JSON to satisfy gate |

On task interruption or compaction, read `resume-protocol.md`, state and current git diff; do not reuse stale evidence after code changes. If blocked, record exact next action and owner. For a review finding, follow `review-triage.md`; do not recursively restart the full workflow.

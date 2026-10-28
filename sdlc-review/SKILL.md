---
name: sdlc-review
description: Perform evidence-based code review, deduplicate findings, and prepare human PR review without endless fix loops.
---
# SDLC Review

1. Read plan, diff, tests, evidence and QA report.
2. Review correctness, regressions, security, performance, concurrency, error handling and maintainability proportionate to risk.
3. Only report actionable findings with file/line, impact, reproduction or reasoning, severity (critical/high/medium/low), and confidence.
4. Distinguish verified defects from hypotheses. Deduplicate by root cause; do not re-open resolved findings without new evidence.
5. Write `review.md` with findings, dispositions and residual risks.
6. Permit at most two **automatic** fix/review cycles. After that, or for unresolved high/critical issues, stop with `needs_human_review` and surface the issue. Never declare success with unresolved blockers.
7. Human owns merge/release approval. Do not merge automatically.

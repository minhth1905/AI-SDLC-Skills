---
name: sdlc-review
description: Review implementation against approved spec and real evidence, triage actionable findings and prevent endless automatic fix/review loops.
---
# SDLC Review — prioritize verified defects

## Inputs
Read approved spec/plan, diff, tests, progress, evidence.json and qa-report.md. Review the actual changed files, not the entire repository by default.

## Procedure
1. Establish baseline: acceptance IDs, changed code, prior known findings, tests actually run and deployment risk.
2. Inspect correctness, regression, security/authorization, concurrency, performance, error handling, data migration and maintainability proportional to tier.
3. For every candidate finding, require: file/location, precise failure scenario, impact, severity, evidence or reproducible reasoning, confidence and suggested minimal fix.
4. Deduplicate by root cause. Separate **confirmed** bugs from **suspected** risks. Style-only suggestions are not blockers unless they violate project standards.
5. Assign disposition: `fix_now`, `needs_human_decision`, `follow_up`, or `not_a_bug`. Critical/high correctness/security issues cannot be silently deferred.
6. Save `review.md` using `references/review-template.md`. Include test gaps and what review cannot prove.
7. If fixable, send a precise finding list to build; after fix, rerun relevant verification. Limit automatic review/fix cycles to two; do not restart review from scratch without new evidence.
8. If budget exhausted or high-risk ambiguity remains, stop as `needs_human_review`. Never label unresolved blockers as completed.
9. Human owns PR merge and release. A clean AI review is **not** human approval.

## Review examples
- Rails: missing `includes` in a loop may be an N+1; cite call site and query behavior, not a vague performance warning.
- Rails: race-prone booking code must show interleaving or missing transactional guard.
- NestJS: job retried after side effect without idempotency guard is a concrete duplicate-action risk.
- SSE: response termination path may leak subscriptions; show exact lifecycle.

## Common rationalizations to reject
| Claim | Better standard |
|---|---|
| "Looks good" | Identify which acceptance criteria and tests were examined |
| "Possible race condition" | Show conflicting writes and missing synchronization |
| "Review again until zero findings" | Triage, verify fixes, cap automatic loops |
| "Tests passed so no review needed" | Tests and code review cover different risks |
| "Low severity means ignore" | Record and explicitly disposition |

## Completion checklist
- [ ] Every blocking finding actionable and supported
- [ ] Duplicates merged and resolved findings not reopened without evidence
- [ ] All critical/high issues resolved or escalated
- [ ] Review cycles within budget
- [ ] Human handoff clear

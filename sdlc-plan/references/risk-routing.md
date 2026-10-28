# Task routing and risk tiers

| Tier | Typical change | Artifacts | Approval | Checks |
|---|---|---|---|---|
| T1 | Typo, isolated view/logic fix, small safe refactor | short plan, evidence | no separate plan approval if user asked to implement | targeted tests |
| T2 | New endpoint, bounded UI flow, moderate business logic | spec.md, plan.md, evidence.json, review.md | combined spec/plan approval | unit + integration as applicable |
| T3 | Cross-service design, payment, auth, schema migration, data loss risk, high concurrency | capability map if needed, spec.md, design.md, plan.md, evidence, QA report, review | explicit architecture approval | broader regression, security and rollback |

## Decision tree
1. Could failure leak data, lose money, corrupt persistent state, bypass authorization or cause broad outage? **T3**.
2. Does work span independently deployable capabilities or require new interfaces/migrations? Usually **T3**, unless risk and scope are demonstrably bounded.
3. Is this a new behavior requiring acceptance criteria across several components? **T2**.
4. Is it localized, reversible, and clear? **T1**.
5. Unsure? Classify higher until evidence reduces risk.

## Examples
- Rails: change one i18n string → T1.
- Rails: add an admin filter with authorization and pagination → T2; may escalate for sensitive data.
- Rails: alter booking locking, payment webhooks, or large-table migration → T3.
- NestJS: add a simple DTO field to internal endpoint → T2 if contract changes.
- NestJS: SSE streaming with Cloud Tasks retries and per-user quotas → T3.

## Human approvals
Never use a CLI flag as independent proof of approval. Wait for the human's explicit message and record a short summary of what was approved. If material scope changes, re-approve. No auto-merge.

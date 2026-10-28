# Review triage — actionable findings, bounded loops

Review actual diff against approved acceptance IDs, tests and evidence. Focus on correctness, authorization, data safety, concurrency, performance and regression proportional to tier.

For each finding record: file/location, concrete failure scenario, impact/severity, observed or reproducible evidence, confidence, and smallest safe fix. Separate confirmed bug from suspected risk. Deduplicate by root cause.

| Disposition | Rule |
|---|---|
| fix_now | Reproducible correctness/security defect or regression within approved scope |
| needs_human_decision | Architectural/product choice, high-risk ambiguity or material scope change |
| follow_up | Nonblocking improvement with explicit risk and owner |
| not_a_bug | Unsupported or incorrect finding, with rationale |

Critical/high correctness/security findings cannot be silently deferred. Style-only comments are not blockers unless project standards require them. After fix, rerun impacted checks and update review.md. Maximum two automatic fix/review cycles across resume; do not restart from zero. If exhausted, transition to needs_human_review or blocked per CLI rules and hand off unresolved findings. A clean AI review does not authorize merge.

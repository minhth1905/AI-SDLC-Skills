# Context management — progressive disclosure and safe resume

Keep the main SKILL.md short. Load **only the policy relevant to the current decision**: risk at classification, requirements at spec, execution at build, failure policy on failures, triage at review. Read community routing only before invoking specialist methods.

At task start: repo instructions, ticket, git status, relevant code/tests and `docs/ai-sdlc/index.md` if useful. Do not dump the full repository or every prior task into context.

At phase handoff, persist compact `progress.md`: task ID/tier, current slice, changed paths, decisions, test commands/outcomes, blockers, next safe step, and actual community skill/fallback. Do not copy full chat transcripts, secrets, personal data or raw logs.

After compact/interruption: identify explicit task; run `sdlc.py resume ID`; read state, relevant spec/plan/progress/evidence/review and git diff. Revalidate decisions against current code, verify approval in human conversation, and rerun checks when code changed. Do not re-brainstorm completed slices or infer test passes from old summaries.

Token optimization must never omit a required human gate, evidence, security checks, or rollback consideration. Escalate if artifacts and worktree conflict.

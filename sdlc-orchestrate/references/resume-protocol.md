# Resume protocol for compacted or interrupted sessions

1. Identify active task from explicit user request or `.ai-sdlc-active`. Never assume the most recent folder is current.
2. Run `python3 .claude/ai-sdlc/scripts/sdlc.py resume <task-id>` if installed.
3. Read `state.json` for tier, phase, approval flag and review budget.
4. Read `spec.md` (if present), `plan.md`, `progress.md` and latest `evidence.json`. Read `review.md` when phase is reviewing.
5. Compare artifacts to current git diff/status; a saved artifact may be stale or generated before edits.
6. Continue only the next safe slice. If approval is uncertain, ask rather than inferring.
7. Run tests again when evidence is stale relative to new changes. Never reuse old passing results for modified code.
8. Save a brief progress summary after each slice: decisions, files, tests, blockers and next action.

## Recovery examples
- State `planned`, tier T2, no explicit approval → stop and request plan approval.
- State `building`, progress S2 incomplete → inspect S2 diff/tests, continue S2 only.
- State `verifying`, evidence missing → execute verification; do not advance.
- State `reviewing`, two loops used → escalate findings to human, do not spawn another review agent.

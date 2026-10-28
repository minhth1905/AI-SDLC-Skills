# Execution policy — fast path without losing control

Before each phase, read `community-skills.md` and confirm actual availability of the relevant Addy skill. Use it for specialist method only when available; otherwise use the orchestrator fallback and note which was used in progress.md. Do not spawn subagents by default.

## Phase boundaries
- T1: short plan -> build -> targeted verify -> focused review; no ceremonial spec or approval when implementation explicitly requested.
- T2: testable spec + vertical-slice plan -> one explicit human approval -> build -> verify -> review.
- T3: architecture alternatives, contract/data/security implications, rollout/rollback -> explicit human decision -> build -> verify -> review.
- Every slice: inspect narrow code, create meaningful failing test when feasible, implement minimum behavior, run targeted check, inspect diff, persist progress.
- One agent by default. Delegate only independent disjoint slices with explicit ownership and measurable benefit; avoid multi-agent review ping-pong.
- Do not run entire repository tests repeatedly when targeted checks can isolate the failure; widen checks for T2/T3 before handoff.
- Do not run uncontrolled upstream auto-commit flows. Never auto-commit/push/merge/deploy or enable hooks.
- Stop on high-impact scope drift; revise spec/plan, seek renewed approval. A changed naming choice alone does not need approval.

## Budget
One initial review and at most two **automatic fix/review cycles**. Persist loop count through existing state/progress conventions, do not reset after compact. If a blocker remains, stop with evidence and request a human decision.

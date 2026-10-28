---
name: sdlc-orchestrate
description: Risk-adaptive Jira-ticket-to-PR workflow with decision policies, human gates, evidence, resume and Git-local context.
---
# AI-SDLC Orchestrate v0.6

**Purpose:** execute only requested scope (analysis, plan or implementation), with minimal interruptions and real evidence. Human owns high-impact decisions, commit/push, PR merge and release. Never invent ticket details, approvals, test results or community skill invocations.

## Progressive policy loading
Load references **at the decision point**, not all at once:
- Classification: `references/risk-classification.md`
- Requirement ambiguity / spec: `references/requirement-analysis.md`
- Phase execution / agent budget: `references/execution-policy.md`
- Test, gate or environment failure: `references/failure-recovery.md`
- Review findings: `references/review-triage.md`
- Compact, recovery or context budget: `references/context-management.md` and `references/resume-protocol.md`
- Before specialist methodology: `references/community-skills.md`
- When creating task artifacts: `references/spec-template.md`, `references/plan-template.md`, `references/review-template.md`

## Lifecycle
1. **Understand:** read CLAUDE.md/AGENTS.md, user ticket, relevant code/tests and git status. Identify analysis-only vs plan-only vs implementation. Never run beyond requested scope.
2. **Resume/init:** `python3 .claude/ai-sdlc/scripts/sdlc.py resume ID`; if no state, classify T1/T2/T3 and `init ID --tier Tn`. Never overwrite existing task progress.
3. **Spec/plan:** T1 brief plan; T2 spec + vertical-slice plan with **one combined human approval**; T3 explicit architecture/contract/rollback decision. Write canonical `docs/ai-sdlc/ID/` artifacts, transition `new → planned`; STOP if awaiting approval.
4. **Build:** T2/T3 require actual human approval before `approved --human-approved → building`; T1 `planned → building`. Prefer installed Addy methodology, fallback locally when unavailable. Implement/test one slice at a time and persist progress. Default **one agent**.
5. **Verify:** `building → verifying`. Invoke `sdlc-verify`; run actual relevant checks, record `evidence.json` and `qa-report.md`, then `sdlc.py gate ID`. A gate only validates reported evidence, not independently executed commands.
6. **Review:** `verifying → reviewing`. Use Addy review method when installed, otherwise focused diff review; record `review.md`. Triage actionable findings, at most **two automatic fix/review cycles** total; escalate unresolved blockers.
7. **Capture:** only after `reviewing → ready_for_human_review` with passing gate and review. Invoke `sdlc-capture`, dry-run and execute `context_store.py`, inspect generated docs and git diff. Never auto-commit, push, merge or deploy.

## Stop and handoff
Stop for high-impact unknowns, changed approved scope, missing approval, dangerous/production commands, failed verification without a safe fix, exhausted review budget, or plan-only completion. Handoff tier, phase, changed files, real checks, unresolved risks, next human decision and context paths. On compact, resume from persisted state and current diff; never assume stale evidence is valid.

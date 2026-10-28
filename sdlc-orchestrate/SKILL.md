---
name: sdlc-orchestrate
description: Run risk-adaptive ticket-to-PR workflow with Addy community methods and team-owned state, approvals, evidence, and Git context.
---
# AI-SDLC Orchestrate (v0.5)

Run only the scope requested: analysis, plan or implementation. Read repo CLAUDE.md/AGENTS.md, git status, ticket, existing code and docs/ai-sdlc/index.md. Do not auto-commit, push, merge, deploy, run destructive migrations or disclose secrets.

## Risk routing
- **T1**: localized, reversible, low-risk fix; concise plan, targeted test, review; no separate approval when implementation was requested.
- **T2**: bounded feature, new endpoint or business logic; spec and plan, **one combined human approval** before build; unit/integration checks.
- **T3**: payment, security, auth, concurrent writes, migrations, potential data loss, cross-service architecture; capability boundaries where needed, explicit architecture approval, broader regression, rollback/security checks.
- If uncertain, classify higher. Reassess on scope change and stop for reapproval.

## Community methods (do not duplicate)
Read `references/community-skills.md`. When creating canonical task artifacts, use the installed templates in `references/spec-template.md`, `references/plan-template.md` and `references/review-template.md` as lightweight starting points; adapt them to the task tier, and do not generate unnecessary sections for T1. Prefer **installed** Addy skills for spec, planning, incremental build/TDD and review. Use their methods for the relevant phase; never claim a plugin was invoked when it was not available. If missing, apply the compact built-in fallback below; disclose the fallback. Upstream mandatory gates still apply when using upstream skills. Never allow upstream automatic commits or incompatible artifact overwrites.

## Workflow
1. **Resume or initialize:** `python3 .claude/ai-sdlc/scripts/sdlc.py resume ID`; if absent, classify and `init ID --tier Tn`. Read existing task artifacts before changing anything.
2. **Specify:** T1 short acceptance notes. T2/T3 write `docs/ai-sdlc/ID/spec.md`: behavior, assumptions, edge cases, testable acceptance IDs. Ask only blocking questions (batch at most three). Never invent missing ticket content.
3. **Plan:** write `plan.md`: scope, ordered small vertical slices, likely files, acceptance-to-test mapping, risks, rollback where relevant. T3 add `design.md` with alternatives and architecture decisions. Transition `new → planned`. Stop for required approval.
4. **Build:** T2/T3 only after explicit user approval: `planned → approved --human-approved → building`. T1 `planned → building`. Implement smallest slice, write failing test where feasible, fix, run targeted checks, update `progress.md`; avoid unrelated edits. Default one agent.
5. **Verify:** `building → verifying`; invoke `sdlc-verify`. Run real project test commands, record exit codes and acceptance evidence, write qa-report.md; `sdlc.py gate ID` must pass. On failure return to build or stop blocked.
6. **Review:** `verifying → reviewing`; use installed Addy code-review-and-quality method, or fallback: examine changed diff for correctness, security, concurrency, regression, performance and maintainability; document actionable, evidence-based findings in `review.md`. Maximum **two** automatic fix/review cycles; unresolved blockers escalate. `reviewing → ready_for_human_review` only after gate and review.
7. **Capture:** invoke `sdlc-capture`, create a curated manifest, dry-run and execute `context_store.py`; inspect Git-local handoff and index. Human reviews PR and documentation.

## Recovery and safety
Persist `state.json`, `progress.md`, `evidence.json`, `review.md` in the target Git project. After compact, read state, spec, plan, progress, evidence, review and current diff; continue at the recorded phase, never restart blindly. No automatic approval, invented test passes, repeated review loops, or dangerous commands without permission.

## Handoff
Report tier, actual changes, real test results, remaining risks, knowledge files and exact next human action. A clean AI review is not merge approval.

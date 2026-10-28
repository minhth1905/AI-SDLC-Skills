---
name: sdlc-orchestrate
description: Coordinate plan, build, verify and review with risk-based human gates, persistent artifacts and v0.2 local lifecycle commands.
---
# SDLC Orchestrate (v0.2)

## Start or resume
- Find the task's `docs/ai-sdlc/<task-id>/state.json`. If missing, run `python3 .claude/ai-sdlc/scripts/sdlc.py init <task-id> --tier T1|T2|T3` after classifying risk.
- For an existing task, run `python3 .claude/ai-sdlc/scripts/sdlc.py resume <task-id>` and read plan, progress, evidence and review artifacts before taking action. **Never restart brainstorming merely because context compacted.**
- Keep `.ai-sdlc-active` set to the task ID only if optional Claude hooks were installed and explicitly enabled.

## Phases
`new → planned → approved (T2/T3) → building → verifying → reviewing → ready_for_human_review`; failures go to `blocked` or a recorded correction phase.
- After plan, use `sdlc.py transition <task-id> planned`.
- T2/T3: stop for human approval of the proposed approach. After the human actually approves, use `transition <task-id> approved --human-approved`. Never auto-approve.
- Use `sdlc-build`; transition to `building` and then `verifying`.
- Use `sdlc-verify`, record real evidence, and run `sdlc.py gate <task-id>` before review. Then transition to `reviewing`.
- Use `sdlc-review`, ensure `review.md` exists; transition to `ready_for_human_review` only if evidence gate passes.
- Max two automatic review/fix cycles; unresolved findings or exhausted budget require human intervention.
- Do not merge or deploy without explicit human approval.

## Rules
Prefer one agent; ask only blocking questions; document assumptions. Never fabricate tests, claim security enforcement, or silently change scope. Use code for lifecycle and AI for reasoning. The CLI is a local convention and can be modified by the agent, not a security boundary.

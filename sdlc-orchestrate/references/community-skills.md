# Community skill routing (v0.5)

AI-SDLC retains **only** `sdlc-orchestrate`, `sdlc-verify`, and `sdlc-capture`. The Addy plugin is a separate, optional dependency. No upstream content is copied into this repository.

| Phase | Addy skill (when installed) | Built-in fallback |
|---|---|---|
| Spec | `spec-driven-development` | Orchestrator writes concise testable spec |
| Plan | `planning-and-task-breakdown` | Orchestrator creates vertical-slice plan |
| Build | `incremental-implementation` + `test-driven-development` | Orchestrator implements/test slices |
| Verify | `test-driven-development` for test method | **`sdlc-verify` always owns evidence** |
| Review | `code-review-and-quality` | Orchestrator performs focused diff review |
| Capture | — | **`sdlc-capture` always owns Git context** |

## Availability and safety
1. Check whether each named upstream skill is installed and invocable in the current Claude Code/Codex environment. Names in this document do not install or invoke plugins.
2. If available, read and apply that skill's instructions for its phase. If unavailable, use fallback and record that fact in `progress.md`. Do not hallucinate an invocation.
3. **Do not call upstream `/build auto` or other commands with uncontrolled commit/push behavior.** Follow the incremental method without automatic Git writes.
4. Upstream `spec-driven-development` may require separate approval gates. Either honor those gates or use the built-in fallback when the team's combined T2 checkpoint is preferable.
5. Upstream planning may write `tasks/plan.md`; use `docs/ai-sdlc/ID/plan.md` as canonical and do not overwrite an unrelated active plan.
6. T1/T2/T3 policy, approvals, state machine, evidence, two-cycle review cap and context capture are always team-owned.
7. Pin and validate upstream versions for team-wide use. This is agent-instruction routing, not a programmatic skill-dispatch API.

Claude Code installation:

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

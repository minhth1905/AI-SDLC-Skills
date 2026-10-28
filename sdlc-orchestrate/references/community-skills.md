# Community skills adapter — Addy Osmani Agent Skills

This is a **routing contract**, not a vendored dependency. Team AI-SDLC owns task state, approval, artifacts, evidence and Git-local handoff. Addy Osmani's skills own their specialist engineering methods when installed.

## Installation

For Claude Code, install as a plugin, independently of AI-SDLC:

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

Or install selected skills with `npx skills add addyosmani/agent-skills --skill <name>` (note: per-skill install does not include shared repo-level references). Read upstream README for current setup. Do not copy upstream skill content into this repository.

## Routing matrix

| Phase | Preferred upstream skill | Fallback | Team-owned output |
|---|---|---|---|
| Requirement/spec (T2/T3) | `spec-driven-development` | `sdlc-spec` | task `spec.md` |
| Break down/plan (T2/T3) | `planning-and-task-breakdown` | `sdlc-plan` | task `plan.md` |
| Build (multi-file) | `incremental-implementation` + `test-driven-development` | `sdlc-build` | code, tests, `progress.md` |
| Test behavior | `test-driven-development` | `sdlc-verify` | real checks, `evidence.json` |
| Pre-PR review | `code-review-and-quality` | `sdlc-review` | findings in `review.md` |
| Git-local knowledge | **`sdlc-capture`** | no automatic fallback | task handoff + index |

## How an orchestrator invokes an upstream skill

1. Detect whether the skill is actually available in the current agent's installed skills/plugin registry. **Never assume installation just because the project references it.**
2. Read that installed skill's instructions and use its workflow for the relevant phase.
3. Map upstream output into `docs/ai-sdlc/<task-id>/` and synchronize `state.json` / `progress.md`.
4. Follow upstream methodology without duplicating separate artifact trees. If upstream mandates `tasks/plan.md`, place the approved plan under AI-SDLC task folder as canonical, and provide a link/shim if necessary; do not overwrite a separate active plan.
5. **Team policy wins on conflicts**: T1 avoids full spec, T2 uses one combined human checkpoint, T3 requires architecture approval, no automatic commit/push/merge, no more than two automatic review/fix cycles. Any upstream command that requires additional mandatory approval must still be honored when invoking it; either ask, or use fallback when those extra gates are unsuitable.
6. If plugin invocation is unavailable, say so and use the local fallback, without pretending an upstream skill ran.
7. Record in `progress.md` which skill/adapter was used and whether fallback occurred.

## Important upstream differences

- `spec-driven-development` has multi-phase human gates; T2 combined approval and this workflow may conflict. Use upstream for the spec phase only and keep the rest under AI-SDLC, or explicitly honor upstream gates if using the entire workflow.
- `incremental-implementation` normally commits each slice. Team AI-SDLC **never auto-commits**: use the iterative implementation and verification parts only; do not invoke a command whose side effects cannot be safely constrained.
- `planning-and-task-breakdown` defaults to `tasks/plan.md`; avoid competing active plans.
- `code-review-and-quality` can produce review findings; team triage, severity and two-cycle cap remain mandatory.

## Pinning / team rollout

Track upstream version or commit in your team's dependency policy before broad rollout; test upgrades on representative Rails and NestJS tasks. The routing matrix is only a prompt-level adapter in v0.4. It is **not** an executable skill-dispatch engine.

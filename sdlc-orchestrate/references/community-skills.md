# Mandatory Addy skill routing (when installed)

The three team-owned skills remain `sdlc-orchestrate`, `sdlc-verify`, and `sdlc-capture`. Addy Osmani's agent-skills is a separately installed dependency, not vendored into this repository.

**Rule: for every phase actually executed, if the mapped Addy skill is installed and readable, you MUST load and apply it.** Do not silently use the built-in fallback for convenience, speed or a preferred approval style. T1 may skip unnecessary phases, but cannot bypass an available skill for a phase it actually performs.

| Phase executed | Required Addy skill(s) if available | Fallback ONLY when unavailable |
|---|---|---|
| Specify | `spec-driven-development` | Team concise acceptance spec |
| Plan | `planning-and-task-breakdown` | Team vertical-slice plan |
| Build | `incremental-implementation`; `test-driven-development` for test-writing work | Team incremental implementation and tests |
| Verify | `test-driven-development` when developing or correcting tests | `sdlc-verify` always runs actual evidence checks |
| Review | `code-review-and-quality` | Team focused diff review |
| Capture | No Addy mapping | `sdlc-capture` always owns Git-local context |

## Required discovery and audit
1. At ticket start, inspect the **actual current runtime's skill catalog** (Claude Code plugin/skill listings or Codex skill inventory). Determine for each mapped name: available and readable, unavailable, or unknown. A README mention is not proof of installation.
2. At the start of each executed phase, check again if availability was unknown or may have changed. **Read the installed skill's instructions and apply its relevant methodology**, not merely mention its name. Never claim invocation when only the mapping was read.
3. Record a compact routing table in `docs/ai-sdlc/ID/progress.md`: phase, mapped skill, availability, `used` / `fallback` / `blocked`, and reason. Record skill source/version if available. Preserve it on resume.
4. Fallback is allowed only after confirming the skill is unavailable/unreadable, or the runtime cannot invoke it. Record the exact limitation. If availability cannot be determined, **do not assume absent**: attempt to inspect the catalog, then stop and ask for access/confirmation if still unknown.
5. If an installed skill requires unsafe commands, unauthorized commits, or incompatible approval gates, **do not silently replace it with fallback**. Apply its safe methodology where possible, honor stricter approval gates, and stop for a human decision if its mandatory instructions cannot be followed.
6. Team-owned tier classification, human approval, evidence gate, maximum two review/fix cycles, no automatic commit/push/merge/deploy, and capture remain authoritative safety constraints. Do not execute upstream `/build auto` or equivalent uncontrolled Git actions.
7. Upstream output paths (e.g. `tasks/plan.md`) must not overwrite unrelated work. Canonical team artifacts remain `docs/ai-sdlc/ID/`; copy/adapt the upstream method's results without claiming the upstream wrote canonical files.
8. After compaction, inspect the routing table and current skill availability; do not repeat completed phases or fabricate skill use.

This is a **prompt-enforced routing contract**, not a deterministic runtime dispatcher. Compliance requires checking actual runtime availability and recording what was done.

Claude Code installation:

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

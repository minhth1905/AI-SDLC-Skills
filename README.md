# AI-SDLC Skills Kit v0.5 — Lean workflow

A risk-adaptive, one-command engineering workflow for Claude Code. **Addy Osmani's agent-skills** supplies optional engineering methods; this repository supplies **workflow orchestration, verifiable evidence contracts and Git-local knowledge capture**.

## Three team skills

| Skill | Team responsibility |
|---|---|
| `sdlc-orchestrate` | Risk tiers, approvals, spec/plan/build/review fallback, state and resume |
| `sdlc-verify` | Real checks, acceptance evidence and QA gate |
| `sdlc-capture` | Curated implementation, decisions and handoff in target project's Git |

Community methods (when installed): `spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `code-review-and-quality`. See [routing policy](sdlc-orchestrate/references/community-skills.md). Without the Addy plugin, the orchestrator uses compact fallback instructions; it does not pretend the community skill ran.

## Install into a Git project

```bash
git clone https://github.com/minhth1905/AI-SDLC-Skills.git
cd AI-SDLC-Skills
python3 scripts/install.py --target /path/to/project
```

Existing files are protected by default. To upgrade an existing installation, inspect local modifications first, then:

```bash
python3 scripts/install.py --target /path/to/project --force
```

The old four skills (`sdlc-spec`, `sdlc-plan`, `sdlc-build`, `sdlc-review`) are **not** installed by v0.5. Existing copies are not deleted unless you explicitly add `--prune-legacy` (which permanently deletes those four target directories; back up any custom edits first). Do not use `--force` or `--prune-legacy` without reviewing the target.

Install Addy independently in Claude Code if desired:

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

## Run

From the target project in Claude Code:

```text
/sdlc OOPS-123 Fix booking concurrency and add regression tests
```

For T2/T3, the agent must stop for actual human approval of spec/plan before building. After approving:

```text
/sdlc OOPS-123 Approved. Continue implementation according to the plan.
```

After compaction: `/sdlc OOPS-123 Resume`. The agent reads `docs/ai-sdlc/OOPS-123/` and the current Git diff.

### Tiers

- **T1:** small reversible fix; brief plan, targeted verification; no separate plan approval.
- **T2:** bounded feature; spec and plan, one combined approval; integration tests where applicable.
- **T3:** payment, security, concurrency, migrations or cross-service design; explicit architecture approval, regression/rollback/security review.

The lifecycle is tracked by `scripts/sdlc.py`. Evidence must include actual commands, exit codes and acceptance outcomes; `sdlc.py gate` validates declared fields, **not** independent test execution. After review, `context_store.py` saves `implementation.md`, `decisions.md`, `handoff.md` and `docs/ai-sdlc/index.md` in the target Git project.

## Test

```bash
python3 -m unittest discover -s tests -v
```

CI config: `.github/workflows/test.yml`. Run tests and validate a real Claude Code ticket before relying on this in production.

## Boundaries

- No automatic commit, push, merge, deployment, or irreversible migration.
- No built-in Jira adapter: supply ticket text or a URL accessible to the agent.
- The slash command is prompt-driven, **not** an independently tested skill-dispatch engine.
- Installer does not enable hooks, install third-party plugins, or modify Claude settings.
- Agent-written evidence and human approval flags are not tamper-proof.
- Existing `sdlc-*/references` files may remain in the framework repository for history, but only three `SKILL.md` entrypoints are active.

## License

No license granted unless repository owner adds a LICENSE file.

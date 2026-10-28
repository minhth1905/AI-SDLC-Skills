# AI-SDLC Skills — Ticket-to-Handoff Workflow for Codex & Claude Code

A risk-adaptive engineering workflow that takes a ticket from requirements to implementation, **real test evidence**, code review, and a reusable human handoff.

**Codex-first:** the team can install native skills in `.agents/skills/`. Claude Code remains supported through `.claude/`. The source repository is [minhth1905/sdlc-skills](https://github.com/minhth1905/sdlc-skills); it is **GitHub-distributed**, not an official marketplace listing.

> **Important:** This is an instruction-driven workflow with Python state/evidence scripts, not a deterministic multi-agent workflow engine. Human approval and review still matter. It does **not** automatically commit, push, create a PR, merge, deploy, or perform production migrations.

## Contents

1. [What is included](#what-is-included)
2. [Quick start: Codex](#quick-start-codex)
3. [Install Addy skills](#install-addy-skills)
4. [How a ticket flows](#how-a-ticket-flows)
5. [Risk tiers and approvals](#risk-tiers-and-approvals)
6. [Using the workflow in Codex](#using-the-workflow-in-codex)
7. [Files generated in your project](#files-generated-in-your-project)
8. [Verification and capture](#verification-and-capture)
9. [Claude Code installation](#claude-code-installation)
10. [Upgrade, troubleshooting and testing](#upgrade-troubleshooting-and-testing)

## What is included

| Team skill | Responsibility |
|---|---|
| `sdlc-orchestrate` | Interpret ticket and scope; classify risk; coordinate spec, plan, approval, build, verify, review, resume |
| `sdlc-verify` | Select checks, run actual commands with runner provenance, map acceptance criteria, enforce evidence gate |
| `sdlc-capture` | Curate source-grounded implementation notes, decisions, risks and next human actions in Git-local documents |

The orchestrator uses **Addy Osmani's agent-skills** for specialist methods. For every phase actually executed, an installed/readable mapped Addy skill **must** be used; fallback is allowed only when confirmed unavailable. Skill availability, use and fallback reasons must be recorded in `docs/ai-sdlc/<TICKET-ID>/progress.md`. Unknown availability is not permission to silently fallback.

| Phase | Addy skill, when available | Team-owned responsibility |
|---|---|---|
| Spec | `spec-driven-development` | Scope, acceptance and approval |
| Plan | `planning-and-task-breakdown` | Risk tier, canonical plan and approval |
| Build | `incremental-implementation`, plus `test-driven-development` for test work | State, slices and safety constraints |
| Verify | `test-driven-development` when writing/fixing tests | **`sdlc-verify` owns evidence and gate** |
| Review | `code-review-and-quality` | Findings triage and bounded fix loops |
| Capture | No Addy mapping | **`sdlc-capture` owns handoff** |

See [mandatory Addy routing policy](sdlc-orchestrate/references/community-skills.md). This is a **prompt-enforced contract**, not a technical guarantee of skill invocation; inspect `progress.md` during rollout.

## Quick start: Codex

**Prerequisites:** Git, Python 3, a Git repository for your application, and Codex with skills support. The installer uses only Python's standard library.

Clone the skills repository outside (or alongside) your application project:

```bash
git clone https://github.com/minhth1905/sdlc-skills.git
python3 sdlc-skills/scripts/install.py \
  --target /absolute/path/to/your-app \
  --platform codex
```

For example, if you are in your app directory and cloned the skills repo next to it:

```bash
python3 ../sdlc-skills/scripts/install.py --target . --platform codex
```

**What the installer adds:**

```text
your-app/
├── .agents/
│   ├── skills/
│   │   ├── sdlc-orchestrate/SKILL.md (+ references/)
│   │   ├── sdlc-verify/SKILL.md (+ references/)
│   │   └── sdlc-capture/SKILL.md (+ references/)
│   └── ai-sdlc/scripts/
│       ├── sdlc.py
│       ├── verify_runner.py
│       └── context_store.py
└── ...your existing project files
```

The installer rewrites script paths **in installed Codex skill copies** from `.claude/` to `.agents/`. It does **not** change `AGENTS.md`, install Addy automatically, or install Claude slash commands in Codex.

Start Codex **from your application project** and invoke:

```text
$sdlc-orchestrate Implement OOPS-123.
Ticket: <paste requirement text or accessible ticket URL>.
Use the installed Addy skills for each applicable phase.
```

If the ticket URL is not accessible to Codex, paste its description and acceptance criteria. No built-in Jira connector is included.

## Install Addy skills

Addy skills are **separate** from this repository. Install them using the method supported by your Codex version, and confirm that the Codex session can discover/read these five names:

```text
spec-driven-development
planning-and-task-breakdown
incremental-implementation
test-driven-development
code-review-and-quality
```

Addy upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills).

For a manual, repository-scoped skill installation, use the upstream skill directories **as published by Addy** and place the appropriate directories under `your-app/.agents/skills/`; do not assume a particular upstream folder layout without inspecting it. Restart/reload Codex after installing skills if they do not appear.

Ask Codex to enumerate its available skills before the first ticket. If a required Addy skill is unavailable, the orchestrator may use its documented fallback **only after confirming that fact and recording it**. If installed but inaccessible, investigate rather than pretending it ran.

**Claude Code** can install Addy through its plugin commands:

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

## How a ticket flows

```text
Ticket / acceptance criteria
          │
          ▼
1. UNDERSTAND + RESUME — inspect code, current diff, prior task state
          │
          ▼
2. CLASSIFY RISK — T1 / T2 / T3
          │
          ▼
3. SPEC + PLAN — mandatory Addy methodology if installed
          │
          ├── T2/T3: STOP for human approval
          │
          ▼
4. BUILD — incremental slices, tests, persist progress
          │
          ▼
5. VERIFY — real commands via verify_runner.py + evidence gate
          │
          ├── Failed? Fix and rerun relevant checks, or stop
          ▼
6. REVIEW — Addy review if installed; at most 2 auto fix/review cycles
          │
          ▼
7. CAPTURE — curated implementation, decisions, handoff and index
          │
          ▼
8. HUMAN REVIEW — inspect diff and decide PR/merge/release separately
```

**Ownership:** `sdlc-orchestrate` coordinates phases; `sdlc-verify` validates execution evidence; `sdlc-capture` writes durable knowledge. A review-ready state does **not** mean human QA approval, merge, or deployment.

## Risk tiers and approvals

| Tier | Example | Planning | Human checkpoint | Verification |
|---|---|---|---|---|
| **T1 — Fast** | Small reversible UI/logic fix | Brief plan, relevant acceptance | No separate plan approval when implementation was requested | Targeted checks and focused review |
| **T2 — Standard** | Bounded feature or API | Testable spec and vertical-slice plan | **One combined spec/plan approval** | Unit/integration tests as relevant |
| **T3 — High risk** | Payment, concurrency, auth/security, migration | Architecture choices, contracts, rollout/rollback | **Explicit high-impact design approval** | Risk-based regression and safety checks |

T1 skips unnecessary *phases*, not installed Addy skills for phases it does execute. Additional upstream mandatory approval gates must be honored; conflicts require a human decision, not silent fallback.

## Using the workflow in Codex

### Example: booking concurrency

```text
$sdlc-orchestrate Implement OOPS-123.
Requirement: Prevent two users from booking the same time slot.
Acceptance criteria:
- Only one concurrent request may reserve the slot.
- The losing request receives a clear error.
- Add a regression test for concurrent requests.
Use installed Addy skills and follow the team's approval gates.
```

The orchestrator should classify concurrency as **T3**, inspect existing Rails code and tests, propose the locking/transaction strategy and rollback considerations, then **stop** for your explicit approval before building.

After reviewing the plan, continue in Codex:

```text
$sdlc-orchestrate OOPS-123 Approved. Continue implementation using the approved plan.
```

If a session is compacted or interrupted:

```text
$sdlc-orchestrate Resume OOPS-123. Read existing state, progress and current git diff.
```

The resume path reads Git-local task state. It must not redo completed phases, assume stale evidence is valid, or infer approval from an earlier draft.

### Scope-only requests

You can also ask for **analysis only** or **plan only**. The orchestrator must not start implementation unless requested and approved as applicable.

## Files generated in your project

```text
docs/ai-sdlc/
├── index.md                      # Task handoff index
└── OOPS-123/
    ├── state.json                # Lifecycle phase / task status
    ├── spec.md                   # Requirements and acceptance (when needed)
    ├── plan.md                   # Proposed slices and decisions
    ├── progress.md               # Work status and Addy routing audit
    ├── evidence.json             # Test results and acceptance mapping
    ├── qa-report.md              # Verification summary
    ├── review.md                 # Findings and review status
    ├── implementation.md         # Curated outcome
    ├── decisions.md              # Durable design rationale and risks
    └── handoff.md                # Next human actions
```

Some files are phase-dependent. For example, T1 need not create a lengthy spec or architecture document. Do not dump chat history, credentials or production payloads into these artifacts.

## Verification and capture

**Verify:** Required checks must run through the runner, which records actual command exit codes and a working-tree fingerprint in `evidence.json`. For Codex:

```bash
python3 .agents/ai-sdlc/scripts/verify_runner.py OOPS-123 \
  --name booking-concurrency -- bundle exec rspec spec/requests/bookings_spec.rb

python3 .agents/ai-sdlc/scripts/sdlc.py gate OOPS-123
```

The runner does **not** assert that all acceptance criteria passed by itself. The gate checks evidence structure, required results and freshness; it is not tamper-proof. Changes to code after a test may invalidate the evidence, so rerun checks as necessary.

**Capture:** Once the lifecycle reaches `ready_for_human_review`, create a sanitized manifest matching [capture-manifest.json](sdlc-capture/references/capture-manifest.json), then preview and generate the handoff:

```bash
python3 .agents/ai-sdlc/scripts/context_store.py OOPS-123 \
  --manifest /path/to/capture-manifest.json --dry-run

python3 .agents/ai-sdlc/scripts/context_store.py OOPS-123 \
  --manifest /path/to/capture-manifest.json
```

Review the resulting docs and Git diff. The capture script validates basic inputs and file references but cannot independently prove every narrative claim or catch every secret.

## Claude Code installation

```bash
python3 sdlc-skills/scripts/install.py \
  --target /absolute/path/to/your-app \
  --platform claude
```

This installs `.claude/skills/`, `.claude/ai-sdlc/scripts/`, optional hook files (**not enabled**) and `.claude/commands/sdlc.md`.

Run in Claude Code:

```text
/sdlc OOPS-123 Fix booking concurrency and add regression tests
```

For both runtimes in one project:

```bash
python3 sdlc-skills/scripts/install.py \
  --target /absolute/path/to/your-app \
  --platform both
```

`both` installs both platform layouts; it does not synchronize future changes automatically.

## Upgrade, troubleshooting and testing

**Upgrade:** Update your local checkout of this repository and inspect team customizations before overwriting installed skills:

```bash
git -C sdlc-skills pull
python3 sdlc-skills/scripts/install.py \
  --target /absolute/path/to/your-app \
  --platform codex --force
```

`--force` replaces existing installed skill directories and scripts. Back up any local modifications first. The default is `--platform claude` for backward compatibility, so **always pass `--platform codex` for Codex**. Legacy skill deletion requires explicit `--prune-legacy` and should be reviewed carefully.

**Common issues:**

| Symptom | What to check |
|---|---|
| Codex does not show `$sdlc-orchestrate` | Run from the target Git project; confirm `.agents/skills/sdlc-orchestrate/SKILL.md` exists; reload session |
| Addy skills are skipped | Confirm actual installation/discovery and inspect routing entries in `progress.md` |
| Ticket URL cannot be read | Paste requirements and acceptance criteria; no built-in Jira integration |
| `sdlc.py` or runner not found | Check `.agents/ai-sdlc/scripts/` (Codex) vs `.claude/ai-sdlc/scripts/` (Claude) |
| Gate fails after edits | Rerun affected checks against the current working tree; inspect `evidence.json` |
| Workflow stops before code | T2/T3 approval or unresolved high-impact decision may be required |
| Installer refuses overwrite | Review installed customizations, then explicitly use `--force` if safe |

**Run repository tests:**

```bash
python3 -m unittest discover -s tests -v
```

CI workflow: `.github/workflows/test.yml`. Before rolling out to the team, smoke-test one T1 and one T2/T3 ticket in **real Codex** and inspect Addy routing, approval stops, runner evidence, capture outputs and absence of automatic Git mutations. Additional [Codex rollout notes](docs/codex.md).

## Safety and licensing

- No automatic commit, push, PR creation, merge, deployment or irreversible migration.
- No automatic installation of third-party Addy skills or modification of `AGENTS.md`.
- Evidence and approval markers are not cryptographically attested.
- No license is granted unless the repository owner adds a `LICENSE` file.

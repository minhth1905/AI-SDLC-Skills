---
name: sdlc-capture
description: Curate verified, non-sensitive, Git-local implementation knowledge and human handoff after review.
---
# SDLC Capture v0.8 — durable context, not chat history

**Trigger:** implementation reached `ready_for_human_review` with evidence.json and review.md. Never capture plan-only work as implemented. This status does not mean merged, released, or accepted by human QA.

## Progressive reference loading
- Source-to-code checks: `references/source-traceability.md`
- Choosing what is worth retaining: `references/knowledge-selection.md`
- Redaction and confidentiality: `references/privacy-and-sanitization.md`
- Handoff and manual QA: `references/handoff-quality.md`
- Updating the project index: `references/index-maintenance.md`
- Input schema example: `references/capture-manifest.json`

## Procedure
1. Confirm task ID, `state.json`, actual verification evidence and review. Read ticket/spec/plan/progress plus current Git diff/status. If state and working tree conflict, stop and reconcile.
2. Identify *durable, observed* facts: result, related changed files, non-obvious design decisions, test outcomes, remaining risks, exact next human action. For T1 keep it brief; for T3 include significant safety/rollback decisions.
3. Compare reported changed files with repository paths and diff. No fabricated test passes, unstated deployment claims, or unrelated paths.
4. Redact sensitive material before drafting a manifest. Pattern checks are a backup, not a substitute for review. Do not include raw logs/transcripts/customer data.
5. Prepare JSON matching `references/capture-manifest.json`. Run:
   `python3 .claude/ai-sdlc/scripts/context_store.py ID --manifest PATH --dry-run`
   Inspect the proposed outputs, then run without `--dry-run` if accurate.
6. Inspect `docs/ai-sdlc/ID/{implementation,decisions,handoff}.md` and `docs/ai-sdlc/index.md` in `git diff`. Confirm one index entry per task and clearly distinguished observed facts, residual risks and required human review.
7. Present next human action. Do not automatically commit, push, merge, deploy or edit project-wide instructions/ADRs.

## Source of truth and limitations
State/progress are resumable working memory, not verified long-term facts. Favor current code, approved decisions, review and executable evidence over chat recollection. `context_store.py` validates basic structure and reported file paths, but cannot verify every factual claim, detect every secret, or cryptographically attest tests. Humans review generated knowledge with the PR.

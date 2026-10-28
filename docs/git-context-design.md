# Git-local context architecture (v0.4)

## Decision
Every target application repository owns its AI-SDLC task knowledge in `docs/ai-sdlc/<task-id>/`. No centralized service, embedding store, or chat transcript storage is required.

## Lifecycle
1. `sdlc-orchestrate` creates/loads task state and routes work.
2. Spec/plan/build persist task context incrementally.
3. Verify records actual commands and acceptance evidence.
4. Review records findings and remaining risks.
5. **Capture** runs only after ready-for-human-review state and evidence gate, generating implementation, decisions, handoff, and a discoverable index.
6. Human reviews both code and context files in the PR, then merges when ready.
7. Future sessions read the index and task handoff, then inspect current code and git history before trusting old decisions.

## Boundaries
- Local Git is source of truth. Context is not pushed automatically.
- The capture script does not execute tests; evidence remains agent-reported.
- The script applies basic secret-pattern rejection, not full DLP. Never put sensitive data into the manifest.
- Context can become stale after later code changes; future agents must verify against current code.
- Project-level architecture decisions are suggested, not automatically promoted.
- Task folders are not automatically deleted. Retention follows repository policy.

## Future adapters
Optional Jira backlinks, CI attestations, search/indexing and cross-repo synchronization can be added without changing Git as the authoritative store.

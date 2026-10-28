# Human approval gate — self-contained decision

Before any T2/T3 implementation or consequential architecture approval, present a concise decision summary **in the conversation**, not just a path to plan.md. Aim for 150–250 words unless complexity requires more. Do not imply approval from silence or from creating a plan.

Required fields:
1. **Ticket, status, and decision requested** — say explicitly whether the user is approving architecture, implementation, or both.
2. **Recommended option explained** — describe Option A/B in plain language and concrete implementation terms; never use an option label alone. If alternatives exist, summarize material differences and why the recommendation wins. If the option definition is unavailable, retrieve the plan or ask for it; do not invent it.
3. **Implementation scope** — modules/files or change areas, expected user-visible behavior, explicit exclusions, and dependencies still outstanding.
4. **Risks and trade-offs** — highlight contract, data, security, migration, compatibility, and rollback impacts where applicable; state when none are expected rather than guaranteeing none.
5. **Proposed external actions** — for Jira subtasks, list each proposed title, parent issue, purpose/scope and any unknowns. Do not create or edit tickets until separately authorized.
6. **Clear response choices** — e.g. `Approve implementation plan`, `Approve creation of the two listed Jira subtasks`, `Approve both`, or `Request changes`. Distinguish decisions without forcing two rounds of questions: the user may explicitly approve both in one reply.

The implementation gate still requires the actual human-approved transition in `sdlc.py`. Record approvals and their exact scope in progress.md. A plan-only request remains plan-only even if approval is offered. Never create Jira subtasks or other external side effects based only on approval of architecture/implementation. If an approved scope materially changes, ask again.

Example (illustrative, not a claim about any real ticket):

**TICKET-123 — Awaiting implementation approval**
**Option A:** Extend existing doctor-order configuration and add two banner images. **Alternative:** Build a new catalog service, adding API and migration complexity. Recommend A because it reuses current code.
**Scope:** doctor catalog configuration and assets. **Excluded:** API, schema, calendar UI. **Risk:** existing ordering behavior needs regression tests.
**Proposed Jira subtasks:** (1) `Configure doctor catalog` — implement ordering; (2) `Add catalog banners` — integrate two assets. Parent: TICKET-123.
**Decisions:** Approve implementation plan? Separately approve creating these two Jira subtasks? You may approve either or both.

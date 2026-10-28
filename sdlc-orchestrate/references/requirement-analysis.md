# Requirement analysis — minimize questions, never invent contracts

1. Read exact ticket text and available linked source. If URL cannot be opened, say so; request the missing requirements when they block implementation.
2. Inspect only relevant code, tests, API/schema definitions and existing conventions. Separate **observed current behavior**, **requested behavior**, and **assumptions**.
3. Identify actors, scope in/out, acceptance IDs and failure paths. Prefer observable Given/When/Then criteria. Link each ID to a test or explicit manual check.
4. Classify unknowns: LOW = naming/internal organization; MEDIUM = UX or bounded implementation choice; HIGH = auth, money, persistence, public API, destructive action, concurrency or business semantics.
5. Assume LOW only with explicit note. For MEDIUM, choose existing conventions only if they cannot alter acceptance; otherwise ask. For unresolved HIGH, STOP. Batch up to three blocking questions in one message; avoid serial brainstorming.
6. Ticket conflicts with code or prior docs: describe both, identify the exact behavior decision and ask only if it changes acceptance. Do not silently privilege old docs over current code or Jira over confirmed contract.
7. If independent capabilities have separate consumers/data/deployment, draft capability boundaries before detailed T3 planning; ask approval for consequential boundaries.

T1: one-paragraph objective, acceptance and targeted test in plan. T2: spec + plan one checkpoint when requirements are clear. T3: explicit architecture and high-impact contract approval. Respect plan-only requests and do not implement.

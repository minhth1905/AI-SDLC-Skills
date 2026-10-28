# Risk classification — choose the smallest safe tier

Evaluate **impact**, **blast radius**, **reversibility**, **unknowns**, and **testability** before work. Risk is based on the proposed change, not the ticket label.

| Tier | Signals | Minimum delivery |
|---|---|---|
| T1 | Local, reversible, no contract/data/security/concurrency change | Brief plan with observable outcome; targeted test and focused review |
| T2 | Bounded behavior or API feature with controlled rollback | Testable spec, vertical-slice plan, one combined explicit approval, unit/integration evidence |
| T3 | Money, auth, secrets, destructive or large migration, concurrent writes, external side effects, cross-service contract, high blast radius | Architecture alternatives and failure modes, explicit human architecture decision, rollback, broad regression/security evidence |

Decision sequence:
1. Can a bug leak data, lose money, bypass permissions, corrupt state, or cause broad outage? T3.
2. Does the change alter synchronization, persistent schema, externally consumed contracts, irreversible side effects, or multi-service coordination? Default T3 unless bounded and reversible with evidence.
3. Is it new user-visible behavior or multi-component logic? T2.
4. Is it localized, clear and reversible? T1. Otherwise classify higher and record why.

Do not downgrade because implementation seems short or tests exist. Reclassify before executing newly discovered high-impact scope; record the reason and seek approval. Examples: typo T1; new admin filter T2; booking lock/payment webhook/large table migration T3. Record tier and rationale in plan/state; never fake an approval.

# AI Feedback Loop

Human review notes are exported as structured JSON so AI can help propose model changes without silently converting observations into rules.

## Rules

1. Observations are review input, not approved business rules.
2. Every proposed model change must trace to an equation, assumption, mapping or business rule.
3. Wooldridge-derived logic and Caisse extensions remain separate.
4. Calculated outputs are never changed merely to match reviewer expectations; discrepancies are explained first.
5. Any change altering scenario results requires regression tests.

## Intended loop

`Run scenario -> review result -> capture note -> export JSON -> AI proposes change -> human review -> branch/implementation/tests -> rerun scenario`

# rnd-005: gpt-6-luna reasoning effort (low / medium / high), 2026-11-21
Harder tasks with answer keys (answer-key.md). One run per arm.

| Effort | H1 bug-finder (7 bugs) | H2 security review (9 issues) | Tokens H1 + H2 | Time H1 / H2 |
|---|---|---|---|---|
| low | 6/7 (missed: update does not refresh recency) | 8/9 (missed CSRF) | 5,921 + 5,210 | 15 s / 12 s |
| medium | 6/7 (same miss) | 8/9 (missed CSRF) | 5,284 + 5,179 | 10 s / 12 s |
| high | **7/7** | **9/9** (+ rate limit, enumeration, validation) | 17,925 + 10,821 | 20 s / 30 s |

Finding: low and medium perform and cost the same; high finds the subtle bugs (Map re-insert order, CSRF) at about 2.5x the tokens.
Decision (CEO): bug-finder and code-reviewer -> effort high (a missed bug costs more than 15k tokens). backend-developer, refactoring-specialist, performance-optimizer stay medium.
Harness fix found during this run: Codex 'tokens used' parsing picked up '1.' from a numbered list when output was interleaved; regex now requires a number-only line. Ledger row corrected (1 -> 5,284).
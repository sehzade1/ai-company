# rnd-008: Claude Haiku vs Sonnet for reviews, 2026-11-22
Two review tasks with answer keys (answer-key.md): R1 Turkish copy vs spec (7 planted problems), R2 EN->TR translation spot-check (4 meaning errors + 1 correct sentence as a trap). One general-purpose subagent per model, no tools.

| Model | R1 found | R1 noise | R2 found | R2 false flags | Tokens | Time |
|---|---|---|---|---|---|---|
| Haiku | 7/7 | 0 | 4/4 | 0 | 53,673 | 12.5 s |
| Sonnet | 7/7 | 5 extra items (2 marked 'no fix needed', 3 subjective style notes) | 4/4 | 0 | 51,824 | 8.9 s |

Finding: for checklist-style reviews against a spec or a source text, Haiku is as accurate as Sonnet and its output is cleaner (no padding). Token use is almost the same because ~50k of each call is subagent context overhead, not the work; Haiku tokens are billed cheaper.
Decision (CEO): copy reviews and translation spot-checks -> Claude Haiku. Sonnet stays for directors, judgement calls and reviews without a clear spec.
Cost note: a Claude subagent costs ~50k tokens even for a 1-minute review. For short checks prefer Codex (gpt-6-luna, ~5-10k) or the local model when it is running; use Claude subagents when the job is large enough to amortise the overhead.
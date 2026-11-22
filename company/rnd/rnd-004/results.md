# rnd-004: model choice per role (Codex + Antigravity), 2026-11-21

Objective tasks with answer keys (answer-key.md, test-c2.js). Parallel run, 1 task per role per arm, so the sample is small.

## Codex (all at effort medium; real token counts)
| Model | C1 bug-finder (7 bugs) | C2 parseDuration (21 hidden tests) | Tokens C1+C2 | Time C1 |
|---|---|---|---|---|
| gpt-6-luna | 6.5/7 | 21/21 | 5,176 + 5,050 | 16 s |
| gpt-5.6-terra | 6/7 (wrong reasoning on empty reduce) | 21/21 | 10,247 + 6,235 | 20 s |
| gpt-5.6-luna | 6.5/7 | 12/21 (bug: every valid input throws) | 9,611 + 5,065 | 19 s |
No model explicitly named the non-empty reduce bug (object as initial accumulator); two gave a fix that covers it.

## Antigravity (tokens are chars/4 estimates; real quota use not visible)
| Model | A1 data (5 exact answers) | A2 TR translation (CEO score /5) | Time A1 / A2 |
|---|---|---|---|
| gemini-4-hydrogen-high | 5/5 | 4.8 natural, adds 'kahve kavurma' for clarity | 64 s / 55 s |
| gemini-4-neon-high | 5/5 | 4.7 | 80 s / 72 s |
| gemini-4-argon-high | 5/5 | 4.4 slightly awkward clause order | 112 s / 77 s |
| gemini-3.8-flash-medium | 5/5 | 4.0 over-formal, adds words not in source | 77 s / 63 s |
All 4 flagged the missing brand name instead of inventing it.

## Decision (CEO, small decision, no meeting needed per finance rule)
- Codex: all 5 roles -> gpt-6-luna, effort medium (best quality, about half the tokens of the others).
- Antigravity text roles (researcher, data-analyst, translator, technical-writer, accessibility-reviewer, 3d-modeler) -> gemini-4-hydrogen-high (best and fastest).
- Image roles unchanged (separate image model; not tested with --model).
- Fallbacks: Codex -> gpt-5.6-terra; Antigravity -> gemini-4-neon-high, then gemini-3.8-flash-medium for cheap bulk work.
## Follow-ups (backlog)
- Effort test: gpt-6-luna low vs medium vs high on bug-finder/code-reviewer with a harder task.
- Repeat with 3+ tasks per role before treating small gaps (hydrogen vs neon) as real.
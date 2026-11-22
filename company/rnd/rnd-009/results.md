# rnd-009: Gemini models, larger sample, 2026-11-22
4 more tasks with answer keys, 3 models, parallel run. G4 translation blind-scored by Codex gpt-6-luna.

| Model | G1 data (4) | G2 JSON extraction (traps: old order id, changed qty, cancelled item, relative date, second city) | G3 logic + arithmetic | G4 TR->EN (Codex blind) | Avg time |
|---|---|---|---|---|---|
| gemini-4-hydrogen-high | 4/4 | exact | 2/2 | 5 | 51 s |
| gemini-4-neon-high | 4/4 | exact | 2/2 | 5 | 66 s |
| gemini-3.8-flash-medium | 4/4 | exact | 2/2 | 5 | 55 s |

Combined with rnd-004 (2 tasks): all three models are equal on 6 objective tasks; the only measured differences are speed (hydrogen fastest in 5 of 6 runs here) and rnd-004's translation score (hydrogen 4.8, neon 4.7, flash 4.0, n=1). The 0.1 gap hydrogen vs neon in rnd-004 was noise.
Decision (CEO): keep gemini-4-hydrogen-high as default. Fallback order changes: gemini-3.8-flash-medium first (same accuracy, faster than neon, lighter model), then neon. Real per-call quota cost is still not visible from the CLI.
# rnd-010: does the systematic-debugging method help a worker model? 2026-11-22
Two bug reports that name one symptom while the code hides more root causes (D1 price formatting: padding + negative amounts; D2 memoize: key collisions, null/undefined, falsy results not cached, prototype keys, lost `this`). Fixes scored by 7 hidden tests each (test.js; reference fixes pass 7/7, originals 1/7). Gemini gemini-4-hydrogen-high, 2 runs per arm; the method arm got the full adapted SKILL.md text in the prompt.

| Arm | D1 | D2 | Prompt+answer tokens (est.) | Time |
|---|---|---|---|---|
| baseline | 7/7, 7/7 | 7/7, 7/7 | ~330-440 | 48-58 s |
| + systematic-debugging text | 7/7, 7/7 | 7/7, 6/7 (lost `this`) | ~2,730-2,870 | 58-96 s |

Finding: no quality gain (the baseline was already at the ceiling); the method made prompts ~7x larger and runs ~50% slower, with one regression. The tasks may be too easy for this model, so this does not show the method is useless, only that pasting it into worker briefs is not worth it.
Decision (CEO): keep the 8 adopted skills for Claude sessions (loaded only when triggered, no standing cost). Do NOT paste the method into Codex/Gemini briefs. Backlog: retest with harder, multi-file bugs and with a Claude worker.
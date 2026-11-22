# R&D experiment log

| ID | Date | Hypothesis | Variants | Samples | Quality (1-5) | Tokens/sample | Conclusion |
|---|---|---|---|---|---|---|---|
| rnd-000 | 2026-11-20 | Antigravity can produce image files | image-generator (generic) | 1 | 4 (matches brief; no transparency) | ~2.1k (est.) | Capability proven; baseline for specialisation tests |
| rnd-001 | 2026-11-20 | Type-specialised image briefs (logo / photo / illustration) raise acceptance vs generic image-generator | 3 types x 2 variants (generic vs rnd-image-logo/photo/illustration) | 1 per cell (6 valid + 6 wasted calls from a path-quoting bug in my harness) | Generic: A 3, B 4, C 2 (avg 3.0). Specialised: A 4, B 4, C 5 (avg 4.3) | generic ~1.31k, specialised ~1.56k (+19%); total spend ~17.7k incl. ~9.1k wasted first batch | Specialisation helps for logo and illustration (generic made an over-detailed logo and a photo instead of an illustration), no difference for photo. WEAK evidence (n=1). Proposal: split logo + illustration, keep photo on generic; see rnd\proposal-rnd-001.md |
| rnd-002a | 2026-11-20 | Logo: specialist brief vs generic vs single brief with type sections | 4 logo briefs x 3 variants, blind, 2 scorers (Claude + Codex) | 11 images (1 lost to quota) | generic 2.67 (0/3 accepted), specialist 4.0 (4/4), sections 4.0 (3/4) | unreliable (timeouts logged partial output); rnd-002 worker total ~24.7k incl. failures | image-logo promoted. Illustration arm failed: Antigravity image quota exhausted (429) by parallel calls; rerun sequentially after reset |
| rnd-003 | 2026-11-20 | Local Gemma 3 12B can replace Claude Haiku for cheap writing tasks | local vs Haiku, 3 tasks (translation, bulk descriptions, summary), Codex blind scorer | 1 per task | translation local 4.3 vs Haiku 3.7; bulk local 2.0 (wrote English) vs 5.0; summary local 3.3 vs 5.0 | local ~640 tokens total (free); Haiku subagent ~64k (mostly agent context overhead) | Hire local for translator-draft + private-worker; keep bulk/summary on Haiku. Follow-up: stronger language instruction may fix local bulk drafting |

## Backlog (candidate studies)
1. Split image-generator into specialists (logo/icon, photo-realistic, illustration, UI mockup assets) — does a specialised brief raise acceptance rate?
2. Transparent PNG pipeline (background removal post-processing) for logo/icon work — now also for local FLUX output.
6. Blind comparison: local-image (FLUX schnell) vs Antigravity image-logo / image-illustration (quality, speed, cost).
3. 3D modeler pilot (Blender headless) and whether to split into game-asset vs. product-render specialists.
4. Can Claude Haiku replace Sonnet for some reviews (copy, translation spot-checks) at acceptable quality?
5. Kimi pilot once logged in: translation and bulk drafting vs. current stand-ins.

- rnd-004 (2026-11-21) model per role, Codex + Antigravity: DONE -> gpt-6-luna (Codex), gemini-4-hydrogen-high (Antigravity text). See rnd\rnd-004\results.md. Follow-up: effort test, larger sample.
- rnd-005 (2026-11-21) gpt-6-luna effort: DONE -> high for bug-finder and code-reviewer (7/7, 9/9 vs 6/7, 8/9), medium elsewhere. See rnd\rnd-005\results.md.
- rnd-002b (2026-11-21) illustration arm: DONE -> no gain from specialist brief; image-illustration retired, image-generator handles illustrations; FLUX 0/3 for illustrations. See rnd\rnd-002b\results.md.
- rnd-006 (2026-11-22) transparent PNG pipeline: DONE -> tools\make-transparent.py (plain backgrounds only; --global for text logos). See rnd\rnd-006\results.md.
- rnd-007 (2026-11-22) 3D pilot: DONE -> Antigravity 3d-modeler 4.5/4.5, 2/2 first try; Codex 2.5/3.0, 1/2. 3d-modeler in production (script in reply, CEO runs Blender). See rnd\rnd-007\results.md.
- rnd-008 (2026-11-22) Haiku vs Sonnet reviews: DONE -> Haiku equal accuracy (7/7, 4/4), cleaner output; copy + translation reviews go to Haiku. Subagent overhead ~50k tokens either way. See rnd\rnd-008\results.md.
- rnd-009 (2026-11-22) Gemini larger sample: DONE -> all 3 models equal on accuracy (4 tasks); hydrogen fastest, stays default; fallback order flash then neon. See rnd\rnd-009\results.md.
- rnd-010 (2026-11-22) systematic-debugging text in Gemini briefs: DONE -> no gain at ceiling (base 28/28 vs method 27/28), ~7x prompt tokens; skills stay for Claude sessions only. See rnd\rnd-010\results.md.

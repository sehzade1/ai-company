# Directors' meeting — CEO decision (2026-11-20)

Participants: Engineering, Creative, Operations directors (Opus). Proposals: engineering.md, creative.md, operations.md.
Decision rule: majority where at least 2 directors assign the same role to the same model; in case of conflict, proven capability and cross-review rule.

## Proven facts (from probes)
- Codex sandbox is read-only: cannot write files, cannot run tests/builds. In author roles it produces a DIFF; Claude applies and tests it. (Write permission only with user approval.)
- Antigravity states it can write files, perform web research and cite sources, read images/PDFs, and has an image-generator subagent. Image generation is NOT PROVEN.
- Blender 5.1 is installed locally (C:\Program Files\Blender Foundation\Blender 5.1\blender.exe). No OpenSCAD. Node is available.
- No model has verified built-in image generation. Claude can generate visuals from code (SVG/PIL/three.js/Blender).

## Roster (5 roles per model)

| Model | Role | Director | Confidence | Reviewer (cross) | Fallback |
|---|---|---|---|---|---|
| Codex | backend-developer | Engineering | High | Claude security-auditor + test-writer | Claude Sonnet |
| Codex | refactoring-specialist | Engineering | High | Claude test-writer | Claude Sonnet |
| Codex | bug-finder (only on other models' code) | Engineering | High | Engineering Director (reproduces) | Claude Sonnet |
| Codex | performance-optimizer | Engineering | Medium | Claude test-writer (benchmark) | Claude Sonnet |
| Codex | code-reviewer (Claude/Antigravity code) | Engineering | Medium-High | Engineering Director | Claude Sonnet (if author is not Claude) |
| Claude | test-writer (only active model able to run tests) | Engineering | High | Codex code-reviewer | Codex (diff) |
| Claude | security-auditor | Engineering | High | Engineering Director | Codex code-reviewer |
| Claude | devops-ci | Engineering | Medium | Codex bug-finder | Codex (diff) |
| Claude | frontend-developer | Creative | High | Codex code-reviewer + Antigravity accessibility | Antigravity |
| Claude | ui-ux-designer | Creative | High | Antigravity accessibility + Creative Director | Antigravity |
| Antigravity | researcher | Operations | High | Operations Director (source check) | Claude Sonnet |
| Antigravity | data-analyst | Operations | Medium | Codex code-reviewer (calculation code) | Claude Sonnet |
| Antigravity | image-generator | Creative | Medium-High — pilot PASSED (no transparent background) | Creative Director (opens and inspects file) | Claude (code-based with SVG/PIL, limited) |
| Antigravity | 3d-modeler (Blender Python, headless) | Creative | Medium — MUST BE TESTED | Codex bug-finder (script) + Creative Director (render) | Claude Sonnet (Blender script) |
| Antigravity | accessibility-reviewer | Creative | Medium | Creative Director | Claude Sonnet (if author is not Claude) |
| Kimi | translator | Operations | Low — awaiting login | Operations Director (spot checks) | Antigravity |
| Kimi | technical-writer | Creative | Low — awaiting login | Claude (technical accuracy) | Antigravity |
| Kimi | copywriter | Creative | Low — awaiting login | Creative Director | Claude Haiku |
| Kimi | prompt-engineer (image/agent briefs) | Creative | Low — awaiting login | Creative Director | Claude Sonnet |
| Kimi | bulk-drafter (bulk drafts/content) | Operations | Low — awaiting login | Operations Director (spot checks) | Claude Haiku |

## Resolved disagreements
1. UI/UX: Engineering wanted Antigravity, two directors said Claude. Decision: Claude. Impartial review is provided by Codex code-reviewer + Antigravity accessibility.
2. Bug-finder: Operations proposed Kimi (not working yet). Decision: Codex (two directors), only on other models' code.
3. Test-writer: Codex cannot run tests. Decision: Claude.
4. Image/3D: all assigned to Antigravity, but a pilot test is mandatory before the first task. Without evidence, the role falls back to Claude's code-based backup.
5. Kimi: all 5 roles run with temporary stand-ins. No handover before passing 1 translation + 1 text pilot after login.
6. To avoid piling code review onto Claude, the code-reviewer role was given to Codex (for Claude's and Antigravity's code).

## Finance decisions
- Fallback is per role (table above). When a model is exhausted, at most 2 roles are handed over at the same time.
- Kimi is not included in any fallback list until it logs in.
- Soft budget for Claude and manual logging with `company.ps1 log`.
- Actual budget figures are awaited from the user. Codex numbers are actuals, others are estimates; be careful when comparing.

## Additional decision (CEO, per user request): TestSprite
TestSprite was attached to the Engineering Director as an external QA vendor; Claude test-writer uses it, and Codex code-reviewer can inspect test results. Credit tracking is with Finance. Cloud/tunnel usage depends on per-project user approval. No new agent slot was opened (5 roles per model is preserved).

## Additional decision (CEO, per user request, 2026-11-20): structure update
- Directors switched from Opus to Sonnet (price/performance). Opus is CEO only.
- R&D Department established (`director-rnd`, Sonnet). HR Manager (`manager-hr`, Haiku) and Finance Manager (`manager-finance`, Sonnet) are under the Operations Director.
- The '5 agents per model' rule was removed: the roster changes based on evidence. Adding/splitting/retiring a role: R&D pilot → R&D + HR + Finance price/performance meeting → CEO decision.
- R&D's first agenda: the backlog in rnd/experiments.md (first candidate: specializing the image generator by type).

## Additional decision: rnd-001 (price/performance meeting, 2026-11-20) — details: meeting\rnd-001-meeting.md
| Model | Role | Director | Confidence | Reviewer | Fallback |
|---|---|---|---|---|---|
| Antigravity | image-illustration (editorial/blog/cover illustration) | Creative | Medium (n=1, clear category difference) | Creative Director | Claude (code-based, limited) |
- image-generator is now: product/object photography + logo/icon (until rnd-002 concludes).
- image-logo: experimental (roles\antigravity\rnd-image-logo.md), not used in production.
- Routing: for ambiguous visual tasks, the Creative Director decides which role it goes to.
- rnd-002 follow-up pilot approved (36k cap), awaiting user's go-ahead to start.

## Additional decision: rnd-002 logo arm (CEO, 2026-11-20)
Blind scoring, two scorers (Claude Creative Director + Codex), 4 logo briefs:
| Variant | Avg. score | Accepted |
|---|---|---|
| image-generator (generic) | 2.67 | 0/3 |
| rnd-image-logo (specialist) | 4.0 | 4/4 |
| rnd-image-sections (single brief, sectioned) | 4.0 | 3/4 |
Decision: **image-logo promoted to production** (Antigravity, Creative, reviewer: Creative Director, fallback: Claude SVG). image-generator is now product/object photography + types without a specialist role. Final choice between rnd-image-sections and separate roles will be made after the illustration arm (the illustration arm will be re-run due to quota).
Note: token estimates are unreliable in this round (timed-out calls were logged with partial output); the decision is based on quality.

## Additional decision: Kimi removed (with user approval, 2026-11-20)
Reason: subscription does not include Kimi Code access (HTTP 403). Role files are kept under roles\_retired\kimi\. Stand-ins became permanent owners:
| Role | New owner | File | Reviewer | Fallback |
|---|---|---|---|---|
| translator | Antigravity | roles\antigravity\translator.md | Operations Director | Claude Haiku |
| technical-writer | Antigravity | roles\antigravity\technical-writer.md | Claude (technical accuracy) | Claude Sonnet |
| copywriter | Claude Haiku | worker-claude-copywriter | Creative Director | Claude Sonnet |
| prompt-engineer | Claude Sonnet | worker-claude-prompt-engineer | Creative Director | Antigravity |
| bulk-drafter | Claude Haiku | worker-claude-bulk-drafter | Operations Director | Antigravity |
The Kimi rows in the tables above are invalid.

## Additional decision: local model hired (CEO, rnd-003, 2026-11-20)
Agent `local` = Ollama + Gemma 3 12B (Q4_K_M, 100% GPU on RTX 3060). Free, no quota, data never leaves the machine, actual token count.
rnd-003 (Codex blind scoring, n=1): translation local 4.3 vs Haiku 3.7; bulk description local 2.0 (wrote in English) vs Haiku 5.0; summary local 3.3 (skipped details) vs Haiku 5.0.
| Model | Role | Director | Reviewer | Fallback |
|---|---|---|---|---|
| local | translator-draft (high-volume initial translation; Antigravity translator can do the final pass) | Operations | Operations Director | Antigravity translator |
| local | private-worker (tasks with personal/confidential data: masking, extraction, classification, short summary) | assigning director | assigning director | none — confidential data is not sent to the cloud; ask the user |
bulk-drafter and summaries remain with Claude Haiku.

## Additional decision: local image generation hired (CEO, 2026-11-21)
Agent `local-image` = ComfyUI 0.46.0 + FLUX.1-schnell fp8 (Apache-2.0), D:\AI\ComfyUI_windows_portable, RTX 3060. Free, no quota, data never leaves the machine, ~20-25 s/image.
Pilot (CEO review, n=1): logo 5/5 (text error-free, 2 colors, simple); illustration 3.5/5 (good style, but invented sign text despite 'no text' instruction — schnell does not follow negative prompts).
| Role | Primary | Fallback | Note |
|---|---|---|---|
| Logo / icon / emblem | Antigravity image-logo OR local-image (Creative Director chooses) | the other | local-image if many variants are needed (free) |
| Editorial illustration | Antigravity image-generator (rnd-002b) | local-image (check output if text-free is required) | |
| Product photography / other | Antigravity image-generator | local-image | |
| When Antigravity image quota is full | local-image | Claude code-based | Image work no longer stalls |
| Confidential/private images | local-image | — | Not sent to the cloud |
Open item (R&D backlog): blind comparison of local-image vs Antigravity; background removal for transparent PNGs.

## Reporting chain
Worker → respective Director (verifies, scores, summarizes) → CEO → user. Workers do not report directly to the CEO.

## Addendum 2026-11-21: model per role (rnd-004)
Role files now carry `model:` / `effort:` in frontmatter; company.ps1 passes them (`-m`/`-c model_reasoning_effort` for Codex, `--model`/`--effort` for Antigravity). `-Model`/`-Effort` on the command line override.
- Codex, all roles: gpt-6-luna, effort medium. Fallback gpt-5.6-terra.
- Antigravity text roles: gemini-4-hydrogen-high. Fallback gemini-3.8-flash-medium, then gemini-4-neon-high (rnd-009). Image roles unchanged.
Details: rnd\rnd-004\results.md
## Addendum 2026-11-21: Codex effort (rnd-005)
bug-finder and code-reviewer: gpt-6-luna effort high. Other Codex roles: medium. Details: rnd\rnd-005\results.md

## Addendum 2026-11-21: illustration arm (rnd-002b)
Generic image-generator 4.67, specialist 4.5-4.67, sections 4.5-4.67 (all 3/3 accepted, blind, 2 scorers); local FLUX 2.67-3.33 (0/3, invented text). image-illustration and rnd-image-sections retired; illustrations go to image-generator. image-logo stays. Antigravity quota: ~9 images per ~4.5 h. Details: rnd\rnd-002b\results.md

## Addendum 2026-11-22: 3D modeler (rnd-007)
Antigravity 3d-modeler passed (cup 4.5, chest 4.5, both ran first try) and is in production. It replies with a Blender script; the CEO runs Blender headless. Codex: fallback modeller and script reviewer. Details: rnd\rnd-007\results.md

## Addendum 2026-11-22: review model (rnd-008)
Copy reviews and translation spot-checks: Claude Haiku (same accuracy as Sonnet, cleaner). Sonnet: directors and spec-less judgement. Short checks: prefer Codex or local model over a Claude subagent (~50k overhead). Details: rnd\rnd-008\results.md

## Addendum 2026-11-22: Gemini fallback order (rnd-009)
hydrogen-high, neon-high and flash-medium tied on 4 more objective tasks; hydrogen fastest and stays default. Fallback order: gemini-3.8-flash-medium, then gemini-4-neon-high. Details: rnd\rnd-009\results.md

## Addendum 2026-11-22: adopted working-method skills (obra/superpowers) + rnd-010
Installed 8 adapted skills (brainstorming, systematic-debugging, test-driven-development, writing-plans, verification-before-completion, requesting/receiving-code-review, dispatching-parallel-agents); executing-plans skipped (depends on an uninstalled skill). rnd-010: pasting the debugging method into a Gemini brief gave no gain and ~7x prompt size, so the methods are for Claude sessions only. Notices: THIRD_PARTY_NOTICES.md.

## Addendum 2026-11-22: wshobson/agents (rnd-011)
wshobson review/security briefs on Codex scored 27/32 vs our briefs 29/32 with ~40% more tokens. Not adopted; used later as a catalogue for missing roles (cloud, incident response, observability, DB migration), each tested first. Details: rnd\rnd-011\results.md

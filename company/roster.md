# Roster (maintained by HR, Operations Director)

| Agent | Binary / type | Status | Roles |
|---|---|---|---|
| Claude Opus | main session | active | CEO |
| Claude Sonnet | subagents director-* | active | 4 Directors (Engineering, Creative, Operations, R&D) |
| Claude Sonnet | subagent manager-finance | active | Finance Manager |
| Claude Haiku | subagent manager-hr | active | HR Manager |
| Claude Sonnet | subagents worker-claude-* | active | test-writer, security-auditor, devops-ci, frontend-developer, ui-ux-designer |
| Codex 0.171.0 | %LOCALAPPDATA%\Programs\OpenAI\Codex\bin\codex.exe | active, read-only sandbox | backend-developer, refactoring-specialist, bug-finder, performance-optimizer, code-reviewer |
| Antigravity 1.2.14 | %LOCALAPPDATA%\agy\bin\agy.exe | active, can write files | researcher, data-analyst, image-generator (illustration + photo + other), image-logo (rnd-002), 3d-modeler, accessibility-reviewer. Image quota is separate and limited: one image call at a time, about 9 images then a ~4.5 h reset (rnd-002b); ~220 s per image |
| Kimi Code 2.7.2 | %USERPROFILE%\.kimi-code\bin\kimi.exe | RETIRED 2026-11-20 (roles moved: translator + technical-writer → Antigravity; copywriter + bulk-drafter → Claude Haiku; prompt-engineer → Claude Sonnet). Was: LOGGED IN, model K2.8 Preview set; BLOCKED: subscription has no Kimi Code access (HTTP 403 provider.auth_error, 2026-11-20 23:01). Needs a plan upgrade (kimi.com/code pricing). Earlier TLS/network errors resolved. Roles stay on stand-ins | translator, technical-writer, copywriter, prompt-engineer, bulk-drafter (on stand-ins) |

| Local: Ollama 0.40.13 + gemma3:12b | `company.ps1 delegate -Agent local` (REST 127.0.0.1:11434) | active; needs `ollama serve` running | translator-draft, private-worker. 3-7 s/task, free, real token counts. Note: registry.ollama.ai is blocked on this network; pull models via `ollama pull hf.co/<repo>:<quant>` |
| Local image: ComfyUI 0.46.0 + FLUX.1-schnell fp8 | `tools\comfy-generate.ps1 -Prompt .. -Out ..` (API 127.0.0.1:8188; start with `tools\start-comfyui.ps1`) | active | Logos (text renders well), fallback for Antigravity image quota, private images, many cheap variants. Ignores "no text" instructions in illustrations. ~20-25 s/image, free |
| TestSprite CLI 0.17.0 (vendor) | npm global `testsprite` | PENDING LOGIN (`testsprite setup`) | Cloud E2E/API tests, operated by Claude test-writer; credits tracked by Finance |



## Kimi stand-ins (until login + pilot)
translator → Antigravity · technical-writer → Antigravity · copywriter → Claude Haiku · prompt-engineer → Claude Sonnet · bulk-drafter → Claude Haiku

## Pilot tests
| Test | Status | Result |
|---|---|---|
| Antigravity image-generator: produce a PNG file | PASSED 2026-11-20 | 512x512 PNG of a flat blue rocket, inspected by CEO, matches brief. ~2.1k tokens. Limits: generator outputs 1024x1024 opaque JPEG; PNG/resize via local post-processing; no native transparency. |
| Antigravity 3d-modeler: headless Blender .glb + render | PASSED 2026-11-22 (rnd-007) | Cup 4.5, chest 4.5, both ran first try. Agent cannot write files headless: it replies with the script, CEO runs Blender. |
| Kimi translator + copywriter pilot | blocked (login) | |

## Tools available locally
Blender 5.1 (C:\Program Files\Blender Foundation\Blender 5.1\blender.exe), Node, Python 3.11 (Pillow, numpy, scipy). tools\make-transparent.py: plain-background removal for logos (rnd-006). OpenSCAD not installed.

## Performance notes
- 2026-11-20 Codex: self-reports strongest at backend, bugs, refactoring, tests; weak at DevOps, 3D, images. Read-only sandbox confirmed.
- 2026-11-20 Antigravity: self-reports web research with citations, image/PDF reading, image-generator subagent (unverified).

## Adopted skills
| Source | Skills | Date |
|---|---|---|
| obra/superpowers (MIT) | brainstorming, systematic-debugging, test-driven-development, writing-plans, verification-before-completion, requesting-code-review, receiving-code-review, dispatching-parallel-agents | 2026-11-22 |

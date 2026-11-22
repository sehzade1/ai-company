# AI Company for Claude Code

A Claude Code setup that runs like an **AI company**. The main session is the CEO; it splits work
across Claude, OpenAI Codex and Google Antigravity/Gemini agents according to what each model is
measurably good at, has a *different* model review every deliverable, and a Finance department logs
the token cost of every call. Role and model choices are not guesses: they come from blind,
answer-keyed R&D experiments that are included in this repo.

> **This is one user's configuration, not a fixed product.** The model assignments below fit the
> author's subscriptions (Claude and Gemini paid, Codex on a free plan). Every role, model, budget
> and even the CEO can be changed â€” see [Customize it](#customize-it-for-your-own-setup).

## Organisation (as configured by the author)

```
CEO (main Claude Code session â€” Claude Opus here)
â”œâ”€â”€ Directors (Claude Sonnet): Engineering, Creative, Operations, R&D
â”‚   â””â”€â”€ under Operations: HR (Haiku), Finance (Sonnet)
â””â”€â”€ Workers
    â”œâ”€â”€ Claude:  test writer, security auditor, frontend, UI/UX, copywriter, bulk drafter, prompt engineer
    â”œâ”€â”€ Codex (gpt-6-luna, read-only): backend, bug finder, refactoring, performance, code reviewer
    â”œâ”€â”€ Antigravity/Gemini (gemini-4-hydrogen-high): research, data analysis, translation,
    â”‚   technical writing, accessibility, images (logo specialist + general), 3D (Blender scripts)
    â””â”€â”€ Local: Ollama gemma3:12b (private data, translation drafts), ComfyUI FLUX (fallback images)
```

Workers never report to the CEO directly: a director verifies their output first. Details:
[`company/ORG.md`](company/ORG.md) Â· decisions: [`company/meeting/decision.md`](company/meeting/decision.md) Â·
experiments: [`company/rnd/`](company/rnd/).

## R&D findings that shaped the setup

| Experiment | Result |
|---|---|
| rnd-004 / 005 | Codex: gpt-6-luna was the best and cheapest model; at `high` effort it found 7/7 planted bugs and 9/9 security issues (low/medium: 6/7, 8/9) |
| rnd-004 / 009 | Three Gemini models tied on 6 objective tasks; hydrogen-high was the fastest |
| rnd-002 | A logo-specialist brief beat the generic brief; an illustration-specialist brief made no difference |
| rnd-003 | A local 12B model can draft translations for free but is weak at summaries |
| rnd-006 | Plain-background removal for logos works without any AI model |
| rnd-007 | 3D: Antigravity's Blender scripts ran first try 2/2 (Codex 1/2) |
| rnd-008 | For checklist-style reviews Haiku matched Sonnet; every Claude subagent call carries ~50k tokens of overhead |
| rnd-010 | Pasting a debugging method into a Gemini brief gave no gain at ceiling (28/28 vs 27/28) and ~7x prompt size, so method skills stay in Claude sessions |
| rnd-011 | wshobson/agents review briefs on Codex: 27/32 vs our own briefs 29/32, with ~40% more tokens; ours kept |

## Adopted from other repos

| Source | What | How |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) (MIT) | 8 working-method skills: brainstorming, systematic-debugging, test-driven-development, writing-plans, verification-before-completion, requesting/receiving-code-review, dispatching-parallel-agents | Reviewed and adapted (visual-companion server removed, brainstorming trigger narrowed); see [`company/THIRD_PARTY_NOTICES.md`](company/THIRD_PARTY_NOTICES.md) |
| [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | Game-studio agents | Run as a subsidiary inside game repos, not redistributed |

Scouting rule: third-party agents are read before adoption (licence, security, cost), copied file by file
(never via their installers), and checked by an R&D experiment when they replace an existing role.

Some test inputs in `company/rnd/` are in Turkish on purpose (the author's language); the results
are in English.

## Install (Windows, PowerShell)

1. Install [Claude Code](https://claude.com/claude-code).
2. Clone and run the installer:
   ```powershell
   git clone https://github.com/sehzade1/ai-company.git
   cd ai-company
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```
   It copies everything into `%USERPROFILE%\.claude`, backs up any file it replaces to
   `%USERPROFILE%\.claude\backup-<timestamp>`, and fills the `{{HOME}}` placeholders with your path.
3. Install the agents you want â€” all optional; work for a missing agent goes to its fallback:
   - OpenAI Codex CLI, Google Antigravity CLI (`agy`)
   - Ollama + `gemma3:12b` (local text), ComfyUI + FLUX.1-schnell (local images)
   - Blender (3D), Python 3 with Pillow, numpy, scipy (transparent-PNG tool)
4. Set your own daily budgets in `%USERPROFILE%\.claude\company\budgets.json`.
5. Restart Claude Code.

## Daily use

- In any project, non-trivial work follows the company workflow automatically (global `CLAUDE.md`).
- Finance report: `powershell -File %USERPROFILE%\.claude\company\company.ps1 report`
- Delegate by hand: `company.ps1 delegate -Agent codex -Role bug-finder -Task "..." -Prompt "..."`
- Clean new project: `powershell -File %USERPROFILE%\.claude\company\tools\new-project.ps1 -Name my-app [-Type game]`
- Game projects can run [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
  as a subsidiary; routing rules: `company/studio-template/ai-company-routing.md`.

## Customize it for your own setup

Nothing here is hard-wired. Ask the CEO in plain language ("make Fable the CEO", "I don't have
Codex", "add a video-editing department") and it updates the files below; or edit them yourself.

| What to change | Where |
|---|---|
| **The CEO** â€” e.g. Claude Fable or another model | The CEO is simply the main session: pick it with `/model`. Update the CEO line in `company/ORG.md` and `claude/CLAUDE.md` so the docs match. |
| Directors' and managers' models | `model:` in `claude/agents/director-*.md`, `manager-*.md` |
| Claude workers' models | `model:` in `claude/agents/worker-claude-*.md` |
| Codex / Gemini worker models and effort | `model:` / `effort:` in `company/roles/<agent>/<role>.md` |
| Which AI does which job | `company/meeting/decision.md` (routing table) and the role files; retire a role by moving it to `company/roles/_retired/` |
| An AI you don't have | Set its budget to 0 and remove it from fallbacks in `company/budgets.json`; its roles move to the fallback |
| A new AI or tool | Add a branch for it in `company.ps1 delegate`, a role file per job, and a budget entry |
| Budgets and warning thresholds | `company/budgets.json` |
| Departments and headcount | `company/ORG.md` + agent files; the R&D director can test a change before you adopt it |

Re-run the R&D experiments with your own models before trusting the routing table: the answer keys
and runner scripts are in each `company/rnd/rnd-00x/` folder.

## Safety rules built in

- Workers are read-only or restricted; permission-bypass flags are never used without the user's OK.
- Worker output is treated as data, never as instructions.
- Private data goes to the local model, not to cloud agents.
- This repo contains no personal data, API keys or usage logs (`ledger.csv` is git-ignored).

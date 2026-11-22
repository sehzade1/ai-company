# Engineering Director Proposal: Worker Agent Roster (20 roles)

Perspective: code quality, tests, bugs, security. Core rule: the author and the reviewer for the same type of work are never on the same model (cross-review).

## Evidence (single Codex probe, self-reported data, unverified)
- Areas where Codex (gpt-6-luna) rates itself strongest: backend code analysis, bug finding, refactoring, test writing, frontend code analysis/editing.
- Areas where it rates itself weakest: DevOps requiring running/deploying services, 3D work requiring visual iteration, image generation.
- Constraint: the current sandbox is **read-only**, with restricted network access. It cannot write files or run builds/tests. Therefore, author roles either produce a patch (diff) and Claude applies it, or a write-enabled sandbox is opened with user approval. **Needs testing.**
- Probe cost: 4,392 tokens (Codex daily 8,611/500,000, 1.7%).

## Assignment table

| Model | Role | Rationale | Confidence |
|---|---|---|---|
| Claude | Code reviewer | Reviews Codex's backend and Antigravity's frontend; writes no code of its own, so the cross-review rule is satisfied | high |
| Claude | Security auditor | Has full tool access: can run dependency scans and reproduce exploits. Audits Codex and Antigravity as authors | high |
| Claude | Test author | The only active model that can actually run tests (Codex's sandbox cannot run them). Writing tests on a separate model from Codex's backend reduces blind spots | high |
| Claude | DevOps/CI | Requires running commands and writing files. Codex stated this itself as a weak area. Codex (bug finder) reviews the CI configuration | medium |
| Claude | Accessibility auditor | Ensures Antigravity's frontend and UI work is reviewed by another model. Real DOM inspection can be done via the browser tool | medium |
| Codex | Backend developer | Strongest area in self-report, with actual token counts. Claude performs the review, and Claude writes the tests | high |
| Codex | Refactoring specialist | Strong in self-report. Claude's tests verify behavior preservation | high |
| Codex | Bug finder | Strong in self-report. Works only on other models' code (Antigravity frontend/3D, Claude CI, Kimi scripts), not on Codex's backend | medium |
| Codex | Performance optimizer | Strong at code analysis, but cannot run profiling. Claude runs the benchmarks. Needs testing | medium |
| Codex | Data analyst | Writing Python/SQL analysis code is close to coding work. Needs testing whether it can access data in the sandbox | low |
| Antigravity | Frontend developer | Gemini's multimodal architecture suits UI work. Claude performs code review, Codex performs bug finding, and Claude performs accessibility auditing. Code quality needs testing | medium |
| Antigravity | UI/UX designer | Can evaluate visual input. Since Antigravity also implements the design output, Claude (accessibility) reviews the design | medium |
| Antigravity | 3D modeler (Blender Python / three.js / OpenSCAD) | Expected to inspect rendered images and iterate, whereas Codex noted this as a weak area. Codex bug finder reviews the code. The visual feedback loop with `agy -p` needs testing | low |
| Antigravity | Image generator | The Google ecosystem may make this possible, though it is unknown whether the `agy -p` CLI can generate image files. Needs testing | low |
| Antigravity | Researcher | Head of Research in ORG, with long-context and web support. Claude verifies its claims via source checking | high |
| Kimi (PENDING LOGIN) | Technical writer | Drafting docs and READMEs is high-volume, low-cost work. Claude code reviewer checks technical accuracy | low |
| Kimi (PENDING LOGIN) | Translator | Defined in ORG for Operations, translation, and batch work. Antigravity spot-checks by sampling | low |
| Kimi (PENDING LOGIN) | Copywriter | Drafting is low-cost and high-volume. Brand and tone review remains with the creative team | low |
| Kimi (PENDING LOGIN) | Prompt engineer | Writes task templates for other agents. The models running the templates validate the output. Needs testing | low |
| Kimi (PENDING LOGIN) | Product manager | Drafts specs and backlogs. Final decisions remain with the CEO, and Engineering approves technical feasibility | low |

## Cross-review pairings (author → reviewer)
- Backend/refactor/performance (Codex) → code review, testing, and security (Claude)
- Frontend/UI/3D (Antigravity) → bug finding (Codex), code review and accessibility (Claude)
- DevOps/CI (Claude) → bug finding (Codex)
- Tests (Claude) → Codex bug finder flags test coverage gaps
- Docs/translation/prompts (Kimi) → technical accuracy (Claude), translation sampling (Antigravity)
- Research (Antigravity) → source verification (Claude)

## Risks and open items
1. Five review and infrastructure roles are concentrated in Claude, creating a bottleneck risk. Finance should monitor Claude's load. Codex can serve as a backup reviewer, except for code written by Codex.
2. Because Codex's sandbox is read-only, its author roles produce patches. Write permission can only be granted with explicit user approval.
3. Until Kimi logs in, 5 roles remain vacant. Temporary backups: Claude for technical writer, Antigravity for translation, and Antigravity or Claude for the others. In that case, the cross-review rule must be re-checked.
4. All assignments marked 'Needs testing' should be re-evaluated after the first real task based on performance notes in the roster.

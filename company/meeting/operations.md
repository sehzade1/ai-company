# Operations Directorate proposal: worker roster (20 roles)

Perspective: cost, work volume, research quality, accessibility, and budget balance.
Evidence: roster.md, ORG.md, budgets.json, and a single capability query made to Antigravity (2026-11-20). Antigravity's response is the model's own claim, not a verified test result.

## Antigravity probe (self-reported)
- Live web search is performed via `search_web` and provides URL sources (self-reported).
- Practical context window: it also stated 'unknown'. The long-context claim **must be tested**.
- Image and PDF reading is done with `read_file` (self-reported).
- Image generation is done via the `image-generator` subagent (self-reported). **Must be tested.**
- In CLI mode, it can write and edit files (self-reported). Therefore, the rule that the worker must remain read-only should be explicitly enforced.
- Weaknesses: CAPTCHA, sandbox limits, unverified estimation.
- Cost: 302 tokens (estimated, chars/4), 0.1% of the daily budget.

## Role assignment

| Model | Role | Rationale | Confidence | Fallback |
|---|---|---|---|---|
| Codex | Backend developer | Coding agent, runs in a sandbox, and reports actual token counts. Giving the largest volume to a measurable model is the healthiest choice for Finance. | high | Claude Sonnet |
| Codex | Test writer | Whoever writes the tests can run them in the same sandbox; high-volume and repetitive work. | high | Claude Sonnet |
| Codex | Refactoring specialist | Multi-file mechanical changes suit a coding agent. Claude performs the review (the author does not review their own work). | medium | Claude Sonnet |
| Codex | DevOps/CI | Script and pipeline file generation. The sandbox blocks actual deployments, which is operationally safe. | medium | Claude Sonnet |
| Codex | Performance optimizer | Running code is required to measure and compare. There may be benchmark constraints in the sandbox; **must be tested**. | medium | Antigravity |
| Claude (Sonnet/Haiku) | Frontend developer | Has all tools, file editing, and browser access; can also perform visual verification. | high | Codex |
| Claude (Sonnet/Haiku) | UI/UX designer | In ORG, Design & Docs is already under Claude; design skills are available. | high | Antigravity |
| Claude (Sonnet) | Code reviewer | Since Codex writes most of the code, review stays on a different model (cross-review rule). | high | Antigravity |
| Claude (Sonnet) | Security auditor | High-risk, low-volume work. The most reliable tool access is here, and a security-review skill is also available. | medium | Codex (read-only) |
| Claude (Sonnet) | Product manager | Decision-heavy work close to the CEO. Because its volume is low, the risk of unmeasured usage is small. | medium | Antigravity |
| Antigravity | Researcher | Has web search and source citation (self-reported); head of Research in ORG. Sources will still be checked by Operations. | high | Claude Sonnet (WebSearch) |
| Antigravity | Data analyst | Long document and PDF/image reading (self-reported), work close to research. Context limit is unknown; **must be tested**. | medium | Claude Sonnet (data skills) |
| Antigravity | Image generator | The only model among the 4 that claims to be able to generate images (`image-generator`, self-reported). | low (**must be tested**) | None: requires an external tool, or Claude handles image generation via SVG/code |
| Antigravity | 3D modeler (Blender Python / three.js / OpenSCAD) | Being multimodal, it can inspect render outputs itself. Balances Codex's load. | low (**must be tested**) | Codex |
| Antigravity | Accessibility auditor | Can inspect contrast and layout by reading screenshots; a different model from Claude, which writes the frontend. | medium | Claude Sonnet (design:accessibility-review) |
| Kimi (PENDING) | Translator | Head of Operations per ORG; batch work and translation are cheap volume work. Cannot be used until login. | low (**must be tested**) | Antigravity |
| Kimi (PENDING) | Copywriter | Draft and variation generation is high-volume and cheap work. Claude does the final polish. | low (**must be tested**) | Claude Haiku |
| Kimi (PENDING) | Technical writer | README and documentation drafts are batch work. Reduces Claude's unmeasured usage. | low (**must be tested**) | Claude Haiku |
| Kimi (PENDING) | Bug finder | Broad code scanning is volume work; Codex/Claude verify the findings. Code-reading quality is unknown. | low (**must be tested**) | Codex (read-only) |
| Kimi (PENDING) | Prompt engineer | Produces templates and brief drafts for other agents; low risk. | low (**must be tested**) | Claude Sonnet |

Distribution: 5 roles per model, 20 total. Coding volume is with Codex, decisions and reviews with Claude, research and multimodal work with Antigravity, and text volume with Kimi.

## (a) Temporary fallbacks until Kimi logs in

| Kimi role | Temporary fallback | Note |
|---|---|---|
| Translator | Antigravity | Budget usage is 0.1%, plenty of headroom. |
| Copywriter | Claude Haiku | Cheap and fast. Usage must be logged manually with `company.ps1 log`. |
| Technical writer | Antigravity | To avoid overloading Claude. Claude Sonnet does the final read-through. |
| Bug finder | Codex (read-only) | Token counts are actually measured. Claude verifies the findings. |
| Prompt engineer | Claude Sonnet | Low volume. |

Post-login step: Kimi is given a small pilot task (1 translation + 1 code scan). HR records the result in the roster; roles are only handed over after that.

## (b) Fallback rules when budget runs out
- Every role in the table has a 'Fallback' column. Rule: the fallback must not be the same model that reviews the work. If it is, review moves to a third model.
- An EXHAUSTED model should hand over at most 2 roles at a time to its fallback; otherwise the fallback model is pushed to the WARNING level. Remaining tasks are deferred and reported to the CEO.
- If Codex's budget runs out: coding tasks move to Claude Sonnet, and performance work moves to Antigravity.
- If Antigravity's budget runs out: research moves to Claude's WebSearch. There is no fallback for image generation; the task is deferred.

## (c) Notes on budgets.json
1. **Consistency issue:** The value 500000 represents actual tokens for Codex, and a chars/4 estimate for Antigravity and Kimi. The same number does not mean the same thing across these three models. Actual plan limits are unknown, and I am not making up numbers. The user should adjust them according to provider limits.
2. **Claude is unmeasured (0):** Having a model that carries 5 roles remain invisible is a blind spot for Finance. Suggestion: set an estimated 'soft' budget for `claude-sonnet` and log every subagent call with `company.ps1 log`.
3. **Kimi:** Without a login, 500000 is meaningless; its status should also be marked separately as 'pending'. Kimi is 2nd on Antigravity's fallback list—currently a non-working fallback.
4. **Loop risk:** Claude Sonnet's fallback is Codex, and Codex's fallback is Claude Sonnet. If both run out at once, work piles onto Antigravity. In addition, an agent-based fallback list can suggest Codex for non-code tasks (copy, design). Fallback selection should be role-based (the table above).
5. Warning thresholds (70/90) are reasonable.
6. Volume estimate (must be tested): Codex will carry the heaviest load (5 coding roles). Codex's limit should be reviewed before the others.

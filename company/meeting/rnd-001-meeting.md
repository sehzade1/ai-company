# Price/performance meeting — rnd-001 (2026-11-20)

Participants: R&D Director (proposal), HR Manager, Finance Manager. Decision: CEO.
Input: rnd\proposal-rnd-001.md, rnd\experiments.md, ledger.csv. The CEO personally reviewed the illustration pair (C1/C2).

## Votes
| Topic | R&D | HR | Finance | CEO decision |
|---|---|---|---|---|
| image-illustration separate role | Approve | Pilot-more | Approve | APPROVED |
| image-logo separate role | Approve | Pilot-more | Pilot-more | PILOT-MORE (rnd-image-logo remains experimental) |
| Specialist for photo | No split | — | Reject | REJECTED (image-generator remains for photo; rnd-image-photo archived) |
| Follow-up pilot rnd-002 | ~50k | Conditional approval | ~36k cap | APPROVED, 36k cap, with user's start approval |

## Rationale
- For illustration, the general role made a category error (photo instead of illustration + fabricated sign). This is not a difference in taste; the CEO confirmed. Cost per accepted deliverable ~3.9k → ~1.56k (verified by Finance via ledger). Structural cost: +1 role.
- The logo difference (3 vs. 4) is within the noise margin; a single sample is insufficient.
- The ~9.1k tokens spent due to R&D's script error are an experiment cost and are not attributed to the role.

## Implemented changes
- roles\antigravity\image-illustration.md was moved to production (the rnd draft was archived under _retired\).
- roles\_retired\antigravity\rnd-image-photo.md was archived.
- Routing rule (HR proposal): logo/icon/badge → image-generator (until rnd-002 concludes); editorial/blog scene, book/cover illustration → image-illustration; product/object photo → image-generator. If unclear, the Creative Director decides.
- Fallback: image-illustration → Claude (code-based, with the 'restricted' tag).

## rnd-002 terms (follow-up pilot)
Logo + illustration only; 4 briefs per type × 3 variants (general / specialist / type sections within a single brief) = 24 calls, ~36k token cap. Blind scoring: Creative Director + second scorer. If the third variant wins, there will be no need to split roles. Check `company.ps1 status` before starting.

## Finance note (CEO)
The management layer is expensive: in this meeting and pilot, Claude agents spent ~241k tokens (R&D ~100k, HR ~74k, Finance ~68k), while worker image calls spent ~17.7k. From now on, minor decisions should be made with a single manager or directly by the CEO; meetings are only for structural decisions.

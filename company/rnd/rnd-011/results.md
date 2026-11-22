# rnd-011: wshobson/agents role briefs vs our role briefs on Codex, 2026-11-22
Same tasks and answer keys as rnd-005 (H1: 7 planted bugs, H2: 9 security/reliability issues). Codex gpt-6-luna, effort medium (where our briefs had headroom). wshobson briefs (MIT, commit 12bcec7): comprehensive-review/code-reviewer for H1, comprehensive-review/security-auditor for H2, passed as the role brief. Note: wshobson's Codex packaging (.codex-plugin) ships skills only, not agents.

| Arm | H1 bugs found | H2 issues found | Tokens H1 / H2 |
|---|---|---|---|
| ours (bug-finder / code-reviewer) | 6/7 (+ 6/7 in rnd-005) | 9/9 (8/9 in rnd-005) | 4,885 / 5,567 |
| wshobson run 1 | 5/7 + 1 false positive (stored-undefined claim; entries are objects) | 8/9 (session fixation only in a footnote) | 6,286 / 11,248 |
| wshobson run 2 | 5/7 | 9/9 | 6,270 / 7,033 |

Both arms missed "update does not refresh recency" in H1; wshobson also missed the window boundary twice.
Totals over the same tasks: ours 29/32 (4 runs incl. rnd-005), wshobson 27/32 with ~40% more tokens.
Decision (CEO): keep our Codex role briefs. wshobson is not adopted as a subsidiary now; it stays a catalogue to hire from for roles we lack (cloud/Kubernetes, incident response, observability, database migration) when a project needs them, each checked like this first.
# Proposal rnd-001: Specialisation of the Antigravity image-generator role

Date: 2026-11-20 | Author: R&D Director | Evidence strength: WEAK (1 sample per cell)

## Hypothesis
A single general `image-generator` role produces inconsistent results across different job types (logo, product photo, editorial illustration); short briefs containing type-specific craft guidelines increase the acceptable output rate.

## Setup
- Same short brief, two variants: GENERIC (`image-generator`) and SPECIALISED (`rnd-image-logo`, `rnd-image-photo`, `rnd-image-illustration`). Production files were not touched.
- Briefs: A 'logo for Kuzey Kahve'; B 'matte black ceramic mug on a light grey studio background'; C 'autumn street scene with a small café, blog header'.
- Files were neutrally named (shuffled): A1=generic, A2=spec; B1=spec, B2=generic; C1=generic, C2=spec. Location: {{HOME}}\AppData\Local\Temp\claude\9519414f725d5b3e\010961af-914e-42f3-9dc3-0e3758650c0d\scratchpad\rnd-001\
- Scoring: each image was opened with Read; type fit, craftsmanship, usability without rework (1-5). Single scorer (R&D), knowing the mapping; risk of bias.

## Results
| Type | GENERIC score / tokens | SPECIALISED score / tokens | Notes |
|---|---|---|---|
| A Logo | 3 / 1181 | 4 / 1489 | Generic: compass+bean+steam, too much detail, illegible at 32px. Spec: flat background, 2 colours, simple cup+star, legible; star/cup intersection is a bit awkward |
| B Photo | 4 / 1234 | 4 / 1479 | Both are matte mug, clean studio; spec is slightly better centred with softer shadow. Negligible difference |
| C Illustration | 2 / 1513 | 5 / 1706 | Generic output photorealistic (not illustration) and added made-up 'LA PETITE PAUSE' text to the image; spec had consistent watercolour style, limited palette, space for header, no text |
| Average | 3.0 / 1309 | 4.3 / 1558 (+19% tokens) | |

Total spend ~17.7k tokens: 6 valid calls 8.6k + 9.1k wasted on the first attempt due to a file path quoting bug (all 6 images were written to the same file). The bug was in my harness, not a role failure; remained within the experiment budget (20k).

## Conclusion
Specialisation made a meaningful difference for logo and illustration; no difference was measured for photo. The spec brief is ~19% more expensive per call (longer brief + longer prompt/output) but reduces the need for rework.

## Recommendation
- SPLIT: `image-logo` and `image-illustration` (rnd- briefs can be promoted).
- DO NOT SPLIT: keep generic for photo (or `rnd-image-photo` only if justification for the extra cost emerges).
- Cheaper alternative: add type sections to the single image-generator brief instead of separate roles (zero management overhead). This was not tested; should be compared in the pilot.

## Estimated cost per accepted deliverable (score >=4 accepted)
- Before (generic): 1/3 accepted; ~3.9k tokens / accepted deliverable (roughly 1309 x 3).
- After (spec, 3 types): 3/3 accepted; ~1.56k tokens / accepted deliverable.
- If only logo+illustration are split: logo ~1.49k, illustration ~1.71k, photo ~1.23k.
- Caveat: with n=1, these rates are directional indicators, not statistics; acceptance rates will be more moderate in reality.

## Management overhead
+2 role briefs (roster, routing table, HR notes), Director's type-routing decision. Low; ~1 small file per brief.

## Requirements for the follow-up pilot
- At least 3-5 different briefs per type x 2 variants (~30-40 calls, ~50k tokens; requires CEO approval).
- Blind scoring (variant label hidden) and, if possible, a second scorer (Creative Director).
- Third variant: type sections within a single brief.
- Automated check for transparent PNG and 32px legibility for logo; counters for 'added text' and photo/illustration mix-up in illustration.
- Harness fix: file path quoting (no spaces in task name, no $ variables used in the prompt).

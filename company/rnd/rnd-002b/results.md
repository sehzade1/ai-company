# rnd-002b: illustration arm (rerun), 2026-11-21
4 briefs x 4 arms, sequential. Antigravity quota ran out after 9 images (reset ~4.5 h), so brief I4 has only the FLUX image; 12 images scored blind (shuffled ids, resized) by Claude and by Codex gpt-6-luna.

| Arm | Claude avg | Codex avg (raw) | Codex corrected | Accepted (>=4, Claude) | Time/image |
|---|---|---|---|---|---|
| image-generator (generic) | 4.67 | 3.83 | 4.67 | 3/3 | ~220 s |
| image-illustration (specialist) | 4.50 | 4.67 | 4.67 | 3/3 | ~235 s |
| rnd-image-sections | 4.50 | 4.67 | 4.67 | 3/3 | ~215 s |
| local FLUX schnell | 2.67 | 3.33 | 3.33 | 0/3 | ~20 s |

Codex correction: it failed I3 generic for 'letters on the hanging sign'; full-resolution crop (crop-X06-sign.jpg) shows both signs blank, so the hard-fail was overruled.
FLUX again rendered invented text ('COFFEE SHUP') and ignored 'isometric'; usable as a draft or fallback only.

Decision (CEO): illustration specialist gives no measurable gain over the generic brief with the current image model; retire image-illustration and the experimental rnd-image-sections (moved to roles\_retired). image-generator covers illustrations; image-logo stays (it did win in rnd-002a). FLUX stays for logos, quota fallback and private images, not for illustrations.
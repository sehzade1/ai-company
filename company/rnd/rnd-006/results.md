# rnd-006: transparent PNG pipeline, 2026-11-22
Tool: tools\make-transparent.py (Pillow + numpy + scipy, already installed in Python 3.11; no AI model, no network, <1 s per image).
Test: 3 FLUX logos (text logo, emblem, hard case with pale yellow/cream rays) + 1 spot illustration on a cream background. Checked on a checkerboard and on a dark background (preview.jpg, preview2.jpg).

| Image | Result |
|---|---|
| L1 text logo | Default: clean cut, but enclosed letter holes ('a', 'e') stay white. With --global: holes transparent (the cup's cream foam also becomes transparent). |
| L2 emblem | Clean; white sky inside the circle correctly kept. A faint grey ring at bottom-right is a drop shadow the generator drew despite 'no shadow' - not a tool fault. |
| L3 pale sun (hard case) | Pass: cream rays and white centre disk kept, only the outer background removed. |
| S1 spot illustration (cream bg) | Pass: background colour detected automatically (254,246,240), subject and ground shadow kept. |

Rule: logos with text -> add --global; emblems/illustrations with intended white areas -> default. Always add --crop. Check for generator-drawn shadows. Photos or busy backgrounds are out of scope (would need an AI matting model such as rembg; not installed).
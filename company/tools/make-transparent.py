"""Remove a plain background (white or any solid colour) from a logo/icon/spot illustration.

Usage:
  python -I make-transparent.py IN.png OUT.png [--tol 18] [--soft 40] [--global] [--crop] [--pad 24]

How it works (no AI model, no network):
  1. Background colour = median of the image border.
  2. Pixels close to that colour (distance < tol) that are CONNECTED to the border become transparent
     (enclosed areas such as the inside of an 'O' are kept). --global removes every close pixel instead.
  3. A soft edge band (tol..soft) next to the removed area gets partial alpha, and its colour is
     un-mixed from the background so no white halo remains on dark backgrounds.
  4. --crop trims to the visible content plus --pad pixels.
Prints a short report: background colour, % removed, output size.
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--tol", type=float, default=18.0, help="colour distance treated as background")
    ap.add_argument("--soft", type=float, default=40.0, help="distance where the soft edge becomes opaque")
    ap.add_argument("--global", dest="glob", action="store_true", help="remove all background-coloured pixels, not only border-connected")
    ap.add_argument("--crop", action="store_true")
    ap.add_argument("--pad", type=int, default=24)
    a = ap.parse_args()

    img = Image.open(a.src).convert("RGB")
    px = np.asarray(img).astype(np.float32)
    h, w, _ = px.shape

    border = np.concatenate([px[0], px[-1], px[:, 0], px[:, -1]])
    bg = np.median(border, axis=0)
    dist = np.sqrt(((px - bg) ** 2).sum(axis=2))

    close = dist < a.tol
    if a.glob:
        region = close
    else:
        # connected components of background-like pixels; keep those touching the border
        labels, _ = ndimage.label(close)
        edge_ids = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
        edge_ids = edge_ids[edge_ids != 0]
        region = np.isin(labels, edge_ids)

    # soft edge band: pixels within 2 px of the removed region
    reg_img = Image.fromarray((region * 255).astype(np.uint8), "L")
    near = np.asarray(reg_img.filter(ImageFilter.MaxFilter(5))) > 0
    alpha = np.ones((h, w), np.float32)
    band = near & ~region
    ramp = np.clip((dist - a.tol) / max(a.soft - a.tol, 1e-3), 0.0, 1.0)
    alpha[band] = ramp[band]
    alpha[region] = 0.0

    # un-mix background colour from semi-transparent edge pixels (removes halo)
    out = px.copy()
    semi = (alpha > 0) & (alpha < 1)
    aa = alpha[semi][:, None]
    out[semi] = np.clip((px[semi] - (1 - aa) * bg) / aa, 0, 255)

    rgba = np.dstack([out, alpha * 255]).astype(np.uint8)
    res = Image.fromarray(rgba, "RGBA")
    if a.crop:
        bbox = res.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        if bbox:
            l, t, r, b = bbox
            res = res.crop((max(l - a.pad, 0), max(t - a.pad, 0), min(r + a.pad, w), min(b + a.pad, h)))
    res.save(a.dst)
    removed = 100.0 * float(region.sum()) / (h * w)
    print(f"OK: {a.dst} {res.size[0]}x{res.size[1]} bg=rgb({int(bg[0])},{int(bg[1])},{int(bg[2])}) removed={removed:.1f}%")
    if removed < 5:
        print("WARNING: almost nothing removed - background may not be a plain colour", file=sys.stderr)
    if removed > 97:
        print("WARNING: almost everything removed - subject may match the background colour", file=sys.stderr)


if __name__ == "__main__":
    main()

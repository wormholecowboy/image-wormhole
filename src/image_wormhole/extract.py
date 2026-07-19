"""Alpha extraction: split a binary image into transparent RGBA mattes.

A thresholded image is separated into two complementary mattes — one keeping the
black pixels opaque, one keeping the white — with the other side made fully
transparent (alpha 0). Applied automatically after a threshold so variants drop
straight into a compositing tool without an extra step.
"""

from __future__ import annotations

import numpy as np

MIDPOINT = 128  # pixels >= midpoint are treated as "white"
SIDES = ("black", "white")


def to_rgba(gray: np.ndarray, keep: str) -> np.ndarray:
    """RGBA image keeping only `keep` ('black' or 'white') pixels.

    Kept pixels are opaque and rendered in their own colour (white or black);
    the other side is fully transparent (alpha 0).
    """
    white_mask = gray >= MIDPOINT
    mask = white_mask if keep == "white" else ~white_mask
    h, w = gray.shape[:2]
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    if keep == "white":
        rgba[..., :3] = 255  # visible pixels are white; black keeps RGB 0
    rgba[..., 3] = np.where(mask, 255, 0).astype(np.uint8)
    return rgba

"""Adaptive threshold sweep.

Where `threshold` compares every pixel to one global value, adaptive
thresholding compares each pixel to the mean/gaussian of its own local
neighborhood. That strips global shadows and uneven lighting, isolating flat,
high-contrast micro-texture and granular surface detail.

The look is dominated by two knobs, so we sweep a grid over both:
    - block: neighborhood size (locality scale) — small = fine grain, large = broad structure
    - C:     constant subtracted from the local mean — higher = cleaner, lower/negative = noisier
One variant is written per (block, C) combination.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from image_wormhole.image_io import ensure_readable
from image_wormhole.paths import variant_path

TECHNIQUE = "adaptive"

_METHODS = {
    "gaussian": cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    "mean": cv2.ADAPTIVE_THRESH_MEAN_C,
}


def block_sizes(values: list[int]) -> list[int]:
    """Coerce requested block sizes to what cv2 accepts: odd and >= 3.

    Even values are bumped up by one, sub-3 values clamped to 3, then the set
    is deduped and sorted so a sweep never emits collided or invalid blocks.
    """
    out = []
    for v in values:
        b = int(v)
        if b < 3:
            b = 3
        if b % 2 == 0:
            b += 1
        out.append(b)
    return sorted(set(out))


def apply_adaptive(
    gray: np.ndarray, method: str, block: int, c: int, invert: bool = False
) -> np.ndarray:
    """Adaptive threshold of `gray` for one (block, C) pair."""
    ttype = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    return cv2.adaptiveThreshold(gray, 255, _METHODS[method], ttype, block, c)


def variant_tag(method: str, block: int, c: int, invert: bool = False) -> str:
    """Filename tag encoding the params, e.g. 'gaussian_b031_c05' or '..._cm05'."""
    cstr = f"c{'m' if c < 0 else ''}{abs(int(c)):02d}"
    tag = f"{method}_b{block:03d}_{cstr}"
    if invert:
        tag += "_inv"
    return tag


def run(args: argparse.Namespace) -> int:
    src = Path(args.image)
    if not src.is_file():
        print(f"error: no such file: {src}")
        return 1

    readable = ensure_readable(src)
    if readable is None:
        print(f"error: could not convert image: {src}")
        return 1

    gray = cv2.imread(str(readable), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        print(f"error: could not read image: {src}")
        return 1

    blocks = block_sizes(args.block)
    cs = sorted({int(c) for c in args.const})
    if not blocks or not cs:
        print("error: no parameter combinations (check --block/--const)")
        return 1

    out_dir: Path | None = None
    written = 0
    for block in blocks:
        for c in cs:
            tag = variant_tag(args.method, block, c, args.invert)
            path = variant_path(src, TECHNIQUE, tag, out_root=args.out)
            out_dir = path.parent
            cv2.imwrite(str(path), apply_adaptive(gray, args.method, block, c, args.invert))
            written += 1

    print(f"wrote {written} adaptive variants -> {out_dir}")
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        TECHNIQUE,
        help="adaptive threshold sweep over local neighborhoods",
        description="Emit adaptive-threshold variants across a grid of block "
        "sizes and C constants. Each pixel is thresholded against its local "
        "neighborhood (mean or gaussian) rather than one global value — strips "
        "uneven lighting and isolates micro-texture and granular detail.",
    )
    p.add_argument("image", help="source image path")
    p.add_argument(
        "-b", "--block", type=int, nargs="+", default=[3, 7, 15, 31, 51],
        metavar="N",
        help="neighborhood block size(s), odd & >=3; even values are bumped up "
        "(default: 3 7 15 31 51)",
    )
    p.add_argument(
        "-C", "--const", type=int, nargs="+", default=[2, 5, 10],
        metavar="C",
        help="constant(s) subtracted from the local mean; higher = cleaner, "
        "negatives allowed (default: 2 5 10)",
    )
    p.add_argument(
        "-m", "--method", choices=["gaussian", "mean"], default="gaussian",
        help="local averaging method (default gaussian)",
    )
    p.add_argument(
        "--invert", action="store_true",
        help="invert output: foreground black on white",
    )
    p.add_argument(
        "-o", "--out", default="iw",
        help="output root dir (default iw/)",
    )
    p.set_defaults(func=run)

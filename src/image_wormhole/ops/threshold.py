"""Threshold sweep: emit N binary-threshold variants of one image."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from image_wormhole.paths import variant_path

TECHNIQUE = "threshold"


def threshold_values(count: int, low: int, high: int) -> list[int]:
    """Evenly spaced threshold points across (low, high).

    Endpoints are excluded because a threshold at 0 (all white) or 255 (all
    black) yields a degenerate, useless variant.
    """
    if count < 1:
        return []
    xs = np.linspace(low, high, count + 2)[1:-1]
    return sorted({int(round(x)) for x in xs})


def apply_threshold(gray: np.ndarray, value: int) -> np.ndarray:
    """Binary threshold: pixels > value -> white (255), else black (0)."""
    _, out = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    return out


def run(args: argparse.Namespace) -> int:
    src = Path(args.image)
    if not src.is_file():
        print(f"error: no such file: {src}")
        return 1

    gray = cv2.imread(str(src), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        print(f"error: could not read image: {src}")
        return 1

    values = threshold_values(args.count, args.min, args.max)
    if not values:
        print("error: no threshold values to apply (check --count/--min/--max)")
        return 1

    out_dir: Path | None = None
    for v in values:
        path = variant_path(src, TECHNIQUE, f"t{v:03d}", out_root=args.out)
        out_dir = path.parent
        cv2.imwrite(str(path), apply_threshold(gray, v))

    print(f"wrote {len(values)} threshold variants -> {out_dir}")
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        TECHNIQUE,
        help="sweep a binary threshold across N points",
        description="Emit N binary-threshold variants of a source image.",
    )
    p.add_argument("image", help="source image path")
    p.add_argument(
        "-n", "--count", type=int, default=20,
        help="number of threshold variants (default 20)",
    )
    p.add_argument(
        "--min", type=int, default=0,
        help="low end of threshold range, exclusive (default 0)",
    )
    p.add_argument(
        "--max", type=int, default=255,
        help="high end of threshold range, exclusive (default 255)",
    )
    p.add_argument(
        "-o", "--out", default="output",
        help="output root dir (default output/)",
    )
    p.set_defaults(func=run)

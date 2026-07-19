"""Threshold sweep: emit N binary-threshold variants of one image."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

from image_wormhole.extract import SIDES, to_rgba
from image_wormhole.image_io import ensure_readable
from image_wormhole.paths import variant_path
from image_wormhole.preprocess import add_blur_arg, apply_blur, blur_tag

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

    readable = ensure_readable(src)
    if readable is None:
        print(f"error: could not convert image: {src}")
        return 1

    gray = cv2.imread(str(readable), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        print(f"error: could not read image: {src}")
        return 1

    gray = apply_blur(gray, args.blur)
    btag = blur_tag(args.blur)

    values = threshold_values(args.count, args.min, args.max)
    if not values:
        print("error: no threshold values to apply (check --count/--min/--max)")
        return 1

    sides = SIDES if args.keep == "both" else (args.keep,)

    out_dir: Path | None = None
    written = 0
    for v in values:
        binary = apply_threshold(gray, v)
        for side in sides:
            tag = f"t{v:03d}_{side}{btag}"
            path = variant_path(src, TECHNIQUE, tag, out_root=args.out)
            out_dir = path.parent
            cv2.imwrite(str(path), to_rgba(binary, side))
            written += 1

    print(f"wrote {written} threshold variants -> {out_dir}")
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        TECHNIQUE,
        help="sweep a binary threshold across N points",
        description="Sweep a binary threshold across N points. Each threshold "
        "emits a transparent RGBA matte (kept side opaque, other transparent), "
        "ready to composite. Defaults to the black side; the white matte is its "
        "exact inverse — use --keep to change or get both.",
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
        "--keep", choices=["black", "white", "both"], default="black",
        help="which matte to write: black (default), white, or both "
        "(black/white are exact alpha inverses)",
    )
    p.add_argument(
        "-o", "--out", default=".",
        help="output root dir (default: current dir)",
    )
    add_blur_arg(p)
    p.set_defaults(func=run)

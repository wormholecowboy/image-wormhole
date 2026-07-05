"""B/W extractor: keep only the black or the white of a thresholded image,
making the other side fully transparent (RGBA PNG)."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

TECHNIQUE = "extract"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
MIDPOINT = 128  # pixels >= midpoint are treated as "white"


def extract(gray: np.ndarray, keep: str) -> np.ndarray:
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


def _sides(keep: str) -> list[str]:
    return ["black", "white"] if keep == "both" else [keep]


def _inputs(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(
            p for p in target.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS
        )
    return [target]


def run(args: argparse.Namespace) -> int:
    target = Path(args.target)
    if not target.exists():
        print(f"error: no such file or directory: {target}")
        return 1

    inputs = _inputs(target)
    if not inputs:
        print(f"error: no images found in {target}")
        return 1

    sides = _sides(args.keep)
    written = 0
    dests: set[Path] = set()
    for src in inputs:
        gray = cv2.imread(str(src), cv2.IMREAD_GRAYSCALE)
        if gray is None:
            print(f"skip: could not read {src}")
            continue
        # Default: an 'extract/' folder next to the input, so a batch stays grouped.
        out_dir = Path(args.out) if args.out else src.parent / TECHNIQUE
        out_dir.mkdir(parents=True, exist_ok=True)
        dests.add(out_dir)
        for side in sides:
            path = out_dir / f"{src.stem}_{side}.png"
            cv2.imwrite(str(path), extract(gray, side))
            written += 1

    where = str(dests.pop()) if len(dests) == 1 else f"{len(dests)} folders"
    print(f"wrote {written} extract variants -> {where}")
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        TECHNIQUE,
        help="keep only black or white of a thresholded image (transparent RGBA)",
        description="Extract the black or white regions of a thresholded/binary "
        "image into a transparent PNG. Accepts a file or a directory of images.",
    )
    p.add_argument("target", help="thresholded image file, or a directory of them")
    p.add_argument(
        "--keep", choices=["black", "white", "both"], default="both",
        help="which side to keep opaque (default both)",
    )
    p.add_argument(
        "-o", "--out", default=None,
        help="output dir (default: an 'extract/' folder next to each input)",
    )
    p.set_defaults(func=run)

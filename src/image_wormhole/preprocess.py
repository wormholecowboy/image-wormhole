"""Shared pre-processing applied to a source image BEFORE any technique runs.

Ops load their grayscale source, then route it through the pre-processing here
so knobs like `--blur` behave identically across threshold, adaptive and
extract. Each step is a no-op unless explicitly requested, so pixels and output
naming are unchanged when a flag is left at its default.
"""

from __future__ import annotations

import argparse

import cv2
import numpy as np


def add_blur_arg(parser: argparse.ArgumentParser) -> None:
    """Register the shared --blur flag on an op's parser."""
    parser.add_argument(
        "-b", "--blur", type=float, default=0.0, metavar="SIGMA",
        help="Gaussian blur applied before the technique runs; SIGMA is the "
        "blur strength (0 = off, default). Higher = softer.",
    )


def apply_blur(gray: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian-blur `gray` by `sigma`. sigma <= 0 returns the image unchanged."""
    if sigma <= 0:
        return gray
    # Reason: kernel size (0, 0) lets OpenCV derive the kernel from sigma.
    return cv2.GaussianBlur(gray, (0, 0), sigmaX=float(sigma))


def blur_tag(sigma: float) -> str:
    """Filename fragment recording the blur, e.g. '_g3' or '_g2p5'; '' when off.

    Keeps blurred and unblurred runs from overwriting each other's variants.
    """
    if sigma <= 0:
        return ""
    return f"_g{sigma:g}".replace(".", "p")

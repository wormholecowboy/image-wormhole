"""Implicit source normalization so OpenCV can decode any input.

cv2.imread cannot decode HEIC/HEIF (Apple's camera format). Rather than teach
every op about it, ops route source paths through `ensure_readable()` first:
HEIC/HEIF are transparently converted to a PNG (via macOS `sips`) and the
readable path is returned. Converted files land in a temp cache so source
folders stay clean; the original stem is preserved for downstream naming.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

HEIC_EXTS = {".heic", ".heif"}
# Formats cv2.imread decodes natively.
READABLE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
# Everything ops will accept as a source image.
IMAGE_EXTS = READABLE_EXTS | HEIC_EXTS

_CACHE = Path(tempfile.gettempdir()) / "image-wormhole-heic"


def ensure_readable(src: Path) -> Path | None:
    """Return a path cv2.imread can decode.

    Non-HEIC inputs pass through unchanged. HEIC/HEIF are converted to a cached
    PNG (reused if already converted). Returns None if conversion fails.
    """
    if src.suffix.lower() not in HEIC_EXTS:
        return src

    _CACHE.mkdir(parents=True, exist_ok=True)
    dst = _CACHE / f"{src.stem}.png"
    if dst.exists():
        return dst
    try:
        subprocess.run(
            ["sips", "-s", "format", "png", str(src), "--out", str(dst)],
            check=True, capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return dst

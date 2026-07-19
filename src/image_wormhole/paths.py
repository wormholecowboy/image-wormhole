"""Output path helpers implementing the variant folder layout.

Layout:
    <out_root>/<source-stem>/<technique>/<source-stem>_<tag>.<ext>
e.g. beach/threshold/beach_t120_black.png  (out_root defaults to the current dir)
"""

from __future__ import annotations

from pathlib import Path


def technique_dir(source: str | Path, technique: str, out_root: str | Path = ".") -> Path:
    """Return (and create) the folder that holds one technique's variants."""
    stem = Path(source).stem
    d = Path(out_root) / stem / technique
    d.mkdir(parents=True, exist_ok=True)
    return d


def variant_path(
    source: str | Path,
    technique: str,
    tag: str,
    out_root: str | Path = ".",
    ext: str = "png",
) -> Path:
    """Full path for a single variant, e.g. .../beach_t120_black.png."""
    stem = Path(source).stem
    return technique_dir(source, technique, out_root) / f"{stem}_{tag}.{ext}"

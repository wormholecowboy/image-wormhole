"""Output path helpers implementing the variant folder layout.

Layout (approved):
    <out_root>/<source-stem>/<technique>/<source-stem>_<tag>.<ext>
e.g. output/beach/threshold/beach_t120.png
"""

from __future__ import annotations

from pathlib import Path


def technique_dir(source: str | Path, technique: str, out_root: str | Path = "output") -> Path:
    """Return (and create) the folder that holds one technique's variants."""
    stem = Path(source).stem
    d = Path(out_root) / stem / technique
    d.mkdir(parents=True, exist_ok=True)
    return d


def variant_path(
    source: str | Path,
    technique: str,
    tag: str,
    out_root: str | Path = "output",
    ext: str = "png",
) -> Path:
    """Full path for a single variant, e.g. .../beach_t120.png."""
    stem = Path(source).stem
    return technique_dir(source, technique, out_root) / f"{stem}_{tag}.{ext}"

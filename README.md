# image-wormhole

CLI to batch-process photos into graphic-art variants for compositing in Affinity.

Generate many variations of a photo fast → review them in a viewer → drag the
chosen variant into Affinity for editing.

## Status

Early / iterative. First feature in progress: **threshold sweep** (apply a binary
threshold at ~20 points), followed by a **black/white extractor** and
**folder-structure organization** of generated variants.

See `.mem/roadmap.md` for the full feature roadmap.

## Setup

Requires [uv](https://docs.astral.sh/uv/). The project pins Python 3.12.

```bash
uv sync
```

## Usage

```bash
uv run wormhole --help
```

## Stack

Python CLI · OpenCV (opencv-python) · NumPy · Pillow. Wand/ImageMagick deferred
to backlog features.

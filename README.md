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

## Install (use anywhere)

Install as a system-wide command at `~/.local/bin/wormhole` (editable, so new
subcommands appear without reinstalling):

```bash
uv tool install --editable .
```

After adding a new dependency, resync the tool: `uv tool upgrade image-wormhole`.
Uninstall with `uv tool uninstall image-wormhole`.

## Usage

```bash
wormhole --help
wormhole threshold path/to/photo.jpg      # 20 binary-threshold variants
```

Variants are written under `output/` **relative to the current directory**, so
run `wormhole` inside the folder you want the results in.

During local development you can also run without installing: `uv run wormhole ...`.

## Stack

Python CLI · OpenCV (opencv-python) · NumPy · Pillow. Wand/ImageMagick deferred
to backlog features.

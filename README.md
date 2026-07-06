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

Install as a system-wide command at `~/.local/bin/iw` (editable, so new
subcommands appear without reinstalling):

```bash
uv tool install --editable .
```

After adding a new dependency, resync the tool: `uv tool upgrade image-wormhole`.
Uninstall with `uv tool uninstall image-wormhole`.

## Usage

```bash
iw --help
iw threshold path/to/photo.jpg      # 20 binary-threshold variants
iw adaptive path/to/photo.jpg       # grid of local adaptive-threshold variants
iw extract iw/photo/threshold/      # keep black/white as transparent PNGs
```

`adaptive` thresholds each pixel against its local neighborhood instead of one
global value, so uneven lighting is stripped and micro-texture / granular detail
survives. It sweeps a grid over `--block` (neighborhood size, odd & >=3) and
`-C/--const` (constant subtracted from the local mean), one variant per pair.
`--method gaussian|mean` (default gaussian), `--invert` for black-on-white.

`extract` takes a thresholded image or a folder of them and writes RGBA PNGs
(kept side opaque, other side transparent) into an `extract/` folder beside the
inputs. `--keep black|white|both` (default both).

Variants are written under `iw/` **relative to the current directory**, so
run `iw` inside the folder you want the results in.

During local development you can also run without installing: `uv run iw ...`.

## Stack

Python CLI · OpenCV (opencv-python) · NumPy · Pillow. Wand/ImageMagick deferred
to backlog features.

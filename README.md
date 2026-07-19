# image-wormhole

CLI to batch-process photos into graphic-art variants for compositing in Affinity.

Generate many variations of a photo fast → review them in a viewer → drag the
chosen variant into Affinity for editing.

## Status

Early / iterative. Working: **threshold sweep** (binary threshold at ~20 points,
auto-extracted to transparent black/white mattes) and **adaptive threshold**,
with **folder-structure organization** of generated variants.

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
iw threshold path/to/photo.jpg      # transparent black+white mattes per threshold
iw adaptive path/to/photo.jpg       # grid of local adaptive-threshold variants
```

`threshold` sweeps a binary threshold across ~20 points. Each threshold emits
**two transparent RGBA mattes** — one keeping the black pixels, one keeping the
white — with the other side fully transparent, ready to drop into a compositing
tool. Files land in `<stem>/threshold/<stem>_t###_<side>.png`.

`adaptive` thresholds each pixel against its local neighborhood instead of one
global value, so uneven lighting is stripped and micro-texture / granular detail
survives. It sweeps a grid over `--block` (neighborhood size, odd & >=3, `-k`) and
`-C/--const` (constant subtracted from the local mean), one variant per pair.
`--method gaussian|mean` (default gaussian), `--invert` for black-on-white.

Both ops accept `-b/--blur SIGMA` — a Gaussian blur applied before the technique
runs (0 = off); blurred variants get a `_g<sigma>` filename suffix.

Variants are written under `<source-stem>/<technique>/` **relative to the current
directory**, so run `iw` inside the folder you want the results in.

During local development you can also run without installing: `uv run iw ...`.

## Stack

Python CLI · OpenCV (opencv-python) · NumPy · Pillow. Wand/ImageMagick deferred
to backlog features.

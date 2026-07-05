## goals
- [project] image-wormhole: CLI to batch-process photos into graphic-art variants for compositing in Affinity
- [workflow] generate many variants fast → review in a viewer → drag chosen variant into Affinity for editing
- [source] input is heavily processed photos, often used for texture/shapes; frequently composited
- [process] build iteratively, start small, minimal upfront planning
- [roadmap] full feature roadmap (now + backlog + libs) → .mem/roadmap.md

## arch
- [stack] Python CLI
- [libs] OpenCV (opencv-python), NumPy, Pillow (PIL), Wand (ImageMagick)
- [output] variants auto-organized into a structured folder layout as created
- [output-layout] APPROVED: iw/<source-name>/<technique>/<source-name>_<tag>.png; threshold tag = t### (zero-padded threshold value). Default out root renamed output/→iw/ 2026-07-05.
- [output-layout-chained] SECONDARY ops (operate on existing variants, e.g. extract) write to a sibling <technique>/ folder NEXT TO their inputs (keeps a batch grouped for review), not a fresh iw/<source>/ tree. Entry ops (threshold) create iw/<source>/<technique>/.

## decisions
- [picker] iterfzf chosen for CLI picker (bundles fzf binary, pip-installable — no system fzf needed). Text-only, no image thumbnails → pair with an external viewer for eyeballing variants.
- [heic] HEIC/HEIF support = implicit conversion (not native decode, not a `convert` subcommand). Ops route source through image_io.ensure_readable() before cv2.imread; passes non-HEIC through, converts HEIC→PNG via macOS `sips` into a temp cache (reused). Original stem/parent preserved for output naming. src/image_wormhole/image_io.py owns HEIC_EXTS + shared IMAGE_EXTS.

## deploy
- [deploy] install per-machine via `uv tool install --editable .` → shim at ~/.local/bin/iw (a launcher script, NOT a compiled binary; runs the entry point in a uv-managed venv). MUST be run once on EACH machine. Editable: code edits live immediately; only NEW DEPS need `uv tool upgrade image-wormhole`. Output dir relative to cwd. Uninstall: `uv tool uninstall image-wormhole`.
- [deploy-state] shim INSTALLED on current machine (git user wormholecowboy) as of 2026-07-05. Other machine: install separately when used.

## gotchas
- [py] system Python is 3.14 (no reliable opencv-python wheels); project venv pinned to 3.12 via .python-version. Use `uv run`, never system python.
- [heic] `sips` is macOS-only. Both user machines are macOS so fine; a non-mac host would need a fallback (e.g. pillow-heif). Missing sips → op prints skip/error and continues, doesn't crash.
- [shim] `iw` bare command needs ~/.local/bin on PATH; in non-interactive/CI shells it may not be — use `uv run iw ...` there.

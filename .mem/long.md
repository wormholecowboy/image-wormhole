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
- [output-layout] <source-stem>/<technique>/<stem>_<tag>.png; threshold tag = t### (zero-padded threshold value). Default out_root = "." (cwd, not "iw/") since 2026-07-19. No iw/ prefix.
- [arch] Extraction is now DEFAULT post-step of threshold (not a standalone command). Writes a SINGLE transparent RGBA matte per threshold — black by default, `--keep black|white|both` to change (black/white are exact alpha inverses, so both is rarely needed). Shared logic in src/image_wormhole/extract.py (to_rgba). adaptive still emits OPAQUE binary — auto-extract scoped to threshold only; extend to adaptive is a candidate.
- [arch] Shared pre-processing pattern: src/image_wormhole/preprocess.py holds cross-op flags (blur now) applied to gray right after load; each op calls add_blur_arg(p) in add_parser and apply_blur/blur_tag in run. Home for future shared pre-steps.

## decisions
- [picker] iterfzf chosen for CLI picker (bundles fzf binary, pip-installable — no system fzf needed). Text-only, no image thumbnails → pair with an external viewer for eyeballing variants.
- [heic] HEIC/HEIF support = implicit conversion (not native decode, not a `convert` subcommand). Ops route source through image_io.ensure_readable() before cv2.imread; passes non-HEIC through, converts HEIC→PNG via macOS `sips` into a temp cache (reused). Original stem/parent preserved for output naming. src/image_wormhole/image_io.py owns HEIC_EXTS + shared IMAGE_EXTS. (threshold + adaptive route src through ensure_readable.)

## deploy
- [deploy] install per-machine via `uv tool install --editable .` → shim at ~/.local/bin/iw (a launcher script, NOT a compiled binary; runs the entry point in a uv-managed venv). MUST be run once on EACH machine. Editable: CODE edits live immediately, but RENAMING the console-script (pyproject `[project.scripts]`) does NOT — the old executable name persists until `uv tool install --force` (or upgrade). Only NEW DEPS also need resync. Output dir relative to cwd. Uninstall: `uv tool uninstall image-wormhole`.
- [deploy-gotcha] wormhole→iw rename: tool kept exposing old `wormhole` executable; `iw` was never created until `uv tool install --editable . --force` on 2026-07-05 (2nd time). Verify a script rename with `uv tool list` (shows exposed executables) after reinstall.
- [deploy-state] `iw` shim CONFIRMED installed+on-PATH on current machine (git user wormholecowboy) as of 2026-07-05 after --force reinstall. ~/.local/bin already on PATH. Other machine: install separately when used.

## gotchas
- [py] system Python is 3.14 (no reliable opencv-python wheels); project venv pinned to 3.12 via .python-version. Use `uv run`, never system python.
- [heic] `sips` is macOS-only. Both user machines are macOS so fine; a non-mac host would need a fallback (e.g. pillow-heif). Missing sips → op prints skip/error and continues, doesn't crash.
- [shim] `iw` bare command needs ~/.local/bin on PATH; in non-interactive/CI shells it may not be — use `uv run iw ...` there.

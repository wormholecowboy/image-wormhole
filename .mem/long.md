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
- [output-layout] APPROVED: output/<source-name>/<technique>/<source-name>_<tag>.png; threshold tag = t### (zero-padded threshold value)

## gotchas
- [py] system Python is 3.14 (no reliable opencv-python wheels); project venv pinned to 3.12 via .python-version. Use `uv run`, never system python.

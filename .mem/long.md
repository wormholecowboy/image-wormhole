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

## gotchas
- [git] cwd is NOT a git repo; .mem/ rooted at project dir /Users/briangildea/things/myc/image-wormhole

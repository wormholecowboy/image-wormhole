# Image-Wormhole — Feature Roadmap

CLI to batch-process photos into graphic-art variations. Generate many variants
fast → review in a viewer → drag chosen variant into Affinity for editing.
Source material: heavily processed photos, often for texture/shapes, frequently
composited. Build iteratively, minimal upfront planning.

## Now (first build)
1. **Threshold sweep** — apply binary threshold at ~20 threshold points across an
   image; emit one variant per threshold level.
2. **Black/White extractor** — from a thresholded image, extract only the black
   region OR only the white region (isolate one side of the binary result).
3. **Folder organization** — auto-organize all generated variants into a
   structured folder layout as they are created (critical for review workflow).

## Backlog — Creative Processing Techniques
4. **Adaptive Thresholding** — ✅ DONE (`iw adaptive`). Evaluate pixel brightness
   relative to small local neighborhoods. Strips global shadows / uneven lighting
   to isolate flat, high-contrast micro-textures and granular surface detail.
   → `cv2.adaptiveThreshold`. Sweeps a block×C grid; --method gaussian|mean,
   --invert.
5. **Canny Edge Detection** — infer sharp structural gradients, compress to clean
   single-pixel-wide lines. Strips color + texture → geometric, blueprint-like
   skeleton. → `cv2.Canny`
6. **Contour Vectorizing** — trace outer perimeters + island boundaries of shapes
   in thresholded images. Translate to precise X/Y coords → redraw as wireframes
   or export as clean vectors. → `cv2.findContours`
7. **Distance Transforms** — measure how far every foreground pixel sits from the
   nearest background edge → smooth, organic, luminous gradients. Turn 2D
   silhouettes into 3D heightmaps, displacement sources, chrome/metallic
   textures. → `cv2.distanceTransform`
8. **Pixel Sorting & Glitch Art** — target columns/rows of raw pixel arrays,
   reorder by hue / saturation / brightness. Controlled digital artifacts:
   melting, bleeding, liquid dragging textures. → NumPy array ops

## Backlog — Review / Picker
9. **`pick` command** — fzf-style picker to browse/select generated variants from
   the CLI. Use **iterfzf** (bundles the fzf binary, pip-installable). Text-only
   (no thumbnails) → pair with an external image viewer to eyeball variants
   before dragging into Affinity.

## Libraries
- **OpenCV (opencv-python)** — core CV engine: adaptive threshold, Canny,
  contour tracing, distance transforms. High-performance native algorithms.
- **NumPy** — images as multi-dimensional matrix arrays; fast pixel math,
  contrast-boundary selection, pixel-sorting algorithms.
- **Pillow (PIL)** — asset prep, color-space transforms, crop, save to
  PNG/TIFF design formats.
- **Wand** — Python wrapper for ImageMagick; complement custom pipelines with
  halftones, artistic distortions, deep channel blending.

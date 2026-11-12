# Figure and annotation plan

**Licence situation is better than last time.** The preprint is **CC BY 4.0**, so original figures may be annotated directly and shown — no redraw needed, provided each caption carries: description → source (title + DOI) → "annotations by the reviewer" → "CC BY 4.0". The previous post had to redraw because bioRxiv served that paper under CC BY-NC-ND.

## Capture list

| # | Figure | Panels needed | Role in the post | Annotation |
|---|---|---|---|---|
| F1 | **Fig 2A** — ESMFold2 architecture | whole panel | §2.3 anchor | ①–⑤ circled markers + colour boxes on: frozen ESMC, pooled→pair arrow, trunk loop arrow, diffusion transformer, confidence outputs. Handwritten "from ESMFold" on the pooling arrow, "from AF3-style diffusion" on the atom head |
| F2 | **Fig 2B** — scaling of structure prediction vs LM FLOPs | both sub-panels | §3.3 | Mark the two fit lines with their equations and R²; circle the 6B end point |
| F3 | **Fig 2C** — benchmark pass rates | whole panel | §3.1 | Box ESMFold2 single-sequence vs AF3-with-MSA; arrow labelled "MSA 없이" |
| F4 | **Fig 2D** — sample scaling | whole panel | §3.2 | Mark 1 → 1000 seeds, 49% → 65%; circle where Fast meets ESMFold2 |
| F5 | **Fig 2E** — latency vs length | whole panel | §3.4 | Mark L = 1024 with 15.8 s / 9.4 s; handwritten "single H100 · MSA 검색 제외" |
| F6 | **Fig 1A/1B** — ESMC latent space + P@L-LR scaling | 1B at least | §2.1 | Mark the development-run fit and the 6B extrapolation residual |
| F7 | **Fig 3A** — binder hit rates | left + right | §3.5 | Mark the two compute cohorts; circle the one pair that did not improve |
| F8 | **Fig S13** — loops × diffusion steps sweep | whole | §3.2 (margin thumbnail) | Mark the 10-loop/68-step default and the 64-loop tail |
| F9 | **Fig 5A** — Atlas sources | whole | §3.6 (margin thumbnail) | none beyond a label |
| P1 | ESMFold trunk figure from the **previous post's** assets | — | §2.3 gallery, "from ESMFold" vertex | reuse as-is, keep that post's licence line |

## How to capture (same method as the previous post)

bioRxiv serves figures lazily, so:
1. Open `…v1.full` in Chrome, find the figure's `<img>`, and set its CSS to a fixed large box (`width: 1700px; height: 800px; object-fit: contain`) so the full panel is laid out.
2. Move the cursor off the image (hover tooltips otherwise appear in the capture).
3. Take a `screenshot` first (the frame/viewport coordinates only line up after one), then `zoom` the region `[0, 0, ~1440, ~680]` at scale 1 with `save_to_disk`.
4. Saved under `/tmp/claude-tool-results/<session>/` → copy into `imgs/` with the names above.
5. Full-resolution alternative worth trying first: the `…/early/2026/06/04/2026.06.03.729735/F2.large.jpg` form, and `…/embed/graphic-N.gif` for inline equations (that pattern was confirmed in the page source).

## Annotation toolchain (already working)

- Python + PIL, font `/home/claude/fonts/NanumPenScript-Regular.ttf` (handwritten look).
- The font has **no** ①, ✓, →, ·, or em dash — draw circled numbers as a circle + digit, arrows as polygons, and avoid those glyphs in memo text.
- Marker colours: reuse `--mk1..--mk4` from `assets/review.css` and add a fifth for ⑤; keep the same colour per marker across figure, text highlight and code badge.
- Charts that are easier to redraw than to crop (e.g. a combined scaling panel for the 🤔 presentation critique) go to SVG built from the numbers in `_numbers.md`, labelled "redrawn by the reviewer from the figures' values".

## Code excerpts to copy into `code/`

From `/home/claude/biohub/esm` at `fddac93`, with `LICENSE-esm.txt` (MIT) alongside, as in the previous post:

| File to stage | Lines the post shows |
|---|---|
| `esmfold2_layers_shim.py` (excerpt of `esm/models/esmfold2/layers.py`) | L2261–2298 |
| `esmfold2_model_loop.py` (excerpt of `esm/models/esmfold2/model.py`) | L492–520, L734–738, L794–862 |
| `esmfold2_config.py` | L191–225, L300–329, L425–456 |
| `esmc_config.py` | L95–110 |
| `models_constants.py` | L10–18 |

Keep each staged file to the excerpted span plus a header comment naming repo, commit and licence, so `#code-panel(read(...))` line numbers stay stable.

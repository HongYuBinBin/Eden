# Figure–Text–Code triangulation plan

Markers ①–⑤, each with its own colour, used identically on the figure, in the quoted text and on the code panel. Code lines verified in `/home/claude/biohub/esm` at commit **`fddac93`** (MIT, Chan Zuckerberg Biohub).

The anchor figure is **Fig 2A** (ESMFold2 architecture diagram, CC BY 4.0 — annotate it directly).

## Mapping table (goes under the figure gallery in §2)

| Marker | Component | Figure location | Text (section · key phrase) | Code (file : lines) | Origin | Cross-check |
|---|---|---|---|---|---|---|
| ① | Frozen ESMC 6B encoder | Fig 2A, far left ("frozen" box) | A.2.1 · "passed independently to ESMC 6B" | `esm/models/esmc/config.py` L101–104; `esm/models/esmfold2/layers.py` L2339–2347 | from ESM C (and the all-layer trick from ESM-2/ESMFold) | 80 layers × d_model 2560 → 81 hidden-state tensors; matches the paper's `[B, L, Nlayers+1, Dlm]` |
| ② | Layer pooling + projection to pair space | Fig 2A, "pooled → pair" arrow | A.2.1 · "A learnable weight vector … combined via softmax" | `esm/models/esmfold2/layers.py` L2261–2298 (`LanguageModelShim`), weights at L2292 | from ESMFold, widened | `base_z_combine` is a single `[81]` parameter; softmax over layers, then `Linear(2560 → 256)`, then `SingleToPair` |
| ③ | Recurrent folding trunk (48 / 24 layers) + contractive update | Fig 2A, the loop arrow around the trunk | A.2.5 · "Constraining Ā to have eigenvalues in (0, 1)" | `esm/models/esmfold2/model.py` L492–496, L506–520, L734–738, L794, L860–862 | new (built on ref 40; module named `parcae`) | One line is the paper's whole update: `z = a * z + F.linear(injected_pair, b_mat)` (L861). Train T ~ Poisson(3) ∈ [1,6] ↔ `config.py` L209–216; inference `num_loops` default 20 ↔ L444 |
| ④ | Diffusion module → atoms | Fig 2A, right ("diffusion transformer", sliding-window atom attention) | A.2.6 · "truncated noise schedule that skips the very-high-noise regime" | `esm/models/esmfold2/config.py` L262–308; `layers.py` L1763–1827 (`DiffusionStructureHead`, `inference_noise_schedule`) | from AlphaFold3-style all-atom diffusion | 68 steps ↔ `inference_num_steps` L308; Karras power law p = 8, s_max 160, σ_data 16 |
| ⑤ | Confidence head | Fig 2A, "pLDDT / PAE / PDE" output | A.2.7 · "Four pair folding layers" | `esm/models/esmfold2/model.py` L96–151 (`ConfidenceHead`); `config.py` L318–329 | from AlphaFold2/3 | 4 layers ✓; 50 pLDDT / 64 PAE / 64 PDE bins; re-runs once per diffusion sample (`model.py` L408–412 docstring) |

Optional ⑥ if the MSA option gets its own paragraph:

| ⑥ | Optional MSA encoder | Fig 2A, dashed "MSA (optional)" input | A.2.4, A.2.5 · "the MSA is subsampled to 1024 sequences" | `esm/models/esmfold2/config.py` L191–205; `model.py` L529–535, L811–853 | new in this line (ESMFold had none) | `max_depth` 1024 ✓, `column_mask_rate` 0.1; code re-subsamples rows **every loop** (L811–814 comment), which the paper does not say |

## Cross-check findings (feed §2/§3 as 🤔 / 🤯)

1. **🤯 Recycling grew up.** ESMFold recycled 3 times with gradients only on the last iteration. ESMFold2 keeps the shape — Poisson(3) loops, gradients through the last 2 — but makes the update a discretised linear dynamical system so the loop can be unrolled to 64 at inference. The continuity is visible in one line of code (`model.py` L861) and one equation in A.2.5. Direct callback to the previous post.
2. **🤯 Width stayed, depth more than doubled.** ESM-2 3B was 36 layers at embed dim 2560 (verified in `facebookresearch/esm` README, model table); ESMC 6B is 80 layers at the *same* 2560 (`esmc/config.py` L102–104) — 2.2× the depth at identical width. The scale-up went into depth, which is also where the paper finds function information concentrating (layers 50–60).
3. **🤔 The code's defaults are not the paper's defaults.** `num_loops` defaults to 20 and `folding_trunk_num_hidden_layers` to 24 (`config.py` L433–444), i.e. the shipped config reads like ESMFold2-Fast with extra loops, while the paper quotes 48 layers / 10 loops for the headline model. Worth one sentence: a reader who pip-installs and runs the defaults is not reproducing Figure 2C.
4. **🤔 Hidden input corruption.** `DEFAULT_ESMFOLD2_FAST_LM_MASK_PCT = 0.1` (`constants/models.py` L17) and `lm_mask_pct` (`config.py` L453) mean the single-sequence checkpoints mask ~10% of residues *before* the language model, at inference, to match training-time corruption. Neither Figure 2A nor the main text mentions it.
5. **🤔 Dropout that stays on at inference.** `lm_encoder.lm_dropout = 0.25` with `per_loop_lm_dropout = True` (`config.py` L219–225), applied with `training=True` even under `eval()` (`model.py` L785–799), and `force_lm_dropout_during_inference` for binder-design loads (`config.py` L450–452). So the "deterministic" predictor is stochastic by design in the loop — which is plausibly part of why sampling 1000 seeds helps so much (Fig 2D).
6. **🤔 The Atlas is not the benchmarked model.** 1.1 billion structures came from `esmfold2-exp-2026-03` at 3 loops / 22 diffusion steps (A.5.2), far below the 10 loops / 68 steps the accuracy numbers use.
7. **Naming check.** The config refuses `num_recycles` and tells the caller ESMFold2 calls it `num_loops` (`config.py` L163–166) — a nice one-line sidenote on the vocabulary change from the previous post.

## Gallery plan for §2 (2–4 panels beside the main figure)

1. **Code panel A** — `LanguageModelShim` (`layers.py` L2281–2298), marker ②, highlight on the softmax line L2292; badge "②".
2. **Code panel B** — the loop body, trimmed: `model.py` L794, L860–862 with marker ③, highlight on L861, plus a margin memo "= the A.2.5 equation".
3. **Text panel** — the A.2.5 sentences on the contractive constraint, highlighted in ③'s colour (paraphrase in the post body; the panel shows the figure's own words only as a short marked phrase under 15 words).
4. **Prior-work panel** — the ESMFold trunk/recycling excerpt already captured in the previous post, labelled "from ESMFold (Lin et al. 2023)", so ③'s borrowed half is visible.

Cross-file arrows: `config.py` (`num_loops`, `folding_trunk_num_hidden_layers`) → `model.py` L492/L794, drawn with `gallery(links: …)`.

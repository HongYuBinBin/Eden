# Source sheet — ESMC + ESMFold2 review

Every claim in the post must trace to one row here. Read in the browser on 2026-11-12.

## Primary paper (the text vertex)

| Field | Value |
|---|---|
| Title | Language Modeling Materializes a World Model of Protein Biology |
| Authors | Salvatore Candido, Thomas Hayes, Alexander Derry, Roshan Rao, Zeming Lin, Robert Verkuil, … Tom Sercu, Alexander Rives (123 authors) |
| Venue | bioRxiv preprint (not peer reviewed) |
| Posted | June 04, 2026 |
| DOI | https://doi.org/10.64898/2026.06.03.729735 |
| Full text read | https://www.biorxiv.org/content/10.64898/2026.06.03.729735v1.full |
| **License** | **CC BY 4.0** (confirmed on the abstract page: "made available under a CC-BY 4.0 International license") |
| Figure reuse | **Annotate the original figures directly** — attribution + license line required. No redraw needed (contrast with the ESM-2/ESMFold post, where bioRxiv CC BY-NC-ND forced a redraw) |
| Structure | Abstract · Introduction · 5 result sections · Conclusion · Appendix A.1–A.6 · 5 main figures (Fig 1–5) + 48 supplementary figures (S1–S48) |

Appendix map (where the method vertex lives):
- A.1 ESM Cambrian — A.1.1 Architecture, A.1.2 Pretraining Data, A.1.3 Training Details, A.1.4 Evaluations
- A.2 ESMFold2 — A.2.1 Architecture, A.2.4 MSA Module, A.2.5 Recurrent Folding Layers, A.2.6 Diffusion Module, A.2.7 Confidence Head, A.2.8 Training Details, A.2.9 Data, A.2.10 Benchmark Results, A.2.11 Inference, A.2.12 Experimental Models
- A.3 Protein Design · A.4 ESMC Sparse Autoencoders · A.5 ESM Atlas · A.6 Safety and Model Release

## Code (the code vertex)

| Field | Value |
|---|---|
| Repository | https://github.com/Biohub/esm |
| Commit read | `fddac936fc921445da2d099a3e4f7ae928717292` ("Bump version to 3.4.3", 2026-11-09) |
| Package version | 3.4.3 |
| **License** | **MIT** — `LICENSE.md`, "Copyright 2026 Chan Zuckerberg Biohub, Inc." |
| Local checkout | `/home/claude/biohub/esm` (shallow, read-only) |
| Caveat to state in the post | The code is the November 2026 release line; the paper is the June 2026 preprint. Line numbers are quoted against the commit above, and that commit is named in every code caption. |

## Model cards / release pages

| Source | URL | Version | License |
|---|---|---|---|
| ESMFold2 model card | https://biohub.ai/models/esmfold2 | 2026-05 (page also shows 2026-04) | MIT |
| Release post | https://biohub.org/news/world-model-of-protein-biology/ | 2026-05-27 | — |
| Code model ids | `esm/utils/constants/models.py` L12–14 | `esmfold2-2026-05`, `esmfold2-fast-2026-05`, `esmfold2-2026-05-cutoff-2025` | MIT |
| Paper's own release statement | A.6 | — | Source + weights released for ESMC 6B, ESMFold2, ESMC SAEs; ESM Atlas and the binder design system released openly. ESMC 600M/300M weights were already open. |

**Licence wrinkle to note in one sidenote:** the Dec-2024 ESM Cambrian release carried a custom non-commercial licence on Hugging Face (`EvolutionaryScale/esmc-600m-2024-12`: "custom non-commercial license"; the 300M card said "custom open license"), while the 2026 Biohub release is MIT. Verify the current HF card before asserting anything about the 2024 weights.

## Prior work needed for "from …" origin notes

| Model | Why it is needed | Where to get the figure |
|---|---|---|
| ESM-2 / ESMFold (Lin et al. 2023) | The layer-pooling trick and the P@L-LR contact metric come straight from here; the paper cites it as (3) for representation extraction | Already captured in `content/posts/2026-11-12-esm2-esmfold/imgs/` — reuse, with the same licence line as that post |
| AlphaFold3 | The main baseline on every benchmark, and the source of the diffusion-to-atoms design | Link only; do not reproduce its figures (not reusable) |
| Rao et al. contact prediction | P@L-LR definition | Already captured in the previous post (`rao_fig1.jpg`) |
| Prairie et al. (ref 40) | The contractive/linear-recurrent update the trunk is built on; the code module is literally named `parcae` | Look up the reference in the preprint's reference list before writing §2 |

## Not to be reused

- Ramith Hettiarachchi's review (https://ramith.fyi/posts/2023-02-10-esm-2-…/) — format reference only. Credit in the footer; copy no sentence and no annotated image.
- Any AlphaFold3 / Chai-1 / Boltz figure.
- Photos of the authors or any person.

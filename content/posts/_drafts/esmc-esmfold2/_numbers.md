# Numbers sheet — verified against the sources

Rule: nothing goes in the post unless it appears here with a source. "P" = preprint section, "C" = code at commit `fddac93`.

## ESMC (the language model)

| Number | Value | Source |
|---|---|---|
| Model sizes | 300M / 600M / 6B parameters | P A.1.1 |
| Training sequences | ~2.8 billion (vs ~50 million for ESM-2 — close to two orders of magnitude) | P §"Accurate prediction…" intro paragraph |
| Data sources | UniRef, MGnify, JGI Metagenome | P A.1.2 |
| Objective | Masked language modeling | P §"A scaling law…" |
| ESMC 6B width | d_model 2560 | C `esm/models/esmc/config.py` L102 · also `esmfold2/config.py` L455 (`lm_d_model`) |
| ESMC 6B depth | 80 layers | C `esmc/config.py` L104 · `esmfold2/config.py` L456 (`lm_num_layers`) |
| ESMC 6B heads | 40 | C `esmc/config.py` L103 |
| Vocab | 64 | C `esmc/config.py` L101 |
| FFN expansion | 8/3, rounded to a multiple of 256 | C `esmc/config.py` L19, L31–33 |
| Hidden states exposed | 81 tensors = 80 layers + embedding, `[B, L, 81, D]` | C `esmfold2/layers.py` L2347 (docstring) |
| Scaling-law fit (development runs) | P@L-LR = 0.115 × log10(FLOPs) − 1.98, R² = 0.99 | P §"A scaling law…" |
| ESMC 6B final training compute | 1.63 × 10²³ FLOPs; residual from the extrapolation −0.007 P@L-LR | P §"A scaling law…" |
| Development sweep | five models, dimension 512 → 1536, trained past compute-optimality | P §"A scaling law…" |
| µP proxy model | d_model 512, n_layers 16 | P A.1.3 |
| Structure info peaks | later layers, peaking in the penultimate layer | P §"A scaling law…" |
| Function (EC) info peaks | layers 50–60; 100-NN classification over 8,493 proteins, 57 EC classes | P §"A scaling law…", A.1.4.2 |
| SAE probe data | 8 billion tokens across the three model sizes | P A.4.1 |

## ESMFold2 (the folding model)

| Number | Value | Source |
|---|---|---|
| Folding (pairformer) layers | 48 in ESMFold2, 24 in ESMFold2-Fast | P Fig 2A caption, A.2.1 · C `esmfold2/config.py` L433–435 (default 24) |
| LM-side pair encoder | 4 layers | P Fig 2A ("refined with a 4 layer encoder") · C `config.py` L219–223, `model.py` L497–505 |
| Coda layers before the diffusion head | 2 ("two final folding layers") | P Fig 2A · C `config.py` L209–214 (`parcae_num_coda_layers` = 2), `model.py` L518–520 |
| Pair width d_z | 256 | P A.2.1 ("linear projection from Dlm to dz = 256") · C `config.py` L429, `layers.py` L2268 |
| Single width | 384; per-residue input features 451 | C `config.py` L428, L430 |
| Atom-attention window | 128 | C `config.py` L432 |
| Loops: training | T ~ Poisson(mean 3), clamped to [1, 6]; gradients through the last 2 loops only | P A.2.5 · C `config.py` L209–216 (`poisson_mean` 3.0, `min_steps` 1, `max_steps` 6) |
| Loops: inference default | 10 loops (near-optimal); config default 20; scales out to 64 on antibody–antigen | P A.2.11 · C `config.py` L444 (`num_loops` = 20) |
| Diffusion steps | 68 (truncated schedule) default; baselines use 200 | P A.2.11, Fig 2 caption · C `config.py` L308 (`inference_num_steps` = 68) |
| Diffusion token blocks | 12 blocks, width 768, 16 heads; σ_data = 16 | C `config.py` L262–270 |
| Noise schedule | Karras power law, s_max 160, s_min 4e-4, p = 8 | C `config.py` L304–307, `layers.py` L1809–1827 |
| Confidence head | 4 pair folding layers; 50 pLDDT bins, 64 PDE, 64 PAE, 128 distogram bins | P A.2.7 · C `config.py` L318–329 |
| MSA module | optional; 4 layers, subsample to 1024 rows, column-mask rate 0.1; parser cap 16,384 | P A.2.4/A.2.5 · C `config.py` L191–205, `constants/models.py` L16 |
| Diffusion samples | 8 by default | C `config.py` L445 |
| Training cost | 256 H100 GPUs, 127 hours over 3 stages; ESMFold2-Fast 85 hours; ESMC backbone cast to FP8 | P A.2.8 |

## Results numbers (the ones the post must state)

Benchmarks: **FoldBench** (antibody–antigen, protein–protein; ±1σ over 200 bootstrap samples of 5 seeds from 25) and **Runs N' Poses** (protein–ligand; ±1σ over 200 bootstrap resamples). Pass rate = fraction with DockQ ≥ 0.23.

| Claim | Number | Source |
|---|---|---|
| ESMFold2, single sequence, antibody–antigen | 50% ± 2% | P §structure |
| AlphaFold3, **with** MSA, antibody–antigen | 47% ± 2% | P §structure |
| ESMFold2, single sequence, protein–protein | 70% ± 1% | P §structure |
| ESMFold2, single sequence, protein–ligand | 66% ± 1% | P §structure |
| ESMFold2 + MSA, antibody–antigen / protein–protein | 53% ± 2% / 76% ± 1% (AF3: 47% ± 2% / 73% ± 1%) | P §structure |
| ESMFold2 + MSA, 20 loops, antibody–antigen | 55% ± 2% | P §structure |
| ESMFold2-Fast (24 layers, no MSA) | 50% ± 2% AbAg, 68% ± 1% PPI, 63% ± 1% ligand | P §structure |
| Sample scaling, ESMFold2 AbAg | 49% (1 seed) → 65% (1000 samples); PPI 75% → 78% | P §structure, Fig 2D |
| Sample scaling, ESMFold2-Fast AbAg | 45% → 65% at 1000 seeds (ties the full model, without MSAs) | P §structure |
| Scaling law, monomer | LDDT = 0.027 × log10(FLOPs) + 0.181, R² = 0.92 | P §structure, Fig 2B |
| Scaling law, complexes | P(DockQ ≥ 0.23) = 0.060 × log10(FLOPs) − 0.832, R² = 0.93 | P §structure, Fig 2B |
| Latency, 1024 residues, 10 loops / 200 diffusion steps | ESMFold2 15.8 s (1.3× faster than AlphaFold3); ESMFold2-Fast 9.4 s | P §structure, Fig 2E |
| Latency conditions | **single H100 GPU; MSA construction time excluded**; Chai-1 excluded from the plot at 110 s for L = 1024 | P Fig 2E caption |

## Binder design (keep short — one subsection)

| Claim | Number | Source |
|---|---|---|
| Targets | 5: PDGFRβ, EGFR, PD-L1, CD45, CTLA-4 | P §design |
| Modalities | de novo minibinders and scFvs | P §design |
| Designs tested | 84 per target × modality × compute scale | P §design |
| Hit rates, higher-compute cohorts | 36–88% minibinders; 15–29% scFvs | P §design |
| Effect of more search compute | minibinders 53.8% → 70.0%; scFvs 12.1% → 21.0%; improved in 9 of 10 target–modality pairs | P §design |
| Search cost | minibinders ~15k / ~67k candidates ≈ 500 / 2,400 H100-hours; scFvs ~28k / ~117k ≈ 1,800 / 7,700 H100-hours; ranking ensemble 4 → 19 critics | P A.3 |
| Affinities | 68 pM to 70 nM by BLI | P §design |
| Function | PD-L1 minibinder / scFv IC50 1.6 nM / 39 nM vs 2.6 nM for an atezolizumab-derived scFv control | P §design |

## ESM Atlas (headline statistics only — the skill defers side outputs)

| Claim | Number | Source |
|---|---|---|
| Sequences mapped | 6.8 billion | P abstract, §atlas |
| Predicted structures | 1.1 billion | P abstract, §atlas |
| Sources | SPIRE, MGnify (grouped by biome) and others | P Fig 5A caption |
| Structures predicted with | `esmfold2-exp-2026-03`, 3 loops, 22 diffusion steps, step scale 2.0, noise scale 0.3 | P A.5.2 |

**Note the inconsistency to raise as 🤔:** the Atlas was built with an *experimental* March-2026 checkpoint at 3 loops / 22 diffusion steps, not the released 2026-05 model at 10 loops / 68 steps. So the 1.1 billion structures are not the accuracy the benchmark section reports.

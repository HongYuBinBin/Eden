# Outline — ESMC + ESMFold2 integrated review

Language: Korean (English term in parentheses at first use), as in the previous post.
Target length: body 2,000–2,400 words (two models, so the top of the band).
Slug: `content/posts/2026-11-__-esmc-esmfold2/`.
Title: `ESMC + ESMFold2 (Language Modeling Materializes a World Model of Protein Biology)`.

The thread that holds the two models together: **the language model's representation is the only thing the folding model is allowed to see.** ESMC decides how much structure is knowable from sequence; ESMFold2 spends inference compute turning that into atoms. The paper's scaling law (Fig 2B) is the hinge — it makes the two halves one argument rather than two releases.

This post is the sequel to `2026-11-12-esm2-esmfold`, so every section gets one explicit "what changed since ESM-2/ESMFold" beat. Link back with `#ev()` / margin notes rather than re-explaining.

## 💡 Highlights (~7%, 5 bullets, numbers first)
1. 2.8 billion sequences (≈ 56× ESM-2's ~50M) → log-linear returns all the way to 1.63 × 10²³ FLOPs.
2. 80 layers at the same 2560 width as ESM-2 3B — the 6B went into depth, and function clusters in layers 50–60.
3. 50% ± 2% antibody–antigen pass rate **from a single sequence**, beating AlphaFold3's 47% ± 2% *with* an MSA.
4. 15.8 s for 1024 residues on one H100 (Fast: 9.4 s), MSA construction excluded.
5. Five targets, 68 pM–70 nM binders, hit rates 53.8% → 70.0% for minibinders when search compute goes up.

## 1. Introduction (~15%)
- **1.1 "서열에 구조가 숨어 있다"는 약속의 다음 단계** — the concrete cost of the old way: MSA search is the bottleneck ESMFold removed, and MSA-based models still dominate complexes. Rhetorical question: 그래서 서열만으로 복합체까지 갈 수 있나?
- **1.2 Background: ESM-2/ESMFold에서 무엇이 남았나** — contrast masked LM vs next-token (carry over from the previous post in one line), and name what ESMFold left unsolved: complexes, antibodies, ligands, no inference-time knob. Inline [n] citations.
- **1.3 Contributions** — funnel bullets: 6.8B sequences → 1.1B structures → 5 targets → 84 designs each; three artifacts (ESMC, ESMFold2, Atlas) and what is MIT-released (A.6).
- ✏️ callout #1: **P@L-LR** (long-range contact precision) — one-line gloss, since it carries the whole scaling-law section. Note it is the same metric as the previous post.

## 2. Method (~30%)
- **2.1 ESMC는 ESM-2에서 무엇을 바꿨나?** — three bullets: data ×56, depth 36 → 80 at fixed width, µP hyperparameter transfer (proxy d_model 512 / 16 layers). Scaling law as a *design tool*: the fit was made on five small runs and then used to pick 300M/600M/6B.
- **2.2 표현(representation) 안에서 구조와 기능은 어디에 있나?** — structure peaks in the penultimate layer, function peaks at layers 50–60, and function directions exist independent of fold. Keep short; this is the bridge to why ESMFold2 pools *all* layers.
- **2.3 ESMFold2는 그 표현을 어떻게 원자로 바꾸나? (Enter ESMFold2)** — the anchor figure (Fig 2A, annotated ①–⑤) + the 5-step pipeline:
  1. each chain → frozen ESMC 6B, separately (homomer copying problem — state why)
  2. 81 layer states → softmax-weighted pool → pair space (d_z 256)
  3. recurrent folding trunk, 48 layers, looped T times with a contractive update
  4. two coda layers → diffusion transformer → atoms (68 truncated steps)
  5. confidence head (4 layers) → pLDDT / PAE / PDE
  - **What was removed** as separate bullets: the sequence-wise residual stream, triangle attention, and the MSA as a *required* input (now optional).
  - Then the gallery + mapping table from `_triangulation.md`.
- **Training** / **Evaluation** in two bold-labelled short paragraphs: 256 H100 × 127 h, 3 stages, FP8 backbone; FoldBench + Runs N' Poses, DockQ ≥ 0.23.
- Defer with "별도 글에서 다루겠다": SAE / latent-space analysis internals, the Atlas pipeline, and the diffusion loss.

## 3. Results (~35%, most of the critique)
- **3.1 서열 하나로 복합체를 맞출 수 있나?** — 50/70/66% vs AF3; the MSA-on numbers as the second step; one-line takeaway that the single-sequence→MSA gap is now smaller than the AbAg difficulty gap.
- **3.2 추론 때 계산을 더 쓰면 정말 좋아지나?** — loops (10 → 20 → 64) and samples (1 → 1000: 49% → 65%); Fast catching the full model at 1000 seeds. 🤔 interpretive skepticism: with per-loop LM dropout on at inference, "sampling" is partly sampling the *model*, not the structure distribution — is the 1000-seed number a property of the predictor or of the ranking metric?
- **3.3 언어모델 compute가 구조 정확도를 정말 결정하나?** — the two log-linear fits with R² 0.92 / 0.93, and the honest caveat that four checkpoints × three sizes is 12 points. 🤔 presentation critique: the two panels are per-task; a single panel with both axes normalised would show whether monomer and complex gains share a slope — at the cost of clutter.
- **3.4 얼마나 빠른가?** — 15.8 s / 9.4 s at L = 1024 on **one H100**, MSA construction excluded, Chai-1 off the plot at 110 s. State the exclusion explicitly (the comparison's fairness lives there).
- **3.5 설계까지 되나?** — binder numbers, kept to one subsection; 9 of 10 pairs improved; 68 pM–70 nM; PD-L1 IC50 1.6 nM vs 2.6 nM control. 🤔 the search cost (up to 7,700 H100-hours for one scFv target) is the real unit of the hit-rate claim.
- **3.6 (optional) 6.8B 서열 지도** — headline statistics only + the 🤔 that the Atlas used the experimental 3-loop/22-step checkpoint.
- ✏️ callout #2: **DockQ ≥ 0.23** — what "pass" means, in one line.
- ✏️ callout #3 (if room): **pLDDT / PAE** one-liners.
- 🤯 slot: the recycling → linear-recurrence lineage (finding 1 in `_triangulation.md`).

## 4. Conclusion (~5%)
Two or three sentences on the paper's claim, then open questions:
1. Is the single-sequence win on antibodies understanding, or is the 2026 training cutoff overlapping the benchmark? (note `esmfold2-2026-05-cutoff-2025` exists in the code — a cutoff-controlled checkpoint is published, so the authors clearly anticipated this; whether the main numbers use it is worth checking in A.2.9.)
2. If accuracy now buys itself with inference compute, what is the right way to report a folding model — a number, or a curve?
3. Follow-up post: the SAE feature space (A.4) and what "compositional grammar" actually buys.
Sign-off + feedback line + footer credit to the format reference.

## References
Numbered, linked, matching inline [n]: this preprint, ESM-2/ESMFold (Lin et al. 2023), AlphaFold2, AlphaFold3, Rao et al. contact prediction, ref 40 (the contractive recurrence paper — look up its real citation), FoldBench, Runs N' Poses, Biohub/esm repository, ESMFold2 model card.

## Checklist carried from the skill
- [ ] Every Method/Results heading is a question
- [ ] Every figure: source + licence caption, bold interpretive lead, number bullets
- [ ] ①–⑤ consistent across figure / text / code + mapping table
- [ ] Code lines verified at `fddac93` (done — `_triangulation.md`)
- [ ] ≥ 2 cross-check findings surfaced as 🤔/🤯 (7 candidates listed)
- [ ] 1–3 ✏️ callouts; one-line definitions for P@L-LR, DockQ, pLDDT, MSA
- [ ] Every results subsection has a number; speed states hardware + exclusions
- [ ] ≥ 2 open questions in the conclusion
- [ ] No equations/hyperparameters in the body beyond the two scaling fits and the loop counts
- [ ] Side-by-side screenshot comparison against the reference review before publishing

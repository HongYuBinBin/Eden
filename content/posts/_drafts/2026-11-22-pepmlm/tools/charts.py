"""Three figures neither paper draws.

1. benchmark.png - the two models' in silico hit rates against the same RFDiffusion
   baseline, beside the stringency of the test set each was measured on. PepMLM reports
   a bound ("exceeding 38%"), PepPrCLIP a point value (17.7%), so the bars are drawn
   as bounds where the paper gives a bound.

2. ppl.png - pseudo-perplexity of the 203 held-out binders against the 203 PepMLM-650M
   binders, computed from scripts/data/test.csv and scripts/data/gen_650M.csv in the
   official repo. The paper plots a density but leaves the values in Supplementary Table 2.

3. overlap.png - how much of PepMLM's held-out test set was already in its training file,
   computed from scripts/data/train.csv and scripts/data/test.csv.

Sized for the blog's fullwidth display (1244 px): saved at ~2450 px, so labels land near 26 px.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import font_manager
import numpy as np
import pandas as pd
import os, sys, random

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SRC = "/home/claude/pepsrc/pepmlm/scripts/data"

INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#d9d9d9"
BG = "#ffffff"
PML = "#2d6bb3"   # PepMLM        (marker 4 blue)
PPC = "#8b5a8f"   # PepPrCLIP     (marker 2 purple)
BASE = "#8a8a8a"  # RFDiffusion   (neutral grey)
HOT = "#cf3f37"   # the thing to look at (marker 1 red)

for f in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",):
    if os.path.exists(f):
        try:
            font_manager.fontManager.addfont(f)
        except Exception:
            pass
plt.rcParams.update({
    "font.family": ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"],
    "font.size": 20, "text.color": INK,
    "axes.edgecolor": GRID, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": BG, "axes.facecolor": BG,
    "savefig.facecolor": BG,
})


def tidy(ax, xgrid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=.8)
        ax.set_axisbelow(True)


# ---------------------------------------------------------------- 1. benchmark
def benchmark():
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(24.5, 7.6), dpi=100,
                                   gridspec_kw=dict(width_ratios=[1.45, 1], wspace=.34))

    # left: hit rate, model vs the shared RFDiffusion baseline
    rows = ["PepPrCLIP\n(Sci Adv 2025)", "PepMLM-650M\n(arXiv v3)"]
    y = np.arange(len(rows))[::-1]
    model = [17.7, 38.0]
    basel = [30.1, 30.0]
    bound = [False, True]     # is the model number a lower bound?
    bbound = [False, True]    # is the baseline number an upper bound?
    h = .32

    axl.barh(y + h / 2 + .02, model, height=h, color=[PPC, PML], zorder=3)
    axl.barh(y - h / 2 - .02, basel, height=h, color=BASE, zorder=3)

    for i, (v, b) in enumerate(zip(model, bound)):
        axl.text(v + .9, y[i] + h / 2 + .02, ("> " if b else "") + f"{v:g}%",
                 va="center", fontsize=23, color=[PPC, PML][i], fontweight="bold")
    for i, (v, b) in enumerate(zip(basel, bbound)):
        axl.text(v + .9, y[i] - h / 2 - .02, ("< " if b else "") + f"{v:g}%",
                 va="center", fontsize=23, color=MUTED)

    axl.set_yticks(y); axl.set_yticklabels(rows, fontsize=22, color=INK)
    axl.set_xlim(0, 56); axl.set_xlabel("AlphaFold-Multimer ipTM 기준 in silico hit rate (%)", fontsize=21)
    axl.set_title("같은 기준, 같은 베이스라인 — 뒤집힌 승패", fontsize=26, color=INK,
                  pad=16, loc="left", fontweight="bold")
    axl.legend(handles=[Patch(color=PPC, label="PepPrCLIP"),
                        Patch(color=PML, label="PepMLM-650M"),
                        Patch(color=BASE, label="RFDiffusion (공통 베이스라인)")],
               loc="center right", frameon=False, fontsize=18,
               bbox_to_anchor=(1.015, .5))
    tidy(axl)

    # right: how the two test sets were built
    rows2 = ["PepPrCLIP\n(Sci Adv 2025)", "PepMLM-650M\n(arXiv v3)"]
    y2 = np.arange(len(rows2))[::-1]
    thr = [30, 80]
    axr.barh(y2, thr, height=.42, color=[PPC, HOT], zorder=3)
    notes = ["209개 테스트 쌍\nMMseqs2 30% 서열 동일성 클러스터링",
             "203개 테스트 쌍\n타깃 서열만 0.8 임계값 + 수동 80% 필터"]
    for i, (v, n) in enumerate(zip(thr, notes)):
        axr.text(v + 2.5, y2[i] + .04, f"{v}%", va="center", fontsize=23,
                 color=[PPC, HOT][i], fontweight="bold")
        axr.text(1.5, y2[i] - .32, n, va="top", fontsize=17.5, color=MUTED)
    axr.set_yticks(y2); axr.set_yticklabels(rows2, fontsize=22, color=INK)
    axr.set_xlim(0, 100)
    axr.set_xlabel("train/test 분할에 허용된 서열 동일성 상한 (%)", fontsize=21)
    axr.set_title("숫자가 매겨진 시험지는 같지 않았다", fontsize=26, color=INK,
                  pad=16, loc="left", fontweight="bold")
    axr.set_ylim(-.75, 1.55)
    tidy(axr)

    fig.savefig(os.path.join(OUT, "benchmark.png"), bbox_inches="tight", pad_inches=.28)
    plt.close(fig)
    print("benchmark.png")


# ---------------------------------------------------------------- 2. perplexity
def ppl():
    t = pd.read_csv(f"{SRC}/test.csv"); g = pd.read_csv(f"{SRC}/gen_650M.csv")
    tp = t["PPL"].astype(float).values
    gp = g["PPL"].astype(float).values

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(24.5, 7.4), dpi=100,
                                   gridspec_kw=dict(width_ratios=[1.3, 1], wspace=.22))

    bins = np.logspace(0, np.log10(200), 36)
    axl.hist(tp, bins=bins, color=BASE, alpha=.85, label=f"실제 결합 펩타이드 (n={len(tp)})", zorder=3)
    axl.hist(gp, bins=bins, color=PML, alpha=.80, label=f"PepMLM-650M 생성 (n={len(gp)})", zorder=4)
    axl.set_xscale("log")
    for v, c, lab in ((np.median(tp), BASE, f"중앙값 {np.median(tp):.2f}"),
                      (np.median(gp), PML, f"중앙값 {np.median(gp):.2f}")):
        axl.axvline(v, color=c, lw=2, ls="--", zorder=5)
    axl.text(np.median(tp) * 1.1, axl.get_ylim()[1] * .93, f"중앙값 {np.median(tp):.2f}",
             fontsize=20, color=INK, va="top")
    axl.text(np.median(gp) * .95, axl.get_ylim()[1] * .74, f"중앙값 {np.median(gp):.2f}",
             fontsize=20, color=PML, va="top", ha="right", fontweight="bold")
    axl.annotate(f"실제 결합 펩타이드의 꼬리\n최대 {tp.max():.0f} · 40 초과 {int((tp>40).sum())}개",
                 xy=(tp.max() * .92, 1.6), xytext=(30, 9.4), fontsize=18, color=HOT,
                 arrowprops=dict(arrowstyle="->", color=HOT, lw=2,
                                 connectionstyle="arc3,rad=-.25"))
    axl.set_xlabel("pseudo-perplexity (로그 축)", fontsize=21)
    axl.set_ylabel("펩타이드 수", fontsize=21)
    axl.set_title("생성 서열이 실제 결합 서열보다 '더 그럴듯하다'", fontsize=26,
                  color=INK, pad=16, loc="left", fontweight="bold")
    axl.legend(frameon=False, fontsize=19, loc="upper right", bbox_to_anchor=(1, .62))
    tidy(axl, xgrid=False)
    axl.yaxis.grid(True, color=GRID, lw=.8); axl.set_axisbelow(True)

    # right: paired, same target
    lower = (gp < tp).sum()
    axr.barh([1], [100 * lower / len(tp)], height=.44, color=PML, zorder=3)
    axr.barh([0], [100 * (1 - lower / len(tp))], height=.44, color=BASE, zorder=3)
    axr.text(100 * lower / len(tp) - 2, 1, f"{100*lower/len(tp):.1f}%", va="center", ha="right",
             fontsize=26, color="white", fontweight="bold")
    axr.text(100 * (1 - lower / len(tp)) + 2, 0, f"{100*(1-lower/len(tp)):.1f}%", va="center",
             fontsize=26, color=MUTED, fontweight="bold")
    axr.set_yticks([1, 0])
    axr.set_yticklabels([f"생성 서열이 더 낮음\n({lower} / {len(tp)})",
                         f"실제 서열이 더 낮음\n({len(tp)-lower} / {len(tp)})"], fontsize=21, color=INK)
    axr.set_xlim(0, 100); axr.set_xlabel("같은 타깃에서 더 낮은 perplexity를 받은 쪽 (%)", fontsize=21)
    axr.set_title("203개 타깃 1:1 비교", fontsize=26, color=INK, pad=16, loc="left",
                  fontweight="bold")
    tidy(axr)

    fig.savefig(os.path.join(OUT, "ppl.png"), bbox_inches="tight", pad_inches=.28)
    plt.close(fig)
    print(f"ppl.png  (gen median {np.median(gp):.2f} vs real {np.median(tp):.2f}, "
          f"gen lower in {lower}/{len(tp)})")


# ---------------------------------------------------------------- 3. overlap
def overlap():
    t = pd.read_csv(f"{SRC}/test.csv"); g = pd.read_csv(f"{SRC}/gen_650M.csv")
    tr = pd.read_csv(f"{SRC}/train.csv")
    tb = t["Binder"].astype(str).tolist()
    gb = g["Binder"].astype(str).tolist()
    trb = set(tr["Binder"].astype(str))

    def ident(a, b):
        return sum(x == y for x, y in zip(a, b)) / len(a)

    obs = [ident(a, b) for a, b in zip(tb, gb)]
    random.seed(0)
    bylen = {}
    for i, s in enumerate(tb):
        bylen.setdefault(len(s), []).append(i)
    null = []
    for i, gs in enumerate(gb):
        cand = [j for j in bylen[len(gs)] if j != i]
        if cand:
            null += [ident(gs, tb[j]) for j in random.sample(cand, min(5, len(cand)))]

    verb = sum(s in trb for s in tb)
    trl = {}
    for s in trb:
        trl.setdefault(len(s), []).append(s)
    best = [max((ident(s, o) for o in trl.get(len(s), [])), default=0) for s in tb]
    near = sum(b >= .8 for b in best)

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(24.5, 7.4), dpi=100,
                                   gridspec_kw=dict(width_ratios=[1.15, 1], wspace=.52))

    bins = np.linspace(0, 1, 21)
    axl.hist(null, bins=bins, weights=np.full(len(null), 100 / len(null)),
             color=BASE, alpha=.85, label=f"다른 타깃의 정답 (귀무, n={len(null)})", zorder=3)
    axl.hist(obs, bins=bins, weights=np.full(len(obs), 100 / len(obs)),
             color=PML, alpha=.80, label=f"같은 타깃의 정답 (n={len(obs)})", zorder=4)
    axl.axvline(np.mean(null), color=BASE, lw=2, ls="--", zorder=5)
    axl.axvline(np.mean(obs), color=PML, lw=2, ls="--", zorder=5)
    axl.text(np.mean(obs) + .015, axl.get_ylim()[1] * .55, f"평균 {100*np.mean(obs):.0f}%",
             fontsize=20, color=PML, va="top", fontweight="bold")
    axl.text(np.mean(null) + .015, axl.get_ylim()[1] * .72, f"평균 {100*np.mean(null):.0f}%",
             fontsize=20, color=INK, va="top")
    axl.set_xlabel("생성 서열과 정답 서열의 위치별 동일성", fontsize=21)
    axl.set_ylabel("비율 (%)", fontsize=21)
    axl.set_xticks(np.arange(0, 1.01, .25))
    axl.set_xticklabels([f"{int(v*100)}%" for v in np.arange(0, 1.01, .25)])
    axl.set_title("생성 서열은 우연보다 정답에 가깝다", fontsize=26, color=INK, pad=16,
                  loc="left", fontweight="bold")
    axl.legend(frameon=False, fontsize=17.5, loc="upper right", bbox_to_anchor=(1.0, 1.0))
    tidy(axl, xgrid=False)
    axl.yaxis.grid(True, color=GRID, lw=.8); axl.set_axisbelow(True)

    # right: how much of the test set was already in the training file
    labs = ["학습 파일에\n글자 그대로 존재",
            "학습 파일에 80% 이상\n동일한 같은 길이 서열 존재"]
    vals = [100 * verb / len(tb), 100 * near / len(tb)]
    cnts = [f"{verb} / {len(tb)}", f"{near} / {len(tb)}"]
    yy = [1, 0]
    axr.barh(yy, vals, height=.44, color=HOT, zorder=3)
    for i, (v, c) in enumerate(zip(vals, cnts)):
        axr.text(v + 1.5, yy[i], f"{v:.0f}%   ({c})", va="center", fontsize=24,
                 color=HOT, fontweight="bold")
    axr.set_yticks(yy); axr.set_yticklabels(labs, fontsize=20, color=INK)
    axr.set_xlim(0, 100); axr.set_xlabel("203개 테스트 결합 서열 중 비율 (%)", fontsize=21)
    axr.set_title("분할은 타깃 기준이었고, 결합 서열은 양쪽에 남았다", fontsize=25,
                  color=INK, pad=16, loc="left", fontweight="bold")
    tidy(axr)

    fig.savefig(os.path.join(OUT, "overlap.png"), bbox_inches="tight", pad_inches=.28)
    plt.close(fig)
    print(f"overlap.png  (obs mean {100*np.mean(obs):.1f}% vs null {100*np.mean(null):.1f}%, "
          f"verbatim {verb}/{len(tb)}, >=80% {near}/{len(tb)})")


if __name__ == "__main__":
    benchmark(); ppl(); overlap()

"""Two figures the report does not draw.

1. concentration.png - where BoltzProt-1's 12 confirmed binders actually came from.
   The report gives per-target bars only for the five targets with any signal (Figure 1a)
   and the totals only in Table 1. Neither view shows that 11 of 12 binders sit on two targets.

2. revised.png - Table 1's initial vs revised screening-hit counts, with the numbers the
   body text quotes marked on top.

Sized for the blog's fullwidth display (1244 px): saved at ~2500 px, so labels land near 26 px.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#d9d9d9"
BG = "#ffffff"
BP = "#2d6bb3"   # BoltzProt-1  (marker 4 blue)
BG_ = "#8a8a8a"  # BoltzGen     (neutral grey)
HOT = "#cf3f37"  # the thing to look at (marker 1 red)

# Noto Sans CJK KR is the only Korean-capable family on this box.
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

TARGETS = ["PMVK", "IDI2", "AMBP", "MZB1", "HNMT", "GM2A", "METTL16", "ORM2", "PHYH", "RFK"]
BPROT = {"PMVK": 7, "IDI2": 4, "AMBP": 1}
BGEN = {"PMVK": 4, "IDI2": 1}


def concentration():
    fig, ax = plt.subplots(figsize=(12.5, 6.4), dpi=200)
    h = 0.38
    for i, t in enumerate(TARGETS):
        y = len(TARGETS) - 1 - i
        b, g = BPROT.get(t, 0), BGEN.get(t, 0)
        ax.barh(y + h / 2 + 0.02, b, height=h, color=BP, edgecolor="none", zorder=3)
        ax.barh(y - h / 2 - 0.02, g, height=h, color=BG_, edgecolor="none", zorder=3)
        if b:
            ax.text(b + 0.13, y + h / 2 + 0.02, f"{b}", va="center", ha="left",
                    color=BP, fontsize=19, fontweight="bold")
        if g:
            ax.text(g + 0.13, y - h / 2 - 0.02, f"{g}", va="center", ha="left",
                    color=BG_, fontsize=19)
        if not b and not g:
            ax.text(0.13, y, "0", va="center", ha="left", color=MUTED, fontsize=17)

    ax.set_yticks([len(TARGETS) - 1 - i for i in range(len(TARGETS))])
    ax.set_yticklabels(TARGETS, fontsize=19)
    ax.set_xlim(0, 9.6)
    ax.set_xticks(range(0, 9, 2))
    ax.set_xlabel("표적당 확정 결합체 수 (설계 15개 중)", fontsize=19, labelpad=10)
    ax.xaxis.grid(True, color=GRID, lw=1, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)

    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=BP, label="BoltzProt-1 (합계 12)"),
                       Patch(color=BG_, label="BoltzGen (합계 5)")],
              loc="lower right", frameon=False, fontsize=19, handlelength=1.2)

    ax.annotate("12개 중 7개가 이 표적 하나에서", xy=(7.15, 9.2), xytext=(8.0, 7.3),
                color=HOT, fontsize=19, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=2.2,
                                connectionstyle="arc3,rad=-0.25"))
    ax.annotate("나머지 일곱 표적, 설계 105개에서 0개", xy=(0.25, 3.0), xytext=(4.5, 3.1),
                color=HOT, fontsize=19, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=2.2,
                                connectionstyle="arc3,rad=0.2"))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "concentration.png"), bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


def revised():
    fig, ax = plt.subplots(figsize=(12.5, 5.6), dpi=200)
    labels = ["BoltzGen", "BoltzProt-1"]
    initial = [15, 24]
    rev = [7, 14]
    x = [0, 1]
    w = 0.3
    ax.bar([i - w / 2 - 0.015 for i in x], initial, width=w, color="#c9d6e6",
           edgecolor="none", zorder=3, label="최초 집계")
    ax.bar([i + w / 2 + 0.015 for i in x], rev, width=w, color=BP,
           edgecolor="none", zorder=3, label="Adaptyv 프로토콜 개정 후")
    for i, (a, b) in enumerate(zip(initial, rev)):
        ax.text(i - w / 2 - 0.015, a + 0.5, str(a), ha="center", color=MUTED, fontsize=19)
        ax.text(i + w / 2 + 0.015, b + 0.5, str(b), ha="center", color=BP,
                fontsize=19, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=20)
    ax.set_ylim(0, 29)
    ax.set_ylabel("스크리닝 히트 수 (설계 150개 중)", fontsize=19, labelpad=10)
    ax.yaxis.grid(True, color=GRID, lw=1, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.legend(loc="upper left", frameon=False, fontsize=18, handlelength=1.2)

    ax.annotate("본문은 이 둘을 맞세운다\n24 (16.0%) 대 14 (9.3%)",
                xy=(1.16, 19.2), xytext=(1.62, 24.0), color=HOT, fontsize=18, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=2.2,
                                connectionstyle="arc3,rad=0.25"))
    ax.annotate("BoltzGen의 개정값은 7 (4.7%)", xy=(0.165, 7.4), xytext=(0.52, 12.4),
                color=HOT, fontsize=18, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=2.2,
                                connectionstyle="arc3,rad=-0.2"))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "revised.png"), bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


if __name__ == "__main__":
    concentration(); revised()
    print("charts written to", OUT)

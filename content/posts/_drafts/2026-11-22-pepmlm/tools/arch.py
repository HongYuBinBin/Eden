"""pipelines.png - the two pipelines side by side, drawn from the two papers' Methods.

The point the drawing has to carry: in PepPrCLIP the target sequence only enters at the
scoring step, so the generator never sees it; in PepMLM the target IS the context the
peptide is generated in. Markers match the review's triangulation table.

Both papers' own figures are redrawn rather than reproduced: PepMLM's arXiv v3 is
CC BY-NC-ND, which does not permit derivatives.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib import font_manager
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

INK = "#1a1a1a"
MUTED = "#6b6b6b"
BG = "#ffffff"
MK = {1: "#cf3f37", 2: "#8b5a8f", 3: "#b9760c", 4: "#2d6bb3"}
PPC_BG = "#f4eef5"
PML_BG = "#eaf1f9"
BOX = "#ffffff"
EDGE = "#c8c8c8"

for f in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",):
    if os.path.exists(f):
        try:
            font_manager.fontManager.addfont(f)
        except Exception:
            pass
plt.rcParams.update({
    "font.family": ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"],
    "text.color": INK, "figure.facecolor": BG, "savefig.facecolor": BG,
})

fig, ax = plt.subplots(figsize=(24.5, 11.4), dpi=100)
ax.set_xlim(0, 100); ax.set_ylim(0, 48); ax.axis("off")


def band(y0, h, color, label, sub):
    ax.add_patch(FancyBboxPatch((1.2, y0), 97.6, h, boxstyle="round,pad=0,rounding_size=1.1",
                                fc=color, ec="none", zorder=0))
    ax.text(2.6, y0 + h - 1.5, label, fontsize=27, fontweight="bold", va="top", zorder=4)
    ax.text(2.6, y0 + h - 4.6, sub, fontsize=18, color=MUTED, va="top", zorder=4)


def box(x, y, w, h, text, sub=None, ec=EDGE, lw=2.0, fc=BOX, fs=18.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=.8",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    cy = y + h / 2 + (1.0 if sub else 0)
    ax.text(x + w / 2, cy, text, ha="center", va="center", fontsize=fs, zorder=4)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 1.9, sub, ha="center", va="center",
                fontsize=15, color=MUTED, zorder=4)
    return x + w, y + h / 2


def arrow(p, q, col=MUTED, lw=2.2, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22,
                                 lw=lw, color=col, zorder=2, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=2, shrinkB=3))


def marker(n, xy, r=1.55):
    ax.add_patch(Circle(xy, r, fc="white", ec=MK[n], lw=3.0, zorder=6))
    ax.text(xy[0], xy[1] - .05, "①②③④"[n - 1], ha="center", va="center",
            fontsize=20, color=MK[n], zorder=7)


# ------------------------------------------------------------------ PepPrCLIP
band(26.0, 21.0, PPC_BG, "PepPrCLIP  —  만들어 놓고 고른다 (generate → screen)",
     "Science Advances 2025 · 생성기는 타깃을 보지 않는다")

Y = 33.4; H = 6.4
box(3.0, Y, 13.4, H, "PDB 실제\n결합 펩타이드", "학습 세트에서 100~1000개 추출")
arrow((16.4, Y + H / 2), (19.6, Y + H / 2))
box(19.6, Y, 13.0, H, "ESM-2-650M\n임베딩", "잔기별 벡터")
arrow((32.6, Y + H / 2), (35.8, Y + H / 2))
box(35.8, Y, 13.8, H, "가우시안 잡음", "k = 5~22, 분산에 곱함", ec=MK[1], lw=3.2)
marker(1, (36.9, Y + H - .5))
arrow((49.6, Y + H / 2), (52.8, Y + H / 2))
box(52.8, Y, 13.0, H, "ESM-2 마지막 층\n으로 디코딩", "후보 약 100,000개")
arrow((65.8, Y + H / 2), (69.0, Y + H / 2))
box(69.0, Y, 13.6, H, "CLIP 점수로 순위", "코사인 유사도", ec=MK[2], lw=3.2)
marker(2, (70.1, Y + H - .5))
arrow((82.6, Y + H / 2), (85.8, Y + H / 2))
box(85.8, Y, 11.4, H, "상위 펩타이드", "합성·검증 대상")

# the target enters only here
ax.add_patch(FancyBboxPatch((49.4, 27.0), 20.6, 4.4,
                            boxstyle="round,pad=0,rounding_size=.8",
                            fc="white", ec=MK[3], lw=3.0, zorder=3))
ax.text(60.4, 29.2, "타깃 서열  →  ESM-2 타깃 인코더", ha="center", va="center",
        fontsize=16, zorder=4)
arrow((70.0, 29.2), (75.8, Y - .15), col=MK[3], lw=2.6, rad=-.28)
marker(3, (50.6, 30.9))

# ------------------------------------------------------------------ PepMLM
band(2.6, 20.2, PML_BG, "PepMLM  —  타깃 문맥 안에서 바로 채운다 (conditional generation)",
     "arXiv v3 · 타깃이 곧 생성 조건")

Y2 = 6.0; H2 = 6.4
box(3.0, Y2, 20.6, H2, "타깃 서열  +  <mask> × L", "binder를 타깃 C-말단에 이어 붙임",
    ec=MK[4], lw=3.2, fs=17.5)
marker(4, (4.1, Y2 + H2 - .5))
arrow((23.6, Y2 + H2 / 2), (26.8, Y2 + H2 / 2))
box(26.8, Y2, 15.6, H2, "ESM-2-650M\n파인튜닝", "마스크 위치에만 손실")
arrow((42.4, Y2 + H2 / 2), (45.6, Y2 + H2 / 2))
box(45.6, Y2, 16.4, H2, "forward 한 번", "마스크 전 위치 동시 예측")
arrow((62.0, Y2 + H2 / 2), (65.2, Y2 + H2 / 2))
box(65.2, Y2, 16.0, H2, "위치별 top-k 샘플링", "코드 기본값 k = 3")
arrow((81.2, Y2 + H2 / 2), (84.4, Y2 + H2 / 2))
box(84.4, Y2, 12.8, H2, "펩타이드", "논문 기본값은 greedy")

ax.text(50.0, 2.0, "두 파이프라인의 갈림길: 타깃 서열이 ③ 점수 단계에만 들어가는가, "
                   "④ 생성 단계부터 들어가는가", ha="center", fontsize=19.5, color=INK,
        style="italic")

fig.savefig(os.path.join(OUT, "pipelines.png"), bbox_inches="tight", pad_inches=.3)
plt.close(fig)
print("pipelines.png")

"""The architecture figure the report does not have.

BoltzProt-1's report describes BoltzPPI in prose only — there is no diagram of the model
anywhere in its 27 pages. This redraws the description in section 2.2, with the parts that
can be checked against Boltz-2's open code (jwohlwend/boltz @ b1ebfc4, MIT) labelled with
their file and line, and the parts that cannot be checked marked as the report's words only.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
for f in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",):
    if os.path.exists(f):
        try:
            font_manager.fontManager.addfont(f)
        except Exception:
            pass
plt.rcParams.update({"font.family": ["Noto Sans CJK KR", "DejaVu Sans"]})

INK, MUTED, GRID = "#1a1a1a", "#6b6b6b", "#c8c8c8"
MK = {1: "#cf3f37", 2: "#8b5a8f", 3: "#b9760c", 4: "#2d6bb3"}
OPEN_F = "#eef4fb"   # comes from Boltz-2, readable in open code
CLOSED_F = "#fdf1ef" # described in the report only


def box(ax, x, y, w, h, title, sub, edge, face, tsize=15, ssize=12.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.02",
                                lw=2.2, ec=edge, fc=face, zorder=3))
    ax.text(x + w / 2, y + h - 0.052, title, ha="center", va="top", fontsize=tsize,
            color=INK, zorder=4, fontweight="bold")
    if sub:
        ax.text(x + w / 2, y + h - 0.125, sub, ha="center", va="top", fontsize=ssize,
                color=MUTED, zorder=4, linespacing=1.45)


def arrow(ax, p, q, col=INK, lw=2.0, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=17, lw=lw,
                                 color=col, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}"))


def marker(ax, n, xy, r=0.019):
    ax.add_patch(plt.Circle(xy, r, fill=False, ec=MK[n], lw=2.6, zorder=6))
    ax.text(xy[0], xy[1] - 0.004, str(n), ha="center", va="center", fontsize=14,
            color=MK[n], zorder=7, fontweight="bold")


def main():
    fig, ax = plt.subplots(figsize=(13.6, 6.1), dpi=190)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # ---- inputs from the frozen Boltz-2 trunk
    box(ax, 0.015, 0.60, 0.175, 0.265, "Boltz-2 트렁크",
        "단일 표현 s\n쌍 표현 z\n예측 좌표", GRID, OPEN_F)
    box(ax, 0.015, 0.215, 0.175, 0.30, "거리 행렬 둘",
        "전체 좌표 거리\n최소 토큰간 거리\n+ 결합체/표적 마스크", GRID, OPEN_F)

    # ---- (1) pair input construction
    box(ax, 0.245, 0.33, 0.185, 0.50, "쌍 입력 구성",
        "s를 쌍 공간으로 투영\n마스크 임베딩\n거리 이산화 임베딩\n(64 bins, 22 Å)",
        MK[1], OPEN_F)
    marker(ax, 1, (0.2655, 0.858))

    # ---- (2) pairformer
    box(ax, 0.485, 0.33, 0.155, 0.50, "Pairformer",
        "4 blocks\n16 heads\ndropout 0.25", MK[2], CLOSED_F)
    marker(ax, 2, (0.5055, 0.858))

    # ---- (3) two heads
    box(ax, 0.695, 0.595, 0.175, 0.235, "PPI 헤드",
        "logit → σ → p\nfocal loss", MK[3], CLOSED_F)
    marker(ax, 3, (0.7155, 0.858))
    box(ax, 0.695, 0.285, 0.175, 0.235, "confidence 헤드",
        "pLDDT · PDE · PAE", MK[3], OPEN_F)

    # ---- (4) inference pooling
    box(ax, 0.905, 0.405, 0.085, 0.33, "결합 점수",
        "쌍 평균\n(사슬 간)\n+ 토큰 평균\n→ MLP → σ", MK[4], CLOSED_F)
    marker(ax, 4, (0.9255, 0.762))

    arrow(ax, (0.192, 0.73), (0.243, 0.66))
    arrow(ax, (0.192, 0.365), (0.243, 0.44))
    arrow(ax, (0.432, 0.58), (0.483, 0.58))
    arrow(ax, (0.642, 0.62), (0.693, 0.70))
    arrow(ax, (0.642, 0.52), (0.693, 0.43))
    arrow(ax, (0.872, 0.70), (0.903, 0.62))
    arrow(ax, (0.872, 0.41), (0.903, 0.49))

    # the 50% dropout path, drawn as the report describes it
    ax.add_patch(FancyArrowPatch((0.337, 0.325), (0.337, 0.20), arrowstyle="-",
                                 lw=2.0, ls=(0, (5, 4)), color=MK[1], zorder=2))
    ax.text(0.347, 0.155, "학습의 50%에서 트렁크 쌍 표현을 떨어뜨린다 (multi-view)",
            fontsize=13, color=MK[1], va="center")

    ax.text(0.015, 0.075,
            "채움색이 연한 파랑인 상자는 Boltz-2 공개 코드(MIT)에서 그대로 확인되고, "
            "연한 분홍인 상자는 리포트 본문 서술만 있는 부분이다.",
            fontsize=12.5, color=MUTED)
    ax.text(0.015, 0.025,
            "① affinity.py L54·L49-51   ② 보고된 수치 중 16 heads·0.25는 Boltz-2 기본값   "
            "③ affinity.py L176 · confidencev2.py L234   ④ affinity.py L161-176",
            fontsize=12.5, color=MUTED, family="monospace")

    fig.savefig(os.path.join(OUT, "boltzppi.png"), bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)
    print("boltzppi.png written")


if __name__ == "__main__":
    main()

"""Reviewer's own redraw: per-target wet-lab hit rate from Appendix Table A18.

The paper reports one headline number (61.5%, 131/213). The table behind it sits
in the appendix and is never plotted. This chart plots it.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

KR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(KR)
plt.rcParams["font.family"] = "Noto Sans CJK KR"
plt.rcParams["axes.unicode_minus"] = False

# Table A18: (target, tested, confirmed); sorted within each group, high to low
GROUPS = [
    ("잘 알려진 표적", "#2d6bb3", [("CDK1", 22, 22), ("TYK2", 24, 23),
                              ("JAK1", 24, 21), ("PRMT5", 24, 16)]),
    ("새 화학 공간", "#2f8f6b", [("MNK2", 24, 19), ("HDAC6", 24, 15),
                             ("MMP-9", 23, 3)]),
    ("분포 밖(OOD)", "#cf3f37", [("KDR/VEGFR2", 24, 10), ("ELANE", 24, 2)]),
]
OVERALL = 131 / 213 * 100

rows, colors, gpos = [], [], []
y = 0
for gname, gcol, items in GROUPS:
    start = y
    for name, tested, conf in items:
        rows.append((name, tested, conf, conf / tested * 100))
        colors.append(gcol)
        y += 1
    gpos.append((gname, gcol, start, y - 1))

n = len(rows)
ys = [n - 1 - i for i in range(n)]          # first row at the top
seps = [n - 1 - (b + 0.5) for _, _, _, b in gpos[:-1]]

SURFACE = "#fcfcfb"
INK = "#1d2329"
MUTED = "#6b7580"

fig, ax = plt.subplots(figsize=(12.6, 5.2), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

for yi, (name, tested, conf, rate), col in zip(ys, rows, colors):
    ax.barh(yi, rate, height=0.58, color=col, zorder=3)
    ax.text(rate + 1.8, yi, f"{rate:.0f}%", va="center", ha="left",
            fontsize=12, color=INK, zorder=4, fontweight="bold")
    ax.text(rate + 11.5, yi, f"{conf}/{tested}", va="center", ha="left",
            fontsize=11, color=MUTED, zorder=4)
    ax.text(-1.8, yi, name, va="center", ha="right", fontsize=12, color=INK)

ax.axvline(OVERALL, color=INK, lw=1.4, ls=(0, (5, 4)), zorder=5, alpha=.8)
ax.text(OVERALL + 0.8, n - 0.3, "논문이 내세우는 평균 61.5%",
        fontsize=12, color=INK, va="bottom", ha="left")

for s in seps:
    ax.axhline(s, color="#e1e4e2", lw=1, zorder=1)
for gname, gcol, a, b in gpos:
    ax.text(-32.0, n - 1 - (a + b) / 2, gname, va="center", ha="left",
            fontsize=11.5, color=gcol, fontweight="bold")

ax.set_xlim(0, 178)
ax.set_ylim(-0.7, n - 0.05)
ax.set_yticks([])
ticks = [0, 20, 40, 60, 80, 100]
ax.set_xticks(ticks)
ax.set_xticklabels([f"{v}%" for v in ticks], fontsize=11, color=MUTED)
ax.tick_params(axis="x", length=0, pad=6)
ax.set_xlabel("합성·검정한 화합물 가운데 용량–반응으로 저해가 확인된 비율",
              fontsize=11.5, color=MUTED, labelpad=10)
ax.xaxis.grid(True, color="#ebedec", lw=1, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#d8dbd9")

ax.set_title("표적별 습식 실험 적중률 (Mashiach 2026, 부록 Table A18의 수치로 내가 다시 그림)",
             fontsize=13.5, color=INK, loc="left", pad=40, x=-0.145)
ax.legend(handles=[Patch(facecolor=c, label=g) for g, c, _, _ in gpos],
          loc="upper left", bbox_to_anchor=(-0.145, 1.085), frameon=False,
          fontsize=11, ncol=3, labelcolor=INK, handlelength=1.1,
          handleheight=1.1, borderpad=0, columnspacing=1.6, handletextpad=0.5)

fig.subplots_adjust(left=0.17, right=0.99, top=0.845, bottom=0.135)
fig.savefig("/tmp/bon/hitrate_raw.png", facecolor=SURFACE)
print("saved", fig.get_size_inches() * fig.dpi)

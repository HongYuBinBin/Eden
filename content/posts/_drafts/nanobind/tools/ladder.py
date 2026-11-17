"""Reviewer's own figure: the resolution of NanoBind-affi's reference ladder.

Built from data/affinity/reference_set.csv (49 anchors) in the official
repository, which is exactly the ladder hard-coded as 48 intervals in
predict_affi.py. The paper never plots it.
"""
import csv, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

KR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
fm.fontManager.addfont(KR)
plt.rcParams["font.family"] = "Noto Sans CJK KR"
plt.rcParams["axes.unicode_minus"] = False

SRC = "/home/claude/zhaosq17/nanobind/data/affinity/reference_set.csv"
a = sorted(float(r["affinity"]) for r in csv.DictReader(io.open(SRC, encoding="utf-8")))
mids = [(lo * hi) ** 0.5 for lo, hi in zip(a, a[1:])]
folds = [hi / lo for lo, hi in zip(a, a[1:])]

SURFACE = "#fcfcfb"
INK = "#1d2329"
MUTED = "#6b7580"
BLUE = "#2d6bb3"
RED = "#cf3f37"

fig, ax = plt.subplots(figsize=(12.0, 5.0), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

for x, f in zip(mids, folds):
    ax.plot([x, x], [1, f], color=BLUE, lw=1.6, zorder=3, alpha=.55,
            solid_capstyle="round")
ax.scatter(mids, folds, s=34, color=BLUE, zorder=4, edgecolor=SURFACE, linewidth=1.2)

# the one coarse interval
w = max(range(len(folds)), key=lambda i: folds[i])
ax.scatter([mids[w]], [folds[w]], s=70, color=RED, zorder=5,
           edgecolor=SURFACE, linewidth=1.4)

ax.axhline(2, color=INK, lw=1.2, ls=(0, (5, 4)), alpha=.7, zorder=2)
ax.text(1.1e-11, 2.12, "2배", fontsize=11.5, color=INK, va="bottom")

ax.scatter(a, [1.02] * len(a), marker="|", s=90, color=MUTED, zorder=3, linewidth=1)
ax.text(2.4e-3, 1.02, "눈금 49개", fontsize=10.5, color=MUTED, ha="right", va="bottom")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(4e-12, 2e-3)
ax.set_ylim(1.0, 40)
ax.set_yticks([1, 1.5, 2, 3, 5, 10, 25])
ax.set_yticklabels(["1배", "1.5배", "2배", "3배", "5배", "10배", "25배"],
                   fontsize=11, color=MUTED)
ax.tick_params(axis="x", labelsize=11, colors=MUTED)
ax.tick_params(axis="y", length=0)
ax.minorticks_off()
ax.set_xlabel("구간의 기하 중심 $K_d$ (M, 로그 축) — 왼쪽이 강한 결합",
              fontsize=11.5, color=MUTED, labelpad=10)
ax.set_ylabel("구간 폭 (상한 ÷ 하한)", fontsize=11.5, color=MUTED, labelpad=10)
ax.grid(True, which="major", color="#ebedec", lw=1, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#d8dbd9")

ax.set_title("NanoBind-affi가 내놓을 수 있는 답의 해상도 (눈금 49개가 만드는 구간 48개)",
             fontsize=13.5, color=INK, loc="left", pad=18, x=-0.065)

fig.subplots_adjust(left=0.105, right=0.985, top=0.88, bottom=0.145)
fig.savefig("/tmp/nb/ladder_raw.png", facecolor=SURFACE)
print("saved", tuple(int(v) for v in fig.get_size_inches() * fig.dpi))
print("median fold %.3f  within2x %d/%d  max %.1f at %.3g" %
      (sorted(folds)[len(folds) // 2], sum(f <= 2 for f in folds), len(folds),
       max(folds), mids[w]))

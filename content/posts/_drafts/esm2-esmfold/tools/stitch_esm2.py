"""Stitch the tiled PDF captures of Lin et al. Figure 1 and Figure S8.

Offsets are found by correlating the overlap, not by eye, so the result is a
faithful reproduction of the original figure (required: CC BY-NC-ND).
"""
from PIL import Image
import numpy as np

S = "/tmp/esm2/"


def gray(im):
    return np.asarray(im.convert("L"), dtype=np.int16)


def h_offset(a, b, lo, hi):
    A, B = gray(a), gray(b)
    best, bo = None, None
    for o in range(lo, hi):
        w = min(A.shape[1] - o, B.shape[1])
        if w < 150:
            continue
        h = min(A.shape[0], B.shape[0])
        d = np.abs(A[:h, o:o + w] - B[:h, :w]).mean()
        if best is None or d < best:
            best, bo = d, o
    return bo, best


def v_offset(a, b, lo, hi):
    A, B = gray(a), gray(b)
    best, bo = None, None
    for o in range(lo, hi):
        hh = min(A.shape[0] - o, B.shape[0])
        if hh < 100:
            continue
        w = min(A.shape[1], B.shape[1])
        d = np.abs(A[o:o + hh, :w] - B[:hh, :w]).mean()
        if best is None or d < best:
            best, bo = d, o
    return bo, best


def hcat(a, b, lo, hi):
    o, d = h_offset(a, b, lo, hi)
    print("   h offset", o, "diff", round(d, 2))
    W = max(a.width, o + b.width)
    H = max(a.height, b.height)
    c = Image.new("RGB", (W, H), "white")
    c.paste(a, (0, 0)); c.paste(b, (o, 0))
    return c


def vcat(a, b, lo, hi):
    o, d = v_offset(a, b, lo, hi)
    print("   v offset", o, "diff", round(d, 2))
    H = max(a.height, o + b.height)
    W = max(a.width, b.width)
    c = Image.new("RGB", (W, H), "white")
    c.paste(a, (0, 0)); c.paste(b, (0, o))
    return c


def load(n):
    return Image.open(S + n).convert("RGB")


# ----------------------------------------------------------------- Figure 1
print("Figure 1 rows")
top = hcat(load("f1_TL.png"), load("f1_TR.png"), 120, 1400)
mid = hcat(load("f1_ML.png"), load("f1_MR.png"), 120, 1400)
# bottom tiles were captured from a shorter region, so they came back at a
# slightly different scale — normalise before stitching them to the rest
k = (1527 / 1460) / (1568 / 1460)
bl, br = load("f1_BL.png"), load("f1_BR.png")
bl = bl.resize((round(bl.width * k), round(bl.height * k)), Image.LANCZOS)
br = br.resize((round(br.width * k), round(br.height * k)), Image.LANCZOS)
bot = hcat(bl, br, 120, 1400)

print("Figure 1 columns")
tm = vcat(top, mid, 80, 770)
full = vcat(tm, bot, 200, tm.height - 100)
# trim the white margins
a = np.asarray(full.convert("L"))
mask = a < 245
ys, xs = np.where(mask)
full = full.crop((max(0, xs.min() - 12), max(0, ys.min() - 12),
                  min(full.width, xs.max() + 12), min(full.height, ys.max() + 12)))
full.save(S + "fig1_full.png")
print("Figure 1 ->", full.size)

# ---------------------------------------------------------------- Figure S8
print("Figure S8")
s8 = hcat(load("s8_L.png"), load("s8_R.png"), 40, 500)
a = np.asarray(s8.convert("L"))
mask = a < 245
ys, xs = np.where(mask)
s8 = s8.crop((max(0, xs.min() - 10), max(0, ys.min() - 10),
              min(s8.width, xs.max() + 10), min(s8.height, ys.max() + 10)))
s8.save(S + "figS8_full.png")
print("Figure S8 ->", s8.size)

"""Stitch the three 400% tiles of Figure 2A into one wide panel."""
from PIL import Image
import numpy as np

S = "/tmp/pdf2/"
t1 = Image.open(S + "f2a_1.png").convert("RGB")
t2 = Image.open(S + "f2a_2.png").convert("RGB")
t3 = Image.open(S + "f2a_3.png").convert("RGB")

# t1,t2 captured from a 1110-px-wide frame region; t3 from 920. Match scales.
scale3 = (1568 / 1110) / (1568 / 920)
t3 = t3.resize((round(t3.width * scale3), round(t3.height * scale3)), Image.LANCZOS)
# crop all to the same height
h = min(t1.height, t2.height, t3.height)
t1, t2, t3 = t1.crop((0, 0, t1.width, h)), t2.crop((0, 0, t2.width, h)), t3.crop((0, 0, t3.width, h))


def best_offset(a, b, lo, hi, band=(0, None)):
    """Offset o minimising |a[o:] - b[:w-o]| — i.e. b starts at x=o inside a."""
    A = np.asarray(a.convert("L"), dtype=np.int16)
    B = np.asarray(b.convert("L"), dtype=np.int16)
    y0, y1 = band[0], band[1] or A.shape[0]
    A, B = A[y0:y1], B[y0:y1]
    best, bo = None, None
    for o in range(lo, hi):
        w = min(A.shape[1] - o, B.shape[1])
        if w < 120:
            continue
        d = np.abs(A[:, o:o + w] - B[:, :w]).mean()
        if best is None or d < best:
            best, bo = d, o
    return bo, best


o2, d2 = best_offset(t1, t2, 300, t1.width - 150)
print("t2 starts at", o2, "diff", round(d2, 2))

# build t1+t2 first
W12 = o2 + t2.width
c12 = Image.new("RGB", (W12, h), "white")
c12.paste(t1, (0, 0))
c12.paste(t2, (o2, 0))

o3, d3 = best_offset(c12, t3, 600, c12.width - 150)
print("t3 starts at", o3, "diff", round(d3, 2))

W = o3 + t3.width
out = Image.new("RGB", (W, h), "white")
out.paste(c12, (0, 0))
out.paste(t3, (o3, 0))
out.save(S + "f2a_stitched.png")
print("stitched", out.size)

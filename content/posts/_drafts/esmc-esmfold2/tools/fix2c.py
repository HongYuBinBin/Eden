import sys
sys.path.insert(0, "/tmp/gen")
from ink import *
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"
im = load(P + "fig2c_raw.png", scale=1.4)
s = im.width / 1568.0
c = Image.new("RGB", (im.width, im.height + int(150 * s)), "white"); c.paste(im, (0, 0)); im = c
H0 = int(693 * s); X = lambda v: v * s
box(im, 1, (X(172), X(196), X(278), X(556)), pad=3, dash=True)
box(im, 4, (X(398), X(232), X(432), X(556)), pad=3, dash=True)
memo_w(im, "MSA 없이 50", (X(150), X(138)), size=int(X(30)), col=MK[1])
memo_w(im, "MSA 쓴 AF3 는 47", (X(330), X(168)), size=int(X(29)), col=MK[4])
memo(im, "항체-항원에서만 뒤집힌다. 단백질-단백질은 아직 MSA 쪽이 앞선다 (70 vs 73)",
     (X(60), H0 + X(18)), size=int(X(31)), col=INK)
save(im, P + "fig2c_annot.jpg", maxw=1500)

import sys
sys.path.insert(0, "/tmp/gen")
from ink import *
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"
im = load(P + "figS13_raw.png")
s = im.width / 1568.0
c = Image.new("RGB", (im.width, im.height + int(120 * s)), "white"); c.paste(im, (0, 0)); im = c
H0 = int(569 * s); X = lambda v: v * s
box(im, 1, (X(330), X(200), X(500), X(260)), pad=4, dash=True)
memo(im, "16회 넘으면 평평하다", (X(250), X(140)), size=int(X(30)), col=MK[1])
memo(im, "루프는 16까지, 확산 스텝은 12 넘으면 거의 안 변한다", (X(30), H0 + X(14)), size=int(X(30)), col=INK)
save(im, P + "figS13_annot.jpg", maxw=900)

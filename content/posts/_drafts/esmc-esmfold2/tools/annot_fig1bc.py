import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"
im = load(P + "fig1bc_raw.png", scale=1.3)
s = im.width / 1568.0
c = Image.new("RGB", (im.width, im.height + int(210 * s)), "white")
c.paste(im, (0, 0))
im = c
H0 = int(636 * s)
X = lambda v: v * s

# --- panel B
memo(im, "개발용 소형 모델 5개로 먼저 곡선을 긋고\n(P@L-LR = 0.115 log10(FLOPs) - 1.98, R2 = 0.99)\n그 곡선 위에서 300M / 600M / 6B 를 골랐다",
     (X(60), H0 + X(18)), size=int(X(30)), col=MK[3])
box(im, 3, (X(560), X(95), X(760), X(205)), pad=4, dash=True)
arrow(im, (X(300), H0 + X(10)), (X(640), X(215)), col=MK[3], w=int(X(3)), head=int(X(13)), curve=X(60))
memo(im, "6B 실측이 외삽과 0.007 차이", (X(555), X(52)), size=int(X(27)), col=MK[3])

# --- panel C
d = ImageDraw.Draw(im, "RGBA")
d.ellipse([X(1410), X(98), X(1462), X(150)], outline=MK[5], width=int(X(4)))      # ESMC 6B endpoint
memo(im, "0.72", (X(1468), X(98)), size=int(X(28)), col=MK[5])
box(im, 2, (X(1330), X(270), X(1540), X(305)), pad=2, dash=True)                  # ESM2 plateau
memo(im, "0.59 에서 평평", (X(1240), X(315)), size=int(X(27)), col=MK[2])
memo(im, "같은 지표(P@L)로 ESM2 와 ESMC 를 나란히 놓은 그림.\nESM2 는 15B 에서 이미 누웠고, ESMC 는 6B 에서도 오른다.",
     (X(1000), H0 + X(18)), size=int(X(30)), col=MK[1])
arrow(im, (X(1230), H0 + X(10)), (X(1400), X(345)), col=MK[1], w=int(X(3)), head=int(X(13)), curve=X(-40))

save(im, P + "fig1bc_annot.jpg", maxw=1500)

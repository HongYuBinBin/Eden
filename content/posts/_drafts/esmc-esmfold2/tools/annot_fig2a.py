import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"
im = load(P + "fig2a_raw.png", scale=1.6)   # 1568x326 -> 2509x522
W, H = im.size
print("canvas", W, H)

# add headroom below for memos
pad_b = 250
canvas = Image.new("RGB", (W, H + pad_b), "white")
canvas.paste(im, (0, 0))
im = canvas

sx = W / 1568.0
sy = sx


def X(v):
    return v * sx


def Y(v):
    return v * sy


# ---- component boxes (coords measured on the 1568x326 capture) ----
box(im, 1, (X(10), Y(100), X(200), Y(255)), pad=6, fill=True)          # ESMC layer stack
box(im, 2, (X(225), Y(105), X(420), Y(265)), pad=6, fill=True)         # single rep + 2D pair rep
box(im, 3, (X(930), Y(120), X(1115), Y(235)), pad=6, fill=True)        # folding layers (48)
box(im, 3, (X(600), Y(48), X(1180), Y(80)), pad=4, dash=True)          # stable recurrent update arrow
box(im, 4, (X(1385), Y(28), X(1560), Y(175)), pad=5, fill=True)        # diffusion transformer

marker(im, 1, (X(30), Y(92)), r=X(21))
marker(im, 2, (X(243), Y(97)), r=X(21))
marker(im, 3, (X(948), Y(112)), r=X(21))
marker(im, 4, (X(1402), Y(20)), r=X(21))

# ---- handwritten memos under the figure ----
memo(im, "얼려둔 ESMC 6B\n80층 x 2560", (X(20), H + 10), size=int(X(27)), col=MK[1])
memo(im, "81개 층 표현을\nsoftmax 가중합 -> 256차 pair", (X(225), H + 10), size=int(X(27)), col=MK[2])
memo(im, "ESMFold 에서 가져온 방식", (X(225), H + 115), size=int(X(25)), col="#6b6b6b")

memo(im, "루프: 학습 Poisson(3), 추론 10~64회\n수축 사상이라 폭발하지 않는다", (X(760), H + 10), size=int(X(27)), col=MK[3])
memo(im, "코드 기본값은 24층 / 20루프", (X(760), H + 115), size=int(X(25)), col=RED)

memo(im, "확산 68스텝으로\n원자 좌표까지", (X(1360), H + 10), size=int(X(27)), col=MK[4])

# arrows from memos up to the boxes
arrow(im, (X(60), H + 4), (X(70), Y(262)), col=MK[1], w=int(X(3)), head=int(X(13)))
arrow(im, (X(300), H + 4), (X(320), Y(272)), col=MK[2], w=int(X(3)), head=int(X(13)))
arrow(im, (X(880), H + 4), (X(1000), Y(243)), col=MK[3], w=int(X(3)), head=int(X(13)), curve=X(30))
arrow(im, (X(1430), H + 4), (X(1460), Y(183)), col=MK[4], w=int(X(3)), head=int(X(13)))

# the missing confidence head
memo_w(im, "pLDDT / PAE 신뢰도 헤드(4층)는\n이 그림에 아예 없다", (X(1180), Y(250)), size=int(X(26)), col=RED)

save(im, P + "fig2a_annot.jpg", maxw=1500)

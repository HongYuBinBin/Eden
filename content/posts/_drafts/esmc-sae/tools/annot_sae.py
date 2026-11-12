import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-sae/imgs/"


def room(im, bottom=0):
    c = Image.new("RGB", (im.width, im.height + bottom), "white")
    c.paste(im, (0, 0))
    return c


# ---------------------------------------------------------------- Fig 4 A/C/D
im = load(P + "fig4acd_raw.png", scale=1.45)          # 1029 -> 1492
s = im.width / 1029.0
H0 = im.height
im = room(im, int(150 * s))
X = lambda v: v * s

marker(im, 1, (X(72), X(24)), r=X(19))
marker(im, 2, (X(72), X(512)), r=X(19))
marker(im, 3, (X(72), X(795)), r=X(19))

box(im, 1, (X(150), X(120), X(300), X(360)), pad=3, dash=True)
memo_w(im, "1 잔기만 켜지는 보편 특징", (X(120), X(455)), size=int(X(21)), col=MK[1])
box(im, 1, (X(300), X(130), X(430), X(230)), pad=3, dash=True)
memo_w(im, "도메인 전체에 걸친\n패밀리 특이 특징", (X(440), X(140)), size=int(X(21)), col=MK[1])

memo_w(im, "같은 특징 하나가 접힘이 전혀 다른\n네 단백질의 촉매 자리에서 켜진다", (X(560), X(540)), size=int(X(22)), col=MK[2])

memo_w(im, "사전 크기를 키우면 특징 하나가\n여러 개로 쪼개진다", (X(560), X(1010)), size=int(X(22)), col=MK[3])

memo(im, "왼쪽 라벨: 8개 범주로 분류한 16,384개 특징. 합이 16,240개로 사전을 거의 채운다",
     (X(30), H0 + X(18)), size=int(X(24)), col=INK)
memo(im, "분류는 GPT-5 가 특징 설명문을 읽고 한 것이고, 설명문은 SwissProt 주석에서 나왔다",
     (X(30), H0 + X(60)), size=int(X(24)), col=RED)
save(im, P + "fig4acd_annot.jpg", maxw=1500)

# ---------------------------------------------------------------- Fig 4E
im = load(P + "fig4e_raw.png", scale=1.0)
s = im.width / 1568.0
H0 = im.height
im = room(im, int(160 * s))
X = lambda v: v * s

box(im, 4, (X(70), X(45), X(600), X(455)), pad=4, dash=True)
box(im, 5, (X(1000), X(40), X(1560), X(730)), pad=4, dash=True)
memo(im, "P-loop 한 군데에 특징 11개. 위로 갈수록 보편, 아래로 갈수록 키나아제 전용",
     (X(40), H0 + X(10)), size=int(X(25)), col=MK[4])
memo(im, "촉매부는 일곱 패밀리가 공유하고, 갈리는 곳은 조절부다. CK1a 만 촉매부에서도 다른 특징을 켠다",
     (X(40), H0 + X(52)), size=int(X(25)), col=MK[5])
arrow(im, (X(300), H0 + X(4)), (X(330), X(470)), col=MK[4], w=int(X(3)), head=int(X(12)))
arrow(im, (X(900), H0 + X(46)), (X(1050), X(745)), col=MK[5], w=int(X(3)), head=int(X(12)), curve=X(30))
save(im, P + "fig4e_annot.jpg", maxw=1500)

# ---------------------------------------------------------------- Fig S26
im = load(P + "figS26_raw.png", scale=0.9)
s = im.width / 1568.0
H0 = im.height
im = room(im, int(120 * s))
X = lambda v: v * s
box(im, 3, (X(560), X(60), X(760), X(430)), pad=3, dash=True)
box(im, 3, (X(1230), X(60), X(1360), X(430)), pad=3, dash=True)
memo(im, "60~70층이 가장 복원하기 어렵고, 망가뜨렸을 때 perplexity 손해도 가장 크다",
     (X(40), H0 + X(14)), size=int(X(30)), col=MK[3])
save(im, P + "figS26_annot.jpg", maxw=900)

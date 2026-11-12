import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"


def canvas_with_room(im, bottom=0, top=0, right=0):
    c = Image.new("RGB", (im.width + right, im.height + bottom + top), "white")
    c.paste(im, (0, top))
    return c


# ---------------------------------------------------------------- Fig 1B/1C
im = load(P + "fig1bc_raw.png", scale=1.3)          # 1568x636 -> 2038x827
s = im.width / 1568.0
im = canvas_with_room(im, bottom=int(210 * s))
H0 = int(636 * s)
X = lambda v: v * s
memo(im, "개발용 소형 모델 5개로 먼저 곡선을 긋고\n(P@L-LR = 0.115 log10(FLOPs) - 1.98, R2 = 0.99)\n그 곡선 위에서 300M / 600M / 6B 를 골랐다",
     (X(60), H0 + X(18)), size=int(X(30)), col=MK[3])
box(im, 3, (X(560), X(95), X(760), X(205)), pad=4, dash=True)
arrow(im, (X(300), H0 + X(10)), (X(640), X(215)), col=MK[3], w=int(X(3)), head=int(X(13)), curve=X(60))
memo(im, "6B 실측이 외삽과 0.007 차이", (X(560), X(55)), size=int(X(27)), col=MK[3])

memo(im, "ESM2 는 15B 에서 이미 누웠고 (0.59)\nESMC 는 6B 에서도 계속 오른다 (0.72)",
     (X(1020), H0 + X(18)), size=int(X(30)), col=MK[1])
underline(im, (X(1330), X(120), X(1450), X(150)), col=MK[1], w=int(X(4)))
underline(im, (X(1380), X(285), X(1500), X(310)), col=MK[2], w=int(X(4)))
arrow(im, (X(1180), H0 + X(10)), (X(1400), X(330)), col=MK[1], w=int(X(3)), head=int(X(13)), curve=X(-50))
save(im, P + "fig1bc_annot.jpg", maxw=1500)

# ---------------------------------------------------------------- Fig 1D
im = load(P + "fig1d_raw.png", scale=1.3)
s = im.width / 1372.0
im = canvas_with_room(im, bottom=int(150 * s))
H0 = int(885 * s)
X = lambda v: v * s
memo_w(im, "기능(EC)은 50~60층에서 최고", (X(700), X(130)), size=int(X(30)), col=MK[2])
arrow(im, (X(830), X(175)), (X(880), X(215)), col=MK[2], w=int(X(3)), head=int(X(12)))
memo_w(im, "구조는 거의 끝까지 안 나오다가\n50층 넘어서 솟는다", (X(880), X(560)), size=int(X(30)), col=MK[5])
arrow(im, (X(1090), X(640)), (X(1130), X(430)), col=MK[5], w=int(X(3)), head=int(X(12)), curve=X(30))
memo(im, "ESMFold2 가 마지막 층만 쓰지 않고 81개 층을 전부 받아가는 이유",
     (X(60), H0 + X(20)), size=int(X(31)), col=INK)
save(im, P + "fig1d_annot.jpg", maxw=1200)

# ---------------------------------------------------------------- Fig 2C
im = load(P + "fig2c_raw.png", scale=1.4)
s = im.width / 1568.0
im = canvas_with_room(im, bottom=int(150 * s))
H0 = int(693 * s)
X = lambda v: v * s
box(im, 1, (X(150), X(185), X(275), X(560)), pad=3, dash=True)      # single-seq ESMFold2 group
box(im, 4, (X(355), X(230), X(420), X(560)), pad=3, dash=True)      # AlphaFold3 (MSA)
memo_w(im, "MSA 없이 50", (X(120), X(120)), size=int(X(30)), col=MK[1])
memo_w(im, "MSA 쓴 AF3 는 47", (X(300), X(165)), size=int(X(30)), col=MK[4])
memo(im, "항체-항원에서만 뒤집힌다. 단백질-단백질은 아직 MSA 쪽이 앞선다 (70 vs 73)",
     (X(60), H0 + X(18)), size=int(X(31)), col=INK)
save(im, P + "fig2c_annot.jpg", maxw=1500)

# ---------------------------------------------------------------- Fig 2D
im = load(P + "fig2d_raw.png", scale=1.3)
s = im.width / 1368.0
im = canvas_with_room(im, bottom=int(150 * s))
H0 = int(896 * s)
X = lambda v: v * s
memo_w(im, "시드 1개 49 -> 1000개 65", (X(150), X(230)), size=int(X(30)), col=MK[5])
arrow(im, (X(150), X(290)), (X(105), X(560)), col=MK[5], w=int(X(3)), head=int(X(12)), curve=X(-25))
arrow(im, (X(400), X(285)), (X(560), X(285)), col=MK[5], w=int(X(3)), head=int(X(12)))
box(im, 1, (X(560), X(255), X(640), X(330)), pad=3, dash=True)
memo_w(im, "Fast 가 큰 모델을 따라잡는 지점", (X(330), X(390)), size=int(X(28)), col=MK[1])
memo(im, "추론 때 샘플을 늘리는 것만으로 16%p. 다만 루프마다 LM 드롭아웃이 켜져 있다",
     (X(60), H0 + X(18)), size=int(X(30)), col=INK)
save(im, P + "fig2d_annot.jpg", maxw=1400)

# ---------------------------------------------------------------- Fig 2E (crop off the panel-D slice)
im = load(P + "fig2e_raw.png")
im = im.crop((168, 60, 1148, 1059))
im = im.resize((int(im.width * 1.3), int(im.height * 1.3)), Image.LANCZOS)
s = im.width / 980.0
im = canvas_with_room(im, bottom=int(140 * s))
H0 = im.height - int(140 * s)
X = lambda v: v * s
memo_w(im, "1024 잔기에서\nESMFold2 15.8초\nFast 9.4초", (X(690), X(330)), size=int(X(30)), col=MK[4])
arrow(im, (X(900), X(470)), (X(915), X(690)), col=MK[4], w=int(X(3)), head=int(X(12)))
memo(im, "H100 한 장 기준, MSA 검색 시간은 빠져 있다. Chai-1(110초)은 그래프에서 제외",
     (X(30), H0 + X(16)), size=int(X(28)), col=RED)
save(im, P + "fig2e_annot.jpg", maxw=1100)

# ---------------------------------------------------------------- Fig 3A
im = load(P + "fig3a_raw.png", scale=1.25)
s = im.width / 1568.0
im = canvas_with_room(im, bottom=int(140 * s))
H0 = int(725 * s)
X = lambda v: v * s
box(im, 1, (X(1210), X(480), X(1270), X(540)), pad=4, dash=True)
memo_w(im, "PD-L1 scFv 만 제자리", (X(1000), X(400)), size=int(X(29)), col=MK[1])
arrow(im, (X(1190), X(445)), (X(1235), X(478)), col=MK[1], w=int(X(3)), head=int(X(12)))
memo(im, "탐색 계산을 늘리면 10쌍 중 9쌍이 좋아진다. 미니바인더 53.8 -> 70.0%, scFv 12.1 -> 21.0%",
     (X(40), H0 + X(16)), size=int(X(29)), col=INK)
save(im, P + "fig3a_annot.jpg", maxw=1400)

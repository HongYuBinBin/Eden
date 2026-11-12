"""Annotate the high-resolution PDF captures for the ESMC + ESMFold2 post."""
import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

S = "/tmp/pdf2/"
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"


def room(im, bottom):
    c = Image.new("RGB", (im.width, im.height + bottom), "white")
    c.paste(im, (0, 0))
    return c


# ---------------------------------------------------------------- Fig 1B + 1C
b = load(S + "f1b.png")
c = load(S + "f1c.png")
h = min(b.height, c.height)
b = b.crop((0, 0, b.width, h)); c = c.crop((0, 0, c.width, h))
gap = 50
im = Image.new("RGB", (b.width + gap + c.width, h + 200), "white")
im.paste(b, (0, 0)); im.paste(c, (b.width + gap, 0))
ox = b.width + gap
H0 = h

box(im, 3, (330, 540, 700, 800), pad=6, dash=True)
memo(im, "먼저 작은 모델 다섯 개로 곡선을 긋고 (P@L-LR = 0.115 log10(FLOPs) - 1.98, R2 = 0.99)",
     (14, H0 + 20), size=31, col=MK[3])
memo(im, "그 곡선 위에서 300M / 600M / 6B 를 골랐다. 6B 실측은 외삽과 0.007 차이뿐이다",
     (14, H0 + 70), size=31, col=INK)
arrow(im, (300, H0 + 12), (380, 812), col=MK[3], w=4, head=14)

d = ImageDraw.Draw(im, "RGBA")
d.ellipse([ox + 930, 150, ox + 1020, 240], outline=MK[5], width=5)
memo_w(im, "0.72", (ox + 960, 90), size=32, col=MK[5])
box(im, 2, (ox + 800, 420, ox + 1180, 485), pad=4, dash=True)
memo_w(im, "0.59 에서 평평", (ox + 830, 520), size=30, col=MK[2])
memo(im, "같은 지표로 ESM2 와 ESMC 를 나란히. ESM2 는 15B 에서 이미 누웠고 ESMC 는 6B 에서도 오른다",
     (ox + 14, H0 + 20), size=31, col=MK[1])
save(im, P + "fig1bc_annot.jpg", maxw=1600)

# ---------------------------------------------------------------- Fig 1D
im = load(S + "f1d.png")
H0 = im.height
im = room(im, 130)
memo_w(im, "기능(EC)은 50~60층에서 최고", (620, 95), size=30, col=MK[2])
arrow(im, (800, 150), (845, 180), col=MK[2], w=4, head=14)
memo_w(im, "구조는 거의 끝까지 안 나오다가\n50층 넘어서 솟는다", (830, 560), size=30, col=MK[5])
arrow(im, (1030, 640), (1010, 440), col=MK[5], w=4, head=14, curve=40)
memo(im, "ESMFold2 가 마지막 층만 쓰지 않고 81개 층을 전부 받아가는 이유",
     (14, H0 + 16), size=32, col=INK)
save(im, P + "fig1d_annot.jpg", maxw=1340)

# ---------------------------------------------------------------- Fig 2A
im = load(S + "f2a_stitched.png")     # 3008 x 608
H0 = im.height
im = room(im, 330)

box(im, 1, (10, 230, 360, 480), pad=6, fill=True)
box(im, 2, (420, 230, 730, 540), pad=6, fill=True)
box(im, 3, (1745, 285, 1995, 455), pad=6, fill=True)
box(im, 3, (1180, 120, 2160, 180), pad=4, dash=True)
box(im, 4, (2460, 95, 2865, 290), pad=6, fill=True)

marker(im, 1, (32, 206), r=26)
marker(im, 2, (436, 206), r=26)
marker(im, 3, (1760, 262), r=26)
marker(im, 4, (2476, 70), r=26)

memo(im, "얼려둔 ESMC 6B\n80층 x 2560", (20, H0 + 22), size=34, col=MK[1])
memo(im, "81개 층 표현을 softmax 가중합\n-> 256차 pair 표현", (470, H0 + 22), size=34, col=MK[2])
memo(im, "ESMFold 에서 가져온 방식", (470, H0 + 142), size=30, col="#6b6b63")
memo(im, "루프: 학습 Poisson(3), 추론 10~64회\n수축 사상이라 폭발하지 않는다", (1450, H0 + 22), size=34, col=MK[3])
memo(im, "코드 기본값은 24층 / 20루프", (1450, H0 + 142), size=30, col=RED)
memo(im, "확산 68스텝으로\n원자 좌표까지", (2500, H0 + 22), size=34, col=MK[4])

arrow(im, (120, H0 + 14), (140, 492), col=MK[1], w=4, head=15)
arrow(im, (560, H0 + 14), (580, 552), col=MK[2], w=4, head=15)
arrow(im, (1700, H0 + 14), (1860, 470), col=MK[3], w=4, head=15, curve=40)
arrow(im, (2600, H0 + 14), (2650, 302), col=MK[4], w=4, head=15)

memo(im, "pLDDT / PAE 신뢰도 헤드(4층)는 이 그림에 아예 없다", (2250, H0 + 142), size=30, col=RED)
save(im, P + "fig2a_annot.jpg", maxw=1600)

# ---------------------------------------------------------------- Fig 2B (new)
im = load(S + "f2b.png")
H0 = im.height
im = room(im, 140)
memo(im, "언어모델 학습 FLOPs 하나만 바꾸고 폴딩 모델은 구조도 데이터도 계산량도 고정했다",
     (14, H0 + 16), size=30, col=INK)
memo(im, "단 12점이다. 세 크기 x 체크포인트 네 개, 같은 학습 곡선 위의 점들은 서로 독립이 아니다",
     (14, H0 + 66), size=30, col=RED)
save(im, P + "fig2b_annot.jpg", maxw=1280)

# ---------------------------------------------------------------- Fig 2C
im = load(S + "f2c.png")
H0 = im.height
im = room(im, 130)
box(im, 1, (182, 225, 332, 650), pad=4, dash=True)
box(im, 4, (420, 285, 527, 650), pad=4, dash=True)
memo_w(im, "MSA 없이 50", (150, 92), size=30, col=MK[1])
memo_w(im, "MSA 쓴 AF3 는 47", (340, 170), size=29, col=MK[4])
memo(im, "항체-항원에서만 뒤집힌다. 단백질-단백질은 아직 MSA 쪽이 앞선다 (70 vs 73)",
     (14, H0 + 16), size=31, col=INK)
save(im, P + "fig2c_annot.jpg", maxw=1340)

# ---------------------------------------------------------------- Fig 2D
im = load(S + "f2d.png")
H0 = im.height
im = room(im, 210)
box(im, 5, (90, 500, 170, 580), pad=4, dash=True)
box(im, 1, (600, 190, 680, 260), pad=4, dash=True)
memo(im, "시드 1개 49 -> 1000개 65", (14, H0 + 14), size=31, col=MK[5])
memo(im, "오른쪽 위 네모가 Fast 가 큰 모델을 따라잡는 지점이다", (14, H0 + 64), size=31, col=MK[1])
memo(im, "추론 때 샘플을 늘리는 것만으로 16%p. 다만 루프마다 LM 드롭아웃이 켜져 있다",
     (14, H0 + 122), size=31, col=INK)
arrow(im, (120, H0 + 8), (130, 592), col=MK[5], w=4, head=14)
arrow(im, (520, H0 + 58), (628, 272), col=MK[1], w=4, head=14, curve=60)
save(im, P + "fig2d_annot.jpg", maxw=1400)

# ---------------------------------------------------------------- Fig 2E
im = load(S + "f2e.png")
H0 = im.height
im = room(im, 200)
box(im, 4, (995, 770, 1075, 880), pad=4, dash=True)
memo(im, "1024 잔기에서 ESMFold2 15.8초, Fast 9.4초",
     (14, H0 + 14), size=30, col=MK[4])
memo(im, "H100 한 장 기준, MSA 검색 시간은 빠져 있다",
     (14, H0 + 64), size=30, col=RED)
memo(im, "Chai-1(1024 잔기에서 110초)은 그래프에서 제외됐다",
     (14, H0 + 114), size=30, col=INK)
arrow(im, (700, H0 + 8), (1000, 890), col=MK[4], w=4, head=14, curve=-40)
save(im, P + "fig2e_annot.jpg", maxw=1120)

# ---------------------------------------------------------------- Fig 3A
im = load(S + "f3a.png")
H0 = im.height
im = room(im, 130)
box(im, 1, (1290, 510, 1360, 580), pad=4, dash=True)
memo_w(im, "PD-L1 scFv 만 제자리", (1050, 420), size=29, col=MK[1])
arrow(im, (1250, 465), (1305, 515), col=MK[1], w=4, head=13)
memo(im, "탐색 계산을 늘리면 10쌍 중 9쌍이 좋아진다. 미니바인더 53.8 -> 70.0%, scFv 12.1 -> 21.0%",
     (14, H0 + 16), size=30, col=INK)
save(im, P + "fig3a_annot.jpg", maxw=1534)

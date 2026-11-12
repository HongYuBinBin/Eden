"""Redraw the memos on Fig 1B/1C, 2A and 2E at a size that survives downscaling.

Rule used here: the handwriting should land at about 26 px once the page
displays the figure, and the file should be roughly twice the display width so
it stays sharp on a HiDPI screen.
"""
import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

S = "/tmp/pdf2/"
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-esmfold2/imgs/"


def room(im, bottom):
    c = Image.new("RGB", (im.width, im.height + bottom), "white")
    c.paste(im, (0, 0))
    return c


# ================================================================ Fig 2A
# canvas 3008 wide, saved at 2400, shown at 1120 -> memo 70 px here = 26 px on screen
im = load(S + "f2a_stitched.png")
H0 = im.height
im = room(im, 560)

box(im, 1, (10, 230, 360, 480), pad=8, fill=True)
box(im, 2, (420, 230, 730, 540), pad=8, fill=True)
box(im, 3, (1745, 285, 1995, 455), pad=8, fill=True)
box(im, 3, (1180, 120, 2160, 180), pad=5, dash=True)
box(im, 4, (2460, 95, 2865, 290), pad=8, fill=True)

marker(im, 1, (34, 200), r=34)
marker(im, 2, (440, 200), r=34)
marker(im, 3, (1726, 250), r=34)
marker(im, 4, (2484, 62), r=34)

M = 70
marker(im, 1, (56, H0 + 86), r=40)
memo(im, "얼려둔 ESMC 6B, 80층 x 2560", (130, H0 + 40), size=M, col=MK[1])

marker(im, 3, (1586, H0 + 86), r=40)
memo(im, "루프: 학습 Poisson(3), 추론 10~64회\n수축 사상이라 폭발하지 않는다", (1660, H0 + 40), size=M, col=MK[3])

marker(im, 2, (56, H0 + 280), r=40)
memo(im, "81개 층 표현을 softmax 가중합\n-> 256차 pair 표현 (ESMFold 방식)", (130, H0 + 234), size=M, col=MK[2])

marker(im, 4, (1586, H0 + 280), r=40)
memo(im, "확산 68스텝으로 원자 좌표까지", (1660, H0 + 234), size=M, col=MK[4])

memo(im, "코드 기본값은 24층 / 20루프이고, 신뢰도 헤드(pLDDT, PAE) 4층은 이 그림에 아예 없다",
     (130, H0 + 440), size=64, col=RED)

arrow(im, (180, H0 + 30), (200, 500), col=MK[1], w=6, head=22)
arrow(im, (1800, H0 + 30), (1880, 475), col=MK[3], w=6, head=22)
save(im, P + "fig2a_annot.jpg", maxw=2400, q=90)

# ================================================================ Fig 1B + 1C
b = load(S + "f1b.png"); c = load(S + "f1c.png")
h = min(b.height, c.height)
b = b.crop((0, 0, b.width, h)); c = c.crop((0, 0, c.width, h))
gap = 50
W = b.width + gap + c.width            # 2458
im = Image.new("RGB", (W, h + 330), "white")
im.paste(b, (0, 0)); im.paste(c, (b.width + gap, 0))
ox = b.width + gap
H0 = h

box(im, 3, (330, 540, 700, 800), pad=7, dash=True)
d = ImageDraw.Draw(im, "RGBA")
d.ellipse([ox + 925, 145, ox + 1025, 245], outline=MK[5], width=7)
memo_w(im, "0.72", (ox + 955, 60), size=58, col=MK[5])
box(im, 2, (ox + 800, 420, ox + 1180, 485), pad=6, dash=True)
memo_w(im, "0.59 에서 평평", (ox + 800, 510), size=54, col=MK[2])

M = 57
memo(im, "작은 모델 다섯 개로 그은 곡선 위에서 300M / 600M / 6B 를 골랐다", (20, H0 + 30), size=M, col=MK[3])
memo(im, "6B 실측은 외삽과 0.007 차이뿐이다 (P@L-LR = 0.115 log10 FLOPs - 1.98, R2 = 0.99)",
     (20, H0 + 130), size=M, col=INK)
memo(im, "ESM2 는 15B 에서 이미 누웠고(0.59), ESMC 는 6B 에서도 오른다(0.72)",
     (20, H0 + 230), size=M, col=MK[1])
arrow(im, (420, H0 + 22), (470, 812), col=MK[3], w=6, head=20)
save(im, P + "fig1bc_annot.jpg", maxw=2240, q=90)

# ================================================================ Fig 2E
im = load(S + "f2e.png")               # 1120 wide, shown at 643
H0 = im.height
im = room(im, 300)
box(im, 4, (995, 770, 1075, 880), pad=5, dash=True)
M = 45
memo(im, "1024 잔기에서 ESMFold2 15.8초, Fast 9.4초", (14, H0 + 20), size=M, col=MK[4])
memo(im, "H100 한 장 기준, MSA 검색 시간은 빠져 있다", (14, H0 + 115), size=M, col=RED)
memo(im, "Chai-1 은 1024 잔기에서 110초라 그래프에서 빠졌다", (14, H0 + 210), size=M, col=INK)
arrow(im, (700, H0 + 12), (1000, 890), col=MK[4], w=5, head=18, curve=-40)
save(im, P + "fig2e_annot.jpg", maxw=1120, q=90)

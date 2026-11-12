"""Annotate the high-resolution PDF captures for the SAE post."""
import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

S = "/tmp/pdfcaps/"
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-sae/imgs/"


def room(im, bottom):
    c = Image.new("RGB", (im.width, im.height + bottom), "white")
    c.paste(im, (0, 0))
    return c


# ---------------------------------------------------------------- 4A
im = load(S + "A.png")                      # 1204 x 999
im = im.crop((0, 0, 1204, 960))
H0 = im.height
im = room(im, 130)
box(im, 1, (300, 150, 470, 830), pad=4, dash=True)
box(im, 1, (470, 170, 790, 520), pad=4, dash=True)
memo_w(im, "도메인 전체에 걸친\n패밀리 특이 특징", (800, 180), size=30, col=MK[1])
memo(im, "가로는 한 번에 몇 잔기나 연속으로 켜지는가, 세로는 특정 패밀리에만 켜지는가",
     (16, H0 + 14), size=30, col=INK)
memo(im, "왼쪽 아래, 1 잔기만 그리고 보편적으로 켜지는 구석이 해석에 가장 쓸모 있다",
     (16, H0 + 62), size=30, col=MK[1])
arrow(im, (330, H0 + 56), (360, 845), col=MK[1], w=3, head=13)
save(im, P + "fig4a_annot.jpg", maxw=1204)

# ---------------------------------------------------------------- 4C
im = load(S + "C.png")                      # 1568 x 601
H0 = im.height
im = room(im, 120)
underline(im, (70, 0, 1420, 420), col=MK[2], w=3)
memo(im, "접힘도, 반응도, 친핵체 잔기도 다른 네 단백질. 켜지는 특징은 F6716 하나로 같다",
     (16, H0 + 12), size=31, col=MK[2])
memo(im, "서열로도 구조로도 묶이지 않는 넷을 촉매 기하 하나로 묶어낸 셈이다",
     (16, H0 + 60), size=31, col=INK)
save(im, P + "fig4c_annot.jpg", maxw=1500)

# ---------------------------------------------------------------- 4D
im = load(S + "D.png")                      # 1403 x 840
H0 = im.height
im = room(im, 120)
box(im, 3, (590, 420, 900, 740), pad=4, dash=True)
memo_w(im, "같은 방향을 2^13 에서는 큰 점 하나가,\n2^16 에서는 작은 점 여럿이 덮는다", (930, 300), size=27, col=MK[3])
memo(im, "F6716 주변을 디코더 공간에서 본 것. 점 크기가 사전 크기다",
     (16, H0 + 12), size=30, col=INK)
memo(im, "사전을 키우면 특징 하나가 열 개로 쪼개진다. 개념의 경계는 모델이 정하는가, 사전 크기가 정하는가",
     (16, H0 + 60), size=30, col=RED)
save(im, P + "fig4d_annot.jpg", maxw=1400)

# ---------------------------------------------------------------- 4E, two figures
ladder = load(S + "E_ladder.png")
H0 = ladder.height
im = room(ladder, 120)
marker(im, 4, (36, 34), r=26)
memo(im, "P-loop 한 군데에 특징 11개가 걸린다",
     (12, H0 + 12), size=30, col=MK[4])
memo(im, "위로 갈수록 보편, 아래로 갈수록 키나아제 전용. F3614 와 F119 가 아래 그림의 주인공이다",
     (12, H0 + 58), size=30, col=INK)
save(im, P + "fig4e1_annot.jpg", maxw=1257)

camk1 = load(S + "E_camk1.png")
tk = load(S + "E_tk_agc.png")
tkl = load(S + "E_tkl_ck1.png")

def fit(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)

wr = 1280
tk = tk.resize((wr, round(tk.height * wr / tk.width)), Image.LANCZOS)
tkl = tkl.resize((wr, round(tkl.height * wr / tkl.width)), Image.LANCZOS)
right = Image.new("RGB", (wr, tk.height + 24 + tkl.height), "white")
right.paste(tk, (0, 0)); right.paste(tkl, (0, tk.height + 24))

h = max(camk1.height, right.height)
camk1 = fit(camk1, h)
right = fit(right, h)
gap = 50
W = camk1.width + gap + right.width
im = Image.new("RGB", (W, h + 130), "white")
im.paste(camk1, (0, 0))
im.paste(right, (camk1.width + gap, 0))
marker(im, 5, (camk1.width + gap + 26, 150), r=26)
memo(im, "촉매부는 일곱 패밀리가 공유하고, 갈리는 곳은 조절부다. CK1a 만 촉매부에서도 다른 특징을 켠다",
     (12, h + 16), size=34, col=MK[5])
memo(im, "왼쪽 CAMK1 에서 잔기당 특징 밀도는 알파C 나선 22.4, P-loop 21.3, HRD 20.0, DFG 19.7 순이다",
     (12, h + 68), size=32, col=INK)
save(im, P + "fig4e2_annot.jpg", maxw=1600)

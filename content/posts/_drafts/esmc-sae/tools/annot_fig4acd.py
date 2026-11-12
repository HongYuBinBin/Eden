import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

T = "/tmp/claude-tool-results/568ceda1-884c-5789-b35d-d05ab46fa522/"
RAW_AC = T + "mcp-claude-in-chrome-blob-1794464977982-s20obr-bccc3b39.png"   # A, C (+B labels)
RAW_D = T + "mcp-claude-in-chrome-blob-1794465478563-4wz6ig-051920db.png"    # D
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-sae/imgs/"

src = Image.open(RAW_AC).convert("RGB")

# ---------------------------------------------------------------- 4A
A = src.crop((0, 8, 700, 468))
A = A.resize((A.width * 2, A.height * 2), Image.LANCZOS)
s = 2.0
X = lambda v: v * s
im = Image.new("RGB", (A.width, A.height + int(110 * s)), "white")
im.paste(A, (0, 0))
H0 = A.height
box(im, 1, (X(150), X(108), X(300), X(348)), pad=4, dash=True)
arrow(im, (X(150), H0 + X(46)), (X(175), X(340)), col=MK[1], w=int(X(2.2)), head=int(X(9)))
box(im, 1, (X(305), X(118), X(436), X(222)), pad=4, dash=True)
memo_w(im, "도메인 전체에 걸친\n패밀리 특이 특징", (X(446), X(118)), size=int(X(19)), col=MK[1])
memo(im, "가로는 한 번에 몇 잔기나 연속으로 켜지는가, 세로는 특정 패밀리에만 켜지는가",
     (X(16), H0 + X(16)), size=int(X(21)), col=INK)
memo(im, "왼쪽 아래 구석, 1 잔기만 그리고 보편적으로 켜지는 특징이 해석에 가장 쓸모 있다",
     (X(16), H0 + X(52)), size=int(X(21)), col=MK[1])
save(im, P + "fig4a_annot.jpg", maxw=1400)

# ---------------------------------------------------------------- 4C
C = src.crop((0, 492, 700, 792))
C = C.resize((C.width * 2, C.height * 2), Image.LANCZOS)
im = Image.new("RGB", (C.width, C.height + int(95 * s)), "white")
im.paste(C, (0, 0))
H0 = C.height
underline(im, (X(60), X(0), X(660), X(272)), col=MK[2], w=int(X(2.5)))
memo(im, "접힘도, 반응도, 친핵체 잔기도 다른 네 단백질. 켜지는 특징은 F6716 하나로 같다",
     (X(16), H0 + X(14)), size=int(X(21)), col=MK[2])
memo(im, "서열로도 구조로도 묶이지 않는 넷을 촉매 기하 하나로 묶어낸 셈이다",
     (X(16), H0 + X(50)), size=int(X(21)), col=INK)
save(im, P + "fig4c_annot.jpg", maxw=1400)

# ---------------------------------------------------------------- 4D
D = Image.open(RAW_D).convert("RGB").crop((0, 0, 1175, 784))
s = 1.0
X = lambda v: v * s
im = Image.new("RGB", (D.width, D.height + 110), "white")
im.paste(D, (0, 0))
H0 = D.height
box(im, 3, (560, 440, 760, 620), pad=4, dash=True)
memo_w(im, "같은 방향을 2^13 에서는\n큰 점 하나가 덮고,\n2^16 에서는 작은 점\n여럿이 덮는다", (890, 300), size=25, col=MK[3])
memo(im, "F6716 주변을 디코더 공간에서 본 것. 점 크기가 사전 크기다",
     (16, H0 + 14), size=26, col=INK)
memo(im, "사전을 키우면 특징 하나가 열 개로 쪼개진다. 개념의 경계는 모델이 정하는가, 사전 크기가 정하는가",
     (16, H0 + 52), size=26, col=RED)
save(im, P + "fig4d_annot.jpg", maxw=1200)

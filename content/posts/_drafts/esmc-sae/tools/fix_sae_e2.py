import sys
sys.path.insert(0, "/tmp/gen")
from ink import *

S = "/tmp/pdfcaps/"
P = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-sae/imgs/"

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
W = camk1.width + gap + right.width          # ~3258
im = Image.new("RGB", (W, h + 320), "white")
im.paste(camk1, (0, 0))
im.paste(right, (camk1.width + gap, 0))

marker(im, 5, (camk1.width + gap + 40, 150), r=44)

M = 76
memo(im, "촉매부는 일곱 패밀리가 공유하고, 갈리는 곳은 조절부다. CK1a 만 촉매부에서도 다른 특징을 켠다",
     (24, h + 40), size=M, col=MK[5])
memo(im, "왼쪽 CAMK1 에서 잔기당 특징 밀도는 알파C 나선 22.4, P-loop 21.3, HRD 20.0, DFG 19.7 순이다",
     (24, h + 165), size=M, col=INK)
save(im, P + "fig4e2_annot.jpg", maxw=2240, q=90)
print("canvas", W, "-> memo on screen",
      round(M * (2240 / W) * (1120 / 2240), 1), "px")

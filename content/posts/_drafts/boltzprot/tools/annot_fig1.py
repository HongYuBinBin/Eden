"""Annotate panel (a) of the report's Figure 1.

Panel (a) is 1500 px wide out of the 2780 px two-panel crop; shown fullwidth at 1244 px
that is a scale of about 0.83, so r=32 reads as ~27 px and size 32 as ~27 px.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import ink

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

src = Image.open(os.path.join(HERE, "..", "raw", "fig1.png")).convert("RGB")
panel = src.crop((0, 0, 1500, 790))
pad = Image.new("RGB", (panel.width, panel.height + 150), "white")
pad.paste(panel, (0, 0))
tmp = os.path.join(HERE, "..", "raw", "_fig1a.png")
pad.save(tmp)

im = ink.load(tmp)
ink.memo_w(im, "확정 결합체 12개 중 7개가 PMVK 하나에서 나온다",
           (660, 255), size=32, col=ink.MK[1], anchor="ma")
ink.arrow(im, (905, 268), (1135, 205), col=ink.MK[1], w=5, curve=-0.18)

ink.memo_w(im, "표적 10개 중 신호가 난 5개만 그렸다. 나머지 5개는 양쪽 다 0이다",
           (750, 815), size=32, col=ink.MK[4], anchor="ma")
ink.memo_w(im, "괄호 안 숫자는 어세이 결합가다. (2)는 2가 포맷이라 avidity가 끼어들 수 있다",
           (750, 875), size=30, col=ink.MK[4], anchor="ma")

ink.save(im, os.path.join(OUT, "fig1.png"), maxw=1500)
os.remove(tmp)
print("fig1.png written")

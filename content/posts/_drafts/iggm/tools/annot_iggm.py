"""Annotate the three IgGM architecture figures with the shared markers.

Display widths on the blog (measured on the deployed page, 1571px viewport):
  fullwidth figure = 1244 px.
Native sizes: fig3 1420 (x0.876), fig5 1195 (x1.04), fig6 1190 (x1.05).
Marker radii and font sizes below are chosen so each renders near 26 px on screen.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ink

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw")
OUT = sys.argv[1] if len(sys.argv) > 1 else "."


def fig3():
    im = ink.load(os.path.join(RAW, "fig3_framework.png"))
    # 1420 native shown at 1244 (x0.876): r=30 reads as 26 px, font 34 as 30 px.
    # Markers sit in the padding above each box so they never cover a label.
    ink.box(im, 1, (292, 84, 408, 238), w=5)
    ink.marker(im, 1, (350, 42), r=30, w=5)

    ink.box(im, 2, (710, 109, 826, 657), w=5)
    ink.marker(im, 2, (768, 42), r=30, w=5)

    ink.box(im, 3, (1020, 109, 1136, 657), w=5)
    ink.marker(im, 3, (1078, 42), r=30, w=5)

    ink.box(im, 4, (1170, 156, 1412, 668), w=5, dash=True)
    ink.marker(im, 4, (1293, 42), r=30, w=5)

    ink.memo_w(im, "ESM2-650M, 얼림", (350, 690), size=34, col=ink.MK[1], anchor="ma")
    ink.memo_w(im, "1280 + 660 -> 192 + 128", (350, 734), size=30, col=ink.MK[1], anchor="ma")
    ink.memo_w(im, "EvoformerBlockSS x 16", (768, 690), size=34, col=ink.MK[2], anchor="ma")
    ink.memo_w(im, "AF2SMod x 8", (1078, 690), size=34, col=ink.MK[3], anchor="ma")
    ink.memo_w(im, "설계된 CDR 서열 + 복합체 구조", (1404, 734), size=34, col=ink.MK[4], anchor="ra")
    ink.save(im, os.path.join(OUT, "fig3.png"), maxw=1420)


def fig5():
    im = ink.load(os.path.join(RAW, "fig5_sgformer.png"))
    # x1.04 on screen -> r=26 reads as 27 px, font 30 reads as 31 px
    ink.marker(im, 2, (60, 40), r=26, w=4)
    c = ink.MK[2]
    ink.memo_w(im, "L106", (219, 300), size=30, col=c, anchor="ma")
    ink.memo_w(im, "L107", (370, 300), size=30, col=c, anchor="ma")
    ink.memo_w(im, "L109", (466, 196), size=30, col=c, anchor="ma")
    ink.memo_w(im, "L111-112", (571, 8), size=30, col=c, anchor="ma")
    ink.memo_w(im, "L113-114", (728, 8), size=30, col=c, anchor="ma")
    ink.memo_w(im, "L115", (882, 8), size=30, col=c, anchor="ma")
    ink.memo_w(im, "evoformer_ss.py", (60, 500), size=32, col=c)
    ink.save(im, os.path.join(OUT, "fig5.png"), maxw=1195)


def fig6():
    im = ink.load(os.path.join(RAW, "fig6_predict.png"))
    ink.marker(im, 3, (40, 30), r=26, w=4)
    c = ink.MK[3]
    ink.memo_w(im, "L355-362", (342, 186), size=30, col=c, anchor="ma")
    ink.memo_w(im, "L366  Linear(192, 20)", (546, 14), size=30, col=c, anchor="ma")
    ink.memo_w(im, "structure_module.py", (1160, 20), size=32, col=c, anchor="ra")
    ink.save(im, os.path.join(OUT, "fig6.png"), maxw=1190)


if __name__ == "__main__":
    fig3(); fig5(); fig6()

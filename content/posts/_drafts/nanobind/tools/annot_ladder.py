import sys
sys.path.insert(0, "/tmp/nb")
import ink

im = ink.load("/tmp/nb/ladder_raw.png")
print("canvas", im.size)

S = 50   # ~26 px at the blog's 1,322 px display width, file saved at 2,400 px

ink.memo(im, "48개 중 45개가 2배 이내.\n중앙값 1.28배다",
         (330, 300), size=S, col=ink.MK[4], spacing=12)
ink.arrow(im, (560, 440), (690, 690), col=ink.MK[4], w=5, head=20, curve=22)

ink.memo(im, "여기 한 칸만 24.5배",
         (1400, 140), size=S, col=ink.RED, spacing=12)
ink.arrow(im, (1800, 182), (1985, 205), col=ink.RED, w=5, head=18, curve=14)

ink.save(im, "/tmp/nb/ladder.png", maxw=2400)

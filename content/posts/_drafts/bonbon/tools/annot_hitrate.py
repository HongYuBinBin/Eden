import sys
sys.path.insert(0, "/tmp/bon")
import ink

im = ink.load("/tmp/bon/hitrate_raw.png")
print("canvas", im.size)

# memo sized for the blog's full-width column: ~26 px on screen, file at ~2x
S = 52

# dashed box around the two out-of-distribution rows
ink.box(im, ink.RED, (432, 726, 1152, 878), w=5, dash=True)

ink.memo(im, "학습에 없던 표적 두 개가\n맨 아래 두 줄이다.\n100%와 8%가 평균 61.5%로 묶인다",
         (1350, 700), size=S, col=ink.RED, spacing=12)
ink.arrow(im, (1330, 790), (1180, 805), col=ink.RED, w=5, head=20)

ink.save(im, "/tmp/bon/hitrate.png", maxw=2520)

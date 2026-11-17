import sys
sys.path.insert(0, "/tmp/nb")
import ink

# ---- Fig 2B upper: ESM-2 -> residue embeddings -> two pathways
im = ink.load("/tmp/nb/f2b_top.png")
print("top", im.size)
ink.marker(im, 1, (140, 114), r=30, w=5)
ink.marker(im, 2, (88, 648), r=30, w=5)
ink.marker(im, 3, (710, 648), r=30, w=5)
ink.save(im, "/tmp/nb/f2b_top_a.png", maxw=1289)

# ---- Fig 2B middle: the two modules' internals
im = ink.load("/tmp/nb/f2b_mid.png")
print("mid", im.size)
ink.marker(im, 2, (545, 625), r=30, w=5)
ink.marker(im, 3, (1195, 305), r=30, w=5)
ink.save(im, "/tmp/nb/f2b_mid_a.png", maxw=1251)

# ---- Fig 2B lower: mean pooling + concat
im = ink.load("/tmp/nb/f2b_bot.png")
print("bot", im.size)
ink.marker(im, 4, (90, 250), r=30, w=5)
ink.save(im, "/tmp/nb/f2b_bot_a.png", maxw=1568)

"""Hand-annotation helpers: circled markers, boxes, arrows, handwritten memos."""
from PIL import Image, ImageDraw, ImageFont
import math

FONT = "/home/claude/fonts/NanumPenScript-Regular.ttf"
MK = {1: "#cf3f37", 2: "#8b5a8f", 3: "#b9760c", 4: "#2d6bb3", 5: "#2f8f6b"}
INK = "#1b3b6f"
RED = "#cf3f37"


def load(path, scale=1.0):
    im = Image.open(path).convert("RGB")
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    return im


def font(size):
    return ImageFont.truetype(FONT, size)


def _d(im):
    return ImageDraw.Draw(im, "RGBA")


def marker(im, n, xy, r=26, w=4):
    """Circled number in the marker colour."""
    d = _d(im)
    x, y = xy
    col = MK[n]
    d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=w, fill=(255, 255, 255, 215))
    f = font(int(r * 1.9))
    t = str(n)
    bb = d.textbbox((0, 0), t, font=f)
    d.text((x - (bb[2] - bb[0]) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1] - r * 0.08),
           t, font=f, fill=col)
    return im


def box(im, n, rect, w=4, pad=0, dash=False, fill=False):
    d = _d(im)
    x0, y0, x1, y1 = rect
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    col = MK[n] if isinstance(n, int) else n
    if fill:
        rgb = tuple(int(col.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=rgb + (34,))
    if dash:
        _dashed_rect(d, (x0, y0, x1, y1), col, w)
    else:
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=col, width=w)
    return im


def _dashed_rect(d, rect, col, w, dash=14, gap=9):
    x0, y0, x1, y1 = rect
    for (ax, ay, bx, by) in [(x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)]:
        L = math.hypot(bx - ax, by - ay)
        if L == 0:
            continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        t = 0.0
        while t < L:
            e = min(t + dash, L)
            d.line([ax + ux * t, ay + uy * t, ax + ux * e, ay + uy * e], fill=col, width=w)
            t = e + gap


def arrow(im, a, b, col=INK, w=4, head=16, curve=0.0):
    """Straight or gently curved arrow from a to b."""
    d = _d(im)
    ax, ay = a; bx, by = b
    if curve:
        mx, my = (ax + bx) / 2, (ay + by) / 2
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / L * curve, my + dx / L * curve
        pts = []
        for i in range(31):
            t = i / 30
            px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t ** 2 * bx
            py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t ** 2 * by
            pts.append((px, py))
        d.line(pts, fill=col, width=w, joint="curve")
        px, py = pts[-2]
    else:
        d.line([a, b], fill=col, width=w)
        px, py = ax, ay
    ang = math.atan2(by - py, bx - px)
    for s in (+1, -1):
        d.line([b, (bx - head * math.cos(ang + s * 0.42), by - head * math.sin(ang + s * 0.42))],
               fill=col, width=w)
    return im


def memo(im, text, xy, size=30, col=INK, anchor="la", spacing=4):
    d = _d(im)
    f = font(size)
    d.multiline_text(xy, text, font=f, fill=col, anchor=anchor, spacing=spacing)
    return im


def memo_w(im, text, xy, size=30, col=INK, anchor="la", pad=8):
    """Memo on a translucent white plate, for busy backgrounds."""
    d = _d(im)
    f = font(size)
    bb = d.multiline_textbbox(xy, text, font=f, anchor=anchor, spacing=4)
    d.rounded_rectangle([bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad],
                        radius=8, fill=(255, 255, 255, 232))
    d.multiline_text(xy, text, font=f, fill=col, anchor=anchor, spacing=4)
    return im


def underline(im, rect, col=RED, w=5, wobble=3):
    """Hand-drawn underline under a region."""
    d = _d(im)
    x0, y0, x1, y1 = rect
    pts = []
    n = 18
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t, y1 + math.sin(t * 6.1) * wobble))
    d.line(pts, fill=col, width=w, joint="curve")
    return im


def save(im, path, maxw=1500, q=86):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    if path.endswith(".jpg"):
        im.save(path, quality=q, optimize=True)
    else:
        im.save(path, optimize=True)
    print(path, im.size)

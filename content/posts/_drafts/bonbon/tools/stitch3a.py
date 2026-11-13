from PIL import Image
import numpy as np

a = Image.open('/tmp/bon/f3a_t1.png').convert('RGB')
b = Image.open('/tmp/bon/f3a_t2.png').convert('RGB')

# rescale b so its pixels-per-frame-unit matches a
sa = a.width / (1490 - 440)
sb = b.width / (1300 - 490)
k = sa / sb
b = b.resize((round(b.width * k), round(b.height * k)), Image.LANCZOS)
print('a', a.size, 'b', b.size, 'k', round(k, 4))

A = np.asarray(a, dtype=np.float32)
B = np.asarray(b, dtype=np.float32)
h = min(A.shape[0], B.shape[0])
A, B = A[:h], B[:h]

best = None
# b starts at frame x=490 -> in a's coords that is (490-440)*sa = 74 px,
# plus the scroll shift; search a wide range
for off in range(200, A.shape[1] - 200):
    w = min(A.shape[1] - off, B.shape[1])
    if w < 300:
        break
    d = np.abs(A[:, off:off + w] - B[:, :w]).mean()
    if best is None or d < best[1]:
        best = (off, d)
print('best offset', best)

off = best[0]
W = off + B.shape[1]
out = Image.new('RGB', (W, h), 'white')
out.paste(Image.fromarray(A.astype('uint8')), (0, 0))
out.paste(Image.fromarray(B.astype('uint8')), (off, 0))
out.save('/tmp/bon/fig3a.png')
print('saved', out.size)

"""Make a heart-shaped QR code for a URL.

Usage:  python3 make_heart_qr.py https://example.com/page out.png
Needs:  pip install segno pillow opencv-python numpy
"""
import sys
import numpy as np
import segno
import cv2
from PIL import Image, ImageDraw

URL = sys.argv[1] if len(sys.argv) > 1 else "https://claude.ai/artifact/AJawc1VmabkZZczmvvKsFX"
OUT = sys.argv[2] if len(sys.argv) > 2 else "Rojy_heart_QR.png"
HEART_SCALE = 1.25   # bigger = fuller heart, fewer modules cut away

q = segno.make(URL, error="h", boost_error=False)
ver = q.version
M = np.array([[1 if c else 0 for c in row] for row in q.matrix], dtype=np.uint8)
N = M.shape[0]

# Modules that must always stay: finders, format info, timing, alignment, version info.
F = np.zeros((N, N), bool)
F[:9, :9] = True; F[:9, N - 8:] = True; F[N - 8:, :9] = True
F[6, :] = True; F[:, 6] = True
ALIGN = {2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34]}
for r in ALIGN.get(ver, []):
    for c in ALIGN.get(ver, []):
        if (r < 9 and c < 9) or (r < 9 and c > N - 9) or (r > N - 9 and c < 9):
            continue
        F[r - 2:r + 3, c - 2:c + 3] = True
if ver >= 7:
    F[:6, N - 11:N - 8] = True; F[N - 11:N - 8, :6] = True
F[N - 8, 8] = True

# Heart curve: (x^2 + y^2 - 1)^3 - x^2 y^3 <= 0
ys, xs = np.mgrid[0:N, 0:N]
x = ((xs + .5) / N * 2 - 1) * 1.25 / HEART_SCALE
y = -(((ys + .5) / N * 2 - 1) * 1.25 / HEART_SCALE) + 0.1
inside = ((x ** 2 + y ** 2 - 1) ** 3 - x ** 2 * y ** 3) <= 0
G = np.where(inside | F, M, 0).astype(np.uint8)

px = 1400
mod = px // (N + 8)
img = Image.new("RGB", (mod * (N + 8),) * 2, "white")
d = ImageDraw.Draw(img)
for r in range(N):
    for c in range(N):
        if G[r, c]:
            x0, y0 = (c + 4) * mod, (r + 4) * mod
            col = (194, 40, 95) if F[r, c] else (224, 72, 122)
            d.rounded_rectangle([x0, y0, x0 + mod - 1, y0 + mod - 1], radius=int(mod * .28), fill=col)
img.save(OUT)

# Check that the saved image really decodes to the URL.
gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
decoded = cv2.QRCodeDetector().detectAndDecode(gray)[0]
print("saved", OUT, "| decodes to URL:", decoded == URL)

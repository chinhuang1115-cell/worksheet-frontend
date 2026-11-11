"""Gemini 生的白底圖 → 透明背景 PNG。

用法：python tools/cutout.py 輸入.png 輸出.png [--min-hole 3000]
- 從四角往內 flood fill 把相連的白底變透明；
- 被圖形包住、面積 >= min-hole 的白色區塊（例如手指圍起來的洞）也變透明；
  小塊白色（指甲反光、亮點）保留。
- 邊緣做 1.2px 模糊，避免鋸齒。
"""
import sys, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def cutout(src, dst, min_hole=3000, thr=232):
    rgb = Image.open(src).convert("RGB")
    w, h = rgb.size
    a = (np.array(rgb).min(axis=2) > thr).astype(np.uint8) * 255
    m = Image.fromarray(a)
    for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if m.getpixel(p) == 255:
            ImageDraw.floodfill(m, p, 128)
    # 包在裡面的大白洞：只在 16px 格點上找種子，小亮點通常不會被選到；選到也因面積小而保留
    for y in range(0, h, 16):
        for x in range(0, w, 16):
            if m.getpixel((x, y)) == 255:
                ImageDraw.floodfill(m, (x, y), 60)
                big = m.histogram()[60] >= min_hole
                to = 128 if big else 50
                m = m.point(lambda v, to=to: to if v == 60 else v)
    bg = np.array(m) == 128
    alpha = Image.fromarray(((~bg) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out = rgb.convert("RGBA"); out.putalpha(alpha); out.save(dst)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--min-hole", type=int, default=3000)
    a = ap.parse_args(); cutout(a.src, a.dst, a.min_hole)

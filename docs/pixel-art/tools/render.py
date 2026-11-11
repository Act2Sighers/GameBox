"""Pixel-art helpers: text grid -> PNG, auto outline, contact sheet.

A sprite is a list of equal-length strings (square). '.' = transparent.
Other characters are looked up in a palette dict {char: "#rrggbb"}.
Grids are drawn facing RIGHT; mirror horizontally for left.
"""
from PIL import Image, ImageDraw, ImageFont

OUTLINE = "#1d1826"


def outline(grid, ch="O"):
    """Add a 1px outline (4-neighbour) on transparent cells touching a filled cell."""
    h, w = len(grid), len(grid[0])
    out = [list(r) for r in grid]
    for y in range(h):
        for x in range(w):
            if grid[y][x] != ".":
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != ".":
                    out[y][x] = ch
                    break
    return ["".join(r) for r in out]


def to_image(grid, palette):
    h = len(grid); w = len(grid[0])
    assert all(len(r) == w for r in grid), [len(r) for r in grid]
    assert w == h, (w, h)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch not in palette:
                raise KeyError(f"unknown char {ch!r} at {x},{y}")
            col = palette[ch]
            if col:
                c = col.lstrip("#")
                img.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return img


def sprite_image(fill_grid, palette):
    """Fill-only grid + palette -> RGBA image with the standard outline."""
    return to_image(outline(fill_grid), {".": None, "O": OUTLINE, **palette})


def sheet(rows, cell=288, pad=24, labels=None):
    """rows: list of lists of PIL images. Returns a contact sheet (nearest-neighbour scaled)."""
    top = 28 if labels else 0
    ncol = max(len(r) for r in rows)
    out = Image.new("RGBA", (pad + ncol * (cell + pad), top + pad + len(rows) * (cell + pad)), (226, 229, 236, 255))
    d = ImageDraw.Draw(out)
    if labels:
        font = ImageFont.load_default(size=18)
        for j, t in enumerate(labels):
            d.text((pad + j * (cell + pad), 10), t, fill=(40, 40, 60), font=font)
    for i, r in enumerate(rows):
        for j, im in enumerate(r):
            x0, y0 = pad + j * (cell + pad), top + pad + i * (cell + pad)
            d.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], fill=(246, 247, 250, 255))
            k = cell // im.width
            big = im.resize((im.width * k, im.height * k), Image.NEAREST)
            out.alpha_composite(big, (x0 + (cell - big.width) // 2, y0 + (cell - big.height) // 2))
    return out

"""Render text-grid pixel art to PNG.

Usage: python3 render.py <sprite.py> ...   (see sprites/*.py)
A sprite module defines PALETTE (dict char->hex or None) and GRID (list[str]).
"""
import sys, importlib.util
from PIL import Image

def load(path):
    spec = importlib.util.spec_from_file_location("sprite", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def to_image(grid, palette):
    h = len(grid); w = len(grid[0])
    assert all(len(r) == w for r in grid), [len(r) for r in grid]
    assert w == h, (w, h)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            col = palette.get(ch)
            if ch not in palette:
                raise KeyError(f"unknown char {ch!r} at {x},{y}")
            if col:
                c = col.lstrip("#")
                img.putpixel((x, y), tuple(int(c[i:i+2], 16) for i in (0, 2, 4)) + (255,))
    return img

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
sys.path.insert(0, HERE)
from render import to_image
from sprites import SPRITES, PALETTES, OUTLINE
from PIL import Image, ImageDraw, ImageFont

def outline(grid):
    h, w = len(grid), len(grid[0])
    out = [list(r) for r in grid]
    for y in range(h):
        for x in range(w):
            if grid[y][x] != ".": continue
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != ".":
                    out[y][x] = "O"; break
    return ["".join(r) for r in out]

CELL, PAD, LABEL = 288, 24, 28
os.makedirs(os.path.join(HERE, "png"), exist_ok=True)
sheet = Image.new("RGBA", (PAD + 3*(CELL+PAD), LABEL + PAD + 3*(CELL+PAD)), (226, 229, 236, 255))
d = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=18)
for j, f in enumerate("ABC"):
    n = len(SPRITES["1"+f])
    d.text((PAD + j*(CELL+PAD), 10), f"Format {f}  ({n}x{n})", fill=(40,40,60), font=font)
for i, c in enumerate("123"):
    for j, f in enumerate("ABC"):
        key = c + f
        pal = {".": None, "O": OUTLINE, **PALETTES[c]}
        im = to_image(outline(SPRITES[key]), pal)
        im.save(os.path.join(HERE, "png", f"{key}.png"))
        n = im.width
        big = im.resize((n*(CELL//n),)*2, Image.NEAREST)
        x0, y0 = PAD + j*(CELL+PAD), LABEL + PAD + i*(CELL+PAD)
        d.rectangle([x0, y0, x0+CELL-1, y0+CELL-1], fill=(246, 247, 250, 255))
        sheet.alpha_composite(big, (x0 + (CELL-big.width)//2, y0 + (CELL-big.height)//2))
sheet.save(os.path.join(HERE, "sheet.png"))
print("ok")

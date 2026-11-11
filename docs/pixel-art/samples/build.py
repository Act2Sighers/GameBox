"""Rebuild png/ (1x) and sheet.png from sprites.py.  Run: python3 build.py"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, HERE)
from render import sprite_image, sheet
from sprites import SPRITES, PALETTES

os.makedirs(os.path.join(HERE, "png"), exist_ok=True)
rows = []
for c in "123":
    row = []
    for f in "ABC":
        im = sprite_image(SPRITES[c + f], PALETTES[c])
        im.save(os.path.join(HERE, "png", f"{c}{f}.png"))
        row.append(im)
    rows.append(row)
sheet(rows, labels=["Format A (16x16)", "Format B (24x24)", "Format C (32x32)"]).save(os.path.join(HERE, "sheet.png"))
print("ok")

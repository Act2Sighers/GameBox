"""Inject sprite data into ../index.html and write a preview sheet.  Run: python3 -B build.py"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "docs", "pixel-art", "tools"))
sys.path.insert(0, HERE)
from render import sprite_image, sheet
from hero import FRAMES, PALETTE

data = {"palette": PALETTE, "frames": FRAMES}
block = "const HERO = " + json.dumps(data, separators=(",", ":")).replace('],"', '],\n"') + ";"
html_path = os.path.join(HERE, "..", "index.html")
html = open(html_path, encoding="utf-8").read()
new = re.sub(r"(// BEGIN GENERATED: hero\n).*?(\n// END GENERATED: hero)", lambda m: m.group(1) + block + m.group(2), html, flags=re.S)
assert new != html or block in html, "markers not found"
open(html_path, "w", encoding="utf-8").write(new)

ims = [sprite_image(FRAMES[k], PALETTE) for k in ("idle", "walk1", "walk2")]
sheet([ims, [im.transpose(0) for im in ims]], labels=["idle", "walk1", "walk2"]).save(os.path.join(HERE, "hero_sheet.png"))
print("ok")

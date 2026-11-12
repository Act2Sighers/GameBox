"""Hero sprite (format B, 24x24, facing right). Fill-only; outline added automatically.
Based on docs/pixel-art/samples format B skeleton; top of head replaced by a pointed hat.
"""
PALETTE = {
    "H": "#8a4a2b", "h": "#62311c", "j": "#b06a40",   # chestnut hair
    "S": "#f7dcc6",
    "E": "#3a2418", "e": "#7a4a32",
    "C": "#2b3768", "c": "#1f2850",                    # navy hat & cape
    "R": "#e3b341",                                    # gold band / clasp
    "D": "#8a3d5c", "d": "#6a2d47",                    # plum dress
    "K": "#5a3a2e",                                    # boots
}

_TOP = """
........................
....cCC.................
.....cCCCC..............
.......cCCCCC...........
.......cCCCCCCCC........
.......RRRRRRRRRR.......
..cCCCCCCCCCCCCCCCCCCC..
...hhhhhhhhhhhhhhhhhhh..
...HHHHHHHHHHHHHHHHHHH..
...HHHHHHHHHSHHHHHSHHH..
...HHHHHHHSSEESSSSEESH..
...HHHHHHHSSEESSSSEESH..
...HHHHHHHSSeeSSSSeeSH..
...HHHHHHHHSSSSSSSSSH...
...hHHHHHHHHSSSSSSS.....
....hhhhhCCCRCCCC.......
....hhhhCCCCDDDCCCC.....
.....hhcCCCCDDDCCCCC....
......ccCCCSDDDSCCCCC...
.......DDDDDDDDDDDD.....
......DDdDDdDDdDDDD.....
""".split()

_FEET = {
    "idle":  [".........SS...SS........", ".........KKK..KKK......."],
    "walk1": [".........KKK..SS........", "..............KKK......."],
    "walk2": [".........SS...KKK.......", ".........KKK............"],
}
BLANK = "." * 24
FRAMES = {k: _TOP + v + [BLANK] for k, v in _FEET.items()}


def _carry(frame):
    """Arms raised to hold furniture overhead: hands at the cape front disappear, hands appear above the brim."""
    g = [list(r) for r in frame]
    for x in (11, 15):
        if g[18][x] == "S":
            g[18][x] = "C"
    for y in (4, 5):
        g[y][3] = "S"
        g[y][20] = "S"
    return ["".join(r) for r in g]


for _k in list(_FEET):
    FRAMES["carry_" + _k] = _carry(FRAMES[_k])

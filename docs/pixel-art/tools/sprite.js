// Pixel-art sprite helper for games (copy inline into a game's HTML).
// grid: array of equal-length strings, '.' = transparent, drawn facing RIGHT.
// palette: { char: "#rrggbb" }. A 1px outline is added around the silhouette.
// Returns { right, left } canvases at 1x; draw them scaled with imageSmoothingEnabled = false.
const PIXEL_OUTLINE = "#1d1826";
function makeSprite(grid, palette, outlineColor = PIXEL_OUTLINE) {
  const h = grid.length, w = grid[0].length;
  const filled = (x, y) => x >= 0 && y >= 0 && x < w && y < h && grid[y][x] !== ".";
  const right = document.createElement("canvas");
  right.width = w; right.height = h;
  const ctx = right.getContext("2d");
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const ch = grid[y][x];
      let color = null;
      if (ch !== ".") {
        color = palette[ch];
        if (!color) throw new Error(`unknown char ${ch} at ${x},${y}`);
      } else if (filled(x + 1, y) || filled(x - 1, y) || filled(x, y + 1) || filled(x, y - 1)) {
        color = outlineColor;
      }
      if (color) { ctx.fillStyle = color; ctx.fillRect(x, y, 1, 1); }
    }
  }
  const left = document.createElement("canvas");
  left.width = w; left.height = h;
  const lctx = left.getContext("2d");
  lctx.translate(w, 0); lctx.scale(-1, 1); lctx.drawImage(right, 0, 0);
  return { right, left };
}

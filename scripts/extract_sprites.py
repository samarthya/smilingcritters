"""
extract_sprites.py
------------------
Splits the 2×4 Smiling Critters sprite sheet into 8 individual PNGs.
Also generates icon-sized copies (48×48) for use in buttons and UI chrome.

Usage:
    python scripts/extract_sprites.py <path-to-spritesheet>

Example:
    python scripts/extract_sprites.py images/sprinte2.png

Output:
    assets/sprites/{id}.png   — 200×200 px, transparent square
    assets/icons/{id}.png     —  48×48 px, transparent square (for UI icons)
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not found. Install it with:  pip install Pillow")
    sys.exit(1)


# ── Character order in the sheet (row-major, L→R, top→bottom) ─────────────────
# Row 0: Bubba, DogDay, CatNap, KickinChicken
# Row 1: Hoppy, PickyPiggy, Bobby, CraftyCorn
SPRITE_ORDER = [
    "bubba",    # row 0, col 0  — blue elephant
    "dogday",   # row 0, col 1  — orange dog / fire
    "catnap",   # row 0, col 2  — purple cat
    "kickin",   # row 0, col 3  — yellow chicken
    "hoppy",    # row 1, col 0  — green rabbit
    "piggy",    # row 1, col 1  — pink pig
    "bobby",    # row 1, col 2  — red bear
    "crafty",   # row 1, col 3  — white/cyan unicorn
]

COLS = 4
ROWS = 2
ROOT        = Path(__file__).parent.parent
OUT_SPRITES = ROOT / "assets" / "sprites"
OUT_ICONS   = ROOT / "assets" / "icons"

SPRITE_SIZE = 200   # px — large card avatar
ICON_SIZE   = 48    # px — small button / strip icon


def alpha_crop(img: Image.Image) -> Image.Image:
    """Crop away transparent border from an RGBA image."""
    if img.mode != "RGBA":
        return img
    bbox = img.getbbox()
    if bbox is None:
        return img
    pad = 6
    w, h = img.size
    x0 = max(0, bbox[0] - pad)
    y0 = max(0, bbox[1] - pad)
    x1 = min(w, bbox[2] + pad)
    y1 = min(h, bbox[3] + pad)
    return img.crop((x0, y0, x1, y1))


def fit_to_square(cell: Image.Image, size: int) -> Image.Image:
    """Resize to fit within size×size, centred on transparent canvas."""
    cell.thumbnail((size, size), Image.LANCZOS)
    square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ox = (size - cell.width) // 2
    oy = (size - cell.height) // 2
    square.paste(cell, (ox, oy), mask=cell)
    return square


def extract(sheet_path: str) -> None:
    sheet = Image.open(sheet_path).convert("RGBA")
    sw, sh = sheet.size
    cell_w = sw // COLS
    cell_h = sh // ROWS

    print(f"Sheet size : {sw}×{sh}  |  Cell size : {cell_w}×{cell_h}")
    OUT_SPRITES.mkdir(parents=True, exist_ok=True)
    OUT_ICONS.mkdir(parents=True, exist_ok=True)

    for idx, sprite_id in enumerate(SPRITE_ORDER):
        row = idx // COLS
        col = idx % COLS
        left   = col * cell_w
        upper  = row * cell_h
        right  = left + cell_w
        lower  = upper + cell_h

        cell = sheet.crop((left, upper, right, lower))
        cell = alpha_crop(cell)

        # ── 200px sprite ──────────────────────────────────────────────────────
        sprite = fit_to_square(cell.copy(), SPRITE_SIZE)
        sprite_path = OUT_SPRITES / f"{sprite_id}.png"
        sprite.save(sprite_path, "PNG")

        # ── 48px icon ─────────────────────────────────────────────────────────
        icon = fit_to_square(cell.copy(), ICON_SIZE)
        icon_path = OUT_ICONS / f"{sprite_id}.png"
        icon.save(icon_path, "PNG")

        print(f"  [{idx+1}/8] {sprite_id:10s}  sprite→{sprite_path.name}  icon→{icon_path.name}")

    print(f"\nDone!")
    print(f"  Sprites : {OUT_SPRITES}")
    print(f"  Icons   : {OUT_ICONS}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <spritesheet_image>")
        sys.exit(1)
    extract(sys.argv[1])

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


W, H = 900, 1260
SCALE = 2
CARD_W, CARD_H = W * SCALE, H * SCALE

RARITY_COLORS = {
    "一般": (126, 132, 138),
    "稀有": (66, 145, 224),
    "罕见": (150, 82, 214),
    "史诗": (232, 133, 42),
    "传说": (238, 193, 71),
}

ELEMENT_COLORS = {
    "木": (67, 166, 92),
    "火": (219, 70, 55),
    "土": (166, 119, 64),
    "金": (187, 193, 198),
    "水": (54, 116, 188),
}

REGION_PALETTES = {
    "沃衡区": ((106, 79, 39), (220, 182, 89), (63, 130, 83)),
    "澄曜区": ((158, 54, 38), (244, 143, 57), (210, 197, 126)),
    "澜桥区": ((37, 87, 135), (87, 164, 194), (198, 183, 124)),
    "砚岭区": ((70, 75, 87), (143, 134, 112), (58, 101, 89)),
    "霜港区": ((65, 91, 116), (145, 188, 207), (185, 186, 174)),
    "青棠区": ((58, 126, 93), (114, 183, 122), (72, 132, 168)),
}


@dataclass
class Card:
    name: str
    fields: dict[str, str]
    source: str
    section: str
    candidate: bool = False

    @property
    def cid(self) -> str:
        return self.fields.get("ID", "")

    @property
    def region(self) -> str:
        return self.fields.get("地区", "")

    @property
    def element(self) -> str:
        return self.fields.get("元素", "")

    @property
    def cost(self) -> str:
        return self.fields.get("费用", "-")

    @property
    def ctype(self) -> str:
        return self.fields.get("类型", "")

    @property
    def stats(self) -> str:
        return self.fields.get("身材", "-")

    @property
    def rarity(self) -> str:
        return self.fields.get("稀有度", "一般")

    @property
    def role(self) -> str:
        return self.fields.get("牌组角色", "")

    @property
    def keywords(self) -> str:
        return self.fields.get("关键词", "无")

    @property
    def effect(self) -> str:
        return self.fields.get("基础效果", "")

    @property
    def flavor(self) -> str:
        return self.fields.get("风味文本", "")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size)


FONT_REG = "C:/Windows/Fonts/Noto Sans SC (TrueType).otf"
FONT_MED = "C:/Windows/Fonts/Noto Sans SC Medium (TrueType).otf"
FONT_BOLD = "C:/Windows/Fonts/Noto Sans SC Bold (TrueType).otf"
FONT_SERIF = "C:/Windows/Fonts/NotoSerifSC-VF.ttf"


def load_fonts(scale: int = SCALE) -> dict[str, ImageFont.FreeTypeFont]:
    return {
        "title": font(FONT_BOLD, 36 * scale),
        "subtitle": font(FONT_MED, 20 * scale),
        "body": font(FONT_REG, 28 * scale),
        "body_small": font(FONT_REG, 24 * scale),
        "flavor": font(FONT_SERIF, 23 * scale),
        "big": font(FONT_BOLD, 52 * scale),
        "stat": font(FONT_BOLD, 46 * scale),
        "tiny": font(FONT_REG, 18 * scale),
    }


FONTS = load_fonts()


def parse_cards(workspace: Path) -> list[Card]:
    card_root = next(p for p in workspace.iterdir() if p.name.startswith("03-"))
    atlas = max(
        [p for p in card_root.iterdir() if p.is_dir()],
        key=lambda p: sum(1 for c in p.iterdir() if c.is_dir()),
    )

    cards: list[Card] = []
    for district in sorted(atlas.iterdir(), key=lambda p: p.name):
        if not district.is_dir():
            continue
        for md in sorted(p for p in district.iterdir() if p.suffix == ".md" and "bak_" not in p.name):
            text = md.read_text(encoding="utf-8")
            matches = list(re.finditer(r"^(#{3,4})\s+(.+)$", text, re.M))
            section = ""
            parent_id = ""
            form_index = 0
            for i, match in enumerate(matches):
                level = match.group(1)
                title = match.group(2).strip()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                block = text[match.end() : end]
                fields = {
                    key.strip(): value.strip()
                    for key, value in re.findall(r"- \*\*(.+?)\*\*:\s*(.+)", block)
                }
                is_card = "ID" in fields or (
                    level == "####"
                    and {"地区", "元素", "费用", "类型", "身材", "稀有度", "基础效果"}.issubset(fields)
                )
                if not is_card:
                    if level == "###":
                        section = title
                        parent_id = ""
                        form_index = 0
                    continue

                if "ID" not in fields:
                    form_index += 1
                    fields["ID"] = f"{parent_id}-F{form_index}" if parent_id else f"FORM-{len(cards) + 1:03d}"
                if level == "###":
                    parent_id = fields.get("ID", "")
                    form_index = 0
                cards.append(
                    Card(
                        name=title,
                        fields=fields,
                        source=str(md.relative_to(workspace)),
                        section=section,
                        candidate=("候补" in section or "候补" in title),
                    )
                )
    return cards


def seed_for(card: Card) -> int:
    digest = hashlib.sha256(f"{card.cid}:{card.name}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill, anchor="mm") -> None:
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    text = re.sub(r"\s+", "", text.strip())
    if not text:
        return []
    lines: list[str] = []
    current = ""
    for ch in text:
        trial = current + ch
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def fit_text(draw: ImageDraw.ImageDraw, text: str, font_path: str, start_size: int, min_size: int, max_width: int, max_lines: int):
    for size in range(start_size, min_size - 1, -2):
        fnt = font(font_path, size)
        lines = wrap_text(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(font_path, min_size)
    lines = wrap_text(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        last = lines[max_lines - 1]
        while draw.textlength(last + "…", font=fnt) > max_width and last:
            last = last[:-1]
        lines = lines[: max_lines - 1] + [last + "…"]
    return fnt, lines


def draw_gradient(img: Image.Image, box: tuple[int, int, int, int], top, bottom) -> None:
    px = img.load()
    x1, y1, x2, y2 = box
    for y in range(y1, y2):
        t = (y - y1) / max(1, y2 - y1)
        col = mix(top, bottom, t)
        for x in range(x1, x2):
            px[x, y] = col + (255,)


def draw_clouds(draw: ImageDraw.ImageDraw, rng: random.Random, box, fill):
    x1, y1, x2, y2 = box
    for _ in range(6):
        cx = rng.randint(x1 + 40, x2 - 40)
        cy = rng.randint(y1 + 30, y1 + 150)
        r = rng.randint(18, 42)
        for i in range(3):
            draw.ellipse((cx + i * r - r, cy - r // 2, cx + i * r + r, cy + r // 2), fill=fill)


def draw_art(base: Image.Image, card: Card, box: tuple[int, int, int, int]) -> Image.Image:
    rng = random.Random(seed_for(card))
    x1, y1, x2, y2 = box
    region_cols = REGION_PALETTES.get(card.region, ((76, 82, 92), (150, 152, 140), (90, 110, 120)))
    elem_col = ELEMENT_COLORS.get(card.element, region_cols[1])

    art = Image.new("RGBA", (x2 - x1, y2 - y1), (0, 0, 0, 0))
    draw_gradient(art, (0, 0, x2 - x1, y2 - y1), mix(region_cols[1], (255, 255, 255), 0.22), mix(region_cols[0], (0, 0, 0), 0.08))
    d = ImageDraw.Draw(art, "RGBA")
    aw, ah = art.size

    draw_clouds(d, rng, (0, 0, aw, ah), (*mix(region_cols[1], (255, 255, 255), 0.55), 95))

    if card.region in ("沃衡区", "青棠区"):
        for i in range(8):
            y = ah - 70 - i * 18
            d.arc((-80, y - 120, aw + 80, y + 90), 0, 180, fill=(*mix(region_cols[2], (255, 255, 255), i / 12), 170), width=5)
        for _ in range(45):
            bx = rng.randint(20, aw - 20)
            by = rng.randint(ah // 2, ah - 25)
            h = rng.randint(25, 90)
            d.line((bx, by, bx + rng.randint(-12, 12), by - h), fill=(*region_cols[2], 160), width=3)
            if rng.random() < 0.55:
                d.ellipse((bx - 5, by - h - 6, bx + 8, by - h + 7), fill=(*mix(elem_col, (255, 230, 160), 0.28), 190))
    elif card.region == "澄曜区":
        d.ellipse((aw - 170, 35, aw - 35, 170), fill=(255, 210, 92, 160))
        for i in range(7):
            left = 40 + i * 92
            d.polygon([(left, ah - 80), (left + 28, ah // 2 + rng.randint(-20, 35)), (left + 72, ah - 80)], fill=(*mix(region_cols[0], (0, 0, 0), 0.12), 150))
        for _ in range(11):
            cx = rng.randint(30, aw - 30)
            cy = rng.randint(ah // 2, ah - 80)
            d.line((cx, cy, cx + rng.randint(-40, 40), cy - rng.randint(35, 85)), fill=(255, 225, 120, 120), width=4)
    elif card.region == "澜桥区":
        for i in range(7):
            y = ah - 45 - i * 28
            d.arc((20, y - 45, aw - 20, y + 45), 0, 180, fill=(*mix(region_cols[1], (255, 255, 255), 0.25), 150), width=6)
        for i in range(5):
            px = 45 + i * 145
            d.rounded_rectangle((px, ah - 165, px + 95, ah - 130), radius=18, fill=(235, 214, 150, 135))
            d.line((px + 15, ah - 130, px + 5, ah - 65), fill=(90, 80, 60, 120), width=5)
            d.line((px + 80, ah - 130, px + 88, ah - 65), fill=(90, 80, 60, 120), width=5)
    elif card.region == "砚岭区":
        for i in range(5):
            left = -40 + i * 160 + rng.randint(-20, 20)
            d.polygon([(left, ah - 60), (left + 95, 130 + rng.randint(-15, 40)), (left + 210, ah - 60)], fill=(*mix(region_cols[0], (255, 255, 255), i / 12), 165))
        for _ in range(10):
            x = rng.randint(45, aw - 45)
            d.line((x, 120, x + rng.randint(-60, 60), ah - 110), fill=(35, 36, 39, 70), width=3)
    elif card.region == "霜港区":
        for i in range(6):
            left = 35 + i * 110
            d.polygon([(left, ah - 60), (left + 42, ah - 210 - rng.randint(0, 70)), (left + 84, ah - 60)], fill=(205, 230, 240, 100))
        for _ in range(16):
            cx = rng.randint(20, aw - 20)
            cy = rng.randint(40, ah - 60)
            r = rng.randint(8, 24)
            d.line((cx - r, cy, cx + r, cy), fill=(240, 250, 255, 120), width=3)
            d.line((cx, cy - r, cx, cy + r), fill=(240, 250, 255, 120), width=3)

    # Central subject or spell sigil.
    cx, cy = aw // 2, ah // 2 + 32
    aura = Image.new("RGBA", art.size, (0, 0, 0, 0))
    ad = ImageDraw.Draw(aura, "RGBA")
    for r in range(150, 35, -16):
        ad.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(*elem_col, max(18, 120 - r // 2)), width=8)
    aura = aura.filter(ImageFilter.GaussianBlur(3))
    art.alpha_composite(aura)
    d = ImageDraw.Draw(art, "RGBA")

    if card.ctype == "妖怪":
        body = mix(elem_col, (255, 255, 255), 0.18)
        shadow = mix(elem_col, (0, 0, 0), 0.38)
        d.ellipse((cx - 105, cy - 100, cx + 105, cy + 122), fill=(*body, 235), outline=(*shadow, 230), width=7)
        d.ellipse((cx - 72, cy - 172, cx + 72, cy - 34), fill=(*mix(body, (255, 255, 255), 0.12), 245), outline=(*shadow, 230), width=7)
        if card.element in ("木", "土"):
            d.polygon([(cx - 55, cy - 145), (cx - 132, cy - 215), (cx - 86, cy - 91)], fill=(*body, 230), outline=(*shadow, 220))
            d.polygon([(cx + 55, cy - 145), (cx + 132, cy - 215), (cx + 86, cy - 91)], fill=(*body, 230), outline=(*shadow, 220))
        elif card.element in ("火", "金"):
            d.polygon([(cx - 56, cy - 130), (cx - 104, cy - 225), (cx - 20, cy - 165)], fill=(*mix(body, (255, 220, 120), 0.3), 230), outline=(*shadow, 220))
            d.polygon([(cx + 56, cy - 130), (cx + 104, cy - 225), (cx + 20, cy - 165)], fill=(*mix(body, (255, 220, 120), 0.3), 230), outline=(*shadow, 220))
        else:
            d.polygon([(cx - 68, cy - 118), (cx - 118, cy - 185), (cx - 34, cy - 154)], fill=(*body, 220), outline=(*shadow, 220))
            d.polygon([(cx + 68, cy - 118), (cx + 118, cy - 185), (cx + 34, cy - 154)], fill=(*body, 220), outline=(*shadow, 220))
        d.ellipse((cx - 48, cy - 112, cx - 18, cy - 82), fill=(32, 30, 28, 230))
        d.ellipse((cx + 18, cy - 112, cx + 48, cy - 82), fill=(32, 30, 28, 230))
        d.arc((cx - 42, cy - 92, cx + 42, cy - 40), 15, 165, fill=(38, 32, 28, 200), width=5)
        for _ in range(6):
            ang = rng.random() * math.tau
            rr = rng.randint(102, 155)
            px = cx + int(math.cos(ang) * rr)
            py = cy + int(math.sin(ang) * rr)
            d.ellipse((px - 10, py - 10, px + 10, py + 10), fill=(*mix(elem_col, (255, 255, 255), 0.35), 160))
    else:
        d.rounded_rectangle((cx - 130, cy - 150, cx + 130, cy + 150), radius=36, fill=(245, 233, 198, 205), outline=(*elem_col, 245), width=9)
        for i in range(6):
            yy = cy - 95 + i * 38
            d.line((cx - 85, yy, cx + 85, yy + rng.randint(-8, 8)), fill=(*mix(elem_col, (0, 0, 0), 0.25), 160), width=5)
        d.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), outline=(*elem_col, 220), width=8)
        d.line((cx - 102, cy, cx + 102, cy), fill=(*elem_col, 170), width=6)
        d.line((cx, cy - 102, cx, cy + 102), fill=(*elem_col, 170), width=6)

    # Decorative brush strokes.
    for _ in range(5):
        x = rng.randint(20, aw - 20)
        y = rng.randint(30, ah - 30)
        d.arc((x - 90, y - 35, x + 90, y + 35), rng.randint(0, 80), rng.randint(120, 220), fill=(255, 245, 215, 75), width=5)

    mask = rounded_mask(art.size, 36 * SCALE)
    base.alpha_composite(art, (x1, y1))
    return mask


def draw_card(card: Card) -> Image.Image:
    img = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    rarity = RARITY_COLORS.get(card.rarity, RARITY_COLORS["一般"])
    region_cols = REGION_PALETTES.get(card.region, ((70, 70, 75), (140, 140, 130), (95, 115, 130)))
    elem = ELEMENT_COLORS.get(card.element, region_cols[1])

    # Shadow and base.
    d.rounded_rectangle((34, 42, CARD_W - 24, CARD_H - 18), radius=54, fill=(0, 0, 0, 105))
    d.rounded_rectangle((24, 24, CARD_W - 34, CARD_H - 44), radius=58, fill=(*mix(region_cols[0], (32, 28, 25), 0.3), 255))
    d.rounded_rectangle((38, 38, CARD_W - 48, CARD_H - 58), radius=48, outline=(*rarity, 255), width=15)
    d.rounded_rectangle((62, 62, CARD_W - 72, CARD_H - 82), radius=34, fill=(244, 235, 214, 255))
    d.rounded_rectangle((78, 78, CARD_W - 88, CARD_H - 98), radius=28, outline=(*mix(rarity, (255, 255, 255), 0.32), 255), width=4)

    # Top controls.
    d.ellipse((82, 78, 196, 192), fill=(*mix(elem, (255, 255, 255), 0.1), 255), outline=(54, 43, 34, 255), width=5)
    draw_centered(d, (139, 133), card.cost, FONTS["big"], (255, 255, 250, 255))
    d.ellipse((CARD_W - 198, 88, CARD_W - 106, 180), fill=(*elem, 240), outline=(55, 48, 42, 255), width=4)
    draw_centered(d, (CARD_W - 152, 132), card.element or "无", FONTS["body"], (255, 255, 250, 255))
    d.rounded_rectangle((210, 84, CARD_W - 220, 166), radius=20, fill=(74, 57, 43, 235))
    draw_centered(d, (CARD_W // 2, 123), card.region, FONTS["subtitle"], (246, 236, 206, 255))

    # Art panel.
    art_box = (96, 198, CARD_W - 106, 1010)
    draw_art(img, card, art_box)
    d.rounded_rectangle(art_box, radius=40, outline=(58, 48, 39, 255), width=8)
    d.rounded_rectangle((art_box[0] + 12, art_box[1] + 12, art_box[2] - 12, art_box[3] - 12), radius=30, outline=(255, 247, 221, 80), width=3)

    # Name banner.
    title_y1, title_y2 = 1030, 1182
    d.rounded_rectangle((96, title_y1, CARD_W - 106, title_y2), radius=24, fill=(66, 48, 37, 245), outline=(*rarity, 255), width=5)
    name_font = FONTS["title"]
    if d.textlength(card.name, font=name_font) > CARD_W - 390:
        name_font = font(FONT_BOLD, 31 * SCALE)
    draw_centered(d, (CARD_W // 2, title_y1 + 52), card.name, name_font, (255, 248, 220, 255))
    subtype = f"{card.ctype} | {card.rarity} | {card.role}"
    if card.candidate:
        subtype += " | 候补"
    draw_centered(d, (CARD_W // 2, title_y1 + 112), subtype, FONTS["subtitle"], (226, 214, 187, 255))

    # Effect panel.
    panel = (96, 1210, CARD_W - 106, 2138)
    d.rounded_rectangle(panel, radius=30, fill=(253, 247, 231, 255), outline=(92, 75, 58, 255), width=5)
    text_x = panel[0] + 36
    y = panel[1] + 30
    effect = card.effect
    if card.keywords and card.keywords != "无":
        effect = f"【{card.keywords}】{effect}"
    fnt, lines = fit_text(d, effect, FONT_REG, 29 * SCALE, 21 * SCALE, panel[2] - panel[0] - 72, 12)
    line_h = int(fnt.size * 1.28)
    for line in lines:
        d.text((text_x, y), line, font=fnt, fill=(46, 40, 34, 255))
        y += line_h
    if card.flavor:
        y += 16
        d.line((text_x, y, panel[2] - 36, y), fill=(122, 104, 82, 120), width=2)
        y += 20
        ffnt, flines = fit_text(d, f"“{card.flavor}”", FONT_SERIF, 24 * SCALE, 18 * SCALE, panel[2] - panel[0] - 72, 3)
        for line in flines:
            d.text((text_x, y), line, font=ffnt, fill=(92, 78, 62, 255))
            y += int(ffnt.size * 1.24)

    # Bottom stats and ID.
    bottom_y = CARD_H - 254
    d.rounded_rectangle((96, bottom_y, CARD_W - 106, CARD_H - 116), radius=26, fill=(78, 61, 46, 246))
    d.text((128, bottom_y + 32), card.cid, font=FONTS["tiny"], fill=(220, 208, 184, 255))
    d.text((128, bottom_y + 78), card.source.replace("\\", "/"), font=FONTS["tiny"], fill=(190, 178, 158, 230))

    if re.match(r"^\d+\s*/\s*\d+$", card.stats):
        atk, hp = [s.strip() for s in card.stats.split("/")]
        d.ellipse((CARD_W - 286, bottom_y + 18, CARD_W - 192, bottom_y + 112), fill=(151, 66, 51, 255), outline=(255, 238, 190, 255), width=4)
        d.ellipse((CARD_W - 176, bottom_y + 18, CARD_W - 82, bottom_y + 112), fill=(65, 126, 77, 255), outline=(255, 238, 190, 255), width=4)
        draw_centered(d, (CARD_W - 239, bottom_y + 65), atk, FONTS["stat"], (255, 252, 236, 255))
        draw_centered(d, (CARD_W - 129, bottom_y + 65), hp, FONTS["stat"], (255, 252, 236, 255))
    else:
        d.rounded_rectangle((CARD_W - 272, bottom_y + 24, CARD_W - 86, bottom_y + 106), radius=26, fill=(*elem, 245), outline=(255, 238, 190, 255), width=4)
        draw_centered(d, (CARD_W - 179, bottom_y + 65), card.ctype or "法术", FONTS["body"], (255, 252, 236, 255))

    # Rarity shine.
    if card.rarity in ("史诗", "传说"):
        shine = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shine, "RGBA")
        for i in range(7):
            off = i * 280 - 420
            sd.line((off, 70, off + 720, CARD_H - 120), fill=(255, 244, 180, 28), width=18)
        img = Image.alpha_composite(img, shine)

    img = img.resize((W, H), Image.Resampling.LANCZOS)
    return img.convert("RGB")


def safe_name(text: str) -> str:
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", text)
    return re.sub(r"\s+", "", text)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 2
    while True:
        candidate = path.with_name(f"{stem}-v{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    cards = parse_cards(args.workspace)
    args.out.mkdir(parents=True, exist_ok=True)
    manifest_path = args.out / "card_faces_manifest.csv"

    rows = []
    for index, card in enumerate(cards, start=1):
        filename = f"{index:03d}_{safe_name(card.cid)}_{safe_name(card.name)}.png"
        out_path = args.out / filename
        if not args.overwrite:
            out_path = unique_path(out_path)
        draw_card(card).save(out_path, quality=95)
        rows.append(
            {
                "index": index,
                "id": card.cid,
                "name": card.name,
                "region": card.region,
                "element": card.element,
                "type": card.ctype,
                "rarity": card.rarity,
                "role": card.role,
                "candidate": "yes" if card.candidate else "no",
                "source": card.source,
                "file": str(out_path),
            }
        )

    with manifest_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Rendered {len(cards)} card faces")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

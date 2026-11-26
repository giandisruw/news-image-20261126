"""Draw the news-image-20261126 front page (1024x1024 PNG).

Run locally with:  python3 build_image.py
Writes entry.png next to this file. Uses Pillow only at build time;
the shipped entrypoint (main.py) is stdlib-only and just copies it.
No network, no clock, no randomness at render time (the star field
uses a fixed seed, so re-runs are byte-identical apart from PNG
encoder metadata, which Pillow keeps deterministic here).
"""

import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (248, 244, 236)
INK = (20, 24, 31)
NAVY = (16, 35, 63)
NAVY_LIGHT = (28, 58, 96)
RED = (179, 32, 44)
GOLD = (200, 155, 60)
GREY = (90, 92, 96)
RULE = (20, 24, 31)
WHITE = (255, 255, 255)
SKY_BLUE = (120, 180, 230)
EARTH_BLUE = (52, 110, 190)
EARTH_GREEN = (84, 150, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def draw_rocket_panel():
    """Lead illustration on its own panel so nothing can spill out."""
    pw, ph = 506, 372
    panel = Image.new("RGB", (pw, ph), NAVY)
    d = ImageDraw.Draw(panel)
    rng = random.Random(26)

    # Stars.
    for _ in range(70):
        x, y = rng.randint(6, pw - 6), rng.randint(6, ph - 120)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 225, 240))

    # Moon, top right.
    d.ellipse([pw - 118, 26, pw - 48, 96], fill=(235, 230, 205))
    d.ellipse([pw - 102, 44, pw - 88, 58], fill=(205, 198, 170))
    d.ellipse([pw - 84, 62, pw - 70, 76], fill=(205, 198, 170))

    # Earth: a big disc rising from the bottom edge, clipped by panel.
    d.ellipse([-150, ph - 130, 330, ph + 210], fill=EARTH_BLUE)
    d.ellipse([-40, ph - 90, 90, ph - 20], fill=EARTH_GREEN)
    d.ellipse([120, ph - 110, 240, ph - 40], fill=EARTH_GREEN)
    d.ellipse([-150, ph - 130, 330, ph + 210], outline=(140, 190, 240), width=3)

    # Rocket, climbing diagonally from lower left toward the moon.
    # Body: a long rounded shape drawn as a rotated polygon via a
    # temporary layer, so the angle is exact and the edges stay clean.
    rocket = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rocket)
    # Flame.
    rd.polygon([(150, 300), (185, 300), (168, 348)], fill=(255, 140, 40))
    rd.polygon([(158, 300), (178, 300), (168, 330)], fill=(255, 210, 90))
    # Fins.
    rd.polygon([(148, 250), (128, 300), (152, 292)], fill=RED)
    rd.polygon([(188, 250), (208, 300), (184, 292)], fill=RED)
    # Body and nose.
    rd.rounded_rectangle([148, 150, 188, 300], radius=18, fill=WHITE)
    rd.polygon([(148, 168), (188, 168), (168, 128)], fill=RED)
    # Window and stripe.
    rd.ellipse([156, 196, 180, 220], fill=SKY_BLUE, outline=NAVY, width=2)
    rd.rectangle([148, 246, 188, 256], fill=NAVY)
    rocket = rocket.rotate(28, resample=Image.BICUBIC, center=(168, 220))
    panel.paste(rocket, (0, 0), rocket)

    # Motion dots trailing the rocket.
    for i, (x, y) in enumerate([(96, 300), (76, 322), (58, 342)]):
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 210, 90))

    # Panel frame.
    d.rectangle([0, 0, pw - 1, ph - 1], outline=INK, width=3)
    return panel


def story_card(draw, x, y, w, h, tag, tag_colour, headline, body):
    """One small news card; text is wrapped to the card, never over it."""
    draw.rectangle([x, y, x + w, y + h], outline=(190, 184, 170), width=1)
    draw.line([x, y, x + w, y], fill=tag_colour, width=4)
    tx, ty = x + 14, y + 12
    tag_f = font(SANS_B, 14)
    draw.text((tx, ty), tag, font=tag_f, fill=tag_colour)
    ty += 22
    head_f = font(SERIF_B, 18)
    for line in wrap(draw, headline, head_f, w - 28)[:2]:
        draw.text((tx, ty), line, font=head_f, fill=INK)
        ty += 22
    ty += 2
    body_f = font(SANS, 14)
    for line in wrap(draw, body, body_f, w - 28)[:3]:
        draw.text((tx, ty), line, font=body_f, fill=(52, 56, 64))
        ty += 17


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)

    # ---- Masthead -------------------------------------------------
    centre(d, 26, "THE WORLD", font(SERIF_B, 70))
    centre(d, 104, "THURSDAY, 26 NOVEMBER 2026", font(SANS_B, 21))
    centre(d, 132, "THE DAY'S WORLD NEWS  —  IN ONE PICTURE",
           font(SANS, 15), fill=GREY)
    d.line([MARGIN, 158, W - MARGIN, 158], fill=RULE, width=2)
    d.line([MARGIN, 162, W - MARGIN, 162], fill=RULE, width=1)

    # ---- Lead story ----------------------------------------------
    lead_y = 176
    panel = draw_rocket_panel()
    img.paste(panel, (MARGIN, lead_y))
    # Caption under the art, inside the lead column.
    cap_f = font(SANS, 13)
    caption = "Shenzhou-24 lifts off from Jiuquan on a Long March-2F rocket."
    para(d, MARGIN, lead_y + 372 + 8, caption, cap_f, 506,
         fill=GREY, leading=17)

    rx = 566
    rw = W - MARGIN - rx  # 422
    y = lead_y + 2
    d.text((rx, y), "SPACE  •  CHINA — PAKISTAN", font=font(SANS_B, 16),
           fill=RED)
    y += 30
    head_f = font(SERIF_B, 44)
    for line in ["PAKISTAN", "REACHES", "ORBIT"]:
        d.text((rx, y), line, font=head_f, fill=INK)
        y += 52
    y += 4
    d.text((rx, y), "Shenzhou-24 docks with Tiangong",
           font=font(SERIF_B, 20), fill=NAVY)
    y += 32
    body = ("China's Shenzhou-24 launched from Jiuquan at 8:18 a.m. and "
            "docked about three and a half hours later. Muhammad Zeeshan "
            "Ali, a 40-year-old Pakistan Air Force pilot, is the first "
            "Pakistani in orbit — and the first foreign astronaut to "
            "visit the Tiangong station.")
    y = para(d, rx, y, body, font(SANS, 15), rw, leading=20)
    y += 6
    d.line([rx, y, W - MARGIN, y], fill=(190, 184, 170), width=1)
    y += 8
    crew = ("Crew: Tang Hongbo • Wu Yi • Muhammad Zeeshan Ali. "
            "He flies as a payload specialist for 5–10 days.")
    para(d, rx, y, crew, font(SANS, 13), rw, fill=GREY, leading=18)

    # ---- The rest of the day --------------------------------------
    sec_y = 596
    d.line([MARGIN, sec_y, 380, sec_y], fill=RULE, width=1)
    d.line([644, sec_y, W - MARGIN, sec_y], fill=RULE, width=1)
    centre(d, sec_y - 11, "THE REST OF THE DAY", font(SANS_B, 16))

    cards = [
        ("STRAIT OF HORMUZ", RED,
         "Two tankers hit mines in the Strait of Hormuz",
         "Two tankers exploded and caught fire on a route Iran called "
         "unauthorised; the claims were unverified."),
        ("NEW YORK", NAVY_LIGHT,
         "US jury convicts Huawei",
         "A New York jury found Huawei guilty of bank fraud and "
         "conspiracy to steal trade secrets."),
        ("GAZA CITY", RED,
         "Strike kills Hamas security chief in Gaza City",
         "An Israeli airstrike killed Hamas internal security chief "
         "Naeem Abu Nahel and members of his family."),
        ("CARTAGENA", NAVY_LIGHT,
         "20 hostages freed after a 17-hour siege",
         "Colombian forces stormed a supermarket in Cartagena and freed "
         "all 20 people alive."),
        ("MARKETS", (150, 110, 20),
         "Asian tech shares tumble as AI doubts deepen",
         "Japan's Nikkei fell 2.8%; South Korean shares dropped more "
         "than 6% at one point. Nvidia fell again."),
        ("BEIJING", NAVY_LIGHT,
         "Graft probe reaches China's Politburo",
         "Investigators opened an inquiry into Shanghai party chief "
         "Chen Jining — the fourth such probe since 2025."),
    ]
    cw = 304
    ch = 132
    gap = 20
    gx, gy = MARGIN, 622
    for i, (tag, colour, headline, body) in enumerate(cards):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + 10)
        story_card(d, cx, cy, cw, ch, tag, colour, headline, body)

    # ---- Ticker ----------------------------------------------------
    ty = 908  # band top; grid row 2 ends at 896
    d.rectangle([MARGIN, ty, W - MARGIN, ty + 66], fill=NAVY)
    d.text((MARGIN + 18, ty + 8), "ALSO TODAY",
           font=font(SANS_B, 15), fill=GOLD)
    tick_f = font(SANS, 15)
    d.text((MARGIN + 18, ty + 30),
           "Thanksgiving in the US  •  India marks Constitution Day  •  "
           "EU leaders meet in Brussels",
           font=tick_f, fill=WHITE)
    # Second ticker line sits inside the band on its own row.
    d.text((MARGIN + 18, ty + 48),
           "18 years since the Mumbai attacks of 26 November 2008",
           font=tick_f, fill=(200, 210, 225))

    # ---- Credit line ------------------------------------------------
    centre(d, 982, "Sources: Reuters, Nature, China Daily Asia and the "
           "26 November morning editions.",
           font(SANS, 12), fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

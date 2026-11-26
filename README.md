# THE WORLD — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/giandisruw/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/giandisruw/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Built for the [make.fun](https://make.fun/bounty/news-image-20261126) bounty
`news-image-20261126` — "Sum up 26 November's world news in one image".

## The image

A one-page newspaper front page for Thursday 26 November 2026,
drawn by a Python program (Pillow, build time only).

The front page leads with Pakistan reaching orbit: Shenzhou-24
launched from Jiuquan at 8:18 a.m. and docked with the Tiangong
station about three and a half hours later, carrying Muhammad
Zeeshan Ali — the first Pakistani in orbit and the first foreign
astronaut to visit Tiangong. The lead illustration shows the
rocket climbing past Earth toward the Moon.

Below it, six more stories from the day:

- **Strait of Hormuz** — two tankers hit mines, exploded and caught
  fire on a route Iran called unauthorised; the claims were unverified.
- **New York** — a US jury convicts Huawei of bank fraud and
  conspiracy to steal trade secrets.
- **Gaza City** — an Israeli strike kills Hamas internal security
  chief Naeem Abu Nahel and members of his family.
- **Cartagena** — Colombian forces free 20 hostages alive after a
  17-hour supermarket siege.
- **Markets** — Asian tech shares tumble as AI doubts deepen:
  Japan's Nikkei fell 2.8%, South Korean shares dropped more than
  6% at one point, Nvidia fell again.
- **Beijing** — a graft probe reaches China's Politburo with an
  inquiry into Shanghai party chief Chen Jining.

A dark ticker at the foot carries Thanksgiving in the United States,
India's Constitution Day, the EU leaders' meeting in Brussels, and
18 years since the Mumbai attacks of 26 November 2008.

## How it works

`build_image.py` renders the front page to `entry.png`
(1024×1024 PNG, well under the 1 MiB limit) with all text wrapped
to its column, so nothing overlaps or is cut off. The lead
illustration is drawn on a panel of its own, so the Earth's curve
is clipped to the panel and cannot spill onto the caption or the
stories below. No network, no clock, no randomness at render time
(the star field uses a fixed seed).

`main.py` is the entrypoint: standard library only, it checks the
bundled `entry.png` is a real PNG and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).
Running it twice writes byte-identical output.

To re-render the image locally:

```sh
python3 build_image.py
```

To test the entrypoint:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The rendered image was checked visually: every headline and
caption is legible, nothing overlaps, and the page fits its
1024×1024 frame.

## Files

- `main.py` — entrypoint: copies the bundled `entry.png` to the output directory (stdlib only)
- `build_image.py` — the drawing code and all story text (Pillow, build time only)
- `entry.png` — the rendered front page
- `NOTES.md` — research notes: every story with its sources
- `README.md` — this file
- `LICENSE` — MIT licence
- `.makefun/owner.json` — claim file naming the payout wallet

# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/simpson007/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/simpson007/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A program that writes one image summing up the world's news of Tuesday 17 November 2026 — the US–Iran clash in the Gulf, Ukraine's strike on the Crimea bridge, the Manila Quad summit and a market sell-off — to /output/entry.png.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## What's in the picture

A one-page newspaper front page for Tuesday 17 November 2026:

- **Lead — The Gulf:** Bahrain said its defences shot down Iranian drones aimed at a US radar site; US warplanes hit a missile site on Qeshm Island; a tanker was hit by a mine in the Strait of Hormuz.
- **Ukraine:** Kyiv's 1,300-drone barrage hit the Crimea bridge; Russia struck bridges in Kyiv in reply.
- **Manila:** Trump met Modi at the Quad, on the sidelines of the ASEAN summit.
- **Markets:** Nasdaq −2.5% (into correction), S&P −1.9%, Dow −1.4%, Brent −3.6%, gold −0.8%.
- **Also:** COP31's fossil-fuel exit draft, five EU states planning a Rwanda return hub, Japan scrambling jets, Gaza aid crossings, Pattinson as Bond, Amazon's lost satellites.

## How it was made

`render.py` draws the front page with Pillow (deterministic: fixed text and geometry, no network, no randomness) and writes `entry.png` (1024×1024, about 135 KiB). `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ngqr1ydj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>

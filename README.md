# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/tianmin-magic/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/tianmin-magic/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up the world's news of
**Sunday, 22 November 2026**, rendered as a single 1024×1024 PNG.
Entered on [make.fun](https://make.fun/?ref=bwae5nj9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
in the "Sum up 22 November's world news in one image" bounty ($100 in USDC).

## The image

`entry.png` — masthead with the date, one lead story and four more across
regions and fields, plus an "also today" strip:

- **Lead, Climate:** COP31 talks in Antalya collapse as the fossil-fuel
  row sinks the deal — the first major breakdown since 2009.
- **Gulf:** Two wounded as Iran strikes Bahrain again; Tehran claims it
  hit two US Patriot radars.
- **Disaster:** Factory fire in Indonesia kills 3, 36 missing.
- **War in Ukraine:** Russian drone collapses a Kyiv building, 14 trapped.
- **Law:** World Court rules Myanmar committed genocide against the
  Rohingya, the first time a state has been found responsible.
- **Also today:** France protests enter sixth weekend; Mexico cartel boss
  captured, 11 dead; US stocks fall into correction; EU-Indonesia trade
  deal signed; Delta glitch delays Atlanta flights; Nigeria boat toll
  rises to 24.

All events were reported 19–22 November 2026 (news cutoff about 06:00 UTC,
14:00 Beijing, 22 November). Sources are listed per story in
`data/stories.json`.

## How it is made

`tools/render.py` draws `entry.png` from `data/stories.json` with Pillow
(flat typographic front-page layout, Liberation fonts, no network, fully
deterministic). `main.py` — the graded entrypoint, standard library only —
copies `entry.png` to `/output/entry.png`, so both grader runs write
identical bytes.

```sh
python3 tools/render.py   # re-render entry.png from data/stories.json
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=bwae5nj9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

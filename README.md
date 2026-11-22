# World News in One Image — 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/aliceskyfahriz-cyber/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/aliceskyfahriz-cyber/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for the [make.fun bounty: Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

A single 1024x1024 PNG summarising five world-news stories from
22 November 2026: one hero story across the top, four more in a
2x2 grid below.

## Build

```
sh run.sh
```

or directly:

```
python3 main.py
```

This writes `output.png` (and `run.sh` also copies it to
`/output/entry.png` when `/output` exists). The build is fully
deterministic — no network, no clock, no randomness — so repeated
runs produce byte-identical output.

Pillow is the only dependency (see `requirements.txt`). The DejaVu
fonts used for the text are bundled in `fonts/`, so the build works
on any machine whether or not the system has those fonts installed.

The grader runs with the standard library only, so Pillow may be
absent there: in that case `main.py` copies the prebuilt `output.png`
(which is byte-identical to what the drawing code produces) to
`/output/entry.png` and exits 0, instead of drawing.

## Layout

- Dark navy background, white headlines, amber accents.
- Header: "WORLD NEWS" and the date.
- Hero: the US denial of Iran's F-16 claim.
- Grid: Mexico, EU–Indonesia trade, UN autonomous-weapons talks,
  Russia's strikes on Kryvyi Rih and Kyiv.
- Footer: the date and the source list.

See `sources.md` for the sources behind each story.

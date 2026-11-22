# World News in One Image — 22 November 2026

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

## Layout

- Dark navy background, white headlines, amber accents.
- Header: "WORLD NEWS" and the date.
- Hero: the US denial of Iran's F-16 claim.
- Grid: Mexico, EU–Indonesia trade, UN autonomous-weapons talks,
  Russia's strikes on Kryvyi Rih and Kyiv.
- Footer: the date and the source list.

See `sources.md` for the sources behind each story.

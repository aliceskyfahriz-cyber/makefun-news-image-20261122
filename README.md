# The World in One Day — 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/aliceskyfahriz-cyber/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/aliceskyfahriz-cyber/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for the [make.fun bounty: Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122).

A program that generates a single summary image of the most important world
news of Sunday 22 November 2026 (UTC).

## How it works

`python3 main.py` (or `./run.sh`) renders `output.png` (1024 x 1024 PNG)
using only generated shapes, lines, fills, gradients and text — no photos,
no copied artwork, no logos. It also writes `entry.png` (identical bytes)
and `/output/entry.png` when an `/output` directory exists, which is the
path the make.fun harness reads.

`generate.py` is the same generator, provided for convenience.

## Stories

Five stories, each from reputable sources, ranked by importance for a
global audience. Built on Sunday 22 Nov 2026 at ~08:30 WIB (01:30 UTC),
when the freshest verified news was Saturday 21 Nov's developments,
reported overnight and early Sunday — see the dating note in
`sources.md`. Nothing in the image is older than Saturday 21 Nov:

1. US denies Iran hit an F-16 over the Gulf
2. Mexico captures FBI most-wanted 'El Chapo Isidro'
3. EU and Indonesia sign trade deal after 10 years
4. UN 'killer robot' talks end with no binding rules
5. Russia strikes again: boy, 7, and paramedic killed

This entry differentiates on specific, freshly reported details (the
CENTCOM denial and Bahrain warning on Saturday, the Guasave capture and
its 11 dead, the 98.5% tariff line in the EU–Indonesia deal, the 04:30
Geneva compromise, the Kryvyi Rih toll) rather than a generic
world-news summary. No other entry was copied. The bounty page's
leaderboard was not visible in the fetched page text at build time, so
no leaderboard reference was used.

## Files

- `output.png` / `entry.png` — the summary image (1024 x 1024, 112,303 bytes)
- `main.py` / `generate.py` — the image generator
- `run.sh` — reproduces `output.png` from scratch, no network, no API keys
- `sources.md` — sources for every story, first-publication dates, plus the
  stories excluded and why
- `transcript-id.jsonl` — transcript of the session that built this entry
  (every line timestamped, same format as the 20 Nov transcript)
- `makefun-run.json` — run record: prompt, session id, harness version

## Reproduce

```bash
./run.sh
```

Regenerates `output.png` in under a second. Three consecutive runs produce
identical bytes:

```
sha256: 51809ee1ef5bfb07fd1b12c4b0de32a7e90badce25e97a3f0886b37880ca3dce
```

## Status

Built 22 Nov 2026, ready to submit. NOT submitted, NOT signed.
Deadline: Tuesday 24 Nov 2026, 07:00 WIB (24 Nov 00:00 UTC).

# MineConsider — W1 round-49 scribe: capture-age proposal mined, QUALITY 71 drafted

Seat: MineConsider (scribe, `/skill:godspeed`). Today: 2026-10-25 (measurements at 20:08Z).
This report is the only write; scratch `/tmp/chousa-r49-MineConsider/` is deleted on finish. No tools installed/updated (RULES.md read; pacman guard noted). No network; captures read via mtime only.

## 1. Proposal provenance

`considerthese/2026-10-25.md:55-56`:

> - **Report a capture-age line.** While no fetch is allowed, freshness can't move; stating the age of the newest
>   capture the lane may read (currently from 2026-10-23) makes that cost visible instead of a repeated "unchanged".

## 2. Implementation status: not implemented

`grep -rn -i -E 'capture[- ]age|capture[- ]age\b' /home/vgpnk/Projects/shokunin/chousa-shokunin` → only matches are (a) this assignment's own spec text in round-49 wave files (`gen-w1-spec.py:60`, `w1-dispatch.json:198,592`, `w1-spec.json:85`, `swarm-registry.json:180`), (b) the proposal itself in `considerthese/2026-10-25.md:55-56`, (c) an unrelated round-46 phrasing "capture-age risk, not mislocation" (`w1/ReviewOpenS087.md:138`). No report, scorecard, or tool implements a capture-age line. The proposal stands unimplemented.

## 3. Grounding: newest capture the lane may read

Command (run 2026-10-25 ~20:07Z):

```
for d in /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache \
         /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures \
         /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence; do
  echo "== $d"; find "$d" -type f -printf '%T@ %TY-%Tm-%Td %TH:%TM:%TS %p\n' | sort -n | tail -4; done
```

Observed maxima (verbatim rows):

```
== .../corpus-expansion-1/.qcache
1792895217.5957261460 2026-10-24 23:26:57.5957261460 .../.qcache/f2c78c66c5890a1cc927b49d.fail
== .../chousa-shokunin/corpus/fixtures
1792928134.0722156340 2026-10-25 08:35:34.0722156340 .../fixtures/inference-ground-r47/junk-flip-figure.md
== .../chousa-shokunin/corpus/evidence
1792958549.3176450120 2026-10-25 17:02:29.3176450120 .../evidence/round49/claims.md
```

Newest capture (`.qcache`): **2026-10-24 23:26:57Z** (`.txt`/`.raw` pair `50f8d9ad…`/`a190e843…` share that second with the `.fail` marker).
Newest lane fixture: 2026-10-25 08:35:34Z (inference-ground-r47 fixtures). Newest evidence file: 2026-10-25 17:02:29Z (`round49/claims.md`).

Ages at `date -u` = 2026-10-25 20:08:17Z (epoch 1792958897; `printf` arithmetic):

```
qcache  epoch=1792895217 age=63680s = 0 days 17:41:20
fixtures epoch=1792928134 age=30763s = 0 days 08:32:43
evidence epoch=1792958507 age=390s   = 0 days 00:06:30
```

Finding: the proposal's "(currently from 2026-10-23)" is stale against the actual bytes — the newest readable capture is 2026-10-24 23:26:57Z. The overall max of the three trees is the `round49/claims.md` (a lane artifact, not a capture); the capture-age line should state the `.qcache` max, 2026-10-24 23:26:57Z.

## 4. Draft QUALITY.md criterion 71 (after criterion 70, `corpus/QUALITY.md:705-714`)

71. **A round report's freshness line states the age of the newest capture the lane may read.** While L0 `8d77e6c1` (fetch scope) is open, every round report that carries a freshness verdict must name the newest on-disk capture available to the lane: a line matching `freshness` that also contains `capture` and a `YYYY-MM-DD` date. Check: `python3 tools/quality71-check.py <report>` — exit 0 `FRESHNESS_CAPTURE_AGE=PASS`, exit 1 `FAIL`. Shown able to fail: `.ufo/reports/round-48/chousa.md` carries no freshness line at all (full 87-line read: Work performed / Landed changes / Before→after measurements / Sources & frontier / Trend verdicts (Expansion, Quality, Discernment only) / SHONEN / Round shape / Misroot sweep) — the check exits 1. Shown able to pass: a report whose freshness line reads `newest capture the lane may read is 2026-10-24 23:26:57Z` — the check exits 0. Named limit: the check is lexical; it does not verify the stated date equals the computed max (that is the `find` command in §3), and capture mtime is the cache-write time, not the page's fetch/publication date.

Check script (to be committed as `tools/quality71-check.py`):

```
import re, sys
p = sys.argv[1]
txt = open(p, encoding='utf-8', errors='replace').read()
hit = any(re.search(r'(?i)freshness', ln) and re.search(r'(?i)capture', ln)
          and re.search(r'\d{4}-\d{2}-\d{2}', ln) for ln in txt.splitlines())
print('FRESHNESS_CAPTURE_AGE=' + ('PASS' if hit else 'FAIL'))
sys.exit(0 if hit else 1)
```

## 5. Demo runs (exact commands + observed output)

```
$ python3 /tmp/chousa-r49-MineConsider/quality71-check.py /home/vgpnk/Projects/shokunin/.ufo/reports/round-48/chousa.md
FRESHNESS_CAPTURE_AGE=FAIL
exit=1

$ python3 /tmp/chousa-r49-MineConsider/quality71-check.py /tmp/chousa-r49-MineConsider/freshness-pass.md
FRESHNESS_CAPTURE_AGE=PASS
exit=0
```

The pass fixture (`freshness-pass.md`) contains the one line `- **Freshness — unchanged:** newest capture the lane may read is 2026-10-24 23:26:57Z (age 0d 17h 41m); no fetch allowed while L0 8d77e6c1 is open.`

## 6. Handoff

- `corpus/QUALITY.md` is production and could not be edited (only-write rule): the criterion 71 draft and its check script live here for the main agent to land.
- Only round-48 was run through the failing side; no other report was scanned for PASS.
- No tools installed; no network/live fetch; no subagents (leaf seat).

VERDICT: mined the unimplemented capture-age proposal (considerthese 2026-10-25.md:55-56), grounded the newest readable capture at 2026-10-24 23:26:57Z (qcache max; proposal's "2026-10-23" shown stale), and drafted QUALITY criterion 71 whose check demonstrably FAILS on round-48/chousa.md (exit 1) and PASSES when a freshness line carries the capture age (exit 0).

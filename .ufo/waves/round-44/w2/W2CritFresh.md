# W2CritFresh — a pre-launch capture is not a freshness improvement

seat: W2CritFresh (critic, leaf)
round: 44
wave: 2
date: 2026-10-24
write scope: this file only. No fetch. No SCORECARD edit. No production edit.

## Axes

- operability: the comparison is a local `stat` against the watchdog launch line. No network. A later reader can re-run the commands below.
- calibration: the grade is unchanged, not improved, and not harmed. A cache open can still support a depth quote-location. It must not be counted again as freshness. No numeric freshness score is invented.
- depth: freshness here means a live surface was re-observed after launch. A file written before launch is an earlier process's stored rendering. Hashing it shows the stored bytes are still those bytes.

## Route 2, quoted

From `corpus/lessons/round-43-verifier-spotcheck.md` line 159, the route 2 text:

> 2. Freshness self-grade. Next scorecard must not call a pre-round cache open a freshness improvement. Closure grade is unchanged, not harmed.

The rule sentence inside that item is: "Next scorecard must not call a pre-round cache open a freshness improvement."

The grade sentence in the same item is: "Closure grade is unchanged, not harmed."

The finding that route points at, same file line 113:

> **freshness: unchanged.** The lane's scorecard says improved narrowly. The only open is a capture written the day before launch. No live surface was re-checked. Not harmed.

## Why a capture written before this round's launch is not a freshness improvement

This round's launch is the earliest instant a "re-checked this round" claim can be true. The closure used that clock for round 43. The same file gives this round's launch:

```
2026-10-24T21:36:37-03:00 launch chousa round=44 pgid=3105723 driver=hyaku-inline attempt=1
```

Source: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` line 1223. It is the only `launch chousa round=44` line. There is no `complete chousa round=44` line yet. That does not move the bound. Reading a file after launch does not make the file a this-round observation.

A capture is a stored rendering. Its mtime and ctime are the write time of that file. If both precede launch, this round did not write the observation and did not compare it to the URL. Opening the file, recording sha256, and finding a quote observes the stored bytes. It does not observe whether the URL still serves those bytes. The round-43 scorecard cell that the closure rejected already says the missing half out loud: "S078 opened from a committed capture, sha256 recorded; no fetch" (`SCORECARD.md` line 2373). "No fetch" is the absence of a live re-check, not a freshness proof. Calling that open improved counts one cache read as two axes: depth (the quote is in the stored bytes) and freshness (the surface was re-checked). Route 2 forbids the second count. The first can still hold. The axis is not harmed, because the stored bytes are still there and still match the recorded hash.

"Committed" does not repair the date. Both capture paths fail `git -C /home/vgpnk/Projects/shokuknow ls-files --error-unmatch` (exit 1, pathspec not known to git). The sha256 of the Europe PMC file is recorded in tracked lane files (`corpus/SOURCES.md` line 88; `corpus/knowledge/search-log-method-r39.md` line 26). A hash written into a row is a registry fact about an older file. It is not a new observation at launch.

Wave 2's own start is later than the round launch, so it is not a looser bound and cannot rescue a pre-round file:

```
acquire_start 2026-10-24T21:49:57-03:00
launch_start 2026-10-24T21:49:57-03:00
```

Source: `.ufo/waves/round-44/w2-launcher-outer.log`. `date -d @1792889397` on the wave-2 parent-lifetime receipt epoch prints `2026-10-24T21:49:57-0300`, the same instant.

## Measured files

Both captures live under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`. Keys are sha256 of the URL, first 24 hex digits. No URL was fetched.

Round-43 exemplar, the capture the closure graded unchanged. URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`, key `2cef078d8f9f87802e19e770`.

```
stat /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt size=80107 mtime=2026-10-23 20:40:06.022034917 -0300 ctime=2026-10-23 20:40:06.022034917 -0300
833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
```

Size 80107 and sha256 `833b13e3…` match the closure and the S078 row. Mtime equals ctime, both `2026-10-23T20:40:06-0300`. That is 87573 seconds before the round-43 launch `2026-10-24T20:59:39-03:00`, and 89791 seconds before this round's launch. The 12-word quote named in `corpus/knowledge/search-log-method-r39.md` line 25 is in this file at byte offset 17410 (12 words). This seat does not adopt the closure's "byte offset 17383" as the start of that 12-word string: bytes 17383:17410 are `ly in the database itself, `. The quote is in the pre-launch file. The 27-byte pointer slip does not create a freshness improvement and does not remove the quote.

This round's C3 capture, the file `corpus/evidence/round44/c3-count.py` reads by URL. URL `https://www.rfc-editor.org/rfc/rfc7089.txt`, key `d0c4a09a9de32cb91d5e3797`.

```
stat /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt size=107130 mtime=2026-10-23 20:33:05.526350588 -0300 ctime=2026-10-23 20:33:05.526350588 -0300
c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
```

Mtime equals ctime, both `2026-10-23T20:33:05-0300`, 90212 seconds before this round's launch and 91012 seconds before the wave-2 launch. The C3 quote `constitutes a promise that the resource state` is in that file at byte offset 14896. Presence of the quote is a depth predicate if an entry and an S079 row later cite it. It is not a freshness improvement. `corpus/SOURCES.md` has 0 rows matching `| S079`. `corpus/knowledge/citation-version-binding-r36.md` does not exist in the lane tree. There is not yet a new row whose open could be mis-scored. If one is added from this file, the freshness cell still stays unchanged.

`corpus/evidence/round44/claims.md` lines 13–14 already say freshness is not a claim and that a pre-round capture open is not a freshness improvement. That sentence is the frozen rule, not this seat's measurement. The mtimes above are what make the rule operable.

## Boundary, so the rule is not widened

Route 2 names a pre-round cache open with no live re-check. It does not say that every local file older than launch is freshness-inert. Round 42's closure agreed a narrow freshness improvement for opening the installed `pdftotext` manual and recording its sha256. This seat re-stated that file only as a boundary:

```
pdftotext_man size=1890 mtime=2026-08-21 04:51:48.000000000 -0300
```

That mtime is also before its round's launch (`2026-10-24T19:58:10-03:00`). This seat does not reopen the round-42 grade and does not treat mtime-before-launch, by itself, as the whole rule. The defect route 2 names is the cache open: the only new act was reading a campaign `.qcache` file written the day before launch, and no live surface was re-checked.

## Grade

Freshness for a capture written before `2026-10-24T21:36:37-03:00`: **unchanged**. Not improved. Not harmed. The next scorecard must not call that open a freshness improvement, narrowly or otherwise. This seat did not edit `SCORECARD.md`. Line 2373 remains the round-43 inflation; route 2 says the next block must not repeat it.

## Commands

Local only. No `curl`, `wget`, or fetch. No `jj`. No `git commit`.

- `stat -c 'stat %n size=%s mtime=%y ctime=%z'` on the two `.qcache` paths above
- `sha256sum` on those two paths
- `git -C /home/vgpnk/Projects/shokuknow ls-files --error-unmatch` on both relative paths → exit 1
- `date -d @1792889397` and `date -d @1792889279`
- Python `find` of the two quote byte strings; no article text printed
- `rg -n "launch chousa round=44" /home/vgpnk/Projects/shokunin/.ufo/watchdog.log` → one line, 1223

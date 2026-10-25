# W2ScribeFresh — round 44, wave 2

Seat: chousa leaf scribe. Milestone: Round 44 wave 2: genuine seats after the usage-error wave.
Assigned item only: draft the SCORECARD freshness sentence. It must say unchanged, not improved.
Measured clocks below. No production file was edited. `SCORECARD.md` was not edited. No fetch. No `jj`. No git commit.

## Draft sentence

Paste this sentence. Do not paste a freshness grade that says improved.

Freshness is unchanged, not improved: the RFC 7089, WARP, and E2867 captures named by this wave were written on 2026-10-23, before round-44 launch at 2026-10-24T21:47:59-0300, and no live surface was re-checked.

Paste-ready scorecard row, same grade, house table form (`SCORECARD.md` round-43 row is the shape, not the grade):

| freshness | **unchanged** | RFC 7089, WARP, and E2867 captures named by this wave were written on 2026-10-23, before launch 2026-10-24T21:47:59-0300; no live surface was re-checked |

`SCORECARD.md` has no Round 44 section yet (search for `Round 44` returned no matches). This row is a draft for that later block. It does not rewrite the round-43 row.

## Axes

1. Operability — one paste-ready sentence and one table row, each saying unchanged, bound to a named launch clock and to captures this seat statted. Production scorecard left untouched.
2. Calibration — the grade is unchanged, not improved. A pre-round cache open is not upgraded. Unrun live checks are not reported as passes.
3. Depth — birth time and mtime, URL-prefix binding for the RFC file, launcher wall clock matched to the receipt epoch, and the wave-1 log quoted as a usage error rather than a recheck.

## Why the grade is unchanged

Round-43 closure route 2, `corpus/lessons/round-43-verifier-spotcheck.md:159`:

~~~~
2. Freshness self-grade. Next scorecard must not call a pre-round cache open a freshness improvement. Closure grade is unchanged, not harmed.
~~~~

The owned-axis line that route points at (`corpus/lessons/round-43-verifier-spotcheck.md:113`):

~~~~
- **freshness: unchanged.** The lane's scorecard says improved narrowly. The only open is a capture written the day before launch. No live surface was re-checked. Not harmed. Routed below so the next scorecard does not repeat the inflation.
~~~~

Frozen claims, `corpus/evidence/round44/claims.md:12-14`:

~~~~
Freshness is not a claim. A pre-round capture open is not a freshness
improvement (round-43 closure route 2).
~~~~

Freeze log, `LOG.md:1565`:

~~~~
- Freshness will not be scored improved from a pre-round capture. The round-43 closure routed that inflation.
~~~~

The round-43 scorecard cell this draft must not copy (`SCORECARD.md:2373`):

~~~~
| freshness | **improved narrowly** | S078 opened from a committed capture, sha256 recorded; no fetch |
~~~~

That cell is the inflation route 2 names. Round 44 still reads a committed capture and still does not re-check a live surface. The assimilation draft `/.ufo/waves/round-44/assimilation/draft/citation-version-binding-r36.md` says `verified-at: 2026-10-24`, `opened from a committed capture`, and `No live TimeGate was opened`. That draft is not in `corpus/knowledge/` and `S079` is not a row in `corpus/SOURCES.md` (search for `S079`, `rfc7089`, and `RFC 7089` returned no matches). Even if that open lands, it is a pre-round cache open. It is not a freshness improvement.

## Clocks (quoted)

Wave-1 launcher, `.ufo/waves/round-44/launcher-outer.log`:

~~~~
acquire_start 2026-10-24T21:47:59-03:00
granted lane=chousa wave=round-44-w1 seats=64 live=43 pending=64 cap=256
launch_start 2026-10-24T21:47:59-03:00 parent_will_be_child
launcher_exit=0 2026-10-24T21:48:02-03:00
released lane=chousa wave=round-44-w1
~~~~

Wave-1 receipt start and end, `corpus/evidence/round44/parent-lifetime.receipt`:

~~~~
start parent_pid=3226659 epoch=1792889279
reap name=ScribeFreshnessLine child_pid=3227187 exit_code=1 epoch=1792889282
end parent_pid=3226659 epoch=1792889282 n_spawned=64 n_reaped=64
~~~~

Wave-2 launcher, `.ufo/waves/round-44/w2-launcher-outer.log`:

~~~~
acquire_start 2026-10-24T21:49:57-03:00
granted lane=chousa wave=round-44-w2 seats=32 live=44 pending=0 cap=256
launch_start 2026-10-24T21:49:57-03:00
~~~~

Wave-2 receipt start, `.ufo/waves/round-44/w2-parent-lifetime.receipt` line 1: `start parent_pid=3259975 epoch=1792889397`. That file had no `end` line when read.

`date` against those epochs, then `stat` of the three qcache files named by this wave, then the RFC URL prefix. Command and output:

~~~~
$ printf 'wave1_local='; date -d @1792889279 '+%Y-%m-%dT%H:%M:%S%z'; printf 'wave1_utc='; date -u -d @1792889279 '+%Y-%m-%dT%H:%M:%SZ'; printf 'wave2_local='; date -d @1792889397 '+%Y-%m-%dT%H:%M:%S%z'; printf 'wave2_utc='; date -u -d @1792889397 '+%Y-%m-%dT%H:%M:%SZ'; echo '--- stat ---'; stat -c '%n size=%s mtime_epoch=%Y mtime=%y birth_epoch=%W' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt; echo '--- url prefix ---'; python3 -c 'import hashlib; print(hashlib.sha256(b"https://www.rfc-editor.org/rfc/rfc7089.txt").hexdigest()[:24])'
wave1_local=2026-10-24T21:47:59-0300
wave1_utc=2026-10-25T00:47:59Z
wave2_local=2026-10-24T21:49:57-0300
wave2_utc=2026-10-25T00:49:57Z
--- stat ---
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt size=107130 mtime_epoch=1792798385 mtime=2026-10-23 20:33:05.526350588 -0300 birth_epoch=1792798385
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt size=28659 mtime_epoch=1792798570 mtime=2026-10-23 20:36:10.486713407 -0300 birth_epoch=1792798570
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt size=13942 mtime_epoch=1792798580 mtime=2026-10-23 20:36:20.291295276 -0300 birth_epoch=1792798580
--- url prefix ---
d0c4a09a9de32cb91d5e3797
~~~~

Launcher wall clocks match the receipt epochs. For each of the three files, birth epoch equals mtime epoch, and both are before wave-1 launch epoch `1792889279` and wave-2 launch epoch `1792889397`. The RFC filename is the first 24 hex digits of sha256 of `https://www.rfc-editor.org/rfc/rfc7089.txt`, which is the URL `corpus/evidence/round44/c3-count.py` reads from the local qcache. That counter opens `CACHE / (key + ".txt")`. It does not fetch.

Comparison against wave-1 launch epoch `1792889279` (separate local python `stat`, same files):

~~~~
FILE d0c4a09a9de32cb91d5e3797.txt
  size=107130
  mtime_epoch=1792798385
  mtime_local=2026-10-23T20:33:05-0300
  mtime_utc=2026-10-23T23:33:05Z
  before_wave1_launch=True
  delta_sec_mtime_minus_wave1=-90894
FILE 5f54e82c87a76eefdc9a0d35.txt
  size=28659
  mtime_epoch=1792798570
  mtime_local=2026-10-23T20:36:10-0300
  mtime_utc=2026-10-23T23:36:10Z
  before_wave1_launch=True
  delta_sec_mtime_minus_wave1=-90709
FILE 0034b800811072de3980e85b.txt
  size=13942
  mtime_epoch=1792798580
  mtime_local=2026-10-23T20:36:20-0300
  mtime_utc=2026-10-23T23:36:20Z
  before_wave1_launch=True
  delta_sec_mtime_minus_wave1=-90699
~~~~

The RFC file is 90894 seconds before wave-1 launch. Same pattern as the round-43 spot-check: a capture written the day before launch.

## No live recheck (what was run, and what was not)

Wave-1 scribe log, entire file `corpus/evidence/round44/seat-logs/ScribeFreshnessLine.log`:

~~~~
error: Cannot combine --prompt with --auto.
~~~~

That wave reaped `ScribeFreshnessLine` at exit 1 three seconds after start. It did not re-check a live surface. This wave's draft is the first freshness sentence for the round.

Search of `corpus/evidence/round44` `*.py` and `*.sh` for `urlopen`, `curl`, or `wget`: no matches. `LOG.md:1559` records no external fetch at the freeze (`L0 8d77e6c1` still open). This seat did not fetch, did not run `tools/quote-reopen.py`, and did not run `research-gate.sh --drift`. Those unrun checks have not passed. The sentence does not claim `GATE_DRIFT: none`, a live TimeGate, or a new drift detector.

## Gates

| Gate | Result | Basis |
|---|---|---|
| Sentence says unchanged, not improved | HOLD | Draft sentence and table row above. Verdict word is unchanged. |
| Reason is pre-launch captures, no live recheck | HOLD | `stat` birth and mtime 2026-10-23; launch 2026-10-24T21:47:59-0300; counters have no fetch calls; wave-1 log is the usage error. |
| SCORECARD.md not edited | HOLD | Only this report was written. `Round 44` is absent from `SCORECARD.md`. |
| Round-43 row rewritten | NOT DONE | Append-only. The inflated cell stays as history. |
| C1 / C2 / C3 counters | NOT RUN | Not this item. Not scored here. |
| Live re-open or `--drift` | NOT RUN | Not a pass. |

## Out of scope

- S077 by document rather than arithmetic. Named in the wave context. Not this sentence.
- Gate admit for S079 and the 11-column row. Other scribe seats. Not appended here.
- File sha256 of the RFC capture as printed in the assimilation draft. Not recomputed here. The URL-prefix check above is the binding this seat ran.

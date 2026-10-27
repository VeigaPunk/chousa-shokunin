# R57W1CritC2Controls — attack on the R57-C2 controls' probative value

Seat: R57W1CritC2Controls (leaf critic, no subagents). Lane tip at dispatch f9736a39a0.
Frozen refs: claims base 6656f0770a1460d6ba73d9d2976f698a35311921; C2 frozen at c2f914c53201a8f8ee4fef823b82681051d55592.
Scratch: /fast/scratch/hyaku/chousa-r57/R57W1CritC2Controls (TMPDIR=$PWD, PYTHONDONTWRITEBYTECODE=1); deleted before yield.

## Method

The frozen counter was never copied for mutation — only imported read-only (importlib) by my fixture
builder, and invoked directly against scratch fixture roots via its own `--root` flag (store,
refetch.tsv, lesson read from `--root`; pinned set read from the lane via read-only git). Frozenness
of the counter under test:

    $ git -C .../chousa-shokunin show c2f914c5...:corpus/evidence/round57/c2-count.py | sha256sum
    d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9  -
    $ sha256sum .../corpus/evidence/round57/c2-count.py
    d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9

identical — the counter exercised below is the frozen one.

Context observed while building: lane store now holds 41 reproduced-capable + 5 drifted-capable
genuine pairs (46/47; dispatch note said 43/47 — L1 retries progressed). I used genuine bytes
read-only.

## Attacks (fixture → observed frozen-counter output)

1. ALLFAIL rebuilt at 599 s spacing (two curl_rc=28 rows 10:00:00Z / 10:09:59Z per URL):
   `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL` exit=1
   → counter did NOT call it UNREACHABLE. Spacing leg holds at boundary-1.

2. ALLFAIL rebuilt at 600 s spacing (10:00:00Z / 10:10:00Z):
   `SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=47 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL` exit=1
   → 600 s IS accepted (`(fails[-1]-fails[0]).total_seconds() >= 600`; "at least 600 seconds", inclusive).

3. EMPTY-with-header-only refetch.tsv (header row, zero data rows):
   `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL` exit=1
   → header presence alone creates no verdicts; parser does not crash on zero rows.

4. JUNK variant with .txt NOT recipe-consistent (random 4096-byte raw, deliberately wrong .txt,
   successful records, FLAG lines written for all 47 so FLAGGED cannot mask the leg):
   `SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 UNREACHABLE=0 BYTE_BACKED=47 CONSISTENT=0/47 FLAGGED=47/47 C2=FAIL` exit=1
   → CONSISTENT leg fails it even though every verdict exists and flags match. The leg is live.

5. Do-nothing reaching BYTE_BACKED=32 / REPRODUCED=5 (5 genuine REPRODUCED pairs S082 S085 S086
   S088 S089; 5 genuine DRIFTED pairs S083 S087 S113 S114 S121 absent=0; 22 random-bytes pairs with
   recipe-consistent .txt as DRIFTED; 15 triples with fabricated two-failure >=600 s records as
   UNREACHABLE — the 15 are required because PASS also demands VERDICTS=47/47):
   `SET=47 VERDICTS=47/47 REPRODUCED=5 DRIFTED=27 UNREACHABLE=15 BYTE_BACKED=32 CONSISTENT=32/32 FLAGGED=22/22 C2=PASS` exit=0
   verbose spot-check: `CAPTURE S082 ... REPRODUCED`, `CAPTURE S083 ... DRIFTED absent=0/2`,
   `CAPTURE S090 ... DRIFTED absent=8/8`, `CAPTURE S121 ... DRIFTED absent=0/6`.

## Assessment of the do-nothing (frozen — reported, not patched)

The predicate's wording does permit it, and this was disclosed before data. claims.md "What the
counter cannot prove (disclosed before data)": "A forge with five genuine captures and 27 random-byte
'drifted' ones would pass; the REPRODUCED count is printed separately for that reason and the wave
attacks it." My fixture matches that disclosure exactly in mechanism: only REPRODUCED is bound to the
pin by sha256; DRIFTED and UNREACHABLE are fetch-record attestation that any lane-side writer can
fabricate (my 22 random pairs + 15 failure records were constructed in scratch in seconds). The
printed summary line separates the counts for precisely this reason — a reader sees
REPRODUCED=5 DRIFTED=27 UNREACHABLE=15 BYTE_BACKED=32 and knows 5 are digest-bound, 42 are
attestation-only. Calibration: acceptable as a disclosed tradeoff; the probative weight of C2=PASS
rests on REPRODUCED plus the lane's fetch-record provenance, not on the counter alone. The boundary
legs (600 s inclusive, header-only empty, CONSISTENT recipe check) all behave as frozen.

No tool installs were needed (pacman paused; nothing installed).

VERDICT: attacked the C2 controls' probative value — spacing leg (599 rejects / 600 accepts UNREACHABLE),
EMPTY-header-only FAIL, JUNK non-recipe .txt FAILs CONSISTENT, and the disclosed 5+27 do-nothing PASSES;
frozen counter survived exactly as specified.

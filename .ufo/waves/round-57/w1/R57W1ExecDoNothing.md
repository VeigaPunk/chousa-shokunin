# R57-W1 · R57W1ExecDoNothing — R57-C2 do-nothing control (build + attack)

seat: `R57W1ExecDoNothing` · wave 57/1 · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
frozen counter under attack: `corpus/evidence/round57/c2-count.py` (blob `b1895cd9`, identical at
`c2f914c` and at HEAD — `git rev-parse c2f914c:…/c2-count.py HEAD:…/c2-count.py` → same sha; worktree
`git diff HEAD -- corpus/evidence/round57/c2-count.py` empty). Never edited.

## Task

Build the round's do-nothing control for R57-C2 — a lane state that skips the claimed re-fetch work —
and confirm the frozen counter rejects it. Two variants required: (A) freeze commit + the 14 wrap-up
captures, no `refetch.tsv`; (B) same captures + a `refetch.tsv` holding ONLY the failure rows of the
current record. Both must FAIL.

## Result — the claim's do-nothing bar SURVIVES

Both required variants FAIL with `VERDICTS=0/47`, exit 1. No do-nothing state I could build reaches
`C2=PASS`. The full sweep (all fixtures are scratch clones of the lane; frozen counter byte-identical in
each; `git rev-parse --show-toplevel` asserted == fixture dir before every run):

```
A    exit=1  SET=47 VERDICTS=0/47  REPRODUCED=0  DRIFTED=0  UNREACHABLE=0 BYTE_BACKED=0  CONSISTENT=0/0  FLAGGED=0/0  C2=FAIL
B    exit=1  SET=47 VERDICTS=0/47  REPRODUCED=0  DRIFTED=0  UNREACHABLE=0 BYTE_BACKED=0  CONSISTENT=0/0  FLAGGED=0/0  C2=FAIL
```

- **Variant A** (`laneA`: clone @ `c2f914c` + the 14 capture files, no `refetch.tsv`):
  `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL`, exit 1.
  Per-triple (`--verbose`): 47 `CAPTURE` lines, 37 `MISSING` + 10 `MISSING capture not the last
  successful attempt's bytes`. No verdict is computable without a fetch record.
- **Variant B** (`laneB`: same captures + a `refetch.tsv` with only the 15 failure rows of the live
  record, snapshot sha256 `d5c5413d402ab5b30f89047baa02305b2b638aef344479eda32cfa58103ee98c`, 109 rows):
  `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL`, exit 1.
  Failure rows only ever produce `UNREACHABLE`, and only where no capture file exists (see variant C).

## Spec defect found (reported, not patched — claims are frozen) + one self-correction

1. **The spec's own command cannot work.** The task says the 14 wrap-up captures were "committed at
   `6656f077`" and to read them with `git show 6656f077:corpus/captures/<name>`. But at that base
   commit `corpus/captures/` **does not exist**: `git ls-tree -r --name-only 6656f077 -- corpus/captures | wc -l`
   → `0`, and all 14 `git show 6656f077:corpus/captures/<name>` lookups fail (`ABSENT_AT_BASE` for all 14).
   The 14 files live in commit **`b022b13`** ("hyaku run9 wrap-up: remaining round-57 captures",
   2026-10-27 04:47:39). I used `b022b13` and, to remove any hand-assembly doubt, also ran the **real**
   pre-refetch lane tree at `b022b13` (`laneB0`): `VERDICTS=0/47 … C2=FAIL`, exit 1, and its 47
   per-triple verdict lines are **byte-identical** to variant A's (`diff` clean). The do-nothing bar
   therefore holds for both readings of the spec.
2. *(Self-correction.)* My first hand-extraction loop omitted `c7266931a1731db3ff6ae77d.raw` — I
   transcribed that 24-hex key one character short. The lane file is **correctly** named: a python check
   over all 14 stems finds **no** stem whose length differs from 24, and `key(S110 url)` equals the
   on-disk stem exactly. The omission was caught by re-extracting the tree wholesale with
   `git archive b022b13 corpus/captures | tar -x -C .` (14 files, names taken from git, not from my
   typing); every number in this report comes from that wholesale extraction. No lane defect.

## Supplementary calibration sweep (all FAIL except the deliberate forge)

| var | state | summary | exit |
|---|---|---|---|
| C | A's record (failure rows only) but **no** capture files | `VERDICTS=1/47 UNREACHABLE=1` (`S105`, 3 failed attempts 08:06:12→08:30:12 = 1440 s ≥ 600) | 1 |
| D | real lane tree @ `fd95724` (pre-wrap-up) | `VERDICTS=0/47 … C2=FAIL` | 1 |
| E | 14 wrap-up bytes + **full** live record | `VERDICTS=9/47 REPRODUCED=0 DRIFTED=9 BYTE_BACKED=9 CONSISTENT=0/9 FLAGGED=0/9` | 1 |
| F | full live record, no captures | `VERDICTS=1/47 UNREACHABLE=1` | 1 |
| H | forge G minus the self-written `FRESHNESS-FLAG` lines | `VERDICTS=47/47 REPRODUCED=5 … FLAGGED=0/42 C2=FAIL` | 1 |
| I | **stale bytes attested as a fresh fetch** (no network) | `VERDICTS=10/47 REPRODUCED=10 DRIFTED=0 BYTE_BACKED=10 C2=FAIL` | 1 |

### The sharpest finding: the `REPRODUCED >= 5` cryptographic floor does not attest freshness

Variant I is the strongest do-nothing I could build: take the 14 pre-existing wrap-up captures (committed
`b022b13`, 04:47 — **before** the L1's round-57 re-fetch commit `f9736a3`, 05:15), regenerate each `.txt`
with the frozen recipe, and self-attest them in `refetch.tsv` as a successful attempt. Result:
**`REPRODUCED=10`** — the counter binds the digest to the *pin*, and 10 of the 47 pins are already
satisfied by bytes that pre-date this round's fetch:

```
pins reproduced by PRE-EXISTING wrap-up bytes: S090 S102 S103 S105 S106 S109 S110 S112 S123 S127
count REPRODUCED obtainable with ZERO new bytes and ZERO network: 10
```

(The pin is the digest of the recipe `.txt`, not of the `.raw` — e.g. S105 pin `2197abe27dad…` is the
`.txt` digest of the wrap-up `.raw` `d36191c7…`.) So `REPRODUCED >= 5` is satisfiable by material that
was already in the lane before the claimed re-fetch. The claim nonetheless still FAILS here
(`VERDICTS=10/47 < 47`), so **the do-nothing state does not reach `C2=PASS`** — the bar holds on the
`VERDICTS=47/47` term, not on the digest term. For the live lane the wrap-up bytes are byte-identical to
the L1's round-57 refetch raws (`git rev-parse b022b13:<f> f9736a3:<f>` → SAME for all 14), i.e. this
round's re-fetch was content-redundant for those URLs.

### The claim's disclosed forge reproduces exactly — and is stronger than disclosed

Claim text: *"A forge with five genuine captures and 27 random-byte 'drifted' ones would pass."* I built it
(variant G) and it passes: `SET=47 VERDICTS=47/47 REPRODUCED=5 DRIFTED=42 BYTE_BACKED=47 CONSISTENT=47/47
FLAGGED=42/42 C2=PASS`, exit 0. Exact numbers differ from the disclosure (5 genuine + **42** random, not 27),
and the forge additionally needs the 42 self-written `- FRESHNESS-FLAG <id> <key> absent=m/m` lines — variant H
shows removing them flips it to `FLAGGED=0/42 C2=FAIL`.

**Stronger than disclosed (variant G2):** the forge passes with **zero bytes from the L1's re-fetch and zero
network** — the 5 "genuine" captures are harvested straight out of `b022b13` (pre-existing wrap-up bytes whose
recipe-`.txt` reproduces 10 of the 47 pins), the other 42 are `os.urandom(4096)` with recipe-consistent `.txt`,
and the record + flag lines are self-written:
`SET=47 VERDICTS=47/47 REPRODUCED=5 DRIFTED=42 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=42/42 C2=PASS`, exit 0.
This confirms the disclosure rather than contradicting it — the disclosure is *under*-stated on the
random-byte count and silent on the flag lines.

## Contrast — the live lane (read-only counter run, no lane write)

```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
exit=0
```
`DRIFTED` = S083 S087 S113 S114 S121, all `absent=0` (hence `need_flag=0`, `FLAGGED=0/0`); `UNREACHABLE` =
S105 (3 failed attempts). This is the state the L1 has moved to during this wave (dispatch snapshot was
38 REPRODUCED / 5 DRIFTED / 4 pending; the S100 S103 S105 S106 retries have since landed).

## Boundaries honoured

- Wrote only this file in the lane. `git diff --name-only HEAD` in the lane shows only
  `corpus/evidence/round57/refetch.tsv` + `.ufo/waves/round-57/w1.ready.partial`, both the **L1's** live
  edits (they pre-existed my first read); my runs were read-only.
- Frozen counters/controls never edited: `git diff --quiet HEAD --` → UNMODIFIED for `c2-count.py`,
  `c3-count.py`, `controls/build-c2-controls.py`. Mutating experiments ran in scratch clones only.
- No network fetch performed; only committed bytes under `corpus/captures` were read.
- Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecDoNothing/` — **deleted before yield** (`rm -rf`,
  verified absent). No tool was installed or upgraded this wave (none needed).

**VERDICT: the R57-C2 do-nothing control was built (variants A and B, both `VERDICTS=0/47 C2=FAIL` exit 1) and the claim's do-nothing bar SURVIVES — but the disclosed forge reproduces at `C2=PASS` (and stronger than disclosed: with zero network and zero bytes from this round's re-fetch), while the `REPRODUCED >= 5` digest floor is satisfiable by 10 pre-existing wrap-up bytes and does not by itself attest freshness.**

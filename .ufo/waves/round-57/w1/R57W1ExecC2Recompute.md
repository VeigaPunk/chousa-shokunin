# R57W1ExecC2Recompute — independent recompute of all 47 R57-C2 verdicts

seat R57W1ExecC2Recompute (leaf executor, chousa lane, round 57 w1), 2026-10-27. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` read-only except this report. Claim **R57-C2** (freshness) frozen at `c2f914c53201a8f8ee4fef823b82681051d55592`; counter `corpus/evidence/round57/c2-count.py` frozen (never edited — copied into scratch to mutate). Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecC2Recompute` (removed on exit, §6).

## 1. Method

Re-derived all 47 verdicts **without importing the frozen counter**: `scratch/recompute.py` written from the predicate in `corpus/evidence/round57/claims.md:24-49` — pinned set from `git show 6656f0770a1460d6ba73d9d2976f698a35311921:<spans.tsv>` over the 12 `corpus/evidence/**/spans.tsv` manifests; REPRODUCED/DRIFTED/UNREACHABLE per the predicate; CONSISTENT = committed `.txt` byte-equal to the campaign recipe applied to the committed `.raw`. Second, independent oracle: the **campaign's own** `quote-lint.py` (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint.py`, sha256 `e864a01f26ac92fda281b1b04eaeb6c47b7cd843726b012511b8d980eff7b958` — matches the digest the lane's recipe claims, verified) rather than the lane's copy of it.

## 2. Step 1 — the frozen counter's summary line

```
$ python3 .../corpus/evidence/round57/c2-count.py --verbose
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS   exit 0
```
Identical line and exit 0 against the **committed** tree (`git archive HEAD | tar -x` → scratch, `--root`), so the receipt reproduces from committed bytes alone, not working-tree state.

## 3. Steps 2–4 — per-triple table: my verdict vs the counter

**47 compared, 0 disagreements** (verdict, absent count, CONSISTENT flag, attempt/failure tally all matched). A first run of mine reported 47 disagreements — a column-index bug in my own table parser (`awk $1,$3,$4` over `CAPTURE <id> <key> pin=… <verdict> <note>` picked `pin=`); the corrected parse agrees on all 47. R = REPRODUCED, D = DRIFTED, ✓ = counter agrees with mine:

```
S082 R✓ | S083 D0/2✓ | S085 R✓ | S086 R✓ | S087 D0/2✓ | S088 R✓ | S089 R✓ | S090 R✓
S091 R✓ | S092 R✓ | S093 R✓ | S094 R✓ | S096 R✓ | S097 R✓ | S098 R✓ | S099 R✓
S100 R✓ | S101 R✓ | S102 R✓ | S103 R✓ | S104 R✓ | S105 UNREACHABLE✓ | S106 R✓ | S107 R✓
S108 R✓ | S109 R✓ | S110 R✓ | S111 R✓ | S112 R✓ | S113 D0/6✓ | S114 D0/9✓ | S115 R✓
S116 R✓ | S117 R✓ | S118 R✓ | S119 R✓ | S120 R✓ | S121 D0/6✓ | S122 R✓ | S123 R✓
S124 R✓ | S125 R✓ | S126 R✓ | S127 R✓ | S128 R✓ | S129 R✓ | S130 R✓
```

**CONSISTENT 46/46 under both oracles** (`CAMPAIGN-RECIPE CONSISTENT: 46/46 consistent, 0 bad, 1 no-capture` — the 1 is S105, no bytes). **Pin binding recomputed:** 35 of 47 pins bind via the `.txt` digest, 6 via the `.raw` digest (S082, S100, S101, S115, S122, S124), 6 unbound (5 DRIFTED + S105) — all 41 REPRODUCED are digest-bound.

**DRIFTED absent counts re-derived by hand** (each quote located in the defined text form): S083 0/2, S087 0/2, S113 0/6, S114 0/9, S121 0/6 — every quote present, so no `FRESHNESS-FLAG` is required and `FLAGGED=0/0` is correct. Character: S083/S087/S121 are **stable** pages differing from the pin (site changed since); S113/S114 are **dynamic** — raw sha256 differs *between the two round-57 attempts* (`18201d55…`→`ba8dbc5a…`, `fe77ace1…`→`56c2f612…`), a stronger drift than a stale pin.

**≥600 s spacing** on the retry URLs: S100 08:05:22Z→08:29:33Z (1451 s), S103 (1441 s), S105 08:06:12Z→08:30:12Z (1440 s)→08:33:48Z (+216 s; first→last 1656 s), S106 (1437 s). The counter's `fails[-1]-fails[0] >= 600` (`c2-count.py:231`) is **equivalent** to the predicate's "two failed attempts ≥600 s apart" pairwise reading (max pairwise separation = max−min).

## 4. Falsification attacks (all on scratch copies)

**(a) Commit-restoration — decisive.** `git archive HEAD` → scratch, restore the byte deleted in `e0e73e0`:

```
$ git show b022b13:corpus/captures/e3ca8f4fdd15420b80096a75.raw > fx/corpus/captures/…
$ python3 c2-count.py --root fx
CAPTURE S105 … MISSING capture not the last successful attempt's bytes
SET=47 VERDICTS=46/47 … C2=FAIL   exit 1
```
Removing it again returns `UNREACHABLE … VERDICTS=47/47 C2=PASS`. **S105's verdict is decided by the presence of a file, and the file's presence is what breaks it.**

**(b) The deleted bytes regenerate the pin bit-exactly** — the orphan is the PDF whose recipe text form hashes to S105's pin:

```
$ git show b022b13:corpus/captures/e3ca8f4fdd15420b80096a75.raw | pdftotext -layout - - | sha256sum
2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e   ← == S105's pin
$ git show 6f3276b:corpus/captures/e3ca8f4fdd15420b80096a75.txt | sha256sum
2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e   ← == S105's pin
```
I checked all **41** of S105's round-50 manifest quotes against that text form: **absent = 0/41** — every pinned quote present. The URL was reachable and its content unchanged; only the round-57 attempt record is empty (3 × `curl_rc=28` with `http_code=200` — the server answered, the body transfer timed out). UNREACHABLE is an artefact of the record plus the deletion, not a surface fact. Both blobs remain recoverable from git history (`6f3276b` `.txt`, `b022b13` `.raw`).

**(c) Tamper test — the CONSISTENT leg binds.** Flipping 10 bytes of the committed S118 `.txt` in a scratch copy of HEAD → `REPRODUCED=40 DRIFTED=6 CONSISTENT=45/46 C2=FAIL`. Good.

**(d) Quote-splicing forgery — the counter's weakness.** Fixture with **5 genuine REPRODUCED** and **42 fabricated** captures (random bytes, recipe text embedding every pinned quote of its triple so `absent=0` → no FRESHNESS-FLAG needed), each with a successful `refetch.tsv` row:

```
SET=47 VERDICTS=47/47 REPRODUCED=5 DRIFTED=42 UNREACHABLE=0 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=0/0 C2=PASS   exit 0
```
**42 of 47 captures fabricated and the counter passes.** The claim *discloses* this in advance (`claims.md:58-60`: "A forge with five genuine captures and 27 random-byte 'drifted' ones would pass… the wave attacks it"), so it is not hidden — but my variant is stronger than the disclosed JUNK control, whose random bytes make `absent>0` and so *do* trip the flag leg (`FLAGGED=0/47`, FAIL); the disclosed weakness is only realizable if the forger also writes the flag lines, whereas the splicing variant needs no flags at all. `MIN_REPRODUCED = 5` is the only barrier, and it is a *count*, not a *set*. Live margin is large (41 ≫ 5). **No predicate change proposed** — calibration datum only.

## 5. Findings against the frozen claim (reported, not patched)

1. **R57-C2 survives.** 47/47 reproduce exactly; CONSISTENT 46/46 under two independent oracles; the tamper test confirms the CONSISTENT leg binds bytes; the counter reads only `refetch.tsv`/`corpus/captures`/the lesson file/manifests — never a gate or probe.
2. **S105's UNREACHABLE is a record artefact.** The lane's own history holds bytes that regenerate S105's pin exactly and contain all 41 of its pinned quotes; the verdict became UNREACHABLE only because the L1 removed the orphan bytes in `e0e73e0` (restoring them → 46/47 FAIL). Disclosed in that commit message and in `.ufo/waves/round-57/w1/R57W1ExecControlsReRun.md:89`. Reported because the freshness axis claims quote re-verification, and for S105 the lane's own bytes would have re-verified all 41 — that evidence now lives only in git history.
3. **`MIN_REPRODUCED = 5` is a weak floor** against the splicing forge of §4d; the disclosed JUNK control does not actually exhibit the hole (random bytes trip the flag leg).
4. **Latent, not triggered: divergent "defined text form" for OLE/zip raws.** The predicate defines the DRIFTED-absent form as `tools/capture-text.py` stdout, but the CONSISTENT leg compares the committed `.txt` against the *recipe* form. For S100 (OLE `.doc`) these differ: `capture-text.py` yields 842 readable chars (`中国知网他引频次查询方法说明…`) while the committed `.txt` is the 1 406 840-byte UTF-8-replacement blob. S100 is REPRODUCED (bound via the `.raw` digest) and has no round-50 manifest rows, so **no live effect** — but a future drifting OLE capture would check absence against the readable form and consistency against the blob.
5. **Verdict-stability caveat.** The counter reads the **working tree**; mid-wave the lane's `corpus/captures/` was in flux (uncommitted `.raw`/`.txt` rewrites for S111/S113/S114), so the receipt is reproducible from a commit only once those land. Confirmed reproducible from `HEAD` now (§2).

## 6. Boundaries, tooling, cleanup

Writes: **only this report**. No other lane file created or modified; the frozen counter, controls builder, claims file and every counter fixture untouched (mutations ran on scratch copies). Nothing written to the fleet root `/home/vgpnk/Projects/shokunin`, any sibling lane, or `/home/vgpnk/Projects/shokuknow` (read-only; `quote-lint.py` read only). **No network fetch** by this seat — every byte came from `corpus/captures/` or git history. No `git commit/add/stash/checkout/reset/push` and no mutating `jj` command anywhere. Scratch used with `TMPDIR=$PWD`, `PYTHONDONTWRITEBYTECODE=1`, and **deleted before yield** (`rm -rf -- $S`; absence confirmed). Tooling: **no installs or upgrades** — only `python3`, `git`, `xxd` and `pdftotext` (verified `26.08.0`, as the counter's env guard requires), all already present; no pacman transaction (host-wide pacman guard PAUSED).

## VERDICT

Independent recompute of all 47 R57-C2 verdicts from committed bytes: **0 disagreements** with the frozen counter (`SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0) — **the claim SURVIVES**; the attack found that **S105's UNREACHABLE is manufactured by deleting bytes that regenerate its pin exactly (restoring them flips the counter to 46/47 FAIL)** and that **a 5-genuine quote-splicing forgery also yields C2=PASS**, so C2's cryptographic floor is the REPRODUCED count alone (live margin 41≫5).

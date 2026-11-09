# R100ExecC1Repro — C1 reproduction + identity-rule probes

Falsify seat. Attack tree `$S/repo` = shared clone @ 6d4e8487 (tool under test: `tools/gate-records.py` in that clone).
Receipts in `.ufo/waves/round-100/w1/` (seat-prefixed). Fixture repos `fx/`, `fx2/`, `gt/` under my scratch
`/fast/scratch/hyaku/chousa-r100/R100ExecC1Repro/`; every fixture git call names `-C <D>`; each fixture's
`git rev-parse --show-toplevel` == its dir (asserted in-script); commits with `-c user.name=fixture
-c user.email=fixture@invalid`.

## (a) Frozen C1 counting command and before command — reproduced exactly

Command: `python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work ../w-cand`
(run in `$S/repo`; work dir under scratch). Tail + exit at
`R100ExecC1Repro-c1-candidate.txt`:

```
NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12
CHALLENGE_CONTROLS_R100=PASS
exit=0
```

Before command: same battery with `--tool ../base-gate.py --no-oracles`
(`base-gate.py` = `git show 929c784c…:tools/gate-records.py` from `$S/repo`) → tail + exit at
`R100ExecC1Repro-c1-base.txt`:

```
NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=3/11 REVPOS=3/3 PROD=4/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=0/0
CHALLENGE_CONTROLS_R100=FAIL
exit=1
```

Comparison: identical to `corpus/evidence/round100/before/c1-base.txt` line 51 (`REV=3/11 PROD=4/6 … FAIL`)
and `…/before/c1-candidate.txt` lines 51/63 (`REV=3/11` resp. `REV=11/11 PROD=6/6 … PASS`, same
`HARM_SAME=27/27 BASE_REV_ADMITTED=8/11`, same oracle lines `o1..o12 … PASS`). Artifact: the battery's
three meaningful numbers (`NEG, MARK, BOUND, NORM, POS, REV, REVPOS, PROD, HARM_SAME, BASE_REV_ADMITTED,
ORACLES_REJECTED`) are stale-claim-free — claims.md's predicate line is reproduced character-for-character.

## (b) Identity-rule probes (28 rev records of my own, committed S230 capture vs variants)

Base facts: S230 capture `corpus/captures/b5b8d050eea0c638e95ba674.txt` (184 bytes, 23 words; its `.raw`
sibling 20493 bytes / 620 words); tree blob `66f24cb2…` for `.txt`, `d3f6fe68…` for `.raw`.
All probes verified with `--root $S/repo --repo <fixture>`, registry id S230, quote = first 3-word line as
the battery's `rev_record` builds it. Full commands + verbatim record + observed GATE_RECORD line and exit
code per probe are in `R100ExecC1Repro-revprobes-phase1.txt` (12 probes), `…-phase2.txt` (16 probes),
`…-crossrev.txt` (8 probes), `…-universal.txt` and `…-rawonly.txt`.

### Refused (FAIL CHALLENGE) — identity holds beyond battery spellings

| # | Record (rev, path) | Observed | Named limit covering it |
|---|---|---|---|
| 01 | 3089f25f…, `corpus/captures/b5b8….txt` | `FAIL CHALLENGE` rc=1 | claim sentence (exact) |
| 02 | idem, `./corpus/captures/b5b8….txt` | `FAIL CHALLENGE` rc=1 | sentence ("whatever the path's spelling") |
| 08 | idem, `./corpus/../corpus/captures/b5b8….txt` | `FAIL CHALLENGE` rc=1 | sentence (F-1 class) |
| 13 | ee8aa903…, same capture path, capture bytes CRLF'd (one-byte classes differ, but the blob IS the capture entry's bytes) | `FAIL CHALLENGE` rc=1 | sentence; (b) does NOT apply — blob equals the entry of that rev, it merely differs from the older revision's bytes |
| p-r1-txt / p-r1-dot | at original rev, exact + `./` capture path | `FAIL CHALLENGE` rc=1 | sentence |
| p-r1-raw | at original rev, capture `.raw` path (620 words) | `FAIL CHALLENGE` rc=1 | sentence via sibling `.txt` |
| multi3 rec 1 | same as p-r1-txt, in a 3-record file | `FAIL CHALLENGE` | sentence + multi-record cache/pkg (no cross-rev cache bleed) |
| multi3 rec 3 | same as p-r1-raw, in same file | `FAIL CHALLENGE` | sentence |

### Refused but NOT by the identity rule — rev grammar gate (recorded, not counted)

| # | Record | Observed | Note |
|---|---|---|---|
| 03-abbrev-rev | rev=`3089f25` (7-hex abbrev) | `FAIL LINE,REV` rc=1 | `check()` gates rev on `HEX40_RE` (tools/gate-records.py:340); the battery assumes this refusal |
| 04-tag-rev | rev=`s230tag` | `FAIL LINE,REV` rc=1 | same gate |
| 05-rev-brace | rev=`<40hex>^{commit}` | `FAIL LINE,REV` rc=1 | same gate |
| 06-rev-tilde | rev=`<40hex>~0` | `FAIL LINE,REV` rc=1 | same gate |
| leadslash/backslash/4-dots | various | git rc=1 (unresolvable) | not grammar, git itself |

### Admitted (OK) — each covered by a named limit; none falsify the sentence

| # | Record | Observed | Named limit |
|---|---|---|---|
| 11-oldrev-copy | 00b4b6f3… (capture `.txt` moved away, capture set at that rev = `{.raw}`), path `sub/moved.txt` (byte-identical challenge) | `OK` rc=0 | (c) capture set read from record's rev: at this rev the blob is not a capture entry (the `.txt` entry is gone) — sentence predicts admission |
| 12-raw-at-rev2 / G / p-head-raw / C | raw path at revs where the sibling `.txt` is absent | `OK` rc=0 | (d) raw judged by own bytes (620 words > 200 → not challenge) |
| 14-trailnl-copy | challenge + 1 trailing `\n`, at `sub/tn.txt` at rev 834b5a29… | `OK` rc=0 | (b) byte identity — the copy's oid ≠ capture oid at that rev |
| D-rev7-crlfcopy / p-head-crlfcopy | CRLF rewrite of challenge at `sub/crlf.txt` | `OK` rc=0 | (b) same |
| F-rev8-upper / p-head-upper | byte-identical challenge at `CORPUS/CAPTURES/B5B8….TXT` | `OK` rc=0 | sentence's capture-entry clause: the entry path pattern is lowercase `corpus/captures/<24 lower-hex>.(txt\|raw)` (`CAPANY_RE`), so a case-variant path is not an entry (battery r7 class) |
| E-rev7-moved / i-movedat8 / p-head-moved / B | byte copy at `sub/moved.txt` at revs where the capture has been removed or CRLF'd | `OK` rc=0 | (c)+(b) as above |
| sp | trailing-space-appended copy at `sub/sp.txt` | `OK` rc=0 | (b) |
| j-tnnat8 / noncap | challenge page at `notes/noncap.txt`, bytes never committed under a capture path (fixture CPAGE-class) | `OK` rc=0 | "not a capture of that rev is not judged" clause of the sentence |
| symlink-quote | symlink `sub/link.txt → ../corpus/captures/b5b8….txt`, quote from capture text | `FAIL LINE` rc=1 | unrelated to identity; symlink blob (47 bytes, target path text) cannot carry a 3-token quote from it |

Two probes answered live and complicate nothing once run: (i) `.raw` whose sibling `.txt` is challenge while
the raw bytes are clean → shipped tool prints `FAIL CHALLENGE` (my clean-sibling v5, `…-crossrev.txt` v5);
and (ii) `.crc rename/deletion` cases are exactly limit (c)'s specified behavior (see table).

### Cross-rev memo on "capture set read from the record's rev or another?"

Probes `x-revA-cap / x-revA-blob / x-revB-cap / x-revB-blob` (fixture `gt/`: A: challenge at capture path,
B: benign at same path; byte copy at `notes/blob.txt` in both) → shipped tool: A refutes
(`FAIL CHALLENGE`), B admits (`OK`); the record's rev drives the capture set. The spec's "of that rev's
tree" wording is the shipped tool's real behavior — not a HEAD-tree or working-tree artifact.

## Findings against the C1 fence

1. **Battery blind spot vs the sentence's central phrase (confirms R100CriticClaims F-1 independently).**
   I built the one-line HEAD-tree stand-in (`capture_oids(repo, "HEAD")` in `rev_capture_text`).
   `R100ExecC1Repro-standin-head.txt` shows the frozen battery `--no-oracles` against it prints
   `NEG=7/7 … REV=11/11 REVPOS=3/3 PROD=6/6 … CHALLENGE_CONTROLS_R100=PASS` with exit 0 — the exact frozen
   PASS line minus `ORACLES_REJECTED` (which `--no-oracles` zeroes). The single-commit fixture
   (`fixture_repo` commits once) cannot distinguish "capture set at rev" from "capture set at HEAD".
   The shipped tool behaves per the sentence; the evidence offered for it does not.
   Smallest correction: second fixture commit (change capture bytes) + 3 cross-rev legs; cheapest possible —
   one fixture commit and three records as in `…-crossrev.txt` (A-refuse, B-admit, byte-copy refuse-at-A).
   This is the correct reading of the C1 kill rule: the counter did not enforce "that rev's tree".

2. **"Not judged" clause has no admitted challenge-shaped non-capture leg (confirms F-2).**
   My `notes/noncap.txt` record (`R100ExecC1Repro-universal.txt`): frozen tool `OK` (per the clause);
   a "judge every rev blob" stand-in (`is_challenge(blob)` directly) prints `FAIL CHALLENGE` rc=1.
   Under the frozen battery that universal stand-in FAILS (`REV=9/11 REVPOS=2/3 PROD=5/6 … FAIL`, exit 1,
   receipt `R100ExecC1Repro-universal.txt` tail) — but only because `.raw`-sibling and NOTE legs trip it
   for unrelated reasons (r5/r6/prod-rev-raw, q3); the one quadrant that isolates "challenge-shaped,
   non-capture, must be admitted" is untested. One leg kills the whole family; it currently doesn't exist.

3. **Claim's own negative facts all held (in both directions).** Every admission above lands inside a named
   limit (a–d) or the sentence's explicit "not a capture is not judged" clause; no admission fell outside
   every named limit. Two sibling variants the spec asked about (CRLF at the same capture path;
   trailing-newline copy) behave exactly per (b) and its mirror; `x-revA/B` shows no read-from-other-rev
   behavior. Rev-spelling variants are refused by grammar (`HEX40_RE`), never admitted — a stronger stance
   than the battery's 8/11 base-admitted count suggests.

Net: the C1 sentence's wording is true of the tool; its numbers reproduce. The counter cannot see the two
failure modes above because of fixture/battery shape — noting both is the falsification content of this seat.
C2 n/a (out of scope for R100ExecC1Repro).

VERDICT: R100ExecC1Repro C1 fired — a HEAD-tree tool that violates the "that rev's tree" clause prints the frozen battery PASS and the "not judged" clause is untested for challenge-shaped non-capture blobs, so the predicate's numbers cannot certify the sentence as written.

# Round 79 frozen claims — the subject copy stops being a textual derivative; the self-assessment counter validates its own repairs

Frozen 2026-11-04, before any seat scored anything. Base revision
`ee70e6df19fe43b1b384166cf5d360c3b99dafe2` (round-78 lane tip). Pre-freeze instruments, controls
and the digest-bearing repairs: `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`. Two claims, distinct axes, each causally separable: C1 changes the outer
battery's copy mechanism and needs only those bytes; C2 changes one counter and three
append-only repair lines.

Instrument digests at the controls commit (`sha256sum`, full):

| instrument | sha256 |
|---|---|
| `corpus/evidence/round79/matrix-battery-v6.py` | `bb91406e9130d9a1960d99226c69380435fc933385db79e0e6ea6b5542a61e1d` |
| `corpus/evidence/round79/forge-battery.py` | `5761edc5c012321119427824c6e21d1d9123713d0a39e485be84ebbcad4fc936` |
| `corpus/evidence/round79/derivative-check.py` | `af6fbe722c92096afcc5c3c30d0d8e276be2f3dbd265a2bca0df3a0e35397bc1` |
| `corpus/evidence/round79/selfcheck-v2.py` | `b99ccee5b20bb29c2e0ab83e6db39ba038b5ab501c1e7e1630054a5f88ffeed2` |
| `corpus/evidence/round79/selfcheck-control.py` | `00cf811a686e885d7c426c0b6d9ad4c17308e42cb3d9d937d6f200deb9f4499d` |
| `corpus/evidence/round79/forgers/a9-v6-wrapper-normalizer.py` | `851222ed6fff9c83c18fa9a54974ca4db3df99f166f3385cef1d760be6b306c5` |
| `corpus/evidence/round79/forgers/a8-v5-salt-normalizer.py` | `65f590afaa6cf88ff40807ba9f61cd5d661d6bfe98a792f2dd5d965d6373c953` |
| `corpus/evidence/round78/matrix-battery-v5.py` (the subject C1 supersedes) | `5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0` |
| `corpus/evidence/round78/selfcheck.py` (the counter C2 supersedes) | `f5acdd825ab7dcafa1385ad2b9a6c22df848c4e856947746cd006c22837bf9af` |

## C1 — operability (lowest scored non-retired axis; the historical numeric 3/10 is held)

**Target axis:** operability — a runnable artifact whose stated outcome a reader can
re-derive. The round changes the *outer battery's copy mechanism*, not the number the lane
reports. Sourced on S196.

**Target sentence (the event the kill rule names):** the round-78 battery's subject copy is
a textual derivative of a committed file — one four-line normalizer deletes the `_r78<hex>`
salt family and recovers every subject byte-for-byte — and the round-79 battery's copy is
not: no 40-byte window of a copy occurs in its committed source, while the legitimate matrix
is still accepted and one text-level normalizer per salt family is refused.

**Predicate (frozen sentence, identical to the instrument's docstring and the receipt label):**

> `python3 -B corpus/evidence/round79/forge-battery.py --battery corpus/evidence/round79/matrix-battery-v6.py --work DIR`
> exits 0 and prints exactly `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`.

`handled` counts the six forgeries that are REFUSED (battery exits non-zero, receipt intact,
last `BATTERY=` line FAIL) or DETECTED (the battery's own `RECEIPT_LINES` trailer does not
match the receipt). Four are the round-77/78 channels (trailing salt strip, parent cmdline,
printed order digest, detached append); two are one text-level normalizer per salt family —
`a8` for the round-78 `_r78<hex>` family and `a9` for the round-79 wrapper family. The
positive control is the lane's legitimate matrix `corpus/evidence/round76/loader-matrix-v3.py`,
which must still be ACCEPTED.

**Supporting measurement (not the predicate, one command):**

> `python3 -B corpus/evidence/round79/derivative-check.py --battery BATTERY`
> prints `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096` exit 1 for v5 and
> `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` exit 0 for v6.

**Before (measured at base `ee70e6df`, receipts committed with the controls):**
`controls/forge-battery-before-v5.txt` — `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1`,
exit 1, with `a8-v5-salt-normalizer … verdict=FORGED` and the other five REFUSED/DETECTED;
`controls/derivative-before-v5.txt` — `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096`, exit 1.

**After (measured at the controls commit, before the freeze):**
`controls/forge-battery-after-v6.txt` — `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`,
exit 0; `controls/derivative-after-v6.txt` — `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23`, exit 0.

**Kill rule:** C1 fails if the after receipt's predicate line differs, if the positive control
is MISS, if any forger is FORGED, or if any copy shares a 40-byte window with its committed
source. A structure-identity forger (unmarshal the payload and canonicalise the fresh
identifier table) is a *different* channel: re-emission preserves behaviour, so such a
normalizer recovers the module's structure. That is a recorded limit measured by the wave,
not a falsification of this claim's sentence, which is about the textual channel.

**Do-nothing control:** at the base the only battery on disk is v5, whose receipt is
`handled=5/6` at exit 1 (the sixth forger, `a8`, is FORGED), and its copies are 13/13 textual
derivatives. A round that does nothing cannot reach the target.

## C2 — calibration (sourced on S197)

**Target axis:** calibration — the lane's self-assessment read against observed repo state.
The predicate counts unresolved classes; it is not an assertion.

**Target sentence:** round 78's counter accepts presence-only repair lines and audits only
the newest `## Round-<n> addition` block, so a hollow mirror and a newer block each reach
PASS with the defects still present; the successor validates every repair line against the
bytes it names (digest) and audits every block, so neither false-green survives.

**Predicate (frozen sentence, identical to the instrument's docstring and the receipt label):**

> `python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .`
> exits 0 and prints exactly `SELFCHECK2=PASS unresolved=0/3`.

The three classes are the round-77 spot-check's routed defects 1, 3 and 4, carried by round
78: the `SKILL.md` gate-registry row whose cell count does not match its header (row 168), the
`QUALITY.md` criterion whose backticked pointer resolves to no committed path (116, plus 102
and 103 which the wider audit also resolves), and the `## Mistakes` row of
`corpus/lessons/round-77.md` stranded below `## Boundaries` (line 73).

**Before (measured at base `ee70e6df`):** `controls/selfcheck2-before.txt` —
`SELFCHECK2=FAIL unresolved=3/3`, exit 1, one unresolved finding per class; the predecessor on
the same bytes prints `SELFCHECK=PASS unresolved=0/3`, exit 0
(`controls/selfcheck-v1-before.txt`).

**Controls (measured before the freeze, `controls/selfcheck-control-before.txt`):**
`CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2` — the hollow mirror and the newer
block each reach `SELFCHECK=PASS unresolved=0/3` exit 0 on the predecessor and each is refused
by the successor (`SELFCHECK2=FAIL unresolved=3/3` exit 1).

**After (measured at the landing):** `controls/selfcheck2-after.txt` —
`SELFCHECK2=PASS unresolved=0/3`, exit 0, with three append-only digest-bearing repair lines
(`correction: SKILL.md:168 cells=7 digest=…`, a criterion carrying
`supersedes: 116 digest=…`, `erratum: round-77.md:73 digest=…`).

**Kill rule:** C2 fails if the after receipt's predicate line differs, if a hollow repair line
(right words, wrong digest) resolves any class, or if a newer `## Round-<n> addition` block
hides an earlier criterion from the audit.

**Do-nothing control:** without the successor counter and the digest-bearing repairs the same
bytes print `SELFCHECK2=FAIL unresolved=3/3` at exit 1, and the predecessor prints PASS on the
hollow mirror — a do-nothing round cannot reach the target.

## Shared boundaries

No network, no package adoption, no sibling-lane or fleet-repo write other than the round
report and L0 appends, no host question presumed answered. Frozen instruments and receipts are
never amended after a seat scores them; a post-freeze finding is reported as a limit, never as
a repaired predicate. Seats are author-lane evidence: the non-author closure still rules.

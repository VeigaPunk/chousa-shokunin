# RevC3RefBind — C3 cross-reference bindings, staged-id purge, ALLOWED_IDS width

Seat: wave 2 falsifier, round 46. Target bytes: lane commit `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`
(extracted with `git archive` to `/tmp`). Frozen claims read first; no predicate, counter target or kill
rule changed. Entry digests at `d09fc8e7`:
```
7bffb9d20f5bf149c0e408810cf6fc0b4a1346096b05fffef130e9bc063e71ae  corpus/knowledge/evidence-pool-versioning-r39.md
9ab4268431ea602b865dc3db60c8429334809987495a9e3d8f5b2651c58a4f26  corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md
```
Counter: `234e2272e8e21e82ed92d7565b4b2e48ca9448a1969687fc002c0de49102f3c5`, byte-identical at the new HEAD
(F4), so every mutation below applies to both.

## Assignment answers

**A1/A2 — the S079 and S081 sentences name the right documents.** Base entry line 23 (tokens at chars
4704/4797): "RFC 7089 (`S079`) makes an archived state addressable by date, and the NDL note on WARP's URL
renewal (`S081`) shows a capture timestamp embedded in the URL". Amendment line 21 repeats it (chars
3982/4075); amendment line 29 restates the mapping (chars 6223/6266). Against the registry:
`SOURCES.md:89` = "RFC 7089 … Memento" (`S079`), `SOURCES.md:91` = "NDL current-awareness E2867, WARP URL
renewal" (`S081`), whose key is exactly the timestamp-in-URL fact claimed. **Correct by document**; no entry
names S079 or S081 for any other document.

**A3 — no staged id survives.** `\bS<id>\b` counts over both committed entries:
`S120:0 S121:0 S122:0 S127:0 S128:0 S071:0 S095:0`; `PRISMA-S`: 0 in each; no `round N's \`S###\``
references. Only S079, S081, S082, S084, S085–S089 occur. The amendment's `S082` is re-bound to the lane's
held row (`evidence-archive-field-policy-r41.md`, row `S082` = AVeriTeC README, `SOURCES.md:92`), not the
staged PRISMA-S package row (`search-log-fields-r36.md:4`: `source: S082 … Table 1 (PRISMA-S checklist)`).
**Purged in prose — but not certifiable by the counter (F2).**

**A4 — the whitelist is wider than the entries need.** Need = {S079,S081,S082,S084,S085–S089} (9);
`ALLOWED_IDS` = S079–S089 (11). Admitted, cited by neither entry: **`S080`** (WARP FAQ, collection cadence;
no citation and no wave-1 recommendation — the id no entry should cite) and **`S083`** (AVeriTeC paper;
uncited, only recommended at `ConnectSiblings.md:113`, so unused rather than improper). Worse: the slot is
document-blind — `S082` is admitted, so the staged PRISMA-S meaning passes (F2).

## Findings

### F1 — HIGH (measurement, not claim failure): `REF_BOUND=2/2` tests token co-occurrence, not binding
`c3-count.py:138-146` sets a hit if **any** sentence of **either** entry contains the sid and the token, in
any order or polarity. Mutants on the committed copy, `--lane-only`:
- `m1` base line 23 documents **swapped** ("WARP (`S079`) … RFC 7089's URL renewal (`S081`)") → `REF_BOUND=2/2 C3=PASS`
- `m5` amendment binds `S079` to **PRISMA-S**, base untouched → `REF_BOUND=2/2 C3=PASS`
- `m7` base `S079` **deleted**, RFC 7089 re-cited as `S089` (wrong document) → `REF_BOUND=2/2 C3=PASS`
- `m8` both substantive sentences renamed ("the Memento extension (`S079`)", "the archive's URL renewal
  (`S081`)"), leaving document tokens only in amendment line 29 → `REF_BOUND=2/2 C3=PASS`

`m8` proves the leg is satisfied entirely by the "Staged material corrected on adoption" bookkeeping
sentence — a sentence that asserts the mapping without citing the document. The predicate says the two
cross-references "bind by document"; the counter cannot distinguish a correct binding from a swap, a
deletion or a negation. So `REF_BOUND=2/2` is not evidence for the predicate. On the committed bytes the
predicate is nonetheless **true** (A1/A2, re-derived against SOURCES lines 89/91), so C3 is not refuted;
the leg is non-evidentiary, and any verdict citing `REF_BOUND=2/2` as proof overstates it.
`ReviewOpenS087.md:112` treated this very test as the "re-bind by document" check; it does not perform one.

### F2 — MEDIUM: `ALLOWED_IDS` cannot exclude the staged PRISMA-S binding of `S082`
- `m2` base cites `S083` → `REF_ID_UNBOUND=0 C3=PASS`; `m3` base cites `S080` → `0 PASS`
- `m4` base cites `S090` → `REF_ID_UNBOUND=1 C3=FAIL` (out-of-band ids are caught)
- `m6` amendment: "PRISMA-S (`S082`) is the staged search-reporting binding" → `REF_ID_UNBOUND=0 C3=PASS`

The `unb` check is "every id lies in S079–S089", not "every id names a document the entry may cite".
A per-entry allowance (base {S079,S081,S085–S087}; amendment {S079,S081,S082,S084,S088,S089}) kills
m2, m3 and m6 at zero cost.

### F3 — MEDIUM (content, persists at HEAD): the S084 figure is attached to the wrong set
Committed amendment line 26: "…(row `S084`) counts 5,959 of 7,572 real-source answers carrying a
web.archive.org link and **1,582** giving no archive field at all." The row says:
- `evidence-snapshot-coverage-r40.md:12`: "1,582 answers name a `source_url` and carry no archive field at
  all, **1,491 of them a real source** rather than `Metadata`"
- `r40.md:21`: "Of the 7,572 answers that name a real source … 5,959 (78.7%) carry a web.archive.org link"
- `SOURCES.md:94` (S084): "…5,959 carry a web.archive.org link and **1,491** carry no archive field"

Arithmetic excludes the quoted pair: 7,572 − 5,959 = 1,613, so "5,959 … and 1,582" does not partition the
set. `CritC3Inference.md:72,89` already recommended "1,491 of 7,572"; the landing did not apply it. New as an
unapplied-at-landing defect, not as a correction.

### F4 — LOW (record integrity): `d09fc8e7` is no longer HEAD
At 07:37:22 −0300, mid-wave, the lane committed `3807537db7e7` "round-46: wave-2 corrections (… entry
narrowings …)". `git diff --stat d09fc8e7 3807537` over the two entries: 5 insertions/5 deletions (base
4+/2-, amendment 6). `c3-count.py` is identical across the two, and both trees print the full PASS (F1/F2/F3
properties persist at HEAD). Verdict language must name the sha scored: `d09fc8e7` is the round-46 landing;
`3807537` is a later correction commit.

## Verdict on the assignment

- Bindings: **correct in the committed bytes** (A1/A2); the certifying counter is document-blind (F1).
- Staged ids: **none survive** (A3); the counter could not certify absence (F2).
- Whitelist: **wider than needed** — `S080` (never cited, never recommended) and `S083` (uncited) admitted,
  and `S082`'s slot admits the staged PRISMA-S meaning (F2).
- C3 predicate: **holds on the committed bytes** by manual re-derivation; F1/F2 cap what the counter proves,
  F3 is a content defect inside the entry the depth claim is built on.

## Residual risk / verification gaps

- A1/A2 verify the document binding against `SOURCES.md` rows, not the rows' own span fidelity (other seats).
- My train.json recount matches 3,068 records / 8,479 answers / 5,959 web.archive links but gives 7,959
  real-source answers under "not None/Metadata" and 7,546 under "starts with http"; I did not reconstruct the
  exact 7,572 predicate, so F3 rests on the row's own `1,582 all / 1,491 real-source` split and the 1,613
  complement, not on my recount.
- Mutants ran `--lane-only` (span rows untouched), so default-mode `CAPTURE_BOUND=11/11` is implied, not
  separately run per mutant.
- HEAD moved during this seat; F4's sha pair is the anchor if the lane advances again.

## Commands run (verbatim, decisive output)
```
$ python3 corpus/evidence/round46/c3-count.py        # d09fc8e7 tree
ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS                 EXIT=0
$ python3 corpus/evidence/round46/c3-count.py --lane-only
… CAPTURE_BOUND=skipped REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS            EXIT=0
$ for n in m1 m2 m3 m4 m5 m6 m7 m8; do python3 /tmp/…-$n/…/c3-count.py --lane-only; done
m1 2/2 PASS | m2 0 PASS | m3 0 PASS | m4 UNBOUND=1 FAIL | m5 2/2 PASS | m6 0 PASS | m7 2/2 PASS | m8 2/2 PASS
$ grep -n "^| S079 \|^| S080 \|^| S081 \|^| S083 " corpus/SOURCES.md
89:| S079 | RFC 7089, HTTP Extension for Time-Based Access to Resource States — Memento
90:| S080 | NDL Web Archiving Project (WARP) FAQ — https://warp.ndl.go.jp/en/info/qanda
91:| S081 | NDL current-awareness E2867, WARP URL renewal — https://current.ndl.go.jp/e2867
93:| S083 | AVeriTeC corpus paper, Schlichtkrull et al., arXiv:2305.13117v3 HTML
$ git diff --quiet d09fc8e7 3807537 -- corpus/evidence/round46/c3-count.py && echo IDENTICAL
IDENTICAL
```
Tooling: nothing installed or upgraded; no network; no lane production file, git or jj state written.
Scratch `/tmp/chousa-r46w2-RevC3RefBind*` removed.

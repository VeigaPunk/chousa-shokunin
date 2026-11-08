# R90ScoutRegistry — registry reconnaissance at `9bad12011187d114ba2c4588c5df08a21ab28145`

Seat: `R90ScoutRegistry` (scout, leaf). Scope: (a) S220's row and capture, (b) the `S219`/`S220` id
reservation, (c) an independent C3 tally count, (d) the fleet census. Read-only: no production
edit, no lane/fleet git mutation, no commit, no network beyond C3's own selftest.

## Ground and method

| item | value |
|---|---|
| attack revision | `9bad12011187d114ba2c4588c5df08a21ab28145` (freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a` + receipts) |
| base | `f54a45ed197dd475af50d82e43a22df3d2e99782` (218 registry rows) |
| clone used | `git clone --shared <lane> $S/repo` + `git -C $S/repo checkout 9bad1201…` |
| scratch | `/fast/scratch/hyaku/chousa-r90/R90ScoutRegistry/` (`repo/`, `tree-s219/`, `work/`), removed at yield |
| receipts (this seat) | `.ufo/waves/round-90/w1/R90ScoutRegistry/receipts/{a1,a2,a3,b1,c1,d1}-*.txt` |

---

## (a) S220 — the row, the capture, the quote, the hash

**Row.** `corpus/SOURCES.md` line 232 at `9bad1201`:

> `| S220 | GNU grep(1) manual page, Matching Control, `-x`/`--line-regexp` — https://man7.org/linux/man-pages/man1/grep.1.html | docs | A | GNU grep's whole-line match semantics (`-x`), for a receipt field checked as one token; not regex anchoring and not this lane's driver | Matching Control, `-x , --line-regexp` paragraph; man7.org page read 2026-11-08, capture key e6ec761219e8044b0e9e067a | `-x` selects only matches that exactly match the whole line, so a required receipt value must equal a whole token rather than occur inside a longer one | mined | 2026-11-08 | 180d | corpus/evidence/round90/claims.md |`

Its `used-by` cell names `corpus/evidence/round90/claims.md`, which exists at `9bad1201`
(`git cat-file -e 9bad1201:corpus/evidence/round90/claims.md` → present).

**Registry size.** `grep -c '^| S[0-9]\{3\} ' corpus/SOURCES.md`:

| revision | rows |
|---|---|
| base `f54a45ed` | **218** |
| freeze `8d9893b4` | **219** |
| attack `9bad1201` | **219** |
| master HEAD `aa7d4223` | 219 (identical bytes; the capture commit adds no row) |

`git diff f54a45ed 8d9893b4 -- corpus/SOURCES.md` is **one added line** — the S220 row — with no other
cell touched. 219 unique ids, `S001`–`S218` plus `S220`; **`S219` is absent** (`grep -c '^| S219 '` → 0),
which is the reservation of (b). So the claimed "218 → 219 with that one mined row and its `used-by` cell"
holds exactly.

**Capture.** `corpus/captures/e6ec761219e8044b0e9e067a.{txt,raw}`. The key is derivable:
`sha256("https://man7.org/linux/man-pages/man1/grep.1.html")[:24]` = `e6ec761219e8044b0e9e067a` — the same
key `curation-r89.py:94` would look up.

**Quote located.** After whitespace normalisation of the whole `.txt` the sentence
`Select only those matches that exactly match the whole line.` is present (normalised offset 3134) and
the same holds for the `.raw` after tag-stripping. The sentence is soft-wrapped in **both** captures:

| capture | line numbers of the quote |
|---|---|
| `e6ec761219e8044b0e9e067a.txt` | **166–167** (line 166 begins ` Select only those matches that exactly match the whole`, line 167 carries ` line. For a regular expression pattern, …`) |
| `e6ec761219e8044b0e9e067a.raw` | **152–153** (line 152 begins the same text, line 153 carries ` line.`) |

The row's own anchor — the `-x , --line-regexp` option label — is at `.txt` line **165** / `.raw` line
**151**, immediately above the quote, so the anchor and the quote are adjacent in the capture.

**Hashes.** `sha256sum` of the two files:
`.txt` = `5a5e69c56413ba682b1609cba2baacafb393ff6821d5b752938efc390fd12823`,
`.raw` = `d6f07a7f75c6275f6986df2501d355ebd22fa1475ce50dc6039f1fb028d6a3c2`.
Both are byte-identical to the `S220` refetch row in `corpus/evidence/round57/refetch.tsv` line 188
(`raw_sha256` / `txt_sha256` columns). **Match confirmed.**

**Refetch row.** `corpus/evidence/round57/refetch.tsv:188`:

```
S220  https://man7.org/linux/man-pages/man1/grep.1.html  e6ec761219e8044b0e9e067a  1  2026-11-08T09:52:31Z  0  200  d6f07a7f…  5a5e69c5…
```

`http_code` = **200**, `curl_rc` = **0**. `fetched_utc` = `2026-11-08T09:52:31Z`; the capture's mtime is
`2026-11-08 06:52:31.363632228 -0300` = **`09:52:31Z`** — the fetched_utc **is** the access instant
(second precision). Note line 187 is the *same key with the same hashes* under id `S219`
(`fetched_utc 2026-11-08T09:44:57Z`) — the earlier, id-reserved attempt; the committed bytes are the
later `S220` access and are identical in content.

**Word count.** The brief says the quote is 11 words. Measured: whitespace-delimited tokens of
`Select only those matches that exactly match the whole line.` = **10**; it is 11 only if the
sentence-final `.` is counted as its own token (`line` + `.`). The quote text itself is byte-exact
either way — the discrepancy is in the counting convention, not in the source. Flagging it as an
observed deviation from the expected value, not a defect of the capture.

**One further observation (not a kill-rule hit).** The capture bytes are **not in the tree at
`9bad1201`**: `git cat-file -e 9bad1201:corpus/captures/e6ec761219e8044b0e9e067a.txt` → *does not exist*.
They were committed one commit later, in `aa7d4223` ("round-90: S220 source capture"), whose parent is
`9bad1201` (`git merge-base --is-ancestor 9bad1201 aa7d4223` → yes). So at the attacked revision the
S220 row cites a capture key whose bytes are not yet committed in-tree; they are in the tree at master
HEAD, hash-verified against the refetch ledger. The row's `used-by` cell points at a file that *is*
committed at `9bad1201`, so the registry row itself is not dangling.

Receipts: `receipts/a1-s220-row.txt`, `receipts/a2-capture-quote.txt`, `receipts/a3-located-lines.txt`.

---

## (b) The id: why `S220` and not `S219` — collision re-derived

`S219` is reserved to the round-89 / round-90 control fixtures' **mirror row**, which is written into a
scratch copy of the registry as a *disposal* row:

```
curation-r89-controls.py:41   S219_ROW = ("| S219 | mirror row (own-work) — corpus/SOURCES.md | own-work | A | mirror | … | supersedes S031 — mirror disposal row | mined | … |")
curation-r90-controls.py:42   S219_ROW = (…same…)
curation-r89-mutants.py:36    MIRROR_ROW = (…same…)
curation-r90-mutants.py:36    MIRROR_ROW = (…same…)
```

**Re-derivation.** Scratch copy of the `9bad1201` tree, the S220 row's id changed to `S219` (one row;
still 219 rows), then the unchanged r89 battery run against that copy:

```
$ python3 -B corpus/evidence/round89/curation-r89-controls.py --root <scratch>/tree-s219 --work <scratch>/work
...
CASE_DEVIATION SUP-clause-mirror: NOT refused by r89 or NOT accepted by the prior counter
  r89: rc=1 CURATION_R89=FAIL
  prior: rc=1 CURATION_R88=FAIL
FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=6/7
CONTROLS=FAIL        (exit 1)
```

**The case that stops being accepted by the prior counter is `SUP-clause-mirror`** — the only case whose
prior-counter acceptance changes. In the pristine tree the same battery prints
`FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7 / CONTROLS=PASS` (exit 0) with
`OK SUP-clause-mirror: refused by r89 (LEG_FAIL TEACHES … sup_unresolved=1), accepted by the prior
counter` / `prior: rc=0 CURATION_R88=PASS`.

**Mechanism** (isolated, one fixture per counter — `receipts/b1-s219-reservation.txt`):

| tree | `curation-r89.py` | `curation-r88.py` |
|---|---|---|
| mirror only (no real S219) | `TEACHES_FLAGGED S031 … disposition=superseded by S219`, `sup_unresolved=1`, **FAIL** | `disposition=superseded by S219`, `LEG_FAIL` none → **PASS** |
| mirror + a real S219 row | `TEACHES_FLAGGED S031 … disposition=UNRESOLVED`, `TEACHES_UNRESOLVED=1`, **FAIL** | `disposition=UNRESOLVED`, `LEG_FAIL TEACHES … unresolved=1`, **FAIL** |

`parse_registry` (`corpus/evidence/round89/curation-r89.py:80-90`) is a **last-wins** dict:
`reg[cells[0]] = cells`. A real `S219` row sits *later* in `corpus/SOURCES.md` than the fixture's
injected mirror row, so the real row overwrites the mirror's and the mirror's
`supersedes S031 — mirror disposal row` edge vanishes. The r89 counter then cannot dispose S031's
flagged `teaches` cell, and — because the fixture's whole point is that the *prior* counter accepts the
shape — the prior counter refuses too. This is exactly the defect class already recorded in
`corpus/lessons/round-89.md` item 2 ("a mirror fixture id that collides with a real registry row is
silently discarded by last-wins", first seen with `S099`), and it is why the fixture id was moved to the
then-unused `S219`.

**Reservation, confirmed.** `S219` is absent from the real registry (`grep -c '^| S219 '` → 0) and the
row under it was written as `S220`. The failed gnu.org attempt is logged under `S219` in
`refetch.tsv` (line 186, `curl_rc=28`, `http_code=000`) and in
`.ufo/waves/round-90/egress.tsv` line 2 ("reserved id + failed attempt … no registry row written under
S219 (that id is the round-89 control fixture's mirror row)"), and it is not a registry row. Matches
the plan's disclosed reservation.

**Reverted.** The scratch copy's `S220` row was restored and `diff -q` against the pristine clone's
`corpus/SOURCES.md` reports `IDENTICAL_TO_PRISTINE` (`S219` count 0, `S220` count 1). The lane repo was
never touched.

**One extra observation (not a kill-rule hit).** The round-90 battery's frame is *regression*, not
*prior-acceptance*: `curation-r90-controls.py` against the same S219-collided tree still prints
`FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 / CONTROLS=PASS` (exit 0) — it requires both counters to
refuse, and here both do. The r89 frame's `PRIOR_ACCEPTED_FORGERY` leg is the one that exposes the id
collision, so the collision detector lives in the *prior* instrument, not the current one.

Receipt: `receipts/b1-s219-reservation.txt`.

---

## (c) C3 — independent tally count (not via the tool's own rule)

`SKILL.md` at `9bad1201`:

```
$ grep -c 'PASS (275 cases' SKILL.md   → 9
$ grep -c 'PASS (283 cases' SKILL.md   → 0
```

I classified **every** `PASS (N cases` occurrence in the file by my own rule — current = a Gates-table
row whose first cell names `research-gate`, **or** a line carrying the host-note `Selftest `PASS (`
phrase; historical = everything else — split further into the `, N skipped` shape and the bare `N cases`
shape (the latter are not tally cells at all and the tool's regex does not match them):

| class | count | where |
|---|---|---|
| **current** | **9** | lines 86–93 (8 Gates-table rows whose first cell names `research-gate`) + line 781 (host note, Round-37 section: `Selftest `PASS (275 cases, 0 skipped)` on this host.`) |
| historical, `, N skipped` shape | **3** | line 186 (`PASS (256 cases, 0 skipped)`, the Round-25 historical paragraph), line 188 (`PASS (161 cases, 0 skipped)`), line 640 (`PASS (215 cases, 0 skipped)`, Round-27) |
| historical, bare `N cases` shape | 12 | lines 160, 161, 186×3, 250, 273, 309, 346, 393, 437, 489 — per-round historical tallies without a skip count; **not** tally cells |
| **total `PASS (N cases` strings** | **24** | |

So: **9 current, 3 historical** in the bound shape — exactly the claim's `TALLY_ROWS=9` /
`OTHER_OCCURRENCES=3`, derived independently rather than read off the tool.

**Tool cross-check** (with a selftest receipt I captured myself, so the expected number is not a
literal):

```
$ TMPDIR=$S/work bash tools/research-gate.sh --selftest      # in the 9bad1201 clone
RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)          # exit 0, 166.33 s
ok-case  282 bash-pin-override-missing    exit=2
ok-case  283 bash-pin-override-fake       exit=2

$ python3 -B corpus/evidence/round90/skill-tally-r90.py --root <clone> --selftest <captured selftest>
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0      (×9)
TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL   (exit 1)
```

`EXPECTED_CASES=283` and `EXPECTED_SKIPPED=0` re-derive from the tool's own live verdict line, and the
`9/9` stale count matches the independent count above. At the attack revision the predicate is
`STALE_TALLIES=9/9`, which is what the brief expects (the repair lands after the wave).

Receipt: `receipts/c1-tally-occurrences.txt`.

---

## (d) Census

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit 0
```

```
$ bash …/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa
chousa	rows	219
chousa	tier.A	140
chousa	tier.B	59
chousa	tier.C	20
chousa	status.mined	183
chousa	status.queued	12
chousa	status.rejected	24
FLEET	rows	219 …	FLEET	missing	0
exit 0
```

**Exit 0, row count 219** — as expected. No `E`-code, no missing registry; the only findings are four
`W04` same-URL-across-scopes warnings, which by the tool's own contract do not change status.

The count is pinned to the attacked tree as well as the working lane: running the same census with
`--file <clone>/corpus/SOURCES.md` (the `9bad1201` bytes) also prints `rows 219`, and the lane's
working-tree `corpus/SOURCES.md` is byte-identical to `9bad1201`'s and to `aa7d4223`'s
(`git diff --stat` empty in both directions).

Receipt: `receipts/d1-census.txt`.

---

## Findings

| # | finding | severity |
|---|---|---|
| 1 | The brief's "11 words" for the quote holds only if the sentence-final `.` is a separate token; the whitespace-token count is **10**. The quote text is byte-exact. | observation (counting-convention deviation) |
| 2 | The capture bytes are **not committed at `9bad1201`**; they land one commit later in `aa7d4223` (child of `9bad1201`). Hash-verified against the committed `S220` refetch row, and the row's `used-by` cell points at a file that *is* committed at `9bad1201`. | observation (provenance timing) |
| 3 | The round-90 controls frame (`PRIOR_REGRESSION`) does **not** expose the `S219` id collision — it passes on a collided tree because both counters refuse. Only the r89 frame's `PRIOR_ACCEPTED_FORGERY` leg does. | observation (instrument placement) |

No kill rule of any claim is hit by this seat's scope: the S220 row and its capture re-open cleanly, the
id reservation is real and re-derived, the C3 tally count is independently confirmed (9 current / 3
historical), and the census is clean at 219 rows.

## Registry row list (the S220 row, in full)

| field | value |
|---|---|
| id | S220 |
| source | GNU grep(1) manual page, Matching Control, `-x`/`--line-regexp` — https://man7.org/linux/man-pages/man1/grep.1.html |
| kind | docs |
| tier | A |
| scope | GNU grep's whole-line match semantics (`-x`), for a receipt field checked as one token; not regex anchoring and not this lane's driver |
| anchor | Matching Control, `-x , --line-regexp` paragraph; man7.org page read 2026-11-08, capture key e6ec761219e8044b0e9e067a |
| teaches | `-x` selects only matches that exactly match the whole line, so a required receipt value must equal a whole token rather than occur inside a longer one |
| status | mined |
| opened | 2026-11-08 |
| recheck | 180d |
| used-by | corpus/evidence/round90/claims.md |

## Counts at a glance

| quantity | value |
|---|---|
| registry rows at base `f54a45ed` | 218 |
| registry rows at freeze `8d9893b4` | 219 |
| registry rows at attack `9bad1201` | 219 |
| rows added by the round | 1 (S220), `used-by` = `corpus/evidence/round90/claims.md` |
| `S219` rows in the real registry | 0 (reserved to the r89/r90 fixture mirror row) |
| capture quote located | `.txt` lines 166–167, `.raw` lines 152–153 |
| capture sha256 vs refetch row | match (`.txt` `5a5e69c5…`, `.raw` `d6f07a7f…`) |
| refetch `http_code` / `curl_rc` | 200 / 0 |
| refetch `fetched_utc` vs file mtime | 2026-11-08T09:52:31Z == 09:52:31Z (equal) |
| `PASS (275 cases` / `PASS (283 cases` in SKILL.md | 9 / 0 |
| C3 current tally cells (independent) | 9 (8 Gates rows + 1 host-note `Selftest` line) |
| C3 historical occurrences (independent) | 3 (lines 186, 188, 640) — plus 12 bare-shape historical strings the tool's regex does not match |
| census exit / rows | 0 / 219 |

## Tooling

No tool was installed, upgraded, or removed by this seat. (`/home/vgpnk/.omp/agent/RULES.md` was read
for the tooling directive; the pacman guard in the seat brief was honoured by not touching pacman at
all.) Every check used the repo's own committed instruments plus `git`, `grep`, `awk`, `sed`, `sha256sum`
and `python3` already present on the host.

VERDICT: R90ScoutRegistry C1 held — S220's row, capture quote (`.txt` 166–167 / `.raw` 152–153), sha256 and refetch instant all re-derive cleanly, with two recorded observations (the quote is 10 whitespace-tokens not 11, and the capture bytes commit only at `aa7d4223`, one commit after the attacked revision).
VERDICT: R90ScoutRegistry C2 held — the `S219` reservation is real and re-derived: a real S219 row makes the r89 battery's `SUP-clause-mirror` case stop being accepted by r88 (`PRIOR_ACCEPTED_FORGERY` 7/7→6/7, `CONTROLS=FAIL`), and the scratch copy was reverted identical to pristine.
VERDICT: R90ScoutRegistry C3 held — an independent count of `SKILL.md` gives 9 current tally cells (8 Gates rows naming `research-gate` + the host-note `Selftest` line) and 3 historical occurrences, matching the tool's `TALLY_ROWS=9 OTHER_OCCURRENCES=3`, with `EXPECTED_CASES=283` re-derived from the tool's own selftest verdict.

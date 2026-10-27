# FrontierCurator — round-60 frontier curation audit

Seat: frontier curation (§2b step, `corpus/SOURCES.md` contract v1 as carried in
`/home/vgpnk/Projects/shokunin/CORPUS.md`). Read-only against the frozen claims, the current
counters, the registry and prior committed evidence. No external fetch, no writes outside this
file, no git/jj mutation. All commands were run from
`/home/vgpnk/Projects/shokunin/chousa-shokunin`; scratch at
`/fast/scratch/hyaku/chousa-r60/FrontierCurator` (removed before yield — every command and its
output below is inline, so nothing here depends on that directory).

## 0. Pins and the freeze-digest discrepancy (corroborates five peer seats)

- Assigned immutable claim SHA-256: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.
- Observed: `sha256sum corpus/evidence/round60-claims.md` → `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (3355 bytes, 17 lines).
- My extra probes (all ran, none matched): raw bytes; trailing newline stripped; CRLF; `strip()`;
  `path+bytes`, `bytes+path`, `abs-path+bytes`; the C1-only and C2-only halves; and every
  contiguous line-range removal (171 combinations over 18 split lines). No candidate reproduces
  `09d8053f…`.
- State: the file is **untracked** (`git status --porcelain` → `?? corpus/evidence/round60-claims.md`),
  so no committed byte-set exists to arbitrate. Its mtime is `2026-10-27 17:51:18`, the dispatch
  spec's is `17:55:15`; the digest appears 64× in `.ufo/waves/round-60/w1-spec.json`.
- [INFERENCE] Because every seat writes through a fresh mtime, a seat could not have produced
  these bytes after dispatch without an mtime change; the mismatch therefore most likely
  originated at freeze time (digest taken over different bytes than were written), not from wave
  traffic. Unresolved: which bytes the digest names. This is a `landing`-class freeze defect and
  blocks certifying any verdict against "the frozen claims"; it is reported, not repaired here.

## 1. Census before (registry state this seat found)

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          # 133
awk -F'|' '...NF!=13...' corpus/SOURCES.md                                      # malformed: 0
awk -F'|' '...tier...' corpus/SOURCES.md                                        # A=106 B=22 C=5
awk -F'|' '...status...' corpus/SOURCES.md                                      # mined=109 queued=19 rejected=5
awk -F'|' '...duplicate ids...' corpus/SOURCES.md | sort | uniq -d               # (empty)
awk -F'|' '...enum/tier inflation...' corpus/SOURCES.md                          # (empty)
awk -F'|' '...mined used-by paths...' | while read p; do [ -e "$p" ]||echo; done # (empty)
# last id: S133
```

Driver census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
```

This matches the committed `corpus/evidence/round60/census-start.txt` byte for byte (five
pre-existing W04, `exit=0`). Freshness queue —
`sources-census.sh overdue --root /home/vgpnk/Projects/shokunin chousa` → **exit 0, 133 `cadence`
lines, 0 `overdue` lines**: no row is due for recheck on 2026-10-27 (earliest NNd due date is
2027-01-17, from the round-24 `90d` rows).

## 2. The sourced leg C2 rests on: S101, cell by cell

`corpus/SOURCES.md:111` (cells, `|`-trimmed):

| cell | value |
|---|---|
| id | S101 |
| source | 中国学术期刊（光盘版）检索与评价数据规范（修订本）— copy hosted by 哈尔滨工业大学 — `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc` |
| kind / tier | docs / B |
| scope | the data specification whose fields and type identifiers underlie Chinese journal evaluation and citation statistics |
| anchor | section 11 (文献标志码), section 14.1 and 14.4 (参考文献) and the 15.7 parameter table **(UTF-16LE text of the raw .doc capture)**; located quotes char 11170, char 11205, char 11993, char 12161, char 13247, char 34374 |
| status / opened / recheck | mined / 2026-10-25 / 180d |
| used-by | `corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md, corpus/lessons/round-59.md` |

### 2a. The row's six anchors do not index the form any lane command prints

QUALITY criterion 97 defines the check — `python3 tools/capture-text.py <raw> --locate '<quote>'`
must print `LOCATED count=1 offset=N` with `N` equal to the stated `char N`. Ran for all six
registry quotes plus the two quotes the recent rounds used:

```
stated char 11170  -> LOCATED count=1 offset=11972   (line 217)
stated char 11205  -> LOCATED count=1 offset=12007   (line 217)
stated char 11993  -> LOCATED count=1 offset=12795   (line 241)
stated char 12161  -> LOCATED count=1 offset=12963   (line 245)
stated char 13247  -> LOCATED count=1 offset=14049   (line 270)
stated char 34374  -> LOCATED count=1 offset=25123   (line 406)
stated char 12960  -> LOCATED count=1 offset=12960   (line 245)   # round-60 quote
stated char 797    -> LOCATED count=1 offset=797     (line 71)    # r58/r59 quote
```

Result: **0/6 stated offsets equal the located offset; 6/6 phrases are uniquely locatable in the
defined OLE text form.** The row is therefore *reference-drift*: its `anchor` cell names a
"UTF-16LE text of the raw .doc capture", a decode no lane tool prints (263 U+FFFD, control bytes;
QUALITY 97's own text says so and says the six anchors "stay wrong until the correction rows
land"). The defined form itself is pinned here: `tools/capture-text.py` on
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` → 27,012 characters, sha256
`a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867` (identical to the round-60
`FORM_SHA` in `corpus/evidence/round60/c2-count.py:11` and to `.ufo/waves/round-60/s101-open.txt`).

The repair that exists is out-of-registry: `SCORECARD.md:2736-2748` "Round 54 pointer corrections"
carries nine anchored `correction:` lines (six for S101) mapping the old→new offsets. Contract v1
rule 2 sanctions only two moves on a row — `status`/`recheck`/`used-by` in place, and a **new row
whose `teaches` opens `supersedes S0NN —`**. A SCORECARD block is neither, so `SOURCES.md` read
alone still sends a reader to unusable offsets.

### 2b. The round-60 quote is inside a registry-anchored phrase (positive finding)

The C2 counter's `EXPECTED = 'c. 文献类型及载体类型标志；'` (`c2-count.py:9`) sits at char 12960,
line 245; the registry phrase 文献类型及载体类型标志 is at 12963 — the round's quote is the
registry anchor re-cut three characters earlier to take in the list marker `c. ` and the
full-width `；`. So C2's source evidence **is** bound to an already-registered phrase; no new
source claim is being made, and the claim's own wording ("does not claim new ground") is accurate.

## 3. Conformance findings

### F1 — blocker · the freeze digest does not match (see §0)
Cross-confirmed by `ClaimPlanner.md`, `IntegrityCritic.md`, `RegistryScan.md`, `S101Reopen.md`,
`FrontierReviewer.md`. My addition: no normalization/carries reproduces it and the mtime order
puts the divergence before dispatch. Action: the L1 must state which bytes the digest names (or
report the freeze as unverifiable) before any C1/C2 verdict is admitted.

### F2 — high · C2's counter cannot distinguish "landed this round" from "nothing happened", and does not cover the frontier line the lane has held open since round 55

- The counter's `ENTRY` is the **round-37** file (`c2-count.py:8`,
  `corpus/knowledge/citation-count-semantics-r37.md`, committed at `763b337`, working tree clean).
  Its `METADATA` leg needs `source: S101 — https://jc.hit.edu.cn/`, `verified-at:` and `recheck:`
  — present at entry lines 5, 8, 9. Its `LIMIT` leg needs `#### Unknown` plus the exact sentence
  "Whether the specification copy (S101) is the version in force" — present at lines 74, 79.
  Nothing in the counter reads a round-60 artifact path.
- Ran at the inspected tree, with no round-60 knowledge change:
  `python3 -B corpus/evidence/round60/c2-count.py --root <lane> --work <scratch>`
  → `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1` / `C2=PASS`, exit 0.
  (The `FORM` path is module-level `ROOT/'.ufo/waves/round-60/s101-open.txt'` (`c2-count.py:7`), so
  `--root` does not relocate it; `--work` is parsed and unused.)
- The lane's own frontier map names the unclosed item at `corpus/README.md:1211`: "the entry leg
  waits for a round whose counter covers S101's `used-by`". No leg of `c2-count.py` opens
  `corpus/SOURCES.md` at all, so C2 cannot close that line, and QUALITY 100's `used-by`
  old→new discipline is left to the lesson prose only.
- Consequence for the round: a C2=PASS would be honest about the pinned source bytes but cannot
  evidence the claimed new note, and would leave the frontier item exactly where round 55 left it
  (five rounds carried). The fix is not mine to land: either the counter gains a `used-by` leg
  plus a round-60 artifact binding, or the round reports this frontier line as **unchanged** and
  says why.

### F3 — high · the contract-sanctioned S101 correction row never landed; a validated draft is provided below

Evidence: §2a (0/6), QUALITY 97's named limit ("the six S101 anchors stay wrong until the
correction rows land"), `corpus/README.md:1211` (carried since round 55). No row with `supersedes
S101` exists: `grep -c 'supersedes S101' corpus/SOURCES.md` → 0. Fix, shown able to fail (§4).

### F4 — medium · the queued count overstates the live frontier

`status=queued` rows: S008 S009 S010 S011 S012 S017 S018 S019 S020 S021 S022 S023 S024 S026 S027
S028 S030 S031 S032 (19). Five of them are retired in substance by supersedes rows from round 25
(S019←S029, S020←S033, S021←S032, S022←S030, S024←S031) yet still read `queued` with the old
teaching intact; the three replacement rows S030/S031/S032 are themselves `queued`. A reader of
the table alone therefore sees 19 live leads where the live set is 14, and cannot tell old from
current without the unlabelled prose note at the file's end. Rule 2 permits an in-place `status`
change with an old→new log, so this is cheap: set the five retired rows `queued`→`rejected` and
log it. Measured on a lane-shaped scratch copy (`validate` → the five baseline W04 and `ok`,
`exit=0`; `census` → `status.mined 109 · status.queued 14 · status.rejected 10`), **or** leave
them and record this reading in the round-60 lesson. I did not change them — a curation decision
for the L1.

### F5 — medium · rule 2 append-only is violated across the lane's history (22 rows, 13 commits)

Sweep: for every commit touching `corpus/SOURCES.md`, parse the S101-style rows of the parent and
the commit and diff the cells; flag any changed cell that is not `status`/`recheck`/`used-by`.
Non-permitted cell edits found, none accompanied by a `supersedes` row:

```
round-30 fc97f43  S050.scope S055.teaches
round-32 53cf649  S060.scope S060.anchor S060.teaches S061.teaches
round-33 4c076a0  S062.anchor
round-34 bf7c931  S064.anchor
round-38 870074e  S071.teaches
round-46 3807537  S088.anchor ; 45ede9c S085.teaches S086.teaches S087.teaches S088.scope
round-47 3d2a063  S085.anchor
round-49 763b337  S096.source/anchor/teaches S098.teaches S099.scope S100.scope/anchor/teaches
                  S101.anchor/teaches S102.anchor/teaches S103.source/anchor/teaches
round-50 1d7aba0  S105.scope S105.anchor
round-51 41b4dca  S107.source S107.anchor
round-52 643ac77  S113.teaches
round-56 9897707  S129.scope S129.anchor S129.teaches
```

(`applies to 22 distinct rows`.) Some of these were honest narrowings, but the contract's only
repair path is a supersedes row; the mechanism is exactly how F3's unusable offsets survived.
`captured-by`: **none** — the census has no append-only check (E01–E12 do not compare revisions),
so nothing would have caught it. Fix candidates for the L1's `## Mistakes`: the carried S101
reference-drift (F3) and this class; both name the rule and the missing check.

### F6 — low/medium · the Search log has no note for rounds 53–59 (nor 33–39, 46–47)

Measured: the `## Search log` section holds 23 entries; round labels present are
24, 25, 26, 27, 28, 29, 30, 31, 32, 40, 41, 42, 43, 44, 45, 48, 49, 50, 51, 52. Absent:
33, 34, 35, 36, 37, 38, 39, 46, 47, **53, 54, 55, 56, 57, 58, 59** — and rounds 53–59 all carry a
`## Gate` section (`grep -c '^## Gate' corpus/lessons/round-5[3-9].md` → 1 each), i.e. each did
source work. Rule 5 asks for one prose note per bounded search. Round 60's own re-open of S101 is a
bounded search and has no note; a draft is supplied in §4c.

### F7 — low · no coverage/frontier section for rounds 58 and 59

`grep -n '^## Round' corpus/README.md` ends at `1234:## Round57 coverage and frontier`; rounds 58
and 59 have lessons and logs but no frontier record, so the round-60 section (required by the
frontier step's own bookkeeping) must both add itself and re-state the S101 line honestly.

## 4. Drafted artifacts (ready for the L1 to land; nothing written outside this report)

### 4a. Corrected S101 pointer row — **validated, with a red-before control**

Row appended after S133 (11 cells, NF=13). Scope cell deliberately identical to S101's so the
validator's E04 duplicate-URL gate is exercised; `teaches` opens `supersedes S101 —`.

```
| S134 | 中国学术期刊（光盘版）检索与评价数据规范（修订本）— copy hosted by 哈尔滨工业大学 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc | docs | B | the data specification whose fields and type identifiers underlie Chinese journal evaluation and citation statistics | sections 11, 14.1, 14.4 and the 15.7 parameter table in the defined OLE text form (tools/capture-text.py on corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw, 27012 characters, sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867); lines 217, 241, 245, 270, 406; located offsets 11972, 12007, 12795, 12963, 14049, 25123 | supersedes S101 — the six anchors re-pointed from a whole-file UTF-16LE decode (capture-text.py --locate gives 0/6 at the stated offsets) into the defined OLE text form (6/6, each located once) | queued | 2026-10-27 | 180d | — |
```

Shown able to fail, then pass (both ran against a lane-shaped scratch copy, `--file`):

```
# RED — same row, `supersedes S101 —` removed
file	E04	S134 duplicate url jc.hit.edu.cn/…/1f6f2731-….doc within scope the data specification whose fields …
exit=1
# FIXED — as drafted
file	W04	S051 … S053 … S073 … S074 … S075 …      (the five baseline warnings only)
file	ok	…/SOURCES-fixed.md
exit=0
# census on the fixed draft
file	rows 134 · tier.A 106 · tier.B 23 · tier.C 5 · status.mined 109 · status.queued 20 · status.rejected 5
```

So landing S134 predicts `rows 133→134`, `queued 19→20`, `tier.B 22→23`, `exit=0` with the same
five W04. If the L1 prefers `mined`, the row must also carry the citing note in `used-by`.

Gate line this row needs (contract rule 1 — URL, access date, ≤25-word located quote):

```
S134 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc
opened offline 2026-10-27 from the lane-owned capture (no fetch); raw sha256 6063a3af…, defined form sha256 a8e3e7ad… (27012 chars)
quote: `c. 文献类型及载体类型标志；` — defined OLE form, char 12960, line 245, count=1 (tools/capture-text.py --locate)
```

### 4b. S101 `used-by` (QUALITY 100) — exact old→new, only if the round lands a citing note

```
old: corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md, corpus/lessons/round-59.md
new: corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md, corpus/lessons/round-59.md, corpus/lessons/round-60.md
```

(and add `corpus/knowledge/<round-60 note>.md` only if a new entry file is created; if the note is
folded into the existing entry, the entry path is already present and the added token is the
lesson). Status `mined` and `recheck 180d` stay unchanged — reopening is not a recheck event.

Optional second leg, **not required by the frozen C2 predicate**: the entry's own provenance line
(`corpus/knowledge/citation-count-semantics-r37.md:5`) also names "UTF-16LE text of the raw
capture", so it fails criterion 97's first clause too. The lane's convention is an anchored
`correction:` line rather than a rewrite:

```
correction: corpus/knowledge/citation-count-semantics-r37.md:5 form "UTF-16LE text of the raw capture" -> tools/capture-text.py defined OLE form (27012 chars, sha256 a8e3e7ad…); the entry's quoted spans are already in that form
```

### 4c. Search-log note for round 60 (rule 5)

```
- Round 60 (2026-10-27): question — what does the lane-held capture of the HIT data specification
  state about the bibliographic type/carrier notation, and can that statement be located in the
  defined OLE text form? Where: the lane-owned committed capture only
  (corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw → tools/capture-text.py, 27012 chars, sha256
  a8e3e7ad…); no URL was fetched (L0 `8d77e6c1` still open). Identified 1 source, screened 1,
  included 1 (S101, re-opened — no new row), excluded 0. Located `c. 文献类型及载体类型标志；` once
  at char 12960/line 245, and the six registry anchors at 11972, 12007, 12795, 12963, 14049,
  25123 (each count=1; the registry's own six offsets equal none of them — S134 drafted).
  Stop rationale: the claim's one external fact has one primary capture; present-day validity and
  CNKI implementation stay unknown by scope.
```

### 4d. Mistakes rows for `corpus/lessons/round-60.md ## Mistakes`

```
1. **landing (freeze digest not bound)** · `corpus/evidence/round60-claims.md` sha256
   `65721569…` vs the assigned `09d8053f…`; file untracked, mtime 17:51:18 precedes the spec's
   17:55:15; no normalization and no contiguous-line removal reproduces the assigned digest.
   Captured-by: none — no pre-data step writes the freeze digest beside the artifact and re-checks
   it before writing `.ready`. Fix: write `sha256` into the freeze record at creation and re-check
   it at dispatch; shown able to fail by the printed mismatch above.
2. **reference-drift carried five rounds** · S101 anchors six quotes in a decode no tool prints
   (0/6 under criterion 97's own check), named as pending in round 54 and at
   `corpus/README.md:1211`, still unlanded in round 60 while the claim's counter reads a different
   form. Captured-by: QUALITY 97 names the limit but no check requires an open frontier line to be
   closed or retired. Fix: land S134 (validated above) or record a retirement reason.
```

## 5. Verified / not verified

Verified by execution here: the driver census and its exit code, the frozen manual census block,
`overdue` (exit 0, 0 due), the S101 cell dump, `capture-text.py --locate` for eight phrases,
`sha256sum` of the claims file and the defined form, the `c2-count.py` run, the 13-commit registry
cell sweep, the lesson/heading/search-log greps, the draft-row control pair.

Not verified: whether the on-disk claims bytes are the frozen bytes (F1); any external truth about
S101 (no fetch, and L0 `8d77e6c1` open); the C1 counter and its controls (peer seats ran them —
`FrontierReviewer.md`, `IntegrityCritic.md`, `CounterAudit.md`); no LSP device was available, so
all references are textual. Nothing outside this report was written, and no git/jj state changed.

## 6. Handoff checklist for the L1 (§2b frontier step)

1. Resolve F1 first: state the bytes the assigned digest names, or declare the freeze unverifiable.
   Do not read any C1/C2 verdict as admitted until that is settled.
2. Paste the census before/after with exit codes: `sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin chousa`; before is `census-start.txt` (`exit=0`, five W04);
   after is `exit=0` again, `133` rows if nothing lands (or `134` / `queued 20` / `tier.B 23` with
   S134 — measured on the draft).
3. Land or retire the S101 frontier line: either append §4a's validated row plus its Gate line and
   §4b's `used-by` old→new, or record in the lesson why the front is unchanged. Do not record a new
   numeric score for it; the round-54 measurement stands as the last real move.
4. Add the §4c Search-log note (round 60 is a bounded offline search and currently has none).
5. Add a `## Round60 coverage and frontier` section to `corpus/README.md` and carry forward the
   S101 entry-leg line verbatim from `:1211` if it is still open, naming the counter that must
   cover it.
6. Choose one §4d mistakes row (both are new; F1's is the stronger round lesson).
7. In the report, state that C2's counter has no leg for the claimed new artifact or for
   `used-by` (F2), so a `C2=PASS` receipt proves the pinned source bytes and the round-37 entry's
   limit sentence, nothing about a round-60 note.

# R92ScoutRegistry — registry and corpus-surface reconnaissance, round 92 wave 1

**Seat:** R92ScoutRegistry (scout) · **Lane:** chousa · **Wave:** round-92 / w1
**Target tree:** carrier C5 `16ccf7693c61b8ffe392fc757352304f239bfcad` (freeze F5 `42e0337822a508208800f98faa3a63c6af9f8c27`)
**Scratch:** `/fast/scratch/hyaku/chousa-r92/R92ScoutRegistry` (clone via `git clone --shared`, checked out at C5; removed before yield)
**Receipts:** `.ufo/waves/round-92/w1/R92ScoutRegistry/receipts/` (11 files, `01`–`11`)

No edits to production bytes. No lane/fleet git or jj mutation, no commits, no pushes, no subagents, no network
beyond local file reads. Every command below was run in the clone at C5 (or against the lane's own read-only
`corpus/SOURCES.md`); every command names the receipt that carries its raw output and exit code.

---

## F1 — S070's premise re-opens byte-exact, but its anchor label is the one S073 superseded (C1-adjacent, registry surface)

**Command** — `sha256sum /usr/share/man/man1/sha256sum.1.gz` → `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (exit 0).
Receipt `01-s070-premise.txt`.

The registry row S070 (`corpus/SOURCES.md:80`) records `file SHA-256 93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`.
**The row's recorded sha still matches the installed file byte-for-byte.** The installed package is `coreutils 9.12-2`
(`pacman -Qi coreutils`), matching the row's `coreutils 9.12-2`.

**Command** — `zcat /usr/share/man/man1/sha256sum.1.gz | grep -n 'Print or check SHA256'` →
`11:Print or check SHA256 (256\-bit) checksums.` (exit 0). Receipt `01`.

The decompressed line carrying the claim's quote is **line 11**, exactly as the row's anchor says (`quote at line 11`).
Raw bytes (`od -c` of that line) are `P r i n t   o r   c h e c k   S H A 2 5 6   ( 2 5 6 \ - b i t )   c h e c k s u m s .`
— the hyphen is roff-escaped as `\-`.

**Command** — `zcat … | sed -n '4p;5p;11p;19p;20p;54p;55p;56p'` → the row's other anchor spans resolve to real lines
(4 = `sha256sum \- compute and check SHA256 message digest`; 5 = `.SH SYNOPSIS`; 19 = the `-c, --check` tty-link;
20 = `read checksums from the FILEs and check them`; 54 = `The sums are computed as described in FIPS-180-2.`;
55 = `When checking, the input should be a former output of this program.`; 56 = `The default mode is to print a line with: …`).
Receipt `01`. **All of S070's recorded offsets resolve to the lines they claim.**

### F1a — the row's `SYNOPSIS` anchor label is the label S073 exists to correct

S070's anchor cell reads `NAME/DESCRIPTION and SYNOPSIS \`-c, --check\` (decompressed lines 4–11, 19–20, 54–56; quote at line 11)`.
S073 (`corpus/SOURCES.md:83`, `mined`, `opened 2026-10-24`) carries `supersedes S070 —` in its anchor and teaches:
*"the `-c, --check` entry is a DESCRIPTION `.TP` item, not a SYNOPSIS line: `.SH SYNOPSIS` line 5 (body 6–7, no option
entries), `.SH DESCRIPTION` line 8, `-c, --check` at decompressed lines 19–20"*. Receipt `03`.

My measurement agrees with S073 and against S070's label: decompressed line 5 is `.SH SYNOPSIS`, line 8 is `.SH DESCRIPTION`,
and lines 19–20 sit under DESCRIPTION. **S070's `SYNOPSIS` label is wrong on the bytes; S073 is the live row.** S073 pins the
same file sha (`93c17dff…403f`, re-opened 2026-10-24).

This does **not** move the C1 predicate: the claim's rule 5 (digest check, including the minus-self self-pin) rests on the
page's *digest-printing* text at line 11, and the self-pin leg is independently verified — the recorded self row
`5f288597d4bad803cbd3ba511d06e362c99911c30782742f378a872977f03275` equals the sha256 of `instrument-pins.txt` with its own
row removed, re-derived by reimplementing the driver's rule (`control-driver-r92.py:179-190`) and again by the
raw-bytes-minus-the-row-line variant — both give `5f288597…f03275`, MATCH True (receipt `11-self-pin-derivation.txt`);
the driver prints `RECEIPT SELF_PIN OK rev=42e0337… receipts_rev=16ccf769…`, `CONTROL_DRIVER_R92=PASS`, exit 0).
It is a citation-precision finding on the registry surface, not a kill-rule firing.

### F1b — the claim's quote is the *rendered* form, not a literal substring of the source bytes (carried from r91, unchanged)

**Command** — `grep -c 'Print or check SHA256 (256-bit) checksums\.' <decompressed>` → `0` (exit 1);
`grep -c 'Print or check SHA256 (256\-bit) checksums\.'` → `1` (exit 0). The literal claim-quote string does **not** occur
in the decompressed roff. **Command** — `man --nh --nj -P cat …| grep -n 'Print or check'` → line 10:
`Print or check SHA256 (256-bit) checksums.  Legacy interface to the` — it **is** literal in the rendered page.
Receipt `02-quote-form.txt`.

Round 91's spot-check already made this point (`corpus/lessons/round-91-verifier-spotcheck.md:67` records the *rendered*
form and accepts the row) and round 91's lesson (`:17-19`) says the same, but the lesson calls it **"7 words"** while
`printf '%s\n' 'Print or check SHA256 (256-bit) checksums.' | wc -w` → **6** (receipt `02`). The r92 claim text
(`corpus/evidence/round92/claims.md:37`) inherits the r91 wording unchanged except for the added clause "including the
self-pin". So the r92 claim cites S070 for a quote it does not literally contain, and the r91 lesson's word count is off by one.
Neither is a C1 kill rule; both are citation-precision findings.

### F1c — the r92 tree records no S070 re-open artifact

`corpus/SOURCES.md` is **byte-identical between base and carrier** (`git diff --stat d7780fef..16ccf769 -- corpus/SOURCES.md`
→ empty), so S070's row was not touched this round; its `opened` cell still reads `2026-10-23`. The only round-92 bytes
naming S070 are `corpus/evidence/round92/claims.md:37`, `corpus/evidence/round92/egress.tsv:3` and
`.ufo/waves/round-92/claims.json:49`. `corpus/lessons/round-92.md` — which `claims.md:6` names as the place the freeze and
carrier are recorded — **does not exist at F5 or C5** (`git ls-tree` on both revisions → empty). Receipt `03`.

So the round-92 claim's "re-opened this round" has no committed re-open record (no `GATE-RECORD` line, no registry edit, no
lesson). This is the same gap r91's scout named (F4 in the r91 seat report) and it is carried, not fixed.

---

## F2 — the six routed sources are `mined` and each `used-by` names its citing entry as an exact token (no drift)

Re-derived independently of the counter (own parser + own tokeniser, matching `curation-r92.py`'s `used_by_tokens`).
Receipt `04-six-sources-usedby.txt`.

| source | status | tier | `used-by` cell | exact-token names |
|---|---|---|---|---|
| S214 | `mined` | A | `corpus/knowledge/search-transparency-reporting-r84.md` | r84 ✓ |
| S018 | `mined` | B | `corpus/knowledge/search-transparency-reporting-r84.md` | r84 ✓ |
| S023 | `mined` | A | `corpus/knowledge/search-transparency-reporting-r84.md` | r84 ✓ |
| S215 | `mined` | A | `corpus/knowledge/provenance-recording-r85.md` | r85 ✓ |
| S026 | `mined` | A | `corpus/knowledge/provenance-recording-r85.md` | r85 ✓ |
| S031 | `mined` | A | `corpus/knowledge/provenance-recording-r85.md` | r85 ✓ |

**No drift on any of the six.** Each row's `used-by` cell holds exactly one token, and that token is the citing entry's
repo path — an exact token under the counter's split (`[^A-Za-z0-9._/-]+`), so `used_by_tokens` yields a one-element list
containing the path. The basename is *not* a separate token; the counter's `source_link` accepts either
`entry in tokens or entry_rel in tokens`, and it is the **full path** that matches.

**Two-sided check over all 219 registry rows** (not just the six): exactly six rows token-join to either routed entry
(S018, S023, S214 → r84; S026, S031, S215 → r85), all six `mined`, and each is cited by at least one Located-quote row of
that entry. **Zero mined-and-named-but-uncited rows.** **Zero substring-only mentions** anywhere in the registry
(a scan of every `used-by` cell for the entry basenames found no row that mentions an entry without an exact token).

**Capture presence** — every cited source's capture file exists on disk (`capture_text` key = `sha256(url)[:24]`):
S214 → `a640b15abf781e5c583d7088`, S018 → `248b43277f376e437a356909`, S023 → `f5545a194c06ab421875b047`,
S215 → `6e48bcc4a04d13b7b3ebb68e`, S026 → `67983a3dbbd1d690aa648744`, S031 → `11d6cc56bb24adfc61eea2b4`. Receipt `04`.

---

## F3 — the two entries' row shapes re-derive exactly to the pinned counts (13/7 quote rows, 11/6 decision rows, all widths 3/4)

Re-derived from raw bytes by splitting the file on `## ` and enumerating every pipe-leading line with its cell count and
kind (HEADER / SEP / DATA). Receipt `05-quote-and-decision-rows.txt`.

**`corpus/knowledge/search-transparency-reporting-r84.md`**
* `## Located quotes` — 15 pipe-leading lines = 1 header (`qid`) + 1 separator + **13 DATA rows, all width 3**
  (Q1…Q13; Q1–Q5 → S214, Q6–Q8 → S018, Q9–Q13 → S023).
* `## Decision table` — 13 pipe-leading lines = 1 header (`Situation`) + 1 separator + **11 DATA rows, all width 4**.

**`corpus/knowledge/provenance-recording-r85.md`**
* `## Located quotes` — 9 pipe-leading lines = 1 header + 1 separator + **7 DATA rows, all width 3**
  (Q1–Q4 → S215, Q5–Q6 → S026, Q7 → S031).
* `## Decision table` — 8 pipe-leading lines = 1 header + 1 separator + **6 DATA rows, all width 4**.

**The decision-count pin matches.** `curation-r92.py`'s `DECISION_COUNTS` pins `11` and `6`; `FLOORS` pins `13` and `7`;
measured 13/7 quote rows and 11/6 decision rows — every pin agrees, and 11 + 6 = 17 = the `WARRANT_OK=17/17` denominator.
Receipt `05`.

**Two located quotes are never warranted** (not a defect, an observation the L1 may want named): r84's `Q10`
(`Recommended practice is to describe the date … Date`) and r85's `Q3` (`then we can say that the bar chart
prov:wasDerivedFrom the dataset.`) are cited by no decision row. Every warrant qid that *is* used resolves to an existing
quote row of the same entry (no dangling qid). No claim sentence forbids an unwarranted quote row.

**C2's frozen counter on the committed C5 bytes:** `python3 -B corpus/evidence/round92/curation-r92.py --root .` →
`CURATION_R92=PASS` (exit 0) with `Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17
TFREQ_MAX_DF=3 UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0 LEGS_MEASURED=14/14 SUPERSEDED_LIVE=0`. Receipt `08`.

---

## F4 — the registry census is clean (exit 0); the seat spec's row-count grep matches nothing

**Command** — `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ five `W04` warnings (S051, S053, S073, S074, S075 — duplicate URL across scopes) and a final
`chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`, **EXIT=0**. Receipt `06`.

`W04` is a warning code; the census's own contract says "W-codes … never change status". The same run against the
clone's committed `corpus/SOURCES.md` (sha256 `7a2f6d53fe47ac9dc8c8931f8e21619862f0b919ecea0cd387e7f92544f5c1c1`, identical to
`git show 16ccf769:corpus/SOURCES.md`) gives the identical output and **EXIT=0** — so the result is the tree's, not the
working directory's.

**Row count.** The seat spec's `grep -cE '^ (0, 3)\|[[:space:]]*S[0-9](3,)' corpus/SOURCES.md` returns **0, exit 1**.
That pattern is a literal alternation on `" (0, 3)|"` / `"S<digit>(3,)"`; it does not match this registry's shape
(`| S214 | … |`), so it is a malformed expression rather than a count of 0 rows. Resolved counts, three ways
(receipt `10`): `grep -cE '^[[:space:]]*\| S[0-9]{3,} '` → **219**; `awk -F'|' 'NF==13'` → **221** (219 data rows + the
2 header/separator rows, which also have 11 cells); the census's own `census` mode reports `file rows 219`
(tier A 140 / B 59 / C 20; mined 183 / queued 12 / rejected 24) and `FLEET rows 219`. An independent 11-cell parse yields
**219 rows, 219 unique ids**. The registry's row count is **219**.

---

## F5 — the frozen claims name two instrument paths that have never existed in the tree (C1/C2 wording; not my kill rules)

`corpus/evidence/round92/claims.md` and `.ufo/waves/round-92/claims.json` name
`corpus/evidence/round92/control-forgeries-r92.py` and `corpus/evidence/round92/curation-r92-controls.py`.
Neither path exists at C5, and `git log --all --diff-filter=A` shows **neither name has ever existed at any revision**.
The tree carries `forgeries-r92.py` and `curation-controls-r92.py` instead. Receipt `07-claim-instrument-names.txt`.

Running the claim's literal command lines from the clone:
* `python3 -B corpus/evidence/round92/control-forgeries-r92.py --work <scratch>` → exit **2**, `python3: can't open file … No such file or directory`.
* `python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work <scratch>` → exit **2**, same.

The tree's actual instruments carry the claimed tokens:
* `forgeries-r92.py --work <scratch>` → exit 0, `FORGERY_REFUSED=3/3 POSITIVE=pass` (3 OK lines + the positive).
* `curation-controls-r92.py --root . --work <scratch>` → exit 0,
  `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 CARRIED_F1_F4=refused-by-both DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4`.

**Wording findings this surfaces for C2** (the sibling C2 seat has the mandate; I record the bytes):
1. the claim's C2 statement lists the controls' field tail as `… DUPCOUNT_R92=1 PRIOR_REGRESSION=7/7`, but the **summary
   line actually ends `PRIOR_REGRESSION=4/4`** — `7/7` occurs only on the earlier `OK regression: FORGERY_REFUSED=7/7
   PRIOR_REGRESSION=7/7 rc=1` line. All seven named tokens do occur somewhere in stdout, so a per-token grep succeeds and a
   strict line-order match would not. Receipt `08`.
2. the C1/C2 counting-command paths are the two non-existent names above.

**Unpinned twin instruments.** `corpus/evidence/round92/tally-r92.py` and `tally-controls-r92.py` are present at C5 and
are **byte-identical** to `skill-tally-r92.py` / `skill-tally-r92-controls.py` (same sha256:
`ac5bf547…`, `3eb7918e…`), but only the `skill-tally-*` paths are in `instrument-pins.txt` (16 rows). History shows the
`skill-tally-*` copies were **added** at F2 (`487b8f25`) while the originals were **never deleted** — duplicated, not renamed.
No `expected.tsv` row names a twin, so C1's rule 5 is not engaged; but two unpinned executables that are exact copies of
pinned ones sit in the evidence directory. Receipt `09-unpinned-twin-instruments.txt`.

---

## What I did not touch (stated so it is not read as covered)

* C3's `## Gates` scoping, case-range pins and selftest — outside this seat's surfaces; not exercised here.
* The C1 driver's pin/freshness legs beyond the incidental runs recorded in `07` (I ran `verify` once at F5/C5:
  `CONTROL_DRIVER_R92=PASS`, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7`, exit 0 — a supporting
  datapoint, not a claim verdict; the C1 mandate sits with the executor/reviewer seats).
* `tools/research-gate.sh`, `tools/gate-records.py`, `SKILL.md` — confirmed unchanged base→C5 (`git diff --stat` on
  `tools/` and `SKILL.md` → empty).

## Tools

None installed or upgraded. `RULES.md` read first; the pacman guard is honored — the only `pacman` use was the
read-only `pacman -Qi coreutils` (version query, no transaction). No `sudo`, no sysctl, no service restart, no network.

## Scratch

`/fast/scratch/hyaku/chousa-r92/R92ScoutRegistry` (clone + `work/`) — removed with `rm -rf` after the receipts were
copied into `.ufo/waves/round-92/w1/R92ScoutRegistry/receipts/`.

---

VERDICT: R92ScoutRegistry C1 fired — S070's premise re-opens byte-exact (recorded sha256 still matches the installed
`sha256sum.1.gz`; every anchor offset resolves; the self-pin minus-self digest re-derives), but the claim cites the
superseded row S070 (S073 exists to correct its wrong `SYNOPSIS` anchor label), quotes the rendered rather than the literal
source form, and the round-92 tree carries no re-open record for it — citation-precision findings, not a kill-rule firing.
VERDICT: R92ScoutRegistry C2 held — all six routed sources are `mined` with `used-by` naming their citing entry as an exact
token (zero substring-only mentions, zero mined-but-uncited rows, all captures present), the 13/7 quote rows and 11/6
decision rows re-derive at widths 3/4 exactly matching the pinned counts, and the registry census validates clean at exit 0
with 219 rows — the C2 predicate's registry surfaces are sound (the claim-vs-tree instrument-path and `PRIOR_REGRESSION`
wording findings belong to F5 and do not change the C2 verdict).
VERDICT: R92ScoutRegistry C3 n/a — this seat's surfaces are the registry and the corpus entries the claims read; C3's
`## Gates` scoping, case-range pins and selftest were outside scope and were not exercised.

# R91ScoutRegistry — registry and corpus-surface reconnaissance (chousa, round 91)

Seat: `R91ScoutRegistry` (scout, leaf). Wave: round-91 w1.
Scratch: `/fast/scratch/hyaku/chousa-r91/R91ScoutRegistry` (deleted on yield).
Tree attacked: clone of `chousa-shokunin` at carrier **C3 = `67954adc599bd605705d94a1ea7abb582491a907`**
(`git clone --shared` + `git checkout 67954adc`), verified with `git rev-parse HEAD` →
`67954adc599bd605705d94a1ea7abb582491a907`.
Freeze **F3 = `4d00d7519290569879f853d7122b82a927cda1f3`** read from the same clone.
No edits, no commits, no network, no subagents, no tool installs (nothing needed installing).

Receipts written by this seat (all under `.ufo/waves/round-91/w1/R91ScoutRegistry/`):

| receipt | what it carries |
|---|---|
| `01-s070-premise.txt` | S070's premise re-opened from committed bytes (sha256, decompressed line 11, `wc -w`, `grep -cF`) |
| `02-s221-attempt.txt` | the planned S221 attempt: egress commit, egress table, the `refetch.tsv` row, `grep -c '| S221 |'`, capture-key absence |
| `03-six-sources.txt` | the six routed sources' registry cells (`status`, `used-by`, tier, capture keys) |
| `04-c2-surfaces.txt` | C2's read surfaces: 20 located-quote rows, 17 decision rows, per-row capture resolution |
| `05-census.txt` | `sources-census.sh validate` exit code and the registry row count |
| `06-drift-checks.txt` | drift probes on the S070 citation path and the plan's S221 receipt |
| `07-s070-gate-form-probe.txt` | `tools/gate-records.py` probe of the three record forms against S070 |
| `08-corroboration.txt` | C2 counter run on the C3 clone + quote-literal probes |

---

## 1. S070's premise, re-opened from committed bytes

**Observed (all commands run from the C3 clone; the man page is a host file, read-only).**

```
$ sha256sum /usr/share/man/man1/sha256sum.1.gz
93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f  /usr/share/man/man1/sha256sum.1.gz
exit=0
```

**The row's recorded sha still matches, exactly and in full.** `corpus/SOURCES.md:80` (S070) records
`file SHA-256 93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`; the installed file hashes to
the same 64 hex digits. The row's `opened` cell is `2026-10-23`, `recheck` is `on-release`, `status` is `mined`,
`kind` `docs`, `tier` `A`. The installed coreutils is `9.12-2` (`pacman -Qi coreutils`), matching the row's
`coreutils 9.12-2`. **No drift on the digest.**

**The decompressed line that carries the quote.**

```
$ zcat /usr/share/man/man1/sha256sum.1.gz | grep -n 'Print or check SHA256'
11:Print or check SHA256 (256\-bit) checksums.
exit=0
```

Decompressed line 11 it is; the file is 83 decompressed lines. The row's `anchor` cell names
`decompressed lines 4–11, 19–20, 54–56; quote at line 11` — re-measured on the installed page
(receipt 08 §E6), lines 4–11 carry the NAME/SYNOPSIS/DESCRIPTION block through the quote, 19–20 carry the
`-c, --check` entry, 54–56 carry the FIPS-180-2 / check-input paragraph. **The anchor spans are accurate.**

**Registry row cells, verbatim** (`corpus/SOURCES.md:80`):

- `source` = `` GNU coreutils `sha256sum(1)` manual — `/usr/share/man/man1/sha256sum.1.gz` ``
- `anchor` = `` NAME/DESCRIPTION and SYNOPSIS `-c, --check` (decompressed lines 4–11, 19–20, 54–56; quote at line 11); coreutils 9.12-2; file SHA-256 `93c17dff…` (opened locally 2026-10-23) ``
- `teaches` = `` `sha256sum` prints or checks SHA256 (256-bit) checksums, and `--check` reads checksums from files rather than computing a policy. ``

**Two findings on the citation path.**

**F1 — C1's source quote is not a literal substring of the source bytes.**
`corpus/evidence/round91/claims.md:33` carries the quote `"Print or check SHA256 (256-bit) checksums."`.
Against the installed page:

```
$ zcat /usr/share/man/man1/sha256sum.1.gz | grep -cF 'Print or check SHA256 (256-bit) checksums.'
0            (exit=1, no match)
$ zcat ... | grep -cF 'Print or check SHA256 (256\-bit) checksums.'
1            (exit=0, match)
```

The roff source carries `256\-bit`; the hyphen is escaped. The claim's quote is the *rendered* form, not a byte
substring. The same holds for `corpus/lessons/round-91.md:18` (uncommitted working tree). Under the lane's own
citation rule (`CORPUS.md` "A quote names its location"; QUALITY 154 "a located quote is re-opened, `grep -c`'d at
the named location"), the printed quote does not grep at the named location; the S070 row's `teaches` cell has the
same rendered form, so the row and the claim agree with each other and disagree with the bytes. **This is a
citation-precision finding, not a claim-firing one** — the man page's own words do state that the tool "prints or
checks a digest", which is what C1 rule 5 rests on. Note the S073 row quotes line 20 literally
(`read checksums from the FILEs and check them`, 8 words, verified) because that line has no escape.

**F2 — the lesson's word count for that quote is off by one.**
`corpus/lessons/round-91.md:18` says the line reads the quote *"(7 words)"*. Measured: `wc -w` on the rendered
form = **6**, and `wc -w` on the raw roff line = **6**. Six is also what `tools/gate-records.py` would compute if a
record ever named it (that tool counts whitespace-separated tokens of the quote). The lesson's "7 words" is a
mis-count of the very quantity the lane's word-count rule checks — the same class as the lesson's own Mistake row
5 ("a quote's word count miscounted again", `words=5` → 4 for the S001 record).

**S070 vs S073 (supersession).** `S073` (`corpus/SOURCES.md:83`) is `mined`, opens
`` `supersedes S070 —` `` in its `anchor`, and its `teaches` cell corrects S070's anchor label (the `-c, --check`
entry is a DESCRIPTION `.TP` item, not a SYNOPSIS line). S073's own quote is at line 20; it does **not** carry the
line-11 quote C1 cites. So the correction edge does not supply C1's quote, and the lane's QUALITY 174/178 rule
("a frozen `teaches` cell is not evidence; the superseding row's is") does not invalidate C1's grounding —
S070's `teaches` cell is the one cell in the registry that carries the digest sentence. **Citing S070 rather
than S073 is defensible here and I record it as such.** Two further cells are consistent with the round: S070's
`used-by` names `corpus/knowledge/engine-swap-canary-r36.md, corpus/knowledge/claim-pin-provenance-r37.md` and no
round-91 claims file, while the lane's precedent rows (S216, S218, S220, S166–S179) *do* name their citing
claims file; and no `GATE-RECORD` line exists for S070 in the round-91 lesson (only S001 has one). QUALITY 173
requires a `GATE-RECORD` line for every row the round opened/re-anchored/re-opened *or* a named schema gap. I
probed all three forms against S070 (receipt 07): `url/admit` is impossible (S070's `source` cell carries no URL
and there is no capture), and `rev` fails `LINE,REV` (the man page is not a repo blob). **That is a genuine schema
gap and the lesson does not name it** — the round-91 lesson names no schema gap anywhere (grep for
`schema|gap` over `corpus/lessons/round-91.md` returns nothing). This is a finding against the lesson's
`## Gate` completeness, not against C1's predicate.

---

## 2. The planned S221 attempt

**Egress table commit and URL.** `corpus/evidence/round91/egress.tsv` is committed, and its only commit is:

```
$ git log --oneline -- corpus/evidence/round91/egress.tsv
7b19dd0b round-91: egress table committed before the first fetch
$ git show -s --format='%H %cI %s' 7b19dd0b
7b19dd0b96f69a2167cb17e31cb998643d1a1b8d 2026-11-08T08:05:08-03:00 round-91: egress table committed before the first fetch
```

The URL in that committed table is
`https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-term-weighting-1.html`, method
`curl -fsSL --compressed --max-time 15 GET via tools/capture-fetch.py`, scope `open`.
The egress table is committed **before** the fetch (commit 08:05:08-03:00; fetch row timestamp
`2026-11-08T11:05:29Z` = 08:05:29-03:00, 21 s later). Ordering holds.

**The `refetch.tsv` row.** The row exists — but **only in the lane working tree, not in any committed revision**:

```
$ git show 67954adc:corpus/evidence/round57/refetch.tsv | grep -c 'S221'
0            (grep exit=1, no match)
$ git show 4d00d751:corpus/evidence/round57/refetch.tsv | grep -c 'S221'
0            (grep exit=1, no match)
$ grep -n 'S221' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round57/refetch.tsv
189:S221	https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-term-weighting-1.html	64fdb4143cc4f628a805cf0a	1	2026-11-08T11:05:29Z	28	000	-	-
```

Shape matches the plan's `S221 … 28 000 - -`: `curl_rc=28`, `http_code=000`, both sha columns `-`. The row is an
**uncommitted modification** of `corpus/evidence/round57/refetch.tsv` in the lane working tree (visible as the
`+S221 …` line in `git diff 67954adc -- corpus/evidence/round57/refetch.tsv`). **F3 — the plan and the lesson both
cite a receipt that is not in the tree they point at.** `plans/round-91.md:33` (committed at F3) says the failed
attempt is recorded as "`refetch.tsv` row `S221 … 28 000 - -`", and `corpus/lessons/round-91.md:26` repeats it, but
at F3 and C3 that row does not exist in the committed bytes. It lands only in the working tree. The lesson is
itself uncommitted (`?? corpus/lessons/round-91.md`), so the two are consistent with each other and inconsistent
with the committed tree. The lane rule "A quote names its location" / "An index row is a claim" points the same
way. This is a **citation-precision finding against the round's own documentation**, not a C1/C2/C3 predicate
failure — the attempt really happened (the tool wrote the row), and the row is byte-identical to what the plan
describes.

**`grep -c '| S221 |' corpus/SOURCES.md` is 0** — in the C3 clone *and* in the lane working tree, `grep` exit 1
(no match). No `S221` row exists in the registry; the highest id is `S220`. Consistent with "no S221 row is
written".

**No capture key exists for the URL.** The key derivation is `sha256(url)[:24]`, verified against a committed
row: `printf '%s' 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/' | sha256sum | cut -c1-24`
→ `f5545a194c06ab421875b047`, which is exactly the key the committed `refetch.tsv` carries for S023. For the
attempted URL:

```
$ printf '%s' 'https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-term-weighting-1.html' | sha256sum | cut -c1-24
64fdb4143cc4f628a805cf0a
$ ls corpus/captures/64fdb4143cc4f628a805cf0a.raw corpus/captures/64fdb4143cc4f628a805cf0a.txt
ls: cannot access 'corpus/captures/64fdb4143cc4f628a805cf0a.raw': No such file or directory
ls: cannot access 'corpus/captures/64fdb4143cc4f628a805cf0a.txt': No such file or directory
exit=2
```

The key matches the one the `refetch.tsv` row records, and **neither capture file exists** — the fetch produced no
bytes, as claimed. The only capture mentioning "document frequency" is `44be8711b50a9daae2865b02` (S093, an
arXiv capture), unrelated to this URL.

---

## 3. The six sources cited by the two routed entries' Located-quotes rows

The two routed entries are `corpus/knowledge/search-transparency-reporting-r84.md` (`source: S214, S018, S023`)
and `corpus/knowledge/provenance-recording-r85.md` (`source: S215, S026, S031`).

Every one of the six is `status=mined` and its `used-by` cell names the entry that cites it — **no drift in any
of the twelve cells**:

| id | `corpus/SOURCES.md` line | `status` | `used-by` | names the citing entry |
|---|---|---|---|---|
| S214 | 227 | `mined` | `corpus/knowledge/search-transparency-reporting-r84.md` | yes |
| S018 | 28 | `mined` | `corpus/knowledge/search-transparency-reporting-r84.md` | yes |
| S023 | 33 | `mined` | `corpus/knowledge/search-transparency-reporting-r84.md` | yes |
| S215 | 228 | `mined` | `corpus/knowledge/provenance-recording-r85.md` | yes |
| S026 | 36 | `mined` | `corpus/knowledge/provenance-recording-r85.md` | yes |
| S031 | 41 | `mined` | `corpus/knowledge/provenance-recording-r85.md` | yes |

Repo-wide, each of the six is cited by exactly one knowledge entry — the same entry its `used-by` names
(`grep -rlE '\bS214\b' corpus/knowledge/` and siblings, receipt 03), so the `used-by` cells are neither stale nor
over-broad.

One edge worth naming, not a drift: `S031`'s `teaches` cell opens `` supersedes S024 — `` and `S024` is `queued`
with `used-by —`. `S024` is the row the r85 entry must *not* cite (round-86 K4), and `S024`'s own capture-based
`teaches` still names `publication,modification` terms the live row refuses — that is the known, disclosed
round-86 state (`corpus/evidence/round91/curation-r91.py` prints `TEACHES_FLAGGED S024 terms=publication,modification
disposition=superseded by S031`, `TEACHES_UNRESOLVED=0`). It is not round-91 drift.

Each of the six has its capture on disk, and the capture key is derivable from the row's own URL by
`sha256(url)[:24]` — S214 `a640b15abf781e5c583d7088`, S018 `248b43277f376e437a356909`, S023
`f5545a194c06ab421875b047`, S215 `6e48bcc4a04d13b7b3ebb68e`, S026 `67983a3dbbd1d690aa648744`, S031
`11d6cc56bb24adfc61eea2b4`. Both `.raw` and `.txt` exist for all six.

---

## 4. The surfaces C2 reads

Counted with `curation-r91.py`'s own parsing (`section_lines` → `data_lines` → `table_rows(width)`), on the C3
clone, so the numbers are the instrument's numbers, not a re-derivation:

- **`## Located quotes` data rows = 20** (13 in `search-transparency-reporting-r84.md`, 7 in
  `provenance-recording-r85.md`). Matches C2's `Q_ROWS=20`.
- **decision rows (width 4) = 17** (11 + 6). Matches C2's `TFREQ_OK=17/17` and `WARRANT_OK=17/17`.
- **capture files that resolve each quote: all 20 resolve; 0 absent.** Every quote's `source` id maps to an
  existing `.txt` capture through the registry URL, and every quote's text is present in that capture
  (`LOCATED` for all 20; `rows whose capture file is ABSENT = 0`, `rows whose quote is not in the capture = 0`).

Corroboration by running the frozen counter on the C3 clone (read-only, `--root .`):

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0
SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,
provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0
TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS_MEASURED=13/13
VERDICT fields_hold=1 legs_ok=13/13 DETECTOR_WITNESS=11/11
CURATION_R91=PASS
exit=0
```

**No row's capture is absent; no surface drift.** (Note: `QUOTES_LOCATED=20/20` requires the tool's
quote-stripping — `raw_quote.strip().strip('"')` — before the substring test; the raw cell text carries the
surrounding quotation marks and does not locate without that strip. I applied the same strip in my own
re-derivation.)

---

## 5. Registry census

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

**Exit code 0.** Five `W04` warnings, all pre-existing duplicate-URL warnings, and an `ok` line for the lane.

**Row count.** The seat's literal command
`grep -cE '^ (0, 3)\|[[:space:]]*S[0-9](3,)' corpus/SOURCES.md` prints **0** with exit 1 — that ERE matches no
registry row shape (rows are `| S### | …`), so it is not a usable counter here; I record its output verbatim and
give the real count beside it. Two independent counters agree:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin | grep -i chousa
chousa	rows	219
chousa	tier.A	140   chousa	tier.B	59   chousa	tier.C	20
chousa	status.mined	183   chousa	status.queued	12   chousa	status.rejected	24
$ grep -cE '^ *\| S[0-9]{3,} \|' corpus/SOURCES.md
219
```

**219 registry rows**, unchanged from base (the census's own start and end receipts for this round both print the
same five W04s and exit 0; `corpus/SOURCES.md` in the lane working tree is byte-identical to the C3 blob,
sha256 `7a2f6d53fe47ac9dc8c8931f8e21619862f0b919ecea0cd387e7f92544f5c1c1` both sides — so the census result
transfers to C3 unchanged). The registry count matches the round's lesson claim "Registry 219 → 219 rows".

---

## Findings summary

| # | finding | surface | severity |
|---|---|---|---|
| F1 | C1's source quote `"Print or check SHA256 (256-bit) checksums."` is a *rendered* form; the source bytes carry the roff escape `256\-bit`, so `grep -cF` of the printed quote at the named location returns 0 (the escaped form returns 1). `corpus/evidence/round91/claims.md:33`; `corpus/SOURCES.md:80` `teaches`. | C1 source | citation precision (the grounding sentence is real; the quote is not a literal substring) |
| F2 | `corpus/lessons/round-91.md:18` says the quote is "(7 words)"; `wc -w` = **6** on both the rendered form and the raw roff line. | lesson | documentation mis-count (the quantity QUALITY 154/154's word-count check computes) |
| F3 | The `refetch.tsv` row `S221 … 28 000 - -` that `plans/round-91.md:33` and `corpus/lessons/round-91.md:26` cite is **not committed** at F3 or C3 — it exists only as an uncommitted working-tree edit of `corpus/evidence/round57/refetch.tsv`. | plan + lesson | citation precision (the attempt is real and the row's bytes match the description) |
| F4 | The round re-opened S070 but recorded no `GATE-RECORD` line for it (the lesson carries only the S001 rev record) and named no schema gap for the missing form; all three forms are impossible for S070 (probed: `url/admit` PARSE-fails — no URL/capture; `rev` fails `LINE,REV` — the man page is not a repo blob). QUALITY 173 requires a record *or* a named gap. | lesson `## Gate` | QUALITY 173 completeness |
| F5 | S070's `used-by` names only two knowledge entries and no round-91 claims file, while the lane's precedent rows (S166–S179, S216, S218, S220) do name their citing claims file; S073's `used-by` names `corpus/knowledge/receipt-binding-r38.md` only. | registry | weak drift, and the precedent is not uniform: S023, S031 and S215 are each cited by an earlier claims file (`corpus/evidence/round86/claims.md`, `round88/claims.md`) whose path is likewise absent from their `used-by`, so "a claims-file citation must appear in `used-by`" is not a uniform lane rule. Recorded, not asserted as a defect. |
| — | **No drift found** on: S070's recorded sha256 (full match), S070's anchor spans (4–11, 19–20, 54–56), the six routed sources' `status`/`used-by` (12/12 correct), C2's surface counts (20 quote rows, 17 decision rows, 20/20 captures resolve and locate), the registry row count (219), the census exit (0), the `| S221 |` absence (0), and the absence of a capture key for the attempted URL. | | |

**What I did not run** (out of seat scope, or not required): the six C1 receipts/forgeries, the C2 controls
battery, the C3 tally/controls, and the fresh `bash tools/research-gate.sh --selftest` (~6 min) — none of those
items name this seat. I ran `curation-r91.py --root .` on the clone once, read-only, as corroboration for item 4;
I did not run the C2 controls battery and make no claim about it.

**Unresolved gaps for the integrator.**

1. F3 (the uncommitted `refetch.tsv` row) — the round's documentation cites a receipt that is not in the frozen
   tree; it lands with the landing commit. Nothing for me to fix; flagging for the L1's landing decision.
2. F4 (the missing S070 `GATE-RECORD` / unnamed schema gap) — the lesson is uncommitted and can still be amended
   to name the gap, the way round 86's lesson names its own gap for `S217`
   (`corpus/lessons/round-86.md:31`).
3. F1/F2 (quote form and word count) — a lesson/claim wording fix, or a decision that the rendered form is the
   lane's convention for man pages. I did not assume either; I measured and reported.

---

VERDICT: R91ScoutRegistry C1 fired — S070's premise re-opens byte-exact (recorded sha256 and anchor spans match the installed page) but the claim's own source quote is the rendered roff form rather than a literal substring of the source bytes, the lesson miscounts its words (6, not 7), and the re-open carries neither a GATE-RECORD line nor a named schema gap (QUALITY 173) — a citation-precision finding on this seat's surfaces, not a kill-rule firing (this seat did not run the C1 driver or its battery).
VERDICT: R91ScoutRegistry C2 held — all six routed sources are `mined` with `used-by` naming their citing entry, C2's read surfaces are exactly 20 located-quote rows and 17 decision rows, all 20 quotes resolve to an on-disk capture and locate in it, and the frozen counter prints CURATION_R91=PASS with Q_ROWS=20 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 on the C3 clone.
VERDICT: R91ScoutRegistry C3 n/a — this seat touched only the registry and corpus surfaces the claims read; the case-range, tally and selftest surfaces were outside its scope and were not exercised.

# R86RevSupply — append-only forensics on the round-86 registry edit

Seat `R86RevSupply`, lane chousa round 86 (L1 `ChousaR86`). Leaf seat: no subagents, no network, no
production edits, no git mutation. Every check reads committed bytes via `git show` / `git archive`.
No tool was installed or upgraded; scratch lived at `/fast/scratch/hyaku/chousa-r86/R86RevSupply/` and was
deleted before yield. Output: this file plus `.ufo/waves/round-86/w1/R86RevSupply/` (scripts and `receipts/`).

## Revisions and the one registry commit

| label | commit | `corpus/SOURCES.md` blob |
|---|---|---|
| base (round-85 tip + spot-check) | `3bfb6885958ad4a674ad1896f70d1e836be609e4` | `2c6b06bdd1a1618794b6560da2de073cb9cd57ad` |
| egress table | `e446875260a11e3489a0d78344d71d7fbb006a42` | `2c6b06bdd1a1618794b6560da2de073cb9cd57ad` |
| freeze | `d0b1bd06872cdf0eeb03eccd099ff69ae6704307` | `2c6b06bdd1a1618794b6560da2de073cb9cd57ad` |
| landing (attacked bytes) | `667a5d091dc46168ed95eda0ae7f19a9bcf139a2` | `266bb540a73372933cb33cc4e1cc582c2650ffd6` |
| round-84 verifier spot-check | `43c3f7284eee4889cdcc6ac1626573f6579cd533` | `a9fbac08cb6d5308db246a5244c9830f6d050303` |
| round-85 prefreeze | `5d0b94139ae8baf60d6f630715bc495f0a93b448` | `a9fbac08cb6d5308db246a5244c9830f6d050303` |
| S024 row origin (round-25) | `0fc037e6` | `5aa3160388ec2eb686e34ea14d4ba9312c802720` |
| round-85 in-place edit | `02df67db` | `2c6b06bdd1a1618794b6560da2de073cb9cd57ad` |

`corpus/SOURCES.md` is byte-identical at base, egress and freeze (`2c6b06bd`), so the registry edit exists
only in the landing commit: `git -C <lane> log --oneline --reverse 3bfb6885..667a5d09 -- corpus/SOURCES.md`
prints exactly `667a5d09 round-86: landing — S216/S217 rows, S031 mined / S024 restored, …` (exit 0,
receipt `receipts/sources-log-base-to-landing.txt`).

## (1) Cell-level diff, base → landing, every changed cell

Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff 3bfb6885958ad4a674ad1896f70d1e836be609e4 667a5d091dc46168ed95eda0ae7f19a9bcf139a2 -- corpus/SOURCES.md`
→ exit 0, two hunks, `4 2 corpus/SOURCES.md` from `--numstat` (receipts `01-sources-diff.txt`,
`01b-sources-numstat.txt`). Machine table: `receipts/03-cell-diff.tsv` (exit 0, 29 changed cells across 4 rows;
original: `.ufo/waves/round-86/w1/R86RevSupply/sources-cell-diff.py`).

Columns are the 11 registry fields (`id … used-by`). `RESTORATION` = the landing bytes equal the row's bytes
before the round-85 in-place edit (see §2); `ALLOWED` = one of the three cells `CORPUS.md` rule 2 lets change in
place (`status`, `recheck`, `used-by`); `OUTSIDE_RULE2` = a pre-existing row changed in a cell rule 2 freezes.

| row | column | old value (base) | new value (landing) | class |
|---|---|---|---|---|
| S024 | anchor | `lastReviewed property definition paragraph (capture key 11d6cc56bb24adfc61eea2b4)` | `page heading lastReviewed, definition paragraph` | RESTORATION |
| S024 | status | `mined` | `queued` | ALLOWED |
| S024 | opened | `2026-11-08` | `2026-10-21` | RESTORATION (the expected `opened` restoration) |
| S024 | used-by | `corpus/knowledge/provenance-recording-r85.md` | `—` | ALLOWED |
| S031 | anchor | `lastReviewed property definition paragraph; Schema.org page served 2026-10-21` | `lastReviewed property definition paragraph; page re-opened 2026-11-08 (capture \`11d6cc56bb24adfc61eea2b4\`, \`Date on which the content on this web page was last reviewed for accuracy and/or completeness.\`)` | **OUTSIDE_RULE2 — new edit, named F1** |
| S031 | status | `queued` | `mined` | ALLOWED |
| S031 | used-by | `—` | `corpus/knowledge/provenance-recording-r85.md` | ALLOWED |
| S216 | all 11 cells | `<absent>` | `S216` · `RFC 9110, HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.html` · `spec` · `A` · `the status-code registry's own definition of 203 Non-Authoritative Information and of 200 OK; not a capture-store policy` · `section 15.3.4, first paragraph of 203 Non-Authoritative Information (capture key b1b13a12aee75c6ecc20fb91)` · `203 means a transforming proxy modified the enclosed content from the origin server's 200 response, so a 203 body is not the origin's representation` · `mined` · `2026-11-08` · `365d` · `corpus/evidence/round86/claims.md` | ADDED_ROW (appended, line 229) |
| S217 | all 11 cells | `<absent>` | `S217` · `DCMI Namespace Policy — https://www.dublincore.org/documents/dcmi-namespace/` · `spec` · `A` · `how DCMI says it maintains and supersedes terms in its namespaces` · `—` · `REJECTED: the registered URL redirects to /specifications/dublin-core/dcmi-namespace/ and both served a 9-line stub with no policy prose, so no quotable sentence grounds a row; flip: re-open when that page or a mirrored policy document serves the supersession prose and a clause can be quoted` · `rejected` · `2026-11-08` · `on-release` · `—` | ADDED_ROW (appended, line 230) |

Unchanged in both pre-existing rows: `source`, `kind`, `tier`, `scope`, `teaches`, `recheck` (and for S024 also
nothing else). No `recheck` cell changed anywhere in the file.

**Named changes outside `status`/`recheck`/`used-by` in pre-existing rows (as the seat requires):**

1. **S024 `opened`** — restoration, not a new edit: `2026-10-21` is the value the row carried at its origin
   `0fc037e6` and at `43c3f728`/`5d0b9413`; round 85 (`02df67db`) had changed it to `2026-11-08`.
2. **S024 `anchor`** — restoration for the same reason (byte-identical row at the same three revisions, §2).
3. **S031 `anchor`** — **not** a restoration: no earlier revision carries the new value; this is a new in-place
   edit made by the landing commit in a cell `CORPUS.md` rule 2 freezes (finding F1).

## (2) S024 row bytes: landing == `43c3f728` == an earlier revision

Command (receipts `02-s024-sha256.tsv`, `02b-sources-blob-ids.txt`, `02c-s024-cmp.txt`,
`02d-s024-cmp-origin.txt`, `02e-s024-origin-add.txt`; all exit 0 unless stated):

```sh
for r in 0fc037e6 43c3f7284eee4889cdcc6ac1626573f6579cd533 5d0b94139ae8baf60d6f630715bc495f0a93b448 667a5d091dc46168ed95eda0ae7f19a9bcf139a2; do
  printf '%s ' "$r"; git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show "$r:corpus/SOURCES.md" | grep '^| S024 |' | sha256sum
done
cmp <(git show 43c3f728:corpus/SOURCES.md | grep '^| S024 |') <(git show 667a5d09:corpus/SOURCES.md | grep '^| S024 |')
cmp <(git show 0fc037e6:corpus/SOURCES.md | grep '^| S024 |') <(git show 667a5d09:corpus/SOURCES.md | grep '^| S024 |')
```

Observed: all four revisions print
`17ad12a15f6c8ab206166545b71124bdaa05b373b099ccb2a229ce303d4bf01a  -` (336 bytes), and both `cmp` calls print
nothing with `cmp` exit 0 (`IDENTICAL-43c3f728-vs-landing`, `IDENTICAL-0fc037e6-vs-landing`, `cmp_exit=0`).
Cited earlier revisions:

- **`43c3f7284eee4889cdcc6ac1626573f6579cd533`** (round-84 verifier spot-check) — whole-file blob
  `a9fbac08cb6d5308db246a5244c9830f6d050303`.
- **`0fc037e6`** (round-25, the commit that introduced the row) — the row's parent `0fc037e6^` has **no** S024
  row (`grep -c` prints `0`, grep exit 1) and `0fc037e6` adds exactly one (`grep -c` prints `1`, grep exit 0);
  `git merge-base --is-ancestor 0fc037e6 3bfb6885` exits 0, so this is an earlier revision on the base's
  ancestry, not a side branch.
- Third witness: **`5d0b94139ae8baf60d6f630715bc495f0a93b448`** (round-85 prefreeze) carries the same
  whole-file blob `a9fbac08…`; it is a distinct commit from `43c3f728` (its parent) with identical bytes.

**What round 85 changed and landing reversed.** `git diff 5d0b9413 02df67db -- corpus/SOURCES.md`
(receipt `07-r85-inplace-edit.diff`, exit 0) shows the round-85 in-place edit at `02df67db` changing exactly the
four S024 cells above in the opposite direction (`anchor` gains the capture key, `status queued→mined`,
`opened 2026-10-21→2026-11-08`, `used-by —→corpus/knowledge/provenance-recording-r85.md`), and appending S215.
The landing restores all four S024 cells, so the net S024 effect base→landing is the exact inverse of
`02df67db`. Whole-file blob: base/egress/freeze `2c6b06bd`, landing `266bb540`, pre-edit `a9fbac08`.

## (3) Four rows, 11 columns; opened dates vs `fetched_utc` vs the egress commit's order

Commands and receipts: `python3 -B .ufo/waves/round-86/w1/R86RevSupply/registry-check.py --repo <lane>
--rev 667a5d09… --ids S216,S217,S024,S031` → exit 0 (`receipts/03b-registry-check-landing.txt`,
`03c-registry-check-base.txt`); `refetch-order.py --base … --landing … --egress e4468752…` → exit 0
(`receipts/04-refetch-egress-order.txt`); `capture-integrity.py --base … --landing …` → exit 0
(`receipts/05-capture-integrity.txt`); documented census on an extracted landing tree → exit 0
(`receipts/14-census-landing.txt`; tree built with
`git -C <lane> archive 667a5d091dc46168ed95eda0ae7f19a9bcf139a2 | tar -x -C $S`, then
`bash .ufo/waves/round-86/w1/R86RevSupply/census-landing.sh $S`).

**11 columns.** `S024 11`, `S031 11`, `S216 11`, `S217 11`; whole file
`ROWS=217 MALFORMED=0 DUPES=0 ENUM_BAD=0`, tiers `A=138 B=59 C=20`, statuses `mined=181 queued=12 rejected=24`.
The documented census independently prints `rows: 217`, `malformed: 0`, empty dupes / enum / missing-used-by
lines. Both new `used-by` paths (`corpus/evidence/round86/claims.md`, `corpus/knowledge/provenance-recording-r85.md`)
exist at the landing revision.

**Opened dates.** S216 and S217 `opened=2026-11-08`; the four added refetch rows carry
`fetched_utc=2026-11-08T06:00:10Z` (S216, S217, S031) and `2026-11-08T06:00:11Z` (S023). The date agrees.

**Egress order.** The egress commit `e4468752` has author time `2026-11-08T02:55:55-03:00` and committer time
`2026-11-08T03:00:03-03:00` = **`2026-11-08T06:00:03Z`** (epoch 1794117603). Every added fetch is after it:
`+7 s` (S216, S217, S031) and `+8 s` (S023). `EGRESS_BEFORE_ALL_ADDED_FETCHES=1/1 SCOPE_MATCH=4/4
REFETCH_ORDER=PASS`, exit 0. The added URL set and the egress table's intended-target URL set are equal in both
directions (`ADDED_URLS_NOT_INTENDED=[]`, `INTENDED_URLS_NOT_FETCHED=[]`), and the attempts are `1,1,1,3` —
S023's re-open is the third and last attempt allowed by `tools/capture-fetch.py` `MAX_ATTEMPTS = 3` (line 64;
refusal at lines 208–209). The landing commit's committer time, `2026-11-08T03:06:26-03:00` = `06:06:26Z`, is
after the last fetch (`receipts/13-attempts-and-landing-time.txt`).

**Capture integrity.** `CAPTURE_INTEGRITY=PASS`, exit 0: for all four added rows `key == sha256(url)[:24]`, and
the committed `.raw`/`.txt` sha256 equal the row's `raw_sha256`/`txt_sha256`. S216 capture:
raw 1,187,554 B / 19,014 lines, txt 485,289 B / 21,414 lines; its 19-word Gate quote is verbatim
(whitespace-normalized) at txt **lines 12267–12269**, inside the §15.3.4 body (heading line 12261, first
paragraph 12266–12273). S031 capture: raw 11,063 B / 330 lines, txt 1,193 B / 313 lines; its 16-word quote is
verbatim at txt **line 211**. S217 capture: raw 392 B / **9 lines**, txt 88 B / **9 lines**; the raw body is a
meta-refresh page whose canonical/refresh target is
`https://www.dublincore.org/specifications/dublin-core/dcmi-namespace/`.

**Supersession edges (registry side).** `supersession-edges.py` lists 10 `supersedes` edges. At base:
`INVERSIONS=1 [('S031', 'S024')]` (S031 `queued`, S024 `mined`); at landing: `INVERSIONS=0 []`
(S031 `mined`, S024 `queued`). The other nine edges are not the live-vs-unadopted form (e.g. S029/S019 and
S033/S020 are superseding-mined/superseded-queued; S073/S176/S200/S201 are both-mined). Receipts
`10a-supersession-edges-base.txt`, `10b-supersession-edges-landing.txt`, both exit 0.

**Registry side of C2 K4.** `corpus/knowledge/provenance-recording-r85.md` at base contains `S024` 3× and `S031`
0×; at landing `S024` 0× and `S031` 3× (grep counts with exits `S024_base_exit=0`, `S031_base_exit=1`,
`S024_land_exit=1`, `S031_land_exit=0`; receipt `08-r85-entry-citations.txt`), and it opens
`source: S215, S026, S031`. S023's Definition line is at capture `f5545a194c06ab421875b047.txt` line 8786 in
both base and landing: ` Date on which the resource was changed. $` (receipt `09-s023-line8786.txt`, pipeline
exit 0).

## (4) Any other row whose bytes changed: none

`python3 -B .ufo/waves/round-86/w1/R86RevSupply/line-diff-assert.py --repo <lane> 3bfb6885… 667a5d09…` → exit 0,
`OPCODES=3 EXPECTED=3 MATCH=True` (receipt `06b-line-diff-assert.txt`): `replace` old line 34 (S024),
`replace` old line 41 (S031), `insert` at old line 229 (S216+S217). No deletion, no reordering; the row count
goes 215 → 217 and every other row's bytes are identical. `git diff -U0` (receipt `06-sources-diff-U0.txt`) and
`--numstat` `4 2` agree.

## Findings (each with command, receipt, observed line, exit)

- **F1 — `CORPUS.md` rule 2 violation in place: S031 `anchor`.** Rule 2 (`/home/vgpnk/Projects/shokunin/CORPUS.md`
  line 116: "Only `status`, `recheck` and `used-by` change in place") freezes `anchor`; the landing changed it
  (`old` → `new` in the table above) and no earlier revision carries the new value. The round lesson discloses
  the change in prose but logs no old→new for that cell. The rule-2-compliant alternatives did not exist for a
  re-open: `opened`/`anchor` are both frozen and no column is defined for a re-open date, so this is also a
  contract gap (`[INFERENCE]`: the round encoded the re-open in the only text cell that could carry it; the
  registry has no compliant way to record a re-open of a queued row).
  Command: cell diff command in §1. Receipt: `receipts/03-cell-diff.tsv`. Observed: `S031 CELL_CHANGED anchor
  …`; exit 0.
- **F2 — S217 `teaches` asserts an uncommitted fetch.** The cell says "the registered URL redirects to
  `/specifications/dublin-core/dcmi-namespace/` **and both served a 9-line stub**", but committed bytes exist
  only for `https://www.dublincore.org/documents/dcmi-namespace/` (the meta-refresh stub). The redirect-target
  key `175b6981c851ee27413b2e24` = `sha256(target)[:24]` has **no** committed capture and there is **no**
  `refetch.tsv` row for it; the egress table lists only the `/documents/` URL, and a fetch of the target would
  have been out of scope. The rejection verdict is unaffected (the one committed body is already unquotable),
  but half of the stated reason is unverified, and the round lesson repeats it. Command:
  `capture-integrity.py` (§3). Receipt: `receipts/05-capture-integrity.txt`. Observed:
  `QUOTE S216 … found=True …`, `S217_REDIRECT_TARGET=… key=175b6981c851ee27413b2e24 committed_captures=[]`;
  exit 0.
- **F3 — S217 is the only row with `anchor` = `—`.** `CORPUS.md` line 99 requires the anchor to be an exact
  section/heading/page/line plus revision and never a bare homepage; it does not define `—` for the anchor cell
  (unlike `used-by`, where `—` is specified). For a stub body there is no location to name, so the value is a
  convention extension, not a contract value. Command/observed: the landing census awk in
  `receipts/12-anchor-dash-and-lesson.txt` prints `anchor-dash rows: S217`; exit 0.
- **F4 — lesson statement contradicts the committed captures (S023).** `corpus/lessons/round-86.md` line 27 says
  the S023 re-fetch "produced different bytes (txt sha `20dc0c3ab772…`, previously `f5545a19…` stored under the
  same key)". Observed: `f5545a194c06ab421875b047` is the capture **key** = `sha256(url)[:24]`, not a content
  sha; the committed S023 raw blob is `d7f1419d…` (`sha256 fb32e12f…`) and the txt sha is `20dc0c3a…` at
  `3a17f4da` (round-84), at base and at landing — the re-fetch produced **identical** bytes, and line 8786
  already held the `modified` Definition at base. The S023 row itself is unchanged, and the line number holds.
  Command: §3 receipt 11. Receipt: `receipts/11-s023-capture-identity.txt`. Observed:
  `3bfb6885… raw_sha=fb32e12fa9bee137…`, `667a5d09… raw_sha=fb32e12fa9bee137…`,
  `line8786@base= Date on which the resource was changed.`; exit 0.
- **F5 — S024 restoration log is incomplete.** The lesson logs `status`, `used-by` and `opened` old→new for
  S024 but not the `anchor` cell it also changed (restored). Rule 2 requires each in-place change to be logged
  old→new. The restoration itself is complete and provable (§2); only its disclosure is partial.
  Command: §1 cell diff; receipt `receipts/03-cell-diff.tsv`; observed S024 anchor line; exit 0.

No other row's bytes moved; no deletion; no column-count, duplicate-id, enum or missing-`used-by` defect; the
capture keys and hashes for the four fetched rows all verify; the egress commit precedes every round-86 fetch by
7–8 s and the fetched URL set equals the approved set exactly.

## Verdicts

VERDICT: R86RevSupply C2 held — every registry-side property I was assigned holds at 667a5d09 (S024→S031 inversion 1→0, S024 restored byte-identically at 0fc037e6/43c3f728/5d0b9413/landing, four rows parse as 11 columns, egress precedes all four fetches by 7–8 s with scope 4/4, no other row changed), with one named rule-2 deviation (S031 `anchor`), one ungrounded cell sub-claim (S217 "both served a 9-line stub"), and one inaccurate lesson sentence (S023 "different bytes"); the counter predicate itself was not run by this seat.
VERDICT: R86RevSupply C1 n/a — this seat did not run the operability battery; it verified only S216's registry bytes (11 cells, capture key/hash, quote verbatim at §15.3.4 lines 12267–12269), which hold.

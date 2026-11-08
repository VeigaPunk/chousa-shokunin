# R86ScribeLesson — round-86 lesson and criteria vs committed bytes (report-contract conformance leg)

Root `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Revisions: base `3bfb6885958ad4a674ad1896f70d1e836be609e4`
(round-85 tip + non-author spot-check), egress table `e446875260a11e3489a0d78344d71d7fbb006a42` (committed
2026-11-08T03:00:03-03:00, before the first 06:00:10Z fetch), claim freeze `d0b1bd06872cdf0eeb03eccd099ff69ae6704307`,
landed bytes under attack `667a5d091dc46168ed95eda0ae7f19a9bcf139a2`. Lesson under test:
`corpus/lessons/round-86.md` (blob `c79c4deba4f5c16047969b3e6d339d59d5dab8c5` at the landing);
`corpus/lessons/round-85.md` (blob `be4a746936e8a626728855b1365daf3bb19cd012` at both base and landing).

Every tree is `git -C <lane> archive <rev> | tar -x -C <scratch>/tree`; the scratch root is
`/fast/scratch/hyaku/chousa-r86/R86ScribeLesson/` and is deleted before this yield. No network fetch was made (a GET
would be a finding this round; none was attempted). No lane/fleet git mutation, no commit, no push, no production
edit, no file written outside `.ufo/waves/round-86/w1/R86ScribeLesson.md` and
`.ufo/waves/round-86/w1/R86ScribeLesson/`. No tool was installed or upgraded (no pacman transaction, no `uv tool
install`, no binary dropped on `PATH`), so there is nothing to record on the tooling directive.

## Verdict summary

| item | verdict |
|---|---|
| (1) `gate-records.py verify` on the round-86 lesson at the landing tree | **pass** — 2 records, 2 OK, 0 fail, exit 0 |
| (2) the lesson's "no record form for a 200-refused row" claim | **false as written** (F1) — the tool has **three** forms, one of which records the S217 decision today |
| (3) `## Claim outcomes` "verified" retraction | **pass** — round-85 file unedited, retraction filed in round-86; one residual stale assertion noted (F5) |
| (4) QUALITY 173–176 cited artifacts | 173 **fails its own Check** (F2, F4); 174's cited artifact **does not say what the criterion claims** (F3); 175, 176 **pass** |
| (5) Gate section: access date, URL, ≤25-word located quote for S216; S217 rejection reason | **pass** for S216/S217 (F6 = an adjacent gap on S023) |

---

## (1) The seat's counting command

```sh
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/gate-records.py verify \
  --root <tree at 667a5d091dc46168ed95eda0ae7f19a9bcf139a2> \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin \
  <tree>/corpus/lessons/round-86.md
```

Observed (receipt `01-verify-round86-lesson.txt`):

```
GATE_RECORD <tree>/corpus/lessons/round-86.md:12 S216 OK
GATE_RECORD <tree>/corpus/lessons/round-86.md:13 S031 OK
GATE_RECORDS files=1 records=2 ok=2 fail=0
```

**Exit code 0.** Summary line: `GATE_RECORDS files=1 records=2 ok=2 fail=0`. Two records, both OK. The tool bytes used
are the committed ones (`sha256 fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287`, identical in the
landing tree and in the lane working copy, and identical to the `instrument-pins.txt` pin). The same tool also verifies
`corpus/lessons/round-84.md` (3 OK) and `corpus/lessons/round-85.md` (3 OK) against the landing tree — receipts 15 and
11.

## (2) The lesson's schema-gap claim (Mistakes item 1) against the tool's own bytes

The lesson (`corpus/lessons/round-86.md` lines 63–69) says:

> `tools/gate-records.py` has **only two record forms** — `url/admit` (success + capture + quote) and `url/unreach`
> (failure) — so a *successful fetch refused on content* has **no record form** and **any GATE-RECORD line for it would
> fail `REFETCH`**. … **Fix:** … a `decision=reject` admit form over a committed capture, **expecting no REFETCH refusal**.

**F1 — the claim is false on the committed bytes.** Receipts `02-tool-forms.txt`, `12-record-forms-probed.txt`,
`13-reject-over-capture-claim.txt`, `14-s217-three-shapes.txt`.

The tool's docstring (lines 17–25) and its code name **three** forms, not two:

```
  url/admit   GATE-RECORD S<id> url=… fetched=… tier=… decision=<admit|reject>
              capture=corpus/captures/<24 hex>.txt capture_sha256=… words=<n> quote="<text>"
  url/unreach GATE-RECORD S<id> url=… fetched=… tier=… decision=reject capture=none curl_rc=<n>
              http=<nnn> words=0 quote=none
  rev         GATE-RECORD S<id> rev=<40 hex> path=<repo-relative path> line=<n> words=<n> quote=<text to end of line>
```

`tools/gate-records.py:87-89` — `URL_ADMIT`, `URL_UNREACH`, `REV_KEYS`; `parse()` branches on all three
(`:131-145`).

What the tool actually refuses, probed with the committed tool against the landing tree:

| shape for S217 (HTTP 200, `curl_rc=0`, `txt_sha256` == capture sha) | observed | exit |
|---|---|---|
| **A** `url/admit` with `decision=reject` over the capture | `GATE_RECORD … S217 FAIL PARSE` | 1 |
| **B** `url/unreach` over the same 200 (`curl_rc=0 http=200`) | `GATE_RECORD … S217 FAIL REFETCH` | 1 |
| **C** `rev` form naming S217 (`rev=667a5d0… path=corpus/SOURCES.md line=230 quote=REJECTED: …`) | `GATE_RECORD … S217 OK` | **0** |
| **D** `url/admit` with `decision=admit` over the stub capture | `GATE_RECORD … S217 OK` | 0 |
| **E** `url/unreach` over a *203* fetch (the peer seat's `c03-reject-success-203.md` line) | `GATE_RECORD … S021 OK` | 0 |

So, precisely:

1. **A is rejected at PARSE, not REFETCH.** The single guard is `tools/gate-records.py:148` —
   `if form == "admit" and kv["decision"] != "admit": return None`. The docstring at line 19 already advertises the
   admit form as `decision=<admit|reject>`; the code contradicts its own documentation with that one line.
2. **B fails REFETCH for the reason the tool states** — `check()` computes `success = kv["curl_rc"] == "0" and
   kv["http"] == "200"` (`:249`) and the unreach leg demands `not success` (`:250`), so a 200 can never be recorded as
   an unreach. This part of the lesson is right.
3. **The lesson's "no record form … is possible" is refuted by shape C.** A `rev`-form GATE-RECORD line naming S217 —
   quoting the registry row that carries the rejection — verifies **OK, exit 0** against the committed tool. A
   GATE-RECORD line for S217 is possible today, without any repair to the tool.
4. **The lesson's "expecting no REFETCH refusal" for a `decision=reject` admit form is already true.** With a scratch
   copy of the tool whose only change is widening `:148` to accept `decision="reject"`, a reject-over-capture record
   for S217 verifies **OK, exit 0** (receipt 14b): S217's refetch row is `http=200`, `curl_rc=0`, `txt_sha256` equal to
   the capture sha, so the admit REFETCH leg (`:238`) passes. The routed "missing form" is therefore one parse guard,
   not a new form.

Net: the *narrow* point survives — the tool cannot express "fetched OK, refused on content" in a **fetch-bearing**
record (the `url/admit` form demands `decision=admit`; the `url/unreach` form demands a non-200). The *stated* grounds
do not: the tool models three forms, one of which (the `rev` form) already records this round's decision, and the
proposed repair needs no new REFETCH behaviour at all. QUALITY 173 repeats the same misstatement (see F2).

## (3) The `## Corrections` / retraction leg

**Pass** (receipt `04-corrections-retraction.txt`, `11-corrections-sweep-round85-assertions.txt`).

- `corpus/lessons/round-85.md` **still prints "verified"** for both claims — lines 46–47, `| … | **verified** (measured
  at the landing revision) |` and `| … | **verified** (counter) |`.
- The round-85 file was **not edited**: `git rev-parse 3bfb6885:corpus/lessons/round-85.md` and
  `git rev-parse 667a5d0:corpus/lessons/round-85.md` are both `be4a746936e8a626728855b1365daf3bb19cd012`; the
  `git diff --stat 3bfb6885 667a5d0 -- corpus/lessons/round-85.md` is empty. (Its own `## Corrections` blocks, lines 88
  and 105, are also unedited and do not retract the column — the retraction is filed in round 86, exactly as the
  round-85 spot-check's routed defect 4 asked.)
- The retraction is filed: `corpus/lessons/round-86.md` line 48, `## Corrections to round-85 records (routed defect 4)`,
  lines 50–52: "printed **"verified"** for C1 and C2 while the filed verdict was an honest stop. This entry retracts
  that column: **C1 and C2 of round 85 did not verify as stated**". The lesson states the append-only discipline
  ("the round-85 file is not edited"), and the bytes agree.
- The retraction's factual basis checks out against the round-85 non-author check: `corpus/lessons/
  round-85-verifier-spotcheck.md` `## Claim verdicts` reads "C1 — does not verify as stated (honest stop)" and "C2 —
  does not verify as stated (honest stop)".

**F5 — residual stale assertion in round-85.md that the round-86 retraction does not cover (beyond the literal
item).** `corpus/lessons/round-85.md` still asserts, at line 31, "`S024`: status `queued` → `mined`; anchor gains the
capture key `11d6cc56bb24adfc61eea2b4`; opened date 2026-10-21 kept", and its Gate block still carries
`GATE-RECORD S024 … decision=admit` (line 16) for a row the round-86 landing restored to `queued` with `used-by —`.
Those two lines are the round-85 inversion the round closed, and they now stand uncorrected in the file the gate
reads. The machine check cannot catch it: the tool's `check()` reads only the tier cell (`regrow[3]`, `:220`) and never
the status cell, so `round-85.md` still verifies 3 OK / exit 0 against the landing tree (receipt 11f). The round-86
`## Corrections` block sweeps the claim-outcomes column but not these two mentions, while the lesson's own lesson-learned
note (round-85 `## Mistakes` item 1) makes a sweep-the-every-mention claim. Not a C1/C2 predicate question; a
corrections-sweep gap on the same defect class the round set out to close.

## (4) QUALITY 173–176 — each cited artifact, checked against the artifact

The four criteria were added by the landing commit (`corpus/QUALITY.md` lines 1110–1116, diff base→landing = 10
inserted lines, receipt `05-quality-173-176.txt`).

**QUALITY 173 — fails.** Cited artifacts: the tool's record forms, and the S217 registry row.

*F2 — the criterion misstates the artifact it cites.* 173 says "`tools/gate-records.py` models **only** `url/admit`
(success + capture + quote) and `url/unreach` (failure)". The artifact's own docstring (`:17-25`) says "Every record must
parse into exactly one of **three** forms" and lists `url/admit`, `url/unreach` **and `rev`**; `parse()` implements
`REV_KEYS` (`:89`, `:153`). So the cited artifact does **not** say what the criterion claims, and the criterion's
operative sentence — "no `GATE-RECORD` line could be written for it" — is false (shape C above: exit 0). The registry
row part of the citation *is* correct: `corpus/SOURCES.md:230` carries the reason and the flip condition ("REJECTED:
… no quotable sentence grounds a row; flip: re-open when that page or a mirrored policy document serves the
supersession prose and a clause can be quoted").

*F4 — 173's own Check clause is not satisfied.* The clause: "every registry row the round touched is either recorded in
a `GATE-RECORD` line or the lesson names the schema gap that prevents one." The rows the round touched are S216, S217,
S031, S024, S023 (`git diff 3bfb6885 667a5d0 -- corpus/SOURCES.md`, receipt 08/16). S216 and S031 have lines in the
round-86 Gate block; S217 is covered by the named gap. **S023 has neither**: the round re-opened it this round
(`refetch.tsv` row 184, `2026-11-08T06:00:11Z`, HTTP 200) and the lesson's Gate block says "Fetches
`2026-11-08T06:00:10–11Z`, one `capture-fetch.py` GET each" — but no `GATE-RECORD` line anywhere carries that
timestamp (receipt 15c: only S216 and S031 do). The schema gap named in the lesson does not cover S023 either: S023's
fetch was a 200 that the round **admitted** (its `modified` Definition is the round's warrant), not a 200 refused on
content. And the record was available: an S023 admit line at `06:00:11Z` quoting "Date on which the resource was
changed." (the very quote the round used) verifies **OK, exit 0** against the committed tool (receipt 15d) — the
round-84 lesson's S023 line is for the earlier `02:16:27Z` attempt only. The lane's own convention for this is in
`corpus/lessons/round-85.md` ("One record per registry row opened or re-anchored this round"), which round 85 honoured
for its S024 re-open (line 16). Reading "touched" as "recorded anywhere in the lane's lessons" would excuse S023 via
round-84's line; reading it as "this round's fetch" does not. Either way the criterion's Check, as written, does not
test what it is meant to test.

**QUALITY 174 — the cited artifact does not say what the criterion claims.** Cited artifact:
`curation-r86.py`'s `SUPERSEDED_LIVE=0`. The counter exists and prints `SUPERSEDED_LIVE=0` at the landing tree
(`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20`, `CURATION_R86=PASS`, exit 0). But the
criterion's sentence is "A row that a later row supersedes is not the live citation while the superseding row is
unadopted", and the check it names does not witness that sentence:

* **F3a — the check passes while the defect is present.** With S024 flipped back to `mined` **and** re-credited to the
  same `corpus/knowledge/provenance-recording-r85.md` entry while S031 is `mined` (the round-85 inversion's
  live-citation half), the counter still prints `SUPERSEDED_LIVE=0 … QUOTES_LOCATED=20/20` / `CURATION_R86=PASS`,
  **exit 0** (receipt 10, P1). The counter's rule (`:93-99`) fires only when the superseded row is `mined` **and** the
  superseding row is not; once S031 is `mined`, S024 may be `mined` and credited to the same entry with no finding — even
  though the r85 entry's own `source:` line says `S031` and the registry would then credit both.
* **F3b — the relation is found by a case-sensitive literal, so the check can be switched off.** At the base tree the
  counter prints `SUPERSEDED_LIVE=1` (exit 1); changing only `supersedes S024 —` → `Supersedes S024 —` in S031's
  `teaches` cell makes it print `SUPERSEDED_LIVE=0` (receipt 10, P2 and the base-tree probe) — the row silently leaves
  the check's scope without any change in registry semantics. (`re.match(r"supersedes (S\d{3,}) —", teaches)`, `:96`.)

The criterion's other factual citations check out: at the base tree S024 was `mined` and S031 `queued` (receipt 08),
S031's `teaches` opens `supersedes S024 —` and refuses the comparison ("no comparison to other date properties
claimed"), and `CORPUS.md` rule 2 ("Only `status`, `recheck` and `used-by` change in place… A correction is a new row
whose `teaches` opens `supersedes S0NN —`") reads as cited (fleet root `CORPUS.md:116-118`, receipt 16a).

**QUALITY 175 — pass.** Cited artifact: `curation-r86.py`'s `UNENTAILED_TERM=0` "over the frozen term set". The counter
exists, prints `UNENTAILED_TERM=0` at the landing tree (exit 0), and its term set is literally `DEFECT_TERMS =
("modification", "modified")` with the check scoped per entry (`joined` is rebuilt per entry, `:126`) and per decision
cell (`cells[1] + cells[2]`), i.e. it implements "a located quote of the same entry" as the criterion says. The
criterion's supporting citations also verify: at the base tree `corpus/knowledge/search-transparency-reporting-r84.md`
row "Recording when a resource changed" read "record a modification without its date | Q10 (S023)" with Q10 = the
`Date` subproperty recommendation, and `corpus/knowledge/provenance-recording-r85.md` row "Recording when content was
last reviewed" read "… when only its modification date is known | Q7 (S024)" with Q7 = the `lastReviewed` definition;
S031's own `teaches` cell refuses the comparison. The landing commit repaired both cells (r84 row 9 now cites Q13 =
"Date on which the resource was changed."; r85 row 6's Never cell no longer mentions a modification date, and the r85
entry's `source:` line reads `S215, S026, S031`).

**QUALITY 176 — pass.** Cited artifacts, all present and saying what is claimed:

* the counter computes the mutant by rewriting the subject tool's `r[6] == "200"` to `r[6].startswith("2")` —
  `corpus/evidence/round86/gate-records-r86.py:287`, `src.replace('r[6] == "200"', 'r[6].startswith("2")')`;
* the subject tool really contains that literal — `tools/gate-records.py:238` (`r[6] == "200"`), the only occurrence;
* the mutant leg requires it to accept every positive and the class record — `:435-451` (`mut_pos_ok`,
  `mut_accepts_d1`), and prints `MUT17_NOT_RELAXED` when the mutant still refuses D1;
* `controls/receipts/c1-k0-donothing.txt` exists and prints `D1_REFUSED=0/1 MUT17_KILLED=0/1 … GATE_RECORDS_R86=FAIL`,
  exit 1 — exactly the Check the criterion names.

## (5) The Gate section

**Pass for what the item asks** (receipt `06-gate-section.txt`), with one adjacent gap (F6) and one false sentence in the
same block (F3c).

*S216.* The Gate block's line 12 carries the access date `fetched=2026-11-08T06:00:10Z` (matching `refetch.tsv` row
181 exactly: id S216, that URL, `curl_rc=0`, `http=200`, `txt_sha256` = the capture sha), the URL
`https://www.rfc-editor.org/rfc/rfc9110.html`, `tier=A` (matches `corpus/SOURCES.md:229`), the capture
`corpus/captures/b1b13a12aee75c6ecc20fb91.txt` with key = `sha256(url)[:24]` (recomputed: `b1b13a12aee75c6ecc20fb91`)
and `capture_sha256=ec14fa3499c2dfbc…` (prefix of the capture's sha256), and a **19-word** quote (≤25) that is located
verbatim in the capture at lines 12266–12269 (RFC 9110 §15.3.4, "…the enclosed content has been modified from that of
the origin server's 200 (OK) response by a transforming proxy"). The tool's own `QUOTE_ABSENT` check agrees (record OK).

*S217 rejection reason.* Named in the Gate block (lines 29–31): "the DCMI Namespace Policy URL redirects to
`/specifications/dublin-core/dcmi-namespace/` and both served a 9-line stub with no policy prose, so no ≤25-word quote
grounds a row. Reason and flip condition are in the registry row". The committed capture
`corpus/captures/52db06f9e0e2eaf35bbdb321.txt` is 9 lines of blank lines plus the redirect URL — consistent with the
"stub" description — and the registry row (`corpus/SOURCES.md:230`) carries the reason and the flip condition.

**F6 — the round-86 re-open of S023 has no GATE-RECORD line (adjacent to item 5).** The Gate block declares four
fetches at `06:00:10–11Z` (S216, S217, S031, S023) but writes two GATE-RECORD lines. S217 is excused by the named gap;
S023 is not (its 200 was admitted, and the gap is about a 200 refused on content). An S023 admit line at `06:00:11Z`
quoting the round's own warrant verifies OK against the committed tool (receipt 15d). See F4 — the same gap is
QUALITY 173's Check failing.

**F3c — the S023 bullet's byte-drift sentence is false against committed bytes** (receipt
`07-s023-byte-drift-and-record-gap.txt`). Lines 26–28 read: "The re-fetch of the same URL produced **different bytes**
(txt sha `20dc0c3ab772…`, previously `f5545a19…` stored under the same key), so the capture is the newer body and the
line number is the one measured on it." Committed bytes contradict every clause:

* all three `S023` refetch rows carry the **same** `txt_sha256` = `20dc0c3ab7724e1f4be59217c190fa796a66c29b7a653e8d707d64f5fac43a79`
  (`02:16:27Z`, `03:54:40Z`, `06:00:11Z`) — the body did **not** change;
* the capture file's content sha256 is `20dc0c3ab772…` at `3a17f4da` (round-84 land), at the base and at the landing —
  one commit in its whole history — so the capture is the **same** body, not a newer one;
* `f5545a19…` is the capture **key** = `sha256(url)[:24]`, not a text digest; **no capture file in the tree has a
  content sha starting `f5545a19`**. It cannot have been a previous "txt sha stored under the same key" — the key is
  derived from the URL, so it necessarily repeats.

The consequence is not cosmetic: the `modified` Definition ("Date on which the resource was changed.") sits at line
8786 of the capture **as committed at round 84**, so the round-84 entry could have cited it then; the re-fetch did not
locate anything new, and the lesson's narrative of why the round-84 warrant was missing is unsupported. C2's own K4
("the round-84 repair's added quote is not from S023") is unaffected — the added quote *is* from S023 and is located in
the S023 capture — so this is a false sentence in a filed lesson, not a claim failure.

---

## Further findings (outside the five items, same leg)

**F7 — the lesson has no `Check command` line.** `corpus/lessons/round-83.md`, `round-84.md` and `round-85.md` each
carry a `**Check command**:` line; `round-86.md` has zero occurrences (`grep -c "Check command"` = 1, 1, 1, 0). The
lane's own convention ("the three records above are checked by the same command", round-85 `## considerthese`) is
broken by this round's lesson, and the reader is given no command to reproduce the Gate block.

**F8 — the round-85 non-git-setup and D1 "before" receipts are cited correctly; the "zero D1 lines" wording is loose.**
`controls/receipts/c1-k0b-frozen-instrument.txt` prints the r85 battery's `354/354 … GATE_RECORDS_R85=PASS`, exit 0,
and its trailing `# D1 class lines in the r85 counter:` / `0`. Measured: `grep -c "D1-203"` in
`corpus/evidence/round85/gate-records-r85.py` = **0** ✓, `grep -c "MUT17"` = 0 ✓, but `grep -c "D1"` = **3** — the r85
counter does contain three `D1` mentions, but they are the *other* D1 (`D1-stale-refetch-txt-sha-drift`, a distinct
class) and not `D1-203-admit`. The frozen `claims.md` wording ("zero `D1-203-admit` or mutant lines in its bytes
(grep count 0)") is precise; the lesson's paraphrase in `## Claim outcomes` ("with zero D1 lines in its bytes (grep
count 0)") is not — as written it is false by a factor of three. Recorded, not fatal to any claim.

**F9 — the `S024` restoration is byte-exact, but the landing commit also edited three cells that `CORPUS.md` rule 2
does not allow to change in place, and the lesson's old→new log does not cover them.**
`corpus/SOURCES.md` S024 at the landing is **byte-identical** to its pre-round-85 row at `43c3f7284eee4889cdcc6ac1626573f6579cd533`
(all eleven cells), and differs from the base row in four cells (`status`, `used-by`, `opened`, `anchor`) — receipts 08
and 16f. The lesson logs `status`, `used-by`, `opened` old→new but not the `anchor` edit, and it does note that the
`opened` change was itself outside `CORPUS.md` rule 2 and that the restoration is logged as rule 2 requires. Three cells
outside rule 2's three (`opened` and `anchor` on S024; `anchor` on S031) were edited in place by the landing commit;
only the `opened` one is flagged as a rule-2 issue, and no anchor edit is logged old→new (S031's anchor change is
described in prose, "anchor gains the re-open date and the located definition", without the old value). This is a
disclosure gap in the lesson's own change log, not a claim failure.

## Reproducibility and hygiene

* Scratch: `/fast/scratch/hyaku/chousa-r86/R86ScribeLesson/` — trees `tree/` (landing), `base/`, `base86/` (base +
  the frozen counter), fixture copies `p1/`, `p2/`, probe lessons `probe/`, one scratch tool copy
  (`tool-allow-reject.py`, the committed tool with the single parse guard widened) and the shell/python drivers
  `r09.sh`–`r16.sh`, `cells.py`. **Deleted before this yield.**
* Every receipt cited above was copied into
  `.ufo/waves/round-86/w1/R86ScribeLesson/receipts/` first (15 files, each header naming the exact command and
  showing the observed output and exit code).
* One stray file was created and deleted during the run by a mistyped path
  (`/fast/scratch/hyaku/chousa-r76.tmp`, outside this seat's scratch dir); it was removed immediately and nothing was
  written under `/tmp`. No file outside this seat's output folder and this seat's scratch dir was written or modified.

VERDICT: R86ScribeLesson C1 held — the landing predicate reproduces exactly (`TOOL=present POSITIVE=15/15
FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1
D1_REFUSED=1/1 MUT17_KILLED=1/1` / `GATE_RECORDS_R86=PASS`, exit 0) and the lesson's two Gate records verify
(`files=1 records=2 ok=2 fail=0`, exit 0), but the lesson's schema-gap reasoning (Mistakes item 1) and QUALITY 173
misstate the tool: it has three record forms, the `rev` form already records the S217 decision, and the proposed
`decision=reject` admit form needs no REFETCH change.
VERDICT: R86ScribeLesson C2 held — the landing predicate reproduces exactly (`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0
MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS`, exit 0) and the round-85 "verified" column is
retracted without editing the round-85 file, but QUALITY 174's cited `SUPERSEDED_LIVE=0` check passes while the
round-85 inversion is present, the lesson's S023 byte-drift sentence is false on committed bytes, and QUALITY 173's own
Check fails for the unrecorded S023 re-open.

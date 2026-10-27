# R56RegisterR55Late — round-55 settlement register

date: 2026-10-27 · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` · read at round-55 rev `53f1ce6b` and at
HEAD `99eff0e` · read-only; no product, counter, claims, registry or other seat's report written; scratch
`/fast/scratch/hyaku/chousa-r56/R56RegisterR55Late` removed · no network · no tool installed.

Question: the eleven W1 seats of round 55 that left no report file — what did each actually find, does it falsify
or narrow a landed round-55 statement, and what disposition does it carry? Plus the two salvaged reports.

## 1. The eleven (list verified, not assumed)

```
python3 -c  # results names minus .ufo/waves/round-55/w1/*.md
48 seats, 37 md files, MISSING 11: R55ExecC1Seeds R55MutC1Builder R55SentC1 R55SimplifyBuilder
R55GroundNmpaEn R55GroundMedsci R55DraftEntry R55DraftRows R55DraftC3Fixes R55RegisterW2A R55ScoutFrontier
EXTRA (md with no results entry): []
$ git ls-tree --name-only 53f1ce6b:.ufo/waves/round-55/w1/ | grep -c '\.md$'
36
$ git ls-tree -l 53f1ce6b:.ufo/waves/round-55/w1/ | awk '$5 ~ /\.md$/ {n++; if($4<200) s++} END{print n, s+0}'
36 0
```

At the frozen rev the no-report count was **12**, not 11: `R55MutC2Counter` had no report at `53f1ce6b` and was
salvaged later (present at HEAD). The seat-spec list is therefore correct at HEAD and one short at `53f1ce6`.

## 2. Per-seat findings and dispositions

| seat (agent) | output form | finding | landed round-55 statement at `53f1ce6b` | disposition |
|---|---|---|---|---|
| `R55ExecC1Seeds` (executor) | 1125 B reasoning fragment, no verdict | none assertable. Fragment reports seeds 1–46 of a wider sweep passing; no table, no receipt, run cut mid-sweep | `corpus/evidence/round55/claims.md:94` (target 4/4 ×4) unaffected. The committed `c1-seed-sweep-L1.txt` is 40 lines, all `LEGS=4/4` (verified: `grep -c '^seed='`=40, `grep -c 'LEGS=4/4'`=40) | none |
| `R55MutC1Builder` (mutation-tester) | JSON error, `aborted: true` | none. Only a pristine baseline PASS 4/4 ran; the mutation matrix never ran (seat reports the archive-copy constraint) | `SCORECARD.md:2804` already discloses "six counter clauses no control exercises (`R55MutC1Counter`)" and "the falsify wave did not run"; nothing claims a builder mutant matrix | none |
| `R55SentC1` (sentinel) | 1171 B fragment, no verdict | unverified lead: on SIGINT (`rc=130`) `soffice.bin` is gone but the profile/work dir survive. No command, no exit receipt, and the run involves LibreOffice, which no C1 leg runs | would narrow `claims.md:84` ("default a `$TMPDIR` mkdtemp removed on exit") to normal exit only — **not established** by the fragment | none (lead) |
| `R55SimplifyBuilder` (simplifier) | 701 B fragment, no verdict | the ZIP half of the defined-form rule is never exercised: the four legs are GENOLE/OLEPIN (OLE) and REFUSE/REGRESS (`c1-count.py:282,299,331,391`; REGRESS = round-54's 3 rows). Confirmed by reading the counter | `claims.md:62-64` states the zip rule but the four legs and the target (`claims.md:94`) never test one; no landed sentence claims ZIP coverage, so nothing is falsified — the gap is narrowed *coverage* | none to the land; gap carried (see §5) |
| `R55GroundNmpaEn` (scribe) | 6769 B fragment, no verdict | reached: S126 adds only identity/official-host/date over S125; bind narrowly, refuse any legal-hook/structure inference as *unique* to S126 | consistent: `grey-literature-and-chinese-search-record-r40.md:5` binds S126 for headline/`Updated:`/first+third paragraphs; `:22` attributes issuer to S125 **and** S126; `:18` uses both for the shared structure claim. No unique-substance claim | none |
| `R55GroundMedsci` (scribe) | 574 B fragment, no verdict | S113's page shows `paymentAmount=10` as a metadata field, no displayed price; drop the med-sci bullet | landed: the entry has **0** `S113` occurrences (`grep -c S113` → 0); verdict says "S113 not cited" (`SCORECARD.md:2805`) | none (already integrated) |
| `R55DraftEntry` (scribe) | 8452 B fragment, cut mid-sentence | none as a verdict; the plan it reached matches the landed entry (quotes, "should" rendering, date/issuer bound to S125/S126, S113 dropped) | `r40:6,13-24` carry exactly that; the fragment's `2019 0× 发布 0×` sweep is the landed `r40:28` line `13718 0 [7,1,1,0,0,0,1,1,8,5]` (token 4 = `2019` → 0) | none |
| `R55DraftRows` (scribe) | 1114 B fragment, no verdict | lead: S124's form may carry CR, so universal-newline reads could shift offsets. Checked: `capture-text.py bdff…raw` → `rc 0 len 13718 CR 0 LF 865 CRLF 0`, `即“灰色文献”` `find`=1012, count 1 | concern is null (no CR). The real defect in that area — the lesson's `char 994` for `即“灰色文献”` (should be 1012) — was found by closure D4, not this seat, and is corrected at HEAD `corpus/lessons/round-55.md:31` | none |
| `R55DraftC3Fixes` (scribe) | complete JSON, VERDICT | four r36 findings (I3 latent string, I5 hedge, O4 char 569 not 575, verified-at scope), QUALITY 97/98 (transposed positions, exclusion sets, 469 LF, ctypes/SHELL split), lesson row 2 BAD count (both dumps missing → BAD=9; S101-only 6; S100-only 3) | all landed: `source-type-taxonomy-r36.md:38-45` (E01–E04), `QUALITY.md:945` (E05/E06/E07), `QUALITY.md:947` (E09 boundary), `corpus/lessons/round-55.md:29` (E08). The draft's `0/6` and `3/3` supplement numbers were not carried; E09's observation is the counter's own `rc=0 marker=SPAWNED` | none (integrated) |
| `R55RegisterW2A` (scribe) | JSON error, no report | explicit: only a subset of the `R54W2Exec` reports was read; names unread `R54W2ExecQuarantineVerify`, `R54W2ExecLedger`, `R54W2ExecC2Rerun`; "No report file was written" | falsifies `corpus/lessons/round-55.md:21`, which names `R55RegisterW2A.md` and `R55RegisterW2B.md` as "the integration register" for the remaining W2 findings. Only W2B exists (26-row table) | **appended correction** (R-B, §4) |
| `R55ScoutFrontier` (scout) | complete JSON, VERDICT | ranking only (S101 comparison 1st, r41–r48 family 2nd, freshness 3rd, theme B 4th); date histogram 2026-10-19..26. Attacks no landed statement | none touched. Its rank-1 S101 comparison is still unopened in round 56; not a round-55 statement | none |

## 3. The two salvaged reports

| report | finding | falsifies / narrows? | disposition |
|---|---|---|---|
| `R55MutC2Counter.md` | nine one-check-removal mutants of the round-55 C2 counter; each admits a shortcut root the frozen counter refuses, every mutant passes its pristine root, all nine checks load-bearing; controls reproduce byte-for-byte; counter sha256 restored `6fa1e4b4…` | no. Corroborates `claims.md:140` (`C2=PASS`) and the control receipts. Side observation: lane tip moved while it ran, counter bytes identical | none |
| `R55ExecBuilderOld.md` | the builder re-derives round-47..54 quote tables; round 49 differs in 9 rows (`STALE=9`, S100-1..3, S101-1..6); synthetic probes A/B refuse a formless raw and an OLE-sidecar-only quote | no. The frozen REGRESS covers round 54 only (`claims.md:79-81`). Its candidate `QUOTE` chars (11972, 12007, 12795, 12963, 14049, 25123) are E05's located/drift values (`SCORECARD.md:2788`) | none |

Null result I checked before reporting a defect: the round-54 lesson's `1431`/`2843` (`corpus/lessons/round-54.md:15`)
are **Registry anchor chars**, not round-49 span offsets — `SOURCES.md` S100 anchor cell reads `char 1296, char 1431,
char 2843`, while round-49 `spans.tsv` at `dba605de` gives offsets 1296/1423/2763 (span start + 8/+80 = the anchor). No
contradiction; the lesson's arrows are old-quote-char → new-quote-char.

## 4. Register-level defects (verified against committed bytes, not inferred)

**R-A — `corpus/lessons/round-55.md:17` says "`.ufo/waves/round-55/w1/` 35 of 48 reports"; the same revision
commits 36 non-empty `.md` reports.** `git ls-tree -l 53f1ce6b` → 36, smallest 2657 B; at HEAD 37 (after
`R55MutC2Counter.md`). Disposition: appended correction (36 of 48 at `53f1ce6b`; 37 of 48 at HEAD; no-report
count 12 then, 11 now).

**R-B — `corpus/lessons/round-55.md:21` names `R55RegisterW2A.md` as an integration register; that file has never
existed.** `git cat-file -e 29cfb12a:.ufo/waves/round-55/w1/R55RegisterW2A.md` → `fatal: path ... does not exist`;
absent at `53f1ce6b` and at HEAD. So "the remaining findings are dispositioned in the integration register (W2A,
W2B)" holds only for the W2B half; the `R54W2Exec*` findings that W2A was to register are undispositioned.
Disposition: appended correction naming W2B alone and recording the W2A half as never written.

**R-C — one carried round-56 item is unsatisfiable as written.** `.ufo/waves/round-55/w2-spec.json:170` and its
unchanged copy in `.ufo/waves/round-56/w1-spec.json` (`R55W2ScoutW2Integration`) instruct: "read …/R55RegisterW2A.md
and R55RegisterW2B.md … and check what actually landed". The first path does not exist at `29cfb12a`, `53f1ce6b` or
HEAD. Routed to the L1: the item can only be executed scoped to `R55RegisterW2B.md`; I do not edit the frozen item.

## 5. Limits

- 7 of the 11 outputs (`R55ExecC1Seeds`, `R55SentC1`, `R55SimplifyBuilder`, `R55GroundNmpaEn`, `R55GroundMedsci`,
  `R55DraftEntry`, `R55DraftRows`) are truncated reasoning, not results: no verdict, no command receipt. None is
  upgraded to a finding; the two with a checkable claim (CR/newline, S113 display) I checked myself and both are null.
- `R55SentC1`'s interrupt-cleanup observation stays a lead: reproducing it needs a signal experiment the round-55
  claim never asked for. It does not affect `claims.md:94`.
- The ZIP defined-form gap (`R55SimplifyBuilder`) is not closed by round 56 either: the battery is
  `m1..m7` + `oracle-m8-unpinned.py`, and only `oracle-m8` mentions zip, as a capability of the oracle, not as an
  attacked document class; the gate inherits the four legs' OLE + round-54 inputs.
- No statement above rests on the w1-results `note` field (null for all 48) or on a campaign tool.

VERDICT: settled the eleven report-less round-55 W1 seats and the two salvaged reports — ten carry no finding
against a landed round-55 statement (one ZIP coverage gap, one unverified interrupt lead), one (`R55RegisterW2A`)
falsifies `round-55.md:21` and with it the carried item `R55W2ScoutW2Integration`; three register defects survive
verification (35-vs-36 report count, the absent W2A register, the unsatisfiable carried item).

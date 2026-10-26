# R52W2ReviewLesson — attack on `corpus/lessons/round-52.md` section by section, and erratum completeness

seat: R52W2ReviewLesson (leaf; no dispatch) · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only for me except this report) ·
scratch `/fast/scratch/hyaku/chousa-r52/R52W2ReviewLesson` (TMPDIR exported there; removed at exit) · no installs (tooling rules read; pacman paused, nothing needed).

Every command below ran from my scratch (TMPDIR exported) or the lane root; nothing was written outside this report.

## 1. `## Mistakes` — evidence pointers resolve; every "shown able to fail" command re-run

Row 1 (capture-form). Pointer `corpus/lessons/round-51.md` refused-doc paragraph resolves (lines 54–57; the `.docx` refusal, `.txt` sidecar 168,952 chars / 72,117 U+FFFD). I counted the main part myself:

```
$ unzip -p .../3a8b45977cd111e45e3980a5.raw word/document.xml | grep -c '<w:instrText' → 50 ; grep -c '<mc:Fallback' → 60
```

Shown able to fail, re-run: `python3 corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/naive-tool.py --work <scratch>/w1` →
`REAL=PASS ... locate=(0, 1, 10319) chars=21910 / LEGS=4/9 / C1=FAIL` rc 1 (REVISIONS, LAYOUT, ALTCONTENT, MAIN_PART, REFUSE fail). `controls/c1-before.txt` carries the same REAL line (26–27). Cache-sidecar control `LEGS=0/9` (c1-before.txt:39–41).

Row 2 (reference-drift). `round-51.md:88-89` confirmed: `register S120 (round 5) verdict: present` then `...  char 39411  form .raw unzipped → word/document.xml UTF-8`. Re-run the shift proof:

```
$ unzip -p <raw> word/document.xml > doc.xml (1,464,476 B)
$ python3: for each of the 3 S120 quotes: count=0 find=-1  (sentence split across runs; byte search wrong)
$ python3 tools/capture-text.py <raw> --locate '<q>' → LOCATED count=1 offset=8996 / 9020 / 9428, rc 0 each
```

Row 3 (vacuous forge). `controls/forge-shape.py` exists (85 lines). `c1-count.py --tool controls/forge-shape.py` → `REAL=PASS ... locate=(0, 1, 0) chars=21 / LEGS=9/9 / C1=PASS` rc 0 (the frozen counter passes the forge). Supplement re-run: tool → `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS`, forge → `0/4 ... FAIL` rc 1, naive → `0/4 ... FAIL` rc 1 — matches the row.

Row 4 (fleet-root strays). `/home/vgpnk/Projects/shokunin/.tower/quarantine/fleet-root-strays-20261026T2010/` holds `p.out` (62 B, mtime 20:10) = `QUOTE S115 char 13246 spans/S115-1.txt` + `SPANS_ROWS=1 WRITTEN=1`, and empty `p.err`; and `目標値に到達` is exactly once at char 13246 in the capture-text form (re-located). W1 `R52MutBuildSpans.md` "Killer quote" matches.

Row 5 (non-Word main parts). Candidate vs landed, same raw, re-run:

```
$ git show 804a4537:tools/capture-text.py > cand.py
$ cand.py .../cb101e95f5f5e98d019eeca1.raw → rc=0 stdout 0 bytes (empty form, indistinguishable from empty document)
$ python3 tools/capture-text.py .../cb101e95f5f5e98d019eeca1.raw → rc=2 stderr=REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root {...spreadsheetml...}workbook)
```

Row 6 (size bomb). I built a 350,669-byte package whose `word/document.xml` inflates to 360,000,113 bytes:

```
$ python3 tools/capture-text.py bomb.docx → rc=2 stderr=REFUSED 'word/document.xml' inflates to 360000113 bytes (limit 268435456)
```

Candidate (source `3986a971…`) has no size gate (no `MAX_PART`/`bounded`); W1 `R52SentCapture` H1 measured its bomb path (rc 0, 3.03 GB RSS; `MemoryError` under `ulimit -v 2000000`).

## 2. `## Spot-check intake` — all six dispositions true, cited runs re-executed

1. C1 counter nonce-only: `c1-count.py:256` `random.SystemRandom()`/`--seed`, `:258` `mkdtemp(prefix="c1r52-", dir=a.work)` — no fixed dir/file names. 2. W1 `R52ExecAdopterTwin.md:308-320` shows the patch green `SELFTEST=PASS findings=40`, `FIXTURES_SHA256=9822ad59…`, round-50 pin 26/26, round-51 counter 5/5; not applied to the lane (no `assimilate-rows.py` change in the freeze→land diff). 3. C1 + S115 built (verified below). 4. W1 `R52ExecPointerAnchor.md` red-before `ANCHORED=0/4` rc 1 on the lane, green-after 4/4, forged anchor 3/4; not landed (no SCORECARD change in the diff). 5. SKILL row 133 carries "the round-49 and round-50 one-shot counters are not this round's verdict"; re-ran: `ASSIMILATE_CITES=all ... round49/c1-count.py` → `SETS_PASS=3/3 C1=PASS` rc 0; `... round50/c1-count.py` → `SELFTEST_DEFAULT=FAIL ... LEGS=4/5 C1=FAIL` rc 1. 6. No in-lane repeat; fleet-root incident stands (row 4).

## 3. `## Gate`

Collision check re-run (the documented section-10 pattern) into my scratch: `reg-ids` 116 lines (S001–S116), `staged-ids` 114 (S082–S195, md5 `d91867693dc4b0a4a901922ca8297c22`, identical to W1's), `collisions` 35 (S082–S116). The lesson's 112/114/31 (round-52.md:36) are the base-state numbers from W1 `R52ExecCollision`; after landing S113–S116 the same commands now collide staged S113–S116 too — exactly what the W1 forward note predicted. Not false; the lesson never labels them base-time.

Renumber map vs Registry: staged S111→S113, S112→S114, S125→S115, S129→S116; S126 held→S112 (JAHBS URL matches lane S112); S133 dropped (same medsci URL as S111). All four rows exist with `opened 2026-10-26`, `mined`, `recheck 180d`, `used-by` naming exactly the citing entry, `source:` lines in each entry; `REF_ID_UNBOUND=0`.

Normalisation paragraph: staged S125 title strings `提出様式`/`C2H`/`Evidence to Decision` are 0× each in the text form (tool output 19,682 chars, 0 CR); `翻译`/`译`/`translat` 0× in the 中国全科医学 `.txt`; the S116 cell leads with the archive URL (needed for C2's first-URL bind). All hold.

Decisions table — re-opened FOUR decisions' captures (all observed values match the table):
- NIPH half (S125): `3a8b4597….raw` 178,056 B; tool form 19,682 chars exit 0; `.txt` sidecar 168,952 chars, 72,117 U+FFFD, `文献検索期間` absent; quotes at 8996/9020/9428 once each; `使用したデータベース` 9408 and `使用した検索式` 9419 once each.
- JPW (S129): `e84bfe97808591d23fe3266f.txt` 5,328 chars / 10,106 B (sha256 `93558b6d…` = span digest), `.pdf`/`.raw` 343,301 B; `検索者` 0×; `項目7` 0×; row labelled `検索戦略` with number 7 at char 619 (context `検索戦略            7     用いたフィルター…`); the unbroken recheck string 0×; `用いたフィルターや制限も含め，` once at 641.
- Reception half (S111/S112): `453d492b….txt` 8,804 chars / 14,135 B; `cacddf3b….txt` 6,179 chars / 11,676 B; `检索或查询日期` once at 1719; `PRISMA-S` 15×; `16` first at 2389; `paymentAmount` at 4178; SinoMed `42bac883….txt` (1,675 chars) stops at `并针对中文` (1×; continuation `并针对中文数据库等本土化应用挑战提出实践建议` 0×).
- search-log-fields-r36 (S082/S083/S090): `01f657b3d0ab045c494b3f92.txt` 265 chars of `Client Challenge`; `14aaa168a5cb4d833ca78b0b.txt` 210,708; `02b3b0e812df68ca305c7bc3.txt` 3,542 chars, `参照` 0×; article PDF `58b1b564…` 506,589 B; `copied and pasted exactly as run` 0/2,549 `.txt`; newest capture 2026-10-24 23:26; staged line 15 carries `_article/-char/ja`.

## 4. Quarantine block
Register S120 row (absent-defect-register.md:55) = `payload-absent` with the three quotes; lesson lines 74–78 carry the verdict `present` with `char 8996/9020/9428 form capture-text` — all three re-located exactly once at those offsets (above). The claim that round-51's `char 39411` is an offset of nothing holds: `find()` of the sentence in `word/document.xml` = −1 (count 0), verified for all three quotes; round-51.md:89 is that line, and the round-51 spot-check's section-4 row accepted it without re-locating the offset.

## 5. `## considerthese`
`python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51` → `R47 operability: lane=improved verifier=harmed`, `R48 UNPARSED lane_axes=6 verifier_axes=0`, `R50 calibration: lane=improved verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1` rc 1 — exact match. Spans/lesson consistency: `build-spans.py --check` → `SPANS_ROWS=38 STALE=0` rc 0; C2 `C2=PASS` rc 0 (`BOUND=4/4`, `QUOTE_ROWS=38 ON_BOUND=38/38`, `CAPTURE_BOUND=38/38`, `ANCHOR_BOUND=4/4`, `QUARANTINE_VERDICTS=1/1`); cross-reader agreement on all eight PK raws (tool vs `docx_text`: same text each, e.g. 19,682/19,682 on NIPH).

## 6. `## Census`
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `ok`, the five pre-existing W04 (S051/S053/S073/S074/S075), matching `census-start.txt`. Rows 112→116 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 116); tiers now A=100 B=11 C=5; added by tier A S114 S115, B S113 S116 (matches lesson).

**Defect 1 (dangling pointer)**: the lesson's Round-end bullet cites `corpus/evidence/round52/measure-after.txt` (round-52.md:140); that file does not exist — `ls corpus/evidence/round52/` shows only `census-start.txt` (and no `measure-*` anywhere under round52; rounds 46–51 each have a `measure-after.txt`). The end-state content I verified by running the command myself, but the named receipt is absent from the lane.

**Defect 2 (undocumented normalisation)**: staged S112's tier (SOURCES.append.md:37) is B; the landed S114 row (SOURCES.md:124) is A. The lesson's normalisation paragraph (round-52.md:51) records the S125 title, S129 cell order and S112 teaches-cell rewrites but not this tier raise; the erratum is silent. No frozen predicate reads tier, so this is a disclosure gap, not a claim change.

## 7. Erratum completeness (freeze 37468ead → land e769c037)
`git diff --stat 37468ead e769c037` → 110 files, +10,150; **none** of the frozen files change: `claims.md`, `c1-count.py`, `c2-count.py`, `build-spans.py`, `controls/*` are absent from the diff (unchanged). The post-freeze additions map one-to-one onto E1–E4: `c1-supplement.py` (E1), `tools/capture-text.py` (E2), reader-divergence named (E3), C2 limits (E4). I diffed candidate `804a4537` → land for the tool: exactly the E2 changes (root check `if not stack and el.tag != W+"document"`, `MAX_PART=256 MiB` + `bounded`, `MemoryError`→`Refused`, `unquote` + `..`/`/` target refusal, `el.clear()`, `RuntimeError/NotImplementedError`→refusal, `--locate ''` usage exit 2). Commits: `804a4537` is post-freeze and an ancestor of land; 01c17ce (integration) + e769c03 (E2(e) refusals) are the only post-candidate tool commits. No claim-relevant change is un-disclosed.

## VERDICT
Attacked `round-52.md` section by section (Mistakes evidence/able-to-fail runs, Spot-check intake, Gate collisions/renumber/normalisation/decisions re-opened, quarantine S120 quotes + `char 39411`-of-nothing, considerthese verdict-gap, Census) and the erratum completeness: every claim and command verified true, with two lesson defects — `measure-after.txt` cited at round-52.md:140 does not exist, and the staged→landed S114 tier B→A change is undocumented in the normalisation paragraph and erratum (collision counts are base-time, correctly attributed, now lower/upper-dated by the landed rows).

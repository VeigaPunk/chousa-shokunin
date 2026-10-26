# R52DraftSkillGates — SKILL.md `## Gates` rows for round 52 (draft)

Seat: `R52DraftSkillGates`, leaf (no dispatch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
working tree at HEAD `13bc28063b4bd7ea2e521167413ee9829202a420` (`13bc280`), only `SKILL.md`
dirty (see Conflict). Nothing installed (no install needed). Scratch
`/fast/scratch/hyaku/chousa-r52/R52DraftSkillGates` (all `TMPDIR` uses), removed at the end.
This report is my only write; no lane file, index or jj state touched.

## What was read (grounding)

- `SKILL.md:76` `## Gates`; rows `130` (`assimilate-rows`), `131`/`132` (round-49/50), `133` (round-51),
  `137` (the one existing `correction:` line — the append-only pattern followed below).
- `tools/capture-text.py` (115 lines: rule 1-28, `main_part` 45-62, `text_form` 65-96, `main` 99-115);
  `corpus/evidence/round52/claims.md` (both predicates, targets, controls, kill rules);
  `round52/c1-count.py` (constants 45-48, legs 258-341); `round52/c2-count.py` (58-81,
  `NO_BASE_OR_REGISTER` 152-156, builder import 88-92); `round52/build-spans.py` (`docx_text` 1-30,
  `CONTEXT=80`); `round52/controls/{build-c2-controls,c1-before,c2-before,c2-controls,naive-tool}`.
- `corpus/lessons/round-51-verifier-spotcheck.md` §6 (routed defects 1-6); `corpus/evidence/round47/c2-count.py`
  (registration = the path in the `entry` cell of a row whose verdict-map cell carries an exit code).

## Commands and observed output

Registry line at the current tree (required paste; run twice — see Conflict for why they differ):

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && TMPDIR=$S python3 corpus/evidence/round47/c2-count.py --list | tail -20
ENTRY_POINTS=129 (abc=103 dependence=+8 check_named=+18)
FLOOR=92
GATES_ROWS=58
REGISTERED=129/129
UNREGISTERED=0
DANGLING=0
MISMATCHES=0
C2=PASS
# 20:06:16-03:00
```

The same command at 20:05:5x, before a concurrent write landed rows 134-135, printed `GATES_ROWS=56 / REGISTERED=125/129 / UNREGISTERED=4 / C2=FAIL` with `UNREGISTERED_PATH` lines for `corpus/evidence/round52/build-spans.py`, `…/round52/c1-count.py`, `…/round52/c2-count.py`, `tools/capture-text.py` — exactly the four entry points these drafts register. The count moves because those paths are entry points: named in `corpus/QUALITY.md`/`SKILL.md` outside `## Gates` (check-named) and as dependency literals.

`capture-text` behaviour (exit codes, refusals, `--locate`), all from the tool at `13bc280`:

```
$ sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw
16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763  …/3a8b45977cd111e45e3980a5.raw
$ python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw > $S/niph.txt; echo RC=$?
RC=0
$ python3 -c "t=open('$S/niph.txt',encoding='utf-8').read(); q='SRにおける文献検索期間について明記する'; print(len(t), t.count(q), t.find(q))"
19682 1 8996
$ python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する'
LOCATED count=1 offset=8996      RC=0
$ python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate 'zzz-not-present-zzz'
LOCATED count=0 offset=-1        RC=1
$ python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate ''
LOCATED count=0 offset=-1        RC=1
$ python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate '文献検索'
LOCATED count=3 offset=9002      RC=1     # 2+ hits: first offset still printed
$ python3 tools/capture-text.py …/6dc68fd6b32ce9c8dfcebce8.raw   # OLE Word .doc, real capture
$ python3 tools/capture-text.py …/02408e0c9018e826396cd149.raw   # PDF, real capture
$ python3 tools/capture-text.py …/001287c436f0e6b1d166ae8d.raw   # HTML, real capture
REFUSED not a zip (an OOXML capture is a zip package)   ×3, RC=2, stdout 0 bytes each
$ python3 tools/capture-text.py $S/no-rels.docx                   # zip, no _rels/.rels
REFUSED no _rels/.rels in the package                            RC=2, stdout 0 bytes
$ python3 tools/capture-text.py $S/no-officedoc-rel.docx          # rels without officeDocument
REFUSED no officeDocument relationship in _rels/.rels            RC=2, stdout 0 bytes
$ python3 tools/capture-text.py $S/dangling-target.docx           # target absent from the zip
REFUSED officeDocument target 'word/missing.xml' is not in the package   RC=2, stdout 0 bytes
$ python3 tools/capture-text.py
usage: capture-text.py [-h] [--locate QUOTE] raw … error: the following arguments are required: raw   RC=2
```

`no-rels.docx`, `no-officedoc-rel.docx` and `dangling-target.docx` are zips I built in scratch with
`python3 -` + `zipfile` (member sets named above); the `.doc`/PDF/HTML rows are real cache captures.

Mid-session the candidate gained a root check (working tree 20:10, blob `1726cd04…`, absent from
the `804a453` blob `3986a971…`); `c1-count.py` still passes on it:

```
$ python3 tools/capture-text.py $S/workbook.docx   # officeDocument target root is <workbook>
REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root …spreadsheetml…}workbook)   RC=2
$ python3 tools/capture-text.py $S/deck.docx       # <p:presentation>
REFUSED main part 'ppt/presentation.xml' is not WordprocessingML (root …presentationml…}presentation)   RC=2
$ python3 tools/capture-text.py $S/theme.docx      # <a:theme>
REFUSED main part 'word/theme/theme1.xml' is not WordprocessingML (root …drawingml…}theme)   RC=2
$ TMPDIR=$S python3 corpus/evidence/round52/c1-count.py --work $S | tail -3
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9
C1=PASS
```

The two readers agree byte for byte on the pinned capture (C1 vs C2 independence check):

```
$ python3 - <<'PY'   # import corpus/evidence/round52/build-spans.py, call docx_text on the raw
BUILDER_CHARS 19682
BUILDER_COUNT 1 OFFSET 8996
SAME_AS_TOOL True    # == $S/niph.txt written by tools/capture-text.py
PY
```

Round-52 counters at the current tree (`$S/work1` created first — see finding 2):

```
$ TMPDIR=$S python3 corpus/evidence/round52/c1-count.py --work $S/work1 | tail -3
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9
C1=PASS
$ TMPDIR=$S python3 corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/naive-tool.py --work $S/work1 >$S/naive.out; echo RC=$?
RC=1   … REAL=PASS rc=0 count=1 locate=(0, 1, 10319) chars=21910 / LEGS=4/9 / C1=FAIL
# cache-txt-tool.py → REAL=FAIL … chars=168953 / LEGS=0/9 / C1=FAIL ; const-tool.py → LEGS=0/9
# /nonexistent/tool.py → REFUSE=FAIL tool absent, REAL=FAIL tool absent, LEGS=0/9
$ TMPDIR=$S python3 corpus/evidence/round52/c2-count.py; echo RC=$?         # entries not in the lane yet
ENTRIES=0/3 / BOUND=0/4 (min 3) REFUSED=0 / NEW_GROUND=0/3 / CAPTURE_BOUND=0/0 / SUBSTANCE=FAIL
C2=FAIL   RC=1
$ TMPDIR=$S python3 corpus/evidence/round52/c2-count.py --lane-only          # same, CAPTURE_BOUND=skipped, RC=1
$ TMPDIR=$S python3 corpus/evidence/round52/build-spans.py --check; echo RC=$?
build-spans: no input /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/quotes.tsv
RC=2
$ python3 corpus/evidence/round52/c1-count.py --per-leg 0 >/dev/null 2>$S/c1-per0.err; echo RC=$?
RC=2   (stderr: per-leg must be >= 1)
$ TMPDIR=$S python3 corpus/evidence/round52/c1-count.py --work $S/nonexistent-work >/dev/null 2>$S/err-work.txt; echo RC=$?
RC=1   (stderr tail: FileNotFoundError: … /nonexistent-work/c1r52-infny2p8)
```

Round-51 routed defect 5 — the round-49/round-50 one-shot counters, both modes, direct exit codes
(no pipe into `tail`, so `$?` is the counter's):

```
$ TMPDIR=$S ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py; echo RC=$?
SETS_PASS=3/3 / C1=PASS   RC=0
$ TMPDIR=$S python3 corpus/evidence/round49/c1-count.py; echo RC=$?
SETS_PASS=2/3 / C1=FAIL   RC=1
$ TMPDIR=$S ASSIMILATE_CITES=all python3 corpus/evidence/round50/c1-count.py; echo RC=$?
SELFTEST_DEFAULT=FAIL / BASELINE=PASS rc=0 findings=26 / PERTURB_PASS=6/6 / EXPECTED_BAD=PASS rc=2
R49_REGRESSION=PASS rc=0 / LEGS=4/5 / C1=FAIL   RC=1
$ TMPDIR=$S python3 corpus/evidence/round50/c1-count.py; echo RC=$?
SELFTEST_DEFAULT=PASS / BASELINE=FAIL rc=1 findings=? / … / R49_REGRESSION=FAIL rc=1 / LEGS=3/5 / C1=FAIL   RC=1
$ python3 tools/assimilate-rows.py --selftest | tail -2                         # default (source) mode
FIXTURES_SHA256=3b7ad25837a954be5623d27a7b1a231ddf661e67e5a961f0800a112b2260bd00
SELFTEST=PASS findings=27 expected=27
$ ASSIMILATE_CITES=all python3 tools/assimilate-rows.py --selftest | tail -2   # same package, env all
DIFF unexpected STRIPPED S024 used-by
SELFTEST=FAIL findings=36 expected=27
```

So defect 5 is real on both counters and cannot be cured for round 50 by the env alone: its leg 1 (lane default package) needs source mode and its leg 2 (round-50 pinned package) needs `all`, so it prints 4/5 with the env, 3/5 without, and never 5/5 at a tip at or after round 51. Round 49 reaches full sets with the env.

## Draft (for the L1 to integrate; not written to SKILL.md by this seat)

```SKILL.md
| `capture-text` (r52 C1; the OOXML `.docx` text form for claim-vs-source checks) | tool | `python3 tools/capture-text.py RAW` (text form on stdout, UTF-8) · `python3 tools/capture-text.py RAW --locate QUOTE` (one line `LOCATED count=<n> offset=<first offset or -1>`, offsets are code-point indices into the printed form). Rule: main part = the `_rels/.rels` relationship whose Type ends in `/officeDocument` (leading `/` stripped, never a fixed member name); inside it, in document order, a `w:t` emits its text (XML entities decoded), a `w:tab`/`w:br`/`w:cr` whose parent is a `w:r` emits tab/newline/newline, the end of every `w:p` (nested ones included) emits a newline, an `mc:Fallback` subtree emits nothing, and nothing else emits text (`w:delText`, `w:instrText`, the `w:tab` stops of `w:pPr/w:tabs` dropped). OOXML zip packages only: an OLE `.doc`, a PDF or an HTML capture is refused, never converted, and the cache `.txt` sidecar is never read | `0` text printed, or `--locate` found the quote exactly once · `1` `--locate` found it 0 or 2+ times (an empty QUOTE counts 0; with 2+ the first offset is still printed) · `2` refused (`REFUSED <reason>` on stderr, nothing on stdout: not a zip, no `_rels/.rels`, no officeDocument relationship, its target absent from the package, unparsable part, or a main part whose root is not `w:document` — a workbook, a presentation or a theme part) or usage (no RAW argument) | `python3 corpus/evidence/round52/c1-count.py` → `LEGS=9/9` `C1=PASS` exit 0 on this tree; `--tool` controls exit 1: `corpus/evidence/round52/controls/naive-tool.py` `LEGS=4/9`, `cache-txt-tool.py` `0/9`, `const-tool.py` `0/9`, an absent path `0/9` (`tool absent`) | NIPH capture `3a8b45977cd111e45e3980a5.raw` sha256 `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763` → 19682 characters, `SRにおける文献検索期間について明記する` exactly once at offset 8996; the tool itself carries no digest pin (the counter takes `--tool`), candidate `804a45370dc992bfe714817281535055c2f9b032` blob `3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1`, working tree blob `1726cd041955d336cc76e97014a622d9bfd43695030e98ddf7711ebe0c33044c` (adds the root check) | read-only: stdout only, one `REFUSED` line on stderr, no temp file, no network | chousa |
| `chousa round-52 counters and checks` (r52 C1 capability, C2 depth) | gate | `python3 corpus/evidence/round52/c1-count.py [--tool PATH] [--seed N] [--work DIR] [--per-leg K]` (`--work` MUST already exist; scratch is created under it or `$TMPDIR` and removed on exit; every package, member and file name is freshly random) · `python3 corpus/evidence/round52/c2-count.py [--root LANE] [--lane-only]` · `python3 corpus/evidence/round52/build-spans.py [--root LANE] [--cache DIR] [--check]` (a zip `.raw` reads as `docx_text`, the builder's own reader of the same rule, so C2 never runs the C1 tool) · controls `python3 corpus/evidence/round52/controls/build-c2-controls.py` (no options; scratch roots only) and the C1 `--tool` values `corpus/evidence/round52/controls/naive-tool.py`, `corpus/evidence/round52/controls/cache-txt-tool.py`, `corpus/evidence/round52/controls/const-tool.py` | C1 `0` only with `LEGS=9/9` (`PARAS` `RUNS_ENTITIES` `REVISIONS` `LAYOUT` `ALTCONTENT` `MAIN_PART` `LOCATE` `REFUSE` `REAL`) · `1` a leg short (a control tool: naive 4/9, cache-txt 0/9, const 0/9, absent 0/9) or a `--work` directory that does not exist (it aborts `FileNotFoundError`, so mkdir it first) · `2` usage (`--per-leg` below 1, argparse). C2 `0` only with `ENTRIES=3/3`, `BOUND>=3` of 4 and `BOUND+REFUSED=4`, `REF_ID_UNBOUND=0`, `NEW_GROUND=3/3`, `QUOTE_ROWS>=3` per bound id, `QUOTES_IN_SPAN`/`QUOTES_IN_ENTRY`/`QUOTES_IN_LESSON`/`QUOTE_SHORT`/`SPAN_CONTEXT` full, `CAPTURE_BOUND` full (printed `skipped`, not failed, under `--lane-only`), `SUBSTANCE=PASS`, `ANCHOR_BOUND=BOUND`, `INFERENCE_GROUNDED=3/3`, `QUARANTINE_VERDICTS` full with `QUARANTINE_BLOCKED_ADOPTED=0` · `1` otherwise (an empty tree prints `ENTRIES=0/3` … `C2=FAIL`) · `2` `NO_BASE_OR_REGISTER` (read from the lane tree: `git -C LANE show BASE_REV:corpus/SOURCES.md` and the campaign register; `--root` does not redirect that read). build-spans `0` built, or `STALE=0` under `--check` · `1` a refused quote, a missing capture or a stale row · `2` no input or usage (`build-spans: no input PATH`) | frozen predicate `corpus/evidence/round52/claims.md` at `37468eadd8d098e80289b2f31a22de3872d4a1f6`; before and control receipts `corpus/evidence/round52/controls/{c1-before,c2-before,c2-controls}.txt` (base `LEGS=0/9`; STAGED and TOOLED both `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL` exit 1); C1 `LEGS=9/9` measured on this tree, `REAL` `locate=(0, 1, 8996) chars=19682` | NIPH `REAL_SHA` `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763` (19682 characters, quote once at 8996); C2 `BASE_REV` `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`, `MIN_BOUND=3`, `MIN_PER_ID=3`, span context 80 characters, campaign register `absent-defect-register.md` with one theme row (`S120`) | read-only except `build-spans.py` without `--check` (writes `corpus/evidence/round52/spans.tsv` and `spans/` inside `--root`), `build-c2-controls.py` (scratch roots under `$TMPDIR` only) and the counters' own `tempfile.mkdtemp`; no network | chousa |
correction: SKILL.md:131–132 (the round-49 and round-50 one-shot rows) — those counters need `ASSIMILATE_CITES=all` at a tip at or after round 51, where the adopter default is `source`: at tip `13bc280` `ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py` prints `SETS_PASS=3/3` then `C1=PASS` exit 0 (without the env `SETS_PASS=2/3`, `C1=FAIL`, exit 1), and `ASSIMILATE_CITES=all python3 corpus/evidence/round50/c1-count.py` prints `SELFTEST_DEFAULT=FAIL`, `BASELINE=PASS rc=0 findings=26`, `PERTURB_PASS=6/6`, `EXPECTED_BAD=PASS rc=2`, `R49_REGRESSION=PASS rc=0`, `LEGS=4/5`, `C1=FAIL` exit 1 — the env removes that row's leg 1 while its round-50 pinned package needs it (`ASSIMILATE_CITES=all python3 tools/assimilate-rows.py --selftest` on the lane default package prints `DIFF unexpected STRIPPED S024 used-by`, `SELFTEST=FAIL findings=36 expected=27` against the source-mode expectation), so at such a tip the round-50 counter prints `LEGS=4/5` with the env and `LEGS=3/5` without it (`SELFTEST_DEFAULT=PASS`, `BASELINE=FAIL rc=1`, `R49_REGRESSION=FAIL rc=1`), and neither counter is round 52's verdict.
```

The draft registers without touching the lane: I fed the two row lines to the registry counter's own
reader on a scratch `SKILL.md` (`## Gates` + a header and separator row + my rows):

```
$ TMPDIR=$S python3 - <<'PY'   # round47/c2-count.py's gates_table_rows + round-46 names()
DRAFTED_ROWS 2
PARSED_ROWS 4          # + the header and separator rows
ENTRY_CELLS 2
tools/capture-text.py	registered=True
corpus/evidence/round52/c1-count.py	registered=True
corpus/evidence/round52/c2-count.py	registered=True
corpus/evidence/round52/build-spans.py	registered=True
corpus/evidence/round52/controls/build-c2-controls.py	registered=True
PY
```

## Conflict — SKILL.md already carries two r52 rows that are not this seat's draft

`git status --short` in the lane prints ` M SKILL.md`; `git diff --stat SKILL.md` prints
`1 file changed, 2 insertions(+)`, and `git diff` shows the insertions are exactly a
`capture-text` row and a `chousa round-52 counters and checks` row inserted before the existing
`correction:` line (which moved from line 135 to 137). `stat -c '%y' SKILL.md` →
`2026-10-26 20:05:55.737093356 -0300`; my first read of the file, minutes earlier, showed the
round-51 row at line 133 with the correction at 135 and no r52 rows. I did not write `SKILL.md`
at any point; the two counter runs above bracket the write (56 rows / 125 registered before,
58 / 129 after). Verbatim, as the tree holds them now (lines 134-135):

```
| `capture-text` (r52 C1; the OOXML `.docx` text form for claim-vs-source checks) | tool | `python3 tools/capture-text.py RAW` (text form on stdout, UTF-8) · `python3 tools/capture-text.py RAW --locate QUOTE` (`LOCATED count=<n> offset=<o or -1>`, offsets are code-point indices into the text form). Rule: main part = the `_rels/.rels` relationship target whose Type ends in `/officeDocument`; `w:t` text, run-level `w:tab`/`w:br`/`w:cr` as tab/newline/newline, newline at every `w:p` end, nothing from `mc:Fallback`, `w:delText`, `w:instrText` or `w:pPr/w:tabs`. Reads OOXML zips only: an OLE `.doc` (UTF-16LE runs, round 48), a PDF or an HTML capture is refused, not converted | `0` text printed, or `--locate` found the quote exactly once · `1` `--locate` found it 0 or 2+ times · `2` refused (`REFUSED <reason>` on stderr, nothing on stdout: not a zip, no officeDocument relationship, missing or unparsable main part) or usage | `python3 corpus/evidence/round52/c1-count.py` (nine legs on packages generated at counting time, plus the pinned NIPH capture) | NIPH capture `3a8b45977cd111e45e3980a5.raw` sha256 `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763`: 19682 characters, `SRにおける文献検索期間について明記する` once | read-only; stdout only; no network | chousa |
| `chousa round-52 counters and checks` | gate | `python3 corpus/evidence/round52/c1-count.py [--tool PATH] [--seed N] [--work DIR] [--per-leg K]` (scratch under `--work` or `$TMPDIR`, removed on exit; every package, member and file name drawn from fresh randomness) · `python3 corpus/evidence/round52/c2-count.py [--root LANE] [--lane-only]` · `python3 corpus/evidence/round52/build-spans.py [--root LANE] [--cache DIR] [--check]` (a zip `.raw` reads as `docx_text`, its own reader of the `capture-text` rule, so C2 does not run the C1 tool) · controls `python3 corpus/evidence/round52/controls/build-c2-controls.py`, `corpus/evidence/round52/controls/naive-tool.py`, `cache-txt-tool.py`, `const-tool.py` (C1 `--tool` controls) | C1 `0` only with `LEGS=9/9` (`PARAS`, `RUNS_ENTITIES`, `REVISIONS`, `LAYOUT`, `ALTCONTENT`, `MAIN_PART`, `LOCATE`, `REFUSE`, `REAL`); `1` a leg short; `2` usage. C2 `0` only with `ENTRIES=3/3`, `BOUND>=3` and `BOUND+REFUSED=4`, `REF_ID_UNBOUND=0`, `NEW_GROUND=3/3`, every quote leg `n/n`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=BOUND`, `INFERENCE_GROUNDED=3/3`, every theme register row with a verdict and none blocking a bound document; `--lane-only` skips `CAPTURE_BOUND`; `1` otherwise; `2` no base/register. build-spans `0` built or `STALE=0`, `1` a refused quote or stale row, `2` usage | before receipts `corpus/evidence/round52/controls/c1-before.txt` (base `LEGS=0/9`; naive 4/9, cache-txt 0/9, const 0/9), `c2-before.txt`, `c2-controls.txt` | frozen in `corpus/evidence/round52/claims.md` at `37468eadd8d098e80289b2f31a22de3872d4a1f6`; C2 `BASE_REV` `00f8c7f5272a1d98b6d34913985fa4537e00aaf9` | read-only on the lane; C1 and the controls write only their own scratch | chousa |
```

Both of those rows register (`REGISTERED=129/129`), so the conflict is duplication, not breakage;
the L1 must pick one set. Differences a reader should weigh: the existing C1 row says `2 usage`
where a non-existent `--work` exits 1 with a `FileNotFoundError` traceback, and it omits
`--seed`/`--work`/`--per-leg`; the existing r52 row's C2 `1`/`2` mapping is right, and its
receipt line is the same set I cite. My draft also states the `--work` prerequisite, the empty-QUOTE
and 2+-hit `--locate` cases, the empty-tree C2 output, and the `NO_BASE_OR_REGISTER` dependence on
the lane tree rather than `--root`.

## Findings

1. **`--work` is not created** (`c1-count.py:258` `mkdtemp(..., dir=a.work)`): a missing directory aborts with `FileNotFoundError` and exit **1** — the code of a failed leg — so "bad scratch argument" and "counter failed" look alike (`--per-leg 0` does exit 2). Fix, not applied (no production write this seat): `mkdir(parents=True, exist_ok=True)` first, or exit 2.
2. **`--root` does not redirect the base read**: `BASE_REV` comes from `git -C LANE show` (line 152), so `--root /…/empty-root` prints `C2=FAIL` exit **1**, not `2`; `NO_BASE_OR_REGISTER` needs the lane git object or the campaign register to vanish. The draft row says so, so an operator does not misread a `2`.
3. **Both `.docx` readers agree**: `tools/capture-text.py` and `build-spans.docx_text` give 19682 characters at offset 8996, byte-identical strings — the C2 "its own reader" claim holds on the one capture both touch; `c2-count.py` imports `build-spans.py` by path with no digest pin (88-92), a reader's check, not counted.
4. **The registry counter's first run was a race, not a defect**: 56 rows / 125 registered before the concurrent write, 58 / 129 after, and the four `UNREGISTERED_PATH` lines name exactly the four entry points these rows register — the two rows must land together.
5. **Round-51 defect 5 confirmed and bounded**: with `ASSIMILATE_CITES=all` the round-49 counter passes (exit 0) and the round-50 counter cannot (`4/5`, exit 1); without it they print `2/3` and `3/5`. The `correction:` sentence states both, so a later round does not re-litigate it.
6. **`build-c2-controls.py` was not re-run** (it copies the r52 evidence tree and the staged package into `$TMPDIR` and scores twice); its receipt `controls/c2-controls.txt` records `STAGED`/`TOOLED` both `REF_ID_UNBOUND=31`, `BOUND=0/4`, `C2=FAIL` exit 1, which the draft row cites.
7. **The candidate changed under this seat**: `git status` at 20:06 showed only `SKILL.md` dirty, so `tools/capture-text.py` was the `804a453` blob `3986a971…`; at 20:10 it is `M`, blob `1726cd04…`, with a `w:document` root check — not my write. C1 still prints `LEGS=9/9` on the new blob, but the two readers now diverge on a non-Word main part (tool `REFUSED` exit 2, `build-spans.docx_text` returns `''`), which no leg tests; the draft row's `2` cell names the check so an operator is not surprised, and the L1 must decide whether it joins the frozen predicate (it does not contradict it — a workbook main part is outside the written rule).

## Out of scope / not done

- No write to `SKILL.md`, `corpus/`, `tools/`, the index or jj state (the rows stay in the fenced block); no entry, quote, span or lesson drafted (other seats); no tool installed, `pacman` untouched.
- No network: the `.docx`, PDF, HTML and OLE captures are on-disk cache bytes; `build-c2-controls.py` not run (finding 6) and round-52 C2 not measured against entries (they are absent: `ENTRIES=0/3`). Boundary note: one exploratory refusal run captured stderr in `/tmp/e` (a few hundred bytes) before I switched every later capture to `$S`; all scratch is under `/fast/scratch/hyaku/chousa-r52/R52DraftSkillGates` and is removed.

VERDICT: drafted and grounded both r52 Gates rows (capture-text: 0/1/2 exits, the text-form rule,
OLE/PDF/HTML refusals, `--locate` 0/1/2+/empty cases, NIPH `16fc8c55…`/19682 chars/8996; round-52
counters: C1 `LEGS=9/9` pass and 4/9–0/9 controls, C2 `ENTRIES=0/3` fail on an empty tree,
`build-spans` exit 2 without input, `NO_BASE_OR_REGISTER` scoped to the lane) plus the defect-5
`correction:` sentence (r49 `C1=PASS` exit 0 / r50 `LEGS=4/5` exit 1 under
`ASSIMILATE_CITES=all`), and found the tree already carrying a non-seat pair of r52 rows
(`GATES_ROWS` 56→58, `REGISTERED` 125→129) for the L1 to resolve, plus two counter defects
(`--work` exits 1 with a traceback; `--root` does not redirect `BASE_REV`).

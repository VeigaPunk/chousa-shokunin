# R52W2DraftScorecardVerdict — the round-52 SCORECARD block (draft)

Seat: leaf, no subagents. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip `d1d972c` (landed lane commit
`e769c037`, base `00f8c7f5`, freeze `37468ead`). Scratch `/fast/scratch/hyaku/chousa-r52/R52W2DraftScorecardVerdict/`
(`TMPDIR` exported there; removed at exit). Attacked: the round-52 claims table's before→after cells, the five axis
verdicts, the capability pointer, and the round-53 candidate list — every number below is from a run I made at the tip,
because round 51's block is the shape and its numbers are not inherited.

## Receipts (commands and observed output, run at `d1d972c`)

```
$ python3 corpus/evidence/round52/c1-count.py                         # rc=0
PARAS=PASS ok / RUNS_ENTITIES=PASS ok / REVISIONS=PASS ok / LAYOUT=PASS ok
ALTCONTENT=PASS ok / MAIN_PART=PASS ok / LOCATE=PASS ok / REFUSE=PASS ok
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9
C1=PASS
$ for i in 1 2 3; do python3 .../c1-count.py; done; python3 .../c1-count.py --seed 7
LEGS=9/9 C1=PASS  ×3 (fresh nonces) · LEGS=9/9 C1=PASS (seeded)   # rc=0 each
$ python3 corpus/evidence/round52/c1-supplement.py                    # rc=0
PREFIX=PASS ok / RELS_FORM=PASS ok / SYNTAX=PASS ok / REAL_TEXT=PASS rc=0 chars=19682
SUPPLEMENT_LEGS=4/4 · C1_SUPPLEMENT=PASS      (--seed 7: same, rc=0)
$ python3 .../c1-count.py --tool .../controls/forge-shape.py          # rc=0
REAL=PASS rc=0 count=1 locate=(0, 1, 0) chars=21
LEGS=9/9 · C1=PASS
$ python3 .../c1-supplement.py --tool .../controls/forge-shape.py     # rc=1
PREFIX=FAIL g_paras: text differs at 27 (got 135 chars, want 141) / RELS_FORM=FAIL rc=2
SYNTAX=FAIL rc=2 / REAL_TEXT=FAIL rc=0 chars=21
SUPPLEMENT_LEGS=0/4 · C1_SUPPLEMENT=FAIL
$ python3 .../c1-count.py --tool controls/{naive-tool,cache-txt-tool,const-tool}.py
naive-tool -> LEGS=4/9 C1=FAIL · cache-txt-tool -> LEGS=0/9 C1=FAIL · const-tool -> LEGS=0/9 C1=FAIL
$ python3 corpus/evidence/round52/c2-count.py                          # rc=0
ENTRIES=3/3 · BOUND=4/4 (min 3) REFUSED=0 · BOUND_IDS=S113,S114,S115,S116 · REF_ID_UNBOUND=0
NEW_GROUND=3/3 · QUOTE_ROWS=38 ON_BOUND=38/38 · SPAN_IDS=4/4 (min 3 each)
QUOTES_IN_SPAN=38/38 · QUOTES_IN_ENTRY=38/38 · QUOTES_IN_LESSON=38/38
QUOTE_SHORT=38/38 · SPAN_CONTEXT=38/38 · CAPTURE_BOUND=38/38 · SUBSTANCE=PASS
ANCHOR_BOUND=4/4 · INFERENCE_GROUNDED=3/3 · QUARANTINE_VERDICTS=1/1 (S120)
QUARANTINE_BLOCKED_ADOPTED=0 · C2=PASS
$ python3 corpus/evidence/round52/c2-count.py --lane-only              # rc=0, CAPTURE_BOUND=skipped, C2=PASS
$ python3 corpus/evidence/round52/build-spans.py --check --root <lane>  # rc=0
SPANS_ROWS=38 STALE=0
$ python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51      # rc=1
R46 axes lane=6 verifier=6 · R47 operability: lane=improved verifier=harmed · R47 axes 6/6
R48 UNPARSED lane_axes=6 verifier_axes=0 · R49 axes 6/6
R50 calibration: lane=improved verifier=unchanged · R50 axes 6/6 · R51 axes 6/6
VERDICT_GAPS=2 UNPARSED=1
$ python3 tools/capture-text.py .qcache/3a8b45977cd111e45e3980a5.raw --locate '<the three S120 quotes>'
LOCATED count=1 offset=8996 · LOCATED count=1 offset=9020 · LOCATED count=1 offset=9428   # rc=0 each
$ git show 00f8c7f5:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   # 112
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                        # 116
$ awk -F'\t' 'NR>1{print $1}' corpus/evidence/round52/spans.tsv | sort | uniq -c   # 6 S113 · 9 S114 · 14 S115 · 9 S116
$ git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5 -- corpus/knowledge   # no output, rc=1
$ ls corpus/evidence/round52/measure*          # ls: cannot access ... rc=2 (absent); round51/measure-after.txt exists
$ ls -l tools/capture-text.py                  # -rwxr-xr-x 6201 bytes, 142 lines
```

## Findings

1. **C1's verdict is `improved narrowly`, by the seat spec's own rule and by measurement.** The frozen counter is
   forgeable: `controls/forge-shape.py` scores `LEGS=9/9` and its REAL leg passes with `chars=21` against a pinned
   capture of 19,682 characters — the leg checks the tool against itself (`count=1` of its own stub), so a forged
   tool's REAL line certifies nothing. The supplement refuses the same forge `0/4`, but it is post-freeze
   (`claims-erratum.md` E1) and therefore not the claim's rule.
2. **The REAL leg's self-consistency is the mechanism, not an accident of the forge.** Observed directly: the same
   leg prints `locate=(0, 1, 8996) chars=19682` for the landed tool and `locate=(0, 1, 0) chars=21` for the forge,
   both `PASS`. QUALITY 88 names this; the scorecard must not turn the supplement's `4/4` into the claim's verdict.
3. **C2 is `improved` as presence and binding only, and its refusal arm is unwitnessed.** At the tip all four
   documents bind (`BOUND=4/4 REFUSED=0`), so the predicate's "every other one is REFUSED … `refused-doc` line"
   half is not exercised by this round's data (`grep -c refused-doc corpus/lessons/round-52.md` → 1, and that
   occurrence is prose about round 51's refused-doc paragraph). Entailment is uncounted by the claim's own text;
   `S113` is a second carrier and earns no coverage credit (`corpus/lessons/round-52.md:55`).
4. **The lesson's Census cites a receipt that does not exist.** `corpus/lessons/round-52.md:140` points at
   `corpus/evidence/round52/measure-after.txt`; `ls corpus/evidence/round52/measure*` → rc 2 (round 51's
   `measure-after.txt` is present, round 52's is not). No counter reads it, so no claim moves; the draft below
   says so in its own words and cites no such file.
5. **Calibration is `improved narrowly`, and the gap is visible not closed.** `verdict-gap.py --from 46 --to 51`
   prints `R47 operability: lane=improved verifier=harmed`, `R48 UNPARSED`, `R50 calibration: lane=improved
   verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1` rc 1. I checked the lesson before writing this: line 88 names
   all three (R47, R48, R50) — no under-report, contrary to what the truncated line first suggested.
6. **QUALITY 89's "shown able to fail" claim reproduces.** The three S120 verdict quotes re-locate at 8996 / 9020 /
   9428 with `count=1` each in the capture-text form; the round-51 offset 39411 is not a contiguous offset.
7. **Lane-root hygiene, wave-2 instance (not mine, not deleted).** `git status --porcelain` shows untracked
   `forge.out` (202 B, 20:24), `naive.out` (383 B, 20:24), `sup-forge.out` (187 B, 20:25), `sup-naive.out` (274 B,
   20:25) at the lane root — the wave-1 fleet-root stray class, now inside the lane, written by some wave-2 seat
   with a relative redirect. My own runs wrote only into `$TMPDIR`. It touches no counter.
8. **Coverage and adjacency hold on my own checks.** Base grep for the three theme terms finds nothing in
   `corpus/knowledge` (rc 1); rows 112 → 116; 38 span rows at 6/9/14/9 across the four ids; W1 `R52ConnSiblings`
   prints "NO OVERLAP" over 20 sibling lanes × 13 terms. Freshness is the cache's newest mtime, 2026-10-24 23:26.

## Draft — `SCORECARD.md` (append at EOF, after line 2660; one fenced block)

```SCORECARD.md
## Round 52 verdict — 2026-10-26 (OOXML capture text form; three search-record notes on four documents; lane-vs-verifier verdict gap)

Claims frozen in `corpus/evidence/round52/claims.md` at `37468eadd8d098e80289b2f31a22de3872d4a1f6` before any round-52 seat existed; errata `corpus/evidence/round52/claims-erratum.md` E1–E4. Base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`, landed `e769c037`. After-measurement: the counters below re-run at the tip in wave 2 — the round has no `measure-after.txt`; `corpus/lessons/round-52.md:140` cites one that does not exist. No fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability acquisition) | tool absent at base → `LEGS=0/9 C1=FAIL` exit 1; same-interface controls naive 4/9, cache-txt 0/9, const 0/9 → `LEGS=9/9 C1=PASS` exit 0 on three fresh-nonce runs and `--seed 7`; supplement `SUPPLEMENT_LEGS=4/4` | `python3 corpus/evidence/round52/c1-count.py`; `python3 corpus/evidence/round52/c1-supplement.py` | **improved narrowly**: the frozen counter is forgeable — `controls/forge-shape.py` scores 9/9 with a 21-character REAL stub, because that leg checks the tool against itself — and the supplement that refuses it 0/4 is post-freeze, not the claim's rule, and passable by a tool that reimplements the text form | plumbing |
| C2 depth (sourced) | `ENTRIES=0/3 BOUND=0/4 C2=FAIL` exit 1; staged-entry control `REF_ID_UNBOUND=31 BOUND=0/4` → `ENTRIES=3/3 BOUND=4/4 QUOTE_ROWS=38 CAPTURE_BOUND=38/38 SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 C2=PASS` exit 0 | `python3 corpus/evidence/round52/c2-count.py` (`--lane-only` prints `CAPTURE_BOUND=skipped`) | **improved** as presence and binding; entailment is uncounted (the claim says so before data), one document is a second carrier and earns no coverage credit, and the claim's refusal arm is unwitnessed at the tip (`REFUSED=0`) | ground |

The numeric operability scale stays 3/10; no other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `tools/capture-text.py`, and the post-freeze supplement; the frozen counter is forgeable (`controls/forge-shape.py` → 9/9, REAL `chars=21`) |
| depth | **improved** | C2; three entries on four documents, three credited (`S114`, `S115`, `S116`) |
| calibration | **improved narrowly** | `python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51` → `R47 operability: lane=improved verifier=harmed`, `R48 UNPARSED`, `R50 calibration: lane=improved verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1` rc 1 — the debt is now visible, not closed; the S120 verdict line re-locates at `char 8996` |
| coverage | **improved narrowly** | rows 112 → 116; `git grep` of `文献検索期間`/`完全な検索戦略`/`检索报告清单` at the base finds nothing in `corpus/knowledge`; `corpus/README.md` `## Round52 coverage and frontier` |
| freshness | **unchanged** | newest capture in the campaign cache is 2026-10-24 23:26; no fetch (L0 `8d77e6c1` open) |
| adjacency | **unchanged** | W1 `R52ConnSiblings`: 20 sibling lanes × 13 terms, "NO OVERLAP"; no sibling parses WordprocessingML (wave-2 re-check pending) |

## Capabilities (round-52 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| OOXML `.docx` text form for claim-vs-source checks | prints a WordprocessingML capture's text form on stdout (main part from `_rels/.rels`; run-level `w:tab`/`w:br`/`w:cr`; nothing from `mc:Fallback`, `w:delText`, `w:instrText` or tab stops), locates a quote's offset with `--locate`, and refuses with exit 2 and `REFUSED …` on stderr a non-zip, a relationship-less package, a missing target, a non-Word main part, a part inflating past 256 MiB, and an encrypted or unsupported-compression member | `python3 tools/capture-text.py RAW --locate 'SRにおける文献検索期間について明記する。'` → `LOCATED count=1 offset=8996`; `python3 corpus/evidence/round52/c1-count.py` (`LEGS=9/9`); `corpus/QUALITY.md` 87–90 | 52 |

## Planned — round 53 (not started)

Candidates: apply the adopter twin-id `held` label and registry-refusal-order patch (W1 `R52ExecAdopterTwin`: `SELFTEST=PASS findings=40`, `FIXTURES_SHA256=9822ad59…`, round-50 pin 26/26, round-51 counter 5/5) — it moves the fixtures digest and the SKILL pin, so it needs its own round; land the anchored-correction check (W1 `R52ExecPointerAnchor`: lane `ANCHORED=0/4` rc 1, scratch green 4/4, forged anchor 3/4) as a calibration claim, which needs four append-only anchored `correction:` successors; admit `search-tracking-record-r40.md` with its quote re-cut to the break-free span at char 935; close the two verdict gaps (`R47 operability`, `R50 calibration`) and parse round 48's bullet axes; fold the supplement's representation legs and the pinned NIPH text digest into a successor C1 counter, since the frozen one certifies generator-shape agreement.
```

## Touched surfaces

- Written: this report only. The block above is drafted here for the L1 — `SCORECARD.md`, the counters, the lesson,
  the tool and the entries were read, never edited; no `git`/`jj` mutation, no commit, no fetch, no pacman (paused
  host-wide), no install. Scratch created and removed; nothing else written outside it.

## Out of scope (not attempted here)

The four rows' re-open and the three entries' entailment (reviewer/critic seats), the admission case and the Gate
verdict (L1), the adopter and pointer-anchor patches (landing them changes `tools/` and the fixtures digest), and any
wave-2 connector verdict still running.

VERDICT: attacked the round-52 claims table, axis verdicts, capability pointer and round-53 candidate list by
re-running every counter at the tip — C1 holds `LEGS=9/9` yet is forgeable (forge 9/9 with a 21-char REAL stub,
supplement 0/4), C2 holds `BOUND=4/4 QUOTE_ROWS=38 CAPTURE_BOUND=38/38` with its refusal arm unwitnessed, the
verdict-gap check reports 2 gaps + 1 unparsed, and the lesson cites one receipt that does not exist
(`corpus/evidence/round52/measure-after.txt`) — so the draft carries `improved narrowly` / `improved` and no
inherited number.

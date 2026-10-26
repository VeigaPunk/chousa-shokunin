# R52W2ExecReplayAll — replay every counter from committed bytes (round 52, wave 2)

Seat: `R52W2ExecReplayAll` (leaf). Lane replay target `e769c03738d08c36109556ebf301a1db0dcf143d` (base
`00f8c7f5272a1d98b6d34913985fa4537e00aaf9`, freeze `37468eadd8d098e80289b2f31a22de3872d4a1f6`). All work in
`/fast/scratch/hyaku/chousa-r52/R52W2ExecReplayAll` (clone, base export, base-git clone, two mutation clones;
`TMPDIR` there; removed at exit). No lane, fleet or `shokuknow` write; captures opened read-only.

Replay root: `git clone -q --shared … $S/clone && git -C $S/clone checkout -q e769c037…` → `rev-parse HEAD`
`e769c037…`, toplevel `$S/clone`. Lane reference tree `d1d972cf…`, `git status --porcelain` only untracked
`.ufo/waves/round-52/w2*` dispatch files (plus sibling seats' stray outputs, §4).

## 1. Replay table — every seat-listed counter, clone (committed bytes) vs lane working tree

| # | command (cwd = clone or lane root) | clone exit · verdict | lane exit · verdict | same? |
|---|---|---|---|---|
| 1 | `python3 corpus/evidence/round52/c1-count.py` | 0 · `LEGS=9/9` `C1=PASS`; REAL `rc=0 count=1 locate=(0, 1, 8996) chars=19682` | 0 · identical | yes |
| 2 | `c1-count.py --seed 7` | 0 · `LEGS=9/9` `C1=PASS` (same REAL line) | 0 · identical | yes |
| 3 | `c1-supplement.py` | 0 · `SUPPLEMENT_LEGS=4/4` `C1_SUPPLEMENT=PASS`; `REAL_TEXT=PASS rc=0 chars=19682` | 0 · identical | yes |
| 4 | `c2-count.py` | 0 · `ENTRIES=3/3 BOUND=4/4 REFUSED=0 BOUND_IDS=S113,S114,S115,S116 REF_ID_UNBOUND=0 NEW_GROUND=3/3 QUOTE_ROWS=38 ON_BOUND=38/38 SPAN_IDS=4/4 QUOTES_IN_SPAN=38/38 QUOTES_IN_ENTRY=38/38 QUOTES_IN_LESSON=38/38 QUOTE_SHORT=38/38 SPAN_CONTEXT=38/38 CAPTURE_BOUND=38/38 SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 (S120) QUARANTINE_BLOCKED_ADOPTED=0 C2=PASS` | 0 · identical | yes |
| 5 | `c2-count.py --lane-only` | 0 · same tally, `CAPTURE_BOUND=skipped`, `C2=PASS` | 0 · identical | yes |
| 6 | `build-spans.py --root $S/clone --check` | 0 · `SPANS_ROWS=38 STALE=0` | 0 · identical | yes |
| 7 | `python3 corpus/evidence/round51/quote-substance-check.py corpus/evidence/round52/spans.tsv` | 0 · `IDS=4 QUOTES=38 FAILURES=0` | 0 · identical | yes |
| 8 | `python3 corpus/evidence/round47/c2-count.py` (gate registry) | 0 · `ENTRY_POINTS=132 (abc=103 dependence=+8 check_named=+21) FLOOR=92 GATES_ROWS=58 REGISTERED=132/132 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS` | 0 · identical | yes |
| 9 | `verdict-gap.py --from 46 --to 51` | **1** · `VERDICT_GAPS=2 UNPARSED=1` (`R47 operability: lane=improved verifier=harmed`, `R50 calibration: lane=improved verifier=unchanged`, `R48 UNPARSED lane_axes=6 verifier_axes=0`) | 1 · identical | yes |
| 10 | `python3 corpus/evidence/round52/controls/build-c2-controls.py` (spec path is round-52-relative; committed at `corpus/evidence/round52/controls/`) | 0 · STAGED `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL exit=1`; TOOLED `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL exit=1` | 0 · identical | yes |
| 11 | `bash …/scripts/sources-census.sh validate --file corpus/SOURCES.md` | 0 · `ok`, five W04 (S051, S053, S073, S074, S075) | 0 · identical (`--root … chousa` form too) | yes |

Also replayed from committed bytes (not on the seat list, same tree):

| # | command | clone exit · verdict |
|---|---|---|
| 12 | base export `git archive 00f8c7f \| tar -x -C $S/base` + `c1-count.py --tool $S/base/tools/capture-text.py` | 1 · `LEGS=0/9 C1=FAIL` (`REAL=FAIL tool absent`); `ls` → `base/tools/capture-text.py: No such file` |
| 13 | `c2-count.py --root $S/basegit` (clone at `00f8c7f`) | 1 · `ENTRIES=0/3 BOUND=0/4 REFUSED=0 NEW_GROUND=0/3 INFERENCE_GROUNDED=0/3 QUARANTINE_VERDICTS=0/1 (S120) C2=FAIL` — byte-equal to `controls/c2-before.txt` body |
| 14 | `c1-count.py --tool controls/{naive,cache-txt,const}-tool.py` | 1 / 1 / 1 · `LEGS=4/9` / `0/9` / `0/9` — verdict lines equal to `controls/c1-before.txt` |
| 15 | `git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f -- corpus/knowledge` | 1 · no output (README "Base sweep") |
| 16 | `build-c2-controls.py` body vs committed `controls/c2-controls.txt` | diff = only the receipt's two header lines (`# round-52 C2 do-nothing controls…`, `$ python3 …`); every measurement line equal |

**Differences vs the lane working tree: none**, in any verdict line or exit code (all eight paired outputs
diffed `SAME` after temp-path normalisation; #9–#11 equal). Why: `git diff --stat e769c03 d1d972c` is
`only .ufo/waves/round-52/{gen-w2-spec.py,w2-dispatch.json,w2-spec.json,w2-run.err}` and `git status` shows no
tracked modification, so the working tree's tracked bytes — all a counter reads — are the lane-commit bytes.

## 2. What I attacked, and the result

- **A1 frozen artifacts since the freeze** — `git diff --stat 37468ea e769c03 -- claims.md c1-count.py
  c2-count.py build-spans.py`: empty; only `SOURCES.md +4`, `quotes.tsv +39`, `spans.tsv +39` (C2 deliverables).
  Predicates and counters are the frozen bytes. **Holds.**
- **A2 the counters read committed bytes only** — the clone (no working-tree extras) reproduces all eleven runs;
  `c1-count.py` has no reference to `knowledge|SOURCES|quotes.tsv|spans` (`grep -n` → empty). **Holds.**
- **A3 the REAL kill rule is live** — in `$S/mut` I changed one hex char of `REAL_SHA` (16fc8c55→16fc8c56):
  `REAL=FAIL pinned capture missing or digest differs`, `LEGS=8/9`, `C1=FAIL`, exit 1. The capture's own digest
  is `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763` (`sha256sum
  .qcache/3a8b45977cd111e45e3980a5.raw`), equal to the pinned constant. **Holds.**
- **A4 the supplement's pinned text digest is independently reproducible** — `tools/capture-text.py <raw>` →
  19,682 chars, `sha256 754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9`; `build-spans.py`
  `docx_text` → `chars 19682 sha256 754aae42…`, `same True`; `c1-supplement.py` `TEXT_SHA` is that value. **Holds.**
- **A5 the E1 forge, replayed against both counters** — `c1-count.py --tool controls/forge-shape.py` →
  `REAL=PASS rc=0 count=1 locate=(0, 1, 0) chars=21`, `LEGS=9/9`, `C1=PASS` exit 0 (E1's premise true);
  `c1-supplement.py --tool controls/forge-shape.py` → `SYNTAX=FAIL g_paras: rc=2`, `REAL_TEXT=FAIL rc=0
  chars=21`, `SUPPLEMENT_LEGS=0/4`, `C1_SUPPLEMENT=FAIL` (lesson mistake 3 / QUALITY 88 "shown able to fail"
  true). **Holds, and the frozen counter's vacuity on representation is confirmed, as disclosed.**
- **A6 the claim's separability (C2 does not run the C1 tool)** — with `tools/capture-text.py` moved out of the
  clone, `c2-count.py` still prints `CAPTURE_BOUND=38/38 … C2=PASS` exit 0; restored, `git status` clean.
  **Holds.**
- **A7 `build-spans.py --check` is not vacuous** — in `$S/mut2`: one offset digit changed in `spans.tsv` →
  `SPANS_ROW_STALE spans/S113-2.txt`, `STALE=1`, exit 1; one byte appended to `spans/S113-1.txt` →
  `SPANS_FILE_STALE spans/S113-1.txt`, `STALE=1`, exit 1; `git checkout --` restores clean. **Holds.**
- **A8 all 38 span rows re-derived independently from the committed manifest + cache** (my script, not
  `build-spans.py`): each `capture_sha256` names a cache file by `sha256(url)[:24]`, each committed span file is
  the exact slice at the recorded `offset` of the derived form — `rows 38 BAD 0`; per-id `S113 6, S114 9,
  S115 14, S116 9` (≥3 each). Quotes ≤25 whitespace words / ≤160 chars, present in entry and lesson: 0
  violations. Every `char N` in an `anchor` cell is a quote offset of that id (S113 `2034,2328,2433,3139,4850`;
  S114 `1650,1707,1785,5530`; S115 `8996,9020,9408,9419,9428`; S116 `475,592,641,753`) — all **OK**. Entries carry
  only bound `S###` tokens (9/10/19/6) and one `source: S11x — <url>` line each. **Holds.**
- **A9 before/control receipts** — #12–#16 reproduce. Named limit: the per-leg `want N chars` numbers inside
  `controls/c1-before.txt` do **not** (fresh random text per run, e.g. naive REVISIONS `want 40`→`got 48`);
  every `PASS/FAIL` and `LEGS=` line does, and the claim uses only `LEGS=`.
- **A10 census** — both forms exit 0 (`ok`), same five pre-existing W04; rows `112` at base → `116` at
  `e769c03`; new-row tiers `S114 A, S115 A, S113 B, S116 B` (lesson's "A S114 S115; B S113 S116"). **Holds.**
- **A11 verdict-gap exit 1 is correct behaviour, not drift** — the two gaps are real disagreements in the
  files it reads: `SCORECARD.md` R47 axis row `operability … **improved, disputed as a trade**` vs
  `corpus/lessons/round-47-verifier-spotcheck.md:35` `| operability | **harmed** …`; SCORECARD R50
  `calibration | **improved narrowly**` vs verifier R50 `| calibration | unchanged |`; R48's verifier writes
  axes as bullets → `UNPARSED`. The tool's own docstring: exit 1 when a gap or an unparsed round exists.
- **A12 DEFECT D1 (landed lesson citation)** — `corpus/lessons/round-52.md:140` cites
  `corpus/evidence/round52/measure-after.txt`: absent at `e769c03` (`git ls-tree -r --name-only e769c03 | grep
  round52/measure-after` → nothing; `git log --all -- …/round52/measure-after.txt` → empty, never committed) and
  absent on the lane FS (`ls` → ENOENT). Rounds 40–51 each have one; round 52's sibling `census-start.txt` is
  committed. The claim is true (my re-run gives `exit=0`, `ok`, five W04) but its receipt is missing. Fix (L1):
  commit the L1's census output, or cite `census-start.txt`.
- **A13 spec-vs-tree path** — the seat text's `controls/build-c2-controls.py` is
  `corpus/evidence/round52/controls/build-c2-controls.py` (no top-level `controls/`); correct in context.
- **A14 gate registry** — `round47/c2-count.py` `REGISTERED=132/132 MISMATCHES=0`, i.e. the round-52 additions
  (Gates rows, README block, entry points) did not break the registry its checks depend on. **Holds.**

## 3. Located quote used above

`SRにおける文献検索期間について明記する` — capture-text text form of `.qcache/3a8b45977cd111e45e3980a5.raw`
(S115), `count=1`, first offset **char 8996** (19,682-char form), and `--locate` prints
`LOCATED count=1 offset=8996` (independent `str.find` agrees). 13 whitespace words.

## 4. Named limits of this replay

- Randomized counters: `c1-count.py`/`c1-supplement.py` receipts keep their `PASS/FAIL` and leg counts
  reproducible, never their per-leg character counts (nonce text).
- `quote-substance-check.py` tolerates extra bytes appended to a span file (`FAILURES=0` on the tampered
  `S113-1.txt`); byte-exactness is `build-spans.py --check`'s leg (`STALE=1` in the same run) — not a defect.
- C2 measures binding and presence, not entailment (frozen; E4); this seat judged replay, not the entries.
- Scope (not mine, not touched): five untracked outputs sit at the lane root from sibling wave-2 seats —
  `forge.out`, `naive.out`, `sup-forge.out`, `sup-naive.out`, `s115form.txt`; quarantine before the lane commit.

**VERDICT: I attacked the landed wave-1 products by replaying all eleven seat-listed commands plus six
before/control/mutation runs from a clean clone of `e769c03` — every counter, check, control and before-receipt
reproduces with the documented verdict and exit code (9/9 & 4/4 C1 PASS, C2 PASS with 38/38 on every quote leg,
`STALE=0`, `MISMATCHES=0`, verdict-gap exit 1 by design), no result differs from the lane tree because
`e769c03→d1d972c` touches only `.ufo` dispatch files, and mutation runs show the C1 REAL digest leg, the
supplement's pinned text digest and `build-spans --check` all fail when their pinned input is altered; the one
defect found is a dangling citation, `corpus/lessons/round-52.md:140` naming a `measure-after.txt` that was
never committed.**

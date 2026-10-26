# R52W2CritAxisC1 — C1 as an axis move

Seat: R52W2CritAxisC1. Attacked: **C1's axis claim** — is `tools/capture-text.py` an
operability move or plumbing; which lane workflows call it; does it move the round-1
operability observable (SCORECARD.md:7, 3/10); are C1 and C2 causally separable as
claims.md asserts. All commands ran in the scratch clone at the TIP commit
`e769c03738d08c36109556ebf301a1db0dcf143d` (`git rev-parse e769c037…` confirmed;
`git rev-parse --show-toplevel` = the fixture) with `TMPDIR=$S`. No tool installs were
needed (system `python3`; nothing installed). No network/fetch.

## 1. Baseline at TIP (both counters pass)

```
$ cd $S/clone; TMPDIR=$S python3 corpus/evidence/round52/c2-count.py   # rc=0
QUOTES_IN_SPAN=38/38 … CAPTURE_BOUND=38/38 SUBSTANCE=PASS ANCHOR_BOUND=4/4
INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 (S120) C2=PASS
$ TMPDIR=$S python3 corpus/evidence/round52/c1-count.py                # rc=0
PARAS=PASS … REFUSE=PASS REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9 C1=PASS
```

## 2. Causal separability (claims.md lines 12–18) — both directions hold at TIP

**A. Delete `tools/capture-text.py`, run C2 → still PASS:**
```
$ git rm -q tools/capture-text.py
$ TMPDIR=$S python3 corpus/evidence/round52/c2-count.py   # rc=0
INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 (S120) C2=PASS
```
(`grep -c capture-text` on the output → 0.) Grep: `c2-count.py` and `build-spans.py`
carry no reference to the tool — the only hit is a comment, `build-spans.py:15`
("claim is verifiable without the C1 tool `tools/capture-text.py`"); `c2-count.py`
loads the builder via `importlib` (`c2-count.py:88-92`) and reads the pinned cache
(`c2-count.py:57`).

**B. Delete the three entries, run C1 → still PASS:**
```
$ git rm -q corpus/knowledge/japanese-search-record-niph-form-r52.md \
           corpus/knowledge/japanese-prisma-item-wording-r40.md \
           corpus/knowledge/chinese-prisma-s-reception-r52.md
$ TMPDIR=$S python3 corpus/evidence/round52/c1-count.py   # rc=0
PARAS=PASS … REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9 C1=PASS
```
`grep -n "knowledge\|SOURCES\|entries"` over `c1-count.py` → empty; the counter's only
external input is the pinned `REAL_RAW` NIPH capture (`c1-count.py:46`, absolute cache
path). The claim's separability sentence reproduces exactly.

Note (expected): `c1-supplement.py` — part of C1's own counter family, not C2 — depends
on the tool: with it absent `SUPPLEMENT_LEGS=0/4 C1_SUPPLEMENT=FAIL`; restored, `4/4
C1_SUPPLEMENT=PASS`.

## 3. Runnable artefact vs scorecard observable

**It is a runnable artefact producing its stated outcome on the lane's real inputs.**
The REAL leg runs the actual NIPH capture (`3a8b45977cd111e45e3980a5.raw`): exit 0,
19682 characters, `SRにおける文献検索期間について明記する。` exactly once at offset 8996.
Cross-check of the two readers (claim note, claims.md lines 16–18):
```
$ python3 tools/capture-text.py $RAW > niph-tool.txt
$ python3 - <<'EOF' > niph-builder.txt   # import build-spans.docx_text
$ cmp niph-tool.txt niph-builder.txt && echo READERS_AGREE     # READERS_AGREE
$ sha256sum niph-tool.txt   # 754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9
$ python3 -c "t=open('niph-tool.txt').read(); print(len(t),t.find('SRにおける文献検索期間について明記する。'))"
# 19682 8996
```
Byte-identical output; the digest equals E1's `TEXT_SHA` (`c1-supplement.py:47`).

**But it does not move the round-1 operability observable.** SCORECARD.md:7 is
unchanged: `| operability | 3 | … | 1 |` (last-change round 1); the score definition
(SCORECARD.md:12-13) counts only the three archive inputs that exit 1 with exactly one
`RESEARCH_GATE: DRIFT` summary through `tools/research-gate.sh` (counting command,
SCORECARD.md:29), which capture-text neither touches nor feeds. SCORECARD.md:2658 still
reads `## Planned — round 52 (not started)` — no round-52 block landed; no scorecard
line references the tool. So C1 is a **capability acquisition**, not a score-moving
operability move — consistent with the claim's own preamble (claims.md line 28:
"lowest scored axis, 3/10; capability acquisition") and tag (claims.md line 64:
"Tag: plumbing").

## 4. Which lane workflows call it now (grep over the landed tree)

Callers: (a) SKILL.md:134 Gates row `capture-text` (tool row; usage, `--locate`,
exit codes 0/1/2); (b) the S115 entry — `japanese-search-record-niph-form-r52.md:3`
(source, `text form python3 tools/capture-text.py`), `:4` (verified-at), `:5`
(recheck command), `:29` (searcher-sweep command); (c) the lesson — round-52.md:75-77
(S120 verdict lines, `form capture-text`, offsets 8996/9020/9428), :48, :60, :111-124
(quarantine/form tables); (d) QUALITY.md:917 (criterion 87) and :921 (criterion 89)
check commands; (e) `c1-count.py:248` and `c1-supplement.py:131` (default `--tool`).
Non-callers: `build-spans.py` (own `docx_text` reader, build-spans.py:75-106),
`c2-count.py`, `tools/inference-ground.py` (grep: no reference), `research-gate.sh`.
So the tool is exercised by real lane workflows (entry rechecks, lesson verdicts, skills
Gates) and by C1's own counters; no other automated measurement depends on it.

## Verdict

C1's axis: `tools/capture-text.py` is a genuine, reproducible runnable capability (real
NIPH input: 19682 chars, offset 8996, readers agree), used by the S115 entry, the
lesson's S120 verdicts and SKILL.md Gates — but it does **not** move the round-1
operability observable (SCORECARD.md:7 stays 3/10, round 1), and C1/C2 are causally
separable exactly as claims.md states: deleting the tool leaves C2=PASS, deleting the
three entries leaves C1=PASS 9/9 at TIP e769c037.

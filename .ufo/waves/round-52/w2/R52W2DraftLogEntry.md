# R52W2DraftLogEntry — round-52 LOG entry, drafted against the landed lane

Seat: scribe (draft only). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, lane tip `d1d972c`
(round-52 integration `e769c03738d08c36109556ebf301a1db0dcf143d`, base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`,
freeze `37468eadd8d098e80289b2f31a22de3872d4a1f6`, C1 candidate `804a45370dc992bfe714817281535055c2f9b032`).
Scratch `/fast/scratch/hyaku/chousa-r52/R52W2DraftLogEntry`, `TMPDIR` pinned there and removed before hand-off.
No tool installs (pacman is host-paused; nothing was needed). Nothing written outside this report.

## What I attacked, and the result

| attacked (wave-1 / landed artifact) | how | result |
|---|---|---|
| C1 "after" claim (`claims.md` R52-C1 target) | ran the frozen counter at the tip three times, fresh nonces | holds: `LEGS=9/9 C1=PASS` ×3, `REAL=PASS … chars=19682 locate=(0, 1, 8996)` |
| C1 "before" receipt (`controls/c1-before.txt`) | read it; re-derived the base row count independently | holds: tool absent at base, `LEGS=0/9 C1=FAIL exit=1` |
| the three cheap controls | ran all three through **both** counters | holds: 4/9 (naive), 0/9 (cache-txt), 0/9 (const); supplement 0/4 for each |
| E1 forge claim "the frozen counter is forgeable" | ran `controls/forge-shape.py` (85 lines) | holds: `LEGS=9/9` on the frozen counter, `SUPPLEMENT_LEGS=0/4` on the supplement |
| the supplement's "real tool 4/4" | ran it at the tip | holds: `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS`, `REAL_TEXT=PASS chars=19682` |
| C2 "after" claim | ran the frozen C2 counter at the tip | holds: `C2=PASS`, `BOUND=4/4 (min 3) REFUSED=0`, all legs `38/38`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=4/4`, `INFERENCE_GROUNDED=3/3`, `QUARANTINE_VERDICTS=1/1 (S120)` |
| C2 "before" + controls | read `controls/c2-before.txt`, `controls/c2-controls.txt` | holds: base `ENTRIES=0/3 BOUND=0/4 C2=FAIL`; both controls `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL` |
| span manifest (lesson "38 quotes, STALE=0") | `build-spans.py --check` at the lane root | holds: `SPANS_ROWS=38 STALE=0` exit 0 |
| registry growth 112 → 116 | counted rows at tip and at base | holds: 116 / 112; S113–S116 present at `SOURCES.md:123-126` |
| S120 re-location (lesson `## Quarantine slice`) | `tools/capture-text.py --locate` on the three verdict quotes | holds: `count=1 offset=8996`, `9020`, `9428` |
| SKILL row digest pins (`SKILL.md:134`) | hashed the NIPH raw and its text form | holds: raw `16fc8c55…b09763`, text form `754aae42…f24b0d9`, 19,682 chars |
| verdict-gap implementation | ran `--from 46 --to 51` and `--from 51 --to 51` | holds: `VERDICT_GAPS=2 UNPARSED=1`; round 51 alone `VERDICT_GAPS=0 UNPARSED=0` |
| lesson `## Census` round-end receipt | `git ls-files corpus/evidence/round52/`, `find . -name 'measure-after*'` | **FAILS**: `corpus/evidence/round52/measure-after.txt` does not exist (see Findings 1) |

## Draft — intended lane path `LOG.md`, appended after line 1831 (Round 51 entry), 12 physical lines

```markdown
## Round 52 — the OOXML `.docx` text form and the NIPH form re-grounded; the search-record theme continued by document (2026-10-26)

Evidence that motivated the round: the round-51 closure's routed defects (`corpus/lessons/round-51-verifier-spotcheck.md` section 6 — a forgeable C1 counter, and a `.docx` refused "for its capture form") and the SCORECARD round-52 plan. Claims frozen at `37468eadd8d098e80289b2f31a22de3872d4a1f6` after their do-nothing controls were scored (`corpus/evidence/round52/claims.md`, `controls/`); C1 candidate `804a45370dc992bfe714817281535055c2f9b032`, integration `e769c03738d08c36109556ebf301a1db0dcf143d` on base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`; errata E1–E4 in `claims-erratum.md`. No external fetch (L0 `8d77e6c1` open).

- **C1 operability (capability acquisition).** `python3 tools/capture-text.py RAW [--locate QUOTE]` prints the text form of an OOXML WordprocessingML capture — main part from the `_rels/.rels` relationship whose Type ends `/officeDocument`, `w:t` text with entities decoded, run-level `w:tab`/`w:br`/`w:cr` as tab/newline/newline, a newline per `w:p`, nothing from `mc:Fallback`, `w:delText`, `w:instrText` or `w:pPr/w:tabs` — and prints a quote's code-point offset. Frozen counter `python3 corpus/evidence/round52/c1-count.py`: at the base `LEGS=0/9 C1=FAIL` exit 1 (tool absent, `controls/c1-before.txt`); at the lane tip `LEGS=9/9 C1=PASS` on three independent runs, `REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682`. Same-interface controls: `naive-tool.py` (member strip) `LEGS=4/9`, `cache-txt-tool.py` (the `.txt` sidecar) `0/9`, `const-tool.py` `0/9`. The frozen counter is forgeable in one shape — the 85-line `controls/forge-shape.py` scores `9/9` (erratum E1) — so the post-freeze `c1-supplement.py` re-spells the generated documents and pins the NIPH text form's sha256: real tool `SUPPLEMENT_LEGS=4/4`, the forge `0/4` (reported beside the frozen verdict, never instead of it).
- **Post-candidate tool changes (E2).** After `804a4537` the tool went 115 → 142 lines: a main part whose root is not `w:document` is refused (`tools/capture-text.py:97`; two `.xlsx` and an OLE `.doc`'s theme part had printed an empty text form at exit 0), `_rels/.rels` or a main part over 256 MiB and `MemoryError` are refused (`:61`, `:116`; the candidate rendered a 524,901-byte package into 60,000,000 characters), a target normalising outside the package root is refused (`:73`), `el.clear()` runs per end event (`:111`), and encrypted or unsupported-compression members, percent-decoded targets and an empty `--locate` are handled (`:114`, `:74`, `:131`). These add refusal classes the frozen sentence does not list; its own classes and every other behaviour are unchanged and no frozen leg exercises the new ones.
- **C2 depth (sourced).** Three entries adopted by document on four new rows S113–S116 (registry 112 → 116): `japanese-search-record-niph-form-r52.md` (S115, the NIPH template round 51 refused for capture form), `japanese-prisma-item-wording-r40.md` (S116), `chinese-prisma-s-reception-r52.md` (S113, S114). `python3 corpus/evidence/round52/c2-count.py`: `C2=FAIL` at the base (`ENTRIES=0/3 BOUND=0/4`, `controls/c2-before.txt`) → `C2=PASS` at the tip — `ENTRIES=3/3 BOUND=4/4 (min 3) REFUSED=0`, `QUOTE_ROWS=38 ON_BOUND=38/38`, `SPAN_IDS=4/4`, `CAPTURE_BOUND=38/38`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=4/4`, `INFERENCE_GROUNDED=3/3`, `QUARANTINE_VERDICTS=1/1 (S120)`; `build-spans.py --check` → `SPANS_ROWS=38 STALE=0`. Controls (`controls/c2-controls.txt`): the staged entries copied unchanged and rewritten by the adopter each give `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL`. Coverage credit is three documents, not four: the 梅斯医学 record (S113) is a second carrier of a reading the lane already holds through `chinese-search-record-r39.md` (`corpus/README.md:1124`).
- **S120 re-located.** The round-51 quarantine verdict's `char 39411` named an XML form in which the sentence is split across runs; the round-52 verdict line carries offsets in the capture-text form, re-located this wave: `LOCATED count=1 offset=8996`, `9020`, `9428` for its three quotes. Verdict `present` stands; only the offset is superseded (lesson Mistakes row 2, `## Quarantine slice`).
- **Frontier / quality.** Census `sources-census.sh validate --root … chousa` exit 0, `ok`, the same five pre-existing W04 (S051 S053 S073 S074 S075); six mistakes mined in `corpus/lessons/round-52.md` `## Mistakes` (capture-form, reference-drift, vacuous counter, fleet-root stray, non-Word main part, size bomb); QUALITY 87–90 (a capture read through a defined text form before a quote is located or the source refused; a counter that varies representation with one pinned-content leg; a verdict offset re-located in its stated form; a reader that refuses non-target and inflated parts); README block `## Round52 coverage and frontier` (`corpus/README.md:1113`); SKILL.md Gates rows `capture-text` and `chousa round-52 counters and checks` (`SKILL.md:134-135`), with the NIPH capture's pins verified — raw `16fc8c55…b09763`, text form `754aae42…f24b0d9`, 19,682 characters. considerthese pick implemented: `python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51` → `R47 operability: lane=improved verifier=harmed`, `R50 calibration: lane=improved verifier=unchanged`, `R48 UNPARSED`, `VERDICT_GAPS=2 UNPARSED=1` (round 51 alone: `VERDICT_GAPS=0 UNPARSED=0`).
- **Waves.** W1 45 seats, 45 reports (`w1-results.json`, `w1/`); the L1 held the planner seat.
```

## Gates I ran (observed output, at the lane tip unless stated)

```
$ python3 corpus/evidence/round52/c1-count.py --work $S/c1work            # runs 1, 2, 3
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9
C1=PASS                                                                   # exit 0, three times
$ python3 corpus/evidence/round52/c1-supplement.py --work $S/sup1
PREFIX=PASS ok / RELS_FORM=PASS ok / SYNTAX=PASS ok
REAL_TEXT=PASS rc=0 chars=19682
SUPPLEMENT_LEGS=4/4
C1_SUPPLEMENT=PASS                                                        # exit 0
$ for t in naive-tool cache-txt-tool const-tool forge-shape; do c1-count/supplement --tool .../$t.py
c1 naive-tool exit=1 LEGS=4/9 C1=FAIL        sup naive-tool exit=1 SUPPLEMENT_LEGS=0/4 FAIL
c1 cache-txt-tool exit=1 LEGS=0/9 C1=FAIL    sup cache-txt-tool exit=1 SUPPLEMENT_LEGS=0/4 FAIL
c1 const-tool exit=1 LEGS=0/9 C1=FAIL        sup const-tool exit=1 SUPPLEMENT_LEGS=0/4 FAIL
c1 forge-shape exit=0 LEGS=9/9 C1=PASS       sup forge-shape exit=1 SUPPLEMENT_LEGS=0/4 FAIL
$ python3 corpus/evidence/round52/c2-count.py
ENTRIES=3/3 · BOUND=4/4 (min 3) REFUSED=0 · BOUND_IDS=S113,S114,S115,S116 · REF_ID_UNBOUND=0
NEW_GROUND=3/3 · QUOTE_ROWS=38 ON_BOUND=38/38 · SPAN_IDS=4/4 (min 3 each) · QUOTES_IN_SPAN=38/38
QUOTES_IN_ENTRY=38/38 · QUOTES_IN_LESSON=38/38 · QUOTE_SHORT=38/38 · SPAN_CONTEXT=38/38
CAPTURE_BOUND=38/38 · SUBSTANCE=PASS · ANCHOR_BOUND=4/4 · INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=1/1 (S120) · QUARANTINE_BLOCKED_ADOPTED=0 · C2=PASS          # exit 0
$ python3 corpus/evidence/round52/build-spans.py --check
SPANS_ROWS=38 STALE=0                                                     # exit 0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa W04 S051/S053/S073/S074/S075 … chousa ok …/corpus/SOURCES.md      # exit 0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 116
$ git show 00f8c7f5:corpus/SOURCES.md | grep -cE '…'                     -> 112
$ sha256sum 3a8b45977cd111e45e3980a5.raw                                 -> 16fc8c55…b09763
$ python3 tools/capture-text.py <raw> | sha256sum                        -> 754aae42…f24b0d9 (19,682 chars)
$ python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51
R47 operability: lane=improved verifier=harmed / R48 UNPARSED lane_axes=6 verifier_axes=0
R50 calibration: lane=improved verifier=unchanged / VERDICT_GAPS=2 UNPARSED=1   # exit 1
$ python3 corpus/evidence/round52/verdict-gap.py --from 51 --to 51        -> VERDICT_GAPS=0 UNPARSED=0
```

Commits read with `git log -1 --format='%h %s'`: `37468ea` frozen claims, `804a453` C1 candidate, `e769c03`
integration (`git diff --stat 804a4537 e769c037 -- tools/capture-text.py` → `32 insertions(+), 5 deletions(-)`).

## Findings

1. **Dangling receipt in the landed lesson (defect, not in my entry).** `corpus/lessons/round-52.md:140` says
   "**Round end:** exit 0, `ok`, the same five W04 warnings (`corpus/evidence/round52/measure-after.txt`)", but that
   file is not in the lane: `git ls-files corpus/evidence/round52/` lists no `measure-after.txt`, and
   `find . -name 'measure-after*'` returns only rounds 40–51. The observation itself is true — I re-ran the census at
   the tip (exit 0, `ok`, same five W04, 116 rows) — so this is a pointer defect of the class the round's own
   Mistakes rows 2 and 6 name. The draft entry above therefore cites no round-end receipt file. One-line fix for the
   L1 (intended lane path `corpus/lessons/round-52.md:140`): cite the command instead, or land the receipt.
2. C2's `REFUSED` branch is empty at the tip (`BOUND=4/4 REFUSED=0`): the claim's "every other one is REFUSED" clause
   is satisfied vacuously, and `refused-doc` lines in the lesson belong to the Gate decisions, not to the counter.
   Stated in the entry as measured (`BOUND=4/4 … REFUSED=0`), not as "3 bound and 1 refused".
3. **Four untracked strays at the lane root, written 20:24–20:25 by another wave-2 seat (not mine).**
   `git status --porcelain` in the lane lists `?? forge.out`, `?? naive.out`, `?? sup-forge.out`, `?? sup-naive.out`
   (202/383/187/274 bytes; heads `PARAS=PASS ok`, `PREFIX=FAIL g_paras: text differs at 24 …`), i.e. replays of the
   C1 controls and supplement. My own redirects were named `c1.out`, `sup.out`, `o-<tool>.txt`, `os-<tool>.txt` and all
   ran after `cd` into my scratch, which is removed; my only lane write is this report. Same class as the round's
   Mistakes row 4 (a W1 seat's fleet-root strays) — now a W2 recurrence inside the lane; the L1 should remove them
   before landing, and the wave-2 context line did not prevent it.
4. Round 51's own entry is 10 physical lines; this draft is 12 including its blank lines — inside the 60-line cap.

## Out of scope (not claimed)

- No fix applied to `corpus/lessons/round-52.md`, `LOG.md`, or any counter; no commit, no census rewrite, no network.
- I did not re-run `controls/build-c2-controls.py` (I read its committed receipt `controls/c2-controls.txt`) and did not
  re-derive the 38 quote offsets independently of `build-spans --check`; both are other seats' attacks this wave.
- Wave-2 counts are not in the draft: `w2-results.json` does not exist yet, so only W1 (45 seats, 45 reports) is stated.

VERDICT: attacked the landed C1/C2 claims, both counters, all four C1 controls, the forge/supplement pair, the span manifest, the registry growth, the S120 offsets, the SKILL digest pins and the verdict-gap — every measured number reproduces as reported (`LEGS=9/9` ×3, `SUPPLEMENT_LEGS=4/4` vs forge `0/4`, controls 4/9 0/9 0/9, `C2=PASS BOUND=4/4` all legs 38/38, `SPANS_ROWS=38 STALE=0`, offsets 8996/9020/9428, `VERDICT_GAPS=2 UNPARSED=1`), with two defects found beside them: the lesson's round-end census receipt `corpus/evidence/round52/measure-after.txt` does not exist (the observation itself reproduces, exit 0, 116 rows), and four untracked replay files sit at the lane root from another wave-2 seat; the LOG entry is drafted (12 lines, the required coverage) and cites only what I ran.

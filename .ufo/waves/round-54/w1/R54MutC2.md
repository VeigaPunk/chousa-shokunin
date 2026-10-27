# R54MutC2 — mutation probe: the R54 C2 counter's new and changed legs

seat: mutation-tester (leaf) · round 54, wave 1 · axes: operability, depth
lane writes: this file only · tools installed: none · LibreOffice: never invoked
(`pgrep -u $USER -af soffice` → no output, rc=1, before and after the probe)
scratch: `/fast/scratch/hyaku/chousa-r54/R54MutC2` (fixture clone + one state dir per input; removed at exit)
bytes under test, lane == scratch copy: `c2-count.py` sha256 `0b83619755d2786ca7e8bb788c3ea1c7a6b94c61473862a6d32c18cae63f8938`,
`build-spans.py` sha256 `e8337aba1ad8859c467a519df9b47ed0010937d9e68e12214c893d71e279b030` (both from the lane's round54 dir).

## Fixture: what has to exist for the counter to run at all

The counter takes lane bytes from `--root` but derives `LANE = parents[3](__file__)` for three things:
`git -C LANE show BASE_REV:corpus/SOURCES.md` (base ids), `git -C LANE grep … BASE_REV -- corpus/knowledge`
(the NEW_GROUND "not at base" leg) and `LANE/corpus/evidence/round51/quote-substance-check.py`.
So the probe is a fixture clone of the lane at the frozen base carrying the two copied scripts at
`corpus/evidence/round54/`, plus one `--root` state per input:

```
$ git clone -q --no-checkout <lane> $D/lane && git -C $D/lane checkout -q c49ffc6ce1c3de87c1dfa96856239ed7274bf07b
$ git -C $D/lane show c49ffc6…:corpus/SOURCES.md | grep -c '^| S';     120
$ git -C $D/lane show c49ffc6…:corpus/SOURCES.md | grep -c '^| S101 ';   1
```

A `--root` state holds `corpus/SOURCES.md` (BASE_REV registry + rows S121 SAMR / S122 openstd / S123 JMU,
and `source-type-taxonomy-r37.md` appended to S101's `used-by`), the two entries, `corpus/lessons/round-54.md`,
`corpus/evidence/round54/{quotes.tsv,spans.tsv,spans/}` and `tools/inference-ground.py`. `build-spans.py`
built the manifest from the three `.txt` sidecars (`QUOTE <id> char <N>` printed the anchor offsets):

```
$ python3 build-spans.py --root <state>
QUOTE S121 char 1797 spans/S121-1.txt
QUOTE S121 char 1829 spans/S121-2.txt
QUOTE S121 char 1463 spans/S121-3.txt
QUOTE S122 char 13300 spans/S122-1.txt
QUOTE S122 char 15188 spans/S122-2.txt
QUOTE S122 char 15743 spans/S122-3.txt
QUOTE S123 char 5506 spans/S123-1.txt
QUOTE S123 char 5576 spans/S123-2.txt
QUOTE S123 char 11542 spans/S123-3.txt
SPANS_ROWS=9 WRITTEN=9
```
Nine located quotes, each unique and on one line of its capture text form (len/words from the manifest;
every quote ≤25 whitespace words and ≤160 chars, so `QUOTE_SHORT=9/9`):

```
S121  29ch 2w 本标准非等效采用ISO国际标准：ISO 690:2021。      (this is also r36's NEW_GROUND term)
S121  27ch 2w 采标中文名称:信息与文献 参考文献和信息资源引用指南。
S121  14ch 1w 20240256-T-469
S122  18ch 2w 标准号：GB/T 7714-2025
S122  47ch 1w 该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务
S122  12ch 1w 国际标准分类号（ICS）
S123  44ch 1w 本文件规定了参考文献的著录信息源、著录用文字、著录用符号、著录通则、各文献类型著录项目与
S123  19ch 1w 本文件适用于作者和编制者著录参考文献。
S123  22ch 1w 文献类型标识、文献载体标识应按照附录Ａ著录。      (this is r37's NEW_GROUND term)
```

Baseline — pristine frozen counter on the passing state (`python3 …/c2-count.py --root <state>`):

```
$ python3 corpus/evidence/round54/c2-count.py --root <state>
ENTRIES=2/2 (min 2) REFUSED_ENTRIES=0
HELD_CITED=S101 HELD_BAD=0
BOUND=3/3 (min 2) REFUSED=0
BOUND_IDS=S121,S122,S123
REF_ID_UNBOUND=0
NEW_GROUND=2/2
QUOTE_ROWS=9 ON_BOUND=9/9
SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=9/9
QUOTES_IN_ENTRY=9/9
QUOTES_IN_LESSON=9/9
QUOTE_SHORT=9/9
SPAN_CONTEXT=9/9
CAPTURE_BOUND=9/9
SUBSTANCE=PASS
ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=2/2
QUARANTINE_VERDICTS=3/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS                       (exit 0)
```

## The six mutants (each: one minimal patch to the frozen counter)

| id | frozen text → mutant |
|---|---|
| M1 | held `good = all(<source-line regex> **and e in used** for e in citing)` → drop `and e in used` |
| M2 | held `citing` keyed on `^source:.*<url>` → `\bS101\b` mention, and `good` keeps only `e in used` |
| M3 | `hrow = [… r[0] == hid and **r[0] in base_ids** and …]` → drop `r[0] in base_ids` |
| M4 | `MIN_BOUND = 2` → `MIN_BOUND = 1` |
| M5 | `new_ground += … and **term in texts[entry]**` → `… and any(t in texts[entry] for t in TERMS.values())` |
| M6 | ok-condition `**len(verdicts) == len(reg_ids)**` → `len(verdicts) == len(set(verdicts) & set(reg_ids))` (tautology) |

M1/M2 in full (probe copies, scratch only — not proposed lane code):

```diff
--- corpus/evidence/round54/c2-count.py            (M1)
-        good = all(re.search(r"^source:\s*" + hid + r"\s+—\s+" + re.escape(url) + r"(\s|$)", texts[e], re.M) and e in used
+        good = all(re.search(r"^source:\s*" + hid + r"\s+—\s+" + re.escape(url) + r"(\s|$)", texts[e], re.M)
                    for e in citing)
--- corpus/evidence/round54/c2-count.py            (M2)
-        citing = sorted(e for e, t in texts.items() if re.search(r"^source:.*" + re.escape(url), t, re.M))
+        citing = sorted(e for e, t in texts.items() if re.search(r"\b" + hid + r"\b", t))
-        good = all(re.search(...) and e in used for e in citing)
+        good = all(e in used for e in citing)
```

## Plausible bad lane states (one dimension each, everything else from the passing state)

B1 stale `used-by`: r37 carries `source: S101 — <url>`, S101's `used-by` never gained r37.
B2 no source line: r37 names S101 in prose only, S101's `used-by` does name r37.
B3 held row added after BASE_REV: the HIT row is not in the base registry (base rewritten out of band, see below).
B4 one bound document: only SAMR bound; openstd and JMU have no row, no `source:` line, a `refused-doc` line in the lesson.
B5 wrong NEW_GROUND term: r37 carries `ISO 690:2021` (the other entry's term) and no `文献载体标识`.
B6 missing quarantine verdict: the lesson re-checks S080 and S088, not S096.

Pristine on each (targeted leg only; every other leg stays green):

```
B1 HELD_CITED=- HELD_BAD=1  REF_ID_UNBOUND=4  C2=FAIL exit 1
B2 HELD_CITED=- HELD_BAD=0  REF_ID_UNBOUND=2  C2=FAIL exit 1
B4 BOUND=1/3 (min 2) REFUSED=2                C2=FAIL exit 1
B5 NEW_GROUND=1/2                             C2=FAIL exit 1
B6 QUARANTINE_VERDICTS=2/3 (S080,S088,S096)   C2=FAIL exit 1
```

## Kill matrix (rows = input, columns = counter; 42 runs, `--root <state>`)

```
state             c2-count m1_held m2_held m3_held m4_min  m5_newg m6_verd
good                PASS     PASS    PASS    PASS    PASS    PASS    PASS
b1_held_usedby      FAIL     PASS    FAIL    FAIL    FAIL    FAIL    FAIL
b2_held_nosource    FAIL     FAIL    PASS    FAIL    FAIL    FAIL    FAIL
b4_minbound         FAIL     FAIL    FAIL    FAIL    PASS    FAIL    FAIL
b5_newground        FAIL     FAIL    FAIL    FAIL    FAIL    PASS    FAIL
b6_verdicts         FAIL     FAIL    FAIL    FAIL    FAIL    FAIL    PASS
```

M1, M2, M4, M5, M6 are killed: the matching bad state is accepted only by its own mutant. The states are
not interchangeable — b1 is still rejected by M2 (its `used-by` is stale, which M2 keeps), b2 still by M1
(no source line at all), so the two held mutations are independent.

## M3 survives every lane state (equivalent mutant), killed only by rewriting the base object

`hrow` requires `r[0] == hid`, and `hid` is the constant `HELD = {HIT: "S101"}`; `S101` is one of the
120 base rows, so `r[0] in base_ids` is true on every reachable input. Measured: all six lane states give
M3 the same verdict, counts and exit code as the pristine counter (`m3_held_new` column == `c2-count` column).
To show the guard is not vacuous in principle, the base was rewritten out of band in a second fixture
(`git read-tree`/`update-index`/`commit-tree` + `git replace $BASE $NEW` so that `show $BASE:corpus/SOURCES.md`
has no S101 row) — a change no lane state can make, since BASE_REV is a frozen hash inside the counter:

```
$ python3 T3/corpus/evidence/round54/c2-count.py   --root <state>   → HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=4 C2=FAIL  exit 1
$ python3 T3/corpus/evidence/round54/m3_held_new.py --root <state>  → HELD_CITED=S101 HELD_BAD=0 REF_ID_UNBOUND=0 C2=PASS  exit 0
```

## Detector liveness (the baseline PASS is not vacuous)

```
span file byte edited (本标准→标准 in spans/S121-1.txt):  QUOTES_IN_SPAN=8/9 CAPTURE_BOUND=8/9 C2=FAIL exit 1
one lesson quote shortened (国际标准分类号（ICS）→…分类号): QUOTES_IN_LESSON=8/9            C2=FAIL exit 1
```

## Findings for the L1 (reported, not patched)

1. The held branch's `r[0] in base_ids` guard is unfalsifiable under the frozen predicate: `HELD` pins the
   id to S101 and S101 is in BASE_REV's registry, so M3 cannot be distinguished by any lane state. The
   claim's "held" requirement is therefore carried only by the `source:`-line + `used-by` pair (M1, M2 —
   both killable). Anything stronger would need `HELD` to name an id the lane may add, or the base-id set
   to be read from the lane's own claim of what it held.
2. A bound id cited by an entry that is not in that row's `used-by`, and without a `source:` line, is
   invisible: the b4 state has r37's only `source:` line = S101 while r37's Inference names S121, and
   S121's `used-by` names only `…r36.md`; pristine prints `REF_ID_UNBOUND=0 BOUND=1/3` — the only red leg
   is the bound count (measured: `grep -n '^source:' r37` → line 7 only, `S121` row used-by
   `corpus/knowledge/source-type-taxonomy-r36.md`). The bound `used == citing` set comes from `DOCS`, so the
   "its `used-by` naming exactly the existing entries citing it" half of the predicate is not measured
   against the entries' own citations.
3. The fixture set (good + 5 bad states) exercises: held source line, held `used-by`, bound count,
   NEW_GROUND term, quarantine verdict count. Not exercised: `--lane-only`, refusal of an entry
   (`refused-entry`), `ENV_CHANGED`, and a capture whose digest changed; those legs were left untouched
   because no mutation in this ticket lands on them.
4. Contract untouched: no predicate, target, counter, control or frozen file was edited. Restoration: the
   lane's `corpus/evidence/round54/c2-count.py` was only read (sha256 `0b836197…` recorded before and after
   the probe, identical to the scratch copy each time); every mutant lives at
   `<fixture>/corpus/evidence/round54/m*_*.py` inside `/fast/scratch/hyaku/chousa-r54/R54MutC2`, which is
   removed on exit. This report is the only lane write.

**VERDICT** — attacked the frozen R54-C2 counter's six new/changed legs with six mutants on six one-dimension bad lane states: M1 (held used-by), M2 (held id without a `source:` line), M4 (MIN_BOUND 2→1), M5 (NEW_GROUND one term) and M6 (verdict count self-compared) are killed on the diagonal, M3 (held row added after BASE_REV) survives every lane state because `r[0] in base_ids` is always true for the constant `HELD` id S101 and differs only when the base object itself is rewritten — a guard no lane state can falsify.

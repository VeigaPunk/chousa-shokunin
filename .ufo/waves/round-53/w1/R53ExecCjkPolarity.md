# R53ExecCjkPolarity — build: the inert CJK polarity leg of `inference-ground`

Seat R53ExecCjkPolarity (leaf; no subagents). Lane HEAD `6365f15b64b89d1ad1ac66fe7d7b81c92e74d90f`; lane `tools/inference-ground.py` sha256 `33d4a37f…962b6d`, not written by this seat. Scratch `/fast/scratch/hyaku/chousa-r53/R53ExecCjkPolarity` (TMPDIR there, removed on exit). No tool installed or upgraded; `pacman` untouched (host pause). Attacking round-52 routed defect 5 (`R52W2ExecInfRegression` §3-4).

## 1. The hole, in the tool's own lines
- `tools/inference-ground.py:325-342` — `polarity_flips` needs `stems = {stem(w) for w in scope}`, and `scope` comes from `words(tok)` (`:256`, `[a-z][a-z'\u2019]*`). A CJK phrase yields no words, so `stems` is empty and `:339-341` returns `[]`: no window at all, not a narrow one.
- `:88-96` — `has_two_words` counts a CJK phrase as a token (round 50); the comment at `:95` states the consequence, but the docstring's named limit (`:60-63`) never mentioned the script.
- Measured at HEAD (§3): a bullet quoting `要求报告检索日期` from a span that affirms it while asserting `不要求… / 没有… / 未要求…` prints `GROUND: PASS`, exit 0, zero findings; the same inversion fires once its carrier is Latin (`R52W2ExecInfRegression` §5).

## 2. Fixture root, built in scratch and run from it
```
corpus/fixtures/inference-ground-cjk/
  SOURCES.md spans.tsv  spans/S901-1.txt spans/S902-1.txt spans/S903-1.txt
  cjk-negation-buyaoqiu.md cjk-negation-meiyou.md cjk-negation-weiyaoqiu.md
  cjk-positive-control.md cjk-span-negated.md cjk-precision-far-negator.md

python3 <tool> --entry corpus/fixtures/inference-ground-cjk/<entry>.md \
  --spans corpus/fixtures/inference-ground-cjk/spans.tsv --counts /dev/null \
  --registry corpus/fixtures/inference-ground-cjk/SOURCES.md --root .
```
Lane path `corpus/fixtures/inference-ground-cjk/SOURCES.md` (fixture-local: **no** `S90x` row may enter the lane's `corpus/SOURCES.md`; `S901`/`S902` are already fixture ids in `corpus/fixtures/inference-ground-r46`):
```
# Fixture registry — the CJK polarity fixtures' three sources

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S901 | CJK polarity fixture — affirmed requirement (本指南要求报告检索日期。) — https://example.invalid/fixture-cjk-a | own-work | A | a fixture span, not a real source | char 0: 本指南要求报告检索日期 | a CJK-carried phrase whose span affirms it | fixture | - | - | corpus/fixtures/inference-ground-cjk/cjk-negation-buyaoqiu.md |
| S902 | CJK polarity fixture — positive control (本指南要求报告检索日期。) — https://example.invalid/fixture-cjk-b | own-work | A | a fixture span, not a real source | char 0: 本指南要求报告检索日期 | a CJK-carried phrase kept with the span's polarity | fixture | - | - | corpus/fixtures/inference-ground-cjk/cjk-positive-control.md |
| S903 | CJK polarity fixture — negated span (本指南不要求报告检索日期。) — https://example.invalid/fixture-cjk-c | own-work | A | a fixture span, not a real source | char 0: 本指南不要求报告检索日期 | a CJK-carried phrase whose span negates it | fixture | - | - | corpus/fixtures/inference-ground-cjk/cjk-span-negated.md |
```
Lane path `corpus/fixtures/inference-ground-cjk/spans.tsv` (seven tab-separated cells per row, as the tool parses):
```
id	url	capture_sha256	offset	span_file	quote	entry
S901	https://example.invalid/fixture-cjk-a	0000000000000000000000000000000000000000000000000000000000000000	0	spans/S901-1.txt	要求报告检索日期	cjk-negation-buyaoqiu.md
S902	https://example.invalid/fixture-cjk-b	0000000000000000000000000000000000000000000000000000000000000000	0	spans/S902-1.txt	要求报告检索日期	cjk-positive-control.md
S903	https://example.invalid/fixture-cjk-c	0000000000000000000000000000000000000000000000000000000000000000	0	spans/S903-1.txt	要求报告检索日期	cjk-span-negated.md
```
Lane paths `corpus/fixtures/inference-ground-cjk/spans/S901-1.txt`, `S902-1.txt`, `S903-1.txt` (one line each, in that order):
```
本指南要求报告检索日期。
本指南要求报告检索日期。
本指南不要求报告检索日期。
```
Lane path `corpus/fixtures/inference-ground-cjk/cjk-positive-control.md` — the template the other five follow (11 lines):
```
# Fixture — CJK-carried affirmation kept: the span affirms a requirement and so does the bullet (positive)

source: S902 — https://example.invalid/fixture-cjk-b — a fixture span, not a real source

#### Observation

- The span says the guide asks for the search date to be reported (`S902`).

#### Inference

- **该指南要求报告检索日期。** `S902` 的原文是"要求报告检索日期"，本条目据此记录每一项的检索日期。
```
The other five files are the same eleven lines with the title line, the two `S902` cells, the Observation sentence's negation and the Inference bullet replaced, exactly as below (lane paths `corpus/fixtures/inference-ground-cjk/<file>`):
```
cjk-negation-buyaoqiu.md     # Fixture — CJK-carried reversal: the span affirms a requirement, the bullet negates it with 不 (junk)
- **该指南不要求报告检索日期。** `S901` 的原文是"要求报告检索日期"，本条目据此不记录检索日期。
cjk-negation-meiyou.md       # Fixture — CJK-carried reversal: the span affirms a requirement, the bullet negates it with 没有 (junk)
- **该指南没有要求报告检索日期。** `S901` 的原文是"要求报告检索日期"，本条目据此不记录检索日期。
cjk-negation-weiyaoqiu.md    # Fixture — CJK-carried reversal: the span affirms a requirement, the bullet negates it with 未要求 (junk)
- **该指南未要求报告检索日期。** `S901` 的原文是"要求报告检索日期"，本条目据此不记录检索日期。
cjk-span-negated.md          # Fixture — CJK-carried reversal the other way: the span negates the phrase, the bullet asserts it (junk)
source: S903; Observation: - The span says the guide does not ask for the search date to be reported (`S903`).
- **该指南要求报告检索日期。** `S903` 的原文是"要求报告检索日期"，本条目据此记录每一项的检索日期。
cjk-precision-far-negator.md # Fixture — a CJK negator on a DIFFERENT object (记录) does not reach the quoted phrase (positive)
source: S901; - **该指南不记录检索日期，因为原文是"要求报告检索日期"。** `S901` 的原文是"要求报告检索日期"，本条目据此记录每一项的检索日期。
```

## 3. Red-before — the lane tool at HEAD is inert on all four reversals
```
$ python3 <lane>/tools/inference-ground.py --entry <fixture>.md --spans spans.tsv \
    --counts /dev/null --registry SOURCES.md --root .
cjk-negation-buyaoqiu      exit=0  tokens=1 grounded=1  GROUND: PASS  findings: none
cjk-negation-meiyou        exit=0  tokens=1 grounded=1  GROUND: PASS  findings: none
cjk-negation-weiyaoqiu     exit=0  tokens=1 grounded=1  GROUND: PASS  findings: none
cjk-span-negated           exit=0  tokens=1 grounded=1  GROUND: PASS  findings: none
```

## 4. Smallest patch — `diff -U1`, verified to apply to the lane file (`patch -p1` → byte-identical)
Lane path `tools/inference-ground.py`:
```diff
--- a/tools/inference-ground.py
+++ b/tools/inference-ground.py
@@ -46,2 +46,10 @@
      from three to two, measured on `corpus/evidence/round48/precision-count.py`.
+     Round 53 adds the CJK carrier: `words()` is Latin-only, so a Chinese or
+     Japanese phrase had no window and any reversal it carried passed. A
+     phrase of four or more CJK characters is now read in CHARACTERS — a
+     listed negator (`不 未 没 沒 无 無 非 否 勿 别 別 毋` before it, `ない
+     ません なし 無し 無い` after it) within six characters of the occurrence,
+     inside its own clause — and the bullet's unquoted text repeating the
+     phrase in the opposite polarity is a flip, in both directions. Fixtures:
+     `corpus/fixtures/inference-ground-cjk/`.
 
@@ -60,3 +68,5 @@
 Figures still require a listed negator in the next four words. A different-stem
-flip, a distant negator, or a second bullet can pass; semantics remain for a
+flip, a distant negator, or a second bullet can pass; so can a CJK reversal
+whose bullet never restates the quoted phrase in the prose, or whose negator
+falls outside the six-character window (`并不真正要求…`). Semantics remain for a
 reader to judge.
@@ -359,2 +369,66 @@
 
+# CJK polarity (round-53 `R53ExecCjkPolarity`): `words()` is Latin-only, so a
+# Chinese or Japanese phrase had no window at all, and a bullet could quote a
+# span's affirmed phrase and assert its negation (`不要求…`, `未要求…`,
+# `没有要求…`) and still print `GROUND: PASS`. The window is measured in
+# CHARACTERS, not words, because the script is unspaced: a listed negator
+# within `CJK_WINDOW` characters of the occurrence, inside the occurrence's
+# own clause and line. Prefix negators cover the pre-verbal negative that
+# Chinese and Japanese share; the postfix ones cover the Japanese predicative
+# negative that follows a noun (`記載なし`). A negator inside the phrase
+# itself is not read: the phrase is the same bytes on both sides, so it cannot
+# mark a difference between them.
+CJK_NEG_PRE = ("不", "未", "没", "沒", "无", "無", "非", "否", "勿", "别", "別", "毋")
+CJK_NEG_POST = ("ない", "ません", "なし", "無し", "無い")
+CJK_WINDOW = 6
+CJK_CLAUSE_RE = re.compile(r"[\n。、，,；;：:！!？?（）()「」『』\[\]]")
+CJK_RUN_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
+
+
+def cjk_occurrence_polarity(tok: str, s: str, idx: int) -> tuple[bool, str]:
+    """(negated, cue) for one occurrence of a CJK phrase: the listed negator
+    inside the window, or "" when none is."""
+    before = CJK_CLAUSE_RE.split(s[:idx])[-1]
+    after = CJK_CLAUSE_RE.split(s[idx + len(tok):])[0]
+    tail, head = CJK_RUN_RE.findall(before), CJK_RUN_RE.findall(after)
+    for n in CJK_NEG_PRE:
+        if tail and n in tail[-1][-CJK_WINDOW:]:
+            return True, n
+    for n in CJK_NEG_POST:
+        if head and n in head[0][:CJK_WINDOW]:
+            return True, n
+    return False, ""
+
+
+def cjk_polarity_flips(bullet: str, tok: str, spans: list[str]) -> list[str]:
+    """CJK carriers: the bullet's own prose repeats the phrase in the opposite
+    polarity from the span, read in characters rather than scope-word stems.
+
+    Read only for a phrase of four or more CJK characters (the `has_two_words`
+    token floor), only when every cited span occurrence agrees on the phrase's
+    polarity, and only where the bullet's unquoted text repeats the phrase: a
+    bullet that does not restate the phrase is out of reach, as a Latin bullet
+    that omits the span's scope words is.
+    """
+    if len(CJK_RE.findall(tok)) < 4:
+        return []
+    span_seen = set()
+    for s in spans:
+        start = s.find(tok)
+        while start >= 0:
+            span_seen.add(cjk_occurrence_polarity(tok, s, start)[0])
+            start = s.find(tok, start + 1)
+    if len(span_seen) != 1:
+        return []
+    negated = span_seen.pop()
+    prose, out = unquoted(bullet), []
+    start = prose.find(tok)
+    while start >= 0:
+        hit, cue = cjk_occurrence_polarity(tok, prose, start)
+        if hit != negated:
+            out.append(f"cjk:{cue}" if hit else "cjk:unnegated")
+        start = prose.find(tok, start + 1)
+    return list(dict.fromkeys(out))
+
+
 KEY_PART_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
@@ -497,3 +571,5 @@
             if ok and not is_num:
-                for w in polarity_flips(bullet, tok, grounded):
+                hits = polarity_flips(bullet, tok, grounded)
+                hits += cjk_polarity_flips(bullet, tok, grounded)
+                for w in hits:
                     findings.append({"code": "INF_POLARITY_FLIP", "bullet": i,
```
Negators (`:381-382`) pre `不 未 没 沒 无 無 非 否 勿 别 別 毋`, post `ない ません なし 無し 無い`; window `CJK_WINDOW = 6` characters, clause- and line-bounded (`:384`): six characters before the occurrence (last CJK run of the segment) or six after (first CJK run), never across `。、，；：（）「」` or a newline. Measured on the imported patched module: `PRE:` all twelve `True`; `POST:` all five `True`; `window6 (True,'不')` on `本指南不真正地完全要求报告检索日期。`; `window7 (False,'')` on `本指南不真正地完全彻底要求…`; `flip ['cjk:不']` on `该指南不要求…`; `keep []` on `该指南要求…`.

## 5. Green-after — four reversals refused, two positives kept
```
patched: cjk-negation-buyaoqiu      exit=1  FINDING INF_POLARITY_FLIP bullet=1 token='要求报告检索日期 / cjk:不'
patched: cjk-negation-meiyou        exit=1  FINDING INF_POLARITY_FLIP bullet=1 token='要求报告检索日期 / cjk:没'
patched: cjk-negation-weiyaoqiu     exit=1  FINDING INF_POLARITY_FLIP bullet=1 token='要求报告检索日期 / cjk:未'
patched: cjk-span-negated           exit=1  FINDING INF_POLARITY_FLIP bullet=1 token='要求报告检索日期 / cjk:unnegated'
patched: cjk-positive-control       exit=0  GROUND: PASS  tokens=1 grounded=1
patched: cjk-precision-far-negator  exit=0  GROUND: PASS  tokens=2 grounded=2
```

## 6. The lane's existing entries still pass, at identical token counts
The nine entries the round-50/51/52 manifests name, each with its round's `spans.tsv`, `--counts /dev/null`, `--registry corpus/SOURCES.md`: base and patched printed the **same** `tokens=`/`grounded=` line and exit 0 for every one — r41 7/7, cnki-r40 11/11, istic-r39 18/18, chinese-search-record-r39 9/9, japanese-search-record-r38-amendment 9/9, japanese-search-record-r38 11/11, chinese-prisma-s-reception-r52 7/7, japanese-prisma-item-wording-r40 7/7, japanese-search-record-niph-form-r52 10/10 (10, not the `9` in `R52W2ExecInfRegression` §2 — that entry was revised at `643ac77` after that seat ran). `corpus/knowledge/*-r5[0-2].md` expands to the two r52 files, both above. Latin sets with `--tool <patched>`:
```
round46/c1-count.py → POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass C1=PASS exit=0
round47/c1-count.py → R46_COUNTER=pass R46_ENTRIES=2/2 CANARY=pass C1=PASS exit=0
round48/precision-count.py → CORRECT_BULLETS_PASS=12/12 PRECISION_GATE=PASS exit=0
```

## 7. What the patch still cannot see — both measured, both still `GROUND: PASS` exit 0
- **A Latin negator on a CJK-quoted phrase.** `The guide does not require the reporting of the search date.` with quote `要求报告检索日期` passes: the CJK path needs a CJK negator by a restated phrase, the Latin path has no CJK scope stems, and linking an English sentence to a Chinese quote needs a translation the tool does not have.
- **A Japanese verb-final negation that rewrites the predicate.** span `本様式は各情報源の検索日を記載する。`, bullet `本様式は各情報源の検索日を記載しない。` passes: the bullet no longer contains the quoted phrase, so nothing is located to compare (needs Japanese verb-stem matching).

## 8. Risk and what the L1 integrates
Findings are added only where the bullet's unquoted prose restates a ≥4-character CJK phrase in the opposite polarity within six characters; on the nine landed entries and the 18 fixture cases nothing changed (identical token counts, 12/12, 3/3, CANARY=pass). False-refusal risk is a CJK negator within six characters of a restated phrase that scopes to a neighbouring object — `cjk-precision-far-negator.md` shows one such shape kept, not a guarantee. No frozen C1/C2 predicate, counter, control or target touched; no production file, registry row or counter written. Integrate: the diff into `tools/inference-ground.py`, the fixture files at their fenced lane paths, the two docstring paragraphs. No counter change is needed — none reads `corpus/fixtures/inference-ground-cjk/`.

VERDICT: Built the CJK polarity leg round 52 found inert — red-before, the lane tool passes all four reversals (`不要求`/`没有`/`未要求` and the span-negated direction) with `GROUND: PASS` exit 0, and a 94-line `-U1` patch (twelve pre-negators, five post-negators, six-character clause-bounded window) turns them into `INF_POLARITY_FLIP` exit 1 while both positives stay PASS and the nine landed entries plus the r46/r47/r48 Latin sets are unchanged (12/12, 3/3, CANARY=pass, identical token counts); two residual holes measured and named.

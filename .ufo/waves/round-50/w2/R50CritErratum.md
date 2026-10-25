# R50CritErratum — freeze integrity of the round-50 post-freeze disclosures
seat R50CritErratum (critic, round-50/w2). Attacked `corpus/evidence/round50/claims-erratum.md`
items 1–4 and `corpus/lessons/round-50.md:154` `## Disclosed post-freeze changes`. No installs;
scratch `/dev/shm/chousa-r50-R50CritErratum/` deleted; lane untouched.

## 1. Frozen scope: byte-identical, and the empty diff is not vacuous
```
git -C <lane> diff 6a068f2a 74794db --stat -- corpus/evidence/round50/c1-count.py \
  corpus/evidence/round50/c2-count.py corpus/evidence/round50/claims.md \
  corpus/evidence/round50/controls corpus/evidence/round50/c1-fixtures      → (no output) RC=0
git ls-tree -r --name-only 6a068f2a -- corpus/evidence/round50/controls    → 6 files
git ls-tree -r --name-only 6a068f2a -- corpus/evidence/round50/c1-fixtures → 5 files  (same at 74794db)
TMPDIR=<scratch> python3 corpus/evidence/round50/c1-count.py
→ SELFTEST_DEFAULT=PASS / BASELINE=PASS rc=0 findings=26 / PERTURB_PASS=6/6 / EXPECTED_BAD rc=2
  R49_REGRESSION=PASS rc=0 / LEGS=5/5 / C1=PASS  EXIT=0
python3 corpus/evidence/round50/c2-count.py --lane-only
→ BOUND=3/4 (min 3) REFUSED=1 / BOUND_IDS=S104,S105,S106 / REF_ID_UNBOUND=0 / ON_BOUND=55/55 / C2=PASS
```
Both reproduce `measure-after-1.txt` line for line; the frozen paths exist at both ends, so identity is real.
## 2. Every tracked path changed after the freeze vs what the erratum names
```
git log --oneline 6a068f2a..74794db
→ ec52e63 (C1 candidate) · 7754172 (w1 spec) · 2573dc1 (hardening + w1 reports) · 74794db (C2 adoption)
git diff --name-status 6a068f2a 74794db | awk '{print $1}' | sort | uniq -c    → 132 A, 7 M (139 paths)
   by area: corpus/evidence 72, .ufo/waves 51, corpus/fixtures 5, corpus/knowledge 3, corpus/lessons 2,
            tools 2, SOURCES/README/QUALITY/SKILL 4
```
The 7 M paths: `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/lessons/round-49.md`, `tools/assimilate-rows.py`, `tools/inference-ground.py`.
Items 1–2 name the two tools (✓). The whole C2 candidate is unnamed: 3 entries, SOURCES +5,
quotes.tsv/spans.tsv 56 rows each + 56 span files, lesson, QUALITY 73–79, SKILL gate rows, README,
round-49 lesson, 5 checks + receipts, `corpus/fixtures/assimilate-selftest/` 5 files.
Item 3 (line 26) names `build-spans.py`/`quote-substance-check.py` as changed after the freeze: both
exist at 6a068f2a and are absent from the 139, so they did **not** change; the provenance claim is
true (`diff <(sed 's/round49/round50/g; s/round-49/round-50/g' corpus/evidence/round49/<file>) corpus/evidence/round50/<file>`
→ IDENTICAL_MODULO_ROUND for both) but is filed under a heading that says it changed. Item 4 names no path.
Judgment: read as *changes to a frozen leg's condition*, the list is complete — the only changed
condition input is `tools/inference-ground.py`, disclosed. Read as written ("Changed after the freeze …
all disclosed", line 11), it is materially incomplete and 2 of 4 items are not post-freeze changes.
Undisclosed dependency: `corpus/fixtures/assimilate-selftest/` is C1 leg 1's fixture package (the tool's
default `fix`), added at ec52e63, not in the erratum's path list, and the frozen counter pins only
`c1-fixtures/` (`git diff --stat ec52e63 74794db -- corpus/fixtures/` → no output). No harm today, but
the "unchanged" proof misses a leg input and that leg is unpinned.
## 3. `has_two_words` CJK floor: fair repair, not a goalpost move; one undisclosed consequence
Necessity, measured with the freeze-time tool (`git show 6a068f2a:tools/inference-ground.py`):
```
r41 old: GROUND … bullets=4 tokens=0 grounded=0 / INF_UNGROUNDED bullet=1..4 / GROUND: FAIL rc=1
r41 new: GROUND … bullets=4 tokens=7 grounded=7 / GROUND: PASS rc=0
r40 old rc=0 · r39 old rc=0
```
So the erratum's "could not be met by any honest entry" (line 20) overstates: 2 of 3 entries already
exited 0 under the old tool; only the pure-CJK entry was blocked. Boundary and non-vacuity (scratch
entries, `--spans corpus/evidence/round50/spans.tsv`):
```
`使用手册` (4 CJK chars, in an S105 span): old rc=1 tokens=0 → new rc=0 tokens=1 grounded=1
`使用手`  (3 chars):                      old rc=1          → new rc=1 tokens=0   (floor is 4)
`完全不存在` (absent from spans):          new rc=1 INF_TOKEN_NOT_IN_SPAN
```
`has_two_words` is applied to the backticked/quoted phrase only (`grounding_tokens`, lines 158–168), and
each token must still appear verbatim in a cited span (line 519). The change converts CJK quotes from
*ignored* (never span-checked) to *required in a span*: monotone in strictness at rule 4; rule 3's floor
moves from "two words" to "≥4 CJK chars" = 2 two-character Chinese words. Fair repair; the leg's text is
unchanged. Undisclosed consequence: rule 5 (polarity) is structurally unreachable for CJK tokens —
`polarity_flips` builds `inner = words(tok)` and `uw = words(unquoted(bullet))` from a Latin-only
`WORDS_RE`, so scope is empty and it returns `[]` (lines 307–330). Before the change a pure-CJK bullet
failed at rule 3, so the skip was unreachable; now it passes rules 3–4 and skips rule 5. The erratum
(lines 20–25) does not say this; the tool's public rule 3 still reads "two or more words" and the
Named-limit paragraph (55–59) does not name the CJK polarity skip — only the inline comment (92–96) does.
Regression claim verified independently: `round46/c1-count.py`, `round47/c1-count.py`,
`round48/c1-count.py`, `round48/precision-count.py` run with `--tool ig-old.py` and `--tool
tools/inference-ground.py` → 4/4 IDENTICAL stdout, rc=0 both. Receipt caveat:
`inference-regression-after.txt` says `entries=65 differing=2`; the same loop at the tip gives
`entries=68 differing=5` (the three round-50 entries now differ too) — a pre-adoption snapshot, cited
without the qualifier.
## 4. assimilate-rows hardening: fair; the used-by widening is *required* by the unchanged check
Frozen leg meanings are unchanged: the leg definitions live in the frozen `c1-count.py`, and the hardening
adds only paths no perturbation takes (option clash, no-entry fixture, 120 s timeout, multiset compare,
tab-free findings); §1 reproduces `LEGS=5/5`, `PERTURB_PASS=6/6`, `findings=26`, `EXPECTED_BAD rc=2`,
`R49_REGRESSION rc=0`. used-by: the pre-freeze line was `users = sorted(e for e, tx in texts.items() if sid
in TOKEN_RE.findall(tx))` — one staged id. C2's unchanged check requires `used == citing` over the
*document's* citing entries (`c2-count.py:149–171`); the SXU document is staged as S124 (r40) and S135
(r41), so the old line yields at most one citing entry and C2 was unattainable through the tool. The new
line widens to `twins = {t for t in cited if mapping[t][0] == lid}` — it makes the generated cell satisfy a
stricter frozen check, it does not relax the check. Coverage note: neither `c1-fixtures` (single staged id
per row) nor `R49_REGRESSION` (round-49 package) exercises twin ids; only `c2-count` does (`BOUND=3/4`).
## 5. Item 4 (S107): premise verifiable, wording false
```
sed -n '14p' .ufo/waves/round-50/w1/DraftEntryR41.md
→ source: S107 — https://bs.bnu.edu.cn/docs/20160407183946745914.pdf — §2.3.2 …
git log --diff-filter=A --oneline -- .ufo/waves/round-50/w1/DraftEntryR41.md   → 2573dc1 (before 74794db)
git log --all --oneline -S'S107' -- corpus/SOURCES.md                          → (no commit)
git grep -n S107 74794db -- corpus/                                            → claims-erratum.md:27 only
cut -f1 corpus/evidence/round50/quotes.tsv | sort | uniq -c  → S104 18, S105 34, S106 3, no S107
```
(spans.tsv identical counts; `refs/jj/keep/f5cb8fd…`, not an ancestor of the tip, holds the same erratum
text and no S107 row.) So the draft binding IS in committed bytes. But "the row and its quotes were
removed before any commit" (line 27) is false as written: the staged row and its recheck line are
committed at the tip — `.ufo/waves/round-50/assimilation/append-tool.md:4` (`| S107 | “中国知网”大学生论文
管理系统使用手册（教师）…`) and `renumber.tsv:6` (`S145 → S107 append bs.bnu.edu.cn/…`), both added by
74794db, the commit that carries the claim. True only for `corpus/` paths. The frozen REFUSED leg itself
holds (`BOUND=3/4 REFUSED=1`).
## 6. "all three entries exit 0 under tools/inference-ground.py"
Text unchanged (`claims.md` byte-identical, §1); the *condition* changed because the tool is its input. At the tip all three exit 0 (my runs: r39 0, r40 0, r41 0; `INFERENCE_GROUNDED=3/3`) — the leg holds under the disclosed condition; it is not the frozen condition, and the erratum says so.
## Smallest safe corrections (disclosure-side only; no predicate, counter, target or control touched)
1. Line 11: split into "changed after the freeze" and "provenance notes"; move item 3 to the second, and
   either enumerate the 139 paths or drop "all disclosed".
2. Item 4: say "never committed to `corpus/` (no Registry row, no entry); the staged append block that
   carried S107 is committed as wave evidence at `…/assimilation/append-tool.md:4`".
3. Item 2: add "CJK tokens skip rule 5 (polarity)"; update the tool docstring rule 3 (≥4 CJK characters) and the Named-limit paragraph.
4. Add `corpus/fixtures/assimilate-selftest/` and `corpus/evidence/round49/c1-count.py` to the erratum's diff path list; state that the lane-default fixture package is unpinned (candidate, unchanged since ec52e63).
5. Requalify `inference-regression-after.txt` as a pre-adoption snapshot, or re-run it at the tip.
VERDICT: attacked the freeze integrity of claims-erratum.md items 1–4 and the lesson's Disclosed section —
defect found, in the disclosure, not in the counters: the frozen scope is byte-identical and both counters
pass, and both tool changes are fair repairs (CJK tokens are span-checked, floor 4 chars, earlier-round
counters byte-identical; the used-by widening only meets C2's unchanged `used == citing`), but the section
lists two non-changes as changes, calls an incomplete list "all disclosed", omits C1 leg 1's unpinned
fixture package from its proof, does not disclose that CJK tokens bypass the polarity rule (leaving the
tool's stated rule 3 contradicting the code), and asserts a removal "before any commit" while the S107 row
is committed at the tip in `assimilation/append-tool.md:4` and `renumber.tsv:6`.

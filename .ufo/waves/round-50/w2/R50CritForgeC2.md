# R50CritForgeC2 — forge the C2 counter: cheapest lane bytes that print `C2=PASS` (round 50, wave 2)

Attacked: the frozen C2 counter `corpus/evidence/round50/c2-count.py` (landed `74794db`) and its leg
`corpus/evidence/round50/quote-substance-check.py`, by building the cheapest lane bytes in
`/dev/shm/chousa-r50-R50CritForgeC2/root` and running the counter with `--root` (its `git show`/`git grep`
stay on the real lane by design, `:144,178`). Lane never mutated; every run is a read; frozen claims at
`6a068f2a` untouched and no counter/target/control edit is proposed. No tool installed; pacman untouched.
Siblings cover landed-byte mutation (`R50MutLandedC2`) and the CJK floor's internals (`R50MutInferenceCJK`).

## 1. Forge result — `C2=PASS` on 34 lines of entry/lesson prose

Byte inventory: 3 entries (9+9+11 lines: title, `source:`, term line, quotes line, `#### Inference` with
one bullet saying "asserts nothing"), a 5-line lesson, 3 registry rows, 9 quote rows. No Observation, no
Unknown, no assertion, no prose claim anywhere.

```
$ python3 corpus/evidence/round50/c2-count.py --root /dev/shm/chousa-r50-R50CritForgeC2/root
ENTRIES=3/3   BOUND=3/4 (min 3) REFUSED=1   BOUND_IDS=S104,S105,S106   REF_ID_UNBOUND=0
NEW_GROUND=3/3   QUOTE_ROWS=9 ON_BOUND=9/9   SPAN_IDS=3/3   QUOTES_IN_SPAN=9/9
QUOTES_IN_ENTRY=9/9   QUOTES_IN_LESSON=9/9   QUOTE_SHORT=9/9   SPAN_CONTEXT=9/9
CAPTURE_BOUND=9/9   SUBSTANCE=PASS   ANCHOR_BOUND=3/3   INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=0/0 ()   QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS   rc=0
```

The 9 quotes are: a page timestamp (`更新时间：2020 年 7 月`, 12 non-space), a title block
(`产品名称：“中国知网”大学生论文管理系统使用手册`, capture `28750bcdf5d36cd90a7709fb.txt` UTF-8,
char 83, exactly once — the ≥12-char row for S106), a chapter heading, and three 4-CJK common
words (`引证检索`, `参考文献`, `中国知网`) each recorded twice as identical rows.

## 2. Which shortcuts pass, which leg refuses each

| shortcut | result | refusing leg (when refused) |
|---|---|---|
| quotes from navigation/boilerplate (timestamp, title block, heading); the 25-word cap is inert for CJK (48/55 real rows are 1 whitespace "word") | **PASS** | none — `SUBSTANCE` floor is 3 non-space chars, one ≥12 per id |
| quotes no bullet uses | **PASS** | none — `QUOTES_IN_ENTRY/LESSON` are substring tests |
| bullet grounded by a phrase in **no** manifest row (M1) | **PASS** | none — `inference-ground` reads span files, not quotes |
| one `char N` per bound row (the landed lane already ships 3 for 55 quotes) | **PASS** | `ANCHOR_BOUND` only needs ≥1 and membership |
| `refused-doc` line that is not true (M6: asserts the bound SEU doc was refused) | **PASS** | none — `c2-count.py:170` matches a string, never the bound set |
| `source:` + `used-by` that merely lists the citing entries | **PASS by spec** | `BOUND` drops on any extra/missing entry (M5: `BOUND=2/4`, `REF_ID_UNBOUND=4`) |
| inference bullet that quotes a phrase but asserts nothing (M1/M17) | **PASS** | none — presence only |
| CJK floor: 4-char common word as the only token | **PASS** | 3 chars refused (M2: `INFERENCE_GROUNDED=2/3`); 1 char refused (M11: `0/3`) |
| duplicate manifest rows to reach `MIN_PER_ID=3` | **PASS** | distinct rows only → `SPAN_IDS=0/3` (M7) |
| root-supplied checkers gutted to `sys.exit(0)` (M13) | **PASS** | none — both legs are files inside the measured tree (`:208`, `:219`) |

## 3. Teeth (mutation matrix, exact counter output per variant)

| variant | decisive leg | C2 |
|---|---|---|
| m2 3-CJK token | `INFERENCE_GROUNDED=2/3` | FAIL |
| m3 anchor = another id's quote offset | `ANCHOR_BOUND=2/3` | FAIL |
| m4 no `refused-doc` line | `REFUSED=0` | FAIL |
| m5 `used-by` names a non-citing entry | `BOUND=2/4`, `REF_ID_UNBOUND=4` | FAIL |
| m6 false `refused-doc` for a **bound** doc | `REFUSED=1`, all legs green | **PASS** |
| m7 distinct rows only (2 per id) | `SPAN_IDS=0/3` | FAIL |
| m11 1-char quotes, real legs | `SUBSTANCE=FAIL`, `INFERENCE_GROUNDED=0/3` | FAIL |
| m12 3-char quotes, real legs | `SUBSTANCE=PASS`, `INFERENCE_GROUNDED=0/3` | FAIL |
| m13 checkers gutted, nothing else | `SUBSTANCE=PASS`, `INFERENCE_GROUNDED=3/3` | **PASS** |
| m14 falsified digest (3 rows) / m15 offset +1 (1 row) | `CAPTURE_BOUND=6/9` / `8/9` | FAIL |
| m16 span extended 200 chars | `SUBSTANCE=FAIL` (OVERWIDE_SPAN) | FAIL |
| m17 bullet asserts the **opposite** of its CJK quote | `INFERENCE_GROUNDED=3/3` | **PASS** |

## 4. Structural holes the closure must know about (no counter edit proposed)

1. **Manifest and bullets are decoupled** (m1). `inference-ground` grounds a token in *any* span text of a
   cited id, so a bullet may quote a phrase in no `spans.tsv` row; 32 of the landed 55 quotes (58%) are in
   no Inference bullet, so `SUBSTANCE` never judges the quotes that carry the arguments.
2. **A false refusal passes** (m6). The refused leg is a string match on the lesson (`:170`); nothing
   cross-checks that the named URL is *not* bound. The landed line is true (the 教师 capture
   `275c79d45b1e9b0fd32cef93.txt` has `grep -c 引文核对` → 0, `标明引文` → 9), but its negation passes too.
3. **Both substantive legs are root-supplied** (m13): `quote-substance-check.py` and `inference-ground.py`
   are read from the measured tree, so their exit code is the whole check and a `--root` candidate can ship
   `sys.exit(0)`. The landed lane does not — r50 `quote-substance-check.py`/`build-spans.py` are the r49
   files with the round number replaced (`diff` shows only round/path lines; erratum item 3 is true) — but
   the *evidence* for SUBSTANCE is an exit code, not an independent measurement.
4. **`QUARANTINE_VERDICTS=0/0` is vacuous and self-declared.** Replayed the lesson's own sweep
   (`awk -F'|' … $2 ~ "\`chousa\`" …` → 24 rows; theme hosts in column 6 → 0; whole file → 0), so the
   vacuity is real, not a parse bug (the counter's `f[5]` = awk `$6`, consistent). If a theme row
   ever appears, the verdict is read from the **lesson's** text, not the register's own class — the
   lane can self-declare `present`.
5. **Tree, not commit.** Entries, registry, lesson and manifest are read from `root` (`:146`); only the
   base registry comes from git. A dirty tree passes; `git status --porcelain corpus/ tools/` is empty now,
   so today's pass equals the commit — re-run it only on a clean tree.
6. **CJK polarity is invisible.** `words()` is Latin-only, so m17 (a bullet asserting the opposite of
   its quote) passes every leg. The tool's own docstring names this; the counter inherits it silently.
7. **Registry substance is unread.** `BOUND` needs only `mined`/date/`used-by`/`source:` equality; my
   rows say `scope: probe`, `teaches: nothing` and pass. Depth of the row is a reader's judgement.

## 5. Real-lane calibration (what the pass actually measures)

- 55 rows, 47 distinct quotes, 23 in their entry's Inference (32 not); 11 rows under 12 non-space
  chars, all S105; every inference-used quote occurs **exactly once** in its capture (max = 1). Weakest
  bullet tokens: `第 6 章 辅助功能` (7 chars, a chapter heading) and `各项内容都相同` (7); the 4-char
  floor permits both, so the closure must read those two bullets as prose.
- The post-freeze CJK floor is **load-bearing for exactly one entry**: with the pre-freeze tool
  (`git show 3c51da77:tools/inference-ground.py`) r39 and r40 exit 0 but
  `citation-matching-semantics-r41.md` prints `tokens=0 grounded=0`, 4×`INF_UNGROUNDED`, rc=1. So the
  disclosed relaxation (erratum item 2) is what makes `INFERENCE_GROUNDED=3/3` reachable at all —
  admissible only because it is a disclosure, not a post-data narrowing, and it does not touch the
  leg's text.
- Peer `R50ReopenRowS105`'s −80/−48 "offset drift" is a false positive, retracted: `offset` is the
  span-block start (`max(0, off−80)`), and `cap[30581:30751] == spans/S105-3.txt` with the quote at span
  index 80; `CAPTURE_BOUND=55/55` independently forbids the drift theory. Naming note only.

## 6. What the closure must spot-check by hand (this is the only safe correction; the counter is frozen)

1. Read the 32 quotes that no bullet uses and confirm they belong in Observation/Unknown — not filler.
2. Read the two 7-char bullet tokens (`第 6 章 辅助功能`, `各项内容都相同`) in their bullets.
3. Confirm the lesson's `refused-doc` line names a document that is *not* bound and that its reason matches
   the capture (done here: 引文核对 absent, 标明引文 present), and that no quote's claim rests on a
   heading/timestamp/title block (landed: `更新时间`, `第 6 章`, `产品名称`, used only as scoping).
4. Re-run `SUBSTANCE` and `INFERENCE_GROUNDED` by reading the two checker files at the commit, not by
   trusting `SUBSTANCE=PASS`; and run on a clean tree.
5. Treat `QUARANTINE_VERDICTS=0/0` as no evidence, per `corpus/lessons/round-50.md:117`.
6. Do not accept a bullet that only quotes a phrase (m1/m17 class): every Inference bullet of the
   three entries must be read as an assertion.

Scratch `/dev/shm/chousa-r50-R50CritForgeC2/` deleted (root + 14 variant roots + `ig-base.py`).

VERDICT: attacked the frozen C2 counter and `quote-substance-check.py` with a 34-line forge — **defect found**: boilerplate/title-block quotes, duplicate quote rows, one anchor, a false `refused-doc`, assertion-free and even polarity-inverted inference bullets, and a 4-char common-word token all print `C2=PASS` (rc=0), while the capture digest/offset binding, anchor membership, `used-by` equality, the ≥3-distinct-row and 12-char floors, and the 4-CJK bullet floor have real teeth; the two substantive legs are root-supplied exit codes and `QUARANTINE_VERDICTS=0/0` is vacuous, so the pass measures binding and presence, never entailment.

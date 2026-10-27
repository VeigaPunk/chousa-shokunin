# R53DraftQuality — QUALITY criteria 91–94 (round 53, wave 1)

Seat: scribe. Lane repo `/home/vgpnk/Projects/shokunin/chousa-shokunin` at HEAD `6365f15`
(frozen claims `a6ff732`, candidate v4 `32aab5e`, `BASE_REV` `5b550133`). No lane file written;
scratch `/fast/scratch/hyaku/chousa-r53/R53DraftQuality` (removed at exit). No install needed
(no pacman/uv/npx call made; pacman guard respected).

## 1. Behaviour

Drafted four append-only criteria in the shape of 87–90 (bold lead, evidence with file:line,
`Check:`, `Shown able to fail (ran):`, `Named limits:`, `— <lesson or closure item>`). Every
check named below was run from this seat; every red-before is a text I opened or an output I
produced, not a claim I copied. I did not write, renumber or measure either frozen claim: the
numbers quoted are check runs, and no claim verdict is asserted here (executive/reviewer seats
own the measurement).

Placement: `corpus/QUALITY.md` ends at criterion 90 (`:923`); criteria 87–90 themselves sit
under the round-51 header (`:849`), so the L1 may append these four either with or without a
new `## Round-53 additions (appended 2026-10-26; criteria 1–90 unchanged)` line.

## 2. Gates — drafted criteria (intended lane path `corpus/QUALITY.md`, appended after `:923`)

```markdown
  91. **A frozen capability counter generates representation variance inside the input's identity rule, so a forge
      keyed to one spelling fails.** The round-52 counter drew text and names from fresh randomness (criteria 81, 85)
      and still spelled every document one way, so an 85-line forge passed `LEGS=9/9` (ran:
      `python3 corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/forge-shape.py` →
      `LEGS=9/9 C1=PASS`). The round-53 counter spells one URL five ways inside the census identity — http or
      https, upper-case host, a trailing `/` (`corpus/evidence/round53/c1-count.py:96`) — writes Registry rows at
      0–3 leading spaces (`:138`) under `##` + space or tab (`:141`), and re-draws the spelling for every staged
      row and every entry citation. Check: `python3 corpus/evidence/round53/c1-count.py --tool <tool> --seed 53
      --per-leg 1` — the landed tool gives `LEGS=8/8 C1=PASS`; the same tool with `url_of` replaced by an
      exact-spelling read (`re.search(r"https?://[^\s|]+", s).group(0)`) gives `LEGS=5/8` with
      `TWIN=FAIL HELD=FAIL MIX=FAIL map=differs`, while RECHECK/ORDER/NOENTRY/REAL/REGRESS still pass (both ran).
      Named limits: `spell` varies host case only — the counter's own expectation lowercases the whole URL
      (`:191`) while the tool's identity lowercases the host alone (`tools/assimilate-rows.py:133`), so a
      path-case variant would set the expectation against the tool and is not generated (reported below); the
      REAL leg's spellings are the campaign's own, so the spelling-keyed tool passes REAL
      (`CITED=6 APPEND=5 HELD=0 TWIN=1`) and only the six generated legs catch it; a tool that normalises
      *more* than the census identity (casefolding the path) is not exercised at all.
      — `corpus/lessons/round-52-verifier-spotcheck.md` section 6 item 3; `corpus/lessons/round-52.md`
      `## Mistakes` row 3.

  92. **An adopter label names what is true of the registry: `held` only for a URL a Registry row carries, `twin`
      only for an id the same run minted, and the count line carries both.** At `BASE_REV` the adopter labelled
      staged S195 `held` — `CITED=6 APPEND=5 HELD=1`, `S195 → S118` — although no row of `corpus/SOURCES.md` at
      that revision carries its URL (0 rows match `url_of`; the id `S195` does not occur there): the id was
      minted by the run, which is `twin`. Check: `python3 corpus/evidence/round53/c1-count.py` legs TWIN, HELD,
      MIX, REAL — the landed tool prints `HELD=0 TWIN=1` on REAL and `LEGS=8/8 C1=PASS`; the tool at `BASE_REV`
      prints `HELD=1` with no `TWIN=` token at all and `LEGS=1/8` (both ran). Shown able to fail (ran): the base
      tool's HELD case reaches `map=ok rows=1` and still fails its leg, because its count line carries `HELD=`
      but no `TWIN=`; the label defect itself appears only on REAL. Named limits: the legs read
      `renumber.tsv`, `append.md` and the count line — right counts with wrong labels fail the map leg
      (observed on the spelling-keyed tool), right labels with one missing count token fail the count leg
      (observed on `BASE_REV`); neither leg reads the label's prose. — `corpus/lessons/round-52-verifier-spotcheck.md`
      section 6 item 4 (round-51 routed 2).

  93. **A refusal reason is the decisive one: when a row or entry is refused on two grounds, the Gate and the tool
      state the ground that holds alone, and a province reason is used only for the claim's spine.** Round 52
      refused the grey-literature entry with "out of province for its spine" (`corpus/lessons/round-52.md:64`)
      although the headline is a search-record field and so in province, and the ground that held alone was URL
      duplication — `SOURCES.append.md:36` and `:58` carry the same URL byte for byte (ran); the non-author
      closure recorded it as a disputed reason (`round-52-verifier-spotcheck.md:77`, "agree on the decision,
      **disagree on one reason**"). Check: for each refusal cell naming two grounds, withdraw one ground and
      re-test the other on the row alone; the cell's first ground must be the one that survives. Runnable legs
      (ran): the two campaign rows' URLs are identical; a staged row that is both ten cells and URL-less gets one
      line, `REFUSED S200: staged row has 10 cells, not 11`, from the `if`/`elif` at
      `tools/assimilate-rows.py:467-469` — the cell-count ground, not the URL ground. Named limit: the Gate side
      is a manual check, as 89 is; the two legs show the grounds, not the Gate's choice of one.
      — `corpus/lessons/round-52-verifier-spotcheck.md` section 6 item 2; the `grey-literature-and-chinese-search-record-r40.md`
      Gate row of round 52.

  94. **A routed defect that two closures carry is landed with a test or retired with a reason in the next round,
      never carried a third time unlanded.** The adopter twin-label defect was routed in round 51
      (`round-51-verifier-spotcheck.md` section 6 item 2, "fix with a self-test row each") and carried in round 52
      (`round-52-verifier-spotcheck.md` section 6 item 4, "built in scratch and not landed"), with no commit
      touching the tool in that window (ran: `git log --oneline 41b4dca..5b550133 -- tools/assimilate-rows.py` →
      0 lines). Round 53 landed it: `git log --oneline 5b550133..32aab5e -- tools/assimilate-rows.py` →
      `32aab5e round-53: C1 candidate — adopter v4 twin label, recheck pre-pass, registry-first refusal;
      self-test cases`, carrying `corpus/fixtures/assimilate-selftest/cases/twin-recheck` and `…/refusal-order`,
      and `python3 tools/assimilate-rows.py --selftest` → `SELFTEST=PASS findings=40 expected=40` (ran). Check:
      for every item a second closure re-lists, one of — a commit inside the round window that touches the named
      surface and carries the self-test case, or a lesson sentence naming why it is retired; a third carry with
      neither fails. Named limit: the window is read by path, so a landing that renames or moves the surface is
      invisible to it, and the retirement-sentence branch is unreadable mechanically; the criterion binds the
      queue, not the fix (the claim's counter owns that). — `round-51-verifier-spotcheck.md` section 6 item 2
      (routed 2 of 4), `round-52-verifier-spotcheck.md` section 6 item 4.
```

## 3. Receipts (commands run from this seat, verbatim tails)

Generator variance — `python3 gen-variance.py` (imports `c1-count.py`, `random.Random(53)`):

```
URL https://6efbe-015.test/b481/51b7e6
SPELL http://6EFBE-015.TEST/b481/51b7e6/
SPELL https://6efbe-015.test/b481/51b7e6/
SPELL http://6EFBE-015.TEST/b481/51b7e6/
SPELL https://6EFBE-015.TEST/b481/51b7e6
SPELL http://6efbe-015.test/b481/51b7e6/
ROW ' | S001 | Lane doc f7f — https://7b742-131.test/fca8/71cd45 '
ROW '| S003 | Lane doc 0de — http://8ead3-072.test/cb86/8fa55b/ |'
SEP_TAB True
INDENT_WIDTHS [0, 1]
```

Spelling-keyed tool — `python3 corpus/evidence/round53/c1-count.py --tool spell-forge.py --seed 53 --per-leg 1`:

```
TWIN case1 FAIL rc=0 held=0 twin=2 append=3 map=differs rows=5
HELD case1 FAIL rc=0 held=4 twin=0 append=1 map=differs rows=5
MIX case1 FAIL rc=0 held=2 twin=2 append=3 map=differs rows=7
REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
LEGS=5/8
C1=FAIL
```

Tool at `BASE_REV` (`git show 5b550133:tools/assimilate-rows.py`, 514 lines) — same command:

```
REAL FAIL rc=0 map={'S134': ('S117','append'), …, 'S195': ('S118','held')} rows=5 count-line=['CITED=6 APPEND=5 HELD=1']
LEGS=1/8
C1=FAIL
```

Landed tool at HEAD (blob `sha256 32628bbc…8ed636` = `32aab5e:tools/assimilate-rows.py`) — same command:

```
TWIN case1 PASS rc=0 held=0 twin=2 append=3 map=ok rows=3
HELD case1 PASS rc=0 held=4 twin=0 append=1 map=ok rows=1
REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
LEGS=8/8
C1=PASS
```

Two-ground refusal — `python3 tools/assimilate-rows.py … --entry corpus/knowledge/e1.md` on a 10-cell, URL-less
staged row S200 with a sound registry:

```
COLLISIONS=0
REFUSED S200: staged row has 10 cells, not 11
rc=1
```

Duplication ground — `python3 -c "…re.findall(r'https?://[^\s|]+', L[n-1])…"` on the campaign file:

```
36 1 ['https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3']
58 1 ['https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3']
```

S195's URL against the registry at `BASE_REV` (0 rows match `url_of`; no `| S195 |` id):

```
S195 url_of www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
base registry rows carrying it: 0
S195 row present in base registry ids: False
```

Land windows and self-test — `git log --oneline 41b4dca..5b550133 -- tools/assimilate-rows.py` → 0 lines;
`git log --oneline 5b550133..32aab5e -- …` → `32aab5e …`; `python3 tools/assimilate-rows.py --selftest`:

```
FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6
SELFTEST=PASS findings=40 expected=40
rc=0
```

## 4. Touched surfaces

Read only: `corpus/QUALITY.md:849-923`, `corpus/evidence/round53/{claims.md,c1-count.py,c2-count.py}`,
`corpus/evidence/round53/controls/{c1-before.txt,c2-before.txt}`, `corpus/lessons/round-52.md`,
`corpus/lessons/round-5{1,2}-verifier-spotcheck.md`, `tools/assimilate-rows.py`,
`corpus/fixtures/assimilate-selftest/expected.json`, `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`,
git objects `5b550133`, `32aab5e`. Written: this report only. Counters ran with `TMPDIR` in scratch and
`--work` under scratch; both counters wrote nothing in the lane (`c1-count.py` docstring `:32-34`).

## 5. Findings (reported, not patched)

1. **The red-before text criterion 92 names is not in the committed receipt.** `controls/c1-before.txt` has
   0 lines containing `CITED=` (`grep -c` → 0) and shows only `REAL=FAIL`; the `CITED=6 APPEND=5 HELD=1` line
   quoted in `claims.md` (C1 "Before") is reproduced only by re-running the base tool, which I did. The receipt
   should carry the REAL detail line, or the claim should cite the run, not the file.
2. **The counter's expectation and the tool's identity rule are two different rules.** `c1-count.py:191`
   (`norm = lambda u: re.sub(r"^[a-z]+://", "", u.lower().rstrip("/"))`) lowercases the whole URL;
   `tools/assimilate-rows.py:133` lowercases the host only. `url_of("https://Ex.AMple.test/Path/1")` →
   `ex.ample.test/Path/1`, `norm(…)` → `ex.ample.test/path/1`, `agree False` (ran). Unreachable today because
   `Gen.spell` uppercases only the host (`:96-105`), so the variance is safe only by the generator's restraint,
   not by the rule; a path-case spelling would make a correct tool fail the TWIN/HELD legs.
3. **The base tool's HELD leg fails on a count token, not on a label** (`map=ok rows=1`): `HELD=` is present and
   `TWIN=` absent. The label defect shows only on REAL, so a future red-before that cites the generated legs
   would witness the wrong thing.
4. **`--per-leg` default 3 vs the receipts**: my runs used `--per-leg 1` for speed; the frozen target's three
   unseeded runs are the executive seats' to produce, and nothing here substitutes for them.
5. No conflict and no contract modification was produced; the frozen predicates, targets, counters and controls
   were not touched.

VERDICT: built and landed-in-report four QUALITY criteria (91–94) with runnable checks — representation-variance
falsification (spelling-keyed tool 5/8 vs landed 8/8), the `held`/`twin` label red-before (`HELD=1` at `BASE_REV`,
S195's URL in 0 registry rows), the decisive-refusal ground (identical campaign URLs; one-line ten-cell refusal)
and the two-closure queue landing (`32aab5e` + two self-test cases, `SELFTEST=PASS`) — and found the `c1-before.txt`
REAL line missing plus a counter/tool identity-rule divergence, both reported unpatched.

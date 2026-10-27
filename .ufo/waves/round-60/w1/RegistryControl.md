# RegistryControl — round-60 registry and citation-control analysis

Seat: executor. Bounded to the frozen claims (`corpus/evidence/round60-claims.md`), prior committed
evidence, and the current counters/sources. Read-only: one aggregate census run, four counter runs
(all against scratch mirrors or the unmodified lane), and fixture rows under
`/fast/scratch/hyaku/chousa-r60/RegistryControl/` (removed before yield). No fetch, no git/jj
mutation, no write outside this report. Scratch receipts are embedded verbatim below because the
seat may not add files to the wave dir.

Lane state I measured against: `jj-lane.sh state` → `branch=master local=b379919a… remote=b379919a…
ahead=0`, `tracked=0 untracked=3` (`corpus/evidence/round60-claims.md`, `corpus/evidence/round60/`,
`.ufo/waves/round-60/`). So every byte quoted here is either committed at `b379919a` or a round-60
artifact that is not yet committed.

## Verdicts at a glance

| layer | verdict | one-line receipt |
|---|---|---|
| SOURCES.md registry integrity | **holds** | 133 rows S001–S133, contiguous, 11 columns each, 0 duplicate ids, 0 dangling `used-by`; census exit 0 |
| `used-by` ↔ cited-file agreement | **holds** | 124 `used-by` pointers, every file exists and names its own id; 0 defects |
| staged-package id collision control | **blocked as-is** | 52 colliding ids S082–S133; **4 are same-document** (S100–S103) and must not be renumbered |
| 0–3-space guard soundness | **holds (fixture-proven)** | column-zero pattern → 0 collisions on an indented fixture; contract pattern → 1 |
| C2 frozen predicate control | **kill: base meets target** | pristine-base mirror prints `C2=PASS`, exit 0 |
| C2 predicate component (scorecard disposition) | **not implemented** | counter never opens `SCORECARD.md`; `SCORECARD.md` has no round-60 disposition line |
| C2 `--root` isolation | **broken** | form is script-global `ROOT`; mirror run still printed `FORM_PIN=1/1` |
| C2 `--work` argument | **decorative** | parsed, never used |
| S101 locator basis | **consistent but split** | registry offsets resolve in the raw UTF-16LE decode; the round-60 gate uses the filtered form's line 245 |
| assigned immutable claim SHA | **does not match frozen bytes** | file `65721569…`; assignment quotes `09d8053f…` |

## E1 — registry structure (reproduced this round)

```sh
python3 - <<'EOF'   # over corpus/SOURCES.md, rows matched with ^ {0,3}\|\s*S\d{3,}
EOF
data rows 133
dup ids []
max 133 missing []
col-defects 0 []
dangling used-by 0
defects 0 []            # opened ISO / recheck in {ISO, NNd, on-release}
```
```
lane rows at col0: 135 (`grep -cE '^\|' corpus/SOURCES.md`)   # header + separator + 133 rows
lane rows indented 1-3 spaces: 0
```

**E1b — census (round-60 start state, re-run by me, read-only):**

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa  W04  S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa  W04  S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa  W04  S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa  W04  S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa  W04  S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa  ok   /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
census_exit=0
```

**E1c — W04 rows adjudicated individually (all benign, none appendable-as-new):**

| row | status | why the warning is benign |
|---|---|---|
| S050 / S051 | mined / mined | same page, different sections (8.1.2.4 optional tags vs 8.2.5.4.4 in-head insertion); distinct anchors, both cited by `quote-reopen-r30.md` |
| S052 / S053 | mined / mined | anchor-distinct (`#socket-timeouts` vs `#socket.create_connection`) |
| S071 / S073 / S075 | mined / mined / mined | fragment-stripped collision only: `env(1)`, `sha256sum(1)`, `mktemp(1)` are three different man pages under one canonical coreutils URL |
| S059 / S074 | mined / **rejected** | correct rejection: S074's own `teaches` says `REJECTED: S059 already holds this page and digest-input scope`; `used-by` is `—` |

The census's W04 class strips the fragment, so it fires on anchor-distinct rows. It is a warning
class, not a defect class; exit 0 is correct here. No row needs a supersede action.

## E2 — `used-by` drift (registry → knowledge/lesson files)

```sh
# for each used-by path: file must exist AND contain its own S-id
used-by pointers 124 defects 0
```

Zero drift: every `used-by` pointer resolves and every cited file actually names the row. This is
the one registry property a *do-nothing* control cannot fake — the check compares two independent
surfaces (registry cell vs file body).

## E3 — staged-package id collisions, with the same-document subset split out

Reproduced from the lane registry and `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`
(114 staged rows), URLs compared per id:

```
lane rows 133 staged rows 114
collisions 52 same-url 4 diff-url 48
same: ['S100', 'S101', 'S102', 'S103']
```

**This is the finding the plain `comm` guard cannot see.** For S082–S099 and S104–S133 the colliding
id names a *different document* on each side (e.g. S082 = AVeriTeC raw data vs the package's
`10.1186/s13643-020-01542-z`), so renumber-by-document is the right repair. But S100–S103 collide on
the **same URL** on both sides — the CNKI cluster the lane already mined, and the exact sources the
r37 entry and the frozen C2 claim cite:

```sh
grep -m1 '^| S101 |' …/merge/chousa/SOURCES.append.md
| S101 | 中国学术期刊（光盘版）检索与评价数据规范（修订本）— copy hosted by 哈尔滨工业大学 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc | docs | B | …
```
(identical URL to lane row `corpus/SOURCES.md:111`).

Consequence for C2: a mechanical renumber map applied to all 52 collisions would mint **second ids
for S100–S103**, i.e. two registry ids for one document (census E04 duplicate-within-scope on the
next validate) and a *split citation layer* for precisely the source the frozen C2 claim rests on.
Correct handling, per CORPUS.md rule 2 (append-only, supersede, never re-issue an id for held
material): the 4 same-document rows are **not appendable at all** (already held); only the 48
different-document rows take renumbering, each re-pointed by document.

## E4 — the 0–3-space collision guard is sound; the column-zero shorthand is not

Fixture in scratch (`reg-indented.md` has `  | S002 | x |`, i.e. two-space indented; `staged.md` has
`| S002 |` and `| S150 |`):

```
col0-only:  0        # grep -oE '^\|[[:space:]]*S[0-9]{3,}' …
0-3space:   S002 → 1 # grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …  | comm -12
```

The contract pattern catches the indented collision the shorthand misses. Both patterns agree on
today's registry only because it has **zero** indented rows (E1), so the indented failure mode is a
future-appender risk, not a current miss. Guard verdict: sound; keep the `^ {0,3}` form in any
committed counter (this is the `devils-advocate`-class fixture the §10 clause demands).

## E5 — C2: the frozen base already meets the frozen target (kill witness)

Scratch mirror built **from the base commit's own bytes**, not the worktree, so no in-round edit can
explain the result:

```sh
S=/fast/scratch/hyaku/chousa-r60/RegistryControl
git show master:corpus/knowledge/citation-count-semantics-r37.md > "$S/baseroot/corpus/knowledge/citation-count-semantics-r37.md"
cp corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw "$S/baseroot/corpus/captures/"
python3 -B corpus/evidence/round60/c2-count.py --root "$S/baseroot" --work "$S/basework"
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

The frozen claim says *"Base must fail because no round-60 entry exists."* It does not: the counter's
`ENTRY` is the pre-existing `corpus/knowledge/citation-count-semantics-r37.md`, and at base that file
already carries every component the counter tests — `#### Unknown` at line 74 and, at lines 78–79,
literally the sentence the `LIMIT` check greps:

```
78: - Whether the specification copy (S101) is the version in force, and whether
79:   the counted records in S100 or S102 apply its codes.
```

`grep -c 'Whether the specification copy (S101) is the version in force'` on
`git show master:corpus/knowledge/citation-count-semantics-r37.md` → `1`.

So a do-nothing control — zero round-60 work — reaches the target. Per §9 the counter or the target
is wrong, and this round cannot claim C2 as declared.

**The counter does measure something**, which is worth keeping: replacing `#### Unknown` with
`#### Other` in the mirror flips only the LIMIT pin and the exit code.

```
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=0/1
C2=FAIL
exit=1
```
Note `FORM_PIN=1/1` on a root that contains no `.ufo/` at all — see E6.

## E6 — three frozen C2 components are not implemented

1. **"require the scorecard's declared disposition"** — `c2-count.py` contains no reference to
   `SCORECARD` (grep: none; its only inputs are `RAW`, `FORM`, `ENTRY`). `SCORECARD.md` in turn has
   no round-60 disposition line (`grep -n "round 60\|round-60\|Round 60" SCORECARD.md` → 0 matches;
   its newest section is the round-58 verdict block). The component has neither a reader nor a
   referent.
2. **`--work <fresh-absolute-dir>`** — parsed, never used (`grep -n "a.work" c2-count.py` → none).
   The counter writes nothing, so this is not an ENOSPC risk (§7 rule 4 is satisfied by omission),
   but the predicate's fresh-dir requirement is decorative.
3. **`--root <lane-copy>` isolation** — `FORM` is built from module-level `ROOT`
   (`c2-count.py:7`), while `raw`/`entry` come from `root`. Proven by the mirror run above: a root
   with no round-60 form still reports `FORM_PIN=1/1` because the form came from the *lane*. A
   lane-copy invocation therefore mixes the copy's entry with the fleet lane's form, which the
   frozen predicate's `<lane-copy>` does not authorize.

## E7 — the counter never touches the registry, so "S101 citation and metadata" is unpinned

The claim's third component is *"verify its S101 citation and metadata"*. What the counter checks is
three substrings in the entry body (`source: S101 — https://jc.hit.edu.cn/`, `verified-at:`,
`recheck:`). It never reads `corpus/SOURCES.md`, so all of these stay green while the citation layer
rots:

- deleting `corpus/knowledge/citation-count-semantics-r37.md` from S101's `used-by` cell;
- flipping S101's `status` from `mined`, or changing its `recheck`/`opened`;
- pointing the entry at an S-id whose row no longer exists (the counter matches the literal
  `S101 — URL` string, not the registry).

Current row, for the record (all sound today): `S101 | docs | B | mined | opened 2026-10-25 |
recheck 180d | used-by citation-count-semantics-r37.md, lessons/round-58.md, lessons/round-59.md`,
scope limited to "the data specification whose fields and type identifiers underlie Chinese journal
evaluation and citation statistics". Adding one registry read (id exists, `status=mined`, `used-by`
contains the entry) is a three-line change that makes the component real.

## E8 — S101 locator basis: registry = raw UTF-16LE offsets, round-60 gate = filtered-form line

Both resolve; they are different bases, and nothing cross-checks them.

- Registry anchor cites `char 11170, 11205, 11993, 12161, 13247, 34374`. Those are **not** offsets in
  the round-60 form (27,012 chars): there, 11170 lands on `ilizing the ocean curren` and 34374 is
  past the end. They resolve exactly in the raw `.doc` decoded as UTF-16LE (64,512 chars):

```
utf-16le @11170 '为便于文献的统计和期刊评价，确定文献的检索范围，提高检索结果'   # the 文献标志码 sentence
utf-16le @12161 '文献类型及载体类型标志；\x0bd. 其他责任者(译者、校注、校点'      # the C2 quote itself
utf-16le @34374 '参考文献格式，参照ISO 690，采用1位字母：n——顺序编码制（Numeric' # the 15.7 parameter table
```

- The round-60 gate locates the same quote in the filtered form: `LINE=245`,
  `c. 文献类型及载体类型标志；` at form char 12,960 (single occurrence; `QUOTE=1/1`).

So the registry row is *not* stale — my first pass suspected it and the UTF-16LE test disproved that;
recorded here so no later seat re-opens it. The real gap is that an entry can cite S101 with a
form-line locator while the registry row carries raw-text offsets, and no committed check ties the
two locator families together. If the C2 note ships, its Gate should carry both: the registry's
`char 12161` (durable, raw-basis) and the form's `line 245` (artifact-basis).

The pin itself is re-derivable from committed bytes — raw capture is tracked
(`git ls-files` → tracked, sha `6063a3af…`, 47,356 bytes), and:

```sh
python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > $S/form/regen.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  $S/form/regen.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
```

Byte-identical to the pinned `FORM_SHA` and to the wave artifact. But the artifact is **untracked**
at base, so until the L1 commits `.ufo/waves/round-60/`, a closure cannot re-derive the C2 predicate
from committed bytes alone. Committing the wave dir (already required as wave evidence) closes this.

Provenance agrees across committed ledgers: `corpus/evidence/round57/refetch.tsv:66` and
`corpus/evidence/round49/spans.tsv:20` both record S101's URL + capture id `6dc68fd6b32ce9c8dfcebce8`
+ sha `6063a3af…`, matching the current raw. The row's `opened 2026-10-25` is the author-open date
(CORPUS.md:105), so the 2026-10-27 reopen legitimately lives in the wave receipt, not the registry.

## E9 — the assigned "exact immutable claim SHA" does not describe the frozen bytes

```sh
sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
len 3355
```
Assignment / dispatch quote: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.

Variants ruled out (raw, rstrip, rstrip+nl, CRLF, per-line-rstrip join): only the raw/`rstrip+nl`
form matches, at `65721569…`. No file under the lane or `.ufo/` carries the `09d8053f…` string except
the dispatch/spec and the peer reports that quote it.

Timing, so the freeze question is answerable rather than open-ended:

```
2026-10-27 17:51:18  corpus/evidence/round60-claims.md
2026-10-27 17:51:43  .ufo/waves/round-60/s101-open.txt
2026-10-27 17:52:14  corpus/evidence/round60/c2-count.py
2026-10-27 17:55:21  .ufo/waves/round-60/w1.ready        (dispatch)
```

The claims file predates dispatch by four minutes, so its bytes were **not** edited after dispatch;
the mismatch is upstream of the freeze (the quoted digest never described these bytes). The file is
untracked at `b379919a`, so no committed byte pin exists either. I did not modify it.

## E10 — round-60 Gate surface

`corpus/lessons/round-60.md` does not exist yet (newest committed lesson: `round-59.md`). The §2b
Gate requirement ("URL, access date, ≤25-word located quote" per new row) therefore has no landing
site yet; `.ufo/waves/round-60/s101-receipt.txt` already holds all three fields plus the raw/form
digests, so the L1 can carry it into `## Gate` verbatim. Not a defect at wave 1 — a hand-off.

## Findings the L1 can act on

1. **Kill C2 as frozen (E5).** The base mirror passes; the target is reachable with no work. Either
   the counter's `ENTRY` must name a round-60-specific note and the target must be "base fails", or
   C2 reports honestly as not-admitted. Do not repair by weakening; do not narrow after landing.
2. **Implement or drop the scorecard-disposition component (E6.1).** Today it has neither reader nor
   referent.
3. **Derive `FORM` from `root` (E6.3)** and use `--work` for any artifact the counter writes (E6.2).
4. **Add the registry read to the C2 gate (E7)**: id exists, `status=mined`, `used-by` contains the
   entry. This is the cheapest way to make "its S101 citation and metadata" a measured thing.
5. **Do not renumber S100–S103 (E3).** The collision map must carry the same-document split; 48 ids
   take renumber-by-document, 4 are already held.
6. **Carry both locators into the Gate (E8):** registry `char 12161` and form `line 245`.
7. **Commit `.ufo/waves/round-60/` (E8)** so the pinned form is re-derivable from committed bytes.
8. **Reconcile the assignment digest (E9)** before any closure relies on "immutable" claims; the
   file's own sha256 is `65721569…` and it predates dispatch.

## Limits

I did not adjudicate C1 (`c1-count.py` internals belong to the C1 seats; I only confirmed its
`R55` control path resolves: `corpus/evidence/round58/controls/build-spans-r55.py` is tracked, and
the L1's `c1-before.txt` base is an honest `C1=FAIL` with `CANDIDATE_REFUSAL=0/1`, i.e. C1 — unlike
C2 — has a live before→after). I did not judge QUALITY admission for any proposed C2 note, did not
open the S101 source live (offline capture only), and did not test the census beyond its validate
subcommand. Scratch `/fast/scratch/hyaku/chousa-r60/RegistryControl/` removed before yield.

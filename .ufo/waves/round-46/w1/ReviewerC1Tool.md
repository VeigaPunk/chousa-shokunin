# ReviewerC1Tool — code review of `tools/inference-ground.py` against frozen R46-C1

leaf reviewer, no dispatch. item: the six questions at `gen-w1-spec.py:134`. no edits, no
installs, no pacman, no network. scratch `/tmp/chousa-r46-ReviewerC1Tool/` removed at end.

## Provenance — the file moved three times under the review

240 ln (first read) → `61c09d72…be6aeac5` 260 ln @07:26:36 (+`--registry`) →
`397d9878…4111e4f2` 265 ln @07:27:37 (fences no longer hide bullets; junk leg `==1`) →
**`819f83eb…4275326bc` 276 ln** (span-file containment, `:149-160`). Siblings made the edits
(`MutC1Junk`, "sentinel F3" named). Pinned: `819f83eb`, counter `819287e2…c9e0a65` (98 ln).

## Pinned run — C1 does verify at this sha

`python3 s3/c1-count.py --root <lane> --tool s3/inference-ground.py` (counter `819287e2`
pins all six fixtures plus `spans.tsv`/`counts.json`, `PINNED` `:37-46`, and passes):

```
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS   rc=0
```

Six fixtures with the same tool (`--spans`/`--counts`/`--root` in the fixture dir):

```
positive-a rc=0 bullets=1 tokens=1 grounded=1
positive-b rc=0 bullets=1 tokens=1 grounded=1
positive-c rc=0 bullets=1 tokens=2 grounded=2
junk-uncited    rc=1 INF_UNCITED + INF_TOKEN_NOT_IN_SPAN ('the release ships a frozen pool')
junk-ungrounded rc=1 INF_TOKEN_NOT_IN_SPAN ('reverse index of every citation')
junk-borrowed   rc=1 INF_TOKEN_NOT_IN_SPAN ('independently re-verified against a live source'), ('4,137')
```

The predicate is exit-code-only and it holds. The defects below are what it cannot see.

## The six questions

**1. Section ends at heading ≤4, fenced headings literal — yes, two wrinkles.** `break`
`:88-91` skips the flush but the post-loop append `:103-104` still emits `cur`, so a bullet
immediately followed by `#### Next` is kept (p2 bullets=1); levels 1–4 all end it (p19 `##`:
1 bullet rc=0); a fenced `#### Inference` is literal (p16 bullets=2, the bullet after the
fence still belongs to the section). Wrinkle A: HEAD_RE `:51` anchors at column 0, so an
ATX-legal indented heading (`   #### Inference`) is invisible (p10 `INF_SECTION_ABSENT`
rc=1). Wrinkle B: a level-5 heading is correctly not a terminator, but its text is glued
onto the previous bullet (`:97-102`; p17 rc=0 with `##### subordinate note…` inside bullet 1).

**2. Token extraction / numeral variants vs rule 3 — no, three mismatches.** Rule 3
(`:23-25`) says "a numeral of three or more digits, or a percentage"; NUM_RE `:50` needs a
digit then **2+** `[0-9,]`, so (a) `78.7` yields no token (p8 `INF_UNGROUNDED` rc=1, though
the figure is grounded); (b) commas count as digits, so `1,2` is a "three-digit" numeral
(p31 grounded by manifest `12`, rc=0); (c) `numeral_variants` `:123` strips `%`, so
`5,959%` is grounded by the bare count `5959` (p11 rc=0). Backtick/quote tokens also
carry a hidden 4-char floor (`:48-49`): `` `a b` `` is rejected and the regex then pairs
with the *next* backtick, fabricating a token — p9 `token='is fixed at build ('`; direct
trace `[' and ', 'S901']`.

**3. S-id inside code/backticks passes the citation leg — yes, by design and required.**
`:242` — `cited` is `ID_RE.findall(bullet)` over raw text, so `` (`S901`) `` cites S901;
all three positives use exactly that form, and `` `S901` `` costs no token
(`has_two_words("S901")` false, WORD_RE `:52`). `:116` scrubs ids before numeral
extraction, so `S901` never becomes `901` — load-bearing: a bullet carrying only
`` (`S901`) `` is `tokens=0`/`INF_UNGROUNDED` (p29 rc=1), so citing cannot double as
grounding.

**4. Counts leg — not case-safe, not label-safe.** `:252-253` accepts *any* manifest value
for *any* bullet numeral: no key, no label, no cited-source binding. p6 "7,572 answers
carry an archive link (`S902`)" → rc=0, though 7,572 is `answers_named_source` and the
archive count is 5,959. Formats are partial: numbers enter as `str()` + `f"{v:,}"`
(`:202-204`), strings only if `fullmatch(r"\d[\d,]*")` (`:205`) — `5959.0` does not ground
`5,959` (p30 rc=1) and a string `"78.7%"` is dropped (p7 with `counts-strpct.json` →
`INF_TOKEN_NOT_IN_SPAN '78.7%'` rc=1). A missing/unparseable manifest degrades to the
empty set (`:184-190`) with no error.

**5. `--root` mis-reports — yes, silently.** `:230-233` reports
`entry.resolve().relative_to(root)` and falls back to `entry.name` on `ValueError`, never
absolute and never warned. Two entries in `a/` and `b/` with `--root a` both print
`entry=entry.md` (p15, both orders). Default `--root .` is CWD-dependent (run from `/` it
printed `tmp/chousa-r46-ReviewerC1Tool/…`). `c1-count.py:61` passes `--root <fixture_dir>`,
so findings print as `positive-a.md`, not repo-relative; `--json` `:269` writes `entry_rel`
with no basename fallback at all.

**6. All six fixtures — pasted above: 0/0/0/1/1/1.**

## Findings

**HIGH**
1. `:254-256` — the registry escape is an unbounded substring test of the numeral against
   the row's whole `source` cell (title **and URL**); 27 of 86 registry rows carry a
   ≥4-digit run in that URL. Fabrications ground themselves: p23 "2,013 of the answers
   carry an archive link (`S020`)" → rc=0 (title contains `2013`); p24 "1,534 claims were
   re-verified (`S005`)" → rc=0 (title ends `…2025.acl-long.1534`). No fixture needs the
   leg (fixtures pass without `--registry`), claims.md authorises no such escape, and it
   falsifies the docstring's "Rule (the same sentence as `claims.md`, claim C1)" `:16`.

**MEDIUM**
2. Junk class (c) is not exercised. `claims.md:36-38` defines it as "a body that reuses the
   correct spans and figures while its inference asserts something else"; exactly that body
   passes — p1 (correct span + `5,959`, wrong conclusion) → rc=0. `junk-borrowed.md` dies
   only on an *invented* quote and figure, i.e. it is class (b) with borrowed neighbours.
   C1's 3/3 is real; class (c) should not be cited as demonstrated.
3. Zero parsed bullets ⇒ silence: `bullets=0`, rc=0, no finding, for a section written
   with `* ` bullets, as prose, or wholly behind an unterminated fence (p3, p18 at this
   sha; p4 before the fence fix). No `INF_NO_BULLETS` code (`:241-248`). Latent: all 7 lane
   entries use `- ` at column 0 today.
4. The fence fix (`:81-87`) over-corrects: the fence line `continue`s before the blank-line
   flush, so a fence no longer ends a bullet and later text is glued on (`:97-102`) — p26's
   trailing prose is checked against the bullet's citation (`INF_TOKEN_NOT_IN_SPAN
   'reverse index of every citation'` rc=1) — and a `- ` inside a fenced sample starts a
   real bullet (`:92` sits outside the `if not fence` guard) — p27 spurious `bullets=2 /
   INF_UNCITED bullet=2`.

**LOW**
5. Exit 2 is unreachable for `--spans/--counts/--registry`: only a missing entry returns 2
   (`:226-228`); `:137-138`, `:169-171`, `:184-190` silently return empty. Docstring "2
   usage or unreadable input" `:33` is untrue, and a manifest typo exits 1 — the same code
   as a real refusal.
6. Manifest parsing: `lines[1:]` `:140` drops row 1 unconditionally (a headerless manifest
   loses it silently — `spans-noheader.tsv` still rc=0 because the lost row duplicated an
   id) and `len(cells) != 7` `:144` drops rows silently. The `span_file` traversal hole I
   found at `397d9878` is fixed at `:149-160` — verified: a manifest whose only S901 row
   names `../../etc/passwd` now leaves the token ungrounded, rc=1.
7. Section start is `startswith("inference")` `:74`, so `#### Inference notes` or
   `#### Inference was rejected` opens the section.
8. `c1-count.py:72` resolves `--tool` against CWD, not `--root`; a relative control path
   with a foreign `--root` scores the wrong file (the committed controls use absolute
   `/tmp` paths, so `controls/c1-controls.txt` is unaffected).
9. Any Gate row must carry `--registry corpus/SOURCES.md` or it cannot pass the lane's own
   entries: without it both C3 entries fail (`INF_TOKEN_NOT_IN_SPAN bullet=4 token='7089'`
   and `bullet=3 … '7089'`, grounded=6/7 and 4/5, rc=1); with it both pass
   (`7/7`, `5/5`, rc=0). The spec the scribe works from (`gen-w1-spec.py:118`) omits the
   flag, and `SKILL.md:75` `## Gates` has no inference-ground row yet (`grep -n inference
   SKILL.md` → only the prose item `:69`).

## Verdict

C1 as frozen is satisfied at `819f83eb` (3/3, 3/3, rc=0; counter pinned to the same tool).
It is not fit to be quoted as closing "the D7 class": the fixture standing for class (c) is
killed by its invented tokens, not its borrowed ones, and a pure class-(c) body passes (p1).
The two later edits bought real fixes (fences no longer hide bullets; junk leg demands exit
1; span-file containment) at the cost of one new unsound escape (HIGH 1) that no fixture
requires and claims.md does not authorise. Recommended, all within the tool's own contract:
drop the registry leg or reduce it to an exact document-number token with the URL stripped;
bind the counts leg to the cited source; add `INF_NO_BULLETS`; use exit 2 for unreadable
manifests; put `--registry` in any Gate row.

## Residual risk / gaps

- Pinned to `819f83eb`; a fourth edit invalidates the citations (behaviours reproduced at the
  last two shas). No `git archive` counter run (`ExecCounterRun` owns it); lane tree, fleet repo
  and shokuknow untouched; no fetch, no installs.

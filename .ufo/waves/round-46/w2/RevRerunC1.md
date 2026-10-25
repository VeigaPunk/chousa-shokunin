# RevRerunC1 — re-run of R46-C1 on a clean archive of `d09fc8e7` (operability)

seat: `L1Chousa46.RevRerunC1` (reviewer, leaf; no dispatch, no network, no install)
item: re-run C1 over `git archive d09fc8e7…` in /tmp, paste output + exit, hash the counter /
tool / six fixtures, confirm each fixture hash equals `PINNED`, verdict re-derived | diverged.
bounds: read-only on the lane; mutations only in `/tmp/chousa-r46w2-RevRerunC1/` (removed);
only this file written. Frozen claims read first (`corpus/evidence/round46/claims.md`); no
predicate, target or kill rule re-scaled.

## 1. Byte identities at the scored commit

```
$ git -C …/chousa-shokunin archive d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a | tar -x -C /tmp/…/fresh
$ sha256sum corpus/evidence/round46/c1-count.py tools/inference-ground.py \
    corpus/fixtures/inference-ground-r46/*.md …/spans.tsv …/counts.json …/spans/*.txt
819287e2075c3f5b57c4ceb26fb6b3d7594af48e03ad7cfcd61690727c9e0a65  corpus/evidence/round46/c1-count.py
819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc  tools/inference-ground.py
cba03251466e44773ef0ed9e080388b284f30f1ada0034e6b3c824d364ceb778  …/junk-borrowed.md
7b3e6b6e36c771a336d7da17291d94861226af289b2a2c7d4a6ef7d68016e598  …/junk-uncited.md
ab32577d5266fbb07a04a63735e1f4f7432b06841a64fa3ff840b42c2f457fe4  …/junk-ungrounded.md
1378296857c6193d80ce9649f5778216003f10ffdd645c0461fa43c2c46b8a21  …/positive-a.md
1d09c94bd4668fc31389a07354c312ca86b5e8dd0e644b84e3fe69e25a46ced4  …/positive-b.md
4e61f56c8af38418754561096e7e22b8aa54e042bf0b86c4ad36542c7c6f417a  …/positive-c.md
38a536bd9d33d0dc45d441cce6ce1882a1f4e60ee8ecdaebfd9f85a229d2aff4  …/spans.tsv
fd414d0a24883711dab8e27bd36e0aad00e6e09192d51b7bf75228e3f76fbb5c  …/counts.json
7c2aa3214d9409886ca91fefa1ed69599c29ec521cd745affae86f93b762b1ef  …/spans/S901-1.txt
c2184ca73ce45977b629591c786525bf8bf7899bc436f443af91feab396f20e4  …/spans/S902-1.txt
```

PINNED comparison done by script (parse `PINNED` with `ast`, hash each target), not by eye:

```
positive-a.md … junk-borrowed.md spans.tsv counts.json   → MATCH ×8
PINNED_MATCH_ALL=yes   PINNED_ENTRIES=8
```

The frozen kill rule says "a fixture set changed after this freeze fails the claim". The tree
holds **10** fixture files (`git ls-tree -r d09fc8e7 corpus/fixtures/inference-ground-r46 | wc -l`
→ `10`); `PINNED` binds **8**. The two unbound files are `spans/S901-1.txt` and
`spans/S902-1.txt` — exactly the texts the tool grounds against, named by the pinned
`spans.tsv`. Finding C1-F1.

## 2. The counter run (decisive)

```
$ cd /tmp/chousa-r46w2-RevRerunC1/fresh
$ python3 corpus/evidence/round46/c1-count.py --root /tmp/chousa-r46w2-RevRerunC1/fresh
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=3/3
C1=PASS
EXIT=0
```

Default-root form (LANE = `parents[3]` of the counter, i.e. the archived copy) prints the same
four lines, exit 0. The output line reproduces the frozen target verbatim; no leg short.

**Verdict: re-derived.** Every declared figure of R46-C1 reproduces from the archived bytes
alone (no working-tree file read: `--root` points at the archive). The findings below are what
the PASS does not cover, not a divergence in any declared number.

## 3. Findings

**C1-F1 — Medium — `PINNED` does not bind the span texts (kill rule half-enforced).**
`corpus/evidence/round46/c1-count.py:37-46` lists 8 names; the `spans/` files are absent, and
`:77-80` only walks `PINNED`. A post-freeze edit to the *grounding evidence itself* is
invisible as long as it moves no verdict:

```
$ printf '…frozen pool of pages; no revision is recorded per sentence, and every claim was
  independently re-verified against a live source\n' > …/spans/S901-1.txt
$ sha256sum …/spans/S901-1.txt
fbd444c698dd36e9ae91592e63585deda6b990d692a97bdc7fc8e6c9dd978770   # was 7c2aa321…
$ python3 corpus/evidence/round46/c1-count.py --root $PWD
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS      EXIT=0   # no FIXTURES_CHANGED
$ python3 tools/inference-ground.py --entry …/junk-borrowed.md --spans …/spans.tsv --counts …/counts.json --root …
GROUND entry=junk-borrowed.md section=1 bullets=1 tokens=3 grounded=2
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='4,137'             # was grounded=1, 2 findings
```

The edit removed one of `junk-borrowed`'s two kill reasons and still scored full marks. A
*top-level* change is caught — `printf '\n' >> junk-uncited.md` → `FIXTURES_CHANGED=junk-uncited.md`,
`C1=FAIL`, exit 1 — so the mechanism works; it just does not cover the evidence files. Still
open at `3807537` and in the uncommitted worktree counter (`8473abf6`), both of which keep the
same 8-key `PINNED`. One-line close for the executor (not applied): add both span files to
`PINNED`, or hash `sorted(fixture_dir.rglob('*'))`.

**C1-F2 — Medium at `d09fc8e7`; closed at `3807537` — reader-visible inference content that is
not a column-0 `- ` bullet is never checked.** `tools/inference-ground.py:92` (`if
line.startswith("- ")`) is the only bullet branch; the fence comment at `:81-87` justifies
counting fenced bullets because they "render to a reader". The same reasoning applies to
indented and `*` bullets and to a prose section, and none is enumerated:

```
(tool 819f83eb; manifests = the fixture dir, pristine)
prose-only section  → GROUND … section=1 bullets=0 tokens=0 grounded=0 / GROUND: PASS  EXIT=0
"  - uncited…"      → GROUND … section=1 bullets=0 tokens=0 grounded=0 / GROUND: PASS  EXIT=0
"* Therefore …"     → GROUND … section=1 bullets=0 tokens=0 grounded=0 / GROUND: PASS  EXIT=0
```

All three carry an ungrounded assertion and all three exit 0. No committed fixture covers this
form. At `3807537` the tool adds `INF_NO_BULLETS` and fails all three (`bullets=0 …
INF_NO_BULLETS`, exit 1), so this is not live at present HEAD.

**C1-F3 — Medium at `d09fc8e7` and at `3807537` — a filename-keyed stub scores full marks.**
A 4-line stub that exits 1 iff `basename` starts with `junk-` and 0 otherwise:

```
$ python3 corpus/evidence/round46/c1-count.py --root $TREE --tool namesstub.py
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS      EXIT=0
$ … --tool zero.py                       # content-blind constant 0, for contrast
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=0/3 / C1=FAIL      EXIT=1
```

The docstring's "cheapest gates that would score full marks" names only always-0 and
citation-presence-only; the basename oracle is cheaper than both and passes. At `3807537` the
counter is still `819287e2` (no canary), so the hole is open at the scored HEAD. The
**uncommitted** worktree counter (`8473abf6`) adds a `CANARY` leg and catches it
(`CANARY=fail`, `C1=FAIL`, exit 1); that byte state is not committed, so a verifier reading
`d09fc8e7` or `3807537` sees the hole. Observation, not a kill: `8473abf6` also prints a fifth
line, so its output no longer matches the frozen target line verbatim (`TOOL=present
POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS`); the extra leg only strengthens the verdict.

**C1-Obs — lane state moved mid-review; every verdict needs a pinned sha.** First read at
07:3x: `HEAD = d09fc8e7`, worktree clean for the scored files. By 07:39: `HEAD = 3807537`
("round-46: wave-2 corrections…", tool now `3018b1d2…`) **and** the worktree carried
uncommitted edits to `tools/inference-ground.py` (mtime 07:33:33) and
`corpus/evidence/round46/c1-count.py` (mtime 07:38:16, `8473abf6…`). `git status --porcelain`
at that point: ` M corpus/evidence/round46/c1-count.py` plus the same for the tool. Both HEAD
generations still score C1 `3/3 3/3 C1=PASS` exit 0 on their own trees, so the claim's verdict
is stable across the churn — but the tool's behaviour is not (F2 below/above).

**C1-pos — the tool is not vacuous on real corpus content, and `--registry` is load-bearing.**
Against the lane's real `corpus/evidence/round46/spans.tsv` + `corpus/SOURCES.md` (tool
`3018b1d2`, `--counts /dev/null`): `evidence-pool-versioning-r39.md` → `bullets=4 tokens=7
grounded=7 / GROUND: PASS` exit 0; the amendment → `bullets=4 tokens=5 grounded=5 / PASS`
exit 0. Drop `--registry` and r39 fails on `FINDING INF_TOKEN_NOT_IN_SPAN bullet=4 token='7089'`,
exit 1 — the document-number leg is the only thing grounding `RFC 7089` (`S079`), and no
committed counting command passes `--registry`.

## 4. Residual risk and verification gaps

- The counter is exit-code-only and says so; this seat did not re-report wave-1's
  `CritC1Attack` (presence ≠ inference) or `MutC1Junk`'s counts-global `N3`.
- My first mixed-marker probe (`- ` bullet + indented ungrounded bullet) initially passed
  `grounded=2`, but I had mutated the span from a concurrent command; re-run on pristine bytes
  it fails correctly (`bullets=1 tokens=2 grounded=1`, `INF_TOKEN_NOT_IN_SPAN`, exit 1), as
  does the `*` variant. No live mixed-marker hole at `3807537`.
- Corpus census: 7 of 59 `corpus/knowledge/*.md` carry a `#### Inference` section (all
  column-0 `- ` bullets, `non-bullet-lines=0`), so F2 does not bite the current corpus, and the
  tool is not a corpus-wide gate — no committed command runs it on entries without one.
- `--root` reporting is basename-only in the counter's invocation (wave-1 `ReviewerC1Tool` §5);
  the C1 output carries no per-fixture identity, so a mis-mapped fixture name could not be seen
  in the four printed lines.

## 5. Pointers

- counter `corpus/evidence/round46/c1-count.py:37-46` (`PINNED`), `:77-80` (enforcement),
  `:87-92` (legs) — sha256 `819287e2…c9e0a65` at `d09fc8e7` and at `3807537`;
  `8473abf6…c69e03a` uncommitted.
- tool `tools/inference-ground.py:81-92` (fence + `- ` enumeration) — `819f83eb…4275326bc`
  at `d09fc8e7`; `3018b1d2…223f07` at `3807537`/worktree (adds `INF_NO_BULLETS`, designators).
- `corpus/fixtures/inference-ground-r46/spans/S901-1.txt` `7c2aa321…` (pinned? no),
  `S902-1.txt` `c2184ca7…` (pinned? no) — both unchanged `c2f0e9d1`…`3807537`.
- `corpus/evidence/round46/claims.md` R46-C1 target/controls/kill rule (unchanged, not
  contested); `SKILL.md:116-117` Gates rows for the tool and the round-46 counters.
- `/tmp/chousa-r46w2-RevRerunC1/` removed at end of seat. No install performed.

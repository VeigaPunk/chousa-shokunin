# RevRerunC1 — re-run of R46-C1 on a clean archive of `d09fc8e7` (operability)

seat: `L1Chousa46.RevRerunC1` (reviewer, leaf; no dispatch, no network, no install). item: re-run C1 over
`git archive d09fc8e7…` in /tmp, paste output + exit, hash counter / tool / six fixtures, compare each
to `PINNED`, verdict re-derived | diverged. bounds: lane read-only, scratch only, only this file
written; frozen claims read first; no predicate, target or kill rule re-scaled.
## 1. Byte identities at the scored commit
```
$ git -C …/chousa-shokunin archive d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a | tar -x -C /tmp/…/fresh
819287e2075c3f5b57c4ceb26fb6b3d7594af48e03ad7cfcd61690727c9e0a65 c1-count.py · 819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc inference-ground.py
cba03251466e44773ef0ed9e080388b284f30f1ada0034e6b3c824d364ceb778 junk-borrowed.md · 7b3e6b6e36c771a336d7da17291d94861226af289b2a2c7d4a6ef7d68016e598 junk-uncited.md
ab32577d5266fbb07a04a63735e1f4f7432b06841a64fa3ff840b42c2f457fe4 junk-ungrounded.md · 1378296857c6193d80ce9649f5778216003f10ffdd645c0461fa43c2c46b8a21 positive-a.md
1d09c94bd4668fc31389a07354c312ca86b5e8dd0e644b84e3fe69e25a46ced4 positive-b.md · 4e61f56c8af38418754561096e7e22b8aa54e042bf0b86c4ad36542c7c6f417a positive-c.md
38a536bd9d33d0dc45d441cce6ce1882a1f4e60ee8ecdaebfd9f85a229d2aff4 spans.tsv · fd414d0a24883711dab8e27bd36e0aad00e6e09192d51b7bf75228e3f76fbb5c counts.json
7c2aa3214d9409886ca91fefa1ed69599c29ec521cd745affae86f93b762b1ef spans/S901-1.txt · c2184ca73ce45977b629591c786525bf8bf7899bc436f443af91feab396f20e4 spans/S902-1.txt
```

PINNED comparison by script (`ast`-parse `PINNED`, hash each target): `positive-a … junk-borrowed,
spans.tsv, counts.json` → `MATCH ×8`, `PINNED_MATCH_ALL=yes`. The tree holds **10** fixture files
(`git ls-tree -r d09fc8e7 corpus/fixtures/inference-ground-r46 | wc -l` → `10`); `PINNED` binds
**8**. The two unbound files are the span texts the tool grounds against, named by the pinned
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

Default-root form (`LANE = parents[3]`, i.e. the archived copy) prints the same four lines, exit 0;
verbatim match with the frozen target, no leg short. **Verdict: re-derived** — every declared figure
of R46-C1 reproduces from archived bytes alone (`--root` points at the archive; no working-tree file
read). The findings below are what the PASS does not cover, not a divergence in any declared number.
## 3. Findings
**C1-F1 — Medium — `PINNED` does not bind the span texts; the kill rule is half-enforced.**
`c1-count.py:37-46` lists 8 names, `:77-80` walks only `PINNED`. A post-freeze edit to the
grounding evidence is invisible whenever it moves no verdict:

```
$ printf '…frozen pool of pages; no revision is recorded per sentence, and every claim was
  independently re-verified against a live source\n' > …/spans/S901-1.txt
$ sha256sum …/spans/S901-1.txt
fbd444c698dd36e9ae91592e63585deda6b990d692a97bdc7fc8e6c9dd978770    # was 7c2aa321…
$ python3 corpus/evidence/round46/c1-count.py --root $PWD
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS   EXIT=0   # no FIXTURES_CHANGED
$ python3 tools/inference-ground.py --entry …/junk-borrowed.md --spans …/spans.tsv \
      --counts …/counts.json --root …
GROUND entry=junk-borrowed.md section=1 bullets=1 tokens=3 grounded=2
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='4,137'           # before: grounded=1, 2 findings
```

A top-level change *is* caught (`printf '\n' >> junk-uncited.md` → `FIXTURES_CHANGED=junk-uncited.md`,
`C1=FAIL`, exit 1), so the mechanism works and merely misses the evidence files. Reproduced at `3807537`
and at the newest HEAD `e50b388` (same 8-key `PINNED`; mutated span → `C1=PASS`, exit 0). Close: add
both span files to `PINNED`, or hash `sorted(fixture_dir.rglob('*'))`.

**C1-F2 — Medium at `d09fc8e7`; closed afterwards — reader-visible inference content that is not
a column-0 `- ` bullet is unchecked.** `tools/inference-ground.py:92` (`if line.startswith("- ")`)
is the only bullet branch, while `:81-87` argues a fenced line must be counted because it "renders
to a reader" — the same holds for indented and `*` bullets and a prose section, none enumerated
(tool `819f83eb`, pristine manifests):

```
prose-only section → GROUND … section=1 bullets=0 tokens=0 grounded=0 / GROUND: PASS  EXIT=0
"  - uncited…"     → GROUND … section=1 bullets=0 tokens=0 grounded=0 / GROUND: PASS  EXIT=0
"* Therefore …"    → GROUND … section=1 bullets=0 tokens=0 grounded=0 / GROUND: PASS  EXIT=0
```

Each carries an ungrounded assertion and exits 0; no committed fixture covers the form. At
`3807537`+ the tool adds `INF_NO_BULLETS` and fails all three (`bullets=0 … INF_NO_BULLETS`,
exit 1) — not live at present HEAD. A mixed-marker probe (`- ` bullet + indented ungrounded bullet)
first passed `grounded=2` only because a concurrent command of mine had mutated the span; pristine
it fails correctly (`bullets=1 tokens=2 grounded=1`, `INF_TOKEN_NOT_IN_SPAN`, exit 1), as does the
`*` variant — no live mixed-marker hole.

**C1-F3 — Medium at `d09fc8e7` and `3807537`; closed at `e50b388` — a filename-keyed stub scores
full marks.** Four lines exiting 1 iff `basename` starts with `junk-`, else 0:

```
$ python3 corpus/evidence/round46/c1-count.py --root $TREE --tool namesstub.py
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS   EXIT=0
$ … --tool zero.py        # content-blind constant 0, for contrast
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=0/3 / C1=FAIL   EXIT=1
```

The docstring's "cheapest gates that would score full marks" names only always-0 and
citation-presence-only; the basename oracle is cheaper than both and passed at the scored commit.
`e50b388` adds a `CANARY` leg that catches it (`CANARY=fail`, `C1=FAIL`, exit 1). Observation, not
a kill: that extra fifth output line no longer matches the frozen target line verbatim, and it only
strengthens the verdict.

**C1-Obs — the lane moved four times under this seat; pin the sha you score.** (a) first read
`HEAD = d09fc8e7`, scored files clean; (b) 07:39 `HEAD = 3807537` (tool `3018b1d2`, counter unchanged
`819287e2`); (c) worktree dirty: counter `8473abf6` (CANARY), tool `7736688b`, and both
`corpus/evidence/round46/controls/c1-*.txt` rewritten to the canary format; (d) `HEAD = e50b388`
"wave-2 fixes (… CANARY leg …)", which commits (c) — its counter prints `TOOL=present / POSITIVE_PASS=3/3
/ JUNK_KILLED=3/3 / CANARY=pass / C1=PASS`, exit 0. All four score the frozen predicate; the tool's
behaviour differs across them (F2, F3).

**C1-pos — the tool is not vacuous on real content, and `--registry` is load-bearing.** With the
lane's real `corpus/evidence/round46/spans.tsv` + `corpus/SOURCES.md`, `--counts /dev/null` (tool
`3018b1d2`): r39 entry → `bullets=4 tokens=7 grounded=7 / PASS` exit 0; the amendment →
`bullets=4 tokens=5 grounded=5 / PASS` exit 0. Drop `--registry`: r39 →
`FINDING INF_TOKEN_NOT_IN_SPAN bullet=4 token='7089'`, exit 1 — only the document-number leg
grounds `RFC 7089` (`S079`), and no committed counting command passes `--registry`.
## 4. Residual risk and verification gaps
- Counter is exit-code-only by declared design; wave-1 `CritC1Attack` (presence ≠ inference) and
  `MutC1Junk` `N3` (counts manifest is global, so a figure grounds any bullet, any source) are not
  re-reported — `junk-nospan`-style passes remain possible by design.
- Corpus census: 7 of 59 `corpus/knowledge/*.md` carry `#### Inference` (all column-0 `- ` bullets,
  `non-bullet-lines=0`), so F2 never bit the current corpus, and no committed command runs the tool
  on the 52 entries without the section — it is not a corpus-wide gate.
- `--root` reporting is basename-only in the counter's invocation; C1's output carries no
  per-fixture identity, so a mis-mapped fixture name would be invisible in the verdict.
## 5. Pointers
- `corpus/evidence/round46/c1-count.py:37-46` (`PINNED`), `:77-80` (enforcement), `:87-92` (legs) —
  `819287e2…c9e0a65` at `d09fc8e7` and `3807537`; `8473abf6…c69e03a` from `e50b388`.
- `tools/inference-ground.py:81-92` (fence + `- ` enumeration) — `819f83eb…4275326bc` at
  `d09fc8e7`; `3018b1d2…223f07` at `3807537`; `7736688b…2eca` from `e50b388`.
- `corpus/evidence/round46/spans/S901-1.txt` (unpinned, `7c2aa321…`), `S902-1.txt` (unpinned,
  `c2184ca7…`) — identical at `c2f0e9d1`, `d09fc8e7`, `3807537`, `e50b388`.
- `corpus/evidence/round46/claims.md` R46-C1 (target/controls/kill rule uncontested);
  `SKILL.md:116-117` Gates rows. Scratch `/tmp/chousa-r46w2-RevRerunC1/` removed; no install.

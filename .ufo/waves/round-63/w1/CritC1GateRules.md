# Round 63 · w1 · CritC1GateRules (critic) — false positives of the lane-preflight gate rules

Scope: attack the rule of each gate of `corpus/evidence/round63/controls/pos-ref-preflight.py` on real files that
are not this lane's. Read-only. Lane writes: this report only. Scratch used and removed:
`/fast/scratch/hyaku/chousa-r63/CritC1GateRules/`. No installs, no git mutation, no network.

## Findings

1. **Two gates produce false positives on real sibling files: G04 and G05.** Each FAILs on a token that is not a
   path (G04) or on a legitimate citation shape (G05) whose target exists.
   - G04 `caught=18/18` (kagi-shokunin, `SHONEN.md:12`): a ratio in a verdict span, not a path. The `/` makes it
     path-shaped.
   - G05 `.ufo/waves/round-23/{live/,measure-c2-after-v2.json,evaluability.json}` (kake-shokunin,
     `SCORECARD.md`, a capability row): brace shorthand. All three members exist on disk (checked individually).
2. **The shapes that trigger them are wider than the sibling sample.** On a scratch fixture with the same rule code
   (`--only G04,G05`), every cited shape below fails although the file exists or the token is not a path. Control
   `corpus/a/x.json` passes.
3. **G02, G03 and G01 found no false positive on the three real roots.** Their FAILs are true per the lane convention
   (details below). G03 has a scope problem (no grandfather clause), which is a calibration issue, not a false positive.
4. **Copy-scope artifacts are not rule false positives, but they are a trap.** Copying only `corpus/`, `SHONEN.md`,
   `SCORECARD.md` made G01 and G05 FAIL on paths that exist in the real lane (they live in `scripts/`, `tools/`, `.ufo/`).
   G01 and G05 resolve against ROOT. The battery's whole-lane golden is not affected; a corpus-only copy is invalid
   input for those two gates.

## Method

Three sibling lanes: kagi-shokunin, kake-shokunin, tameshi-shokunin (all have `corpus/`, `SHONEN.md`, `SCORECARD.md`).

- (a) Copy-run, as the item specifies: `cp -a` of the three files/dirs into scratch copies, then
  `python3 -B pos-ref-preflight.py --root <copy> --fleet /home/vgpnk/Projects/shokunin --skip G06,G07,G08 --work <scratch>`.
- (b) Authoritative run, the same command on the real sibling roots (read-only; the tool writes only to `--work`):
  `python3 -B pos-ref-preflight.py --root /home/vgpnk/Projects/shokunin/<lane> --fleet /home/vgpnk/Projects/shokunin --skip G06,G07,G08 --work <scratch>/real-<lane>`.
- (c) A detail script (scratch) that imports the reference module and lists every miss with its span, plus
  the census validate command run directly on each real `corpus/SOURCES.md`.
- (d) A fixture (scratch) with one shape per row, run with `--only G04,G05`.

Gates G06, G07, G08 were skipped per the item; they are not judged here.

## Real-root results (authoritative, run (b))

```
kagi-shokunin   G01 PASS  G02 PASS  G03 FAIL 17 without ## Gate  G04 FAIL 1 unresolved: caught=18/18  G05 PASS 7 capability pointers resolve
                PREFLIGHT=3/5 FAILED=G03,G04 ENV=none SKIPPED=G06,G07,G08   exit=1
kake-shokunin   G01 PASS  G02 PASS  G03 PASS 57  G04 PASS 0 pointers resolve  G05 FAIL 1 unresolved: .ufo/waves/round-23/{live/,measure-c2-after-v2.json,evaluability.json}
                PREFLIGHT=4/5 FAILED=G05 ENV=none SKIPPED=G06,G07,G08   exit=1
tameshi-shokunin G01 PASS G02 FAIL 2 not named: r44-anchor-refresh-rule.md,scratch-root-contract.md  G03 FAIL 1: round-57.md  G04 PASS 0 pointers  G05 PASS 18
                PREFLIGHT=3/5 FAILED=G02,G03 ENV=none SKIPPED=G06,G07,G08   exit=1
```

Direct census check on the real registries (`bash scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md`):
exit 0 for all three, only W04 warnings printed. This matches G01 PASS on each real root.

## Copy-run results (run (a)) and why they are not rule false positives

- kagi copy: G03, G04 as above; G05 `.ufo/waves/round-25/observe-1.json` (the copy has no `.ufo/`; real file exists).
- kake copy: G01 `S088 missing used-by scripts/source_recheck.py` (real file exists, 26757 bytes); G05 31 unresolved
  (`.ufo/` absent from copy). Real-root G01 and G05 pass except the brace token above.
- tameshi copy: G01 `S097 missing used-by tools/tally-audit.py` (real file exists); G05 16 unresolved (`tools/`,
  `.ufo/` absent from copy). G02, G03 as above.

Count of copy-only artifacts: G01 2 items, G05 48 items (1 + 31 + 16). None is counted in the rate below.

## Per-gate judgement (real-root FAIL items, one item = one failing token or file)

| Gate | Items | True defect of the lane | False positive of the rule | Note |
|---|---|---|---|---|
| G01 census | 0 | — | 0 | PASS on all three real roots. The PASS detail string `census_findings=0` is hard-coded, not computed from the census output (see calibration). |
| G02 knowledge-index | 2 | 2 | 0 | `r44-anchor-refresh-rule.md`, `scratch-root-contract.md` exist in `tameshi-shokunin/corpus/knowledge/`; `grep -c` for each name in `corpus/README.md` returns 0. Prose mentions of "scratch" exist, the file names do not. |
| G03 lesson-gate | 18 | 18 | 0 | kagi: 17 `round-N.md` (rounds 1–18, no round-2 file) with no `## Gate`. CORPUS.md line 19 requires `## Gate` in each `lessons/round-<N>.md`; these pre-date the convention. tameshi: `round-57.md` (one `##` heading, no Gate). Not false positives, but kagi's 17 are a legacy-scope issue (see calibration). |
| G04 shonen-pointers | 1 | 0 | **1** | kagi `SHONEN.md:12`: `` `SCOPE_FALSIFY: PASS (caught=18/18 failed=0)` `` → token `caught=18/18` tested as a path. |
| G05 scorecard-paths | 1 | 0 | **1** | kake `SCORECARD.md`: `` `.ufo/waves/round-23/{live/,measure-c2-after-v2.json,evaluability.json}` `` → brace shorthand tested as one path. Members exist: `live/`, `measure-c2-after-v2.json`, `evaluability.json` (checked with `test -e`). |

**Rate: 2 false positives out of 22 real-root FAIL items** (G02 2 + G03 18 + G04 1 + G05 1 = 22; G01 0).
Per gate: G01 0/0, G02 0/2, G03 0/18, G04 1/1, G05 1/1.

## Shape probes (fixture, run (d))

Fixture: `SHONEN.md` with `` `and/or` ``, `` `github.com/owner/repo` ``, `` `caught=18/18 failed=0` ``, `` `tools/x.py` ``;
`SCORECARD.md` capability rows with `` `tools/x.py:12` ``, `` `corpus/knowledge/x.md.` ``, `` `corpus/a/{x,y}.json` ``,
`` `corpus/a/x.json` `` (control). Command:
`python3 -B pos-ref-preflight.py --root <fixture> --fleet /home/vgpnk/Projects/shokunin --only G04,G05 --work <w>`
Observed:

```
GATE G04 shonen-pointers FAIL 3 unresolved: and/or,github.com/owner/repo,caught=18/18
GATE G05 scorecard-paths FAIL 3 unresolved: tools/x.py:12,corpus/knowledge/x.md.,corpus/a/{x,y}.json
PREFLIGHT=0/2 FAILED=G04,G05 ENV=none SKIPPED=G01,G02,G03,G06,G07,G08
```

- G04: `and/or`, `github.com/owner/repo`, `caught=18/18` are all false positives (none is a path on disk). The `tools/x.py`
  pointer and the `tools/x.py` file pass. Direct `path_words` probes also return `1/2`, `a/b`, `N/A`, `TCP/IP`,
  `www.rfc-editor.org/rfc/rfc9110.html` as pointers; `https://…` is correctly excluded.
- G05: `tools/x.py:12` (the file exists; G04 strips `:N`, G05 does not), `corpus/knowledge/x.md.` (the file exists; the
  trailing `.` is not stripped), `corpus/a/{x,y}.json` (both members exist) are all false positives. The control passes.
- Not tested by a fixture, by reading (INFERENCE): a token `corpus/a/x.md)` inside a SCORECARD cell is not stripped of `)`,
  so it fails the same way. The G05 regex `[^\s*<>]+` admits `{`, `}`, `,`, so the brace case is the same class.

## Rule change each false positive needs

- **G04 (`caught=18/18`, `and/or`, `github.com/owner/repo`):** accept a pointer only when its first segment is a
  top-level name present under ROOT (`corpus`, `tools`, `.ufo`, `scripts`, or a root file) or the token is a bare file
  with a PATHWORD extension and contains no `=`. Reject tokens containing `=`, `(`, `)`, or a first segment that looks
  like a host (`x.y` with a TLD) and no known top-level name. Keep the existing `:N` stripping.
- **G05 (`:12`, trailing `.`, `{a,b}`):** before the exists check, strip a trailing `:N` or `:N-M` (as G04 does), strip
  a trailing `.`, `)`; expand `{a,b,...}` into its members and check each member; a `{…/}` member with a trailing slash
  is a directory. Keep the `*`, `<`, `>` exclusions.

## Calibration notes (not false positives)

- G03 has no legacy scope. 17 of kagi's 40 `round-N.md` lessons pre-date the `## Gate` convention; the rule fails them
  all. Fix options: a `corpus/` marker of the first round the convention applies to, or check only the rounds named in
  the registry. This changes the rule's scope, so it is a frozen-rule decision for the L1, not a fix in the tool.
- G04 PASSes vacuously on kake and tameshi (0 backtick spans in their `SHONEN.md`; `path_words` yields 0). A gate that
  checks nothing passes; a minimum-count line would make the vacuity visible. Not a false positive.
- G01's PASS detail `census_findings=0` is a literal string; it is not the census finding count. The census itself
  printed W04 warnings on all three real roots (`S033 duplicate url …`), which the gate does not count (correctly,
  under its rule: only E-lines fail).
- G02 is a substring match on the whole README. A name occurring inside a longer name or in prose passes. This is
  a false negative direction. Not exercised; INFERENCE from the code line `miss = [f for f in files if f not in readme]`.
- G01 and G05 read paths outside `corpus/`. A lane copy that omits `tools/`, `scripts/`, `.ufo/` fails them
  (observed, run (a)). The battery copies the whole lane, so this does not affect its numbers; it does mean the tool is
  only valid on a whole-lane root.

## Verdict inputs

- Commands run: copy-run ×3 (run (a)); real-root run ×3 (run (b)); direct census validate ×3; detail script over
  the three real roots; fixture run (d) with `--only G04,G05`; `test -e` on the brace members; `grep -c` on the README
  for the two tameshi names (0 each); `path_words` probes.
- Sibling files touched by my commands: none (the tool writes only to `--work`; the census validate branch writes
  only to stdout). `find` on the three real roots for the last 20 minutes showed tameshi `.git/objects/*` entries that I did
  not produce (no git command ran from this seat); I did not investigate further.
- Installs or updates: none.

VERDICT: FALSE_POSITIVE_GATES=G04,G05 rate=2/22

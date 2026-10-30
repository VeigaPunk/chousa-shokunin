# Draft05 — E12/E13 identity mismatch, red-before, supplement-only repair

## Behavior and axes

Axes: fixture identity correctness, frozen-evidence integrity, and provenance clarity. This is a read-only evidence-mining seat, not an implementation or closure verdict. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

**Finding:** the frozen E12/E13 positive fixtures generate the file identity and README identity independently. The inherited supplement shares one generated identity within each fixture. Preserve the frozen failure; a supplemental pass cannot satisfy C1's frozen kill rule.

## Evidence and provenance

- `corpus/evidence/round64/claims.md:36-44,53-59,67-92` freezes benign E12/E13, the normalization/mirror contract, the baseline failure, and the unmodified-battery three-run kill rule.
- `corpus/evidence/round64/c1-battery-v3.py:201-202,386-394,442-443` defines a fresh random `tag()` on each call; E12 creates `escaped_q{tag()}.md` and separately indexes `escaped\\_q{tag()}.md`; E13 creates `gate notes q{tag()}.md` and separately indexes `gate%20notes%20q{tag()}.md`. Both expect exit 0 with no failed gates.
- `corpus/evidence/round64/controls/c1v3-before-full.txt:38-44` is the inherited observed red-before, not a run performed by this seat:

```text
LEG E12 benign FAIL rc=1 want 0
LEG E13 benign FAIL rc=1 want 0
LEG E14 benign FAIL rc=1 want 0
LEG Z01 zero ok ok
LEG Z02 zero ok ok
LEG Z03 zero ok ok
CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL
```

The full receipt's exit 1 is recorded by `claims.md:67-69`; the receipt itself has no shell exit trailer. The legs-only inherited `controls/before-e.txt:12-15` likewise reports E12/E13 failure but ends `BATTERY=PARTIAL`; it must not be described as an independent full-battery failure or fresh seat execution.

- `corpus/evidence/round64/c1-battery-supplement.py:386-396` binds `t = tag()` once per fixture and uses `{t}` in both identities. No frozen file was repaired. A local comparison shows these are the only differences between the two instrument files.
- `corpus/evidence/round64/claims-erratum.md:3-6` explicitly calls the original benign assertion false and preserves the repair as a separate inherited post-freeze supplement.
- `corpus/lessons/round-64.md:23-25` already records the mistake: “Positive fixtures draw identity twice”; captured-by is “QUALITY 115 and 119 should have required a conforming positive before freeze; missed in attempt1”. This is inherited attribution, not a quality-gate execution by Draft05.

### Causal interpretation

[INFERENCE] When the two tags differ, unescaping E12 or unquoting E13 leaves a README target different from the actual filename. Normalization cannot repair unrelated random identities. The fixture therefore introduces an unindexed file and phantom row while expecting a clean verdict. A conforming G02 checker should reject that malformed fixture, rather than being weakened to admit it. Independent 32-bit draws can coincide; the source defect is independent identity generation, not a mathematical proof that every possible seed fails.

The inherited red-before does not isolate how much of its failure comes from old-tool normalization versus fixture mismatch. Source comparison establishes the mismatch and repair mechanism; this seat does not promote that into a measured supplement pass or claim that the candidate is fully conforming.

## Exact local commands, outcomes, exits

All commands used cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`. File inspections used the read/grep/glob tools; no Python or other execution runtime was invoked, and no battery was rerun.

1. `diff -u /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/c1-battery-v3.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/c1-battery-supplement.py` — exit **1**, expected differences. Complete changed hunk:

```diff
@@ -384,14 +384,16 @@
         _entry(root, nm)
 
     def e12(root):  # D6 benign: a markdown-escaped underscore is a valid index row
-        nm = f"escaped_q{tag()}.md"
+        t = tag()
+        nm = f"escaped_q{t}.md"
         _entry(root, nm)
-        _readme_add(root, f"\n- `knowledge/escaped\\_q{tag()}.md` (fixture)\n")
+        _readme_add(root, f"\n- `knowledge/escaped\\_q{t}.md` (fixture)\n")
 
     def e13(root):  # D7 benign: a percent-encoded link target is a valid index row
-        nm = f"gate notes q{tag()}.md"
+        t = tag()
+        nm = f"gate notes q{t}.md"
         _entry(root, nm)
-        _readme_add(root, f"\n- [fixture](knowledge/gate%20notes%20q{tag()}.md)\n")
+        _readme_add(root, f"\n- [fixture](knowledge/gate%20notes%20q{t}.md)\n")
 
     def e14(root):  # D8 benign: an NFC file name indexed by its NFD spelling
         nm = "caf\xe9-%s.md" % tag()
```

2. `git diff bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/claims.md corpus/evidence/round64/c1-battery-v3.py` — exit **0**, empty output. Those inspected working-tree paths match that ref; this is not an all-files integrity audit. Read-only Git, no mutation.
3. `diff --version` — exit **0**, stdout `diff diff (pi-uu-diff) 0.8.0`.
4. `test ! -e /fast/scratch/hyaku/chousa-r64/Draft05` — exit **0**, no output. No scratch tree or clone was created, so none remains to delete.

Tools installed/updated: none. Existing comparison tool: pi-uu-diff 0.8.0, existing environment channel; reason: compare frozen and supplemental source without running either. No pacman transaction, PATH write, network fetch, service restart, or Git/JJ mutation occurred.

## Gates and limits

- Frozen C1 remains **failed/not established**, as its inherited red-before records and erratum acknowledges. No supplemental result overrides it; only L1 integrates production and the canonical judge decides closure.
- Supplement repair is source-observed, **not execution-validated by this seat**. `controls/ref-preflight-v3.py` remains a candidate, not production; no production-readiness claim is made.
- No new test, benchmark, selftest, null, full preflight, or battery outcome is claimed. No other C1 legs or C2/C3 verdicts are adjudicated here.
- Advisory mistake mining is not outside non-author closure. The missed pre-freeze positive-fixture check is the prevention lesson; it is not permission to edit frozen bytes or narrow the kill rule.

## Touched surfaces, scope conflict, artifacts

Only seat report artifacts are written: `.ufo/waves/round-64/w1/Draft05/report.md` and the explicitly named trailer `.ufo/waves/round-64/w1/Draft05.md` pointing here. Product, instruments, operator inputs, frozen claims/counters, and sibling files are untouched.

Path instructions conflict verbatim: “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft05/ (report.md)” versus “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft05.md”. The report is beneath the requested folder; the later explicitly named trailer receives only a pointer. The conflict is retained for canonical adjudication, not used to change the assignment.

Self-evaluation: accuracy 4/5 (no fresh behavior execution; provenance labels distinguish it); completeness 4/5 (source repair established, supplemental success intentionally not asserted); clarity 4/5 (two path conventions require a pointer); actionability 4/5 (L1 must retain frozen stop and keep supplement distinct); conciseness 4/5 (full command/diff audit costs space). Mean 4.0/5. Highest-impact improvement belongs to authorized integration evidence: attach separately labeled frozen-versus-supplement executions without replacing the frozen verdict. User agreement is not presumed.

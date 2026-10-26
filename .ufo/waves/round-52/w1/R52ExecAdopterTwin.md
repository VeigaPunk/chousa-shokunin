# R52ExecAdopterTwin — round-52 w1: routed defect 2 (twin-id `held` label, refusal ordering)

Lane tool at `13bc280`; `sha256(tools/assimilate-rows.py)=10af959b2b87dad565717b84e68733caab6cb7a940d68fb1c52fca793d4c86f4`.
Scratch `/fast/scratch/hyaku/chousa-r52/R52ExecAdopterTwin/` (`TMPDIR` set to it, removed at the end): `tool.py` = the
lane file byte-identical, `harness-only/tool.py` = new harness + old behaviour, `patched/tool.py` = the patch. No tool
installed; nothing written outside this report and that scratch.

## 1. Both defects reproduce at the lane tip (`sh before-after.sh`, same packages, lane tool then patched copy)

```
### tool=…/tool.py
-- F5: two staged rows, one URL; the second's recheck is 2026-02-30 — re-verify
COLLISIONS=0
CITED=2 APPEND=1 HELD=1                  # HELD=1 for a same-run twin, no refusal
BODYONLY=0
-- F5 renumber.tsv
S101	S002	append	twin.test/shared
S102	S002	held	twin.test/shared        # `held` though the Registry carries no such URL
-- F6 with entries: stderr
REFUSED entry missing: corpus/knowledge/absent.md
REFUSED registry has no `## Registry` heading
REFUSED registry rows outside the Registry section: S001
-- F6 no --entry
COLLISIONS=0
   rc=0                                  # a registry the tool cannot continue from, accepted
### tool=…/patched/tool.py
-- F5
COLLISIONS=0
REFUSED S102: recheck '2026-02-30 — re-verify' has no leading valid date or NNd
-- F5 renumber.tsv
(none)
-- F6 with entries: stderr
REFUSED registry has no `## Registry` heading
REFUSED registry rows outside the Registry section: S001
REFUSED entry missing: corpus/knowledge/absent.md
-- F6 no --entry
COLLISIONS=0
REFUSED registry has no `## Registry` heading
REFUSED registry rows outside the Registry section: S001
   rc=1
```
The recheck half needs a value that is really invalid. `INVALID_RECHECK` (the round-51 review's repro value) is a
*valid* symbolic cadence under `RECHECK_RE = ^(\d{4}-\d{2}-\d{2}|\d+d|[A-Za-z][A-Za-z0-9 _-]*)$`; re-measured:
`'INVALID_RECHECK' RECHECK True LEAD False · '2026-02-30 — re-verify after release' RECHECK False LEAD True ·
'3 months' RECHECK False LEAD False`. A calendar-invalid date is the branch the refusal text names, and it is
swallowed by the same `if action != "append": continue`.

## 2. What the patch changes

- `mapping[sid] = (by_url[u], "twin")`: `held` only for a URL the Registry carries; a second staged row for a URL this
  run minted is `twin`; stdout `CITED=… APPEND=… HELD=<registry rows> TWIN=<twins>` (`grep -rn HELD= corpus tools`
  finds no parser of the old `len(cited)-len(rows)`).
- the recheck is validated for every cited row in a pre-pass before any row is built (held/twin included);
  `stripped.tsv` still records the substituted cell, now on `cells[9] != recheck_ok[sid]`.
- `registry_problems` is computed once, before the no-`--entry` return (refuses there too), and `refused =
  list(reg_bad)` puts the registry lines first in the entry path.
- selftest: `expected.json` may add `cases` (`fixtures`, `findings`, optional `entry`, `[]` = no `--entry`); the
  multiset comparison is unchanged, and `REFUSED` lines are additionally compared in order (`DIFF order`) — a
  refusal's order is what the operator reads. The round-50 pinned package has no `REFUSED` line, so that rule is inert
  there.

## 3. Unified diff (lane path `tools/assimilate-rows.py`, `diff -U0`; applies with `patch -p1`)

```diff
--- a/tools/assimilate-rows.py
+++ b/tools/assimilate-rows.py
@@ -28 +28,4 @@
-  already carries maps to that row's id (`held`, nothing appended); any other
+  already carries maps to that row's id (`held`, nothing appended); a second
+  staged row for a URL this run already minted maps to that same id and is labelled
+  `twin` (nothing appended either — `held` is reserved for the row the Registry
+  already carries); any other
@@ -30 +33,2 @@
-  (`append`). Ids are never shifted by arithmetic.
+  (`append`). Ids are never shifted by arithmetic, and the stdout tail counts the
+  two apart: `HELD=<registry rows> TWIN=<twins>`.
@@ -56,3 +60,6 @@
-would continue from are not the registry's); an entry missing or not UTF-8; a cited
-staged row with no URL; a staged row whose recheck has no leading
-calendar-valid date, `NNd` or cadence. Headings accept a space or a tab after
+would continue from are not the registry's) — checked and printed FIRST, before any
+entry is read, and also without `--entry` (omitting the entries is not a way past a
+broken registry); an entry missing or not UTF-8; a cited staged row with no URL;
+any cited staged row whose recheck has no leading calendar-valid date, `NNd` or
+cadence — `held` and `twin` rows included, because their recheck is still a claim
+about the source even though they carry no row of their own. Headings accept a space or a tab after
@@ -72 +79,6 @@
-`STRIPPED lane column`. `--selftest` also takes `--cites source|all` (default
+`STRIPPED lane column`. The expected file may add `cases`: a list of the shape
+`{"fixtures": <package dir under the fixture root, with its own staged.md,
+registry.md and knowledge/>, "findings": [<that package's expected lines>],
+"entry": [<entry paths to pass; an empty list runs with no --entry>]}` — each case
+is run after the root package and the digest covers every file under the root,
+cases included. `--selftest` also takes `--cites source|all` (default
@@ -83 +95,3 @@
-(a duplicated finding is a difference); `--selftest` with any other option exits 2; a finding line
+(a duplicated finding is a difference), except the `REFUSED` lines, which are also compared in
+order (`DIFF order <observed> (want <expected>)`): a refusal's order is what the operator reads;
+`--selftest` with any other option exits 2; a finding line
@@ -89 +103,2 @@
-map to one lane id (the appended row's `used-by` names the entries citing ANY of them, and keeps the
+map to one lane id (`append` for the first, `twin` for each later one; the appended
+row's `used-by` names the entries citing ANY of them, and keeps the
@@ -238,2 +253,5 @@
-def observe(fix: pathlib.Path, cites: str = "source") -> list[str]:
-    """Run this tool on fixture package `fix`; return its finding lines."""
+def observe(fix: pathlib.Path, cites: str = "source", entries: list[str] | None = None) -> list[str]:
+    """Run this tool on fixture package `fix`; return its finding lines.
+
+    `entries` overrides the default (every `.md` under `knowledge/`); an empty list runs the child
+    with no `--entry` at all, which is a package the tool is asked to refuse."""
@@ -241 +259,2 @@
-    entries = sorted(p.relative_to(know).as_posix() for p in know.rglob("*.md")) if know.is_dir() else []
+    if entries is None:
+        entries = sorted(p.relative_to(know).as_posix() for p in know.rglob("*.md")) if know.is_dir() else []
@@ -310 +329,2 @@
-        want = json.loads(exp.read_text(encoding="utf-8"))["findings"]
+        doc = json.loads(exp.read_text(encoding="utf-8"))
+        want = doc["findings"]
@@ -312,0 +333,12 @@
+        cases: list[tuple[str, pathlib.Path, list[str] | None, list[str]]] = [("", fix, None, want)]
+        for c in doc.get("cases", []):
+            if not (isinstance(c, dict) and isinstance(c.get("fixtures"), str)
+                    and isinstance(c.get("findings"), list) and all(isinstance(w, str) for w in c["findings"])):
+                raise ValueError("each case needs `fixtures` (string) and `findings` (list of strings)")
+            ent = c.get("entry")
+            if ent is not None and (not isinstance(ent, list) or not all(isinstance(x, str) for x in ent)):
+                raise ValueError(f"case {c['fixtures']}: `entry` must be a list of entry paths")
+            d = fix / c["fixtures"]
+            if not (d / "staged.md").is_file() or not (d / "registry.md").is_file() or not (d / "knowledge").is_dir():
+                raise ValueError(f"case fixtures {d}: staged.md, registry.md or knowledge missing")
+            cases.append((c["fixtures"], d, ent, c["findings"]))
@@ -316,9 +348,23 @@
-    got = observe(fix, cites)
-    for g in got:
-        print(f"FINDING {g}")
-    cw, cg = collections.Counter(want), collections.Counter(got)
-    miss, extra = sorted((cw - cg).elements()), sorted((cg - cw).elements())
-    for m in miss:
-        print(f"DIFF missing {m}")
-    for x in extra:
-        print(f"DIFF unexpected {x}")
+    ok, n_got, n_want = True, 0, 0
+    for label, d, ent, want_c in cases:
+        got = observe(d, cites, ent)
+        for g in got:
+            print(f"FINDING {g}")
+        cw, cg = collections.Counter(want_c), collections.Counter(got)
+        miss, extra = sorted((cw - cg).elements()), sorted((cg - cw).elements())
+        for m in miss:
+            print(f"DIFF missing {m}")
+        for x in extra:
+            print(f"DIFF unexpected {x}")
+        # a refusal is judged by the order it is printed in as well as by its presence
+        ro = [g for g in got if g.startswith("REFUSED ")]
+        rw = [w for w in want_c if w.startswith("REFUSED ")]
+        if ro != rw:
+            ok = False
+            for i in range(max(len(ro), len(rw))):
+                o, w = (ro[i] if i < len(ro) else "-"), (rw[i] if i < len(rw) else "-")
+                if o != w:
+                    print(f"DIFF order {label + ': ' if label else ''}{o} (want {w})")
+        n_got += len(got)
+        n_want += len(want_c)
+        ok = ok and not miss and not extra
@@ -326,2 +372 @@
-    ok = not miss and not extra
-    print(f"SELFTEST={'PASS' if ok else 'FAIL'} findings={len(got)} expected={len(want)}")
+    print(f"SELFTEST={'PASS' if ok else 'FAIL'} findings={n_got} expected={n_want}")
@@ -378,0 +424 @@
+    reg_bad = registry_problems(reg_text)      # the ids this run would continue from
@@ -379,0 +426,5 @@
+        if reg_bad:
+            # a registry whose ids cannot be continued from is refused with or without an --entry
+            for r in reg_bad:
+                print(f"REFUSED {r}", file=sys.stderr)
+            return 1
@@ -389 +440 @@
-    refused: list[str] = []
+    refused: list[str] = list(reg_bad)         # the registry precondition is reported first
@@ -399 +449,0 @@
-    refused += [f"{p}" for p in registry_problems(reg_text)]
@@ -438 +488 @@
-            mapping[sid] = (by_url[u], "held")
+            mapping[sid] = (by_url[u], "twin")
@@ -451,0 +502,19 @@
+    # a cited row's recheck is a claim about its source whether or not the row appends (a `held` or `twin`
+    # row carries no row of its own), so every cited recheck is validated before any row is built
+    recheck_ok: dict[str, str] = {}
+    late: list[str] = []
+    for sid in cited:
+        recheck = subst(staged[sid][9])
+        if RECHECK_RE.match(recheck) and (not DATE_RE.match(recheck) or valid_date(recheck)):
+            recheck_ok[sid] = recheck
+            continue
+        m = LEAD_RE.match(recheck)
+        if not m or (DATE_RE.match(m.group(1)) and not valid_date(m.group(1))):
+            late.append(f"{sid}: recheck {recheck[:60]!r} has no leading valid date or NNd")
+        else:
+            recheck_ok[sid] = m.group(1)
+    if late:
+        for r in late:
+            print(f"REFUSED {r}", file=sys.stderr)
+        return 1
+
@@ -467,8 +536,4 @@
-        recheck = cells[9]
-        if not (RECHECK_RE.match(recheck) and (not DATE_RE.match(recheck) or valid_date(recheck))):
-            m = LEAD_RE.match(recheck)
-            if not m or (DATE_RE.match(m.group(1)) and not valid_date(m.group(1))):
-                print(f"REFUSED {sid}: recheck {recheck[:60]!r} has no leading valid date or NNd", file=sys.stderr)
-                return 1
-            stripped.append((lid, "recheck", recheck))
-            cells[9] = m.group(1)
+        recheck = recheck_ok[sid]
+        if cells[9] != recheck:
+            stripped.append((lid, "recheck", cells[9]))
+            cells[9] = recheck
@@ -507 +572,3 @@
-    print(f"CITED={len(cited)} APPEND={len(rows)} HELD={len(cited) - len(rows)}")
+    held_n = sum(1 for v in mapping.values() if v[1] == "held")
+    twin_n = sum(1 for v in mapping.values() if v[1] == "twin")
+    print(f"CITED={len(cited)} APPEND={len(rows)} HELD={held_n} TWIN={twin_n}")
```

## 4. Fixtures — one row per defect

Default package `corpus/fixtures/assimilate-selftest/` (twin label, additive; nothing else in it moves):

```diff
--- a/corpus/fixtures/assimilate-selftest/staged.md
+++ b/corpus/fixtures/assimilate-selftest/staged.md
@@ -11,0 +12 @@
+| S017 | New doc A, staged twice — https://example.test/new-a | docs | A | scope a | section a | the same document as S010, a second staged row for one URL | mined | 2026-10-25 | 90d | corpus/knowledge/a.md |
--- a/corpus/fixtures/assimilate-selftest/knowledge/corpus/knowledge/a.md
+++ b/corpus/fixtures/assimilate-selftest/knowledge/corpus/knowledge/a.md
@@ -1,0 +2 @@
+source: S017 — https://example.test/new-a — section a
--- a/corpus/fixtures/assimilate-selftest/expected.json
+++ b/corpus/fixtures/assimilate-selftest/expected.json
@@ -8,0 +9 @@
+ "MAP S017->S021 twin",
@@ -28,0 +30,25 @@
+],
+"cases": [
+ {"fixtures": "cases/twin-recheck",
+  "findings": [
+   "TOOLEXIT 1",
+   "COLLISIONS -",
+   "REFUSED S102: recheck '2026-02-30 — re-verify after release' has no leading valid date or NNd"
+  ]},
+ {"fixtures": "cases/refusal-order",
+  "entry": ["corpus/knowledge/absent.md", "corpus/knowledge/a.md"],
+  "findings": [
+   "TOOLEXIT 1",
+   "COLLISIONS -",
+   "REFUSED registry has no `## Registry` heading",
+   "REFUSED registry rows outside the Registry section: S001",
+   "REFUSED entry missing: corpus/knowledge/absent.md"
+  ]},
+ {"fixtures": "cases/refusal-order",
+  "entry": [],
+  "findings": [
+   "TOOLEXIT 1",
+   "COLLISIONS -",
+   "REFUSED registry has no `## Registry` heading",
+   "REFUSED registry rows outside the Registry section: S001"
+  ]}
```

Two case packages, whole files (`# <lane path>` then the bytes; six files):

```
# corpus/fixtures/assimilate-selftest/cases/twin-recheck/registry.md
## Registry

| S001 | Lane doc — https://twin.test/lane-1 | docs | A | lane | section 1 | lane row | mined | 2026-01-01 | 90d | — |
# corpus/fixtures/assimilate-selftest/cases/twin-recheck/staged.md
| S101 | Shared doc — https://twin.test/shared | docs | A | shared | section a | first row | mined | 2026-10-25 | 90d | — |
| S102 | Shared doc, staged twice — https://twin.test/shared | docs | A | shared | section b | twin row, calendar-invalid recheck | mined | 2026-10-25 | 2026-02-30 — re-verify after release | — |
# corpus/fixtures/assimilate-selftest/cases/twin-recheck/knowledge/corpus/knowledge/a.md
source: S101 — https://twin.test/shared — section a
source: S102 — https://twin.test/shared — section b
# corpus/fixtures/assimilate-selftest/cases/refusal-order/registry.md
## Rows below

| S001 | Lane doc — https://order.test/lane-1 | docs | A | lane | section 1 | row outside any Registry section | mined | 2026-01-01 | 90d | — |
# corpus/fixtures/assimilate-selftest/cases/refusal-order/staged.md
| S101 | New doc — https://order.test/new | docs | A | new | section a | row a sound registry would append | mined | 2026-10-25 | 90d | — |
# corpus/fixtures/assimilate-selftest/cases/refusal-order/knowledge/corpus/knowledge/a.md
source: S101 — https://order.test/new — section a
```

## 5. Red-before, green-after, pinned run, frozen round-51 counter

```
$ python3 tool.py --selftest --fixtures fixtures                 # lane tool: `cases` unread
DIFF missing MAP S017->S021 twin · DIFF unexpected MAP S017->S021 held
SELFTEST=FAIL findings=28 expected=28                            # rc=1
$ python3 harness-only/tool.py --selftest --fixtures fixtures    # new harness, old behaviour
DIFF missing MAP S017->S021 twin · DIFF unexpected MAP S017->S021 held
DIFF missing REFUSED S102: recheck '2026-02-30 — re-verify after release' has no leading valid date or NNd
DIFF missing TOOLEXIT 1 · DIFF unexpected TOOLEXIT 0 · DIFF unexpected MAP S101->S002 append
DIFF unexpected MAP S102->S002 held · DIFF order cases/twin-recheck: - (want REFUSED S102: recheck …)
DIFF order cases/refusal-order: REFUSED entry missing: corpus/knowledge/absent.md (want REFUSED registry has no `## Registry` heading)
DIFF order cases/refusal-order: - (want REFUSED registry has no `## Registry` heading)
SELFTEST=FAIL findings=45 expected=40                            # rc=1
$ python3 patched/tool.py --selftest --fixtures fixtures         # green
FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6
SELFTEST=PASS findings=40 expected=40                            # rc=0 (was 3b7ad258… / 27 findings)
$ # the two diffs applied with `patch -p1` to a lane-shaped copy, then with no flags at all:
$ python3 tools/assimilate-rows.py --selftest
FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6 · SELFTEST=PASS findings=40 expected=40
$ python3 patched/tool.py --selftest --cites all --fixtures corpus/evidence/round50/c1-fixtures \
    --expected corpus/evidence/round50/c1-fixtures/expected.json
FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43 · SELFTEST=PASS findings=26 expected=26
$ python3 corpus/evidence/round51/c1-count.py --tool …/patched/tool.py --seed 51
SELFTEST_DEFAULT=PASS (skipped: --tool) · LEGACY_ALL=PASS rc=0 · SOURCE_ONLY=PASS map=['S757','S782'] appended=1
bodyonly=[['corpus/knowledge/e.md','S582']] all_rc=0 · PIPE_IDENTITY=PASS d1=ok d2=ok · REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5 · C1=PASS                                               # rc=0; the unpatched tool reports the same
```
The label and the union `used-by` on the default package, plain run (`--staged fixtures/staged.md --knowledge
fixtures/knowledge --registry fixtures/registry.md --opened 2026-10-25 --out dflt --entry …/a.md --entry …/b.md`):
`CITED=6 APPEND=2 HELD=3 TWIN=1`; `S010 S021 append`, `S017 S021 twin`; the appended row's `used-by` is
`corpus/knowledge/a.md` — the entry citing either row.

## 6. Risks and what I did not touch

- `HELD=` changes meaning (twins move to `TWIN=`): re-read any receipt quoting `HELD=<n>` for a twin set. No counter
  parses it; round 51 is 5/5 above.
- Default fixture digest moves `3b7ad258…` → `9822ad59…` (28 root findings, 40 with cases). Round-51's
  `SELFTEST_DEFAULT` leg checks only exit 0 + `SELFTEST=PASS`, so it stays green at integration.
- `RECHECK_RE`'s cadence branch accepts any `[A-Za-z][A-Za-z0-9 _-]*`, so `INVALID_RECHECK` is not invalid — named,
  not fixed (it is the tool's own grammar; narrowing it is a claims-level change).
- Still open from round 51 and untouched: N1 staged-vs-lane precedence, N3/N4 header reading, N5 body tokens,
  N6 `GREP_RE`/`ROW_RE` split, N7 `bodyonly.tsv` header tails. This patch fixes F5 and F6 only.
- Only `tools/assimilate-rows.py` and `corpus/fixtures/assimilate-selftest/` are touched. Counters, claims and every
  other lane file are read-only here; the round-51 counter ran against the scratch copies with `TMPDIR` in scratch,
  and no lane gate was executed as a gate.

VERDICT: both halves of routed defect 2 hold at `13bc280` — a same-run twin is labelled `held` with its
calendar-invalid recheck swallowed, and the registry refusal follows the entry refusal and is absent without
`--entry`; the patch (`twin`, every cited recheck validated, registry first and unconditional) turns red-before into
`SELFTEST=PASS findings=40`, `FIXTURES_SHA256=9822ad59…`, with the round-50 pin 26/26 and the round-51 counter 5/5.

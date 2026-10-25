# ScoutInheritedTree — round 46 / w1

Item: report `git status --porcelain`, `git diff --stat`, lane tip; confirm the three modified paths are the previously left-named inherited ones; name untracked paths this round's seats created; check `.ufo/l0-questions.md` for an operator answer to (a) fetch scope `8d77e6c1`, (b) the round-43 inherited-tree question, (c) the round-44 round-shape question.
Read-only seat: no lane production file, git/jj state, or fleet write outside this report.

## Lane state — two snapshots (cwd = lane root)

```
$ bash …/scripts/hyaku/jj-lane.sh state …/chousa-shokunin   # 07:24, opening
state branch=master local=c2f0e9d100c0d46633a6277b2fd51d2ac99678eb remote=c2f0e9d100c0d46633a6277b2fd51d2ac99678eb ahead=0 behind=0 head=detached tracked=3 untracked=3

Opening 07:24 — the tree held exactly the three inherited modifications plus this wave's first writes:
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/evidence/round41/receipts/cells/cells.json
?? .ufo/waves/round-46/   ?? corpus/evidence/round46/build-spans.py   ?? tools/inference-ground.py

Closing 07:30 — seats kept writing; the same three inherited lines are unchanged (diffstat 70 / 641 / 185 below),
and four more tracked files are now modified by this round:
 M corpus/SOURCES.md                               |   5 +
 M corpus/evidence/round46/c1-count.py             |   5 +-
 M corpus/evidence/round46/c2-count.py             |  27 +-
 M corpus/evidence/round46/c3-count.py             |  10 +-
 7 files changed, 652 insertions(+), 291 deletions(-)
```

Jj's `untracked=3` was already stale at the closing snapshot (6 untracked entries): seats were writing while jj was queried, so `git status` is the operative list. The set kept growing after 07:30 — `SKILL.md` (Gates rows, scribe seats) was modified by 07:31 — so treat each block as a timestamped snapshot, not as a final inventory. Tip `c2f0e9d` "round-46: freeze three claims …" (parent `6e2630a`, r45 verifier spot-check) commits `corpus/evidence/round46/{claims.md,c1-count.py,c2-count.py,c3-count.py,controls/*}` and `corpus/fixtures/inference-ground-r46/*`; `git ls-tree -r c2f0e9d -- tools` lists the 7 pre-existing tools.

## (1) The three inherited modified paths ARE the previously left-named ones — verified

Exact match against `.ufo/l0-questions.md:144` (round 43): "Left untouched, not this round's
work: modified `.ufo/waves/round-40/w1/swarm-registry.json`, `.ufo/waves/round-41/w1/swarm-registry.json`, `corpus/evidence/round41/receipts/cells/cells.json`". Same three.
`corpus/lessons/round-44.md:22-23` calls them "3 modified JSON files … left-named with `not hunk-verified`"; `corpus/lessons/round-45-verifier-spotcheck.md:11` saw the same three.

```
$ sha256sum corpus/evidence/round41/receipts/cells/cells.json
1f5c0afae8024c50013e9a9060988c14506115125e3823042e4512833f293b80
$ stat -c '%y %s %n'
2026-10-24 04:18:06 -0300 18572 .ufo/waves/round-40/w1/swarm-registry.json
2026-10-24 04:42:46 -0300 23757 .ufo/waves/round-41/w1/swarm-registry.json
2026-10-25 06:36:03 -0300  8122 corpus/evidence/round41/receipts/cells/cells.json
$ git diff --numstat
36  34  .ufo/waves/round-40/w1/swarm-registry.json
427 214 .ufo/waves/round-41/w1/swarm-registry.json
149  36  corpus/evidence/round41/receipts/cells/cells.json
$ git log --oneline -2 -- <each>
r40 registry -> d164f88 / 6c01a41 (r40); r41 registry and cells.json -> 1bd9001 (r41)
```
The hash is identical to the round-45 record for the restored file ("snapshotted and restored the bytes (sha256 `1f5c0afae802…`; diff stat unchanged, 185 lines, the round-44 left-named state)" — `corpus/lessons/round-45.md:70-73`); current diff 149/36 = 185 lines. Both registry mtimes predate the round-45 wave (`swarm-registry.json` written 06:32:57; wave dir 06:59) and this round (07:17+); cells.json's 06:36:03 is the ledgered `ScribeGateR41` write-by-default incident, restored byte-exact (`round-45.md:68-77`). No commit has touched any of the three since r41.

**Half of the round-43 inherited-tree debt is already closed without an operator answer** — the question also named "the untracked r40/r41 seat reports":

```
$ git log --oneline -1 --diff-filter=A -- .ufo/waves/round-40/w1/ConnectorSiblingScan.md .ufo/waves/round-41/w1/ConnectorSiblingScan.md
6254b4d round-44: commit the 36 re-verified inherited r40/r41 seat reports (C2 reverified-commit class)
$ git ls-files .ufo/waves/round-40/w1 | wc -l   -> 34 (33 reports + registry)
$ git ls-files .ufo/waves/round-41/w1 | wc -l   ->  4 (3 reports + registry)
```
33 + 3 = 36, matching the commit subject; nothing untracked remains under either `w1/`. The open part of (b) is therefore exactly the three modified JSON files.

## (2) Untracked paths this round's seats created in the lane

- `.ufo/waves/round-46/` (07:23:38–07:24:11): `gen-w1-spec.py`, `w1-spec.json` 56 778 B, `w1-dispatch.json` 135 552 B, `w1-plan.err` 0 B, `w1-run.err` 0 B, `w1/swarm-registry.json` 62 414 B / 32 members — lane plumbing.
- `corpus/evidence/round46/build-spans.py` 4 203 B + `spans.tsv` 2 492 B (header + 11 rows) + `spans/` (11 files, S085-1 … S089-1), all 07:25:22 — ExecSpanBuilder.
- `corpus/knowledge/evidence-pool-versioning-r39.md` 5 451 B (07:25:44) — ScribeEntryBase; `…-amendment-2026-10-23.md` (between 07:25:54 and 07:26:47) — ScribeEntryAmend.
- `tools/inference-ground.py` 9 678 B (07:26:36) — C1 tool seat.

`ls .ufo/waves/round-46/w1/*.md` → no such file at the closing snapshot: reports were in flight and **none had been mis-rooted into the fleet root** (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-46` does not exist). `reportDir` is lane-relative (`.ufo/waves/round-46/w1`; 33 relative report mentions in the dispatch) while item prose carries 73 absolute lane paths (spec) and 131 (dispatch): the round-45 D4 misroot class still hinges on each seat resolving the relative trailer against the lane root.

## (2b) Seats also modified four tracked files, three of them frozen counters

`corpus/SOURCES.md` gained the five rows S085–S089 (`+5`, mtime inside this window; S088/S089 rows name the amendment entry), i.e. the registry mirror landed. The three counters were edited after the freeze commit:

```
$ git diff -U2 corpus/evidence/round46/c1-count.py        # 07:27:37, excerpt (a 3-line comment added)
-    junk = sum(run(tool, fixture_dir, n) != 0 for n in JUNKS) if present else 0
+    junk = sum(run(tool, fixture_dir, n) == 1 for n in JUNKS) if present else 0
$ git diff -U1 corpus/evidence/round46/c2-count.py        # 07:28:28, excerpt
+        if line.lstrip().startswith("```"):            # fence-aware rows
+            fence = not fence
+            continue
+        bare = re.sub(r"<!--.*?-->", "", line)          # HTML comments stripped
+def names(row, path):                                   # boundary, never suffix-of
+    return re.search(r"(?<![A-Za-z0-9_./-])" + re.escape(path) + r"(?![A-Za-z0-9_./-])", row) is not None
$ git diff -U1 corpus/evidence/round46/c3-count.py        # 07:29:33, excerpt (traversal + offset guards)
-        span_path = ev / span_file
+        raw = span_file.strip()
+        if not raw or raw.startswith("/") or ".." in pathlib.PurePath(raw).parts:
+            continue
+        try:
+            o = int(offset)
+        except ValueError:
+            continue
```
The inline comments attribute them to `MutC1Junk` / `MutC2Forge` / (none in c3). Neutrality evidence:

- **C2** — measured: `c2-count.py --list` → `exit=1`, `ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=30 REGISTERED=55/72 UNREGISTERED=17 C2=FAIL`. Frozen before-state was `REGISTERED=55/71`; registered stayed 55 and the one new entry point is the untracked `tools/inference-ground.py`. So no existing registration moved, but the fence / HTML-comment / boundary rules are cases the frozen controls do not contain.
- **C1** — value-neutral over the two recorded control transcripts (`controls/c1-controls.txt`: always-exit-0 → 0/3, cite-only → 1/3; both tools exit 0/1) — [INFERENCE from those transcripts, not re-run]. It does change the score for a tool that crashes (2) or is missing (127), which `!=0` counted as kills.
- **C3** — the frozen `spans.tsv` has no absolute or `..` span path and no non-integer offset (`awk` over columns 4–5 returns nothing), so the new guards cannot fire on this manifest; neutral as measured on the manifest.

Against `claims.md` §Admission ("A rule changed after any seat has scored is not this claim's rule"), the L1 must dispose of all three edits: disclose as an erratum with a value-neutrality measurement (the tabi r22 precedent) or score C1–C3 on the frozen bytes. This seat edited no counter.

## (3) Operator answers in `.ufo/l0-questions.md`

```
$ grep -c "L0 ANSWER" .ufo/l0-questions.md            -> 2
$ grep -n "^chousa | round-4[1-6]"
136 round-41 fetch-scope 8d77e6c1 pending · 140 round-42 still open · 143 round-43 register staleness
144 round-43 inherited tree · 148 round-44 round shape
$ grep -n "^chousa | round-46" -> (empty)
```

- **(a) fetch scope `8d77e6c1`: no answer.** The only two `L0 ANSWER` lines are the planner-taxonomy ruling dated 2026-10-19 (lines 52, 53: "planner is a frozen-topology seat the swarm validator rejects by design"); neither mentions `8d77e6c1`.
- **(b) round-43 inherited tree: no answer.** Line 144 has no answer suffix and no later line supersedes it; no round-45/46 chousa line exists.
- **(c) round-44 round shape: no answer.** Line 148 likewise, truncated by the 768-byte line cap, with no answer text.

The file's 07:25 mtime is an orchestrator append during this wave, not an answer: the answer count is 2 both before and after the wave started.

## Verdict

CONFIRMED. Opening state: exactly the three inherited modified paths named in round 43 (cells.json hash matches the r45 restore, 1f5c0afae802…; both registries mtime-stable since 2026-10-24 and uncommitted since r41), plus this wave's first untracked writes. By 07:30 the wave had added five more untracked paths and modified four tracked files — `SOURCES.md` (rows S085–S089) and all three frozen counters, the latter a post-freeze rule change the L1 must disclose or score on the frozen bytes. The r40/r41 seat reports named in the round-43 question are committed by `6254b4d`, so only those three JSON files remain open there. **No operator answer exists for (a), (b) or (c).**

Unknowns: whether the counter edits were applied by the named mutant seats or by the L1 acting on their findings (the comments are the only attribution); whether any wave-1 seat rewrites `cells.json` or the two registries — no spec item names `round41/receipts` (`grep -c` = 0 in `w1-spec.json` and `w1-dispatch.json`), but `corpus/evidence/round41/c1-count.py` is write-by-default (`round-45.md:68-77`); and whether the round-46 entries/counters verify (other seats own that).

## Pointers

- `.ufo/l0-questions.md:136,140,144,148` open; `:52,53` the two answers.
- `corpus/lessons/round-44.md:22-23`; `corpus/lessons/round-45.md:68-77`; `corpus/lessons/round-45-verifier-spotcheck.md:11`.
- Commits `6254b4d` (36 inherited seat reports), `c2f0e9d` (round-46 freeze); `.ufo/waves/round-46/w1/swarm-registry.json` (32 members).
- `corpus/evidence/round46/{c1,c2,c3}-count.py` (uncommitted mid-wave edits), `controls/{c1,c2}-*.txt`, `corpus/evidence/round46/spans.tsv`.

Tooling: none installed or upgraded (no `pacman`/`uv`/`npx`). No network egress. Scratch: one `/tmp/chousa-r46-c2.out` capture used and deleted; no other scratch.

# SentScope2 — scope and egress audit of the landed round-46 state

item: `git status --porcelain`; confirm no round-46 file names the fleet repo or shokuknow
**for writing**; grep the round's new code for egress and write paths; check that
`corpus/evidence/round46/{controls,spans}/` hold only what the counters read; report every hit
and whether it can write outside the lane.

base `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` (claims frozen `c2f0e9d1`). **The tree moved
under the audit**: 18 dirty paths at `d09fc8e`; HEAD became
`3807537db7e731af508ad7f7d5462f4422ce04c8` ("wave-2 corrections…"), which folded most in;
then `c1-count.py` went dirty, and at the last read `c1-before/controls`, the `round-46.md`
lesson and `tools/inference-ground.py` were dirty again. Each finding names its state.

| # | Finding | True in | Sev |
|---|---|---|---|
| F1 | `inference-ground.py` crashes `UnboundLocalError` → exit **1** = the "findings"/kill code | HEAD `3807537` | **high** |
| F2 | the two fixture span files are unpinned; a mutated fixture set is not refused | both | low-med |
| F3 | `SKILL.md:116` pins `819f83ebdc6c…`; `measure-after` + the file say `3018b1d2…` | HEAD | medium |
| F4 | egress: **none** in the round's code | all | clean |
| F5 | `--json OUT` escapes `--root` (declared); dirty c1 writes /tmp (undeclared) | HEAD / uncommitted | low |
| F6 | `spans/`, `controls/` hold exactly what is read / named | all | clean |
| F7 | 3 inherited dirty paths survive; the live counter ≠ the recorded one | `d09fc8e`→HEAD | medium |
| F8 | no round-46 path landed at the fleet root | all | clean |

C1/C2/C3 each reproduce exit 0, targets met, at `d09fc8e` **and** `3807537`. Nothing here
falsifies a frozen predicate, target or kill rule; F1–F3 are defects in instrument and record.

## F1 — a crash exits 1, and 1 is the code the junk leg counts as a kill  (high)
`tools/inference-ground.py:71` runs `if cur is not None:` inside the **pre-scan** loop (68–80);
`bullets, cur, fence` are first bound at line 83, so any entry with a fence **above**
`#### Inference` raises. A fully grounded entry (the `d09fc8e` tool: `GROUND: PASS`, exit 0):

    $ python3 tools/inference-ground.py --entry probe/fx/grounded-but-fenced.md ...
        if cur is not None:
    UnboundLocalError: cannot access local variable 'cur' where it is not associated with a value
    exit=1

Reachable on a real adopted entry — one fenced block above `#### Inference` (char 3356) in
`corpus/knowledge/evidence-pool-versioning-r39.md` → same `UnboundLocalError`, exit 1;
unmodified, that file is `GROUND: PASS` exit 0. An unevaluable entry is therefore
indistinguishable from a refused one. `c1-count.py` says "a crash (2) … is not a kill", but an
uncaught exception is **exit 1**, so it *is* counted; `SKILL.md:116` maps exit 1 to "findings",
so a crash reads as findings. JUNK_KILLED=3/3 is not itself laundered — `grep -c '```'` = 0 in
all six pinned fixtures, so the set cannot reach the path — but the mechanism is unsound.
Introduced by `3807537`; the `d09fc8e` tool (`819f83ebdc6c…`) returns a real finding.

## F2 — the fixture set is only partly pinned  (both states)
`PINNED` covers the 6 entries + `spans.tsv` + `counts.json`, not
`corpus/fixtures/inference-ground-r46/spans/S901-1.txt` / `S902-1.txt`, which the tool reads
through the manifest. Mutating `S901-1.txt`:

    $ python3 corpus/evidence/round46/c1-count.py --root .
    TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=2/3 / C1=FAIL     (no FIXTURES_CHANGED)

So the kill rule's "a fixture set changed after this freeze fails the claim" is not enforced
for two members of the set; it degrades into a lower score. Harm is one-directional (a
mutation cannot manufacture 3/3) and the gap survives the dirty canary hardening.

## F3 — row pin and the round's own measurement disagree inside one commit  (medium)
    $ git show HEAD:corpus/evidence/round46/measure-after.txt | sed -n 3p
    ### counter revisions: … tool 3018b1d25d762054  build-spans b5c4d83b…
    $ git show HEAD:tools/inference-ground.py | sha256sum   → 3018b1d25d762054…
    $ grep -o 'sha256 `819f83ebdc6c' SKILL.md               → sha256 `819f83ebdc6c

`3807537` recomputed `measure-after.txt` for the corrected tool (and raised `ENTRY_POINTS`
72→73); its only `SKILL.md` edit made `--registry` mandatory. The row's pinned-value cell still
names `819f83ebdc6c…`, the `d09fc8e` bytes — the field whose job is to bind a Gates row to its
bytes is the wrong one. True at `d09fc8e`, false at HEAD.

## F4 — egress: none  (clean)
Grep over `tools/inference-ground.py`, the four round-46 `*.py`, the fixtures and both
dispatchers for `urllib|requests|socket|http\.client|httpx|curl|wget|os\.system|popen`:
**zero hits**. The only spawn is `c1-count.py:57 subprocess.run([sys.executable, …])` — fixed
argv, no shell, no network. The dispatchers write only their own spec JSON under the lane.

## F5 — write scope: every hit
| path:line | write | escapes the lane? |
|---|---|---|
| `tools/inference-ground.py:290` | `pathlib.Path(a.json).write_text(…)` | **yes** — `--json /tmp/…/escape.json` with `--root probe/fx` wrote 109 B; a `../` target likewise. Declared accurately: "read-only (no network); `--json OUT` writes exactly the named path". Caller-chosen, no containment. |
| `build-spans.py:102-105` | `HERE/spans/`, `HERE/spans.tsv` | no — `HERE` only |
| `c1-count.py` (dirty `8473abf6…`) | `tempfile.TemporaryDirectory()` + `shutil.copyfile` | yes, `/tmp`, auto-removed; **undeclared** — the row still says "c1 and c2 are read-only" |
| `c2-count.py`, `c3-count.py` | none | no — print only |

Nothing writes to `/home/vgpnk/Projects/shokunin` or `…/shokuknow`; every out-of-lane
reference is a **read**: the `.qcache` captures (3 sites), the staged package
`merge/chousa/knowledge/…`, `scripts/sources-census.sh validate --root …` (read-only),
`CORPUS.md`, `RULES.md`. Both dispatchers state the prohibition; no item overrides it.

## F6 — `controls/` and `spans/` hold exactly what is read  (clean)
- `spans/`: 11 files = 11 rows = 11 distinct `span_file` names, on-disk vs manifest `diff` empty
  (`SPANS_SET_EQUAL=yes`); `build-spans.py --check` → `SPANS_ROWS=11 STALE=0` exit 0. Fixture
  `spans/` likewise `{S901-1, S902-1}`, its digests all-zero placeholders under `example.invalid`.
- `controls/`: exactly the 6 files `claims.md` names and **no code reads any of them**
  (`grep -rn 'controls/' --include=*.py` → empty) — transcribed records. Re-derived where
  cheap: `c1-before` reproduces on `6e2630a` + this round's counters/fixtures, tool absent →
  `TOOL=absent POSITIVE_PASS=0/3 JUNK_KILLED=0/3 C1=FAIL`, exit 1.
- Stray only: `corpus/evidence/round46/__pycache__/` (gitignored).

## F7 — the base tree was dirty, and the live instrument is not the recorded one
`d09fc8e` carried 18 dirty paths: 11 wave-1 reports, `SKILL.md`, `corpus/SOURCES.md`, both
knowledge entries, `SCORECARD.md`, `tools/inference-ground.py` — folded into `3807537` — plus
**3 inherited paths still dirty** (Oct 24): `.ufo/waves/round-{40,41}/w1/swarm-registry.json`
and `corpus/evidence/round41/receipts/cells/cells.json`, which contradicts its committed self
(`k 12→1`, `predicate_holds true→false`, `gate` retargeted to
`.ufo/waves/round-41/controls/base-gate-r41.sh`). It predates round 46, not this round's
write, but `d09fc8e` is not a clean base until it is settled. After `3807537`, `c1-count.py`
is dirty (`8473abf6…` vs recorded `819287e2…`, adding a `CANARY` leg over a `TemporaryDirectory`):
both print `C1=PASS` exit 0, so the claim holds either way, but by the admission rule the dirty
instrument "is not this claim's rule" and must not be what scores C1. Both `measure-after.txt`
copies are honest about their own tree (72/tool `819f83eb`; 73/tool `3018b1d2`) — reproduced
both. Caveat: the HEAD copy records `measured …07:37:21` while `3807537`'s author date is
`07:32:44`, so that measurement is a claim the file makes, not an independent timestamp.

## F8 — no misroot at the fleet root  (clean)
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-46` ABSENT; `…/.ufo/reports/round-46` holds
only other lanes' files (`kake`, `kotoba`, `kotodama`, `kumitate`; Oct 19–24), no chousa
content; fleet `status --porcelain` shows no untracked chousa or round-46 file.

## Remediation, in dependency order
1. **F1** — delete the pre-scan hunk `tools/inference-ground.py:71-73`, or bind `bullets, cur`
   before line 68. Restores "a crash is not a kill".
2. **F3** — then recompute the pin in `SKILL.md:116`, and add the traceback case to the row.
3. **F2** — add the `S901-1.txt`, `S902-1.txt` digests to `c1-count.py` `PINNED`.
4. **F7** — settle the round-41 `cells.json` contradiction; the dirty `c1-count.py` must not stand.

Reproduce: `c1/c2/c3-count.py --root <tree>` on `d09fc8e` and `3807537` (both exit 0);
`build-spans.py --check`; `sha256sum tools/inference-ground.py` vs the `SKILL.md` pin;
`git rev-parse HEAD` (twice). Scratch trees from `git archive … | tar -x -C /tmp/…`, removed.

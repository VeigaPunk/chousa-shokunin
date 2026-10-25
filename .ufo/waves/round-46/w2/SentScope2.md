# SentScope2 — scope and egress audit of the landed round-46 state

item: run `git status --porcelain`; confirm no round-46 file names the fleet repo or
shokuknow **for writing**; grep the round's new code for egress and write paths; check that
`corpus/evidence/round46/{controls,spans}/` hold only what the counters read; report every
hit and whether it can write outside the lane.

base: lane `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` (claims frozen at `c2f0e9d1`).
**The tree moved under the audit**: at 07:2x–07:36 the worktree was 18 paths dirty at
`d09fc8e`; HEAD then became `3807537db7e731af508ad7f7d5462f4422ce04c8` ("wave-2
corrections…"), which folded most of that in, and `c1-count.py` was left dirty after it.
Every finding below names the state it is true in.

## Verdict

| # | Finding | True in | Severity |
|---|---|---|---|
| F1 | `inference-ground.py` crashes `UnboundLocalError` → exit **1**, the "kill"/"findings" code | HEAD `3807537` | **high** |
| F2 | the two fixture span files are unpinned; a mutated fixture set is not refused | `d09fc8e` + HEAD | low-med |
| F3 | `SKILL.md:116` pins `819f83ebdc6c…` while `measure-after.txt` and the file both say `3018b1d2…` | HEAD `3807537` | medium |
| F4 | egress: **none** anywhere in the round's code | all | clean |
| F5 | write scope: `--json OUT` escapes `--root` (declared); dirty c1 writes /tmp (not declared) | HEAD / uncommitted | low |
| F6 | `spans/` and `controls/` hold exactly what is read / named | all | clean |
| F7 | 3 inherited dirty paths survive; the live counter is not the recorded one | `d09fc8e`→HEAD | medium |
| F8 | no round-46 path landed at the fleet root | all | clean |

C1/C2/C3 each reproduce (exit 0, targets met) at `d09fc8e` **and** at `3807537`. Nothing here
falsifies a frozen predicate, target or kill rule; F1–F3 are defects in the instrument and
the record.

## F1 — a crash exits 1, and 1 is the code the junk leg counts as a kill  (high, HEAD)

`tools/inference-ground.py:71` executes `if cur is not None:` inside the **pre-scan** loop
(lines 68–80); `bullets, cur, fence` are first bound at line 83. Any entry with a code fence
**above** `#### Inference` raises. On a fully grounded synthetic entry (committed-parent tool
prints `GROUND: PASS` exit 0):

    $ python3 tools/inference-ground.py --entry probe/fx/grounded-but-fenced.md ...
        if cur is not None:
    UnboundLocalError: cannot access local variable 'cur' where it is not associated with a value
    exit=1

Reachable on a real adopted entry — one fenced block inserted above `#### Inference`
(char 3356) in `corpus/knowledge/evidence-pool-versioning-r39.md`:

    $ python3 tools/inference-ground.py --entry corpus/knowledge/evidence-pool-versioning-r39.md ... 
    UnboundLocalError: cannot access local variable 'cur' where it is not associated with a value
    exit=1

The same file unmodified is `GROUND: PASS` exit 0. An entry the tool cannot evaluate is
therefore indistinguishable from a refused one. `c1-count.py` says "a crash (2) or a missing
file (127) is not a kill", but an uncaught exception is **exit 1**, so it *is* counted; and
`SKILL.md:116` maps exit 1 to "findings", so a crash reads as findings. The measured
JUNK_KILLED=3/3 is not itself laundered — `grep -c '```'` = 0 in all six pinned fixtures, so
the fixture set cannot reach the path — but the mechanism is unsound. Introduced by
`3807537`: the tool measured at `d09fc8e` (`819f83ebdc6c…`) returns a real finding here.

## F2 — the fixture set is only partly pinned  (low-med, `d09fc8e` and HEAD)

`c1-count.py` `PINNED` covers the 6 entries + `spans.tsv` + `counts.json` — not
`corpus/fixtures/inference-ground-r46/spans/S901-1.txt` / `S902-1.txt`, which the tool reads
through the manifest. Mutating `S901-1.txt`:

    $ python3 corpus/evidence/round46/c1-count.py --root .
    TOOL=present
    POSITIVE_PASS=3/3
    JUNK_KILLED=2/3
    C1=FAIL                      (no FIXTURES_CHANGED line)

The kill rule's sentence — "a fixture set changed after this freeze fails the claim" — is
not enforced for two members of the set; it degrades into a lower score instead. Harm is
one-directional (a mutation can only lower the score; it cannot manufacture 3/3), and the
gap survives the uncommitted canary hardening. Fix: add both digests to `PINNED`.

## F3 — the row's pin and the round's own measurement disagree inside one commit (medium)

    $ git show HEAD:corpus/evidence/round46/measure-after.txt | sed -n 3p
    ### counter revisions: c1 819287e2… c2 60ad448e… c3 234e2272…  tool 3018b1d25d762054  build-spans b5c4d83b…
    $ git show HEAD:tools/inference-ground.py | sha256sum   → 3018b1d25d762054…
    $ grep -o 'sha256 `819f83ebdc6c' SKILL.md               → sha256 `819f83ebdc6c

`3807537` recomputed `measure-after.txt` for the corrected tool (and raised
`ENTRY_POINTS` 72→73), and its only `SKILL.md` edit was to make `--registry` mandatory — the
pinned-value cell of the `inference-ground` row still names `819f83ebdc6c…`, the
`d09fc8e` bytes. So two round-46 records contradict each other, and the one field whose job
is to bind a Gates row to its bytes is the wrong one. True at `d09fc8e`, false at HEAD.

## F4 — egress: none  (clean)

Grep over `tools/inference-ground.py`, the four round-46 `*.py`, the fixtures and both
dispatchers for `urllib|requests|socket|http\.client|httpx|curl|wget|os\.system|popen`:
**zero hits**. The only process spawn is `c1-count.py:57 subprocess.run([sys.executable, …])`
— fixed argv, no shell, no network. `gen-w1-spec.py` / `gen-w2-spec.py` write only their own
spec JSON under the lane `.ufo/waves/round-46/`.

## F5 — write scope: every hit, and whether it escapes the lane

| path:line | write | escapes? |
|---|---|---|
| `tools/inference-ground.py:290` | `pathlib.Path(a.json).write_text(…)` | **yes** — proven: `--json /tmp/…/escape.json` with `--root probe/fx` wrote 109 B; a `../` relative target likewise. Declared accurately in the row: "read-only (no network); `--json OUT` writes exactly the named path". Caller-chosen, no containment. |
| `build-spans.py:102-105` | `HERE/spans/`, `HERE/spans.tsv` | no — `HERE` only |
| `c1-count.py` (dirty `8473abf6…`) | `tempfile.TemporaryDirectory()` + `shutil.copyfile` | yes, to `/tmp`, auto-removed. **Undeclared**: the row still says "c1 and c2 are read-only". Uncommitted drift. |
| `c2-count.py`, `c3-count.py` | none | no — print only |

No round-46 file writes to `/home/vgpnk/Projects/shokunin` or
`/home/vgpnk/Projects/shokuknow`. Every out-of-lane reference is a **read**: the `.qcache`
captures (3 sites), the staged package `merge/chousa/knowledge/…`,
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (read-only
validate), `CORPUS.md`, `RULES.md`. Both dispatchers state the prohibition and no item
overrides it.

## F6 — `controls/` and `spans/` hold exactly what is read  (clean)

- `spans/`: 11 files = 11 manifest rows = 11 distinct `span_file` names; `diff` of on-disk vs
  manifest set is empty (`SPANS_SET_EQUAL=yes`); `build-spans.py --check` →
  `SPANS_ROWS=11 STALE=0` exit 0. Fixture `spans/` likewise `{S901-1, S902-1}`, and the
  fixture manifest's digests are all-zero placeholders under `example.invalid` URLs, so they
  cannot be read as a real capture digest.
- `controls/`: exactly the 6 files `claims.md` names, and **no code reads any of them**
  (`grep -rn 'controls/' --include=*.py` → empty); they are transcribed records, unverified
  by construction. Re-derived where cheap: `c1-before` reproduces byte-for-byte on
  `6e2630a` + this round's counters/fixtures with the tool absent —
  `TOOL=absent POSITIVE_PASS=0/3 JUNK_KILLED=0/3 C1=FAIL`, exit 1.
- Only stray: `corpus/evidence/round46/__pycache__/` (gitignored, untracked).

## F7 — the base tree was dirty, and the live instrument is not the recorded one

At first read, `d09fc8e` + 18 dirty paths: 11 wave-1 reports, `SKILL.md`, `corpus/SOURCES.md`,
both knowledge entries, `SCORECARD.md` and `tools/inference-ground.py` (all folded into
`3807537`), plus **3 inherited paths that are still dirty** — `.ufo/waves/round-40/w1/`,
`.ufo/waves/round-41/w1/swarm-registry.json` (Oct 24) and
`corpus/evidence/round41/receipts/cells/cells.json` (Oct 24 06:36). That last one contradicts
its committed self: `k 12→1`, `predicate_holds true→false`, `gate` retargeted to
`.ufo/waves/round-41/controls/base-gate-r41.sh`. It predates round 46 — not this round's
write — but `d09fc8e` is not a clean base until it is resolved.

After `3807537`, `c1-count.py` is dirty again (`8473abf6…` vs recorded `819287e2…`, adding a
`CANARY` leg on a `TemporaryDirectory`). Both versions print `C1=PASS` exit 0, so the claim
holds either way; per the admission rule the dirty instrument "is not this claim's rule" and
must not be what scores C1.

Both `measure-after.txt` copies are honest about their own tree: the `d09fc8e` copy (72,
tool `819f83eb`) describes `d09fc8e`, the HEAD copy (73, tool `3018b1d2`) describes HEAD —
I reproduced both. One caveat: the HEAD copy records `measured …07:37:21` while `3807537`'s
author date is `07:32:44`, so the measurement is a claim the file makes, not an independently
timestamped event (consistent with an amend; not a defect by itself).

## F8 — no misroot at the fleet root  (clean)

`/home/vgpnk/Projects/shokunin/.ufo/waves/round-46` → ABSENT.
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-46` exists but holds only other lanes'
files (`kake.md`, `kotoba.md`, `kotodama.md`, `kumitate.md`; Oct 19–24) — no chousa content.
`git -C /home/vgpnk/Projects/shokunin status --porcelain` shows no untracked chousa or
round-46 file.

## Smallest remediation, in dependency order

1. **F1** — delete the pre-scan hunk `tools/inference-ground.py:71-73` (or bind
   `bullets, cur` before line 68). Restores "a crash is not a kill".
2. **F3** — after (1), recompute the pin in `SKILL.md:116`, and add the traceback case to
   the row's exit contract.
3. **F2** — add `spans/S901-1.txt` and `spans/S902-1.txt` digests to `c1-count.py` `PINNED`.
4. **F7** — settle the round-41 `cells.json` contradiction, and do not let the dirty
   `c1-count.py` stand as the C1 instrument.

## Reproduce

`python3 corpus/evidence/round46/{c1,c2,c3}-count.py --root <tree>` on `d09fc8e` and on
`3807537` (both exit 0); `build-spans.py --check` → `SPANS_ROWS=11 STALE=0`;
`sha256sum tools/inference-ground.py` vs `grep 'sha256 `819f83ebdc6c' SKILL.md`;
`git rev-parse HEAD` (twice — it changed mid-audit).
Scratch trees were built with `git archive <commit> | tar -x -C /tmp/…` and mutated only
there; `/tmp/chousa-r46w2-SentScope2/` is removed on exit.

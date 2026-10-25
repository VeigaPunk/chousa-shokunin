# R51CritForgeC1 — attack on the frozen C1 counter

Scope: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/c1-count.py` at lane tip
(base 9ec1751, counter committed). No production file edited; counter not edited; scratch under
`/dev/shm/chousa-r51-R51CritForgeC1/` (deleted at close). Axes: **operability** (does the counter see the
five behaviours?) and **calibration** (is a PASS evidence?).

## 1. A 94-line forge with none of the five behaviours passes 5/5

`python3 corpus/evidence/round51/c1-count.py --tool /dev/shm/chousa-r51-R51CritForgeC1/forge-dirname.py --seed 1`
(also seeds 2, 3, 11, 23 — identical verdicts):

```
SELFTEST_DEFAULT=PASS (skipped: --tool)
LEGACY_ALL=PASS rc=0
SOURCE_ONLY=PASS default_rc=0 map=['S532', 'S891'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S630']] all_rc=0 all_map=['S532', 'S630', 'S891']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY renamed-heading rc=1 -> PASS
REGISTRY no-heading rc=1 -> PASS
REGISTRY row-outside rc=1 -> PASS
REGISTRY well-formed rc=0 -> PASS
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
C1=PASS
EXIT=0
```

Lane baseline for comparison (`c1-count.py` with no `--tool`): `LEGS=5/5 / C1=PASS / EXIT=0`. The forge is
indistinguishable from the real tool to this counter.

Fenced, intended lane path `corpus/evidence/round51/controls/forge-dirname.py` (94 lines):

```python
#!/usr/bin/env python3
"""forge-dirname — cheapest C1 forge. Implements none of the five behaviours:
no escaped-pipe splitter, no document-identity rewrite, no source-vs-body
citation rule, no registry-heading scan, no D3 row-outside check. It reads the
counter's per-subtest directory name out of --out and emits canned shapes.
"""
import hashlib
import pathlib
import sys

argv = sys.argv[1:]


def opt(name: str) -> str:
    return argv[argv.index(name) + 1] if name in argv else ""


# --- LEGACY_ALL: never run the adopter; echo 26 and the fixture digest --------
if "--selftest" in argv:
    fix = pathlib.Path(opt("--fixtures")) if opt("--fixtures") else None
    h = hashlib.sha256()
    if fix:
        for q in sorted(x for x in fix.rglob("*") if x.is_file()):
            h.update(q.relative_to(fix).as_posix().encode() + b"\0" + q.read_bytes() + b"\0")
    print(f"FIXTURES_SHA256={h.hexdigest()}")
    print("SELFTEST=PASS findings=26 expected=26")
    sys.exit(0)

out = pathlib.Path(opt("--out"))
scene = out.parent.name                       # s | s-all | d1 | d2 | renamed-heading | ...
work = out.parent
(out / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)

# --- two numbers and three ids, straight out of the nonce's own files --------
reg = [l for l in (work / "registry.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
top = len(reg)
held_n = next(i for i, l in enumerate(reg, 1) if "Held" in l)
st = [l.split(" | ")[0].strip("| ") for l in (work / "staged.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
staged = [l for l in (work / "staged.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
held = f"S{held_n:03d}"
new1 = f"S{top + 1:03d}"
new2 = f"S{top + 2:03d}"
HDR = "staged_id\tlane_id\taction\turl\n"


def append(rows: list[str]) -> None:
    (out / "append.md").write_text("".join(r + "\n" for r in rows), encoding="utf-8")


def renumber(rows: list[str]) -> None:
    (out / "renumber.tsv").write_text(HDR + "".join(rows), encoding="utf-8")


def src(rowline: str) -> str:
    return rowline.split(" | ")[1]


if scene in ("renamed-heading", "no-heading", "row-outside"):
    print(f"REFUSED registry structure ({scene})", file=sys.stderr)
    sys.exit(1)

if scene == "well-formed":
    renumber([f"{st[0]}\t{new1}\tappend\t{src(staged[0])}\n"])
    append([f"| {new1} | {src(staged[0])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |"])
    sys.exit(0)

if scene == "d1":
    renumber([f"{st[0]}\t{held}\theld\t{src(staged[0])}\n"])
    (out / "corpus" / "knowledge" / "e.md").write_text((work / "knowledge" / "corpus" / "knowledge" / "e.md").read_text(encoding="utf-8"), encoding="utf-8")
    sys.exit(0)

if scene == "d2":
    renumber([f"{st[0]}\t{held}\theld\t{src(staged[0])}\n"])
    sys.exit(0)

if scene == "s-all":
    renumber([f"{st[0]}\t{new1}\tappend\t{src(staged[0])}\n",
              f"{st[1]}\t{held}\theld\t{src(staged[1])}\n",
              f"{st[2]}\t{new2}\tappend\t{src(staged[2])}\n"])
    append([f"| {new1} | {src(staged[0])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |",
            f"| {new2} | {src(staged[2])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |"])
    sys.exit(0)

# scene == "s": source-only. a is minted, b is held, c is body-only.
a_id, b_id, c_id = st[0], st[1], st[2]
renumber([f"{a_id}\t{new1}\tappend\t{src(staged[0])}\n",
          f"{b_id}\t{held}\theld\t{src(staged[1])}\n"])
append([f"| {new1} | {src(staged[0])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |"])
entry = (work / "knowledge" / "corpus" / "knowledge" / "e.md").read_text(encoding="utf-8")
body = "".join(l + "\n" for l in entry.splitlines() if not l.startswith("source:"))
body = body.replace(a_id, new1).replace(b_id, "")
(out / "corpus" / "knowledge" / "e.md").write_text(body, encoding="utf-8")
(out / "bodyonly.tsv").write_text("entry\tstaged_id\ncorpus/knowledge/e.md\t" + c_id + "\n", encoding="utf-8")
print("BODYONLY=1")
```

Five behaviours, each faked by a one-line switch: source-only (`scene` from the dirname, `--cites` never
read), bodyonly (canned from the *third* staged row, no detection), D1 identity (the substring `Held` in a
registry row, entry identity never parsed), D2 splitter (`split(" | ")`, registry identity cell never
read), D3 (refuse on the dirname, no heading/row scan).

## 2. Shortcuts, and the leg that should have refused each

| # | Shortcut | Leak | Leg verdict |
|---|---|---|---|
| 1 | per-subtest dir names `s`,`s-all`,`d1`,`d2`,name | c1-count.py:141,158,167,174,194 fixed strings | **accepted** (forge above) |
| 2 | registry size 12–40, ids S500–S900, host `h<n>.example.test` | :122,123,126 | **accepted** (`forge-ranges.py`, adds `12<=top<=40` + `S[5-9]\d\d` + `.example.test` guard, `LEGS=5/5 C1=PASS`) |
| 3 | read the counter source at run time for the oracle | :113–116 pin/26 constants | **accepted** (`forge-src.py`, below) |
| 4 | call order, via a state file in the shared `tmp` root | one `mkdtemp`, fixed 8-call sequence | **accepted** (`forge-order.py`, keyed only on `out.parent.parent/.order`, `LEGS=5/5 C1=PASS`) |
| 5 | D3 as "second top-level heading" instead of row scoping | :188–196 four fixed shapes | **accepted** (`forge-d3heading.py`, `REGISTRY_STRUCTURE=PASS 4/4`) |
| 6 | never write `bodyclash.tsv` | `grep -c bodyclash c1-count.py` → `0` | **accepted** — claim says bodyonly/bodyclash; counter reads only bodyonly |
| 7 | garbage `append.md` / `renumber.tsv` cells | :154–156,196 check only `lstrip(" |").startswith(id)` and `[:2]` | **accepted** |
| 8 | ignore `ASSIMILATE_CITES` | env never set by the counter | **accepted** |

The three refused controls stay refused (`tool-before` 1/5, `const-tool` 1/5, `flag-noop-tool` 2/5, per
`controls/c1-before.txt`): LEGACY_ALL refuses `const` (no digest line), SOURCE_ONLY refuses `flag-noop`
(default must exclude the body-only id). Those legs work; the eight above are what they miss.

## 3. The interesting forge: the oracle read out of the counter's own source

`/proc/<ppid>/cmdline` names the counter; the forge extracts `R50_PIN` and the literal `26` from its text
and prints them without hashing fixtures or running the adopter:

```
FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43
SELFTEST=PASS findings=26 expected=26
```
`c1-count.py --tool forge-src.py --seed 7` → `LEGS=5/5 / C1=PASS / EXIT=0`. So the LEGACY_ALL oracle is a
constant in the same file the tool can read; it is not a behaviour test.

## 4. A shipped control now passes, and the control file is unpinned

`c1-count.py --tool corpus/evidence/round51/controls/echo-tool.py --seed 5` → `LEGS=5/5 / C1=PASS / EXIT=0`.
`controls/c1-before.txt` records the same control at `SOURCE_ONLY=FAIL … all_rc=2` and `LEGS=2/5`. The
recorded row cannot be reproduced at tip because echo delegates every non-selftest call to
`tools/assimilate-rows.py`, and that file gained `--cites` between revisions:
`git show 2573dc1:tools/assimilate-rows.py | grep -c -- --cites` → `0`; `2a3389d` → `7`. `c1-before.txt`
carries no revision line, so it is exactly the round-50 routed defect ("pin the revision a counter was
measured against") still open for C1.

## 5. Cheapest cheat that passes all five legs

The 94-line dirname forge. It reads two integers (registry row count; index of the `Held` row) and three
staged ids, and emits canned files. Nothing about identity, citations, or registry structure is
implemented; `--cites`, `--opened`, `--entry` are decoration.

## 6. The leg I would add (counter not edited)

**`SHAPE_NONCE`** — one leg, three cheap edits inside the existing `main`:
1. name every work dir from the run nonce instead of the scenario: `w = tmp / f"{rnd.getrandbits(24):06x}"`
   (five sites, :141,158,167,174,194); the counter's assertions never read the name.
2. one `mkdtemp` per scenario instead of one shared `tmp`, so call-order state (`out.parent.parent`) cannot
   be shared across calls.
3. one real-range run: copy `corpus/SOURCES.md` (106 rows, ids S001–S106) and a staged row `S050` →
   expect `S050\tS107\tappend`. Validated against the lane tool:
   `RC=0`, `renumber.tsv` = `S050\tS107\tappend\treal.example/doc-x`; a range-guarded forge refuses it.

Second, one-line hardening of LEGACY_ALL — **`MUTATION_SENSITIVITY`**: copy `R50_FIX`, perturb one cell
(`sed -i 's/2026-12-01/2027-01-01/' staged.md`), keep `expected.json`, require `rc!=0` and `SELFTEST=FAIL`.
Measured: lane tool → `DIFF unexpected ROWRECHECK S014 2027-01-01 … SELFTEST=FAIL findings=26 expected=26`,
`rc=1`; `echo-tool.py` → `SELFTEST=PASS … rc=0`. This kills the echo/source-reading family without touching
the pinned package (its digest is unchanged; only the scratch copy is mutated).

Also worth one assertion each, same cost: `bodyclash.tsv` present with the entry+id when a body-only id is
also a lane id; `ASSIMILATE_CITES=all` honoured with no `--cites`; `append.md` row has 11 cells and the
minted id.

## 7. Impacted axes

- **Operability**: `C1=PASS` is currently satisfiable by a tool with zero of the five behaviours, so the
  counted value is not evidence for the claim. C1's predicate is right; its measurement is not.
- **Calibration**: a shipped control (`echo-tool`) passes at tip while `controls/c1-before.txt` records it
  failing, and the control file pins no revision — the round-50 routed defect is unfixed for C1.
- **Depth / identity**: untouched by this item; nothing here bears on C2/C3.

VERDICT: attacked the frozen C1 counter — a 94-line dirname-keyed forge implementing none of the five
behaviours passes `LEGS=5/5 C1=PASS` on five seeds, as do source-reading, range-guard, call-order and
heading-count variants, so the counter is wrong; smallest safe correction is `SHAPE_NONCE` (nonce dir
names, per-scenario roots, one real-range run) plus `MUTATION_SENSITIVITY` on LEGACY_ALL.

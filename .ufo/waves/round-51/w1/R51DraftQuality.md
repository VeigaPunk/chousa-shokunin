# R51DraftQuality — QUALITY criteria 81–84 (chousa round 51, wave 1)

Seat: leaf, no dispatch. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at `cfe6c9fb9b56fa80a3005c1a3aaa522b29966306`. Read: `corpus/QUALITY.md` 73–80 (shape), `corpus/evidence/round51/{claims.md,claims-erratum.md,c1-count.py,c3-count.py}`, `controls/build-c3-controls.py`, `corpus/lessons/round-50-verifier-spotcheck.md` §6, `corpus/lessons/round-50.md` `## Mistakes`. Row numbers confirmed with `R51DraftMistakes`: 1 receipt pin · 2 counter recognises its own DIFF lines · 3 adopter default change · 4 five dangling pointers · 5 C3 tokenizer leading dot. No install, no network, no fetch; scratch in `/dev/shm/chousa-r51-R51DraftQuality/` (removed at the end).

## What I ran at the tip (counters to stdout only)

`c1-count.py` → `LEGS=5/5` `C1=PASS` rc 0 (`--seed 51`: `SOURCE_ONLY=PASS … bodyonly=[['corpus/knowledge/e.md','S582']]`); `--tool tool-before.py` → `LEGS=1/5` `C1=FAIL` rc 1; `--tool flag-noop-tool.py` → `LEGS=2/5` `C1=FAIL` rc 1; `c3-count.py` → `DANGLING=5` `C3=FAIL` rc 1; `build-c3-controls.py` (TMPDIR in scratch) → BLANKET `DANGLING=5`, DELETED `CAP_ROWS=32 POINTERS=59`, EMPTY `DANGLING=5`, all `C3=FAIL`; scratch `c3-corr-probe.py` → non-empty correction target `RESOLVED_BY_CORRECTION=1 DANGLING=4`, zero-byte and missing `=0`; scratch `clash-probe.py` (tool by hand) → `WARN …: body-only staged id S002 is also a lane id`, `bodyclash.tsv` written. Two unseeded control runs drew different nonces (`map=['S529','S764','S862']`, `map=['S528','S784','S878']`) against the frozen receipt's `['S512','S615','S781']`: the packages are generated per run, not stored.

## Draft — append at the end of `corpus/QUALITY.md` (after the trailing `74 (round-50 named limits…)` paragraph)

```
81. **A capability counter generates its own inputs at counting time from a nonce, and keeps its expected values in itself.** A
    counter that reads a package its tool's author can open is satisfiable without the behaviour: the frozen round-50 C1 counter
    searched for one literal `DIFF` line per fixed perturbation, so a tool printing all six lines for any input passed
    (`LEGS=5/5`, W2 `R50CritForgeC1`). The round-51 counter seeds from `os.urandom(8)` unless `--seed`, draws host and ids per run
    (`corpus/evidence/round51/c1-count.py:101,121-127`), hands the tool only
    `--staged/--knowledge/--registry/--opened/--out/--entry` and no expected file (`:77-83`), and keeps the expected relations as
    literals (`:155-157`) beside the fixtures pin (`:47`). Check: `python3 corpus/evidence/round51/c1-count.py [--seed N] [--tool
    PATH]` — five legs, exit 0 `LEGS=5/5` `C1=PASS`; exit 1 on any leg failing; exit 2 `PIN_CHANGED` when the round-50 fixture
    package no longer hashes to the pin. Shown able to fail (ran at the tip, `--tool`): `tool-before.py` `LEGS=1/5`,
    `flag-noop-tool.py` `LEGS=2/5`, each `C1=FAIL` rc 1; `corpus/evidence/round51/controls/c1-before.txt` records the same for
    `tool-before`/`echo`/`const`/`flag-noop`. Named limits: with `--tool` the SELFTEST_DEFAULT leg is skipped and counted as
    passing, so a control starts at 1/5; a tool that reimplements the adopter passes by definition; the nonce legs test the
    adopter's interface on generated packages, never the lane entries. — `corpus/lessons/round-51.md` `## Mistakes` row 2;
    `corpus/evidence/round51/claims.md` R51-C1; round-50 spot-check routed defect 2.

82. **An adopter cites only `source:` ids and lists the ids it leaves in the body.** A default that renumbers every id token turns
    a prose mention into a row for an unrelated document; round 50 answered with a check, round 51 makes the reading the default,
    so the earlier one-shot counters needed the old mode by name. The default cites the ids on `source:` lines, leaves a body-only
    id unchanged in the entry text and lists it in `bodyonly.tsv` with `BODYONLY=<n>`; `--cites all` (env `ASSIMILATE_CITES=all`)
    keeps the round-49/50 reading. Check: `python3 corpus/evidence/round51/c1-count.py` — the SOURCE_ONLY leg requires
    `renumber.tsv` to hold exactly the two `source:` ids (`append` to the registry maximum + 1, `held` to the row carrying the
    URL), `append.md` one row, the body-only id present in the rewritten entry, both cited ids absent from it, `bodyonly.tsv`
    equal to `[["corpus/knowledge/e.md", <body id>]]`, `BODYONLY=1`, and the `--cites all` run to renumber all three and append
    two; `LEGS=5/5` exit 0. Shown able to fail (ran at the tip): `flag-noop-tool.py` (accepts `--cites`, ignores it)
    `SOURCE_ONLY=FAIL default_rc=0 map=['S528','S784','S878'] appended=2 bodyonly=[]`, `LEGS=2/5`; `tool-before.py` `LEGS=1/5`.
    Named limits: `bodyclash.tsv` (a body-only staged id that is also a lane id, `tools/assimilate-rows.py:441-447`) is reached by
    no leg — the counter's staged ids are S500–S900 and its lane ids ≤ S040 (`c1-count.py:121-127`), disjoint by construction, and
    I reached the branch only by hand (`WARN` + `bodyclash.tsv` on staged S002 against registry S002); an id the adopter does not
    renumber still passes unseen (QUALITY 77's limit). — `corpus/lessons/round-51.md` `## Mistakes` row 3;
    `corpus/evidence/round51/claims.md` R51-C1; QUALITY 77.

83. **A self-assessment pointer resolves, or carries a `correction:` line naming a non-empty target.** Five pointers in
    `SCORECARD.md` capability rows and `SHONEN.md` evidence lines name paths the tree does not hold, and no criterion read them.
    Check: `python3 corpus/evidence/round51/c3-count.py [--root LANE]` — `CAP_ROWS=n (base 36)`, `POINTERS=n (base 74)`,
    `RESOLVED_BY_CORRECTION=n`, one `DANGLING <file>:<line> <pointer>` per unresolved pointer, `DANGLING=n`, `C3=PASS` exit 0 only
    when `DANGLING=0` and neither count fell below base. A pointer resolves when `<lane>/<pointer>` is a non-empty file or a
    directory holding a file, or a later `correction: SCORECARD.md:<row line> <pointer> -> <path>` line names that row and an
    existing non-empty `<path>`. Shown able to fail (ran at the tip): `DANGLING SCORECARD.md:1843 measure/final/`, `:2073
    measure-l1/c1-s36361.json`, `:2074 measure-l1/c2-s36371.json`, `:2616 c1-supplement.py`, `DANGLING SHONEN.md:10
    round25-meta-differential.log`, `DANGLING=5 C3=FAIL` rc 1; `controls/build-c3-controls.py` (ran) prints BLANKET `DANGLING=5`,
    DELETED `CAP_ROWS=32 POINTERS=59`, EMPTY `DANGLING=5`, all `C3=FAIL`. Correction branch (ran, scratch roots): non-empty target
    `RESOLVED_BY_CORRECTION=1 DANGLING=4`; zero-byte and missing targets `=0`. Named limits: existence, not truth; the three
    controls prove failure modes only and never a valid correction (my probe is not a round artefact); a `correction:` line names
    a line number, so an edit that shifts the row invalidates it; the counter's own tokenizer produced three of the first eight
    `DANGLING` lines (row 5) — extraction is part of the predicate. — `corpus/lessons/round-51.md` `## Mistakes` rows 4 and 5;
    `corpus/evidence/round51/claims.md` R51-C3; `corpus/evidence/round51/claims-erratum.md` E1.

84. **A receipt names the tool revision it was measured against, and the tip still carries that tool.** The round-50
    after-measurement opened "at the working tree before the final commit" and named no hash, and the `SKILL.md` Gates row named
    candidate `ec52e632`, not the landed tip, so neither could be tied to code. Check: `python3
    corpus/evidence/round51/receipt-check.py <receipt> [...] [--root LANE] [--tip REV] [--skill SKILL.md]` — a receipt's first
    five lines must carry `tool-rev: <40-hex> tool: <lane-relative path> [digest: sha256:<64-hex>]`; `RECEIPT_NO_REV`,
    `RECEIPT_REV_UNKNOWN`, `RECEIPT_REV_UNLANDED` (not an ancestor of the tip), `RECEIPT_TOOL_ABSENT`, `RECEIPT_TOOL_MOVED` (the
    tool's blob at the tip differs from its blob at that revision), `RECEIPT_DIGEST_MISMATCH`, else `RECEIPT_OK`; `CHECKS=n OK=n
    FAILS=n` (the skill line is a check), `RECEIPT_CHECK=PASS` exit 0, exit 1 on any failure, exit 2 when the root is not a git work tree. Shown able to fail
    (ran): the filed round-50 receipt and the current Gates row print `RECEIPT_NO_REV corpus/evidence/round50/measure-after.txt`
    and `SKILL_NO_PIN SKILL.md`, `FAILS=2` rc 1; scratch receipts print `RECEIPT_REV_UNKNOWN … rev=000…0`, `RECEIPT_REV_UNLANDED …
    rev=1fce006153ab`, `RECEIPT_TOOL_MOVED … rev=d603f6f00f78 tool=corpus/evidence/round51/c3-count.py` (the erratum changed that
    blob), `RECEIPT_DIGEST_MISMATCH recorded=000000000000 actual=94ddc7dc273c`, `RECEIPT_TOOL_ABSENT`; a header naming the tip and
    that blob's digest prints `RECEIPT_OK … rev=cfe6c9fb9b56`, `RECEIPT_CHECK=PASS` rc 0. Named limits: the header is a
    convention, not a signature — a receipt can name a revision it did not run at; only the first five lines are read; a receipt
    measuring a tree count has no header form here; the digest leg hashes the blob, not the tool's behaviour; receipts filed
    before round 51 stay as filed (append-only) and fail this check by construction. — `corpus/lessons/round-51.md` `## Mistakes`
    row 1; `corpus/evidence/round51/claims.md` freeze section; round-50 spot-check routed defect 1.
```

## Draft — `corpus/evidence/round51/receipt-check.py` (L1 integrates; this round's after-receipt and Gates row take the header)

```python
#!/usr/bin/env python3
"""receipt-check — a receipt names the tool revision it was measured against, and that revision
still carries the tool (QUALITY 84, round 51).

Header form, in a receipt's first five lines or in a `SKILL.md` Gates table row:
    tool-rev: <40-hex commit> tool: <lane-relative path> [digest: sha256:<64-hex>]
Per receipt: RECEIPT_NO_REV (no header — the round-50 class, a prose header naming no hash,
`corpus/evidence/round50/measure-after.txt:1`); RECEIPT_REV_UNKNOWN (commit not in the lane
repo); RECEIPT_REV_UNLANDED (not an ancestor of the tip); RECEIPT_TOOL_ABSENT;
RECEIPT_TOOL_MOVED (the tool's blob at the tip differs from its blob at the named revision —
the receipt measures code the tip no longer has); RECEIPT_DIGEST_MISMATCH; else RECEIPT_OK.
`--skill SKILL.md` applies the same test to the header in the Gates row (`SKILL_PIN_OK`,
`SKILL_NO_PIN`, or the failing line). Output: one line per receipt, the optional skill line,
`CHECKS=n OK=n FAILS=n` (the skill line counts as a check), `RECEIPT_CHECK=PASS|FAIL`. Exit 0 pass · 1 any failure · 2 root
not a git work tree. Usage: python3 corpus/evidence/round51/receipt-check.py <receipt> [...]
[--root LANE] [--tip REV] [--skill SKILL.md]. Named limits: the header is a convention, not a
signature — a receipt can name a revision it did not run at and this check cannot tell; only
the first five lines are read; a receipt measuring a tree count has no header form here; the
digest leg hashes the blob, not behaviour.
"""

from __future__ import annotations

import argparse, hashlib, pathlib, re, subprocess, sys

LANE = pathlib.Path(__file__).resolve().parents[3]
HEAD_RE = re.compile(
    r"(?:#\s*)?tool-rev:\s*([0-9a-f]{40})\s+tool:\s*([A-Za-z0-9._/-]+)(?:\s+digest:\s*sha256:([0-9a-f]{64}))?"
)


def git(root: pathlib.Path, *args: str) -> tuple[int, bytes]:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    return p.returncode, p.stdout


def pin(root: pathlib.Path, tip: str, label: str, rev: str, tool: str, want: str | None) -> tuple[bool, str]:
    if git(root, "cat-file", "-e", f"{rev}^{{commit}}")[0] != 0:
        return False, f"RECEIPT_REV_UNKNOWN {label} rev={rev}"
    if git(root, "merge-base", "--is-ancestor", rev, tip)[0] != 0:
        return False, f"RECEIPT_REV_UNLANDED {label} rev={rev[:12]}"
    rc_a, at_rev = git(root, "rev-parse", f"{rev}:{tool}")
    if rc_a != 0:
        return False, f"RECEIPT_TOOL_ABSENT {label} rev={rev[:12]} tool={tool}"
    rc_b, at_tip = git(root, "rev-parse", f"{tip}:{tool}")
    if rc_b != 0 or at_rev.strip() != at_tip.strip():
        return False, f"RECEIPT_TOOL_MOVED {label} rev={rev[:12]} tool={tool}"
    if want:
        rc_c, blob = git(root, "cat-file", "blob", f"{rev}:{tool}")
        got = hashlib.sha256(blob).hexdigest() if rc_c == 0 else ""
        if got != want:
            return False, f"RECEIPT_DIGEST_MISMATCH {label} recorded={want[:12]} actual={got[:12]}"
    return True, f"RECEIPT_OK {label} rev={rev[:12]} tool={tool}"


def header(path: pathlib.Path) -> re.Match | None:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:5]:
        m = HEAD_RE.search(line)
        if m:
            return m
    return None


def one(root: pathlib.Path, tip: str, path: pathlib.Path, nopin: str, ok_label: str) -> bool:
    m = header(path)
    if m is None:
        print(f"{nopin} {path}")
        return False
    good, line = pin(root, tip, str(path), m.group(1), m.group(2), m.group(3))
    print(line if ok_label == "RECEIPT_OK" else line.replace("RECEIPT_OK", ok_label))
    return good


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("receipts", nargs="*")
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--tip", default="HEAD")
    ap.add_argument("--skill", help="also require the Gates registry row to carry the header form")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    if git(root, "rev-parse", "--show-toplevel")[0] != 0:
        print(f"ROOT_NOT_GIT {root}")
        return 2
    ok = fails = 0
    for r in a.receipts:
        good = one(root, a.tip, pathlib.Path(r), "RECEIPT_NO_REV", "RECEIPT_OK")
        ok += good
        fails += not good
    if a.skill:
        fails += not one(root, a.tip, pathlib.Path(a.skill), "SKILL_NO_PIN", "SKILL_PIN_OK")
    checks = len(a.receipts) + (1 if a.skill else 0)
    print(f"CHECKS={checks} OK={checks - fails} FAILS={fails}")
    print(f"RECEIPT_CHECK={'PASS' if fails == 0 else 'FAIL'}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

## Receipt-check evidence (the exact script above, run from a scratch copy, `--root .`)

```
$ python3 $S/receipt-check.py --root . corpus/evidence/round50/measure-after.txt --skill SKILL.md
RECEIPT_NO_REV corpus/evidence/round50/measure-after.txt
SKILL_NO_PIN SKILL.md
CHECKS=2 OK=0 FAILS=2 / RECEIPT_CHECK=FAIL                       (rc=1)
$ python3 $S/receipt-check.py --root . $S/fx/good.txt --skill $S/fx/SKILL-pin.md
RECEIPT_OK …/good.txt rev=cfe6c9fb9b56 tool=corpus/evidence/round51/c1-count.py
SKILL_PIN_OK …/SKILL-pin.md rev=cfe6c9fb9b56 tool=corpus/evidence/round51/c1-count.py
CHECKS=2 OK=2 FAILS=0 / RECEIPT_CHECK=PASS                       (rc=0)
$ python3 $S/receipt-check.py --root . $S/fx/{norev,unknown,unlanded,moved,mismatch,absent}.txt
RECEIPT_NO_REV …/norev.txt
RECEIPT_REV_UNKNOWN …/unknown.txt rev=0000000000000000000000000000000000000000
RECEIPT_REV_UNLANDED …/unlanded.txt rev=1fce006153ab
RECEIPT_TOOL_MOVED …/moved.txt rev=d603f6f00f78 tool=corpus/evidence/round51/c3-count.py
RECEIPT_DIGEST_MISMATCH …/mismatch.txt recorded=000000000000 actual=94ddc7dc273c
RECEIPT_TOOL_ABSENT …/absent.txt rev=cfe6c9fb9b56 tool=corpus/evidence/round51/nope.py
CHECKS=6 OK=0 FAILS=6                                              (rc=1)
```

Green path = a header naming the tip and the blob's digest (`git cat-file blob HEAD:corpus/evidence/round51/c1-count.py | sha256sum` → `94ddc7dc273c8314…`); `--root /dev/shm` prints `ROOT_NOT_GIT /dev/shm` rc 2. The `RECEIPT_TOOL_MOVED` fixture is real: `d603f6f` carries c3-count.py blob `6d8b014d0c39…`, the tip `e7ab3d85be61…`.

## Findings and out-of-scope

- C1 is `LEGS=5/5` at the tip; C3 is `DANGLING=5`, so 83's red state is the tip's, not a fixture's.
- The round's three C3 controls never exercise a *valid* `correction:` line; I ran that leg in scratch (`RESOLVED_BY_CORRECTION=1`) so 83's green path is not asserted blind.
- `bodyclash.tsv` is unexercised by C1, reached only by hand — 82's named limit, not a pass.
- `controls/c3-controls.txt` (filed at the freeze) carries the pre-erratum `DANGLING=8` names; `c3-controls-erratum.txt` is the corrected receipt, and 83 quotes the erratum's 5.
- Own slip, disclosed: the EMPTY-TARGET leg of my `c3-corr-probe.py` wrote a zero-byte file through the scratch root's `corpus` symlink into the lane (`corpus/evidence/round51/zero.txt`, 0 bytes, 20:29); removed at once — `git status --porcelain` now shows only this report and the wave directory. A successor probe must copy `corpus` or use a real root. Two counter runs also used the default `TMPDIR` before I pinned it to scratch.
- Out of scope: no edit to `corpus/QUALITY.md`, `SKILL.md`, any receipt, counter or entry, the git index or jj state; no `c2-count.py` run; no network.

VERDICT: drafted and first-falsified QUALITY 81–84 — every check ran at the tip and every red path
was observed (C1 controls 1/5 and 2/5; C3 `DANGLING=5` plus three controls; the new receipt check
red on the round-50 receipt and current Gates row, green only on a pinned fixture) — text only.

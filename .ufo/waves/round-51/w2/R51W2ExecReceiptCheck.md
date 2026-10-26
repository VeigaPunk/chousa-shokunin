# R51W2ExecReceiptCheck — receipt dry-run for what round 51 will file

author: R51W2ExecReceiptCheck · date: 2026-10-25 · leaf seat; only this file written. Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin` at HEAD `72566c84e4184846ff9cbc4c92bc33b8291bc53b` (wave-2
dispatch); the receipt pins `4436e279b91d8d68fd439c9095695035fbeeab74`, an ancestor. No install; no lane file,
index or jj write. Scratch `/dev/shm/chousa-r51-R51W2ExecReceiptCheck/` deleted at end.

## 1. Builder script and the receipt it produced

Intended lane path: `corpus/evidence/round51/measure-after.txt` — **absent at the tip** (§7.1). Ran as `bash
make-receipt.sh /dev/shm/…/lane-at-tip /dev/shm/…/receipt-final.txt`; `lane-at-tip` is a `git clone --shared` of
the lane at `4436e27` (`git status --porcelain` empty) because the counters read history (`measure-r50-at-tip.txt:4`).

```bash
#!/usr/bin/env bash
# usage: make-receipt.sh LANE OUT   -- line 1 = tool pin; then every frozen counter, command + verbatim output
set -u
L=${1:?usage: make-receipt.sh LANE OUT}
OUT=${2:?usage: make-receipt.sh LANE OUT}
REV=$(git -C "$L" rev-parse HEAD); TOOL=tools/assimilate-rows.py
S=/dev/shm/chousa-r51-R51W2ExecReceiptCheck; mkdir -p "$S/tmp"; export TMPDIR="$S/tmp"
DIG=$(git -C "$L" cat-file blob "$REV:$TOOL" | sha256sum | cut -d' ' -f1)
{
  printf 'tool-rev: %s tool: %s digest: sha256:%s\n' "$REV" "$TOOL" "$DIG"
  for c in c1-count.py c1-supplement.py c2-count.py c3-count.py; do
    printf '\n$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/%s\n' "$c"
    ( cd "$L" && env -u ASSIMILATE_CITES python3 "corpus/evidence/round51/$c" )
    printf 'exit=%d\n' "$?"
  done
  printf '\n# tree: %s; %s changes in `git status --porcelain`\n' "$REV" "$(git -C "$L" status --porcelain | wc -l)"
  printf '# nonce: the unseeded c1-count.py SOURCE_ONLY map line is generated per run (fresh hosts/ids); every other line reproduced across runs, and a `--seed N` run is byte-identical across reruns.\n'
} > "$OUT"
```

Draft receipt (59 lines; `$` lines are the commands actually executed, from the lane root):

```text
tool-rev: 4436e279b91d8d68fd439c9095695035fbeeab74 tool: tools/assimilate-rows.py digest: sha256:6b975f91c809485c8d03e6134e2a17bdb7f9079c22218d74e9321a14632572f6

$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py
SELFTEST_DEFAULT=PASS
LEGACY_ALL=PASS rc=0
SOURCE_ONLY=PASS default_rc=0 map=['S816', 'S860'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S507']] all_rc=0 all_map=['S507', 'S816', 'S860']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY renamed-heading rc=1 -> PASS
REGISTRY no-heading rc=1 -> PASS
REGISTRY row-outside rc=1 -> PASS
REGISTRY well-formed rc=0 -> PASS
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
C1=PASS
exit=0

$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py
SHAPE=PASS 3/3
MUTATION=PASS 3/3
CROSS_ENTRY=PASS 3/3
SOURCE_LINE=PASS 3/3
UNKNOWN_SRC=PASS 3/3
CLASH=PASS 3/3
SUPPLEMENT_LEGS=6/6
C1_SUPPLEMENT=PASS
exit=0

$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py
ENTRIES=3/3
BOUND=6/7 (min 5) REFUSED=1
BOUND_IDS=S107,S108,S109,S110,S111,S112
REF_ID_UNBOUND=0
NEW_GROUND=3/3
QUOTE_ROWS=61 ON_BOUND=61/61
SPAN_IDS=6/6 (min 3 each)
QUOTES_IN_SPAN=61/61
QUOTES_IN_ENTRY=61/61
QUOTES_IN_LESSON=61/61
QUOTE_SHORT=61/61
SPAN_CONTEXT=61/61
CAPTURE_BOUND=61/61
SUBSTANCE=PASS
ANCHOR_BOUND=6/6
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
exit=0

$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c3-count.py
CAP_ROWS=36 (base 36)
POINTERS=74 (base 74)
RESOLVED_BY_CORRECTION=4
DANGLING=0
C3=PASS
exit=0

# tree: 4436e279b91d8d68fd439c9095695035fbeeab74; 0 changes in `git status --porcelain`
# nonce: the unseeded c1-count.py SOURCE_ONLY map line is generated per run (fresh hosts/ids); every other line reproduced across runs, and a `--seed N` run is byte-identical across reruns.
```

The same counters in the dirty worktree reproduce the 56-line body except one line (`SOURCE_ONLY … map=['S512',
'S900'] bodyonly=[['corpus/knowledge/e.md', 'S865']]` vs `S816/S860/S507`; `diff` = 2 lines); `--seed 51` twice is
byte-identical (`diff` silent) — hence the nonce note.

## 2. The assigned check, verbatim

```
$ python3 …/round51/receipt-check.py --root …/chousa-shokunin …/receipt-final.txt --skill …/chousa-shokunin/SKILL.md
RECEIPT_OK /dev/shm/chousa-r51-R51W2ExecReceiptCheck/receipt-final.txt rev=4436e279b91d tool=tools/assimilate-rows.py
SKILL_NO_PIN /home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md
CHECKS=2 OK=1 FAILS=1
RECEIPT_CHECK=FAIL
exit=1
```

`RECEIPT_OK` as expected; `SKILL_PIN_OK` is **not** printed although `SKILL.md:130` (the `assimilate-rows` row,
char 2416) carries `tool-rev: cf642c66… tool: tools/assimilate-rows.py digest: sha256:6b975f91…`. The skill leg
never reads that row: `receipt-check.py:56-57` takes `splitlines()[:5]` of `--skill`, and `:91` uses the same
`header()`. That header moved to line 1 of a copy prints `SKILL_PIN_OK … rev=cf642c669b73`, and the pin is sound:
`cf642c6:tools/assimilate-rows.py` = `4436e27:…` = `d1483e793d3f728ae9668965988b44505bd0e691` (`6b975f91…`).

## 3. Perturbations — every named code fires

Each scratch receipt run as `python3 corpus/evidence/round51/receipt-check.py --root . FILE`:

| perturbed receipt | observed | exit |
|---|---|---|
| digest changed (last / first nibble) | `RECEIPT_DIGEST_MISMATCH … recorded=6b975f91c809 actual=6b975f91c809` / `recorded=0b975f91c809 actual=6b975f91c809` | 1 |
| unlanded rev (`c186fecb…`: `cat-file -e` ok, `merge-base --is-ancestor … HEAD` rc 1) | `RECEIPT_REV_UNLANDED … rev=c186fecb97c7` | 1 |
| tool moved since `9ec1751a` (base; blob `b06098cd` vs tip `d1483e79`) | `RECEIPT_TOOL_MOVED … rev=9ec1751a2423 tool=tools/assimilate-rows.py` | 1 |
| rev 40×`f` | `RECEIPT_REV_UNKNOWN … rev=ffffffff…` | 1 |
| tool `tools/not-in-tree.py` | `RECEIPT_TOOL_ABSENT … tool=tools/not-in-tree.py` | 1 |
| no header / line 6 / line 5 | `RECEIPT_NO_REV` / `RECEIPT_NO_REV` / `RECEIPT_OK` | 1/1/0 |
| `--root` = non-git scratch dir | `ROOT_NOT_GIT DIR` (only line) | 2 |

Precedence matches the docstring (`pin()` at `:37-50`: unknown → unlanded → absent → moved → digest). Defects: the
12-char truncation makes a last-nibble error print `recorded == actual`; a missing path ends in `FileNotFoundError`
(exit 1) — no named line, no `CHECKS=` summary.

## 4. Can the header be satisfied by naming a revision it never ran at?

Yes, cheaply. `pin()` (`:37-50`) tests only: commit exists, is an ancestor of the tip, contains the named tool,
and its blob at that revision equals its blob at the tip (plus optionally the rev-blob digest); nothing reads the
body. Observed: header only → `RECEIPT_OK` exit 0; header plus `fake body: C1=PASS C2=PASS C3=PASS` → `RECEIPT_OK`
exit 0; header naming the tip tool **plus the real output of `c1-count.py --tool controls/tool-before.py`**
(`LEGS=1/5`, `C1=FAIL`) → `RECEIPT_OK` exit 0. The `digest:` leg is optional, and a `cf642c6` header passes too.
It binds bytes at a revision, not a run (`QUALITY.md:898-910`) — credibility rests on commands and the tree line.

## 5. open-items-age: PASS at 51, FAIL at 8 rounds

Draft report line: `Open operator items: 8d77e6c1 since round 42 (9 rounds)`
```
$ python3 …/open-items-age.py draft-51.txt --round 51
OPEN_ITEMS_AGE=PASS since=42 rounds=9                                    (exit 0)
$ python3 …/open-items-age.py draft-50.txt --round 51      # file holds "(8 rounds)"
OPEN_ITEMS_AGE=FAIL expected a line beginning: Open operator items: 8d77e6c1 since round 42 (9 rounds)   (exit 1)
```

`LOG.md:1494` is `## Round 42`, `:1499` the first line naming the id; 51 − 42 = 9; matching is an exact prefix, so
a bulleted line fails. Scratch-lane probes: an earlier `## Round 41` line saying "not 8d77e6c1" shifts `since` to
41 and fails the truthful 42 line; presence-only matching PASSes the line even inside a fenced block.

## 6. Replay from committed bytes; one env-hermeticity defect

Clean clone at `4436e27`: `C1`, `C1_SUPPLEMENT`, `C2`, `C3` PASS, each exit 0; body identical to the worktree run
except the c1 nonce line; `--seed 51` stable. But `c1-count.py` is not hermetic — ambient `ASSIMILATE_CITES=all`
(the tool's supported default, `tools/assimilate-rows.py:331,336`) flips it:

```
$ ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py --root .
SELFTEST_DEFAULT=FAIL
SOURCE_ONLY=FAIL default_rc=0 map=['S622','S653','S870'] appended=2 bodyonly=[]   (other legs unchanged)
LEGS=3/5
C1=FAIL                                          (exit 1)
```

`c1-count.py:60` launches the tool with the inherited environment (no `env=`); the post-freeze `c1-supplement.py:46`
strips it and `:6-8` names this flip among the frozen counter's three defects. `env -u ASSIMILATE_CITES` is
load-bearing: a grader with it exported gets `C1=FAIL` on an unchanged tree. Fix: a clean env for the child.

## 7. Calibration findings at the tip

1. `SKILL.md:133` and `round-51.md:27` say the receipt at `corpus/evidence/round51/measure-after.txt` opens with a `tool-rev:` header and passes `receipt-check.py`; it is absent at the tip (`git cat-file -e 4436e27:corpus/evidence/round51/measure-after.txt` → `fatal: path … does not exist`, exit 128; `git ls-tree 4436e27 corpus/evidence/round51/` has no entry). The §1 draft is that artifact; both sentences are false until it lands.
2. `SKILL.md:133` cites "E1-E4" and `c1-supplement.py:4` "E2-E4"; the tip file has one section (`grep -c '^## E'` → 1, 29 lines, E1 only).
3. The Gates pin is text only (`SKILL.md:130`), which `--skill` cannot read; the Done claim ("the `SKILL.md` rows carry the pin", `round-51.md:27`) is not demonstrated — the check prints `SKILL_NO_PIN`.
4. `receipt-check.py` has no committed control (`controls/` holds c1/c2/c3 fixtures and tool variants); w1's `SKILL_PIN_OK` came from a synthetic `$S/fx/SKILL-pin.md` (`R51DraftQuality.md:191`).

## 8. Suggested change inside `receipt-check.py` (draft only, not applied)

```python
def header(path: pathlib.Path, scan_all: bool = False) -> re.Match | None:   # the Gates row is at line 130
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in (lines if scan_all else lines[:5]):
        m = HEAD_RE.search(line)
        if m:
            return m
    return None

def one(root, tip, path, nopin, ok_label, scan_all=False, missing="RECEIPT_UNREADABLE"):
    if not path.is_file():
        print(f"{missing} {path}"); return False
    m = header(path, scan_all)   # main passes scan_all=True for the skill leg
```

Then `--skill SKILL.md` finds the line-130 header and prints `SKILL_PIN_OK … rev=cf642c669b73` (verified by moving
it to line 1 of a copy), and a missing path prints `RECEIPT_UNREADABLE` instead of a traceback. Caveat: a whole-file
scan takes the first header, so a later row pinning another tool needs a row address; today there is one.

## 9. What holds, and hygiene

Holds: `RECEIPT_OK` exit 0 on the lane root and on a clean clone; every named failure code reachable by a one-line
perturbation; `ROOT_NOT_GIT` returns 2 alone; all four counters pass at `4436e27` from committed bytes only; c2/c3
bodies byte-stable across trees, c1 stable under `--seed`; the open-items line passes at 51, fails at 8 rounds. Files
changed: this report only (scratch clones removed; no lane, index, jj or fleet write). No tool installed.

VERDICT — attacked the receipt dry-run: `RECEIPT_OK` exit 0 on the pinned receipt; `--skill` prints `SKILL_NO_PIN`
although `SKILL.md:130` carries a valid pin, because `header()` reads only five lines; every named failure code
fires; a receipt can be header-only, carry foreign-tool output, or name a revision it never ran at;
`open-items-age` PASSes at 51 and FAILs at 8 rounds; the frozen `c1-count.py` fails `C1` under ambient
`ASSIMILATE_CITES=all`; and `measure-after.txt` plus errata E2-E4 are missing at the tip.

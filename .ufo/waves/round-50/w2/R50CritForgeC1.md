# R50CritForgeC1 — C1 freeze forged: the counter certifies recognition, not adoption

Seat: critic, wave 2 (falsify). Target: frozen R50-C1 and `corpus/evidence/round50/c1-count.py` (never edited). Scratch `/dev/shm/chousa-r50-R50CritForgeC1/`, deleted at end. No install, no network.

## Result — four tools pass `c1-count.py --tool <mine>` without running the adopter on the fixtures

`python3 corpus/evidence/round50/c1-count.py --tool <tool>`, exit 0 for each; each prints `BASELINE=PASS rc=0 findings=26`, `PERTURB_PASS=6/6`, `EXPECTED_BAD=PASS rc=2`, `R49_REGRESSION=PASS rc=0`, `LEGS=5/5`, `C1=PASS`:

- `forge-tool.py` — digest==PIN → PASS; else six literal markers → the six DIFF lines.
- `order-tool.py` — reads **nothing**; answers by call ordinal within the counter process (state keyed on `getppid()`).
- `alllines-tool.py` — **never distinguishes** the perturbations: any non-pin digest → print all six DIFF lines, exit 1.
- `selfpin-tool.py` — forge-tool, but reads `PIN` from `c1-count.py:48` at run time: re-pinning is not a defence.

Same mode, real vs forged tool, counter output byte-identical: `--tool tools/assimilate-rows.py` and `--tool alllines-tool.py` into two files, `diff` → no output, rc 0. No-flag (scored) mode is forgeable too: `--root <scratch>` with the cheat at `<root>/tools/assimilate-rows.py` (delegating only the `--fixtures`-less lane default) prints `SELFTEST_DEFAULT=PASS … LEGS=5/5 C1=PASS`, exit 0.

## The cheapest cheat that passes all legs

`alllines-tool.py` (42 lines, no fixture parsing beyond the digest; scratch only, never a lane file):

```python
#!/usr/bin/env python3
import hashlib, json, os, pathlib, sys
REAL = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py")
if "--selftest" not in sys.argv:
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
PIN = "c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43"
DIFFS = ["DIFF missing COLLISIONS S011,S012",
         "DIFF missing MAP S012->S001 held",
         "DIFF missing STRIPPED S015 cell6-pipe",
         "DIFF unexpected TOOLEXIT 1",
         "DIFF unexpected ROWUSEDBY S014 corpus/knowledge/a.md, corpus/knowledge/b.md",
         "DIFF missing MAP S013->S015 append"]
fix = pathlib.Path(sys.argv[sys.argv.index("--fixtures") + 1]) if "--fixtures" in sys.argv else None
if fix is None:
    os.execv(sys.executable, [sys.executable, str(REAL), *sys.argv[1:]])
try:
    json.loads(pathlib.Path(sys.argv[sys.argv.index("--expected") + 1]).read_text(encoding="utf-8"))
except Exception:
    print("SELFTEST=ERROR expected unparseable"); sys.exit(2)
h = hashlib.sha256()
for q in sorted(x for x in fix.rglob("*") if x.is_file()):
    h.update(q.relative_to(fix).as_posix().encode() + b"\0" + q.read_bytes() + b"\0")
dig = h.hexdigest(); print("FIXTURES_SHA256=" + dig)
if dig == PIN:
    print("SELFTEST=PASS findings=26 expected=26"); sys.exit(0)
print("\n".join(DIFFS)); sys.exit(1)
```

PASS output (`python3 corpus/evidence/round50/c1-count.py --tool /dev/shm/.../alllines-tool.py`, exit 0):

```
SELFTEST_DEFAULT=PASS (skipped: --tool)
BASELINE=PASS rc=0 findings=26
PERTURB P1 applied=1 rc=1 -> PASS
PERTURB P2 applied=1 rc=1 -> PASS
PERTURB P3 applied=1 rc=1 -> PASS
PERTURB P4 applied=1 rc=1 -> PASS
PERTURB P5 applied=1 rc=1 -> PASS
PERTURB P6 applied=1 rc=1 -> PASS
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
R49_REGRESSION=PASS rc=0
LEGS=5/5
C1=PASS
```

## Why each leg lets it through

- `c1-count.py:120` — `hit = applied and rc == 1 and re.search(pat, out, re.M) is not None`: a leg asks only whether *its own* DIFF line appears; nothing requires the other five to be absent, so printing all six passes all six. The predicate (`claims.md:26`, "names the perturbed finding in a `DIFF` line") is equally satisfied by naming every finding: the hole is in the frozen predicate, and the counter implements it faithfully.
- `c1-count.py:106-112` — P1-P6 are six fixed literals on a pinned package, and `claims.md:27-30` publishes them, so the recognizer is writable before any candidate runs.
- `c1-count.py:48,100` — the pin is a constant the tool itself prints; `selfpin-tool.py` reads it from the counter.
- `c1-count.py:93` — with `--tool` the lane-default leg is set True unmeasured, leaving only two content-blind legs.
- `c1-count.py:140` — the round-49 leg falls to one line of `os.execv` delegation; it measures the delegated tool.

## Shortcuts tried that a leg refused

- `const-tool.py` → `BASELINE=FAIL` (no `FIXTURES_SHA256` line), `controls/c1-before.txt:35-45`; not rerun by me.
- `echo-tool.py` → `PERTURB 0/6`, rc 0 not 1, `controls/c1-before.txt:19-29`; not rerun by me.
- `alllines-tool.py` **v1**, before the expected-file guard: `EXPECTED_BAD=FAIL rc=1`, `LEGS=4/5`, `C1=FAIL` — one `json.loads` fixes it; that leg is the only thing the bad-expected check buys.
- `order-tool.py` on a nonce perturbation: fresh state → `SELFTEST=PASS` rc 0 (no DIFF); call 9 → `DIFF missing COLLISIONS S011,S012`. Both refused by the expected `ROWRECHECK … <nonce>` line.

## The perturbation P7 that would catch all four

Nonce drawn at count time into S014's `recheck` cell; the expected DIFF **set** required, not searched. Real tool, observed on such a copy (`nonce=re-verify-9f3c2a`, `--fixtures /dev/shm/.../p7`), rc 1:

```
DIFF missing ROWRECHECK S014 2026-12-01
DIFF missing STRIPPED S014 recheck
DIFF unexpected ROWRECHECK S014 re-verify-9f3c2a
SELFTEST=FAIL findings=25 expected=26
```

`forge-tool.py` on that copy printed only `DIFF unexpected TOOLEXIT 0` (rc 1) — no nonce, refused. Draft for the **round-51 successor counter** (not applied this round; the freeze forbids it) — `corpus/evidence/round50/c1-count.py`:

```python
("P7", lambda d, n: edit(d / "staged.md", "2026-12-01 — re-verify after release", n),
 r"^DIFF unexpected ROWRECHECK S014 " + re.escape(nonce) + r"$")
# and in the hit test: set(diff_lines(out)) == EXPECTED_SET[name]
```

with `nonce = "re-verify-" + secrets.token_hex(4)` and the copy's `expected.json` rewritten with the nonce substituted (the P5 branch already rewrites files in `tmp`). Exclusivity kills `alllines-tool`; the nonce kills digest-, order- and literal-keyed tools. Residual: a tool that embeds the pin bytes and *diffs* the copy still passes; only run-time-generated fixtures with a counter-side oracle close that class, at the cost of the hand-written expected file the freeze keeps.

## Calibration — what this does and does not say

The lane's C1 number is not inflated: `tools/assimilate-rows.py:213-232` (`selftest`) runs `observe()` as a child adopter and compares multisets, and the real tool prints `LEGS=5/5 C1=PASS` on its own bytes (I ran it, exit 0). What fails is the counter's power to certify *any other* tool: C1 as frozen cannot separate an adopter from a recognizer in either mode, so it cannot gate a round-51 candidate nor support "operability" as capability. Impacted axis: operability (C1 measurement) and calibration; depth (C2) untouched by this seat.

## Not done / limits

No lane file, counter, fixture or control edited; no campaign tool in `/home/vgpnk/Projects/shokuknow` run; a diff-transcribing cheat is argued, not run; `R49`-leg forgery by canned outputs is [INFERENCE] from the fixed literals at `round49/c1-count.py:290-320`, not demonstrated.

VERDICT — attacked the frozen R50-C1 counter's discriminating power and it did not survive: a 42-line tool that prints all six frozen DIFF lines on any non-pinned digest yields `PERTURB_PASS=6/6 LEGS=5/5 C1=PASS` exit 0, byte-identical to the real tool's output, because `c1-count.py:120` searches for one DIFF line without excluding the other five; defect found, smallest safe correction = round-51 nonce perturbation P7 with exclusive DIFF-set comparison.

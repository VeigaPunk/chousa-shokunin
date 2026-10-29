# RevQualityB — round 62, wave w1 (reviewer, QUALITY draft)

Scope: one draft criterion (next free number **124**) binding a sourced probe-backed entry to its probe. Lane read-only; scratch `/fast/scratch/hyaku/chousa-r62/RevQualityB/` created and removed; no tool installed; no lane file written.

## Findings

1. **The C2 probe's `expected=` values are uncited (red on the real evidence).** `corpus/evidence/round62/controls/candidate-openat2-probe.py` types 14 expected values; its docstring (lines 7–8) says they are the result "the openat2(2) page states or implies". Checked against the rendered S138 page and S139 header: 9 of 14 have a predicting sentence (P02, P04, P05, P07, P08, P10, P12, P13, P14); P01 (`False`, Python stdlib), P03 (`ELOOP` for `os.open` + `O_NOFOLLOW`, an open(2) result, not in S138), P06, P09, P11 have none — they are `INFERENCE`. Ran: cite check on the candidate as committed → `CITES=0/14`, `CITE=FAIL`, exit 1.
2. **The positive entry's Q7–Q9 quote the probe's own output.** `controls/c2v2-positive-entry.md:19-21` quote `S140` ("PROBE P02 … observed=opened expected=opened ok" etc.) and Claims 2 and 4 rest on those lines. The frozen counter accepts this (`positive rc=0 … C2=PASS`, `controls/c2v2-controls.txt`), and criterion 2 accepts an evidence id as the source, so the self-citation loophole is open.
3. **The frozen PROBE leg binds only part of the output.** `corpus/evidence/round62/c2v2-count.py:121` keeps only lines starting `PROBE `, `PROBE_FACTS=`, `HEADER `. The `KERNEL` and `PYTHON` lines — the host facts the entry's `verified-at` names (kernel 7.2.11-arch1-1, Python 3.14.8) — are not compared. Ran (import of the frozen `probe_lines`): committed output with `KERNEL 6.1.0-stale` → equal to live; `PYTHON 3.12.0` → equal. A stale host line reads `PROBE=1/1`.
4. **The live probe matches the committed text today.** Ran: `python3 -B controls/candidate-openat2-probe.py --work <fresh>` → output `diff` against `controls/candidate-openat2-probe.txt` is empty (`SAME`, rc 0 on the probe; 14/14).
5. **The PROBE binding is shown able to fail.** Ran: `python3 -B corpus/evidence/round62/controls/run-c2v2-controls.py --work <absent>` → `probe-output-edited rc=1 … PROBE=0/1 … OK`, `probe-output-stale rc=1 … PROBE=0/1 … OK`, `non-sequitur rc=0 … C2=PASS OK`, `C2V2_CONTROLS_UNEXPECTED=0`, exit 0 (`controls-live.txt`, 8.7 s).
6. **Duplicate check.** `grep` of `corpus/QUALITY.md`: criterion 2 (every claim carries a source — accepts "evidence id", which is the loophole in finding 2), 18 (probe exit 0 is completion only, compare its values — overlaps the value-comparison half), 73 (self-test compares against an expected file written from the rule, never the tool's own output — same principle, scoped to a capability self-test), 81/102 (counter keeps expected values out of the judged tool; scope is the counter, not a probe under a knowledge entry). No criterion requires a probe's expected value to cite its source sentence or binds the full committed output. **duplicate_of=none** (closest: 73 in principle, 2 and 18 in part).
7. **Landing consequence (INFERENCE).** The frozen counter cannot be edited (claims: post-freeze findings are routed as limits). Criterion 124 would fail the landed C2 entry at the next counter that enforces the full-output clause; the cite lines must be added to the probe before landing (comments only — ran: a probe with cite comments prints output identical to the committed text, `MARKED_LIVE_SAME`).

## Draft criterion 124 (text for QUALITY.md)

124. **A knowledge entry that rests on a probe binds the probe's full live output to its committed output in its counter, and every `expected` value in the probe cites the sentence that predicts it or is marked `INFERENCE`.** Round 62's C2 entry `openat2-resolve-r62.md` rests on `openat2-probe.py`, whose 14 `expected=` values are typed literals; the probe's docstring says they are the results "the openat2(2) page states or implies", yet 5 of 14 have no source sentence, and entry Q7–Q9 quote the probe's own `S140` output behind Claims 2 and 4. The frozen C2 PROBE leg compares only the `PROBE`, `PROBE_FACTS=` and `HEADER` lines (`corpus/evidence/round62/c2v2-count.py:121`), so a stale `KERNEL` or `PYTHON` line that the entry's `verified-at` names still reads `PROBE=1/1` (ran). Check: `python3 corpus/evidence/round62/c2v2-count.py` prints `PROBE=1/1`, and `python3 -B corpus/evidence/round62/probe-cite-check.py corpus/evidence/round62/openat2-probe.py` prints `CITES=14/14 … CITE=PASS`, exit 0; the cite check refuses an `S140` cite, a quote lacking the expected errno token, and an uncited probe; the full committed output is compared, so a stale `KERNEL` line fails. Shown able to fail (ran): `run-c2v2-controls.py --work <absent>` prints `probe-output-edited rc=1 … PROBE=0/1 … OK` and `probe-output-stale rc=1 … PROBE=0/1 … OK`; the candidate probe as committed prints `CITES=0/14 … CITE=FAIL`, exit 1. Named limits: the cite check confirms that a quote occurs in S138/S139 and, for an errno value, contains the errno token; that the quote predicts the value beyond that is judged by a non-author reviewer; `INFERENCE` is accepted as marked without judging its evidence. The frozen C2 counter does not meet the full-output clause, so that clause binds from the next counter; round 62 is not rewritten.

## Check runs (Check command = cite check; counter = frozen PROBE leg)

Checker (tested, 29 lines; L1 must commit it as `corpus/evidence/round62/probe-cite-check.py` with the probe, or the Check has no command):

```python
import ast, os, re, subprocess, sys, pathlib
def norm(s): return re.sub(r"\s+", " ", s).strip()
man = subprocess.run(["col", "-bx"], input=subprocess.run(["man", "-l", "/usr/share/man/man2/openat2.2.gz"], capture_output=True, env=dict(os.environ, MANWIDTH="1000", LC_ALL="C.UTF-8")).stdout, capture_output=True).stdout
SRC = {"S138": norm(man.decode("utf-8", "replace")), "S139": norm(pathlib.Path("/usr/include/linux/openat2.h").read_text(errors="replace"))}
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
exp = {}
for n in ast.walk(ast.parse(text)):
    if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "probe" and len(n.args) == 4 and isinstance(n.args[0], ast.Constant):
        exp[n.args[0].value] = n.args[3].value if isinstance(n.args[3], ast.Constant) else None
cites = {}
for l in text.splitlines():
    m = re.match(r"^\s*#\s*cite\s+(P\d+):\s*(.+?)\s*$", l)
    if m: cites.setdefault(m.group(1), []).append(m.group(2))
res = sure = inf = 0
for pid in sorted(exp):
    e, got = exp[pid], None
    for c in cites.get(pid, []):
        if c.startswith("INFERENCE"): got = "i"; break
        m = re.match(r'^(S138|S139) "(.+)"$', c)
        if not m: print(f"  {pid} cite refused: {c[:60]}"); continue
        q = norm(m.group(2))
        if len(q.split()) < 4 or q not in SRC[m.group(1)]: print(f"  {pid} quote not in {m.group(1)}: {q[:60]}"); continue
        if isinstance(e, str) and re.fullmatch(r"E[A-Z0-9]+", e) and e not in q: print(f"  {pid} quote lacks {e}"); continue
        got = "s"; break
    if got is None: print(f"  {pid} expected={e!r} uncited"); continue
    res += 1; sure += got == "s"; inf += got == "i"
print(f"CITES={res}/{len(exp)} SOURCED={sure} INFERENCE={inf}")
ok = bool(exp) and res == len(exp)
print(f"CITE={'PASS' if ok else 'FAIL'}"); sys.exit(0 if ok else 1)
```

Cite lines used in the marked copy (inserted as comments after `a = ap.parse_args()`): P01/P03/P06/P09/P11 `INFERENCE`; P02 `S138 "which affects the handling of symbolic links only in the final component of path"`; P04/P05 `S138 "ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link (or magic link)."`; P07/P08 `S138 "EXDEV how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, and an escape from the root during path resolution was detected."`; P10 `S139 "Make all jumps to "/" and ".." be scoped inside the dirfd (similar to chroot(2))."`; P12 `S138 "EINVAL An unknown flag or invalid value was specified in how."`; P13 `S138 "EINVAL mode is nonzero, but how.flags does not contain O_CREAT or O_TMPFILE."`; P14 `S138 "an O_PATH file descriptor referencing the symbolic link will be returned."`.

| case | command result (ran) | expect |
|---|---|---|
| real evidence: candidate as committed (red-before) | `CITES=0/14 SOURCED=0 INFERENCE=0`, `CITE=FAIL`, exit 1 | FAIL |
| marked positive (cites added, output unchanged) | `CITES=14/14 SOURCED=9 INFERENCE=5`, `CITE=PASS`, exit 0 | PASS |
| forge: P04 cites a quote without `ELOOP` | `P04 quote lacks ELOOP`, `CITES=13/14`, `CITE=FAIL`, exit 1 | FAIL |
| forge: P09 cites `S140` (own output) | `P09 cite refused: S140 …`, `CITES=13/14`, `CITE=FAIL`, exit 1 | FAIL |
| forge: P03 uncited | `P03 expected='ELOOP' uncited`, `CITE=FAIL`, exit 1 | FAIL |

Probe output stays bound: marked copy `--work <fresh>` `| diff` committed `candidate-openat2-probe.txt` → empty.

## Verdict on the criterion

- Can fail: yes — five red runs above; the controls `probe-output-edited` / `probe-output-stale` fail the PROBE leg (ran).
- Not a duplicate: nearest 73 (principle), 2 and 18 (in part); the full-output and expected-cites clauses are not stated in any existing criterion.
- Text is ready, with one landing dependency: the cite-check script must be committed with the probe, and the probe cites added before landing. Its Check depends on `man`/`col` and the installed man-pages 6.19 page (same dependency as the C2 counter).

## Limits and not run

- Not run: the frozen `c2v2-count.py` on the lane (the probe is absent there; `ENTRY`/`PROBE` legs fail on absence, as in `c2v2-before.txt`). PROBE-leg behaviour was measured through its own `probe_lines` function and the controls driver.
- Not run: any kernel other than 7.2.11; entailment of claims to quotes (not machine-checked, per C2 limits).
- Scratch `/fast/scratch/hyaku/chousa-r62/RevQualityB/` removed. No installs. No git mutation.

VERDICT: CRITERION_CHECK_CAN_FAIL=yes duplicate_of=none text_ready=yes

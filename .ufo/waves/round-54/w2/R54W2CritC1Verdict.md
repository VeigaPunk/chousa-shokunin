# R54W2CritC1Verdict — attack on C1's verdict and capability row (operability)

Seat scope: is "improved narrowly" honest for R54-C1; does the capability row's
evidence pointer demonstrate the capability running (AXES.md:57-64); does the
3/10 move. All counter/supplement runs on the integrated tip `178667dc`
(lane tool sha256 `2c0140bc…` = `measure-after.txt:1` header). No lane writes
besides this report; scratch `/fast/scratch/hyaku/chousa-r54/R54W2CritC1Verdict`
removed on exit; `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__` touched:
0 files newer than 1 h); no tools installed (python3 3.14, LibreOffice
26.8.1.1 already present — RULES.md: nothing to record); no network; every
soffice run via the counter's private profile under its `--work` dir.

## Frozen integrity (re-verified)

`git show 5a1a206:corpus/evidence/round54/c1-count.py | sha256sum` →
`633430a4f74a404645690da19f3b5907970d2b7ab1eabf62f6cc65643103b8e5` (matches W1
`R54ReviewC1Counter`'s recorded hash). `git diff 5a1a206..HEAD --stat` over
c1-count/c2-count/claims.md/before+control files → empty. Freeze holds.

## New counterexample: the supplement does NOT separate delegation from parsing

W1 forged the counter two ways: R54CritForgeC1 (sibling-HTML + canned REAL)
and R54ReviewC1Counter M15 (ctypes→soffice delegation). Erratum E1's supplement
closes the first shape. I rebuilt the second as
`/fast/scratch/…/delegate.py` (sha256 `b2e0bab0…`; 37 lines: lane tool imported
for OOXML + `OLE_MAGIC` only; OLE path = `ctypes.CDLL("libc.so.6").system()`
to `soffice --convert-to txt`, refusals keyed on byte markers — never parses
CFB/FIB/Clx, spawns a real child process on every accepted `.doc`).

Hook bypass, direct probe under the counter's own `hook.py`:

```
$ MARK=$S/spawn-marker.txt python3 $S/w-del/hook.py $S/spawnprobe.py   # ctypes.system("echo … > $MARK")
hook-run rc=0
$ cat spawn-marker.txt → SPAWNED_VIA_CTYPE
```

Run receipts (each `--per-leg 3`, private soffice profile under `--work`):

```
$ python3 corpus/evidence/round54/c1-count.py --tool $S/delegate.py --seed 7 --work $S/w-del
GEN=PASS 3 docs / NONWORD=PASS 3 sheets / ENCRYPTED=PASS 3 docs / MALFORMED=PASS 3 docs /
REAL=PASS 5 captures / REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4'] / LEGS=6/6 / C1=PASS  rc=0
$ python3 corpus/evidence/round54/c1-count.py --tool $S/delegate.py --work $S/w-del2          # unseeded, seed=78927062
LEGS=6/6 / C1=PASS  rc=0
$ python3 corpus/evidence/round54/c1-supplement.py --tool $S/delegate.py --seed 7 --work $S/w-del-supp
ISOLATED=PASS 3 docs / RESAVE=PASS 5 resaved captures / HELDOUT=PASS 3 lane files /
SUPPLEMENT_LEGS=3/3 / SUPPLEMENT=PASS  rc=0
```

Mechanism is structural, not a gap: `judge()`/`oracle()` (c1-supplement.py:52-81)
compare the tool's form against a soffice export made at counting time — a
delegating tool's output *is* the oracle, so ISOLATED/RESAVE/HELDOUT cannot
see it. Separation result, full matrix on this tip:

| tool | frozen c1-count | c1-supplement |
|---|---|---|
| landed `2c0140bc` | 6/6 PASS (unseeded `seed=616538535`, my run) | 3/3 PASS (`seed=517911377`) |
| rebuilt W1 forge `f73ac5c3` (deterministic rebuild, = controls/c1-forge.txt sha) | 6/6 PASS (`--seed 7`) | 0/3 FAIL |
| my ctypes delegate `b2e0bab0` | 6/6 PASS (seed 7 + unseeded) | **3/3 PASS** |

## Verdict on the verdict

- **"improved narrowly" is honest — the narrowest honest word.** Generous
  reading dies: the frozen counter still cannot distinguish parsing from
  *delegation* (not merely shortcut-forging), and the supplement judges
  against the same oracle a delegate emits, so no executable in the lane can
  currently tell a real CFB/FIB/Clx reader from a 37-line soffice shim that
  also spawns a forbidden process. The predicate's "fails the run on any
  process spawn" is falsified as a *measured* guarantee (ctypes bypass; M15
  already proved it, my delegate re-proves it end-to-end). Harsher reading
  dies: the frozen rule WAS met by a genuine implementation — m01-m16 sweep
  (R54MutOle) killed 9/16 mutants including every parse-altering one; E2's
  tracked-deletion fix is real (`tracked-deletion-check.py` →
  `TRACKED_DELETION=PASS`, ran) even though no frozen leg reaches it;
  S096's quarantine re-verdict used the tool's actual output (lesson:57).
- **Required caveat in the verdict text:** the supplement "separates" only
  the rebuilt shortcut forge (0/3); a delegating forge passes it 3/3 while
  violating the no-spawn clause invisibly. The lesson's row 4 wording
  ("closes those three shortcuts") is accurate for the forge it names — the
  SCORECARD row must not upgrade it to "supplement establishes the
  capability" (QUALITY 98's check claims the counter "refuses a tool that
  delegates to that reader": only true for Python-audit-event spawns —
  `subprocess.Popen` fires `AUDIT_FORBIDDEN` rc=97 (controls/c1-forge.txt
  shell leg), `ctypes.system` does not).
- **Capability row: admissible, with the behavioral framing.** AXES.md:63-64
  requires "a passing demonstration in the round report" — `measure-after.txt`
  binds tool-sha `2c0140bc` to C1=PASS + SUPPLEMENT=PASS, and the row's what-it-
  can-do ("prints the OLE .doc text form, locates quotes, refuses ole-*") is
  behaviorally demonstrated by the S100/S101 dumps it actually produced
  (`pointer-anchor-check.py` → `ANCHORED=16/16`, ran). The row must NOT claim
  "reads OLE natively" or "spawns nothing" — neither is measured. Pre-claiming
  bar met; mechanism unattributed.
- **3/10 does not move.** Convention held r44-r53: the numeric scale is the
  round-1 archived-export observable; capability acquisitions sit beside it.
  E2 changed no frozen-leg behavior (5 pinned forms byte-identical, erratum).

VERDICT: attacked C1's "improved narrowly" and capability row; both survive
with a one-class correction — the supplement separates shortcut-forge from
candidate but NOT delegate from candidate (new ctypes forge: frozen 6/6 +
supplement 3/3); the verdict and QUALITY 98 must name the ctypes-audit-hook
blind spot and keep the capability row behavioral (no-spawn/unparsed
unclaimed); score stays 3/10.

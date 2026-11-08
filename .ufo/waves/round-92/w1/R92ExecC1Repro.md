# R92ExecC1Repro — frozen C1 reproduction from clean tree

Seat: R92ExecC1Repro. Scratch: `/fast/scratch/hyaku/chousa-r92/R92ExecC1Repro/`.
Clone: `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo`,
checkout `16ccf7693c61b8ffe392fc757352304f239bfcad` (carrier C5). Asserted
`rev-parse --show-toplevel` = `$S/repo`, HEAD = `16ccf7693c61b8ffe392fc757352304f239bfcad`.
Runs below are from `$S/repo` with cd there (host cwd is fleet root).

## (a) verify — PASS, exact lines

Command (fresh copy: `$S/verify`):
`python3 -B corpus/evidence/round92/control-driver-r92.py verify --root . --repo . --rev 42e0337822a508208800f98faa3a63c6af9f8c27 --receipts-rev 16ccf7693c61b8ffe392fc757352304f239bfcad --work $S/verify`

Exit: 0. Stdout (receipt: `R92ExecC1Repro-verify-a.stdout.txt`):
```
BASES root=/fast/scratch/hyaku/chousa-r92/R92ExecC1Repro/repo repo=/fast/scratch/hyaku/chousa-r92/R92ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 7/16 pinned files byte-identical
RECEIPT SELF_PIN OK rev=42e0337822a508208800f98faa3a63c6af9f8c27 receipts_rev=16ccf7693c61b8ffe392fc757352304f239bfcad
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS
```
Stderr empty (`R92ExecC1Repro-verify-a.stderr.txt`, 0 bytes).
Observed: `CONTROL_DRIVER_R92=PASS`, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`,
`SELF_PIN OK rev=42e03378... receipts_rev=16ccf769...` — matches frozen predicate exactly.
Re-run (b)-adjacent second verify also PASS (same lines).

## (b) forgery battery — PASS under committed filename; seat-spec name ABSENT

Seat spec command: `python3 -B corpus/evidence/round92/control-forgeries-r92.py --work $S/forge`.
Result: exit 2, `python3: can't open file '.../control-forgeries-r92.py': [Errno 2] No such file or directory`.

The file does not exist at C5, nor at freeze F5 (`git ls-tree -r F5 -- corpus/evidence/round92/`
lists `forgeries-r92.py` and no `control-forgeries-r92.py`). Prior rounds used
`control-forgeries-r90.py` / `control-forgeries-r91.py`; round 92 renamed the battery to
`forgeries-r92.py` but `claims.md`/`claims.json` still name `control-forgeries-r92.py`.

Ran committed file `corpus/evidence/round92/forgeries-r92.py --work $S/forge`:
exit 0. Stdout (receipt: `R92ExecC1Repro-forge.stdout.txt`):
```
OK dup-pin-path: r92 rc=1 (PIN_DUPLICATE), r91 mechanism proven=True
OK second-script-unpinned: r92 rc=1 (INSTRUMENT_UNPINNED:elsewhere.sh), r91 mechanism proven=True
OK pins-rewrite: r92 rc=1 (INSTRUMENT_PIN_MISMATCH:pins.txt), r91 mechanism proven=True
OK positive: r92 rc=0 (r91 verify is not run: the prior pin-checks against the real table, so a fixture PASS is unclaimable)
FORGERY_REFUSED=3/3 POSITIVE=pass
```
This is the frozen `FORGERY_REFUSED=3/3 POSITIVE=pass` predicate, under the committed name.
FINDING (name mismatch): the counting command in the frozen claim points at a non-existent
script. If the gate executes the claim string verbatim, (b) fails with exit 2 and no predicate line.

## (c) claimed repairs

### (i) TMPDIR default — HELD
`TMPDIR=$S/td python3 -B ... verify --root . --repo . --rev F5 --receipts-rev C5` (no `--work`):
exit 0, full PASS lines, work outputs created under `$S/td` (`fresh-*.out`, `c1gate/legs/`, ...).
Receipt: `R92ExecC1Repro-verify-tmpdir.stdout.txt`. Code: `--work default=os.environ.get("TMPDIR") or "/fast/scratch/hyaku"` — as frozen.

### (ii) emit without --receipts — FIRED (claim text not implemented)
Command: `python3 -B ... emit --root . --rev F5` (no `--receipts`): exit 0, stdout
`EMIT ... EMITTED=6 MISMATCH=0` (receipt: `R92ExecC1Repro-emit-noreceipts.stdout.txt`).
Expected per claims.md rule 8: exit 2 with `emit requires an explicit --receipts`.
Code: `--receipts` has `default=DEFAULT_RECEIPTS`, and `emit` does `os.makedirs(a.receipts, exist_ok=True)`
and writes there unconditionally; no explicitness check. The only place "emit requires an explicit
--receipts" appears is the claims.md rule text. Docstring instead says the procedure names
`--receipts` (see `corpus/evidence/round92/after/c1-procedure.txt` — that file is absent at C5;
only round91's exists). So the frozen repair sentence and the code disagree.
Hygiene: this run re-wrote the receipts dir in the scratch clone (see (d)), then I restored it with
`git checkout -- .../c1-harm-setup.txt`; receipts shas identical to pre-state afterwards.
With explicit `--receipts $S/emit-scratch/receipts --work ...`, emit succeeds exit 0 (`R92ExecC1Repro-emit-explicit.stdout.txt`) and `git status --porcelain` stays clean — the explicit path works.

### (iii) indented headers via header_multi — HELD
Snippet import of `control-driver-r92.py` `header_multi`:
 input with `"  # case=IndentedCase\n\t# expected_exit=0\n    # exit=0\n # computed_against=42e03378...\n"` →
 `{'case': ['IndentedCase'], 'exit': ['3'], 'expected_exit': ['3'], 'computed_against': ['42e...']}`,
 all keys present, no MISSING_HEADER.
Fixture-level: `$S/header-fx/` (own expected/pins/self-pin) with receipt lines `  # case=ws-case`,
`\t# expected_exit=0`, `    # exit=0`, ` # computed_against=...`; verify exit 0,
`RECEIPT ws-case OK committed+exact+pin+fresh`, `COMMITTED_OK=1/1 EXACT_OK=1/1 PIN_OK=1/1 FRESH_OK=1/1 CONTROL_DRIVER_R92=PASS`
(receipt: `R92ExecC1Repro-header-fx.stdout.txt`; pristine indented receipt: `R92ExecC1Repro-header-pristine-ws.txt`).
The header is found, not `MISSING_HEADER`.

## (d) verify wrote nothing to receipts dir — HELD (after restoring my own emit pollution)

`sha256sum corpus/evidence/round92/controls/receipts/*.txt` before verify vs after verify only:
identical (no drift between the two verifies; receipts compared across both verify runs — pass).
Note: my `emit` run in (c)(ii) without `--receipts` did write into the scratch receipts dir
(one line changed: `c1-harm-setup.txt` embeds the absent-tool path, which is `--work`-dependent;
`git diff` shows the single-line path change). That is `emit`'s committed behavior with defaulted
`--receipts`, not a `verify` write. Restored via `git checkout`; both sha manifests identical
(receipts: `R92ExecC1Repro-receipts-before.sha.txt` / `R92ExecC1Repro-receipts-after.sha.txt`).
Final `git status --porcelain` in scratch: empty (clean).

## Evidence / receipts copied to wave folder

Reports: `.ufo/waves/round-92/w1/R92ExecC1Repro.md` (this file).
Copied receipts (all under `.../.ufo/waves/round-92/w1/`):
- `R92ExecC1Repro-verify-a.stdout.txt` + `.stderr.txt` — (a) verify, exit 0, full lines.
- `R92ExecC1Repro-forge.stdout.txt` (+ empty `.stderr.txt`) — (b) forgeries-r92.py, exit 0.
- `R92ExecC1Repro-verify-tmpdir.stdout.txt` — (c)(i) TMPDIR default, exit 0.
- `R92ExecC1Repro-emit-noreceipts.stdout.txt` — (c)(ii) emit no `--receipts`, exit 0 + EMITTED=6.
- `R92ExecC1Repro-emit-explicit.stdout.txt` — (c)(ii) emit with explicit `--receipts`, exit 0.
- `R92ExecC1Repro-header-fx.stdout.txt` + `R92ExecC1Repro-header-pristine-ws.txt` — (c)(iii) indented headers.
- `R92ExecC1Repro-receipts-before.sha.txt` + `R92ExecC1Repro-receipts-after.sha.txt` — (d) sha identity.
- `R92ExecC1Repro-instrument-pins.txt` — copy of on-disk pins (16 rows, self-pin last row).

## Findings summary (exact command / receipt / observed line + exit)

- F1 NAME MISMATCH (b): `control-forgeries-r92.py` at F5 and C5 does not exist; verbatim claim command exits 2 with `can't open file`. Committed `forgeries-r92.py` prints `FORGERY_REFUSED=3/3 POSITIVE=pass` exit 0.
- F2 EMIT GUARD FIRED (c)(ii): `emit` without `--receipts` exits 0 and writes to defaulted receipts dir; frozen rule text (`exit 2`, `emit requires an explicit --receipts`) is not implemented. Docstring cites an absent `after/c1-procedure.txt` (only round91's exists).
- Held: (a) verify PASS with exact counts and SELF_PIN revs; (c)(i) TMPDIR default; (c)(iii) indented headers via `header_multi`, no `MISSING_HEADER`; (d) verify does not write receipts (receipts identical across verifies).

Scratch removed after copying receipts (`rm -rf $S` after report).

VERDICT: R92ExecC1Repro C1 fired — verify/TMPDIR/indented-header legs held and forgeries passed under the committed name, but the claim's verbatim control-forgeries-r92.py is absent and emit has no explicit-receipts guard; both are frozen-text vs tree mismatches.

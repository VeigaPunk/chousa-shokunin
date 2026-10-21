# FC3 falsification: C3 control `entry-colon-denied-component`

Lane: chousa round27 attempt1, landed revision dd72641e574679c4f7882dd43de072b4c8892d6f.
Author: ChousaR27.FC3EntryColonDeniedCompon50-11 (leaf reviewer, no subagents).
Sandbox: /tmp/chousa-r27-falsify-FC3 (git archive of dd72641; mutants m1..m5 and base-gate.sh there).

## Verdict

FALSIFIED on calibration. The targeted fix HOLDS for the control's own fixture.

- HOLDS: reverting the entry-reader denylist arms (M1), or running the pre-fix base gate, makes the control fail for the intended reason. The gate reads and accepts the colon-denylisted entry (exit 0, no META_ENTRY_REFUSED).
- FALSIFIED: the control does not require `reason=denylist`. It passes for other refusal reasons. On the pre-fix base gate it passes for neighbouring fixtures (CX1), and it passes when the denylist refusal is mislabelled (CX2). It is therefore not a denylist-specific control.
- Separate contract conflict, not a defect of this control (CX4): the landed gate still refuses filesystem entry paths by citation-anchor prefix, which the C3 text prohibits. The lane's own compat controls require that behaviour.

## Provenance and fidelity

- Gate sha256 ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84: matches the claimed gate digest.
- Script sha256 5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df: matches `script_sha256` in corpus/evidence/round27-regressions-after.json. That receipt records this control at expected 1, actual 1, errors []. Receipt is fresh for this revision.
- Base gate 64eec5d (pre-fix), sha256 starts c2c813f1b425bc4e.
- Replica: `probe.py` reproduces the control's commands, fixture path and body, environment (CHOUSA_* stripped, LC_ALL=C), and expectations. I did NOT run round27-regressions.py or --selftest (bounds).
- Installs or updates: none. Tools used: bash, python3 (system), git, sha256sum, diff.

## (1) Is the expectation derived from the declared contract?

Control, round27-regressions.py lines 186-189:

    entry = root / 'synthetic:fixture/.config/entry.md'
    entry_text()
    observe('C3', 'entry-colon-denied-component', run(), 1,
            ('META_ENTRY_REFUSED', 'source=refused'), counts={r'^RESEARCH_GATE: ': 1})

- Refusal outcome: derived from the C3 text ("no reading a denylisted synthetic path when a colon occurs earlier"). Independent of gate code.
- Exit 1, `META_ENTRY_REFUSED`, `source=refused`: taken from the gate's own documented vocabulary (header line 35 for META_ENTRY_REFUSED; exit 1 = DRIFT; META line format). Derived from gate docs, not from gate logic, and not from the claim text.
- NOT derived: `reason=denylist`. The contract permits only the denylist reason for this input. The control accepts any META_ENTRY_REFUSED reason (nul, multilink, size, unreadable, stat, read). The suite pins `reason=denylist` only for registry rows (round27-regressions.py lines 175 and 179). No entry control pins it.
- Operability: an uncaught Python exception exits 1 (checked with `python3 -c 'raise RuntimeError(...)'`, exit 1). That is the same code the script uses for mismatch, while its docstring reserves exit 2 for setup. A harness crash therefore reports as a mismatch.
- Operability: the fixture directory `synthetic:fixture/.config/` is created by the loop at lines 170-172, not by this control. The control is order-dependent.

## (2) Mutation evidence

Fix under test: entry reader denylist arms, tools/research-gate.sh lines 2609 and 2616, on `is_denylist_fs_path` (lines 609-613). Base used prefix-only `is_denylist_path` at base lines 2584 and 2591.

Mutants (sandbox copies; `diff` against landed shows exactly these lines):
- M1: lines 2609 and 2616, `is_denylist_fs_path` -> `is_denylist_path` (both entry arms reverted).
- M2: line 2609, second operand only (canonical arm) -> `is_denylist_path "$canon"`.
- M3: line 2616 only (fd-canonical arm) -> `is_denylist_path "$fdcanon"`.
- M4: lines 611-612 -> `is_denylist_path_value "$f"` (filesystem check is full-path only).
- M5: lines 2610 and 2617, `refuse=denylist` -> `refuse=unreadable`.

Full nine-case replica (`python3 probe.py <gate>`, driver exit 0; the count is the result):

| Variant | Target control | Alias control | Other replica cases |
|---|---|---|---|
| landed dd72641 | PASS (exit 1, reason=denylist) | PASS | 0/9 mismatch |
| base 64eec5d (4-case run) | FAIL: exit 0 != 1; missing 'META_ENTRY_REFUSED'; missing 'source=refused' | FAIL (same) | registry-colon FAIL |
| M1 | FAIL: exit 0 != 1; missing 'META_ENTRY_REFUSED'; missing 'source=refused' | FAIL (same) | probe-credentials-after-colon FAIL; 3/9 mismatch |
| M2 | PASS | PASS | 0/9 mismatch |
| M3 | PASS | PASS | 0/9 mismatch |
| M4 | PASS | PASS | registry-legacy-env-anchor FAIL: exit 0 != 2; missing denylist; 1/9 |
| M5 | PASS | PASS | 0/9 mismatch (reason not pinned) |

Claims-side replica (`python3 claims_probe.py <gate>`): landed 0/3; M1 0/3; M4 1/3. Under M4, claims-legacy-env-anchor-refused FAILS (exit 0 != 1; missing 'FINDING CLAIM_SOURCE_SESSION'), because the literal file `synthetic.env:1` is read and supported.

Reading:
- Reverting the targeted fix (M1, or base) makes the control fail for the intended reason: a behavioural acceptance, not a parse or setup error.
- M2 and M3 are not detected by any control. Each arm alone is sufficient for every control: the fd-canonical arm catches the alias (inference from the M2 result), and the canonical arm catches the direct file. The controls cannot tell whether the canonical arm exists.
- M5 is not detected.

## (3) Counterexamples (nearby synthetic inputs)

CX1 (control passes on the pre-fix gate; vacuity). Fixture: `root/synthetic:fixture/.config/entry.md` with a NUL byte in the body (`## Cl\x00aim`).
- Base 64eec5d: exit 1; `FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=entry.md reason=nul unparsed`; `META entry=entry.md source=refused ...`.
- The control's three expectations are all met while the denylist fix is absent. Same result on M1.
- Hardlink variant (second name in the same .config directory): base gives reason=multilink, with the same control-style pass.
- Repro: `python3 nearby.py base-gate.sh` (rows nul-in-colon-denylist and hardlink-in-colon-denylist: control_style_pass=True, pins_denylist_reason=False).

CX2 (control passes with a mislabelled refusal). M5 relabels entry denylist refusals as `reason=unreadable`. Target control PASSES, and so does the whole replica (0/9). Repro: `python3 probe.py m5/tools/research-gate.sh`.

CX3 (blind spot, canonical arm). M2 opens the denylisted canonical path before refusing. By code reading, the `exec {meta_fd}<"$canon"` at line 2611 runs before the fd check at 2616. That contradicts the gate's own header invariant at line 252, "Opens: allowlist metadata only; denylist -> SESSION_READ". All controls PASS on M2, because opens are not observable through the controls' exit and token checks. A FIFO fixture cannot reach this path: a FIFO fails the `-f` usage check before the denylist check.

CX4 (landed gate versus the C3 text; inherited from base). The C3 text says filesystem denylist checks "must inspect complete filesystem paths, not citation-anchor prefixes". Landed `is_denylist_fs_path` (609-613) still ORs in the prefix check. Both inputs below are refused as reason=denylist by landed and by base; the complete-path reading says CLEAN:
- `root/corpus/knowledge/notes.env:v2/entry.md` (exit 1; directory name with colon).
- `root/corpus/knowledge/cfg.env:notes.md` (exit 1).
The prefix arm is required by: independent `legacy-env-anchor-refusal` (registry `synthetic.env:1`) and `claims-legacy-env-anchor-refused` (M4 fails both); selftest `metadata-colon-anchor-denylist-compat` (round27 added it at gate line 6492, per the dd72641 diff). This is a deliberate compat decision that contradicts the C3 text. The target control does NOT depend on it: M4 passes the target. Repro: `python3 nearby.py tools/research-gate.sh`.

CX5 (same class, pre-existing; no control covers it). Sweep path sets apply no denylist. `python3 sweep_probe.py`:
- `where=.config/*.md`: `SWEEP id=SW1 where=.config/*.md looked=local hits=1 at=.config/secret-token.md observed=hit`, exit 1, on base and on landed.
- `where=synthetic:fixture/.config/*.md`: same shape, `at=synthetic:fixture/.config/secret-token.md`, exit 1, on base and on landed.
- No `is_denylist*` call appears in the sweep code (landed call sites: 595, 609-616, 631, 646, 660, 1139, 1166, 1613, 2394, 2401, 2609, 2616). Denylisted names are printed verbatim. Not in C3's reported set; recorded as a named gap.

CX6 (boundary, judgment; not a counterexample). `root/synthetic:.config/entry.md` is CLEAN on base, landed and M4. The complete component is `synthetic:.config`, not `.config`, so component semantics allow it. The C3 phrase "when a colon occurs earlier" could be read to want refusal. No control covers it; the lane should decide and pin it.

## Commands and exit codes

- `git -C <lane> archive dd72641... | tar -x -C /tmp/chousa-r27-falsify-FC3`: exit 0.
- `git show dd72641:tools/research-gate.sh | sha256sum`: ca39d14d... (match).
- `python3 probe.py tools/research-gate.sh`: mismatches=0 total=9.
- `python3 probe.py m1|m2|m3|m4|m5/tools/research-gate.sh`: 3/9, 0/9, 0/9, 1/9, 0/9.
- `python3 probe.py base-gate.sh <target, alias, ordinary, registry-colon>`: 3 of 4 mismatch.
- `python3 nearby.py <gate>`: run on landed, base and m1..m5 (results in CX1-CX6 and the table).
- `python3 claims_probe.py <gate>`: landed 0/3; m1 0/3; m4 1/3.
- `python3 sweep_probe.py <gate>`: landed and base, both cases exit 1 with a denylisted hit.
- `grep -n "reason=denylist\|denylist'" round27-regressions.py`: lines 175, 179 only (registry rows).
- `python3 -c 'raise RuntimeError(...)'`: exit 1.

## Limits

- Replica, not the script. The target control runs after other C3 controls in the same temporary root; I did not measure whether that carried state is inert. For a single-file entry check it should be, but that is unverified.
- The fd-canonical arm (M3) is race-only and was not exercised; no race was constructed.
- Fixtures synthetic only. No network, no host files, no /proc or live-process inspection by me, no strace, no namespaces. The gate's own `/proc/$$/fd` reads ran only on sandbox fixtures.
- Mutants are sandbox copies. Lane production files, lane git and index: untouched.
- Judgment calls are labelled as such (CX4 contract reading, CX6 boundary).

## Author-lane advice (not an outside admission)

1. Pin `reason=denylist` in `entry-colon-denied-component` and the canonical-alias control. The gate already emits the exact token (`reason=denylist unparsed`). Add NUL and hardlink neighbours with the same pin. This makes CX1 and CX2 detectable.
2. Resolve the prefix-arm conflict (CX4) explicitly. Either amend the C3 text to name the `.env:<anchor>` compat for filesystem paths, or drop the prefix arm from `is_denylist_fs_path` and revise `legacy-env-anchor-refusal`, `claims-legacy-env-anchor-refused` and selftest `metadata-colon-anchor-denylist-compat` together. Do not ship one half.
3. Give the harness a real exit 2 for setup errors (wrap main in try/except, exit 2) so that crashes are not reported as DRIFT.
4. Add a sweep denylist control, or record CX5 as a named limit.
5. Accept M2 and M3 as named blind spots, or add a race-tolerant test that observes the open.

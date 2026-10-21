# FC3 falsification: `claims-canonical-colon-denied` at dd72641e

Item: C3 control `claims-canonical-colon-denied` in `corpus/evidence/round27-regressions.py` (alias setup lines 185–196; claims loop lines 210–223). Targeted production fix: `tools/research-gate.sh` lines 1166–1170 in `claim_source_path` (canonical-target denylist check, absent at base 64eec5d) plus the full-path leg of `is_denylist_fs_path` (lines 609–613). Revision dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256 ca39d14d…92f84 (matches pin).

## Verdict

| Question | Verdict |
|---|---|
| 1. Expectation derived from declared contract, independent of gate code | HOLDS (negative-only; see 1) |
| 2. Reverting the targeted fix fails the control for the intended reason | HOLDS (specific to the canonical leg; see 2) |
| 3. Nearby input or mutant where landed is wrong or the control is vacuous | FALSIFIED (vacuity, one new over-refusal, contract conflict; see 3) |
| Axis: operability | Minor defect: canonical refusal names the benign alias, not the denylisted target (see 4) |
| Axis: freshness | HOLDS: persisted receipt hashes match the scripts (see 5) |
| Axis: calibration | FALSIFIED: all three C3 claims controls are refusal-only; landed refuses benign `creds.env:x/…` alias that base accepted |

Overall: FALSIFIED in part. The targeted mechanism behaves as the control expects. The control itself cannot tell a correct gate from a gate that refuses every claim source, and the landed claims-source check over-refuses benign colon-named paths.

## Setup (sandbox only; no lane writes)

- Pinned extract: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e… | tar -x -C /tmp/chousa-r27-falsify-FC3ClaimsCanonicalColonDe56` → exit 0. `sha256sum tools/research-gate.sh` = ca39d14d…92f84.
- Base for comparison: `git archive 64eec5d41c7cf7f17f5ce1e968e28b3769952596 | tar -x -C …-base` → exit 0; base gate sha c2c813f1…2fe0 (differs, as expected). Base-to-landed diff: `/tmp/chousa-r27-falsify-FC3ClaimsCanonicalColonDe56-gate.diff`.
- Probe: `probe/fc3_probe.py` (sandbox). Replays the control and 20 nearby claim-source inputs, one `verify-claims` gate run per probe on a fresh temp fixture. It does not run `--selftest` or the regression script. Fixture text matches regression lines 57–58 (entry) and 165–175 (registry table written to `synthetic.env:1`).
- Runs: `timeout 110 python3 probe/fc3_probe.py --gate <gate> --label <L> --out probe/results-<L>.json`. Harness exit 0 for all 10 configurations. Per-probe gate return codes are in the JSON.
- Mutants (created with the edit tool; each diff checked against the pinned gate):
  - M1: delete lines 1166–1170 (canonical leg). Diff: 5 lines removed.
  - M2: canonical leg becomes prefix-only `is_denylist_path "$canon"`. Diff: 1 line changed.
  - M3: `is_denylist_fs_path` loses its full-path leg (line 611). Diff: 1 line removed.
  - M4: `is_denylist_fs_path` loses its citation-prefix leg (line 612 becomes full-path only). Diff: 1 line changed.
  - M6: insert `CLAIM_REFUSE=CLAIM_SOURCE_SESSION; …; return 1` at line 1137, so every claim source is refused.
  - M7: insert `if [[ -L $src ]]; … return 1` at line 1138, so every symlinked source is refused.
  - landedDN / M1DN: landed and M1 run with `TMPDIR` under a sandbox directory named `.config`, so the synthetic root path contains `/.config/`.
- Matrix: 21 probes per configuration. `ok` means the gate matched the contract expectation (or the control's expectation for the ambiguous legacy row).

| Configuration | ok / 21 |
|---|---|
| base 64eec5d | 7 |
| landed dd72641e | 18 |
| M1 (canonical leg removed) | 9 |
| M2 (canonical prefix-only) | 8 |
| M3 (full-path leg removed) | 6 |
| M4 (prefix leg removed) | 20 |
| M6 (refuse every claim source) | 14 |
| M7 (refuse every symlink source) | 15 |
| landedDN / M1DN (TMPDIR under `.config`) | 14 / 14 |

## 1. Expectation provenance: HOLDS

- Contract, `corpus/evidence/round27-claims.md` line 15: "Filesystem-path denylist checks must inspect complete filesystem paths, not citation-anchor prefixes … no reading a denylisted synthetic path when a colon occurs earlier."
- The control's expectation is literal: rc 1, `FINDING CLAIM_SOURCE_SESSION`, exactly one `^RESEARCH_GATE: ` line. It calls no gate helper. The only gate-derived inputs are the pre-existing `/.config/` denylist token (gate lines 601–604) and the finding name (gate header line 24).
- Caveat: the expectation asserts refusal only. The independent claims set has no positive claims control (see 3a).

## 2. Mutation: HOLDS (fails for the intended reason)

| Gate | `claims-canonical-colon-denied` | Claim line / finding (from JSON) |
|---|---|---|
| landed | rc 1 ✔ | `observed=refused … verdict=refused`; `FINDING CLAIM_SOURCE_SESSION`; `RESEARCH_GATE: DRIFT` |
| base 64eec5d | rc 0 ✗ | `observed=supported … verdict=match`; no FINDING |
| M1 (canonical leg deleted) | rc 0 ✗ | `observed=supported … at=line:2 verdict=match`; no FINDING |
| M2 (canonical prefix-only) | rc 0 ✗ | `observed=supported`; no FINDING |
| M3 (full-path leg dropped) | rc 0 ✗ | `observed=supported`; no FINDING (the raw control also fails here) |
| M4 (prefix leg dropped) | rc 1 ✔ | `observed=refused`; the control does not depend on the prefix leg |

- Specificity: M1 leaves `claims-raw-colon-denied` passing (rc 1), so the failure is attributable to the canonical leg alone.
- The failure is a read-through of the real span (`verdict=match`), not a parse or setup error.

## 3. Counterexamples: FALSIFIED

### 3a. Vacuity: the control passes gates that never implement the canonical denylist

| Gate | What it does | Target control | Other two C3 claims controls | Positive `alias → benign file` |
|---|---|---|---|---|
| M6 | refuse every claim source as SESSION | PASS (rc 1) | PASS | FAIL (rc 1) |
| M7 | refuse every symlinked source as SESSION | PASS (rc 1, refused by the symlink, not the denylist) | PASS | FAIL (rc 1) |
| M1DN | M1 with `TMPDIR` under `…/.config/` | PASS (rc 1, refused by the raw pre-check on the root path) | PASS | FAIL (rc 1) |

- The independent claims set has three refusal-only controls and no positive claims control, so these gates pass the C3 claims subset.
- Inference, not run: the in-gate selftest has at least 10 positive `tclaims … 0` cases (grep; e.g. `claims-pass` near line 4057), which likely catches M6. Grep finds no claims-mode positive symlink case (`ln -s` appears only in sweeps, pointer and metadata cases; the single claims symlink case, line 6505, expects refusal), so M7 probably survives the selftest too.

### 3b. Landed gate wrong on nearby benign inputs (calibration)

| ID | Synthetic input (under root) | Contract | base | landed | Cause |
|---|---|---|---|---|---|
| CE-1 (minimal) | `alias.md → creds.env:x/entry.md`, benign content | allow | rc 0 supported (accepted) | rc 1 refused, `CLAIM_SOURCE_SESSION` | NEW: canonical leg uses `is_denylist_fs_path`; its prefix leg reads `creds.env` as `*.env` |
| CE-2 | `creds.env:x/entry.md` (raw path) | allow | rc 1 refused | rc 1 refused | pre-existing: raw pre-check prefix leg |
| CE-3 | symlink `creds.env:x → plain/entry.md` | allow | rc 1 refused | rc 1 refused | pre-existing: raw pre-check prefix leg |

- No under-refusal found. Every complete-path denylist form was refused through symlink, directory symlink, colon-in-symlink-name, two-hop chain, and relative source: `/.config/`, `/.omp/`, `/.local/state/`, `credentials/`, `Cookies`, `server.token`, `*.env`. Benign `alias → .config:x/…` and `alias → synthetic:fixture/…` were accepted.
- CE-1 is wrong under the complete-path reading the C3 text requires. It is defensible under a parity reading, because base already refuses the raw form (CE-2). That reading contradicts the C3 text, so the landed behaviour needs an explicit decision.

### 3c. Contract conflict: the control pins the citation-prefix leg

- `control-legacy-env-anchor` (regression lines 212–223) requires `synthetic.env:1` to be refused. Landed refuses it only through the citation-prefix leg. Under M4 the claim is read (`CLAIM_SPAN_NOT_FOUND`, observed unsupported, rc 1, no SESSION), so the control fails for the intended reason.
- Registry sibling (`legacy-env-anchor-refusal`, regression lines 170 and 174–175): with the same `synthetic.env:1` table, `verify-metadata --registry` returns rc 2 `metadata registry refused: denylist` on landed. Under M4 it returns rc 0 `RESEARCH_GATE: CLEAN`. The prefix leg is the sole enforcer of both legacy controls.
- Grammar: `verify-claims` sources are local files with no anchor syntax (gate header lines 44–50). `path#kind:text` anchors exist only in chain mode (lines 78–87). The `:1` in a claims source is a literal filename character. Regression comment line 210 says "Source paths are filesystem inputs too." The counter-reading is header lines 48–50, "same boundary as verify pointers," which would import pointer prefix semantics. The C3 text needs one explicit rule.

## 4. Operability note

- The canonical refusal emits `CLAIM_REFUSE_OBS="path=$(ptr_file_part "$src") …"` (landed line 1168). For CE-1 the finding reads `source=<alias> obs=path=<alias> denied`, which names the benign alias, not `creds.env` or the denylisted target. The raw colon refusal prints the truncated citation prefix (`obs=path=<root>/synthetic denied`).
- For an in-root alias to a denylisted path outside the root, base reports `CLAIM_SOURCE_OUT_OF_CORPUS` and landed reports `CLAIM_SOURCE_SESSION`, because the canonical leg runs before the boundary check. Both are crit and neither reads the file.
- The control checks only the finding name, so it cannot detect any of this.

## 5. Freshness: HOLDS

- `corpus/evidence/round27-regressions-after.json` `script_sha256` = 5afea786…df. Sandbox and lane `round27-regressions.py` both = 5afea786…df (three-way match). Receipt `gate_sha256` = ca39d14d…92f84 = pinned gate.
- Persisted row: `C3 claims-canonical-colon-denied expected 1 actual 1 errors []`. The landed replay reproduces it: rc 1, `CLAIM_SOURCE_SESSION`, one verdict.

## 6. Limits

- Not run: full `--selftest`, the whole regression script, network, any lane edit. Probes are one `verify-claims` each on synthetic fixtures. Expectations were hand-written from the contract.
- Not testable synthetically: the time-of-check/time-of-use gap between the canonical check and `cat`, and bind-mount aliases (nlink and device checks exist; not exercised here).
- An early registry-check attempt aborted because `set -e` from an earlier extraction command persisted in my shell (the gate's expected rc 2 killed the shell). I re-ran with errexit cleared; the aborted output is not used.
- Two foreign `/tmp/chousa-r27-synthetic-*` directories exist (`…-qTfi`, `…-l7j6tga4`). They have the regression-script layout, not mine. I left them alone. My probe removes its own roots.
- Tools: no installs or updates. Present and used: bash 5.3.20, python3 3.14.8, git, tar, sha256sum, diff, grep. `readlink` reports `readlink 0.8.0`; the probes ran against that binary.

## 7. Author-lane advice (not an admission)

1. Add a differential positive pair to the independent set: `alias → synthetic:fixture/entry.md` must be accepted (rc 0, `VERDICT_BEARING_CLAIMS=1/1`) beside `alias → synthetic:fixture/.config/entry.md` refused. This single pair fails M6, M7 and M1DN.
2. Decide CE-1 explicitly. Either drop the citation-prefix leg for claim sources (M4 semantics), flip `claims-legacy-env-anchor-refused` and the registry legacy case, and add a positive for `creds.env:x/…`. Or keep the leg, write the legacy exception into the C3 text, and label CE-1 as a control.
3. Make the canonical refusal name the resolved target (complete path), not `ptr_file_part "$src"`.
4. Keep the synthetic root outside any denylisted component, or let the positive pair detect when it is not.

Reproduction artifacts (sandbox): `probe/fc3_probe.py`; `probe/results-{base,landed,M1,M2,M3,M4,M6,M7,landedDN,M1DN}.json`; mutant gates under `mut/*/tools/research-gate.sh`.

## Addendum (append-only correction)

- Base gate sha256 (64eec5d) is c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6. The "…2fe0" tail in Setup was mistyped; no other values change.

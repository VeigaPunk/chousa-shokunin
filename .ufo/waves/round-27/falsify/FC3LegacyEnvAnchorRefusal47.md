# FC3LegacyEnvAnchorRefusal47: C3 control `legacy-env-anchor-refusal` (round 27 attempt 1, falsify)

Seat: `ChousaR27.FC3LegacyEnvAnchorRefusal47-11` (leaf; no lane writes except this report). Author-lane advice, not an outside admission.
Target: `dd72641e574679c4f7882dd43de072b4c8892d6f`. `sha256 tools/research-gate.sh = ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches the pinned gate).
Comparison base: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, gate `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Item: `corpus/evidence/round27-regressions.py:170` (`('legacy-env-anchor-refusal', root / 'synthetic.env:1')`, loop at 166-175). Expectation: `--registry` on that file gives exit 2, `metadata registry refused: denylist`, and no `RESEARCH_GATE:` line.
Axes: calibration (primary), operability (refusal exit and message identity). Freshness not touched.

## Verdict: FALSIFIED

The control runs green on the landed gate, so its mechanics hold (key output: `research-gate: metadata registry refused: denylist`, exit 2, no verdict line). It is falsified on three points:

1. **Derivation.** Its expectation is not derived from the declared C3 contract. It comes from an accepted monotone-retention decision, which the C3 text's negative clause forbids.
2. **Discrimination.** It guards only the retained citation-prefix arm. It is green at base, and it stays green when the complete-path repair is reverted.
3. **Nearby inputs.** The retained arm is applied inconsistently, and it over-refuses complete paths relative to the frozen text.

## 1. Derivation: falsified

- Frozen text, `corpus/evidence/round27-claims.md:15`: "Filesystem-path denylist checks must inspect complete filesystem paths, not citation-anchor prefixes; preserve existing citation-pointer semantics."
- The control passes `synthetic.env:1` to `--registry` as a real, existing file. Refusal happens only because its citation-anchor prefix `synthetic.env` matches `*.env`. That is the basis the frozen text forbids for filesystem paths.
- The lane classifies `--registry` as a raw filesystem caller (`.ufo/waves/round-27/build/CriticRegistryGrammar.md:68-69`). "Preserve citation-pointer semantics" therefore does not cover it.
- Provenance of the expectation, all lane-internal and none in the frozen claims file:
  - `.ufo/waves/round-27/build/CriticPathScope.md:31-43` (CX1) and `:148` (control 5, "Monotone guard: registry `w/k.env:1` still refused"). The harness control has the same shape.
  - `.ufo/waves/round-27/build/ConnectFailures.md:94-97` and `:195-196`: "The fix must be the union, not a replacement"; "the union is mandatory".
  - `.ufo/waves/round-27/build/ExecRegistry.md:6`: "The raw predicate also preserves prior anchor-prefix refusals such as `.env:1`."
  - `corpus/lessons/round-27.md:91-92`: "accepted monotonicity constraint. A complete-filesystem predicate must add full-path matching without losing old `.env:1` refusal."
- Not derived from the reported r26 failure. The B1-B6 and S1-S10 inputs in `.ufo/waves/round-26/falsify/FRegistryRegistryDeny.md:43-65` contain no `X.env:N` shape.
- The base gate has no selftest pin for this behaviour. `metadata-colon-anchor-denylist-compat` appears only in landed (gate lines ~6491-6493). Base does still refuse `synthetic.env:1` (replica below), so the behaviour is inherited, but its pin is new.

## 2. Discrimination: partly falsified

Replica results. Each replica invocation exited 0; the per-case gate rc is listed.

| variant (sandbox) | change | legacy control | adjacent controls |
|---|---|---|---|
| landed `ca39d14d...` | none | rc 2, green | colon-denied-component rc 2; ordinary-colon rc 0; claims-legacy rc 1; all green |
| base `c2c813f1...` | pre-repair | rc 2, green (passes before the repair) | claims-legacy rc 1 green; colon-denied-component not run (reported baseline failure, not rerun) |
| mutA | drop citation-prefix arm (CX1 full-path swap) | **rc 0, RED**: `exit 0 != 2`; denylist message missing; `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` printed | colon-denied-component still rc 2; claims-legacy rc 1 but FINDING CLAIM_SOURCE_SESSION missing |
| mutR | revert complete-path arm to base prefix-only | rc 2, **still green** | colon-denied-component **rc 0, RED** (the B1 class returns) |
| mutE | refuse any path containing a colon | rc 2, still green | ordinary-colon-is-allowed **rc 2, RED** |
| mutG | refuse any path containing `.env` | rc 2, still green | adjacent-env-substring-negative **rc 2, RED** |

Mutant edits against the landed copy (`diff` exit 1 each, as expected):
- mutA: lines 611-612 of `is_denylist_fs_path` (gate 609-613) replaced by `is_denylist_path_value "$f"`.
- mutR: line 611 removed, so the predicate is prefix-only, equal to base semantics.
- mutE: `[[ $f == *:* ]] && return 0` inserted before 611.
- mutG: `[[ $f == *.env* ]] && return 0` inserted before 611.

mutA fails for the intended reason. The table parsed (`CLEAN`), so this is not a parse or setup error; only the prefix refusal disappeared. Its citation wrapper `is_denylist_path` is unchanged, so pointer sites are untouched.

## 3. Nearby synthetic inputs (valid table; entry as in the control)

- **CE-1, the anchor rule depends on where the first colon sits.** `<root>/synthetic.env:1` gives rc 2 (refused) on landed and base. `<root>/a:b/synthetic.env:1` gives rc 0 with `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` on landed and base. `ptr_file_part` (gate 573-576, applied through `is_denylist_fs_path` at 612) cuts the complete path at its first colon. For `.../a:b/...` the prefix is `.../a`. The frozen literal rule makes the read correct; the anchor rule the control encodes makes it a miss. The landed outcomes are not explained by the control's own stated rule, because only the first colon's position differs. Inherited from base; C3 does not close it.
- **CE-2, over-refusal of complete paths.** `<root>/notes.env:v2/registry.md` (valid table) gives rc 2 `metadata registry refused: denylist` on landed and base; mutA gives rc 0 CLEAN. `<root>/notes.env:v2/entry.md` (clean entry) gives rc 1 `META_ENTRY_REFUSED ... reason=denylist` on landed and base; mutA gives rc 0 `verdict=clean`. These are wrong under the frozen text and right under the accepted monotone lesson.
- **CE-3, the `.env` family has no non-suffix negative.** `grep -c 'environment\|\.envx\|dotenv'` on the harness gives 0. The only `env`-bearing fixtures are `synthetic:fixture.env` (line 169) and `synthetic.env:1` (lines 170, 215). mutG therefore passes every `.env` fixture in the harness [INFERENCE from source; full harness not run]. The replica's added negative `synthetic.environment.md` catches it (rc 0 landed, rc 2 mutG).
- **CE-4, any-colon refusal also passes this control.** mutE is green here. Only `ordinary-colon-is-allowed` detects it. The control alone cannot separate "prefix ends in .env" from "any colon".
- **CE-5, identity, over-refusal only (code read, not executed).** The landed fs predicate calls `ptr_file_part`, which calls `norm_ptr` (gate 567-576). `CriticPathScope.md:105-106` said not to run `norm_ptr` inside the fs helper. The effect can only add refusals (backtick-stripped prefix).
- **CE-6, the mechanism counter measures names.** `round27-mechanisms.py` on landed gives `C3_pointer_predicate_on_registry_path: 0` (base 3). The zero comes from renaming `is_denylist_path` to `is_denylist_fs_path`; the prefix arm survives inside the renamed predicate. The probe scans only `metadata_registry_load`, so it is not evidence for the claimed semantics.

## Provenance check (no rerun)

Recorded `corpus/evidence/round27-regressions-after.json`: `script_sha256 5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df`, `gate_sha256 ca39d14db907ec3f...`. Both equal the sandbox script and gate. Recorded control entry (lines 445-449): expected_exit 2, actual_exit 2, errors []. The replica's landed run agrees.

## Commands and exit codes (sandbox only)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e... | tar -x -C /tmp/chousa-r27-falsify-FC3LegacyEnvAnchorRefusal47`: exit 0.
- `git -C ... archive 64eec5d... | tar -x -C /tmp/chousa-r27-falsify-FC3LegacyEnvAnchorRefusal47-base`: exit 0.
- `bash -n` on landed, base, mutA, mutE, mutG, mutR: exit 0 each.
- `python3 replica.py <gate> <case list>` on landed, base, mutA, mutR, mutE, mutG and the colon-directory fixture: exit 0 each. Per-case gate rc and mismatches are in the JSON outputs.
- `python3 corpus/evidence/round27-mechanisms.py {landed,base}.sh`: exit 0 each (landed all 0; base C1=1, C2=2, C3=5).
- `grep -n metadata-colon-anchor-denylist-compat` on base: exit 1 (absent); on landed: lines 6491-6493.
- `diff` landed against each mutant: exit 1 (expected).

No tools were installed or updated. Used only bash, coreutils, tar, git archive (read-only), sha256sum, diff, and python3 stdlib.

## Limits

- Ran only this control and its adjacent fixtures. Not run: full `--selftest`, the 58-case regression script (L1 owns both), and base `colon-denied-component` (a reported baseline failure, not rerun).
- Replica equivalence is argued from source (same fixtures, env, run and observe) and checked against the recorded after-run for this control.
- Synthetic fixtures only. Not tested: open-time races, bind mounts, the fdcanon arm beyond static reading, case-insensitive filesystems (`.ENV`), chain refs, and `e.env:1.md` entries (same predicate, not executed).
- The gate itself reads `/proc/$$/fd` via `readlink` during normal operation on synthetic fixtures. I did not probe `/proc` directly.
- No LSP device was available. Navigation was grep plus reading, which is not semantic proof.
- The claims analog `claims-legacy-env-anchor-refused` belongs to peer item `FC3ClaimsLegacyEnvAnchorR57.md`; I used it only as a sensitivity check.

## Recommendations (author-lane advice)

1. Reconcile claim and implementation. Either amend C3 to state that raw filesystem inputs keep prior citation-prefix refusals (monotone retention), and label this control a retained-legacy guard rather than repair evidence; or remove the prefix arm and accept the non-monotone loss the accepted lesson forbids. Right now the frozen text and the control disagree.
2. Resolve or document CE-1. A last-colon anchor rule would be consistent with the control's own semantics, but that is a design change, not a repair. Without it, refusal depends on directory names.
3. Add a non-suffix `env` negative (for example `synthetic.environment.md`, expected rc 0) and a control for whichever colon-earlier behaviour is chosen.
4. Do not present this control as before/after evidence. It is green at base.

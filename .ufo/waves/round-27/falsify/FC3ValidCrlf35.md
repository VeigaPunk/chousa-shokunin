# FC3ValidCrlf35: falsification of C3 control `valid-crlf`

Lane: chousa round 27, attempt 1. Target: dd72641e574679c4f7882dd43de072b4c8892d6f (master).
Gate under test: `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches the assigned gate hash).
Base for comparison: 64eec5d41c7cf7f17f5ce1e968e28b3769952596 `tools/research-gate.sh` sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Sandbox: `/tmp/chousa-r27-falsify-FC3ValidCrlf35` (git archive of the target; base archived separately; probes and mutants under it). Synthetic fixtures only.
Axis exercised: calibration (C3). Operability and freshness are not touched by this control.

## Verdict

- Control `valid-crlf` (`corpus/evidence/round27-regressions.py:141`): **FALSIFIED as a guard.** Its expectation is a constant, but the premise that CRLF registries are valid is inherited rather than declared. It is blind to each single CR-handling or edge-whitespace regression. It does not guard the width repair. Its only CR-specific sensitivity appears under joint removal of two mechanisms that are redundant with each other.
- Landed gate, CRLF class: **HOLDS** for CRLF-versus-LF equivalence (16/16 pairs identical on landed, and on base). The lenient and strict behaviours on bare CR, double CR, lone CR and BOM (N3 to N6) are inherited, except the BOM exit-class change (N6), which is low severity.

## Q1: is the expectation derived from the declared contract, independent of gate code?

**Partially.**

- Independent of gate code: yes. Expected rc 0, verdict count 1 and no required token are literals (`regressions.py:141`, tables loop `:144-150`). `int(rc != 2)` only encodes the C1 verdict-anchor rule.
- Declared contract: no. `round27-claims.md:15` (C3) says only "Existing well-formed registry behavior and exact used-by rules remain". `round26-claims.md:84-97` (Claim 3) says "SOURCES.md-shaped" registry, "table rows", "columns located by header name". No declared document (`round27-claims.md`, `round26-claims.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `README.md`, `AGENTS.md`) states CRLF, line-ending, GFM or CommonMark grammar for registries. The only CRLF mention in those documents is the round-26 reader-allocation shape `s3-crlf` (`round26-claims.md:40-41`).
- Where the premise comes from:
  - (a) Base behaviour: the base gate passes this control (rc 0), and base already strips CR per line (`base tools/research-gate.sh:2411`).
  - (b) Lane falsifier oracles: `.ufo/waves/round-26/falsify/FRegistryUsedByMissing.md:90` ("C4 (CRLF registry with the correct path) is clean") and `.ufo/waves/round-26/falsify/FRegistryRejected.md:67` (R23 holds).
  - (c) A GFM reading that lane critics use as reference (`.ufo/waves/round-26/falsify/FRegistryHeaderless.md:93-94`; `.ufo/waves/round-27/build/CriticRegistryGrammar.md:33`). Under CommonMark a CRLF is a single line ending. This is recalled from CommonMark section 2.1 and was not re-verified, because the sandbox has no network.
- It is the only registry-CRLF expectation in the lane. The in-gate selftest CRLF case (`tools/research-gate.sh:5865-5868`) is entry-side only.

## Q2: mutate the targeted fix; does the control fail for the intended reason?

Targeted fix: the landed CR-sensitive row parse and width matching in `metadata_registry_load` (`research-gate.sh:2430` CR strip; `:2439-2440` row trim; `:2466` width compare; `:2490` `header_width`). The scout rationale for the control is `.ufo/waves/round-27/build/ScoutMetadataHeader.md:218-221`: a width check computed from raw text must fail CRLF.

Harness: identical environment and argv to `regressions.py` `run()` (`CHOUSA_*` removed, `CHOUSA_STRICT=0`, `LC_ALL=C`; `bash GATE verify-metadata ENTRY --root ROOT --registry REG`; cwd = ROOT).

| sandbox mutant | edit (line numbers from landed) | valid-crlf result | LF twin result | reading |
|---|---|---|---|---|
| landed | none | rc 0, 1 verdict: PASS | rc 0 | baseline |
| A | CUT 2430 (explicit CR strip) | rc 0: PASS | rc 0 | equivalent: the `[[:space:]]` trim removes CR anyway |
| B | CUT 2466 (width compare) | rc 0: PASS | rc 0 | not caught; `crlf-delimiter-short` gives rc 0 instead of 2 |
| D | CUT 2430 and CUT 2439-2440 | rc 2, 0 verdicts: FAIL (`exit 2 != 0`, `count ^RESEARCH_GATE: 0 != 1`) | rc 0 | intended CR failure: CR stays in the last cell, giving a phantom 4th cell `[$'\r']`; the separator regex fails; "no table" |
| E | CUT 2439-2440 (row trim only) | rc 0: PASS | rc 2 (`lf-edge-ws`) | not CR-specific; caught only by edge-whitespace inputs |
| R | raw-length width compare (3 edits) | rc 2: FAIL | rc 2: FAIL | fails every table; not CR-specific |
| F | CUT 2657 (entry-side CR strip) | rc 0: PASS (control unchanged) | n/a | entry strip is redundant on tested inputs; `entry-crlf-*` unchanged |

Mutant sha256 (first 8 hex): A `5b202d8c`, B `5f8d29a0`, D `d214dd6c`, E `b493261d`, R `8c7173b1`, F `96408000`. Each `diff` against landed matched the intended change (exit 1 is the expected "files differ").

Conclusion: the control fails for the intended reason only under joint removal (D). Each single CR mechanism survives. The width repair (B) is not guarded by this control at all.

Harness sanity: `Path.write_text` keeps the bytes (`b'| id | status | used-by |\r\n|---|---|---|\r\n'`), so the fixture really is CRLF and the failure is not a setup artifact. Under `LC_ALL=C`, bash trim of `'| a |\r'` yields `| a |`, confirming CR is whitespace to the trim.

## Q3: nearby synthetic counterexamples

Each row is one gate invocation on the sandbox copy.

- **N1, control vacuous for edge whitespace (mutant E).** `valid-crlf` passes. The CRLF fixture with 2-space indent and trailing spaces, `  | id | status | used-by |  \r\n|---|---|---|\r\n  | S001 | mined | corpus/knowledge/entry.md |  \r\n`, gives rc 2 "no table". The LF version also gives rc 2. No registry line in the 58 controls has leading or trailing whitespace (`regressions.py:54-55, 133-142, 151, 197, 206`), so no registry control exercises this mechanism. [INFERENCE from reading; suite not run.]
- **N2, control vacuous for width (mutant B).** `valid-crlf` passes. `crlf-delimiter-short` (2-cell delimiter) gives rc 0, expected 2. The base LF twin is also rc 0, so the LF delimiter controls (`regressions.py:138`) are the real guard.
- **N3, inherited lenient: bare CR (landed and base both rc 0, CLEAN).**
  - `| id | status | used-by |` / `|---|---|---|` / `| S001 | mined\r| corpus/knowledge/entry.md |`
  - `| id | status\r| used-by |` / `|---|---|---|` / ROW
  - `|---|---|---|` / `\r| S001 | mined | corpus/knowledge/entry.md |`

  Under CommonMark a bare CR ends a line, so GFM would split the row or end the table. This is not declared and is inherited, not a C3 regression. Low severity: it needs a stray CR byte mid-line.
- **N4, inherited lenient: double CR.** A table with `\r\r\n` endings gives rc 0 on landed and base. CommonMark sees a blank line between header and delimiter, so it would not be a table.
- **N5, inherited strict: lone CR.** A CR-only (classic Mac) table gives rc 2 "no table" on both. CommonMark would accept it.
- **N6, changed by the repair: BOM.** `\xEF\xBB\xBF` plus an LF or CRLF table gives landed rc 2 "no table" (base rc 1, `META_SOURCE_ROW_MISSING`). No false clean was found. The exit class changes from finding (1) to usage (2), and the message does not mention the BOM. It is contract-consistent only if the BOM counts as a header cell. A BOM-stripping reader would accept the table. Low severity; not declared.
- **N7, holds.** On landed, 16 of 16 CRLF/LF pairs give identical rc, verdicts and findings (`probe/invariance_probe.py`). Base gives 16 of 16 too. Repair-level changes on CRLF inputs are the intended ones: `crlf-delimiter-short` 0 to 2 (width), `crlf-prose-break-stale-header` 0 to 2 (base false clean), `crlf-prose-break-reorder-clean` 1 to 0 (base false positive).

## Harness observations

- `observe()` checks only rc, verdict count and listed tokens. There is no forbidden-FINDING check, so a non-rc-affecting (info) finding on CRLF input would pass. No such mutant was found. [INFERENCE]
- The two explicit CR strips (`:2430`, entry `:2657`) are behaviourally redundant on every tested input. `valid-crlf` cannot separate them from the trim.

## Limits

- Did not run `--selftest`, the regression script or any L1-owned command. The 58/58 and 210/210 figures are L1's and were not re-observed. The control was replicated by a single-control probe with identical environment and argv.
- Suite-level claims (N1 survival of E; B guarded by LF controls) come from reading `regressions.py` and from the LF analogue runs, not from a full run.
- CommonMark statements are from memory. No network was used.
- Equivalence claims for A and F hold on tested inputs. The registry-side argument follows from `[[:space:]]` containing CR.

## Commands and exit codes (key)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC3ValidCrlf35`: exit 0; gate sha256 `ca39d14d...` (matches).
- `git ... archive 64eec5d41c7cf7f17f5ce1e968e28b3769952596 tools/research-gate.sh | tar -x -C ...-base`: exit 0.
- `python3 probe/crlf_probe.py --gate <gate> [--only ...]` on landed, base, A, B, D, E, R, F: harness exit 0 each. Per-case gate rc is as tabled above.
- `python3 probe/bare_cr_probe.py`: exit 0. `python3 probe/trim_probe.py`: exit 0. `python3 probe/invariance_probe.py <landed|base>`: exit 0; compared 16, mismatches 0 on each.
- `diff tools/research-gate.sh mut/<X>/tools/research-gate.sh`: exit 1 for each mutant, showing only the intended lines.
- Mutant edits were anchored `edit` operations on sandbox copies only. No lane file was modified.

Install record: none. Only existing tools were used (bash 5.3.20, python3, git, tar, diff, cp).

## Author-lane advice (not an outside admission)

1. Add synthetic controls for CRLF with edge whitespace (indent, trailing spaces and tabs), for mixed line endings, and for a CRLF 2-cell delimiter width negative. Each of mutants B, D and E fails at least one of them.
2. Add a forbidden `^FINDING ` assertion to valid-table controls, so a CR-induced info finding cannot pass silently.
3. Declare the line-ending, BOM and bare-CR policy in the registry contract (Claim 3 or `SOURCES.md`). Then the CRLF expectation becomes contract-derived rather than inherited. Refuse bare CR and BOM with a precise diagnostic, instead of the generic "no table".
4. Delete the redundant explicit CR strips, or keep them and document them as belt-and-braces. The control cannot test them separately.

## Errata (appended after writing; the body above is unchanged)

- Q2 table, mutant E row: the "LF twin result" cell should read `rc 0` (`lf-twin`, PASS under E). The `rc 2` observed under E is for the edge-whitespace fixture `lf-edge-ws`, which is the N1 evidence. Mutant E therefore passes the control's own LF twin, as it passes the CRLF control.
- Commands section, `diff` line: exit 1 was observed directly only for the F diff. For A, B, D, E and R, `diff` printed only the intended lines (`diff` exits 1 when files differ; the individual exit codes were not captured).

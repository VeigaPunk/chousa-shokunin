# FC2AsciiCli falsify: control `ascii-cli-C-2026-10-2１` (C2, freshness)

Scope: round27 attempt1 falsify wave. Leaf member `ChousaR27.FC2AsciiCliC202610223-11`. Author-lane advice, not an outside admission.

- Revision attacked: `dd72641e574679c4f7882dd43de072b4c8892d6f` (master). Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`, matches the pin.
- Base for before/after: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, gate sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
- Sandbox: `/tmp/chousa-r27-falsify-FC2AsciiCliC202610223/` (landed extract), `…-base/` (base extract), `probe/` (mutants, probes, outputs in `probe/out/`).
- Lane untouched: read-only git only (`cat-file`, `archive`, `rev-parse`). No index, branch, or production file changed.

## Verdicts

| Axis | Verdict | Basis |
|---|---|---|
| Item `ascii-cli-C-2026-10-2１` | **FALSIFIED** | Still PASSes with the locale repair reverted (m1). Its failure paths under the harness's own call shape are a decode crash (m2, m6) or a wrong-reason mismatch (m4). |
| Operability | **FALSIFIED** | Harness `run()` decodes gate output strictly (`text=True`). Bash's arithmetic diagnostic can end in a partial UTF-8 sequence, so `UnicodeDecodeError` aborts the whole run, base included. |
| Freshness (landed date-input repair) | **HOLDS** on every tested input | 85/85 CLI rows across 5 locale settings correct. Entry-side Unicode digits rejected under all tested locales. Coverage gap noted in 4f. |
| Calibration | **FALSIFIED** for this control | Expectation only partly contract-derived (required message is a copied gate literal). A wording-only edit flips it. A reject-all gate passes it. The C variant is not a locale discriminator. |

Adjacent finding, outside C2's declared date scope and unchanged from base: the claims-JSON decoder is locale-dependent (4g).

## 1. Item and declared expectation

- Harness: `corpus/evidence/round27-regressions.py:123-128`. Loop `for locale in ('C','en_US.UTF-8')` over tokens `('２０２６-10-21','٢٠٢٦-10-21','2026-10-2１')`. Name `ascii-cli-{locale}-{token}`. Target = locale `C`, token bytes `323032362d31302d32efbc91` (`2026-10-2` + U+FF11 FULLWIDTH DIGIT ONE).
- Expectation (`:125-128`): exit 2; output contains `--as-of must be a valid YYYY-MM-DD date`; output lacks `invalid integer`, `arithmetic syntax`, `cannot change locale`; zero `^RESEARCH_GATE: ` lines.
- Environment: `env.update(CHOUSA_STRICT='0', LC_ALL='C')` (`:28`); per call `env | {'LC_ALL': locale}`; `subprocess.run(..., text=True, capture_output=True, timeout=30)` (`run()` `:60-67`).
- Targeted production fix: landed `metadata_iso_date` begins with `local LC_ALL=C` (`tools/research-gate.sh:2311`), reached from the CLI check at `:6575`. Base has no pin.

### Q1: derived from the declared contract, independent of gate code?

Partly (3 of 4 components).

- Exit 2 and no verdict on a usage error: declared. `corpus/evidence/round27-claims.md:7` ("expected exit2"; "allowing an actual verdict on a usage error") and `.ufo/evidence/round-1/wave-plan.json:475` ("exit 2 setup/usage"). Independent of gate code.
- Non-ASCII digit rejected under any locale: declared (`round27-claims.md:11`). Independent.
- Forbidden bash diagnostic phrases: failure-mode names, independent of gate text.
- Required message `--as-of must be a valid YYYY-MM-DD date`: **not declared**. The claims file specifies no wording. The string is the gate's literal at `tools/research-gate.sh:6575`, duplicated in the gate's own selftest at `:6131`, `:6321`, `:6329`. A contract-neutral wording edit (m4) turns the control into a wrong-reason MISMATCH.

## 2. Mutation evidence (Q2)

Sandbox mutants of the landed gate. Each is one hunk (`diff -u landed.sh mN.sh`). All pass `bash -n`.

- m1: delete `local LC_ALL=C` at `:2311` (revert the locale repair).
- m2: day group `([0-9]{2})` changed to `(.+)` at `:2312`, pin kept (grammar loosened).
- m3: insert `return 1` after `:2311` (reject every `--as-of`).
- m4: `:6575` wording changed to `--as-of must be YYYY-MM-DD`.
- m6: `:6575` check replaced with `:` (no CLI validation).
- m8: delete `local LC_ALL=C` at `verify_metadata` `:2564` (entry-side pin).

sha256: base `c2c813f1…2fe1…` (full value above); m1 `50276d47…46cf3`; m2 `540879e4…4c6ebc4f5`; m3 `2f618e69…5b88067`; m4 `2b195e8a…7977c8c`; m6 `351e66cd…06c43e`; m8 `e64ef599…4b5ca617a2852b1e30902e1132ec4f014b08477`. Full values are reproducible from the sandbox files.

Outcome of the target and its sibling under the harness call shape. "crash" = `UnicodeDecodeError` raised out of `subprocess.run(text=True)`.

| gate | target: C, `2026-10-2１` | sibling: en_US.UTF-8, same token |
|---|---|---|
| base | PASS (rc 2) | crash, byte 233 |
| landed | PASS | PASS |
| m1 (revert) | **PASS** (rc 2) | crash, byte 229 |
| m2 (day grammar) | crash, byte 229 | crash, byte 229 |
| m3 (reject-all) | PASS (vacuous) | PASS (vacuous) |
| m4 (wording) | MISMATCH rc 2, message absent | MISMATCH rc 2, message absent |
| m6 (no CLI check) | crash, byte 74 | crash, byte 74 |
| m8 (entry pin) | PASS | PASS |

Diagnostic rerun with `errors='replace'` (`probe_c2.py`, rc 0): base en_US day gives rc 1 `10#2１: arithmetic syntax error`; m1 en_US day gives rc 1, same; m2 C day gives rc 1 `arithmetic syntax`; m6 C day gives rc 1, same. These are the intended-reason failures, but the harness cannot record them.

**Answer to Q2: no.** Reverting the targeted fix leaves the target PASSing. Its only non-pass outcomes under the harness are wrong-reason (m4) or decode crashes (m2, m6). The en_US sibling is the true discriminator for m1, but it fails by crash on base and on m1.

## 3. Nearby inputs (Q3): landed correct

`probe_c2.py` group G2: 17 inputs × 5 locale settings (C, en_US.UTF-8, C.UTF-8, POSIX, LANG-only en_US.UTF-8), run on base and landed.

- Inputs: the 3 harness tokens; fullwidth day-both `2026-10-２１`; month-first `2026-１0-21`; year-first `２026-10-21`; superscript two; Arabic-Indic three; Devanagari one; fullwidth hyphens; trailing `\n`; trailing ZWSP; math-bold two; digit plus combining acute; leading space; `2026-02-30`; `2026-10-21` (accept).
- landed: **85/85 correct**. base: 20/85 wrong, all under en_US-collation settings (en_US.UTF-8, LANG-only). C.UTF-8 and POSIX clean on base.
- Byte-exact check (`probe/rx_shapes.sh`): under en_US, `^[0-9]$` matches U+FF11 but not U+FF19. Base failures confirm that superscript two, Arabic-Indic three, Devanagari one, and math-bold two are admitted. The admitted set is code-point specific. The control's token is admitted, so it is a real discriminator for the en_US row.
- Entry side (`verify_metadata`, pinned): `verified-at: ２０２６-01-02` gives rc 1, DRIFT, `verified_at=undated`, `META_VERIFIED_AT_UNDATED`, under C, en_US, and LANG-only. The ASCII control gives rc 0.
- Date helpers `metadata_days_from_civil` (`:2326`), `metadata_days_from_iso` (`:2354`), and `metadata_add_days` (`:2359`) are reached only from pinned scopes (`:2356`, `:2372-2377`, `:2575`, `:2780`).

## 4. Counterexamples (minimal)

**a) Locale vacuity.** With m1, `LC_ALL=C bash probe/m1.sh verify-metadata <entry> --root <root> --as-of "2026-10-2１"` gives exit 2 and the required message, so the target PASSes with the repair removed. Under `LC_ALL=en_US.UTF-8` the same command gives exit 1 and `10#2１: arithmetic syntax error`.

**b) Acceptance vacuity.** m3 (every `--as-of` rejected) passes the target. Within this probe only the companion row `--as-of 2026-10-21` exposes m3 (rc 2 MISMATCH under C and en_US). [INFERENCE: the suite's `date_cases` would also expect acceptance; not executed.]

**c) Decode crash on the control's own failure output.** `subprocess.run(['bash', probe/m6.sh, 'verify-metadata', entry, '--root', root, '--as-of', '2026-10-2１'], text=True, capture_output=True, timeout=30)` raises `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xef in position 74`. Bash printed `10#2\xef: arithmetic syntax error…`, cut mid-character. m2 gives the same failure at byte 229.

**d) Sibling crashes base.** `base.sh`, `LC_ALL=en_US.UTF-8`, day token: `UnicodeDecodeError` at byte 233. The yr and arabic en_US rows return clean rc 1 MISMATCH first; the day row aborts. The abort skips every later control (the C3 block at `:131+`) and the JSON write at `:225-236`. Path length does not matter: a 265-character path still crashes (byte 645). [INFERENCE for skipping later controls: from `run()` `:60-67`, whose only handler is `TimeoutExpired`. The crash itself was reproduced.] The planned "run unchanged on an isolated base archive" therefore cannot complete as written, and the planned skip (the long-token crash) does not cover this row.

**e) Wording coupling.** m4 gives rc 2 with the message absent, for all three tokens under C and en_US. A contract-neutral edit is reported as a mismatch.

**f) Entry-side blind spot (landed correct; suite blind).** With m8 and `LC_ALL=en_US.UTF-8`, minimal entry `verified-at: ２０２６-01-02 checked synthetic fixture` run through `verify-metadata <entry> --root <root>` gives rc 0, `RESEARCH_GATE: CLEAN`, `verified_at=dated`. Landed gives rc 1, DRIFT, undated. With `--as-of 2026-10-21`, m8 gives CLEAN with `freshness=unknown`. An ideographic-space prefix (`verified-at: \u3000 2026-01-02`) also flips under m8 (CLEAN, dated). The after-receipt (`corpus/evidence/round27-regressions-after.json`, 58 results: C1 6, C2 21, C3 31) contains no Unicode entry input. The six Unicode rows are all CLI `--as-of` and they pass m8 (observed). [INFERENCE: none of the other 52 controls can detect m8, since their entry content is ASCII by inspection.]

**g) Adjacent, outside C2's declared date scope; landed identical to base.** The claims-JSON path has no pin: `json_str` (`:1061`, `"key"[[:space:]]*:`), the `json_unescape` hex test (`:1090`, `[0-9A-Fa-f]{4}`), and `verify_claims` (`:1330`). Minimal claims lines, run as `verify-claims <file> --root <root>`:

- `{"id": "A\u００41", "source": "src.md", "span": "The span text", "expect": "supported"}` (fullwidth hex escape): en_US gives rc 1, no `RESEARCH_GATE` line, stderr `16#: invalid integer constant`. C gives rc 0 CLEAN.
- `{"id"\u3000: "C1", "source": "src.md", "span": "The span text", "expect": "supported"}` (ideographic space before colon): en_US gives rc 0 CLEAN (`id=C1`). C gives rc 1 DRIFT (`missing id`).
- ASCII control `\u0041`: identical across all four runs.

## 5. Limits and non-run items

- Ran single gate invocations and probe matrices only: `probe_c2.py` (279 rows, 2.49 s), `probe_adj.py`, `probe_adj2.py`, `probe/rx_shapes.sh`. Did not run `--selftest` or the 58-control script. The crash matrix reproduces the harness call shape, not the harness file.
- `probe_adj2.py` sections 1–2 used an argv single-character helper whose return code I misread (0 = match). That section is superseded by the byte-exact `rx_shapes.sh`. No conclusion depends on it.
- Entry-side coverage inference: the other 52 controls were not executed.
- Host: bash 5.3.20, glibc 2.44, python 3.14.8. Locales present: C, C.utf8, en_US.utf8, POSIX. de_DE absent: `LC_ALL=de_DE.UTF-8 bash` prints `cannot change locale (de_DE.UTF-8): No such file or directory` and continues in C. The harness forbids `cannot change locale`, so on such a host en_US rows would record MISMATCH rather than setup exit 2 [INFERENCE]. The gate's own selftest skips the Unicode-locale case there (`tools/research-gate.sh:6307-6327`); the regression control has no skip.
- The decode crash depends on a UTF-8 preferred encoding in the runner (true on this host).
- Tools: none installed or updated. Used host bash, python3, git, diff, sha256sum, timeout. No pacman, network, `/proc`, strace, debugger, or subagents.

## 6. Author-lane advice (not an outside admission)

1. Re-scope the C variant as an ASCII-grammar guard under C. Keep the en_US rows as the locale discriminator, after fixing item 2.
2. Harness: decode with `errors='replace'` (or keep raw bytes) and catch per-row exceptions, so a decode failure becomes a MISMATCH row. As written, one failing row aborts the whole run, including the base run.
3. Replace the literal-message match with contract checks: rc 2, zero `RESEARCH_GATE:` lines, and one diagnostic naming `--as-of`.
4. Add an acceptance companion beside each rejection row in the family (for example `2026-10-21` accepted and classified), so reject-all cannot pass.
5. Add entry-side Unicode rows under en_US: `verified-at: ２０２６-01-02` gives rc 1 undated, and an ideographic-space prefix gives undated. These detect m8.
6. Pin or ASCII-restrict `json_str` and `json_unescape`, or document claims JSON as outside the ASCII contract. Add the two claims rows from 4g.
7. Align the locale-missing policy with the selftest (skip with reason, or setup exit 2), not a mismatch.
8. For L1: run the regression script on base to confirm the day-row abort (4d), and on landed to confirm no decode path is hit. Full selftest and the 58-control run remain L1's.

## Addendum (appended after write)

Full sha256 of the sandbox gate copies used in section 2. The abbreviated forms there are unreliable; use these.
- base (64eec5d4): `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
- landed (dd72641e): `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`
- m1: `50276d4780b11fa24be38f4d4c9297ff3972096ff55b8605bc85f48c8af46cf3`
- m2: `540879e4044f1817e1286dfe7b3e84193daa089ee548cb66b6e5b510c6ebc4f5`
- m3: `2f618e6912d5fd058922a7a8d92f2fe3c236d8d37235c78efca265f5e3b88067`
- m4: `2b195e8ab365974b4341092648e594d7edd61f940ebe46342cfc4683b7977c8c`
- m6: `351e66cd820d132b0e7bda4d9079f927e01e99d75153ef4e873c7272ba06c43e`
- m8: `e64ef5999ed93cf2b7e5651984b5ca617a2852b1e30902e1132ec4f014b08477`

Line references `:28`, `:60-67`, `:123-128`, `:131+`, and `:225-236` in sections 1 and 4 point to `corpus/evidence/round27-regressions.py`, not to the gate.

The harness-call crash matrix (section 2) and the path-length check (4d) were inline Python replications of `subprocess.run(..., text=True, capture_output=True, timeout=30)`. They were not saved as files. Saved artifacts: `probe/out/probe_c2.jsonl`, `probe/out/probe_adj.txt`, `probe/out/probe_adj2.txt`, and the mutants in `probe/`.

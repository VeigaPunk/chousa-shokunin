# ScoutSkillTally — SKILL.md self-test tally (round 35, wave 2)

Access date 2026-10-23. Clone `/tmp/hyaku/chousa-r35/w2/ScoutSkillTally/clone` at `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`. Gate sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (`sha256sum` on the clone's `tools/research-gate.sh`). No installs. SKILL.md at that revision is 591 lines; `git diff --stat e87c5d7 HEAD -- SKILL.md tools/research-gate.sh` printed nothing.

## Verdict

The current self-test tally calibrates. `--selftest` on this host is exactly `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, exit 0, and every case range the Gates table states matches the executed numbers. Round 35 did not add a selftest case, so those `256` cells must not be bumped.

What SKILL.md does not yet name, and what the L1 has to add, is the grep pin and `tools/mechanism-witness.py`. Those are not a selftest-count edit.

## Selftest banner (ran)

```
cd /tmp/hyaku/chousa-r35/w2/ScoutSkillTally/clone
TMPDIR=/tmp/hyaku/chousa-r35/w2/ScoutSkillTally/selftest-tmp \
  timeout 1800 bash tools/research-gate.sh --selftest
```

Exit 0 (`waitpid` status 0). Stderr empty. Stdout sha256 `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12` (258 lines, 12781 bytes, still at that `/tmp` path). Last line: `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`. 256 `ok-case`, 0 `FAIL-case`, 0 `skip-case`, numbers 1..256 with no gap. Index: `.ufo/waves/round-35/w2/ScoutSkillTally/selftest-cases.txt`.

The skip suffix is host-dependent (userns, `/etc/hostname`, flock, a Unicode-digit locale). This run skipped none, so the hardcoded `, 0 skipped` matches here.

Round 35's grep pin (`research-gate.sh:332-399`, `grep_pin_init` called at `:8039`) has no selftest case. Executed 252-256 are the round-34 cases the comments name (`:7899` cases 252-253, `:7932` cases 254-256).

## Case ranges per Gates row (executed names)

All of these match SKILL.md lines 77-84. The `research-gate` row (line 77) states only the banner, not 1-20; those ten `pass-*` / `fail-*` cases plus two `setup-*` are the structure family.

| row | SKILL.md | claimed | executed names (ends) |
|---|---|---|---|
| verify-claims | 78 | 21-30, 41-42 | `claims-pass` … `setup-claims-missing-file`; `claims-boundary-pass/fail` |
| verify-claims r31 | 78 | 216-219, 220-228 | `c1-pass-bound` … `c1-pass-no-line`; `claims-sha-absent` … `claims-sha-crlf` |
| verify-claims r32 | 78 | 235-241 | `claims-r2-sha-nonstring` … `claims-r2-nested-string` (240 is `r2-hash-fault-shim`) |
| verify-claims r33 | 78 | 242-248, 249-251 | `r33-top-nested-line` … `r33-top-dup-id`; `r33-post-literals` … `r33-post-escapes` |
| verify-claims r34 | 78 | 252-253, 254-256 | `claims-longspan`, `claims-longspan-line`; `claims-deadzone`, `-line`, `-edge` |
| verify-chain | 79 | 31-40, 43-44, 229-232 | `chain-pass` … `setup-chain-missing-file`; `chain-pass-boundary`, `chain-fail-boundary`; `chain-exempt-resolvable` … `chain-exempt-mixed` |
| verify-sweeps | 80 | 45-54 | `sweeps-pass` … `setup-sweeps-missing-file` |
| verify-integrity | 81 | 65-73 | `integrity-pass` … `setup-integrity-missing-file` |
| verify-all | 82 | 55-64, 74, 134-136, 233-234 | fixture filenames (`all-pass.md` repeats; 64 `no-such-record.md`); 74 `all-dangling.md`; `json-unterminated-manifest`, `json-nul-terminated-manifest`, `json-unreadable-manifest`; `c1lk-holder-blocks-append`, `c1lk-second-append` |
| verify-metadata | 83 | 137-208, 210-215; 209 is a claims control | 137 `metadata-clean` … 208 `metadata-ordinary-colon-allowed`; 210 `metadata-asof-all-zero-cadence` … 215 `metadata-asof-usage-matcher-fault`; **209 `claims-registry-colon-deny`** |
| --pin/--drift | 84 | 75-85 | `pin-clean` … `setup-pin-drift-exclusive` |

Prose ranges that also match this run: line 107 cases 86-92 (`scope-fail-bounty` … `scope-pass-prose-decoy`) and 112-116 (`scope-fence-shadow` … `scope-fence-unclosed`); line 111 cases 93-94 (`banner-pin`, `drift-banner-version`); line 109 cases 95-98; line 113 cases 99-102; line 115 cases 103-106; line 117 cases 107-111.

Cases the table and the prose do not name: **117-133**. Gate comments (`research-gate.sh:6136`, `:6155`, `:6207`, `:6215`, `:6232`, `:6321`, `:6340`) describe them, but the r22/r23 comments disagree with execution order. Comment "133 (r23)" at `:6321` runs as **129 `chain-fence-anchor`**. Comment "129-132 (r22)" at `:6340` runs as **130-133** (`claims-config-start`, `claims-omp-start`, `claims-localstate-start`, `claims-config-adjacent`). Same class as the round-34 comment bug, and SKILL.md does not cite these numbers, so no SKILL line is false. Do not copy 129-133 from the comments into SKILL.md.

Historical banners (lines 94, 156, 179, 215, 252, 299, 343-344, 395, 527, 546) sit in round narratives. Not re-run. Line 344's "cases 65-74 are the integrity family" is the round-7 story; the current table correctly splits 65-73 integrity and 74 verify-all.

## Round-34 counter rows (committed bytes)

Denominators, from `CLASS_COUNTS` summed in the counter source (asserts hold): `c1-count-v3.py:120-140` TOTAL 42, label `LONGSPAN_MATCH`; `c2-count.py:71-91` TOTAL 37, label `DEADZONE_MATCH`. Older frozen counters stay 30 and 40 (`c1-count.py:91`, `c1-count-v2.py:116`). SKILL.md lines 89-90 quote 42/42 and 37/37. That matches.

Line 89 before/after, from receipts (not re-run):

- `43a1af35…` seed 3493: `LONGSPAN_MATCH=25/42` (`.ufo/waves/round-34/controls/L1-base-v3/base-v3-C-s3493.json`). Seeds 3491 and 3492: `0/42`, `gate_timed_out` (same dir; `NOTE.md` says default locale). SKILL says "0/42" once; the note records two seeds.
- `772a1d8e…` seeds 3601, 3602, 3603: `42/42` (`.ufo/waves/round-34/measure/c1v3-s360{1,2,3-utf8}.json`). That is the x3.
- `a6307edf…` seeds 4601-4604: `42/42` (`w2a2/ExecC1RerunA2/c1v3-a2-s460{1,2,3,4-utf8}.json`). Locales are in `ExecC1RerunA2.md:43-46`, not in the receipt schema.

Line 90, from `.ufo/waves/round-34/w2a2/CritC2AxisFit/committed-receipts.json`: `772a1d8e` seeds 5011 and 5023 are `DEADZONE_MATCH=21/37`; `a6307edf` seeds 5011, 5023, 5033, 5047 are `37/37`.

## Lines the L1 must change (pin paragraph and witness)

Round-35 surfaces are absent. A search of SKILL.md for `RESEARCH_GATE_GREP`, `GATE_GREP`, `mechanism-witness`, `round-35` is empty. Do not edit the `PASS (256 cases, 0 skipped)` cells on lines 77-84 or the round-34 clause on line 92; this run still prints that banner.

Insertion point is the blank line 91, between the last Gates row and the historical paragraph.

- Line 90 current text (keep): `research-gate round-34 attempt-2 counter` … `DEADZONE_MATCH=37/37` … `21/37 on seeds 5011/5023` … `37/37 x4 (seeds 5011, 5023, 5033, 5047)`.
- Add a row whose entry is `python3 corpus/evidence/round35/c1-count.py` and whose verdict cell is `GREP_PIN_MATCH=9/9` (`c1-count.py:48-49`, print at `:283`; nine scenarios S1-S9 in the module docstring). Refusal text in the gate is `research-gate: GREP_PROVENANCE refused:` (exit 2); echo is `GATE_GREP: path=... source=default|override version="..."` (`research-gate.sh:354`, `:397`). The shared `--selftest` does not exercise this.
- Add a row naming `tools/mechanism-witness.py` and `python3 corpus/evidence/round35/c2-count.py`. The counter prints `WITNESS_SEPARATED=%d/%d OUTPUT_EQUIV=%d/%d LANDED_WITNESS=%s` (`c2-count.py:191-193`); absent battery prints `WITNESS_SEPARATED=0/2 battery=absent` (`:157`).
- Line 77 pinned-values cell is the other place a one-line pin belongs. Current cell (keep the self-test half): `expected exits/finding IDs in tools/research-gate.sh; archive digests/expected verdicts in corpus/evidence/round-1/expected.json`. It does not name the grep binary.
- Line 92 current parenthetical ends `round 34: they now read PASS (256 cases, 0 skipped)`. A round-35 clause may say the tally is unchanged. It must not replace 256.

Do not reuse these as the pin paragraph; they are different pins:

- Line 67: a `"sha256"` pin on claim source bytes (`CLAIM_SOURCE_REVISION_MISMATCH`).
- Line 84: `research-gate --pin / --drift`, cases 75-85, behavioral baseline, not the grep binary.
- Lines 125-126: `The old "unchecked grep" diagnosis is superseded` — round-1 `emit_finding` errexit, not PATH resolution.

Adjacent stale pointer, not a selftest tally and already wrong on the pre-pin gate: line 117 says `in_root()` is `tools/research-gate.sh ~:612`. Landed definition is line 834; base gate (`repairs/base-gate.sh`, sha `a6307edf…`) has it at line 765.

## Limits

Historical PASS counts were not re-run. Round-34 counter numerators were read from committed receipts, not reproduced. Skip-count 0 is this host. Gate comments at `:6321` and `:6340` are not SKILL.md defects.

# ScoutC1Counter — c1-count.py, 14 scenarios

Access date: 2026-10-23. Counter read whole (681 lines). No counter execution. No install.

**VERDICT:** No measured 14/14 bypass. Three scenarios can pass without the behaviour their own text names: S9 (recorder log never read), S8 (default identity is an echo string), S7 (one matcher argv covers three claims). Reference A/B cannot be skipped into a pass; reference A can be met by a constant printer.

## Files opened

| path | sha256 | notes |
|---|---|---|
| `corpus/evidence/round36/c1-count.py` | `3fefffe745ed10d2fd06c4c3cc9073ab7bfb46dd82e32c166976fd3aaf4c35be` | whole file, lines 1–681 |
| `corpus/evidence/round36/claims.md` | `ca2c952b0ddb831eaa08cab9a41094dc122aa9d512638c88dbadc4fad587badf` | C1 text, limits 119–135, erratum heading 157 (no body) |
| `tools/research-gate.sh` | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | pin 369–420, `sha256_hex_file` 432–443, drift id 3945–4047. Matches the landed-gate pin. |
| `.ufo/waves/round-36/controls/base-gate-r36.sh` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` | hashed only; not scored |
| `.ufo/waves/round-36/w1-briefs/ScoutC1Counter.md` | (not hashed) | assignment |

`git rev-parse master` → `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (wave base).

## Commands

1. `sha256sum corpus/evidence/round36/c1-count.py corpus/evidence/round36/claims.md tools/research-gate.sh .ufo/waves/round-36/controls/base-gate-r36.sh && git rev-parse master && wc -l corpus/evidence/round36/c1-count.py` — exit 0. Deciding line: gate sha256 `a7d3922c…54e8`; counter `681` lines.
2. `python3` `json.dumps` of fixture C's row — exit 0. Deciding line: `span` is `caf\u00e9` (`ensure_ascii` default).
3. `sha256sum .ufo/waves/round-36/w1/ScoutC1Counter/scenario-table.json` — exit 0. Deciding line: `4254bec0b7c8ed6d71fe8d2e393ed8da8531613cd824635a537c44c73eb46249`.

## Shared machinery (every `same_as_a` scenario)

`same_as_a` (441–443) is not byte equality. `parse` (336–343) keeps a DRIFT boolean (`RESEARCH_GATE: DRIFT` prefix) and `{id: (observed, verdict)}` from `LINE_RE` (75). `expected=` is matched and discarded. Fixture A (89–109) is seed-independent: span is the fixed word list at 92–93; K2 flips the last character (97); K3 is the same span in `leadQ…` (98–104).

`run_gate` (324–333) drops `CHOUSA_*` and `RESEARCH_GATE_*`, then applies the scenario env. S13/S14's `--drift` does not use `run_gate` (633, 652).

## 14 scenarios

| id | name | fixture | assertion | pass condition | lines |
|---|---|---|---|---|---|
| S1 | `S1-shim-first-path` | A; PATH = shim dir + clean path. Shim (200–204) appends `$*` to trip1 and execs `/usr/bin/grep`. | Shim never fires; stdout matches reference A. | `trip_empty(trip1) and same_as_a(rc, out)` | 448–454 |
| S2 | `S2-bash-env-function` | A; `BASH_ENV` = `grep()` that logs to trip2 then `command /usr/bin/grep` (215–218). | Function never called; output matches reference A. | `trip_empty(trip2) and same_as_a(rc, out)` | 455–461 |
| S3 | `S3-no-grep-on-path` | A; PATH = symlink farm of the name list at 466–469, grep omitted. | Absolute pin needs no PATH grep. | `same_as_a(rc, out) and "not found" not in err` | 462–482 |
| S4 | `S4-override-relative` | A; `RESEARCH_GATE_GREP=bin/grep`. | Relative override refused before a match. | `rc == 2 and "GREP_PROVENANCE" in err` | 483–488 |
| S5 | `S5-override-missing` | A; `RESEARCH_GATE_GREP` = scratch `absent-grep`. | Missing override refused. | `rc == 2 and "GREP_PROVENANCE" in err` | 489–495 |
| S6 | `S6-override-non-gnu` | A; stub (207–212) logs `stub $*`, prints `SHIM_VERSION` on stderr for `--version`/`-V`, else exit 0. | Refused, and the stub is called once, argv tail `--version`. | `rc == 2 and "GREP_PROVENANCE" in err and stub_version_only` (501) | 496–505 |
| S7 | `S7-override-distinct-path` | A; recorder A (221–237) as override; `CHOUSA_GREP_PIN_ECHO=1`. | Output equal, echo fullmatches path/source/live version, recorder got the matcher calls. | `same_as_a and echo == want and len(rec_matches) >= 1` | 506–520 |
| S8 | `S8-default-echo` | A; echo on; no override. Version = first line of `/usr/bin/grep --version` (else `/bin/grep`) (522–523). | Default echo names that path, `source=default`, and the live version. | `same_as_a and echo == want` | 521–531 |
| S9 | `S9-override-beats-shim` | A; `BASH_ENV` + recorder A + echo on. Log truncated (534). | Docstring 29–31: function gets nothing **and the recorder receives the matches**. | `trip_empty(trip2) and same_as_a and echo == want9` | 532–545 |
| S10 | `S10-semantic-canary` | B (112–136): seeded long span 32765..32767 plus short span, both `expect=supported`. Landed recorder B. k1 gate inserts python exact-search before the long-span branch (346–377, 560–566). | Every record attributed on the landed recorder; k1 stays output-equal and does not attribute the long id. | `ref_b and len(landed_attr)==len(spans_b) and k1_long_missing and k1_same and syntax.returncode==0` | 546–584 |
| S11 | `S11-manifest-hash-shim` | D (150–197). PATH puts a `sha256sum` that prints `HOSTILE-CUT-OUTPUT  -` first (590–591). `verify-all --json`. | Both sha fields are 64-hex and equal `hashlib` of the record and the gate file. | `rc == 0 and man_ok` (604–609) | 585–612 |
| S12 | `S12-locale-c` | C (139–147): file `lead caf\xc3\xa9 tail\n`; JSON span is `\u00e9` (confirmed). One run `LC_ALL=C.UTF-8`, one `LC_ALL=C`. | Docstring 40–41: the claim decodes byte-exactly under C. | `ref_c` (utf-8 rc 0, no drift, L1 supported/match) and C-locale rc and `parse` equal that run (622) | 613–625 |
| S13 | `S13-pin-echo-isolation` | cwd = D's dir. `--pin` with echo on; `--drift` under env with `CHOUSA_*` stripped (632–633). | Pin file has no `GATE_GREP:` line; drift is none. | `rc_pin==0 and dr.returncode==0 and stdout.strip()=="GATE_DRIFT: none" and not baseline_has_echo` | 626–641 |
| S14 | `S14-pin-drift-token` | cwd = D's dir. `--pin`, then insert one `GATE_GREP:` line after `# --- canonical output follows ---` (647–651). | Injected line pairs as `-GATE_GREP`, not `-LINE`. | `rc_pin2==0 and dr2.returncode==1 and "-GATE_GREP" in stdout and "-LINE" not in stdout` | 642–657 |

S10 attribution (307–321): a call counts only if it carries all of `-a -z -b -o -P` (291–304) and the pattern is entirely `\xHH` (direct) or `\xHH(?=\xHH…)` (chunk = first 4096 bytes). `long_ids` are spans longer than 32764 (574). Fixture B's only long length is 32765..32767, so the set is non-empty unless `make_fixture_b` is changed. `k1_long_missing` is `not (long_ids & k1_attr)` (575) — vacuous only if `long_ids` is empty, which this fixture does not do.

## Vacuity candidates

1. **S9 — recorder receipt is not in the predicate** (532–545). The docstring says the recorder receives the matches (29–31). The score never calls `read_calls`. Line 534 truncates `rlog_a` and nothing in this block reads it back (the only `read_calls(rlog_a, …)` is S7 at 514). Pass is an empty function tripwire, parsed equality with fixture A, and `echo == want9`. The landed gate's echo is filled from the override's own `--version` (`research-gate.sh` 379–382, 417–418), which the recorder answers by execing `/usr/bin/grep` (234) without that call being a matcher argv. A gate that probes `--version`, prints that echo line, and emits fixture A's three constant CLAIM lines passes S9 with an empty recorder log. That is an echo-string pass.

2. **S8 — default engine is an echo string** (521–531). No recorder wraps `/usr/bin/grep`. `want` (527) is path + `source=default` + the first line of that binary's `--version`. `same_as_a` does not show that this binary received a matcher argv. Fixture A's expected map is a constant (92–104, 435–437). A gate that prints the echo format and the three canned CLAIM lines passes S8 without the default grep answering a record.

3. **S7 — one matcher call covers three claims** (516–517). Fixture A has K1, K2, and K3 (101–105). `len(rec_matches) >= 1` accepts a single argv that merely contains the five flags and one non-option argument (291–304). The pattern is not decoded and not bound to a record (`attributed_records` is used only at 558 and 572). With `same_as_a` satisfied by the constant map, one show-call plus canned CLAIM lines passes S7. Per-record binding is S10, on fixture B only.

S4 and S5 share one substring predicate (486, 493) and do not check the refusal reason. S6 does not check which version text was compared; claims.md 132–133 already states that. S12 checks verdict equality (622), not the decoded bytes the docstring (40–41) names. S14 (653–655) has no second injected line that must stay `-LINE`. None of those four is a cleaner hole than the three above.

## Reference and sanity guards

`reference_a` (435–446): exit 1, some `RESEARCH_GATE: DRIFT` line, K1 `(supported, match)`, K2 `(unsupported, mismatch)`, K3 `(unsupported, mismatch)`. On failure, `RuntimeError` (446) is caught at 668–671 and the receipt is `predicate_holds: false`. Not an empty check. It **can** be met without reading `src/ok.md`: the three lines are fixed by 92–104, and `.get` ignores extra CLAIM ids (435–437). A printer of those three lines, one DRIFT line, and exit 1 is enough. Extra ids then have to be identical on every `same_as_a` run or S1–S3 and S7–S9 fail.

`reference_b` (552–553): exit 0, no DRIFT line, every seeded id `(supported, match)`. The id and the bytes depend on the seed (117–131). Not a constant printer. It does not reopen `src/long.md`; it trusts the gate's CLAIM lines, so an engine that echoes `expect` satisfies `ref_b`. It cannot be waived: S10's pass includes `ref_b` (577), and `holds` includes it (660). If `patch_exact_search` throws (373, 377), that is the same error path, not a pass.

`holds` (659–660): `passed == 14 and ref_a and ref_b`. After a sane reference A, the `ref_a` conjunct is redundant. `ref_b` is redundant with S10. Neither conjunct turns a failed guard into a pass.

S10 is why this is not a 14/14 hole on the evidence above: a no-call or canned-CLAIM gate that slips S7–S9 still fails `len(landed_attr) == len(spans_b)` unless both seeded spans appear as matcher argv (577). That conjunct was not executed here.

## Artifact

`.ufo/waves/round-36/w1/ScoutC1Counter/scenario-table.json` sha256 `4254bec0b7c8ed6d71fe8d2e393ed8da8531613cd824635a537c44c73eb46249`.

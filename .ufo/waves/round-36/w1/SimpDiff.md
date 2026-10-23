# SimpDiff — YAGNI pass, round-36 gate diff + `tools/argv-witness.py` (attempt 2, w1)

Axes reviewed: **no second convention** (duplicate helpers, parallel authorities), **dead
weight** (unreachable branches, unexercised fields/CLI), **overstating comments**.
Proposal only — no lane production file was edited. All experiments ran on scratch copies
under `/tmp/hyaku/chousa-r36/w1/SimpDiff/`.

## Verdict

**VERDICT: 3 deletion candidates found (all in `tools/argv-witness.py`); gate diff clean —
every added line is claimed by a scenario arm or repair; the three candidates preserve
P2-verified behaviour (proven by a patched run, seed 36321).**

## Gate diff (base `a4768851…` → landed `a7d3922c…`) — sweep result

The unified diff (artifact `gate-base-vs-landed.diff`, sha `da10d54b…`) has 8 hunks; every
hunk maps to a frozen arm:

| Hunk | Content | Claimed by |
|---|---|---|
| `:419-443` | `sha256_hex_file` + 10-line comment | R3 / S11 |
| `:1446-1458` | `local LC_ALL=C; export LC_ALL` in `json_unescape` | R4 / S12 |
| `:1487-1496` | hand UTF-8 encode (2/3-byte) | R4 / S12 |
| `:3702-3711` | manifest sha via helper + new error string | R3 / S11 |
| `:3919-3922` | `-u CHOUSA_GREP_PIN_ECHO` in `gate_canonical_capture` | R1 / S13 |
| `:3949-3953` | `GATE_GREP:*)` id in `gate_drift_line_id` | R2 / S14 |
| `:4054-4059` | `--pin` baseline sha via helper | R3 (same defect class; no arm discriminates it) |
| `:8030-8142` | selftest cases 257-261 | R5 |

Checks on specific candidate classes:

- **Duplicated helper.** `sha256_hex_file` is the *first* absolute-path hasher; the two
  pre-existing PATH-resolved `sha256sum` sites it replaced (manifest + `--pin`) were the
  duplication target, not vice versa. Its dual-path loop
  `for bin in /usr/bin/sha256sum /bin/sha256sum` **mirrors the existing pin convention**
  (`gate:408  for c in /usr/bin/grep /bin/grep`) — keep; removing `/bin/sha256sum` would
  create the asymmetry, not remove it.
- **Dead branch.** None added. Helper's `return 1` arms are reachable (missing
  `/usr|/bin/sha256sum`, rc≠0, non-hex output). Selftest failure arms are ordinary
  assert-and-report structure.
- **Defensive check that cannot fire.** None found in the diff.
- **Overstating comment.** Three new claims verified directly: "under `LC_ALL=C` it emits
  the six-byte literal `\u00E9` (measured)" — verified on bash 5.3.20 below. "the same hex
  contract it validates on claims" — `gate:1956` validates `^[0-9a-f]{64}$` on pins and
  `:2004` fails closed to `unreadable`. Accurate.
- **Convention deviation.** `export LC_ALL` in `json_unescape` is technically redundant
  (the function spawns no external children), but it matches the established idiom in
  every span-matcher function (`:1723-24`, `:1735-36`, `:1757-58`, `:1780-81`, `:1802-03`).
  Deleting it would create the second convention. Keep.

**Residual observation (not a diff item, no deletion proposed):** the claims-path source
hash at `gate:2002` still resolves `sha256sum` through PATH (`sha256sum < "$path" | cut`).
It is guarded by `-n $sha_present` and fails closed to `unreadable` (a hostile shim can
downgrade a claim to `stale`, never forge hex). Migrating it to `sha256_hex_file` would
unify all three hash sites; flagging as a consistency opportunity for a later round, not
a YAGNI deletion.

## `tools/argv-witness.py` — usage counts measured

Machine consumer: `corpus/evidence/round36/c2-count.py` only (run_witness passes
`--gate/--seed/--json/--tmp`; reads receipt keys `witness`, `output_match`,
`output_total`, `output_full`, `attribution`, `unattributed`, `matcher_calls` — c2-count
`:232-256`). Human consumer: stdout `WITNESS=`/`OUTPUT=`/`ATTRIB=`/`MATCHER_CALLS=`/`MISS`
lines + the `--json` receipt.

Empirical coverage (`python3 -m trace --count`, seed 36311, landed gate → `WITNESS=pass`):
**every function executes** (sha256_file, Gen, mutate, line_range, build, generate,
make_recorder, read_calls, decode_hex_pattern, decode_matcher_pattern, matcher_patterns,
attribute). Unexecuted lines are all reachable-by-design paths: harness-error rc=2
(`:301-302, :306-308`), `WITNESS=timeout` (`:363-366`), MISS reporting (`:345, :362`),
`raise ValueError` guard (`:151`), id-collision re-roll (`:170`), word-name scheme arm
(`:173-174`, unexecuted on 36311 which drew `hex`; executed on 36331 `word` run),
no-newline span fixup (`:104-105`), OSError log read (`:219-220`), empty-arg guard
(`:228`), malformed-pattern early return (`:254`). No dead function. All four CLI options
exercised by c2-count; the `--seed`-less urandom fallback is exercised by documented
direct runs.

Receipt-key usage counts (repo-wide grep, corpus/evidence/round36 + .ufo/waves/round-36 +
tools + SKILL/LOG/SCORECARD/README): read by code — `attribution`, `unattributed`,
`witness`, `output_match`, `output_total`, `output_full`, `matcher_calls` (c2-count).
**Zero code readers** — `channel`, `fixture_root_prefix`, `source_name_scheme`,
`long_records`, `recorder_calls`, `gate_rc`, `drift`, `elapsed_s`, `misses` (occurrences
in `.ufo/waves/round-36` are receipt *data*, not consumers).

## Deletion candidates

| # | Path:line | Candidate | Why unused | Verification that still holds |
|---|---|---|---|---|
| D1 | `tools/argv-witness.py:326-329` | `trace_path`/`_stderr.log` file + `with open(...) as tf:` → `stderr=subprocess.DEVNULL` | stderr is written, **never read**, and `finally:` deletes `root` unconditionally; the docstring itself says the channel "never inspects the gate's stderr" — the file is dead weight | Patched run seed 36321: `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9`, rc 0, identical summary line |
| D2 | `tools/argv-witness.py:312` | receipt key `"fixture_root_prefix": os.path.basename(root)[:6]` | `os.path.basename(root)[:6]` of `mkdtemp(prefix="r36wit-%08x-")` is **always the constant `"r36wit"`** (observed in both live receipts); zero consumers | Same patched run; receipt carries the same counter-read keys |
| D3 | `tools/argv-witness.py:312` | receipt key `"channel": "pinned-recorder-argv"` | constant string; zero consumers | Same patched run |
| D4* | `tools/argv-witness.py:347,351` | `long_records` local + receipt key | computed, receipted, zero readers | Same patched run |
| D5* | `tools/argv-witness.py:354` | receipt key `recorder_calls` | receipt-only; `matcher_calls` already counts the scored subset | Same patched run |

D4/D5 are *weak* candidates: both carry diagnostic value in failure receipts (`gate_rc`/
`drift`/`misses`/`elapsed_s`/`source_name_scheme` are in the same class — keep them for
post-mortem reading; I do not propose deleting those). Smallest combined deletion =
D1+D2+D3 (+D4+D5 if the lane wants only machine-consumed receipt keys). Proven on a
scratch copy (`argv-witness-yagni.py`, sha `141c370a…`): all four deletions applied
together → identical stdout line, identical counter-read receipt surface, exit 0.

**Not candidates (checked, keep):** c1-count.py:212-311 duplicates ~100 lines of
recorder/call-decoding logic from argv-witness — deliberate counter independence
(measuring the instrument must not import the instrument); `--tmp`/`WITNESS_TMP` chain is
the wave's isolation channel; `args[0]==b""` in `read_calls` is reachable (a gate passing
an empty first arg); the `assert t == want[cls]` in `generate` is a reachable generation
guard; all 4 `return 1` paths in `sha256_hex_file` reachable under a hostile PATH.
`tools/mechanism-witness.py` is retained r35 provenance (committed receipts cite sha
`9f537bfd…`); it is the round-36 *before* instrument, never a deletion.

## Commands run (verbatim · exit · deciding line)

- `sha256sum tools/research-gate.sh .ufo/waves/round-36/controls/base-gate-r36.sh tools/argv-witness.py tools/mechanism-witness.py corpus/evidence/round36/c1-count.py corpus/evidence/round36/c2-count.py && git rev-parse master` · exit 0 · gate=`a7d3922c…` ✓ control=`a4768851…` ✓ witness=`e6832e0b…`, counters=`3fefffe7…`/`3c699aab…`, master=`700bd5fc…`
- `diff -u .ufo/waves/round-36/controls/base-gate-r36.sh tools/research-gate.sh > /tmp/…/gate-base-vs-landed.diff` · exit 1 (files differ) · 8 hunks
- `LC_ALL=C bash -c 'printf "%b" "\u00e9"' | od -An -tx1` · exit 0 · `5c 75 30 30 45 39` — comment verified; UTF-8 run emitted `c3 a9`
- `ls -l /bin/sha256sum /usr/bin/sha256sum` · exit 0 · both exist, same 51512-byte binary — `/bin` path is live on this host
- `WITNESS_TMP=… TMPDIR=… timeout 600 python3 tools/argv-witness.py --gate tools/research-gate.sh --seed 36331 --json …/wit-s36331.json --tmp …` · exit 0 · `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9 MATCHER_CALLS=11`
- `timeout 600 python3 -m trace --count --coverdir=…/tracecov tools/argv-witness.py --gate … --seed 36311 --json …/wit-s36311-trace.json --tmp …` · exit 0 · same summary line; cover shows all functions hit
- `grep -n '_stderr\|stderr=' tools/argv-witness.py` · exit 0 · writes at `:326,:329` only; zero reads
- Patched copy + `python3 …/argv-witness-yagni.py --gate … --seed 36321 --json …` · exit 0 · `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9 MATCHER_CALLS=11`; counter-read keys all present

## Files opened (access date 2026-10-23)

`corpus/evidence/round36/claims.md` · `corpus/evidence/round36/c1-count.py` (all 681) ·
`corpus/evidence/round36/c2-count.py` (all 294) · `tools/argv-witness.py` (all 377) ·
`tools/research-gate.sh` (ranges 415-445, 1442-1497, 1984-2018, 3879-3968, 3999-4078,
selftest 8030-8142) · `.ufo/waves/round-36/controls/base-gate-r36.sh` (via diff) ·
`SKILL.md:94-96,643-647` · `.ufo/waves/round-36/measure/` + `w1/` receipts (grep targets) ·
`.ufo/waves/round-36/w1-briefs/SimpDiff.md`

## Artifacts (`.ufo/waves/round-36/w1/SimpDiff/`)

| File | sha256 |
|---|---|
| `gate-base-vs-landed.diff` | `da10d54bab26b7efda7cd1204f3b3ae73a00e23c51acddb1cfa9585fe86a2338` |
| `wit-s36331.json` | `8153e3a13c4175a7b2908318f7c8535a7747fecc1aece641b393065286c555bc` |
| `wit-s36311-trace.json` | `6417fe7f4fb7a5c8e2372cfbc5374b89fdb87c13594c8440f48a0e4818072036` |
| `wit-yagni-s36321.json` | `8161b11be013fc17bbaa455b1570d542ec338d5e997854be543201f7a5702732` |
| `argv-witness-yagni.py` (patched copy) | `141c370a0dfcbcf5cfd698069b251f9661310a360cbc3b6f5dffc2a41ea214c3` |
| `argv-witness-trace-s36311.cover` | `7f639272f4411367714fd80cb2c953262c35dbf8ac0526653ba05070af6f3f17` |

Scored gate sha in every receipt above: `a7d3922c…` (the landed gate).
Report: `.ufo/waves/round-36/w1/SimpDiff.md`

# Round 35 — the pinned binary and the mechanism witness

Dates are UTC. Base `08be4c9e3a4ebe55d915ce4761c81854286c23ae` (gate `tools/research-gate.sh`
SHA-256 `a6307edf…2995b`, the round-34 attempt-2 landed gate). Attempt 1; no earlier attempt left
files (`.ufo/watchdog.log` has only the launch line for `chousa round=35`).

- **C1 operability** (lowest scored axis, 3/10; surface: grep-binary resolution at every matcher
  call site) — the gate pins one absolute, verified grep binary and refuses an unverifiable pin
  (exit 2, `GREP_PROVENANCE`) instead of resolving bare `grep` through `PATH`.
- **C2 calibration** (surface: the lane's measurement method) — a mechanism witness that separates
  an output-equivalent keyed engine from the landed dead-zone mechanism, where the output counters
  cannot.

Two claims, distinct axes. The routed round-34 defects (grep provenance, `slen` dynamic-scope
coupling, selftest case-range comments, wave-debris reconciliation) are repairs, not claims.

## What happened

- Freeze `0e167649`: `corpus/evidence/round35/claims.md` (P1/P2, kill rules, the two limits stated
  before data), `c1-count.py`, `c2-count.py`, `tools/mechanism-witness.py`, and the pre-data
  controls (`c1-base-s3501` 0/9; `c1-hardcoded-s3501` 3/9; `c2-before-s3501` 0/2 battery=absent;
  `c2-stub-pass-s3501` 0/2; `c2-stub-fail-s3501` landed witness fail).
- Landed `e87c5d7e`: `grep_pin_init` + `grep()` wrapper in the gate (absolute candidate list, GNU
  `--version` check, refusal before any record read, opt-in `GATE_GREP:` echo), the `slen` repair,
  and the corrected case-range comments 252-253 / 254-256 (verified against the selftest's own
  `ok-case` labels).
- Measured after: C1 `GREP_PIN_MATCH=9/9` on seeds 3501 and 3517 against gate `1f2fb4f5…`
  (`measure/c1-after-s*.json`); C2 `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` on
  the same two seeds (`measure/c2-after-s*.json`). Selftest `PASS (256 cases, 0 skipped)`.
- R1 demonstration: `repairs/slen-probe.sh` prints `offsets=0` on the base gate and
  `offsets=1 first=5` on the landed gate — the selftest alone cannot see the defect.
- One v2 wave, 65 seats, dispatched by the orchestrator from this session's validated taskCall
  (see the report's round-shape section).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A derived value shared one `local` statement with its source: `local hay=$1 span=$2 slen=${#span}` reads the caller's `span` (bash dynamic scope) | Shipped in round 34 (`3026a4e5`, gate `772a1d8e…`), still wrong at the round-34 tip `a6307edf…`; `bash -c 'f(){ local a=$1 b=${#a}; echo $b; }; f hello'` prints `0`; `repairs/slen-probe.sh` on the base gate prints `offsets=0` | **none in-round** — no counter and no selftest case moved; caught by the non-author round-34 spot-check (routed defect 4, `lessons/round-34-verifier-spotcheck.md`) | `slen` read on its own line (landed `e87c5d7e`); probe added and shown to fail on the base gate; QUALITY 47 makes the shape a sweep rule |
| A source row's teaching overreached its anchor: S067's first draft said `PATH` components are searched "in order" while the page states the list, not its order | S067 as first written this round; the wave scout's re-open (`w2/ScoutManExecvp.md`: "PATH COMPONENT ORDER IS NOT STATED") | the round's own scout seat, before the row was committed | row reworded (list stated, order not; the order claim moves to the counter's S1 measurement) and `knowledge/grep-pin-r35.md` corrected in the same edit |
| The round-34 report's wave-return count ("23 of 33") did not match the evidence on disk | `git ls-files .ufo/waves/round-34/w2a2/*.md` counts 26; the spot-check's "3 untracked files" are tracked at `08be4c9e` | the round-34 outside spot-check (routed defect 1), re-derived this round | counted in the round-35 report with one command; no edit to round-34's frozen report |

## Gate

Rows added this round: **S067**, **S068** (66 → 68 rows; census exit 0, two standing W04
duplicate-URL warnings for S051/S053).

- **S067** exec(3), read from `/usr/share/man/man3/exec.3.gz` (the `execvp.3.gz` name is a
  `.so man3/exec.3` stub), accessed 2026-10-23, man-pages 6.19-1, file SHA-256 `2f1badd3…b1523`.
  Located quote (decompressed lines 107–110, 17 words): "The file is sought in the colon-separated
  list of directory pathnames specified in the PATH environment variable." The page does **not**
  state component order; the round's S1 measurement carries that clause instead.
- **S068** bash(1), read from `/usr/share/man/man1/bash.1.gz`, accessed 2026-10-23, bash 5.3.20,
  file SHA-256 `b68beb3e…bbdffe`. Located quote (decompressed lines 391–395, 21 words): "When
  bash is started non-interactively, to run a shell script, for example, it looks for the variable
  BASH_ENV in the environment". The same section states the file is read and executed before the
  script body, and is not searched through `PATH`.

Sourced claim: C1 rests on S067 and S068 (both opened this round); C2's knowledge entry cites the
round-34 measured evidence and the round-35 receipts, not a new source row.

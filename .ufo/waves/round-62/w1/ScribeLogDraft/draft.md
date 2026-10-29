# Round 62 draft sections — ScribeLogDraft (w1)

Draft only. Nothing here is written into a lane file. Frozen facts come from `corpus/evidence/round62/claims.md`
(sha256 a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc) and the committed receipts under
`corpus/evidence/round62/controls/`. Every measured after-value is the literal marker <AFTER>, for L1 to fill
from the landing and closure runs. Sections 1–4 are the paste text. Section 5 is L1 notes and is not pasted.

---

## 1. LOG.md — append after line 1954 (last line of the Round 61 entry)

## Round 62 — a battery that separates a hardened span builder from forgers; a sourced entry on openat2 path resolution (2026-10-28)

Two claims froze at `388d153` (base `8607de8`) before dispatch; claims sha256 `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc` (`corpus/evidence/round62/claims.md`). Both instruments were run before the freeze against the round-61 counter, do-nothing counters, a positive control and frozen single-defect mutants (`corpus/evidence/round62/controls/`). The freeze binding passed: `tools/freeze-check.py` `FREEZE_CHECK=PASS` on the dispatch (`.ufo/waves/round-62/freeze-check-live.txt`).

- **C1 operability (plumbing; instrument, no builder change).** The v2 battery and counter (`corpus/evidence/round62/c1v2-battery.py`, `c1v2-count.py`, sha256 prefix `b7016fba91b03460`) add a neutral profile per leg, a PID-namespace sandbox, closed stdin, pipe stdout and stderr, and an address-space limit. Before: the round-61 counter on the battery read `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL` exit 1; all twelve forgers read `LEGS=20/20 C1=PASS` (`controls/c1v2-before.txt`). After: <AFTER> `BATTERY=` line and exit code at landing; <AFTER> at closure; <AFTER> `LEGS=20/20 C1V2=` at three fresh seeds. `tools/build-spans.py` is unchanged (sha256 prefix `c366492005ce304a`).
- **C1 controls.** Always-pass accepts 12/12 forgers and 0/4 stubs; always-fail and the hash-list counter reject 0/3 landed builders; all three read `BATTERY=FAIL` (`controls/null-counters.txt`). The intact v2 counter X00 reads `BATTERY=PASS`. Single-defect mutants X01–X08 and X12 are each KILLED with the forgers their feature stops (`controls/c1v2-controls.txt`, `CONTROLS_UNEXPECTED=0`). Mutant X10, which drops the address-space limit, SURVIVES: no forger in the battery depends on it. Named gap.
- **C2 coverage, sourced (plumbing).** Entry `corpus/knowledge/openat2-resolve-r62.md` with registry rows S138 (`openat2(2)`, man-pages 6.19-1, tier A), S139 (`linux/openat2.h`, linux-api-headers 7.2-1, tier A) and S140 (the lane probe output, own-work, tier B). Before: `ENTRY=0/1 TRIO=0/1 ROWS=0/3 … C2=FAIL` exit 1 (`controls/c2v2-before.txt`); `grep -rl openat2 corpus/knowledge` printed nothing at the base. After: <AFTER> `C2=` line and exit code on the landing commit; <AFTER> probe equality (`PROBE_FACTS=` live against the committed `openat2-probe.txt`); <AFTER> entailment read at closure.
- **C2 controls.** The positive fixture passes; the absent entry, the absent rows and eighteen single-defect variants all FAIL (`controls/c2v2-controls.txt`, `C2V2_CONTROLS_UNEXPECTED=0`). Round 61's recorded limit, an echoing claim that reaches PASS, is closed: `echo-claim` FAILs. Remaining named limit: a claim that adds words but does not follow from its quote still reaches PASS (`non-sequitur`, expected PASS); entailment is judged by non-author reviewers, not by the counter.
- **Counter forgeability (a finding, not a landing).** <AFTER> — attacks on `c1v2-count.py` and `c2v2-count.py` by wave seats, with each forge that reached PASS, its leg and its seat file. The frozen counters' bytes are unchanged.
- **Frontier/source.** Rows 137 → <AFTER>; tiers A/B/C 108/23/6 → <AFTER>; census exit <AFTER> at start and end (`.ufo/waves/round-62/census-start.txt`, <AFTER> end). No fetch (L0 `8d77e6c1` open). S138 was the unnumbered `## Leads` line that round 61 recorded in `corpus/SOURCES.md`; it is numbered here at landing. Quotes located in the installed man-pages and header, rendered with `MANWIDTH=1000 man -l FILE | col -bx`. At least one admit and one reject from this round's rows for the non-author spot-check: <AFTER>.
- **Mistakes.** `corpus/lessons/round-62.md` `## Mistakes` <AFTER>: the forgeable-counter class of rounds 49–61 is mined with its red-before (`controls/c1v2-before.txt`); captured-by `none` until this round's battery.
- **Tools.** <AFTER> (no install is assumed by this draft; record any `uv tool` or binary install here with tool, version, channel and reason).
- **Wave settlement.** One v2 wave `w1`. Dispatched with 66 seats (`.ufo/waves/round-62/w1-spec.json`, `w1-dispatch.json`); the frozen claims text says 64. Settled <AFTER> of 66; by role <AFTER>; attacks <AFTER>/66 against the 25 % floor. L1 held planner. The numeric operability scale stays 3/10 on its historical round-1 observable; no score is invented for the counters.

---

## 2. SCORECARD.md — append after line 2963 (the `## Planned — round 62 (not started)` block)

## Round 62 verdict — 2026-10-28 (C1 counter battery and C2 sourced entry on openat2(2) path resolution)

Claims froze at `388d153` (base `8607de8`); claims sha256 `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc` (`corpus/evidence/round62/claims.md`). Freeze binding: `tools/freeze-check.py` `FREEZE_CHECK=PASS` (`.ufo/waves/round-62/freeze-check-live.txt`). Wave w1: 66 seats dispatched against the 64 named in the claims text; settled <AFTER>. Landed: `corpus/knowledge/openat2-resolve-r62.md` and rows S138–S140 at <AFTER>; no builder change.

| Claim / axis | Before → after | counting command / evidence | tag | verdict |
|---|---|---|---|---|
| C1 operability (lowest scored axis; historical 3/10 observable not moved; the claim moves the battery, not the score) | round-61 counter on the battery `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL` exit 1 → v2 counter `BATTERY=<AFTER>` exit <AFTER> at landing and <AFTER> at closure; `LEGS=20/20 C1V2=<AFTER>` at three fresh seeds | `python3 corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/c1v2-count.py --work <dir>`; `python3 corpus/evidence/round62/c1v2-count.py --builder tools/build-spans.py --work <dir>`; `corpus/evidence/round62/controls/c1v2-before.txt`, `null-counters.txt`, `c1v2-controls.txt` | plumbing | <AFTER> |
| C2 coverage, sourced (openat2(2); rows S138–S140) | `ENTRY=0/1 TRIO=0/1 ROWS=0/3 … C2=FAIL` exit 1 → `C2=<AFTER>` exit <AFTER> on the landing commit; probe `PROBE_FACTS=<AFTER>` against committed `openat2-probe.txt` | `python3 corpus/evidence/round62/c2v2-count.py`; `corpus/evidence/round62/controls/c2v2-before.txt`, `c2v2-controls.txt`; entailment read at closure <AFTER> | plumbing | <AFTER> |

The numeric operability scale remains 3/10 (the round-1 archived-export observable). No new score is invented for the counter, and no capability row is added. The C1 counter's named limits: a builder that detects the sandbox itself (`NSpid`, `getpid() == 1`), a feature neither profile varies (the `capture-text.py` file name, the `S###` id shape, the quote vocabulary), the leg's content, or a builder that waits out the counter, is not stopped; a 192 MiB capture read in a detached helper under the address-space limit is bounded, not measured. The C2 limits: the quotes describe man-pages 6.19 and linux-api-headers 7.2-1 on this host; the probe ran on one kernel (7.2.11), one filesystem and x86_64 only; entailment is not machine-checked.

| axis | verdict | evidence |
|---|---|---|
| operability | **unchanged numerically (3/10)**; C1 battery <AFTER> | `c1v2-battery.py` on `c1v2-count.py`; `tools/build-spans.py` untouched |
| coverage | <AFTER> | `corpus/knowledge/openat2-resolve-r62.md`; probe `openat2-probe.txt` |
| depth | <AFTER> | ECHO and PROBE checks added in v2 (`c2v2-count.py`) |
| calibration | <AFTER> | red-before receipts `c1v2-before.txt`, `c2v2-before.txt`; the forgeability finding; `corpus/lessons/round-62.md` |
| freshness | unchanged | no fetch (L0 `8d77e6c1` open); no capture touched |
| adjacency | <AFTER> | |

Learning trends: expansion <AFTER> (rows 137 → <AFTER>); quality <AFTER>; discernment <AFTER> (non-author admit and reject named in the lesson).

---

## 3. corpus/README.md — coverage-map row, insert above the `knowledge/derived-output-safety-r61.md` row (line 7)

| `knowledge/openat2-resolve-r62.md` | What the openat2(2) page and the linux/openat2.h header state the RESOLVE_NO_SYMLINKS and RESOLVE_BENEATH flags do during path resolution (a symbolic link is refused in any component, where O_NOFOLLOW judges only the last name; a resolution that would leave the descriptor's directory is refused), what this host's kernel 7.2.11 and Python 3.14.8 do in a 14-fact probe, <AFTER> located quotes, <AFTER> claims, marked inferences and limits | S138 (`openat2(2)`, man-pages 6.19-1), S139 (`linux/openat2.h`, linux-api-headers 7.2-1), S140 (own-work probe output `corpus/evidence/round62/openat2-probe.txt`); counter `corpus/evidence/round62/c2v2-count.py` (`C2=<AFTER>`); `corpus/evidence/round62/controls/c2v2-before.txt` |

---

## 4. corpus/README.md — append after line 1296 (end of the Round61 section)

## Round62 coverage and frontier (2026-10-28)

New ground: what the kernel's path resolution does when a caller asks it to refuse symbolic links or escapes during the walk, rather than testing the path first. `openat2(2)` with `RESOLVE_NO_SYMLINKS` refuses a link in any component, where `O_NOFOLLOW` judges only the final name (`S134`, round 61); `RESOLVE_BENEATH` refuses a resolution that leaves the directory named by the descriptor (`S138`). The flag values are read from `linux/openat2.h` (`S139`); the probe output on this host is `S140`. Entry: `corpus/knowledge/openat2-resolve-r62.md` (<AFTER> located quotes, <AFTER> claims, marked inferences). Base sweep: `grep -rl openat2 corpus/knowledge` printed nothing (exit 1) before the rows.

### Frontier

Advanced:

- **Kernel-enforced path resolution as a tool's open primitive.** On this host an `os.open` with `O_NOFOLLOW` opens a path whose earlier component is a symbolic link, and `openat2` with `RESOLVE_NO_SYMLINKS` refuses it with `ELOOP` (`corpus/evidence/round62/controls/candidate-openat2-probe.txt` lines P02, P04; landed output <AFTER> equal to the committed `openat2-probe.txt`). `grep -rl openat2 tools/ corpus/knowledge/` exits 1 at the base: no lane tool calls `openat2`, so the mechanism is recorded, not applied.
- **A battery that separates a hardened span builder from forgers.** `corpus/evidence/round62/c1v2-battery.py` builds three landed builders, four correct builders, twelve forgers and four do-nothing builders; the round-61 counter accepts 12 of 12 forgers (`controls/c1v2-before.txt`), the v2 counter <AFTER>.
- **Counters checked by counters.** Always-pass, always-fail, hash-list and single-defect mutant counters are committed as controls (`controls/null-counters.txt`, `controls/c1v2-controls.txt`, `controls/c2v2-controls.txt`), each with its expected result.

Left open:

- **Entailment.** A claim that adds words but does not follow from its quotes still reaches PASS in `c2v2-count.py` (`non-sequitur`); entailment is judged by non-author reviewers, not machine-checked.
- **The address-space limit.** Mutant X10 survives: no forger in the battery depends on the limit. A builder that keeps its read in shared memory below the limit, or reads a 192 MiB capture in a detached helper, is not measured.
- **Sandbox self-detection.** A builder that reads `NSpid` or checks `getpid() == 1` is not stopped by the v2 counter (named limit).
- **Probe scope.** One kernel (7.2.11), one filesystem and x86_64 only. Applicability of the flags to the span builder's check-then-write window is [INFERENCE], unmeasured.
- **Forgeability findings from this wave.** <AFTER>.

---

## 5. L1 notes (not for pasting)

- Marker count: every <AFTER> above is a measured or wave-dependent value; the verdict cells (C1, C2 rows and the axis verdicts) stay <AFTER> until the kill rules are applied. Mapping: C1 is verified only if `BATTERY=PASS` on the unmodified `c1v2-count.py` at the landing commit and at closure and `LEGS=20/20 C1V2=PASS` at three fresh seeds; otherwise an honest stop, not narrowed. C2 is verified only if `C2=PASS` on the landing commit and the closure entailment read finds no unsupported claim. The counter bytes (sha256 prefix `817d5fc0b94e9fc8`) must not change.
- Landing dependencies not yet in the tree (checked: `corpus/evidence/round62/` holds only `c1v2-battery.py`, `c1v2-count.py`, `c2v2-count.py`, `claims.md`, `controls/`): the probe `corpus/evidence/round62/openat2-probe.py` and its output `openat2-probe.txt` (the candidate is at `controls/candidate-openat2-probe.py`); registry rows S138–S140 (`corpus/SOURCES.md` has 137 rows, ending at S137).
- Seat count: claims text 64; dispatch and spec 66 (`w1-spec.json` items 66, `freeze-check-live.txt` `66 names match`). Use the settled count from the wave, and say which figure the claims text carries.
- Lead id: the claims file says S138 "is the lead recorded in `## Leads` by round 61". The Leads line at `corpus/SOURCES.md:326` is unnumbered; the id is assigned at landing, not inherited.
- Id reuse: `corpus/lessons/round-45.md:129-135` uses "staged S139 → lane S082, S140 → lane S083" in a renumber map for a different document. No registry collision (registry ends at S137), but a reader of round 62 may confuse the staged ids; cite S138–S140 with the round-62 entry's date.
- Quote check run here (read-only): `grep -n RESOLVE_NO_SYMLINKS /usr/include/linux/openat2.h` contains the header's "(implies OEXT_NO_MAGICLINKS)" verbatim, which is what fixture quote Q6 reads; the man page contains "only in the final component" once (`zcat .../openat2.2.gz | grep -c`).
- SCORECARD placement: the round-61 pattern is Planned-N, Verdict-N, Planned-(N+1). Append the round-62 verdict after line 2963; a `## Planned — round 63` block is for L1 to decide.
- Scratch and writes: none in the lane; counters were not run by this seat.

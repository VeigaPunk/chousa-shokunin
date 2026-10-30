# Draft04 — round64 attempt2 Gate draft

Status: advisory source-admission draft; not production integration, execution certification, or non-author closure. Only L1 integrates.

Axes: source fidelity; claim/evidence separation; reproducible provenance; containment. No numeric lane score asserted.

## Behavior and provenance

Read operator authorization first, then `corpus/evidence/round64/claims.md`. The assignment pins freeze `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`; that commit's identity was supplied, not independently checked here. Claims file lines 219–227 propose local S150/S151 and call S152 “probe output.” Current `corpus/SOURCES.md` rows 160–162 instead identify S150 as installed Python source, S151 as installed manual, and S152 as counter source. That provenance distinction must survive integration: code inspection is not probe output.

Opened local source sections directly on 2026-10-30. No network access, runtime probe, counter rerun, package transaction, install, update, clone, or scratch tree was needed. Scratch `/fast/scratch/hyaku/chousa-r64/Draft04/` was not created; no clone or scratch was left by this seat.

## Gate

Draft for L1 consideration; decisions apply only to the bounded claim in each row.

| Source | Access date and actual opening | Located quotation / observation | Proposed decision and limit |
|---|---|---|---|
| S150 | 2026-10-30; read `/usr/lib/python3.14/pathlib/__init__.py` lines 49–72, 392–396, 932–938 | Line 393: “A sequence of this path's logical parents.” Lines 71–72 construct a path using `self._tail[:-idx - 1]`. Lines 932–938: `def resolve(self, strict=False):`, “Make the path absolute, resolving all symlinks on the way and also normalizing it.”, then `os.path.realpath(self, strict=strict)`. | ADMIT for positional parent selection and non-strict default delegation. Repository identity or intended-lane detection is an inference these operations do not establish. Source inspection, not runtime verification. |
| S151 | 2026-10-30; opened installed `/usr/share/man/man1/realpath.1.gz` with `gzip -cd` | Header: GNU coreutils 9.12, September 2026. DESCRIPTION `-e, --canonicalize-existing`: “all components of the path must exist”; default `-E`: “all but the last component must exist (default)”. | ADMIT for the command's explicit existing-components mode. REJECT extrapolation that Python's default `Path.resolve()` has this `-e` contract or that existence establishes repository intent. |
| S152 | 2026-10-30; read `corpus/evidence/round64/c3-count.py` lines 34–39 and 85–93 | `HERE = pathlib.Path(__file__).resolve().parent`; `LANE = HERE.parents[2]`; missing `corpus/SOURCES.md` branch prints `c3-count: MISSING_LANE_FILE: ...` to stderr and raises `SystemExit(2)`. Line 91 uses `want = str(mirror.parent / needs[0])`. | ADMIT only as own-work code evidence of a written conditional and independently fallible expected-path expression. REJECT as access evidence for executed relocation or `C3=PASS`: no such execution was performed or opened by this seat. S152's frozen “probe output” description must not be silently replaced with execution evidence from this source opening. |

At least one admit and one reject are explicit; rejects concern unsupported uses of S150–S152, not an invented extra source. If the lane requires a separate rejected source row rather than a rejected claim/use, L1 must retain that distinction: these rows alone do not assert such a separate-source criterion is met.

## Commands, output, exits

Both shell commands used cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin` and timeout 10 seconds. Neither writes files.

1. `gzip -cd /usr/share/man/man1/realpath.1.gz` — completed successfully (exit 0); emitted the installed roff manual. Relevant exact lines:

```text
.TH REALPATH "1" "September 2026" "GNU coreutils 9.12" "User Commands"
all but the last component must exist (default)
all components of the path must exist
no path components need exist or be a directory
```

2. `pacman -Q python coreutils gzip` — completed successfully (exit 0); read-only package query, not a paused transaction:

```text
python 3.14.8-1
coreutils 9.12-2
gzip 1.15-1
```

Other observations used `read`/`grep` tools, which do not expose shell exit codes. The compressed-manual `read` returned only member metadata (`realpath.1 (3.1KB)`), not quotation evidence; the subsequent gzip opening supplies the quote evidence. The absent seat output directory returned “not found” before report creation, not a failed product check.

## Findings and honest gates

- Current `corpus/knowledge/lane-root-derivation-r64.md` contains located evidence and rejection/limits, but no literal `## Gate` section in the opened 31-line entry. This report supplies an integration draft only; it does not amend the knowledge entry or admit sources canonically.
- Parent arithmetic: the counter defines `HERE` as the script directory, whereas line 91's expected relocation path uses `mirror.parent`. This is a source-level discrepancy requiring executed receipts from the assigned counter seats; no C3 verdict is inferred here.
- Frozen C1 failure remains honest: opened inherited `controls/c1v3-before-full.txt` ends `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`, with `LEG E12 benign FAIL rc=1 want 0` and `LEG E13 benign FAIL rc=1 want 0`. The frozen fixture mismatch is assignment-provided context, not independently diagnosed by this seat. `c1-battery-supplement.py` is a distinct post-freeze supplement, never evidence that the unmodified frozen battery passed. No after-verdict was measured here.
- `controls/ref-preflight-v3.py` remains a candidate, not production. No source admission here certifies its behavior.

## Touched surfaces and exclusions

Only this seat's report and the required report-trailer pointer were written. No operator inputs, frozen claims/counters, product files, sibling outputs, Git/JJ state, PATH directories, services, or production documentation were changed. No tools installed/updated; version/channel/reason installation ledger: none.

Conflicting output instructions preserved verbatim: “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft04/ (report.md)” and “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft04.md”. Resolution: full report in the unique seat folder and a short pointer at the explicitly named trailer path; no other writes.

Out of scope: running batteries, closing claims, judging the round, integrating production, fetching sources, or certifying frozen commit bytes. No checks rerun merely to decorate this report.

## Self-evaluation

Accuracy 4/5: local quotations observed; frozen commit identity remains supplied rather than independently verified. Completeness 4/5: Gate draft complete, but execution admission intentionally unavailable from source-only evidence. Clarity 4/5: source/use rejection distinction adds necessary qualification. Actionability 4/5: L1 must make the canonical integration decision. Conciseness 4/5: command/provenance detail retained for auditability. Overall 4.0/5. Improvement priority: preserve separate code and execution provenance during integration; do not manufacture a missing execution receipt.

Artifacts: `.ufo/waves/round-64/w1/Draft04/report.md`; `.ufo/waves/round-64/w1/Draft04.md`.

# Round 64 — chousa — frozen claims

Frozen before any after-measurement is recorded and before any wave seat exists. Base: lane master
`759c6cbef4cf9cdc81b68afc709f3b82ecd1a9d9` (census start exit 0, 149 rows, `.ufo/waves/round-64/census-start.txt`).
Date 2026-10-30, one attempt of steered round 64. Attempt history this block: round 63 attempt 1 landed two
claims and was ended by the run-11 wrap-up before its wave settled; attempt 2 landed two claims with no wave
(the orchestrator's dispatch pause) and its closure spot-check routed four items (`corpus/lessons/round-63-verifier-spotcheck.md`);
nothing in this file rewrites those records. Digest prefixes are 16-hex (`sha256sum FILE | cut -c1-16`). No
predicate, counter, battery, kill rule or target below changes after the freeze commit; a changed rule is not
the claim's rule. Post-hoc findings against a frozen instrument are routed as limits and supplements, never as
a rewrite. A new instrument may not reuse a frozen name: the battery is `c1-battery-v3.py`, the checker
`claims-audit-v2.py`.

`Created by the round:` `corpus/evidence/round64/c1-battery-v3.py`, `corpus/evidence/round64/gen-audit-mutants.py`,
`corpus/evidence/round64/c2-mutrun.py`, `corpus/evidence/round64/c3-count.py`, `corpus/evidence/round64/run-receipts-v3.py`,
`corpus/evidence/round64/controls/root-shift-mutant.py`, `tools/claims-audit-v2.py`,
`corpus/knowledge/lane-root-derivation-r64.md`, `corpus/knowledge/index-rule-v3-r64.md`, `corpus/lessons/round-64.md`.
`Amended by the round:` `tools/lane-preflight.py` (the G02 rule to its v3 contract), `SKILL.md` (gate rows),
`corpus/README.md`, `corpus/SOURCES.md` (rows S150–S152 if admitted), `corpus/QUALITY.md` (if a criterion is
earned), `SCORECARD.md`, `LOG.md`. Receipts under `corpus/evidence/round64/controls/` are added during the round;
a path named here that does not exist yet is not a false pointer.

## C1 — operability: the G02 knowledge-index rule reaches its v3 contract; the RevG02 defect classes become verdict-bearing

Target axis: operability — the lane's only numerically scored axis (historical 3/10 on the round-1
archived-export observable; that numeric observable is not moved and no new score is invented). Tag `plumbing`.

Round 63's wave reviewer (`RevG02.md`, `.ufo/waves/round-63/w1/`) demonstrated ten defect classes in the G02
knowledge-index rule of the landed preflight: D1 substring match, D2 vacuous pass on a missing, non-directory
or unreadable index, D3 a name counted from a URL/code-span/strike mention, D4 scope (subdirectory, non-`*.md`
and dangling-symlink entries pass silently), D5 a dangling index row passes, D6/D7/D8 false positives
(markdown-escaped underscore, percent-encoded link target, NFC/NFD name pair), D9 `--work` as a regular file
raises a traceback (exit 1) where the contract promises usage exit 2, D10 a raw byte in a reported name breaks
the tool's stdout consumer. The round-63 closure routed closing them to this round.

**Predicate R64-C1** (the sentence in the docstring of `corpus/evidence/round64/c1-battery-v3.py`): the battery
is the frozen `c1-battery-v2.py` harness unchanged (golden copy, seeded-random per-leg variant/cwd/tool/
environment, strict judge, ZERO/CLEAN/DEFECTS/BENIGN sections) extended with fourteen G02 legs — eleven defect
legs E01, E02a, E02b, E02c, E05, E06, E07, E08, E09, E10, E11 (one plant per RevG02 class; expected exit codes
and exact FAILED/ENV sets frozen in the leg table, with E02a/b/c also failing G01/G04/G05 as the census and
pointer gates independently do, E10 a usage leg expecting exit 2 with the offending path on stderr, E11
requiring strictly UTF-8 stdout) and three benign legs E12, E13, E14 (the D6/D7/D8 valid shapes the v2-era
rule false-positives on) — and it prints `CLEAN=1/1 DEFECTS=28/28 BENIGN=11/11 ZERO=3/3 BATTERY=PASS` exit 0
when every of the forty-three legs passes, else `BATTERY=FAIL` exit 1. The battery's own lane-root derivation
asserts the files it addresses (`MISSING_LANE_FILE: <path>`, exit 2 — claim C3's instrument).

The **v3 G02 contract** the amended `tools/lane-preflight.py` must implement, frozen here as the rule the
battery legs encode: (i) the index source set is the recursive walk of `corpus/knowledge/`; every
non-directory entry must be a regular file whose name ends `.md` (case-sensitive; the only allowed non-`.md`
name is `.gitkeep`); a symlink is judged by its target (a symlink to a regular `.md` file passes, a dangling
or non-file symlink FAILs the gate); the knowledge path missing, not a directory, or not readable+searchable
by the running uid FAILs; zero `.md` entries under the walk FAILs (no vacuous pass). (ii) The index side:
`corpus/README.md` is normalized — `~~…~~` strike spans removed, markdown escapes `\_` `\*` `\[` `\]` `` \` ``
unescaped, percent-encoding in link targets unquoted, both sides NFC-normalized — and an entry counts as
indexed iff the README then matches `(?<![\w.-])(?:knowledge/)?NAME(?![\w-])` where NAME is the file's name
with the `.md` suffix (whole-token on the left against `[\w.-]`, on the right against `[\w-]`; a leading
`knowledge/` path prefix is allowed and never required). (iii) The mirror direction: every whole-token
`knowledge/…/<NAME>.md` occurrence in the normalized README must name a file that exists as a regular `.md`
file under `corpus/knowledge/` (a phantom row FAILs). (iv) `--work` naming an existing non-directory exits 2
with the contract's usage form (no GATE or summary line on stdout, the offending path on stderr). (v) A
reported name that is not valid UTF-8 is printed backslash-replaced so stdout stays strictly decodable.

Counting command (from the lane root; scratch under `$HYAKU_SCRATCH/chousa-r64/`):

    python3 corpus/evidence/round64/c1-battery-v3.py --tool tools/lane-preflight.py --fleet <fleet root> --work <dir> --jobs 6

**Before** (receipt `.ufo/waves/round-64/c1v3-before-full.txt`, exit 1, committed at or before the freeze):
the current tool at the base reads `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL` — all
seventeen attempt-1 defect legs, all eight attempt-1 benign legs and all three ZERO legs still pass unchanged
(no regression), and all fourteen G2 legs fail: E01/E05/E06/E07/E08/E09 `rc=0 want 1` (the vacuous or
substring pass), E02a/b/c `FAIL=[G01,G04,G05] want [G01,G02,G04,G05]` (G02 never fires), E10
`rc=1 (want 2 …)` (the traceback), E11 `battery-error UnicodeDecodeError` (the consumer breakage),
E12/E13/E14 `rc=1 want 0` (the false positives). A second, legs-only run of the fourteen G2 legs reads the
same fourteen failures (`.ufo/waves/round-64/before-e.txt`). The do-nothing control is this receipt itself:
the instrument that skips the claimed work — the unchanged tool — fails fourteen of the forty-three legs
where the target is `BATTERY=PASS`.

**After target**: the amended `tools/lane-preflight.py` (G02 v3 contract, G04/G05 amendments of round 63
unchanged) reads `CLEAN=1/1 DEFECTS=28/28 BENIGN=11/11 ZERO=3/3 BATTERY=PASS` exit 0 in three runs at the
landing bytes (`controls/c1v3-landed-runs.txt`, distinct seeds), the two committed nulls
(`corpus/evidence/round63/controls/null-pass.py`, `null-diff-oracle.py`) still read `BATTERY=FAIL` exit 1
under the v3 battery (`controls/c1v3-nulls.txt`), and the full preflight `python3 tools/lane-preflight.py
--root . --fleet <fleet root>` prints `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none` exit 0
(`controls/preflight-full-run-r64.txt`). The frozen attempt-2 battery still passes the amended tool ×2
(`controls/c1v2-on-v3tool.txt`) — the G02 change regresses nothing the round-63 freeze pinned. The sibling
receipt the round-63 closure routed (spot-check defect 1): `controls/sibling-g0405.txt`, the preflight run
read-only on kagi, kake and tameshi corpus copies with `--only G04,G05`, exit 0 per copy.

**Kill rule** (frozen): C1 is verified only when, at the closure, the unmodified `c1-battery-v3.py` reads
`BATTERY=PASS` for `tools/lane-preflight.py` at the landing commit in three runs, the nulls read FAIL, and the
v2 battery cross-check passes twice. A miss is an honest stop, not narrowed after landing. A falsifier class
a wave demonstrates against the v3 battery or against the v3 G02 rule is routed to the next battery, not a
refutation.

**Named limits** (disclosed before data): the G02 legs plant one fixture per RevG02 class, not every input
shape (D3's URL-only and code-span-only variants are covered by the strike-row leg E05's class only; D8's
leg pins NFC-file/NFD-index, not the reverse); the whole-token boundary class excludes `[coeff]w.-` on the
left and `[coeff]w-` on the right, so a name written with a trailing punctuation dot still matches
(sentence-final `NAME.md.` indexes) and a hyphenated prefix does not; the walk judges symlinks by target and
requires a real `.md` regular file — a lane that intentionally keeps a dangling entry cannot pass G02 (that
is the contract, not a bug); the mirror direction only checks `knowledge/…`-shaped tokens, so a README that
names an entry by a bare name it never indexed under `knowledge/` is unchecked; the battery never runs G08;
E11's before-failure is recorded as a battery-error (the consumer breakage the class names), not a tool
verdict.

## C2 — calibration: the claims-audit checker survives a committed, frozen mutant battery

Target axis: calibration — self-assessment checked against observed repo state (the axis is unmeasured in
`SCORECARD.md`; no numeric score is invented). Tag `plumbing`.

Round 63 attempt 2's closure routed "a mutation pass on the v2 battery and the checker (the L1-authored
instruments have had no external attack this round)". The checker `tools/claims-audit.py` (frozen bytes
`d48247f9c77ac1e7`) is amended never; this claim adds `tools/claims-audit-v2.py` and a frozen mutation
battery over both.

**Predicate R64-C2** (the sentence in the docstrings of `corpus/evidence/round64/gen-audit-mutants.py` and
`corpus/evidence/round64/c2-mutrun.py`): the frozen generator defines twelve textual mutants of
`tools/claims-audit.py` — A01 the stale-anchor exit 2 turned exit 0, A02 the stale-anchor detection removed
(a missing anchor silently skips), A03 the per-rule `FLAG` lines moved to stderr (consumer breakage), A04
detections suppressed (`fired += 0`), A05 `verbatim-heading` matching made case-insensitive, A06
`json-count` matching digits inside words (the round-63 mistake-2 class), A07 `git-first-commit` run with
`--diff-filter=AM` (the first-add read moves to a later modification), A08 `section-contains-at` treating
an unreadable revision as a pass, A09 the summary count printed without deriving it from the FLAG lines,
A10 rule-row validation weakened (an unknown rule name accepted, `check` silently returning unknown), A11
the selftest's own failing-case exit turned 0, A12 the `scope-narrower` quantifier narrowed to one literal —
each applied to a scratch copy of the target's committed bytes; patch application failure on a target is a
harness error (exit 2), never a kill. The frozen runner builds each mutant and scores it against the frozen
detection matrix, and a mutant is **killed** when at least one leg's exit code or required output differs
from its frozen expectation (the matrix detects the mutation) and **survives** when every leg holds. For
the v1 target the matrix legs are the committed receipts re-derived at run time (`--selftest` →
`AUDIT_SELFTEST=PASS (3 cases)` exit 0; the r62 audit → `FLAGGED=2/2 AUDIT=FAIL` exit 1; the audit-r63 twin
→ `FLAGGED=4/4 AUDIT=FAIL` exit 1; the a2 self-audit → `FLAGGED=0/4 AUDIT=PASS` exit 0; the probe
`corpus/evidence/round63/audit-probe.py` run against the mutant through a scratch mirror tree →
`PROBE_FACTS=11/11` exit 0). For the v2 target the matrix adds: the same receipts with the selftest leg
expecting `AUDIT_SELFTEST=PASS (10 cases)` and the r62 audit additionally requiring a stdout line starting
`FLAG `, the `--selftest-fault 1` red-leg exiting 1 with `FAULT` on stdout, and a frozen scratch-repo leg
whose git-first-commit target is modified after the add commit and must still fire. The runner prints one
`MUT <id> <killed|SURVIVED> <failing legs>` line per mutant and `AUDIT_MUTANTS_KILLED=<k>/12`, exit 0 iff
k = 12.

Counting commands (lane root):

    python3 corpus/evidence/round64/c2-mutrun.py --target tools/claims-audit.py --matrix v1 --work <dir>
    python3 corpus/evidence/round64/c2-mutrun.py --target tools/claims-audit-v2.py --matrix v2 --work <dir>

**Before** (receipt `controls/c2-mutrun-v1.txt`, exit 1, committed at or before the freeze): the v1 target
scores `AUDIT_MUTANTS_KILLED=6/12` — the matrix kills A01–A04, A09 and A12 (the receipts' own exits and the
probe's stale, flag-output and summary expectations), and six mutants SURVIVE it with every leg holding:
A05 (case-insensitive verbatim matching), A06 (digits inside words), A07 (the first-add read moved to a
later modification), A08 (an unreadable revision passing), A10 (weakened rule validation), A11 (the selftest
fault arm) — the honest red-before: the checker's own three-case selftest and its committed audit receipts
do not detect every class. The claim binds `k1 < 12` and the named survivors, not a different split.

**After target**: the v2 target scores `AUDIT_MUTANTS_KILLED=12/12` exit 0 (`controls/c2-mutrun-v2.txt`);
`tools/claims-audit-v2.py` keeps every v1 behavior the frozen receipts pin — the three audit commands and
the probe reproduce their frozen lines through the v2 binary (the runner's v2 matrix includes them
verbatim), and its expanded `--selftest` prints `AUDIT_SELFTEST=PASS (10 cases)` exit 0 with one `CASE`
line per case (the three v1 fixtures plus C4 a stale anchor, C5 a case-only verbatim mismatch, C6 an
unreadable revision, C7 a duplicate rule id, C8 the second quantifier arm, C9 a word-internal digit, C10
the FLAG lines required on stdout — one per surviving mutant class), and `--selftest-fault 1` exits 1 —
the selftest shown able to fail (`controls/audit-v2-selftest.txt`). The v1 checker is not edited; the
frozen attempt-2 receipts remain reproducible at the frozen bytes.

**Controls** (committed at or before the freeze): the v1 mutant receipt above is the do-nothing control —
skipping the claimed work leaves the twelve mutants scored against the v1 matrix with survivors; the
committed `claims-audit.py` outputs the matrix pins are re-derived from the frozen bytes at the same run
(the runner prints each unmuted leg's actual output beside its expectation). A null control: the runner run
against a target that does not exist exits 2 (`controls/c2-mutrun-null.txt`).

**Kill rule** (frozen): C2 is verified only when, at the closure, the unmodified generator and runner
reproduce `AUDIT_MUTANTS_KILLED=12/12` for the v2 target and the v1 receipt's survivors list, and the v2
expanded selftest and fault leg reproduce their stated outputs. A miss is an honest stop. A mutant a wave
seat authors beyond the frozen twelve that survives the v2 checker is routed to the next round's class list,
never folded into this claim.

**Named limits** (disclosed before data): the twelve mutants are authored by the same lane that writes the
v2 checker — the non-author attack this round is the wave's mutation seats, whose fresh mutants are attack
evidence, not the frozen set; the mutants are textual patches anchored on source spans of the v1 bytes,
so a v2 refactor that moves those spans without preserving the anchor is a harness error (exit 2), disclosed,
not a pass; the matrix pins exact output lines, so a mutant that only reformats honest output is killed as a
behavior change (output is the contract); A05 and A08 are killed only if the frozen audit TSVs or the v2
selftest cases actually distinguish the case (measured, not assumed).

## C3 — depth, sourced: `__file__`-derived lane roots assert the exact file they address

Target axis: depth — verifiable technical detail about this lane's instrument family, with a sourced
knowledge entry. Tag `ground`.

Round 63 attempt 2 mined the class (`corpus/lessons/round-63-attempt2.md` `## Mistakes` row 3): two scripts
derived the lane root from `Path(__file__).parents[2]` while living one directory deeper than their model,
measured absent things, and nothing caught the class ("captured-by none"). The routed fix: an
existence-assert rule for `__file__`-derived paths.

**Predicate R64-C3** (the sentence in the docstring of `corpus/evidence/round64/c3-count.py`): every round-64
instrument that derives a lane file from its own `__file__` — the frozen list in the counter is
`corpus/evidence/round64/c1-battery-v3.py` (asserts `corpus/SOURCES.md` and `tools/lane-preflight.py`),
`corpus/evidence/round64/run-receipts-v3.py` (asserts the same two) and
`corpus/evidence/round64/c3-count.py` itself (asserts `corpus/SOURCES.md`) — exits 2 printing
`MISSING_LANE_FILE: <path>` naming the exact missing path, before any measurement, when the file is not
present at the derived location; and the committed relocation probe `c3-count.py --work DIR` verifies, for
each listed instrument, that (i) a copy relocated one directory deeper (the `parents[2]`/`parents[3]`
off-by-one the mistake made twice) exits 2 with `MISSING_LANE_FILE: <path>` and (ii) the intact-tree smoke
runs still work. It prints `SMOKE=3/3 RELOCATION_MATCH=3/3 SHIFT_MUTANT_UNNAMED=1/1 C3=PASS` exit 0.

**Before** (receipts committed at or before the freeze): `controls/root-shift-mutant.py` — a committed copy
of the v3 battery without the startup asserts, placed one directory deeper (`controls/`, the mistake's exact
shape: the derivation is unadapted to the new depth) — run on the intact tree names no missing file: it
measures the wrong root and fails its CLEAN leg with a wrong verdict (`LEG CLEAN clean FAIL rc=1 want 0`,
exit via the `--only` PARTIAL path), recorded raw with the counter's own verdict in
`controls/c3-before.txt` (`SHIFT_MUTANT_UNNAMED=1/1`: the exhibit is unnamed — the unfixed behavior of the
class).

**After target**: `SMOKE=3/3 RELOCATION_MATCH=3/3 SHIFT_MUTANT_UNNAMED=1/1 C3=PASS` exit 0
(`controls/c3-after.txt`) — the three instruments name their missing file under relocation, the intact-tree
smoke runs still work, and the shifted mutant still does not name it (it is the unfixed exhibit, kept as
the red-before exhibit); the fixed instruments' asserts are shown able to fail by the relocation itself
(the mutant is the only committed artifact allowed to fail the contract, as its name records).

**Sourced**: the landed entry `corpus/knowledge/lane-root-derivation-r64.md` states what `__file__`-derived
roots do and do not guarantee — resolution, parents arithmetic with no binding to intent, and where the
existence check belongs (at first use of the derived path, the `realpath -e` refusal semantics) — citing
rows S150 and S151 opened this round (candidate rows: the Python `pathlib.Path.resolve`/`parents` docs of the
installed Python 3.14.8 and the GNU `realpath(1)` page of the installed coreutils, both local, no fetch; the
probe output is S152, own-work), with the `## Gate` recording each row's access date and located quote, ≥1
admit and ≥1 reject for the non-author spot-check. If the sources fail the quote check, the entry does not
land and C3 reports its sourced leg `unprovable` honestly — the asserts and the counter stand or fall on
their own receipts either way.

Counting command: `python3 corpus/evidence/round64/c3-count.py --work <dir>`.

**Kill rule** (frozen): C3 is verified only when, at the closure, the unmodified counter prints
`SMOKE=3/3 RELOCATION_MATCH=3/3 SHIFT_MUTANT_UNNAMED=1/1 C3=PASS` exit 0 and the entry is admitted with its
Gate rows (or C3's sourced leg is reported unprovable with the failure receipts). A miss is an honest stop.

**Named limits** (disclosed before data): the counter's relocation is a directory-depth shift, not a full
rename class; instruments whose lane files come only from caller arguments (`tools/claims-audit.py` v1
derives none from `__file__`) are out of the class and out of the list; the asserts fire at import time, so a
relocated-but-complete tree (a legitimate copy of the whole lane) still passes — the probe relocates the
instrument alone, not the lane.

## Frontier step (not a claim)

Census before and after with exit codes (`.ufo/waves/round-64/census-start.txt` exit 0, 149 rows; the end
receipt lands with the round). One mistake mined into `corpus/lessons/round-64.md` `## Mistakes`. The sourced
claim is C3 (S150–S152 candidates; ≥1 admit and ≥1 reject recorded in the Gate for the spot-check). The
assimilation state is re-derived this round (quarantine slice and id-collision receipts), with adoption
staying closed unless the checks open it; considerthese: exactly one still-unimplemented proposal may be
mined as a lesson pointer, no claim slot.

## Wave shape

One v2 wave (`w1`), 64 seats, validated under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json`
(band 64–128, maxLanes 256), dispatched after this freeze through the inline spawn handoff
(`.ufo/waves/round-64/w1.ready`), never by a lane `task` call. ≥25% attack seats (reviewer/critic/
mutation-tester), a few connector seats, one batched dispatch. Round total: 64 seats in one wave; no
residual call planned — any leftover check rides the wave items or is named in the report. The wave's
attack items (a non-author re-run of every counting command, fresh forgers and mutants against the v3
battery and the v2 checker, re-opens of the new S rows, the claims-file calibration read) are the round's
falsification force for both this round's claims and the round-63 attempt-2 instruments.

## Frozen instruments, digests and receipts

sha256 prefixes of the frozen bytes (`sha256sum FILE | cut -c1-16`), pinned before the freeze commit:
`c1-battery-v3.py` `4b3f0b658bcd3bb6`, `gen-audit-mutants.py` `6e1055b28d315e32`, `c2-mutrun.py`
`0045787ee9de3974`, `c3-count.py` `465a8c5efbb870f7`, `run-receipts-v3.py` `0f3cfae75f711f17`,
`controls/root-shift-mutant.py` `f0f9b26083ff62c3`, `tools/claims-audit-v2.py` `db0e28dd4c033259`.
Before-receipts committed at or before the freeze: `controls/c1v3-before-full.txt` (exit 1),
`controls/before-e.txt`, `controls/c1v3-nulls.txt`, `controls/c2-mutrun-v1.txt` (exit 1),
`controls/c2-mutrun-null.txt`, `controls/c3-before.txt`, `controls/sibling-g0405.txt`,
`.ufo/waves/round-64/census-start.txt`. The after-receipts named in the claims (`c1v3-landed-runs.txt`,
`audit-v2-selftest.txt`, `c2-mutrun-v2.txt`, `c3-after.txt`, `preflight-full-run-r64.txt`,
`c1v2-on-v3tool.txt`) are observed on the pre-landing tree whose measured bytes are the landing commit's,
verified at landing by `git diff --stat <landing-hash> --` over the measured paths being empty.

# R59Reviewer44 — adversarial review (axis: calibration)

Scope: claim design, controls, source grounding, and report/freeze contract for round 59.
Findings only; no lane file other than this report was written; no counter was executed;
no live fetch. All line numbers are from the bytes present at review time (2026-10-27).

## Findings

### High — H1: the round-59 frozen-claims contract does not exist; the wave dispatched against a missing prerequisite, so round-59 calibration has no object

The wave context and every one of the 66 item texts mandate `Read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round59/claims.md; read before work` (`.ufo/waves/round-59/w1-spec.json:10` and item strings, e.g. `:18`, `:362`). That file is absent:

- `read corpus/evidence/round59/claims.md` → "Path not found".
- `corpus/evidence/round59/` contains exactly `census-start.txt` (535 B, mtime 2026-10-27 15:12) and `controls/c1-before.txt` (958 B, mtime 2026-10-27 15:14). Nothing else.
- `git ls-tree -r --name-only HEAD -- corpus/evidence/round59` → empty; `git log --format=%h -- corpus/evidence/round59` → empty. The entire round-59 evidence tree has never been committed, so it is not "frozen" in any VCS-attestable sense (compare the lane's own standard: r40 "claim-freeze commit 6c01a414", r35 "freeze 0e167649", r38 "frozen ... at freeze 504c1d2a" — `LOG.md:1403,1474`, round-58 entry `LOG.md:1902-1906`).
- `.ufo/waves/round-59/w1.ready` was written anyway: `{"lane":"chousa","round":59,"wave":"w1","dispatch":...,"l1":"ChousaR59"}` — a readiness marker carrying no freeze/prerequisite field, so it cannot detect the missing claims input it declares readiness for.

The milestone ("build and falsify controls for positive verdict-path calibration") therefore has no round-59 predicate to calibrate: no claim, no target token, no kill rule, no declared counter. Seats that bound runs to the round-58 counter (many did — e.g. `w1/R59Executor05.md`, `w1/R59Executor07.md`, `w1/R59Executor11.md`) measured a round-58-branded object (`c1-count.py` hardcodes `corpus/evidence/round58/...` fixture rows and a `chousa-r58` scratch default), which cannot evidence a round-59 verdict path.

**Falsifier.** Produce the frozen claims bytes at `corpus/evidence/round59/claims.md` in the dispatch revision (or any lane commit) predating the wave, or a wave context that declares the round deliberately claims-free instead of asserting the file exists and ordering it read.

### High — H2: round-59's only control receipt is an uncommitted, headerless byte-copy of round-58's baseline; its provenance is unattested

- `sha256 corpus/evidence/round59/controls/c1-before.txt` = `sha256 corpus/evidence/round58/controls/c1-before.txt` = `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` (both 958 B). Round 59 preserved no measurement of its own; it copied the predecessor's.
- The copy is bare stdout with no header: no command line, no builder identity, no seed, no counter revision, no timestamp. The lane's own good form is `corpus/evidence/round58/controls/c1-controls.txt`, which carries a command header, the `DENIED=2/2` control evidence, and an interpretation footer. QUALITY 58 ("A counter's measured revision is pinned inside its receipt", `corpus/QUALITY.md:492` area) is unmeetable on a headerless receipt.
- The copied receipt records `DENIED=0/0` — it was produced without `--controls`, so it contains zero do-nothing control evidence. Round 59's controls directory holds nothing else (no `REFUSEALL.py`, no pinned-builder control, no `c1-controls.txt` equivalent), against the declared pattern "Controls are generated ... before dispatch ... receipts preserved under this directory before the build wave" (`corpus/evidence/round58/claims.md`, closing section).

**Falsifier.** A round-59 receipt whose bytes differ from round-58's, carrying builder/seed/counter-revision attestation and committed at freeze; or a committed claims.md explicitly declaring inheritance of the round-58 baseline for a byte-identical base builder. Neither exists.

### High — H3: the only executable predicate in the lane cannot print its positive token as frozen; round 59 dispatched in spite of the lesson recorded one round earlier (QUALITY 115)

Round 58's own close already established, by run, that the positive verdict path is unreachable (`LOG.md:1902-1915`, C1/C2 dispositions). I verified the mechanics statically in the frozen bytes:

- C1 (`corpus/evidence/round58/c1-count.py`, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`): `PASS = "pass"` (`:51`); every refusal-leg pass form is lowercase (`ESCAPE_ENTRY=pass(refused)` literal at `:315`; `FOREIGN`/`expect_refuse` build `f"…{PASS}(refused)"`), but the aggregation requires uppercase: `ref_pass = all(("=PASS" in l) for l in ref_legs)` (`:391`) and `SUMMARY … REFUSE={sum('=PASS' in l …)}` (`:399`). A builder satisfying all 11 declared legs therefore yields `REFUSE=0/7`, `C1=FAIL`, exit 1. The target token is unreachable as frozen.
- C2 (`corpus/evidence/round58/c2-count.py`, sha256 `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503`): `:100-101` requires the manifest `offset` to equal the quote's occurrence start in the defined form (`occurrences[0]!=off → CAPTURE_BIND`). The pinned builder — `tools/build-spans.py`, sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, i.e. byte-identical to the counter's pinned r55 builder constant — writes the span start (`form[max(0,off-80)…]`, "the `offset` column its start", `tools/build-spans.py:16`). Any quote with leading context mismatches by up to 80 chars. The lane's own measurement: builder offsets → `CAPTURE_BOUND=0/12` with `REBUILD=MATCH`; occurrence offsets → `12/12` with `REBUILD=FAIL`; no artifact reaches `C2=PASS` as frozen (`LOG.md`, round-58 C2 disposition).
- This is exactly the defect class QUALITY criterion 115 forbids: "A frozen counter must demonstrate its positive verdict path before it binds round data; a deny-only control set cannot prove that the target is reachable … if the positive control cannot reach the token, do not dispatch" (`corpus/QUALITY.md:974`, grounded in `corpus/lessons/round-58.md`). Round 59 was dispatched with no claims, no counters, and no positive-path demonstration — the criterion's mandated check did not gate this wave.

**Falsifier.** Run the frozen `c1-count.py` unmodified against a scratch builder satisfying each declared leg and obtain `C1=PASS` exit 0; or produce a builder-offset manifest that reaches `C2=PASS` with `REBUILD=MATCH`. Per the recorded runs, neither is possible without editing the frozen counter — which this round forbids.

### Medium — M1: control-design defects in the counter seats are calibrating against

In the same frozen `c1-count.py`:

- **(a) SYMLINK_OUT's target-write guard is cosmetic.** When a candidate refuses with a SYMLINK-class reason but the symlink target has gained unexpected files, the leg is rewritten to `SYMLINK_OUT=pass(refused)(target-dir-written!)` — and because `ref_pass` is a substring test (`:391`), it still counts as a pass. Only `real/spans.tsv` existence fails the leg (the `forbidden_touch` list). *Falsifier:* a builder that prints a SYMLINK refusal after writing `realdir/spans/S501-1.txt` still nets `REFUSE=7/7`-eligible output with the suffix attached.
- **(b) Do-nothing controls are checked only as "not C1=PASS"** (`:377`: `tail[0].strip() == "C1=PASS"` else `denied`). A control failing for the wrong reason (import crash, missing file, instant exception) is indistinguishable from failing for the intended reason, so the control does not prove the battery discriminates. QUALITY 17 ("A new runnable screen needs an independent failing control" — the control's *named observable* must move) is the lane's own bar.
- **(c) Dead assignment evidences an unclean patch path:** `ok_pass` is computed at `:389` and unconditionally overwritten at `:390`; the survivor is the case-fragile substring check that breaks the positive path (H3).

These matter operationally because round-59 seats are using this counter as the only executable predicate in the tree (H1), so its weaknesses are being inherited silently as "calibration" results.

### Medium — M2: "offline source reconnaissance" is one uncommitted census snapshot; warnings without dispositions

Round 59's entire source-side artifact is `corpus/evidence/round59/census-start.txt` (535 B, uncommitted): five W04 duplicate-URL warnings — S051 `w3.org/TR/2017/REC-html52…/syntax.html`, S053 `docs.python.org/3/library/socket.html`, S073 and S075 the *same* `gnu.org/.../coreutils.html`, S074 `docs.python.org/3/library/hashlib.html` — then `chousa ok …/corpus/SOURCES.md`, `exit=0`.

- A census warning is not a disposition. S073/S075 sharing one URL "across scopes" may be legitimate scope-based reuse; nothing in round-59 evidence records why, and no round-59 search-log row or SOURCES.md addition exists (round-58 close: rows remain 133, added A/B/C = 0/0/0, `LOG.md:1902-1915` source paragraph).
- The L0 fetch-scope question `8d77e6c1` remains open with no round-59 disposition; the lane's own lineage records it unanswered since round 29 (`corpus/lessons/round-29-verifier-spotcheck.md:66`; round-40/41 lessons restate the flip condition). With no live fetches and no round-59 claims, any currentness/completeness statement about sources would be ungrounded — correctly, no seat attempted one, but that also means the milestone's "offline source reconnaissance" leg has no substantive output beyond the census copy.

**Falsifier.** A round-59 SOURCES.md search-log entry (or claims section) scoping the reconnaissance and disposing the five warnings; none exists.

### Low — L1: report-contract notes

- A report already existed at this seat's path before this run; it was not authored by this session and is superseded by this file. Its overlapping claims (claims-file absence; receipt contents; census warnings) were re-verified here and hold; its line-number citations for the receipt check out (lines 14–16 = SUMMARY/C1/EXIT).
- `w1.ready`/`w1.ready.partial` encode no prerequisite verification (contents quoted under H1). A ready marker that checked the context's named files would have caught H1 before 66 seats were dispatched.

## Residual risk and verification gaps

- H3 and M1 are static byte reads plus the lane's recorded runs (round-58 LOG dispositions; round-58 W1 seats `R58ScribeMistakeMine.md`, `R58ReviewFrozenClaims.md`; round-59 seats `R59Executor07/08/11` reproduce them). I executed no counter; a run could in principle behave differently, but the string/logic evidence is direct and the recorded reproductions are consistent.
- I cannot exclude a round-59 claims file existing in a non-checked-out branch or remote; the working tree, HEAD tree, and full path history of this checkout contain none.
- Round-59 evidence being uncommitted means freeze-time identity is unverifiable from VCS; if bytes changed between dispatch and review, my mtimes (15:12/15:14) bound only this checkout's state.
- No scratch directory was created (nothing to remove); no tool installed; no pacman transaction; no git/jj/index writes; no live external fetch; no frozen claims, counters, or receipts modified.

Report trailer: `.ufo/waves/round-59/w1/R59Reviewer44.md`

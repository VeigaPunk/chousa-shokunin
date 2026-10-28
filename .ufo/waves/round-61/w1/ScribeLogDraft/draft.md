# Round 61 draft sections (ScribeLogDraft, wave w1)

Scope: text for three lane files, NOT written into them. Frozen facts only. Every value that exists only after measurement is the literal marker `<AFTER>`; the L1 fills each marker from landed counter output and deletes this note. No marker may be filled from a seat report, a fixture or a positive control.

Insertion points for the L1:
- Section 1 → `LOG.md`, appended after the `## Round 60 — pre-frozen counter claims fail no-op controls` entry (the file's last entry).
- Section 2 → `SCORECARD.md`, inserted after the `## Round 60 verdict` block and before `## Planned — round 61 (not started)`.
- Section 3a → `corpus/README.md`, top `## Coverage map` table, as the first data row (above `lessons/round-59.md`).
- Section 3b → `corpus/README.md`, appended after the `## Round57 coverage and frontier` section (re-check the file's last section before landing).

Kill rules that decide every verdict `<AFTER>` (frozen in `corpus/evidence/round61/claims.md`): C1 is verified only when the landed builder reads `LEGS=20/20 C1=PASS` exit 0 at three fresh seeds and `REAL_REBUILD=3/3`; C2 is verified only when `python3 corpus/evidence/round61/c2-count.py` prints `C2=PASS` exit 0 on the landed commit. Any other result is an honest stop and is written as one.

---

## 1. LOG.md entry (append)

## Round 61 — span-builder output safety (C1) and a sourced derived-output-safety entry (C2) (2026-10-28)

Intake: the round-60 closure (`corpus/lessons/round-60-verifier-spotcheck.md`, routed defects) found that the claim digest embedded in the prompts differed from the frozen file and that both frozen targets were reachable or unreachable by construction. Round 61 freezes two claims in `corpus/evidence/round61/claims.md` (sha256 `9afec8d4…ce0acec`, committed at `2b0e17b`, amended once before any seat existed from first freeze `1661b85`; base `9eef15e`). The same digest string appears in `.ufo/waves/round-61/w1-spec.json` and `w1-dispatch.json`. Each counter was built and exercised before the freeze against the base, do-nothing stubs, a token-forging stub, a naive-guard builder, a positive control and frozen mutants.

- **C1 operability (lowest scored axis).** Frozen counter `corpus/evidence/round61/c1-count.py`: 20 legs (P01–P06 behaviour, H07–H20 hazards) run on a builder copy beside `tools/capture-text.py`; each verdict comes from exit code, file tree and peak RSS only. Before, base `tools/build-spans.py` (blob `072415ad…`): `LEGS=7/20 C1=FAIL` exit 1 at seeds 61001 and 61002 (`controls/c1-before.txt`; P03 and H07–H17, H20 fail). After: `LEGS=<AFTER> C1=<AFTER>` exit `<AFTER>` at fresh seeds `<AFTER>`, `<AFTER>`, `<AFTER>`; no-harm `REAL_REBUILD=<AFTER>` (base `3/3`, `controls/regress-base.txt`). Verdict: `<AFTER>` (kill rule: verified only at 20/20 on all three seeds and `REAL_REBUILD=3/3`).
- **C1 discrimination receipts.** `controls/c1-controls.txt` (seed 61001): base 7/20; `exit 0` stub 1/20; `exit 2` stub 14/20; base builder that prints the target token 7/20; naive-guard builder 10/20; reference builder `controls/ref-build-spans.py` 20/20 at seeds 61001–61003; 14 frozen mutants M01–M14 each fail exactly their named legs (`CONTROLS_UNEXPECTED=0`). The verdict is not read from output; the forge-token control shows that.
- **C2 depth (sourced).** Frozen counter `corpus/evidence/round61/c2-count.py` checks the entry `corpus/knowledge/derived-output-safety-r61.md` (TRIO, ROWS, QUOTES, COVERAGE, CLAIMS, LIMITS, CENSUS). Before, base: `ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 LIMITS=0/1 CENSUS=1/1 C2=FAIL` exit 1 (`controls/c2-before.txt`; S134, S135, S136 absent). After: `ENTRY=<AFTER> TRIO=<AFTER> ROWS=<AFTER> QUOTES=<AFTER> COVERAGE=<AFTER> CLAIMS=<AFTER> LIMITS=<AFTER> CENSUS=<AFTER> C2=<AFTER>` exit `<AFTER>` on the landing commit. Verdict: `<AFTER>` (kill rule: verified only at `C2=PASS` exit 0).
- **Sources.** S134 (`open(2)`) and S135 (`rename(2)`) were opened offline from the installed man pages (`/usr/share/man/man2/open.2.gz`, `rename.2.gz`; package man-pages 6.19-1), rendered with `MANWIDTH=1000 man -l FILE | col -bx`; tier A. S136 is a lane file under `.ufo/` or `corpus/`; tier B. No canonical man7.org HTML render was opened this round, so these rows carry no URL (named access disclosure). S137 is a rejected own-work row: the builder docstring is intent, not evidence; it gives the round's Gate its reject. Registry rows: `<AFTER>` (base 133); census exit `<AFTER>`.
- **C2 discrimination receipts.** `controls/c2-controls.txt`: absent entry, absent rows, fabricated quote, cross-row quote, uncited quote, queued row, stale `opened`, row not used-by the entry, missing Limits, junk claim, over-25-word quote and missing provenance line each FAIL; the positive control (8 located quotes: S134 ×3, S135 ×3, S136 ×2) PASSES; a claim that echoes its quote also PASSES (`C2_CONTROLS_UNEXPECTED=0`). Recorded limit: the counter is structural and does not judge that a claim follows from its quotes. Non-author review of the claims against the rendered pages: `<AFTER>`.
- **Named limits (disclosed before data).** C1: (i) guard-then-write TOCTOU, so a directory swapped for a link between check and write is not stopped; (ii) the 64 MiB text-form cap and 96 MiB RSS limit are the lane's choice, not a measured need beyond "largest real `.txt` 15 MB, `.raw` 40 MB" (R55W2SentBuilder §2); (iii) the memory leg checks one 192 MiB read, not a sum over rows; (iv) the row-count × form-size cost is not a leg. C2: the CENSUS clause runs the fleet-root `scripts/sources-census.sh` (the counter's `--fleet` default is the fleet root, outside the lane tree), not a lane file.
- **Freeze discipline.** No counter, predicate, kill rule or control changed after the freeze; a post-data change would be a new claim. Seat reports under `.ufo/waves/round-61/w1/` are evidence to be checked, not measurements.
- **Waves.** One v2 wave, W1 = `<AFTER>` seats (`<AFTER>` executor, `<AFTER>` scout, `<AFTER>` reviewer, `<AFTER>` critic, `<AFTER>` mutation-tester, `<AFTER>` scribe, `<AFTER>` connector, `<AFTER>` sentinel, `<AFTER>` other); L1 held the planner seat; attack share `<AFTER>`; reports `<AFTER>`; dead seats `<AFTER>`.
- **Verdict.** C1 `<AFTER>`; C2 `<AFTER>`. The operability numeric score stays 3/10: the claim measures a leg count, and no new score is invented. Tools: `<AFTER>` (record each install as tool, version, channel, reason; none assumed). No external fetch was frozen as a claim; fetch-scope L0 `8d77e6c1` remains open. `Assimilation: none`.

---

## 2. SCORECARD.md round-61 verdict block (insert)

## Round 61 verdict — 2026-10-28 (span-builder output safety; derived-output-safety entry)

Claims frozen at `2b0e17b` (sha256 `9afec8d4…ce0acec`, amended from `1661b85`) against base `9eef15e`; receipts under `corpus/evidence/round61/controls/`.

| Claim / axis | Before → after | command / evidence | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis; numeric observable 3/10) | before: `LEGS=7/20 C1=FAIL` exit 1 (seeds 61001, 61002); after: `LEGS=<AFTER> C1=<AFTER>` exit `<AFTER>` at seeds `<AFTER>`; `REAL_REBUILD=<AFTER>` | `python3 corpus/evidence/round61/c1-count.py --builder tools/build-spans.py --work <fresh-dir>`; `controls/c1-before.txt`; `controls/c1-controls.txt` (`CONTROLS_UNEXPECTED=0`); `controls/c1-reference.txt`; `controls/regress-base.txt`; after-run receipts `<AFTER>` | `<AFTER>` (kill rule: 20/20 at three fresh seeds and `REAL_REBUILD=3/3`). Controls: exit-0 stub 1/20, exit-2 stub 14/20, so no stub reaches the target. No numeric score delta. |
| C2 depth (sourced: S134, S135, S136) | before: `ENTRY=0/1 … ROWS=0/3 … C2=FAIL` exit 1; after: `ENTRY=<AFTER> … ROWS=<AFTER> QUOTES=<AFTER> … C2=<AFTER>` exit `<AFTER>` | `python3 corpus/evidence/round61/c2-count.py`; `controls/c2-before.txt`; `controls/c2-controls.txt` (`C2_CONTROLS_UNEXPECTED=0`); `controls/c2-positive-entry.md` (8 quotes); after-run receipts `<AFTER>` | `<AFTER>` (kill rule: `C2=PASS` exit 0 on the landed commit). No depth score is invented. The counter does not judge that a claim follows from its quotes; that judgement is non-author review, `<AFTER>`. |

Axis table (historical scale; only the operability observable is numeric):

| axis | round-61 verdict | evidence |
|---|---|---|
| operability | **3/10 unchanged** (numeric observable not moved); C1 leg count `<AFTER>` | the C1 target is a 20-leg count of the builder's output safety; no score is derived from it. `controls/c1-controls.txt`. |
| depth | **<AFTER>** (C2 `<AFTER>`); no numeric score | `controls/c2-controls.txt`; entry `corpus/knowledge/derived-output-safety-r61.md` if landed. |
| coverage | **<AFTER>** (registry rows 133 → `<AFTER>`; S137 rejected, not counted) | `corpus/SOURCES.md`; census exit `<AFTER>`. |
| freshness | **unchanged** (no live fetch; fetch-scope L0 `8d77e6c1` open); S134 and S135 opened from local man pages only | `controls/regress-base.txt`; LOG Round 61 Sources. |
| calibration | **<AFTER>** (non-author review of claims against the man pages: `<AFTER>`); the counter's structural limit is recorded, not measured as calibration | `controls/c2-controls.txt`, `echo-claims rc=0`. |
| adjacency | **not claimed** by the frozen claims | none. |

Learning trends: expansion `<AFTER>`; quality `<AFTER>`; discernment `<AFTER>`.

Planned round-61 candidates, checked against this round: (a) digest binding: the frozen file's sha256 matches the value in the wave spec and dispatch record (`9afec8d4…`); (b) positive and no-op controls: run before dispatch, receipts in `controls/`. (c) "C2 requires a measured no-overreach predicate or should be dropped": **not met**. The frozen C2 measures structure and sourcing only; this is a named limit, and whether a later round adds an overreach predicate is `<AFTER>`.

---

## 3a. corpus/README.md coverage-map row (top table, first data row)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/derived-output-safety-r61.md` | Round-61 note (sourced, 2026-10-28), one entry binding derived-output safety to S134 (`open(2)`), S135 (`rename(2)`) and S136 (lane file) by located quotes; required sections `## Located quotes`, `## Claims`, `## Limits`; `<AFTER: one-line summary of the entry's claims>`; structural limit (claim-to-quote support not judged) named in `## Limits` | `S134`, `S135` (man-pages 6.19-1, local `man -l`); `S136` (lane file); `corpus/evidence/round61/c2-count.py`; `corpus/evidence/round61/controls/c2-controls.txt`; `LOG.md` Round 61 |

---

## 3b. corpus/README.md Round61 section and Frontier (append after the Round57 section)

## Round61 coverage and frontier (2026-10-28)

New ground: `<AFTER: one sentence stating what the entry newly grounds>`. The entry `corpus/knowledge/derived-output-safety-r61.md` is the round's sourced depth claim; its quotes are located in the man pages S134 and S135 and in the lane file S136 (`corpus/evidence/round61/c2-count.py` → `C2=<AFTER>`).

### Frontier

Advanced:

- **Span-builder output safety.** The span builder's output path is measured on 20 legs (`corpus/evidence/round61/c1-count.py` → `LEGS=<AFTER>`), covering the foreign-file, symlink, outside-cache, oversize, unreadable, FIFO and entry-dot hazards that `.ufo/waves/round-56/w1/R55W2SentBuilder.md` measured.
- **Man-page sourcing for a derived output.** Two tier-A rows are opened offline from the installed `open(2)` and `rename(2)` pages, so the entry's quotes are checked against text the lane can re-render (`MANWIDTH=1000 man -l FILE | col -bx`).

Left open:

- **Claim support.** The C2 counter is structural: it proves that quotes exist where their rows say and that every reference resolves. It does not judge that a claim follows from its quotes; the non-author review is `<AFTER>`.
- **Overreach.** No frozen predicate measures whether the entry claims more than its quotes support; the round-61 planned row asked for one, and it was not frozen.
- **Hazard classes outside the 20 legs.** Guard-then-write TOCTOU, the 64 MiB text-form cap beyond the largest real captures, the memory leg as one read rather than a sum over rows, and the row-count × form-size cost stay named limits.
- **The census script is outside the lane.** The C2 CENSUS clause runs the fleet-root `scripts/sources-census.sh`; the lane has no copy.
- **Canonical renders.** S134 and S135 have no man7.org HTML capture; their rows carry no URL.
- **The rest of the grey-literature family** (r41, r48) remains as in round 56.

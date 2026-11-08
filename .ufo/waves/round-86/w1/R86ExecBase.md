# R86ExecBase — lane chousa round 86 reproduction (BEFORE side: C1 do-nothing, C2 do-nothing)

Seat: `R86ExecBase` (leaf executor). Root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions: base `3bfb6885958ad4a674ad1896f70d1e836be609e4`; pre-round-85 tool `43c3f7284eee4889cdcc6ac1626573f6579cd533`
(`tools/gate-records.py`, the `2xx` rule); egress approval `e446875260a11e3489a0d78344d71d7fbb006a42` (not touched — no
fetch this seat); freeze `d0b1bd06872cdf0eeb03eccd099ff69ae6704307`; landed bytes attacked `667a5d091dc46168ed95eda0ae7f19a9bcf139a2`.
Scratch: `/fast/scratch/hyaku/chousa-r86/R86ExecBase/` (deleted before yield; every cited receipt was copied to
`.ufo/waves/round-86/w1/R86ExecBase/` first).
Tools: `python3` 3.14.8, `git` 2.56.0 (system; no installs — nothing needed beyond the stdlib). Network: **none**; every
input is a `git archive` of a committed revision.

## (0) Instrument identity — every pin MATCHES at landing; freeze copies equal landing copies

Command: extraction by `git -C <lane> archive <rev> | tar -x -C <scratch>/<name>` for `43c3f72`, `3bfb688`, `d0b1bd0`,
`667a5d0`, then `sha256sum` (script `verify-before.py`, receipt `verify-before.txt`).

| path | pin (instrument-pins.txt) | at landing `667a5d0` | at freeze `d0b1bd0` | verdict |
|---|---|---|---|---|
| `corpus/evidence/round86/gate-records-r86.py` | `20bc1a73…106d66` | `20bc1a73…106d66` | `20bc1a73…106d66` | MATCH |
| `corpus/evidence/round86/curation-r86.py` | `84a64ad4…e5c5d4` | `84a64ad4…e5c5d4` | `84a64ad4…e5c5d4` | MATCH |
| `corpus/evidence/round86/c2-positives.tsv` | `8c089828…01f3c6` | `8c089828…01f3c6` | `8c089828…01f3c6` | MATCH |
| `tools/gate-records.py` | `fe204539…7aa287` | `fe204539…7aa287` (base86 also `fe204539…`) | — | MATCH |
| `controls/receipts/c1-k0-donothing.txt` | `54219d2c…92fc7d91` | `54219d2c…92fc7d91` | `54219d2c…92fc7d91` | MATCH |
| `controls/receipts/c1-k0b-frozen-instrument.txt` | `6ed57748…b96d3f` | `6ed57748…b96d3f` | — | MATCH |
| `controls/receipts/c2-d0-donothing.txt` | `b3e6c6ad…4e06c` | `b3e6c6ad…4e06c` | `b3e6c6ad…4e06c` | MATCH |
| `instrument-pins.txt` itself | — | `549829c9…4c7aac` | `549829c9…4c7aac` | identical |

The pre-round-85 tool at `43c3f72` hashes `6e7a76f8862f6faaefaf1bccd54cabd79dfd05b43da45178afc640f9368e4c58`, not the pinned
subject tool — expected: the subject `tools/gate-records.py` is unchanged round-85→round-86 (`fe204539…` at `3bfb688`
and at `667a5d0`), while the do-nothing control's tool is the older `2xx` revision named by the receipt header.

No mismatch. Receipt: `.ufo/waves/round-86/w1/R86ExecBase/verify-before.txt`.

## (a) C1 BEFORE — the frozen round-86 battery against the pre-round-85 tool

Command (as assigned; `--repo`/`--work` are required by the instrument and were passed explicitly):

```sh
python3 -B /fast/scratch/hyaku/chousa-r86/R86ExecBase/land/corpus/evidence/round86/gate-records-r86.py \
  --root /fast/scratch/hyaku/chousa-r86/R86ExecBase/land \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --tool /fast/scratch/hyaku/chousa-r86/R86ExecBase/base85/tools/gate-records.py \
  --work /fast/scratch/hyaku/chousa-r86/R86ExecBase/work-c1a
```

Receipt: `.ufo/waves/round-86/w1/R86ExecBase/c1a-before-landroot-base85tool.txt`.
Observed (exit **1**):

```
WRONG_CODE g0066.md D4-non-timestamp-fetched S203 expected=PARSE got=REFETCH
… (12 D4 lines: S203,S204,S205,S206,S207,S008,S209,S210,S211,S028,S082,S083) …
NOT_REFUSED g0354.md D1-203-admit S021
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/355 EXPECTED_CODE=342/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=0/1 D1_FORGES=1 D1_REFUSED=0/1 MUT17_KILLED=0/1
GATE_RECORDS_R86=FAIL
exit: 1
```

This meets the assigned before expectation (`D1_REFUSED=0/1 MUT17_KILLED=0/1`, `GATE_RECORDS_R86=FAIL`, exit 1): the
`D1` class exists (`D1_FORGES=1`) and the `2xx` tool **accepts** it (`NOT_REFUSED … D1-203-admit S021`,
`D1_REFUSED=0/1`), and the mutant leg is unmeasurable on these tool bytes (`MUT17_KILLED=0/1`, see K4 below).
`SETUP=0/1` is also on the frozen control's field line; it is the old tool's own behavior, not a battery miss — probe
`probe-d1-mut-setup.txt`: non-git `--repo` + fresh rev record gives base85 `rc=1`, stdout `… S200 FAIL LINE,REV`
(no `GATE_RECORDS_ERROR`), while the landing tool gives `rc=2`, stderr `GATE_RECORDS_ERROR not a git repo: '<dir>'`
(`setup_ok=1`).

Same run with `--root` at the base tree `3bfb688` (the tree the committed receipt names) is byte-identical on every
body line — receipt `c1b-control-repro-base86root-base85tool.txt`, exit **1**. The landing-root/before-root difference
therefore produces no value drift.

D1 provenance (receipt `probe-d1-mut-setup.txt`): the frozen counter's `build_d1_203_admit` builds, from committed
bytes only, `GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A
decision=admit capture=corpus/captures/58725f5e0ac436166546a5ec.txt capture_sha256=7070b59c3434b677 words=10
quote="Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue."`, expected code `REFETCH`. The
backing `refetch.tsv` row is committed: `S021 … attempt 1 … fetched 2026-11-08T02:15:39Z … curl_rc 0 … http 203 …`,
`sha256(url)[:24] = 58725f5e0ac436166546a5ec` matches the row key, and the stored capture hashes to the row's
`txt_sha256` `7070b59c…` (190 bytes); the quote is located in that capture verbatim. The class is status-code-keyed
(a 203 body cannot ground a registered quote, `S216`), so the wording of the quote is immaterial.

## (b) C2 BEFORE — the frozen curation counter on the base tree

Command (as assigned):

```sh
python3 -B /fast/scratch/hyaku/chousa-r86/R86ExecBase/land/corpus/evidence/round86/curation-r86.py \
  --root /fast/scratch/hyaku/chousa-r86/R86ExecBase/base86
```

Receipt: `.ufo/waves/round-86/w1/R86ExecBase/c2a-control-repro-base86.txt`.
Observed (exit **1**), byte-identical to the committed control's body:

```
SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19
SUPERSEDED_STILL_LIVE S024 is mined while S031 supersedes it and is queued
UNENTAILED corpus/knowledge/search-transparency-reporting-r84.md row=Recording when a resource changed term=modification
UNENTAILED corpus/knowledge/provenance-recording-r85.md row=Recording when content was last reviewed term=modification
CURATION_R86=FAIL
exit: 1
```

This meets the assigned before expectation (`SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0`, `FAIL`,
exit 1), and the `QUOTES_LOCATED=19/19` total matches the claims' stated control.

Incidental (not this seat's score): the same counter on the landing tree prints
`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS`, exit **0**
(receipt `c2b-landroot.txt`); the after side is owned by the wave's scored seats.

## (c) Byte-compare of observed predicate/field lines against the committed controls — NO VALUE DRIFT

The committed receipts were compared after stripping their leading `#` provenance lines (the only difference by
construction: they name the L1 scratch tree and the tool path of the L1 run). Comparison script `verify-before.py`,
receipt `verify-before.txt`, exit **0**:

| comparison | body lines | result |
|---|---|---|
| `c1-k0-donothing.txt` vs c1b (base root, same tool) | 16 vs 16 | **identical=True** (diff emitted nothing) |
| `c1-k0-donothing.txt` vs c1a (landing root) | 16 vs 16 | **identical=True** |
| `c2-d0-donothing.txt` vs c2a (base root) | 6 vs 6 | **identical=True** |

The whole-file sha256 of my receipts differs from the committed ones only because the `#` header (tree/tool paths,
scratch location) differs; the counter output bodies, including the predicate and field lines above, are equal line
for line. The instrument files themselves did **not** differ (all pins match, section 0), so this is not instrument-byte
drift; it is only the receipts' provenance headers. No finding.

## (d) Committed controls are not stale — C1 K3, C1 K4, C2 K1

- **C1 K3 (harm control side).** The before run shows `POSITIVE=15/15 FRESH_POSITIVE=5/5`: every genuine committed
  record (15 frozen + 5 fresh) is accepted by the pre-round tool, reproduced now from committed bytes. The landing-accept
  half of K3 is the after-side seats' measurement; my control's half is live, not stale.
- **C1 K4 (mutant leg derived from the subject tool's bytes).** The before run prints `MUT17_KILLED=0/1`, and the reason
  is verified, not assumed: the counter's `build_mutant` (landing counter lines 284-290) is
  `src.replace('r[6] == "200"', 'r[6].startswith("2")')` and returns `False` when the bytes are unchanged. The `43c3f72`
  tool (`6e7a76f8…`) contains **0** occurrences of `r[6] == "200"` (its `2xx` rule is
  `re.fullmatch(r"2[0-9][0-9]", r[6])`, line 224), so derivation returns `derives=False` and the counter prints
  `MUT17_KILLED=0/1` — exactly the K4 failure mode "cannot derive one". The subject tool at `3bfb688` and `667a5d0`
  (`fe204539…`) contains exactly **1** occurrence and derives a **+7-byte** mutant (`derives=True`), so the mutant leg is
  genuinely available on the claim's subject and the control is not describing stale bytes. The counter hard-codes no
  mutant text (source read; only the `replace` above). Probe receipt: `probe-d1-mut-setup.txt`.
- **C2 K1 (predicate not met at base).** The base-tree run reproduces the frozen predicate failure exactly (field line
  and all three detail lines), exit **1**; the committed control is a live reproduction, not a stale receipt.
- Supporting identity: the counter/tool/TSV shas equal the pins at landing and at freeze, and the working-tree `git grep`
  input the C1 counter reads (`corpus/lessons`) is unchanged from landing: `git -C <lane> diff --stat 667a5d0..HEAD --
  corpus/lessons corpus/SOURCES.md corpus/captures corpus/evidence/round57 corpus/evidence/round86` is empty (HEAD
  `a9bed303` differs from landing only by the untracked/`w1` wave spec), and `git status --porcelain` shows no modified
  tracked file.

## Findings

No drift and no kill-rule finding from this seat's before measurements. Two observations, neither a kill:

1. `SETUP=0/1` appears on the before field line. It is the old tool's missing non-git-repo guard (section a probe) and is
   present verbatim on the frozen `c1-k0-donothing.txt`; it is not a value drift and does not alter the `D1`/`M17` fields
   the seat names.
2. The `D1` record's quote is a cookie-wall sentence from the 203 body. The class is keyed on the HTTP status (a 203
   body cannot ground a quote, `S216`), the quote is located in the committed capture, and the expected code is
   `REFETCH`; the before defect is precisely that the `2xx` tool accepts the record.

## Risks / blockers

None. No network, no installs, no production/lane git mutation; scratch removed before yield. After-side scoring
(`GATE_RECORDS_R86=PASS`, `CURATION_R86=PASS`) is not this seat's assignment and was not used as a verdict.

VERDICT: R86ExecBase C1 held — the before control reproduces byte-identically from committed bytes (`D1_REFUSED=0/1 MUT17_KILLED=0/1`, `GATE_RECORDS_R86=FAIL`, exit 1), with K4's zero explained by the old tool's bytes lacking the `r[6] == "200"` token.
VERDICT: R86ExecBase C2 held — the before control reproduces byte-identically from committed bytes (`SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19`, `CURATION_R86=FAIL`, exit 1).

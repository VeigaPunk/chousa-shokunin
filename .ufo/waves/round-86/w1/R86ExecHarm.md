# R86ExecHarm — C1 K3 harm leg: landing tool vs pre-round-85 tool over ALL committed records

Seat `R86ExecHarm`, leaf. Revisions: base `3bfb6885958ad4a674ad1896f70d1e836be609e4`; landed bytes attacked
`667a5d091dc46168ed95eda0ae7f19a9bcf139a2`; pre-round-85 baseline `43c3f7284eee4889cdcc6ac1626573f6579cd533`
(round-84 tip). Claim freeze `d0b1bd06872cdf0eeb03eccd099ff69ae6704307`. No network was used; every check reads
committed bytes. Every artifact cited below is written under
`.ufo/waves/round-86/w1/R86ExecHarm/` (paths in this report are lane-relative).

Subject tool: `tools/gate-records.py`. Bytes at landing and at the round-86 base are identical
(`sha256 fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287`, matching `instrument-pins.txt`);
the pre-round-85 tool is `sha256 6e7a76f8862f6faaefaf1bccd54cabd79dfd05b43da45178afc640f9368e4c58`. **Round 86 changed
no subject-tool bytes**, so every verdict move below is attributable to the round-85 repair already present at the
base, not to a round-86 edit.

## 1. Denominators

| quantity | observed | receipt |
|---|---|---|
| coarse committed `GATE-RECORD` lines at landing (`git grep -c -E '^[[:space:]]*GATE-RECORD' 667a5d09…`) | **445 lines across 362 files** | `01-grep-counts.txt` |
| records by the tool's own grammar (`lead_strip` + `^GATE-RECORD(?:\s|$)`), every file of the landing extract | **449 records across 366 files** | `02-tool-detected-records.txt`, list in `02b-files-landing.txt` |
| records in the pre-round tree (43c3f728 extract, same scanner) | **355 records across 276 files** | `02c-files-pre.txt`, `07-pre-tree-comparison.txt` |
| frozen positives (`c2-positives.tsv`) | **15** | `04-frozen-positives.txt` |
| fresh positives (counter builder) | **5** (2 admit, 2 rev, 1 unreach) | `06-denominators.txt` |
| forged-battery total (counter builder, landing bytes) | **355** (354 pre-existing + 1 `D1-203-admit`) | `06-denominators.txt` |

Why 449 and not 445. The tool's grammar strips leading Unicode Cf characters and requires `GATE-RECORD` followed by
whitespace/EOL; `git grep`'s `[[:space:]]` does neither. Five records carry a BOM/ZWSP before the word and are
invisible to the grep (`R83ExecForge/forge/c061-bom.md`, `c062-zwsp-prefix.md`, `R84ExecForge/forge/X006-bom.md`,
`X007-zwsp-lead.md`, `R85ExecForge/forge/k04-zwsp-prefix.md`); one grep line is prose, not a record
(`c077-prose-only.md:3` = `GATE-RECORDS are described in prose only.`). 445 + 5 − 1 = 449.

How the run was made. The landing tree was built with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 667a5d091dc46168ed95eda0ae7f19a9bcf139a2 | tar -x -C /fast/scratch/hyaku/chousa-r86/R86ExecHarm/landing`
and the pre-round tree the same way from `43c3f728…`. Both tools were run over the identical 366-file list, identical
`--root`, and the same `--repo` (the lane repo, read-only `git cat-file`):

```sh
python3 -B <tool> verify --root /fast/scratch/hyaku/chousa-r86/R86ExecHarm/landing \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <366 files from 02b-files-landing.txt>
```

Observed summaries (`03-tool-comparison-landing-tree.txt`, exit 1 in both cases because per-record FAILs exist):

```
GATE_RECORDS files=366 records=449 ok=163 fail=286     # landing tool
GATE_RECORDS files=366 records=449 ok=165 fail=284     # pre-round-85 tool
```

The 449 keys are identical in both outputs; no record appears in only one tool's output. A second run with
`--repo` pointing at a scratch clone (`tmp.GKok0g1W7D`, created under
`/fast/scratch/hyaku/chousa-r86/R86ExecHarm/`, `--shared --no-checkout`, `git rev-parse --show-toplevel` asserted
equal to the clone dir, no mutating git command) produced byte-identical stdout for both tools
(`09-clone-identity.txt`), so the verdicts do not depend on the lane working tree.

## 2. Per-record verdict diff (ALL committed records)

`03b-verdict-diff.tsv` records exactly these moves — 4 OK→FAIL and 2 FAIL→OK; 443 records unchanged:

| # | file:line | pre-round-85 | landing | landing code | artifact class |
|---|---|---|---|---|---|
| 1 | `.ufo/waves/round-83/w1/R83ExecForge/forge/c022-decision-reject-admit-form.md:1` | OK | FAIL | `PARSE` | round-83 forge probe (synthetic) |
| 2 | `.ufo/waves/round-85/w1/R85ExecForge/forge/d05-admit-reject-with-capture.md:1` | OK | FAIL | `PARSE` | round-85 forge probe (synthetic) |
| 3 | `.ufo/waves/round-85/w1/R85ExecForge/forge/f01-admit-203-s021.md:1` | OK | FAIL | `REFETCH` | round-85 forge probe (synthetic) |
| 4 | `.ufo/waves/round-85/w1/R85MutationTool/receipts/witnesses/W-M17-203-admit.md:1` | OK | FAIL | `REFETCH` | mutation witness (synthetic) |
| 5 | `.ufo/waves/round-85/w1/R85ExecForge/forge/n02-unreach-203-s021.md:1` | FAIL `REFETCH` | OK | — | round-85 forge probe (synthetic) |
| 6 | `.ufo/waves/round-85/w1/R85MutationTool/receipts/witnesses/W-M31-203-unreach.md:1` | FAIL `REFETCH` | OK | — | mutation witness (synthetic) |

Readings, in order:

- **Rows 3–4 are the C1 target class, not harm.** Both are the committed `S021` 203-body admit: the pre-round-85
  tool's `http 2xx` REFETCH rule accepts them; the landing tool's `http == "200"` rule refuses them with `REFETCH`.
  This is exactly the `D1`/`M17` differentiator the round is built on. The same bytes reproduce the frozen
  `c1-k0-donothing.txt` control (`D1_REFUSED=0/1` on the 2xx tool).
- **Rows 1–2 are the admit-form/`decision=reject` PARSE tightening**, introduced by the round-85 integration commit
  `a8041fcd` (`git log -S 'kv["decision"] != "admit"' -- tools/gate-records.py`), i.e. before the round-86 base. Both
  lines are single-line forge probes whose form says `decision=admit` while the key says `decision=reject` and a
  capture is attached — a contradictory shape, not a lane record.
- **Rows 5–6 are a correction, not a regression.** The pre-round-85 tool treated any `2xx` as a successful retrieval,
  so it refused a legitimate `decision=reject … http=203` record. The landing tool counts `200` only as success, so a
  203 reject record whose refetch row matches is valid. This is the same round-85 rule viewed from the unreach side.
- No genuine lane record is among the moves (see §3).

## 3. The K3 positive legs (what K3 actually protects)

K3 is "a genuine committed record that the pre-round tool accepts is refused at landing (the 15 frozen and 5 fresh
positive legs)". Those legs were run explicitly.

Frozen 15 (`04-frozen-positives.txt`; `corpus/lessons/round-80.md:19-22`, `round-81.md:23-28`, `round-82.md:57-61`):

```
GATE_RECORDS files=3 records=15 ok=15 fail=0      # landing tool,  exit 0
GATE_RECORDS files=3 records=15 ok=15 fail=0      # pre-round-85 tool, exit 0
```

Fresh 5, rebuilt from committed bytes by the frozen counter's own `build_fresh_positives()` (`05-fresh-and-d1.txt`;
S082, S083 admits · S199, S200 revs · S100 unreach):

```
GATE_RECORDS files=5 records=5 ok=5 fail=0        # landing tool,  exit 0
GATE_RECORDS files=5 records=5 ok=5 fail=0        # pre-round-85 tool, exit 0
```

Broader genuine-record check: outside `.ufo/` the landing tree has 27 committed record lines — 26 `OK` and 1
pre-existing `FAIL PARSE` under **both** tools (`corpus/evidence/round80/gate-grounding-check.py:13`, a docstring
template line `GATE-RECORD <id> rev=…`, not a record that ever verified; pre-existing since round 80, not a move).
Every record in `corpus/lessons/round-83…86.md` (including the round-86 `S216` and `S031` records) is `OK` under
the landing tool. So the genuine subset moved zero records OK→FAIL.

## 4. The `D1` class witness (mechanism check)

The frozen counter's `build_d1_203_admit()` run over the landing bytes returns `D1_BUILD=present`, `sid=S021`,
`code=REFETCH` (`06-denominators.txt`). The record is grounded in the committed refetch row
(`corpus/evidence/round57/refetch.tsv`): `S021  https://pubmed.ncbi.nlm.nih.gov/17638714/
58725f5e0ac436166546a5ec  1  2026-11-08T02:15:39Z  0  203  …  7070b59c…` whose `txt_sha256` equals
`sha256(corpus/captures/58725f5e0ac436166546a5ec.txt)` (`10-subject-rows-and-pins.txt`). The generated line:

```
GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A
decision=admit capture=corpus/captures/58725f5e0ac436166546a5ec.txt capture_sha256=7070b59c3434b677
words=10 quote="Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue."
```

Both tools on it (`05-fresh-and-d1.txt`):

```
GATE_RECORD d1-record.md:1 S021 FAIL REFETCH     # landing tool,  exit 1
GATE_RECORD d1-record.md:1 S021 OK               # pre-round-85 tool, exit 0
```

The committed forge `f01-admit-203-s021.md` independently shows the same move (row 3 above, `REFETCH`), so the D1
witness exists both from committed bytes and inside the predicate.

## 5. Denominator reconciliation with the counter's 355

`FORGED_TOTAL=355` was reproduced by importing the frozen counter and calling its own builders over the landing
bytes (`06-denominators.txt`): 20 positives (15 frozen + 5 fresh = 12 admit, 6 rev, 2 unreach) generate
`M01–M21/R01–R08/U01–U06` mutations, plus 0 `D1-stale-refetch-txt-sha-drift` lines on this estate, plus 1
`D1-203-admit`. Breakdown sums to 355; non-D1 total is 354, matching the frozen control
`controls/receipts/c1-k0b-frozen-instrument.txt` (`FORGED_REFUSED=354/354`, exit 0). So 355 = **354 pre-existing
forgeries + 1 new D1 203-body admit**.

The 355 is **not** a committed-record count and does not match 449 by construction: the battery counts generated
forgery lines (one per mutation over 20 positive source lines), while the harm leg counts committed `GATE-RECORD`
lines in the tree. The pre-round tree's 355 committed records is a different set with an unrelated equality; it must
not be read as the battery total.

## 6. Findings and risks

- **F1 (no harm to genuine records).** 0 of 26 verified genuine lane records moved OK→FAIL; frozen 15/15 and fresh
  5/5 are accepted by the landing tool (`04`, `05`). K3 does not fire.
- **F2 (four fixture refusals, disclosed).** The literal all-records sweep has 4 OK→FAIL and 2 FAIL→OK, all six in
  synthetic `forge/` or mutation-witness artifacts. The two `REFETCH` refusals are the intended 203-admit class
  (rows 3–4); the two `PARSE` refusals are the round-85 admit-form/decision tightening (rows 1–2).
- **F3 (residual narrowing risk).** Any future genuine record pairing the admit form with `decision=reject` and a
  capture is now unverifiable (`PARSE`). No committed genuine record has that shape; the grammar documented in the
  tool header lists `decision=<admit|reject>` for the admit form, so the tightening closes a contradiction rather
  than a lane case. The unreach side now accepts `203` reject records (rows 5–6), which is consistent with
  `S216` (a 203 body is not the origin representation, so it cannot ground a quote but may be recorded as
  non-success).
- **F4 (pre-existing, not this round).** `corpus/evidence/round80/gate-grounding-check.py:13` is detected as a record
  by the tool grammar and fails `PARSE` under both tools; it is a docstring template, unchanged this round.

## 7. Tooling

No tool was installed, upgraded, or changed this round; no pacman transaction was attempted. Scratch root
`/fast/scratch/hyaku/chousa-r86/R86ExecHarm/` was used for both extracts, the clone control, and the generated
fresh/D1 records, and is removed before this report was finalized. Nothing outside this seat's wave folder and its
scratch dir was written; the lane repo was only read (`archive`, `grep`, `cat-file`, `show`).

## 8. Receipts (all under `.ufo/waves/round-86/w1/R86ExecHarm/`)

| receipt | contents |
|---|---|
| `01-grep-counts.txt` | `git grep -c` per file at `667a5d09` (362 files) and total 445 |
| `02-tool-detected-records.txt` | per-file tool-grammar counts, `files=366 records=449` |
| `02b-files-landing.txt` | the exact 366-path argument list |
| `02c-files-pre.txt` | the exact 276-path argument list for the pre-round tree |
| `03-tool-comparison-landing-tree.txt` | full stdout/exit of both tools on the landing tree |
| `03b-verdict-diff.tsv` | the six verdict moves, machine-readable |
| `04-frozen-positives.txt` | 15/15 OK under both tools, exit 0 |
| `05-fresh-and-d1.txt` | fresh 5/5 OK under both, exit 0; D1 `REFETCH` (landing, exit 1) vs `OK` (pre, exit 0) |
| `06-denominators.txt` | `FORGED_TOTAL=355`, D1 build line, positive/fresh counts |
| `07-pre-tree-comparison.txt` | both tools over the 43c3f728 extract (276 files, 355 records), exit 1 |
| `07b-pre-tree-diff.tsv` | pre-tree diff: 1 OK→FAIL (`c022`), 0 FAIL→OK |
| `08-cross-tree.txt` | `COMMON_KEYS=355 O2F=1 F2O=0` |
| `09-clone-identity.txt` | clone-vs-lane-repo runs byte-identical (both tools) |
| `10-subject-rows-and-pins.txt` | S021 refetch row, capture sha, registry row, tool hashes, rule-change commits |
| `11-summary-counts.txt` | one-page authoritative command/observed-line/exit index |

VERDICT: R86ExecHarm C1 held — over all 449 committed records the landing tool refuses none of the 15 frozen or 5 fresh positive legs (both 15/15 and 5/5 OK); the only four OK→FAIL moves are synthetic forge/witness fixtures, two of them being the intended `D1` 203-body `REFETCH` class, and no genuine lane record moves.

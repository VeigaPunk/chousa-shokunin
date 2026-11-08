# R86ExecRepro — reproduction of the two frozen round-86 claims from a clean tree

Seat `R86ExecRepro` (leaf). Lane `chousa`, round 86, wave w1. Landing bytes attacked:
`667a5d091dc46168ed95eda0ae7f19a9bcf139a2`. Freeze `d0b1bd06872cdf0eeb03eccd099ff69ae6704307`. All commands
read committed bytes only; no network, no lane or fleet mutation, no production edits. Scratch:
`/fast/scratch/hyaku/chousa-r86/R86ExecRepro` (created with `mkdir -p`, deleted after the receipts were copied).

## (a) instrument-identity leg — pins at the landing revision

Command (receipt `.ufo/waves/round-86/w1/R86ExecRepro/receipts/pins-gitshow.txt`, exit 0):

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
grep -E '^[0-9a-f]{64} ' corpus/evidence/round86/instrument-pins.txt | while read -r pin path; do
  got=$(git show 667a5d091dc46168ed95eda0ae7f19a9bcf139a2:"$path" | sha256sum | cut -d' ' -f1)
  [ "$got" = "$pin" ] && echo "MATCH  $path" || echo "MISMATCH  $path pin=$pin got=$got"
done
```

| path | pin | verdict |
|---|---|---|
| `corpus/evidence/round86/gate-records-r86.py` | `20bc1a733bd6c79f428a16c564cdc49555d8f02c389307eb2c6a28ceeb106d66` | MATCH |
| `corpus/evidence/round86/curation-r86.py` | `84a64ad48d77e63095919942ac113bbb1b54b4e7d9acd21ef85a4f58e545c5d4` | MATCH |
| `corpus/evidence/round86/c2-positives.tsv` | `8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6` | MATCH |
| `tools/gate-records.py` | `fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287` | MATCH |
| `corpus/evidence/round86/controls/receipts/c1-k0-donothing.txt` | `54219d2c9a1d2f8c919b6bb09479e1a2d0f154d6cbbda40926b2fc4992fc7d91` | MATCH |
| `corpus/evidence/round86/controls/receipts/c1-k0b-frozen-instrument.txt` | `6ed57748d21f18927f402caa66c778083c6ea993f30ab2df5aea7a9d88b96d3f` | MATCH |
| `corpus/evidence/round86/controls/receipts/c2-d0-donothing.txt` | `b3e6c6ad05a381f9a55d412dee184adf5be86c05a6774aa34e8a7f741724e06c` | MATCH |

`MISMATCHES=0`, exit 0. A second run with `git cat-file -p <rev>:<path>` (byte-identical to `git show`) gives the
same seven MATCHes (`.ufo/waves/round-86/w1/R86ExecRepro/receipts/pins-catfile.txt`).

Post-freeze stability: `git diff d0b1bd06 667a5d09 -- corpus/evidence/round86/` shows only the two `after/c*-after.txt`
receipts added; the counters, `c2-positives.tsv`, `instrument-pins.txt` and `claims.md` hash identically at the freeze
and at landing (`gate-records-r86.py` `20bc1a73…`, `curation-r86.py` `84a64ad4…`, `c2-positives.tsv` `8c089828…`,
pins `549829c9…`, claims `9c8f01f0…` at both revisions).

## (b) scored runs from a clean tree at the landing revision

Extraction (exit 0):

```sh
S=/fast/scratch/hyaku/chousa-r86/R86ExecRepro
mkdir -p "$S/tree"
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 667a5d091dc46168ed95eda0ae7f19a9bcf139a2 | tar -x -C "$S/tree"
```

C1 (receipt `.ufo/waves/round-86/w1/R86ExecRepro/receipts/gate-r86.out`, **exit 0**):

```sh
python3 -B "$S/tree/corpus/evidence/round86/gate-records-r86.py" --root "$S/tree" --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work "$S"
```

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1
GATE_RECORDS_R86=PASS
EXIT=0
```

Zero `WRONG_CODE` lines and zero `NOT_REFUSED` lines in the receipt (`grep -c` = 0 / 0). The claims counting command
run verbatim in its own extraction (`$S/claimsrun`) prints the identical field line and `EXIT=0`
(`receipts/gate-claimscmd.out`).

C2 (receipt `.ufo/waves/round-86/w1/R86ExecRepro/receipts/curation-r86.out`, **exit 0**):

```sh
python3 -B "$S/tree/corpus/evidence/round86/curation-r86.py" --root "$S/tree"
```

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
CURATION_R86=PASS
EXIT=0
```

The claims counting command against the lane root (`--root /home/vgpnk/Projects/shokunin/chousa-shokunin`, lane HEAD
`a9bed303`, whose only post-landing diff is wave scaffolding — no claim bytes) prints the same line, `EXIT=0`
(`receipts/curation-liveroot.out`).

## (c) field-by-field comparison with `claims.md`

### C1 `C1-BATTERY-R86`

| claims.md requirement | observed | difference |
|---|---|---|
| `GATE_RECORDS_R86=PASS`, exit 0 | `GATE_RECORDS_R86=PASS`, exit 0 | none |
| `TOOL=present` | `TOOL=present` | none |
| `POSITIVE=15/15` | `POSITIVE=15/15` | none |
| `FRESH_POSITIVE=5/5` | `FRESH_POSITIVE=5/5` | none |
| `FORGED_REFUSED` = `EXPECTED_CODE` = generated total | `FORGED_REFUSED=355/355 EXPECTED_CODE=355/355`; `total_forged = len(forged)` computed at runtime (code line 363), not pinned; 355 = 354 legacy forges + the 1 `D1-203-admit` | none |
| `EMPTY_REFUSED=1/1` | `EMPTY_REFUSED=1/1` | none |
| `RC=4/4` | `RC=4/4` | none |
| `SETUP=1/1` | `SETUP=1/1` | none |
| `D1_FORGES=1` | `D1_FORGES=1` | none |
| `D1_REFUSED=1/1` | `D1_REFUSED=1/1` | none |
| `MUT17_KILLED=1/1` | `MUT17_KILLED=1/1` | none |

Kill-rule mapping: **K1** not triggered (PASS at landing). **K2** not triggered: no forged record accepted
(`NOT_REFUSED` count 0) and no refusal outside its expected code (`WRONG_CODE` count 0). **K3** (harm) not exercised
beyond the predicate's own positive legs, which read `15/15` and `5/5`. **K4** verified independently below — the
mutant is derived from the subject tool's bytes, not hard-coded.

### C2 `C2-CURATION-R86`

| claims.md requirement | observed | difference |
|---|---|---|
| `CURATION_R86=PASS`, exit 0 | `CURATION_R86=PASS`, exit 0 | none |
| `SUPERSEDED_LIVE=0` | `SUPERSEDED_LIVE=0` | none |
| `UNENTAILED_TERM=0` | `UNENTAILED_TERM=0` | none |
| `MODIFIED_DEF_CITED=1` | `MODIFIED_DEF_CITED=1` | none |
| `QUOTES_LOCATED` = total, total ≥ 19 | `QUOTES_LOCATED=20/20` (r84 13 + r85 7 = 20; base tree carries 12 + 7 = 19, so the repair adds exactly the one `Q13` row) | none |

Kill-rule mapping: **K1** not triggered. **K2** independently re-checked (below) at 20/20. **K3** is a reviewer
finding, not a counter field; not adjudicated here. **K4** independently re-checked (below): the added quote is
`S023` and the r85 entry cites `S031`, never `S024`.

## Independent identity leg (not the counter's own output)

Receipts: `receipts/identity-leg.out` (exit 0), `receipts/c2-independent.out` (exit 0); scripts kept beside them.

C1 identity (`python3 -B identity.py $S`):

- `S021` refetch row read from committed `corpus/evidence/round57/refetch.tsv`: `curl_rc=0 http=203`, key
  `58725f5e0ac436166546a5ec`, `txt_sha=7070b59c3434b677…`; the committed capture
  `corpus/captures/58725f5e0ac436166546a5ec.txt` hashes to exactly that `txt_sha`.
- `build_d1_203_admit` returns `sid=S021 expected_code=REFETCH` with
  `GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A decision=admit
  capture=corpus/captures/58725f5e0ac436166546a5ec.txt capture_sha256=7070b59c3434b677 words=10
  quote="Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue."` — quote located in the stored
  203 body, tier equal to the `S021` registry cell, no quoted literal hard-coded in the counter.
- Repaired subject tool `tools/gate-records.py` on that line: `GATE_RECORD … S021 FAIL REFETCH`,
  `REPAIRED_TOOL_EXIT=1` (only code `REFETCH`).
- Mutant derived from the subject tool's own bytes (`src.replace('r[6] == "200"', 'r[6].startswith("2")')`,
  `MUTANT_BYTES_DIFFER=True`; the exact string occurs once, at line 238, the admit REFETCH rule):
  `MUTANT_D1_EXIT=0` (`… S021 OK`) and `MUTANT_POSITIVES_EXIT=0` (`GATE_RECORDS files=3 records=15 ok=15 fail=0`).
  So the D1 record is accepted by the relaxed rule and the battery kills it while every positive survives.

C2 independent check (`python3 -B c2indep.py $S`):

- Every `Q` row of both routed entries re-located by normalized containment against the committed capture of the
  registry row's own URL: `INDEP_QUOTES_LOCATED=20/20` (r84 Q1–Q13 all `located=1`, r85 Q1–Q7 all `located=1`).
- `S023` row status `mined`; the DCMI Terms capture (`f5545a194c06ab421875b047`) line **8786** is
  ` Date on which the resource was changed.` — the `modified` Definition cited by r84 `Q13`, matching claims.md.
  (Probe note: my first probe compared the lowercase definition against the raw capture case-sensitively and printed
  `False`; `grep -i` on the same capture finds the line. The capture carries the sentence, the probe's case fold was
  the miss, not the claim.)
- `S024` status `queued`, `S031` status `mined` with `teaches` opening `supersedes S024 —`; the r85 entry's bytes
  contain `S031` and not `S024`; the r84 entry contains neither. No decision-table cell in either routed entry carries
  `modification`/`modified` (independent scan printed no `DECISION-TERM` line), consistent with `UNENTAILED_TERM=0`.

## Risks / notes

- None of the seven pins mismatched and no post-freeze instrument edit exists, so the landing bytes are the bytes the
  freeze pinned.
- Total `355` is a derived count (354 legacy forges + the D1 add), not a hard-coded target; the 2xx control receipt
  `c1-k0-donothing.txt` independently shows `354/355` with `NOT_REFUSED … D1-203-admit S021`, which fixes the legacy
  component at 354.
- Lane HEAD `a9bed303` postdates the landing commit but changes only `.ufo/waves/round-86/` scaffolding; no claim byte
  differs, so the live-root C2 run is landing-equivalent.
- `claims.json` carries `"scoredLanding": null`; that is a freeze-time field, not a C1/C2 predicate field — recorded,
  not counted as a deviation.
- No tool installs or upgrades were needed; nothing was installed or changed on the host.
- Scratch `/fast/scratch/hyaku/chousa-r86/R86ExecRepro` deleted after the receipts above were copied into
  `.ufo/waves/round-86/w1/R86ExecRepro/receipts/`.

VERDICT: R86ExecRepro C1 held — the landing tree reproduces `GATE_RECORDS_R86=PASS` (exit 0) with `D1_REFUSED=1/1` and a mutant genuinely derived from `tools/gate-records.py` bytes.
VERDICT: R86ExecRepro C2 held — the landing tree reproduces `CURATION_R86=PASS` (exit 0) with `QUOTES_LOCATED=20/20`, `MODIFIED_DEF_CITED=1`, and independently re-located quotes from `S023`/`S031`.

# QualityDraft — criterion130 draft (round65, freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd)

Seat: scribe, leaf member (no subagents). Source item: round64 closure before-receipt self-containment
item, captured as `corpus/lessons/round-65.md` `## Mistakes` row 1 ("Before receipt relies on
surrounding provenance instead of self-contained headers"), routed by the round64 outside verifier.
Lane QUALITY.md at the freeze ends at criterion 129, so this drafts **130**.

## Draft criterion130 (QUALITY.md format)

130. **A research receipt offered as evidence of a measured run is self-contained: it declares in-file
the selected revision, the reported child exit and the instrument-blob digest, and a matching header
is judged as consistency only, never as execution authentication.** Round64's before receipt
`corpus/evidence/round64/controls/c1v3-before-full.txt` carries its verdict only through surrounding
provenance (the round64 claims file and lesson): line 1 is `LEG CLEAN clean ok ok` and line 44 the
failed aggregate `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`, with no REVISION/EXIT/
SHA256 header, so no part of the file itself binds it to a revision, an exit code or instrument bytes
(`corpus/lessons/round-65.md` Mistakes row 1; registry row S156 admitted B "for receipt text, not
historical execution authenticity"). Red-before (ran this wave, read-only):
`python3 corpus/evidence/round65/controls/ref-receipt-pin.py --receipt corpus/evidence/round64/controls/c1v3-before-full.txt --root <lane> --revision f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`
→ `RECEIPT_PIN=FAIL header/body`, exit 1 (`QualityDraft/qualitydraft-c130-probe-results.txt` P1).
Positive control, same exhibit's blob digest with `EXIT=1`: `RECEIPT_PIN=PASS`, exit 0 (P2) — a
consistent receipt may report a failed measured command. Boundary control: the byte-identical header
over a fabricated body also passes, exit 0 (P3, fixture `QualityDraft/qualitydraft-c130-fabricated-fixture.txt`)
— header consistency is not output authenticity. Digest tamper and header/caller revision mismatch
fail, exit 1 (P4, P5). Required of every successor receipt: exactly one of each header, in order —
`REVISION=<40 lowercase hex>` equal to the revision the measurement claims, `EXIT=<0..255>` decimal
without leading zeros, `SHA256=<64 lowercase hex> <canonical repo-relative POSIX path>` pinning the
instrument blob at that revision (Git blob, not working bytes), then an empty separator line and a
nonempty body; `corpus/evidence/round65/controls/ref-receipt-pin.py` is the narrow consistency
reference and `python3 corpus/evidence/round65/c1-count.py --work <fresh-dir>` the 20-case acceptance
harness (3 positive incl. `EXIT=1`/`EXIT=255`, 17 negative incl. each missing header), per claims R65-C1.
Limits: no command/body binding, signature, trusted timestamp or process attestation exists, so a
fabricated body under a genuine header passes (P3); blob selection and the caller-supplied revision
are trust assumptions; historical receipts such as S156 are not retrospectively repaired and keep
their original provenance chain; whether the body says anything true remains the outside reviewer's
re-read, not this check. — `corpus/lessons/round-65.md` Mistakes row 1.

## Godspeed axes

1. Draft fidelity — rule sentence, incident, red-before, successor requirement, limits, lesson-row cite.
2. Red-before evidence durability — receipts committed in this seat folder, not scratch-only.
3. Boundary honesty — consistency/authenticity separation demonstrated by receipts, not asserted.
4. Scope hygiene — zero production writes; read-only `git -C`; one clone max (none used).

Moves kept: P2 (`EXIT=1` positive) and P3 (fabricated-body pass) — both sharpen axis 3 at near-zero
cost and harm none. No axis harmed: all probes read-only against the lane.

## Evidence (this wave, ran; artifact sha256)

| file | sha256 |
|---|---|
| `QualityDraft/qualitydraft-c130-probe-results.txt` (P1–P5 transcripts) | `2a5276516011626bfd82ef66875426d91881614a3dc195fb16894ae15ff9e0f5` |
| `QualityDraft/qualitydraft-c130-positive-fixture.txt` (P2 input) | `33583a822781fdec5210e8e6ce701436be2349bf0e5d12e309eacb621d1ffd2c` |
| `QualityDraft/qualitydraft-c130-fabricated-fixture.txt` (P3 input) | `51825270e25b3ede893af4ad03f328ef6511315d319bc13aced819d1bc5a0298` |

Driver: scratch `probe_c130.py` (deleted with scratch after copying; behavior fully described by the
transcript: five subprocess runs of the prefreeze reference validator plus two `git -C … cat-file blob`
digest reads). Explicit `TMPDIR=/fast/scratch/hyaku/chousa-r65/QualityDraft/tmp`. No /tmp evidence.

## Observations (recorded, not acted on)

- Working tree carries uncommitted round65 integration-looking files beyond the freeze: `corpus/QUALITY.md`
  already contains an L1-authored "Round65 addition" criterion 130 at line 939 (freeze copy ends at 129),
  plus untracked `corpus/lessons/round-65.md`, `corpus/knowledge/receipt-identity-r65.md`,
  `corpus/evidence/round65/source-openings.json`, and modified `SCORECARD.md`, `SKILL.md`,
  `corpus/README.md`, `corpus/SOURCES.md`. Consistent with "preliminary uncommitted planning" in the
  frozen claims; this seat treats it as data, drafts independently, and claims no shipping authority.
  My draft and the L1 draft agree on the producing lesson row, the reference validator and the
  consistency-not-authenticity scope; mine states the `EXIT=1`-is-consistent and fabricated-body
  behaviors as run receipts rather than prose only.
- Frozen claims C1 names the target path `tools/receipt-pin.py`; it is absent at the freeze
  (`git ls-tree f99de3b:tools/` has no pin entry). The prefreeze reference lives at
  `corpus/evidence/round65/controls/ref-receipt-pin.py` (S157). C1=PASS therefore requires the L1
  integration to land the target; this seat neither acquires nor writes it.

## Scope

No installs/updates. No network fetches. No git/jj mutations; read-only `git` with explicit `-C`
inside the reference validator only. Wrote only: this folder's three evidence files, `report.md`,
and the sibling `QualityDraft.md` findings file. Scratch deleted after receipt copy.

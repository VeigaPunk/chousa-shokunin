# Attack12 — C1 frozen-case attack: nearby forged/malformed receipts outside `wrong-digest`

Seat: Attack12 (critic, leaf — no subagent dispatch). Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (HEAD at probe time). Base master: `d6ed8155e9b4735639a2cf0a3e479c62f2056195`. Scope: R65-C1 only. Bounded isolated probes in `/fast/scratch/hyaku/chousa-r65/Attack12/` (TMPDIR pinned, read-only `git -C`, no frozen/production writes; scratch deleted after receipts copied here).

## Verdict up front

The frozen counter **does not detect** the strongest nearby bypass. A receipt that binds a *real but wrong* blob digest to the named path (cross-blob swap) is outside all 20 frozen cases, is rejected by the frozen reference validator, yet is **accepted by a weakened-binding validator that still scores `CASES=20/20 C1=PASS`** on the frozen counter. The 20/20 token therefore certifies interface consistency on exactly the 20 frozen receipts — not per-path digest binding. This is a coverage limitation, consistent with the claim's own scope disclaimer; it is not grounds to reject the frozen predicate, but L1 must not treat a bare 20/20 as proof of binding strength.

## Frozen `wrong-digest` branch inspected

`c1-count.py` case 12: `('wrong-digest', v.replace(h, '0'*64), 1)` — correct SKILL.md path, all-zero digest, expects exit 1 with `RECEIPT_PIN=FAIL ` prefix. Reference validator (`controls/ref-receipt-pin.py`, sha256 `0719d717…`) reaches this via one check: `git cat-file blob <rev>:<path>` then `sha256(blob) == claimed`, raising `ValueError('blob/digest')` on mismatch. All digest-mismatch variants collapse into this single branch; the branch itself is sound. sha256 of frozen files recorded in `evidence-frozen-bytes-sha256.txt` (untouched; only read).

## Counterexample (strongest): M1 cross-blob digest swap

Receipt (`M1-cross-blob-swap.txt`): canonical valid receipt for `BASE:SKILL.md`, but the SHA256 field carries the **real digest of `BASE:README.md`**, path still `SKILL.md`. Nearby to `wrong-digest` (same path, same header shape, only the digest string differs) but the digest is a genuine blob digest at the declared revision.

- Byte-equality scan against all 20 frozen receipts: **no match** (table in `evidence-mutations-stage1.json`) → outside the frozen case set.
- Reference validator: exit 1, `RECEIPT_PIN=FAIL blob/digest` → sound.
- Weakened-binding tool (`evidence-cheat-pin.py`, scratch-only): identical CLI and format checks, but digest need only match **some** blob at the revision, not the named one. Result on M1: **exit 0, PASS** (forgery accepted).
- Frozen counter run against the cheat tool: **`CASES=20/20 C1=PASS`, exit 0** (`evidence-counter-vs-cheat.txt`) — identical per-case lines to the reference run (`evidence-counter-vs-ref.txt`, 20/20, matching frozen `controls/c1-positive.txt`).
- No ambiguity defense: at BASE there are no empty files and no duplicate-content blobs (16,845 blobs scanned), so the README-digest-for-SKILL.md binding is an unambiguous misbinding.

Conclusion: the frozen counter cannot distinguish per-path binding from any-blob binding. A target that quietly drops per-path binding passes R65-C1 while attesting false provenance (receipt claims to pin SKILL.md, actually pins README.md). Impacted axis: provenance/identity of receipts; assurance strength of C1 operability scoring.

## Nearby malformed receipts outside the 20 (all rejected by reference; none counter-covered)

Probed against the reference; none byte-equal to any frozen case (evidence JSON):

| Mutation | Ref result | Note |
|---|---|---|
| M2 stale-revision digest (SKILL.md content from `4a11a71`, bound at BASE) | exit 1 FAIL blob/digest | replayed old content; also outside 20 |
| M3 mixed-case digest | exit 1 FAIL digest header | case rule only tested full-upper |
| M4 tree-object digest, path `tools` | exit 1 FAIL blob/digest | non-blob object binding |
| M5 empty-blob digest on SKILL.md | exit 1 FAIL blob/digest | |
| M6 separator line = single space | exit 1 FAIL header/body | |
| M7 `EXIT=00` leading zero | exit 1 FAIL header/body | distinct from overflow/negative |
| M8 tab before path | exit 1 FAIL digest header | |
| M11 UTF-8 BOM | exit 1 FAIL header/body | |

For any of these, a target with a correspondingly weakened branch would pass the frozen counter undetected. Stage-1 note: an earlier stale-digest variant degenerated to the `valid` receipt because tip commit `10e1b84` restores SKILL.md to byte-identical content with BASE (blob `6c1f4b69` at both); corrected M2 uses `4a11a71` (blob `ed9a13f4`, distinct content).

## Spec-ambiguity laxness in the reference (accepted, defensible, untested)

- M9 CRLF line endings: **exit 0 PASS** (universal-newline read translates `\r\n`).
- M10 missing trailing newline: **exit 0 PASS** (no EOF-newline requirement).
The frozen format text specifies ordered headers, empty separator, nonempty output — nothing about line ending or EOF newline — so acceptance is within the letter of the claim. Flag as ambiguity for a future format tightening, not a defect.

## Smallest safe correction

This round (frozen counter must not change): none to the counter. For L1 integration — the acquired `tools/receipt-pin.py` should be verified to bind the digest to the **named** path, ideally byte-identical to the frozen reference or source-reviewed to that effect; a one-off bounded probe of the target with M1/M2 receipts is cheap insurance (both must exit 1). The existing frozen controls (always-pass/always-fail, before/positive) plus this note bound the risk adequately for a 3/10 historical operability axis.

Next round (not this freeze): extend the counter with M1 (cross-blob swap), M2 (stale-revision digest), M3 (mixed-case), M4 (tree digest), M5 (empty digest), M7 (leading-zero exit), and decide CRLF/EOF-newline policy explicitly.

## Housekeeping

- No tool installs needed (python 3.14.8, git 2.56.0 already present); nothing installed or updated.
- Read-only git used with explicit `-C`; no git/jj mutations, no commits/pushes, no network, no fleet/sibling/source-tree writes.
- Frozen bytes untouched (checksums in `evidence-frozen-bytes-sha256.txt`); scratch `/fast/scratch/hyaku/chousa-r65/Attack12/` deleted after evidence copied here.
- Full counter runs: 2 (reference sanity, cheat demonstration); bounded; work dirs under scratch, removed by the counter itself.

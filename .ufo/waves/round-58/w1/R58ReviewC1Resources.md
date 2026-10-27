# R58ReviewC1Resources — C1 input-size and file-kind adversarial review

## Scope and evidence
- Read frozen `corpus/evidence/round58/claims.md` and `c1-count.py`; claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`, freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`.
- At review, `tools/build-spans.py` SHA-256 was `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, equal to the frozen r55 control. The frozen claims and counter hashes were respectively `7aedd8156c9fce185841a740b894600f8a4149b2d8e2034039f634c808373457` and `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
- Scratch only: `/fast/scratch/hyaku/chousa-r58/R58ReviewC1Resources/`. Used copied builder/counter/parser and a copy of the committed S101 capture; no live fetch, lane source edit, git/jj mutation, or install.

## Adversarial probes

### Sparse oversized OLE (.raw)
Used the committed S101 OLE capture as the basis, copied to scratch, then `truncate()`d to 80 MiB: apparent size 83,886,080 bytes, allocated 131,072 bytes, OLE header `d0cf11e0a1b11ae1`. `capture-text.py` on this sparse file returned rc 0 and 27,012 text characters. Built one quote row from that defined text and ran the copied current builder:

```text
rc 0 stderr  stdout QUOTE S551 char 53 spans/S551-1.txt SPANS_ROWS=1 WRITTEN=1  outputs [('spans.tsv', 203), ('S551-1.txt', 373)]
```

The builder accepted the >64 MiB raw input and wrote outputs. `strace -c -e trace=read` confirmed 330 read calls (it did not report aggregate byte count); I do not claim a measured total read volume here. Source inspection explains the path: `tools/build-spans.py:74-84` reads the OLE header, then calls `raw.read_bytes()` before `capture-text`.

The frozen `FAT_RAW` case does **not** catch this valid oversized-file behavior: its fixture at `c1-count.py:282-295` is only OLE magic followed by zeroes, and the base reports `ole-malformed: sector shift 0, mini shift 0`, not `SIZE`. Frozen-counter observed leg: `FAT_RAW=fail(rc=1, reason ['SIZE'] absent in ... ole-malformed ...)`. A valid sparse oversized OLE is a frozen size hazard under claim (4); the frozen fixture under-covers it. The peer size-caps report independently records the same valid-OLE failure mode and a measured read volume; that measurement is not mine.

### FIFO and `/dev/zero` symlink
Ran the frozen counter against the copied base builder using:

```sh
cd /fast/scratch/hyaku/chousa-r58/R58ReviewC1Resources
env TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewC1Resources python3 -B c1-count.py --builder /fast/scratch/hyaku/chousa-r58/R58ReviewC1Resources/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58ReviewC1Resources/frozen-counter
```

Relevant exact results:

```text
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
```

These specific `.txt` hazards were refused promptly (no timeout/hang), because `Path.is_file()` is false for FIFO/device targets. However, the counter marks both legs failed because their refusal reason classes are not named. Thus the counter does not record a pass for either. A symlink to a regular file is followed by `is_file()`/`read_bytes()`; `SYMLINK_CACHE` likewise fails on the base (`rc=0`, accepted). Frozen tests cover the cache `.txt` FIFO and `/dev/zero` symlink, not FIFO/device variants on `.raw` or `quotes.tsv`.

### Regular `.txt` above 64 MiB
Created a regular cache `.txt` of 68,157,441 bytes with one unique quote and ran the copied builder. Exact observed result:

```text
input bytes 68157441 rc 0 seconds 0.12 stderr  stdout QUOTE S552 char 34078720 spans/S552-1.txt
SPANS_ROWS=1 WRITTEN=1 out files [('spans.tsv', 214), ('S552-1.txt', 182)]
```

This is explicitly outside the frozen promise: claims.md says “text-size caps and broader races are not claimed.” The `.txt` path is unbounded (`build-spans.py:85-88`), but this result is **not** a C1 violation or a justified reason to widen the claim. No text-size cap is asserted.

## Frozen counter outcome and overclaim
The full counter run above ended `C1=FAIL` (exit 1); it also observed `SYMLINK_CACHE` accepted, `MANY_QUOTES` accepted, and other base failures. More importantly, its per-leg refusal labels are lowercase `pass`, while aggregation at `c1-count.py:391` tests for `"=PASS"`; therefore its refusal aggregate is always false and the frozen `C1=PASS` target is unreachable. This is an observed source-level defect (also detailed in the size-caps report), not evidence that an otherwise-good size guard would fail.

`expect_refuse` at `c1-count.py:150-160` checks rc/reason, and the FIFO, `/dev/zero`, `FAT_RAW`, and `MANY_QUOTES` callers supply empty `forbidden_touch` lists. They therefore do not check for partial output writes on those legs, despite the broad claim wording “without partial writes.” Do not interpret a leg label alone as proof of zero mutation. In this run, the sparse-raw probe independently showed actual output on accepted input.

## Findings / residual risk
- **Frozen hazard, not caught:** valid sparse 80 MiB OLE raw; accepted by base and not represented by the malformed-OLE counter fixture. The claimed 64 MiB raw-read bound is absent in the reviewed base.
- **Frozen hazards, promptly refused but not counted as passing:** cache `.txt` FIFO and symlink-to-`/dev/zero`; counter's reason-class assertions reject their generic “no defined text form” refusal. No hang was observed for these exact fixtures.
- **Uncovered variants:** `.raw` FIFO/device and `quotes.tsv` FIFO are outside those specific legs; no result claimed for an alternate builder implementation on these paths.
- **Not a frozen hazard:** regular `.txt` >64 MiB; the claims expressly disclaim text-size caps. Its acceptance is not an overclaim by the claim author.
- No claim that counters were rerun against an in-flight hardened builder. No verification gate run.

VERDICT: The valid sparse >64 MiB OLE hazard survives: the reviewed base accepts it and the frozen malformed-OLE FAT_RAW leg does not detect that behavior. FIFO and `/dev/zero` `.txt` fixtures refuse promptly on base but their frozen counter legs report FAIL due to reason-label mismatch; counter C1=PASS is unreachable by its case-mismatched aggregation. The >64 MiB regular `.txt` is outside claim scope, not an overclaim.

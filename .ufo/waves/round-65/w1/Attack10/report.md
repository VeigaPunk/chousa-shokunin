# Attack10 — C1 word-exit axis attack (round65, freeze f99de3bdfaaf)

Seat: Attack10 (critic, leaf). Date: 2026-10-30. Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (HEAD = freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`, verified read-only). Base `d6ed8155e9b4735639a2cf0a3e479c62f2056195` blob `SKILL.md` verified present. No frozen bytes altered; git used read-only with explicit `-C` (cat-file only); all writes in scratch, deleted on exit. Target `tools/receipt-pin.py` is absent (before-control state); reference = `corpus/evidence/round65/controls/ref-receipt-pin.py`. Probes: python 3.14.8, bounded, isolated.

## Assigned question

Does the frozen counter (`c1-count.py`) detect a nearby forged/malformed receipt bypass constructed outside the single frozen `word-exit` case?

**Answer: No — demonstrated, not inferred.** Two distinct bypasses land; neither is visible to the frozen counter.

## Counter branch (frozen, unmodified)

`c1-count.py` case 10: `('word-exit', v.replace('EXIT=0','EXIT=PASS'), 1)`. `v` contains `EXIT=0` exactly once (header), so the case is exactly one token: `EXIT=PASS` must yield exit 1 and stdout starting `RECEIPT_PIN=FAIL `. Pass condition per case: `q.returncode==rc and (rc==0 → stdout.strip()=='RECEIPT_PIN=PASS') and (rc≠0 → stdout.startswith('RECEIPT_PIN=FAIL '))`. Coverage of the malformed-EXIT axis is this single point.

Reference `ref-receipt-pin.py` rejects a word exit via `re.fullmatch(r'EXIT=(?:0|[1-9][0-9]{0,2})', lines[1])` plus `int(lines[1][5:])>255`.

## Finding 1 — pointwise word-exit: lookup-table target scores 20/20 while accepting forged EXIT receipts (counter does NOT detect)

- Battery A (22 malformed EXIT variants vs reference): `PASS, pass, Pass, OK, true, N/A, none, <empty>, 0x0, +1, ' 0', 1.0, 1e0, ٠ (U+0665), 00, 01, 099, '0 ', ' 0 ', '0<TAB>', ==0, EXIT=0\nEXIT=0` — reference returns exit 1 `RECEIPT_PIN=FAIL header/body` on all 22. The reference itself has no EXIT-axis acceptance hole.
- Battery B1: a lookup-table target (`evidence-attack10-lookup-stub.py`: exact answers for the 20 frozen case texts, `PASS`/exit 0 for everything else) run under the frozen counter scored `CASES=20/20 C1=PASS`, counter exit 0 (one bounded run, ~1.4 s).
- Battery B2: the same stub accepts forged receipts `EXIT=OK`, `EXIT=0x0`, `EXIT=00`, `EXIT=N/A` (all exit 0 `RECEIPT_PIN=PASS`) while the reference rejects each (exit 1). Receipts preserved as `evidence-attack10-B-forged-*.receipt`.

Consequence: any target that special-cases the 20 frozen inputs — in particular rejecting exactly `EXIT=PASS` while accepting every other malformed EXIT token — is indistinguishable from a correct validator under `R65-C1`. The word-exit case names a class (non-numeric EXIT) but samples it with one token; nothing in the counter closes the gap. This generalizes to all 20 cases (finite pointwise list).

Classification: **disclaimed tradeoff, not a fixable in-round defect.** `claims.md` already scopes C1: "interface/consistency coverage, not a claim to cryptographic execution authentication or general parser safety." Under the frozen predicate ("CASES=20/20 iff all frozen receipt-consistency cases match their exact exit and token") the lookup-table target truthfully passes. The freeze rule forbids counter/predicate/denominator edits in-round. Smallest safe correction: none to frozen artifacts; the canonical judge should score C1 as pointwise interface consistency only. If class-coverage of "word-exit" is intended, it is a next-freeze decision (add tokens such as `EXIT=OK`, changing the frozen denominator), not an in-round patch.

## Finding 2 — reference accepts malformed-container receipts (fixable reference defect; frozen counter also blind to it)

Mechanism: reference does `text=pathlib.Path(a.receipt).read_text(encoding='utf-8')` (universal newlines translate `\r\n`/`\r` → `\n`) then `lines=text.splitlines()` (splits on `\x0b \x0c \x1c-\x1e \x85 \u2028 \u2029` as well). A receipt whose header lines are separated by form-feed, vertical-tab, U+2028, or U+2029 parses as valid headers with an empty separator and passes; CRLF/CR pass after translation.

Battery A2 evidence (reference, `--revision d6ed8155…`, real digest of real blob — no provenance forgery, malformed container only): `crlf, cr, formfeed(\x0c), vtab(\x0b), uni-lsep(U+2028), uni-psep(U+2029)` all return exit 0 `RECEIPT_PIN=PASS`. Receipts preserved as `evidence-attack10-A2-*.receipt`. The frozen 20 cases contain no alternate-separator case, so a target matching the reference exactly inherits the leniency with no counter signal — and a stricter target also scores 20/20, so the counter cannot distinguish the two behaviors.

Smallest safe correction (candidate included, `evidence-attack10-strict-lines-pin.py`): read with `newline=''` and split on `'\n'` only. Verified bounded: PASS/exit 0 on the three canonical valid inputs (`valid`, `nonzero-valid`, `max-exit`); FAIL/exit 1 on all six exotic receipts. This stays consistent with every frozen case (all use plain `\n`) while rejecting the malformed containers. CRLF tolerance is a judgment call — note peer Attack02 already tracks a CRLF probe (`Attack02/evidence/F2-crlf.txt`), so coordinate to avoid double-counting; `\x0b/\x0c/\u2028/\u2029` acceptance is the unambiguous defect.

## Impact

- C1 (operability, historical 3/10): both findings are coverage/behavior gaps outside the 20 frozen points. No frozen case result is contested; the counter's own arithmetic and branch construction are sound.
- C2: unaffected (independent structural sourced-entry counter).

## Reproduction

`evidence-attack10-wordexit-probe.py` (driver), `evidence-attack10-results.json` (full structured results), stub and strict variant as named above. Receipts byte-preserved. One full-counter run total (B1, against the scratch stub only); all other probes were single-invocation isolated runs against the reference or scratch validators.

## Hygiene

Scratch `/fast/scratch/hyaku/chousa-r65/Attack10/` deleted after evidence copy. No installs needed (python 3.14.8 system). No git/jj mutations, no production writes; seat wrote only this report and `evidence-attack10-*` files under `.ufo/waves/round-65/w1/Attack10/`.

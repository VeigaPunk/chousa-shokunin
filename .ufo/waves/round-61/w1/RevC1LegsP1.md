# RevC1LegsP1 — reviewer, round 61 w1, legs P01 TXT / P02 DOCX / P03 NOPYC

Scope: `corpus/evidence/round61/c1-count.py` (sha256 f1d8b6fd…, matches frozen A1 entry) against predicate R61-C1 in `claims.md`. Counter, reference (`controls/ref-build-spans.py`, sha 86d64c31…, matches claims) and controls read and not edited. Candidate builders were scratch copies of the reference, run with `python3 -B <counter> --builder <b> --work <absent dir> --seed N`. Scratch removed before yield.

## Findings (in-scope legs)

### F1 — P02 DOCX: fixture cannot tell a first-run-only docx reader from the defined form (counter defect, false positive)
- Counter: `add_docx_capture` (c1-count.py:182-194) writes one paragraph = one `w:r` = one `w:t`. Golden (c1-count.py:216-228) expects each `w:p`'s full text.
- Incorrect builder `bad5`: reference with `_ct_form` (ref lines 134-137) replaced by a reader that keeps only the first `<w:t>` of each `<w:p>`.
- `python3 -B c1-count.py --builder bad5 --seed 61001` → `LEG P02 DOCX pass rc=0`, `LEGS=20/20 C1=PASS`. Same at 61002, 61003.
- Demo (scratch, not counter): docx paragraph of two runs `first run alpha ` + `second run beta gamma`, quote `beta gamma`. Reference: form `first run alpha second run beta gamma`, rc 0, span written. bad5: `quote occurs 0x … 'beta gamma'`, rc 1. So bad5 fails on any multi-run paragraph, a shape the leg never presents.

### F2 — P01 TXT: no fixture quote falls inside the start-of-form clamp (counter defect, false positive)
- Golden clamp: c1-count.py:224 `start = max(0, off - CONTEXT)`. Fixtures: `txt_source` (c1-count.py:163-173) puts at least 14 words before the first quote.
- Probe (scratch; imports the counter's own `Fx`, 400 seeds, `two_url_rows` for txt and docx): 1200 txt quotes, min offset 115, 0 below 80; 1200 docx quotes, min 97, 0 below 80. Command output: `txt offsets: n=1200 min=115 count<80=0` / `docx offsets: n=1200 min=97 count<80=0`.
- Incorrect builder `bad4`: reference line 202 `start = max(0, off - CONTEXT)` → `start = off - CONTEXT`.
- `--seed 61001|61002|61003` → `LEG P01 TXT pass rc=0`, `LEGS=20/20 C1=PASS` each.
- Demo, quote at form offset 0: reference manifest `offset 0`, span `UNIQUEQUOTE alpha beta gamma tail words here…`; bad4 manifest `offset -80`, span file empty, rc 0. A quote near document start is realistic and P01 cannot see it.

### F3 — P03 NOPYC: listing-only check misses a rewritten sibling tool (counter defect, false positive)
- `tools_unchanged` (c1-count.py:274-275) compares `sorted(p.name …)` only; used at line 304. Hazard as stated in the docstring (line 14) is writes into `tools/`, not only `__pycache__`.
- Incorrect builder `bad2`: reference plus, in `main()` after `read_quotes`, `tool = TOOLS/"capture-text.py"; tool.write_bytes(tool.read_bytes() + b"\n# touched by build\n")`.
- `--seed 61001|61002|61003` → `LEG P03 NOPYC pass tools=['build-spans.py', 'capture-text.py']`, `LEGS=20/20 C1=PASS` each.
- Demo: after bad2 the tool's bytes differ from the lane copy (`capture-text.py bytes changed: True`). Caveat: my driver's own listing comparison printed `False` because it copied build-spans.py into the fixture before snapshotting; the counter snapshots after its own copy (c1-count.py:137-139), so that artifact does not apply to the counter.

## Correct builders (false-negative probe, P01/P02/P03 and all 20 legs)
- `cb1`: link guard moved before any capture read (new `guard_links`, called in `main()` before `build`); capture-file refusals exit 2 instead of 1 (ref line 213 changed). Refuse-policy.
- `cb2`: replace-policy for links: symlinked `spans`, `spans.tsv` or span files are unlinked, never followed, then written fresh (`guard_out`/`write_out` rewritten).
- `cb3`: reference refuse-policy, reads via `os.open(…, O_NOFOLLOW)` (line 143), oversize refusals exit 3 (line 215).
- Results (counter, exit 0): `cb1` 20/20 at 61001/61002/61003; `cb2` 20/20 at 61001/61002/61003; `cb3` 20/20 at 61001/61002/61003. Each P01/P02/P03 line `pass`.
- Sanity: reference 20/20 at seed 61001 (`bg_20950`, exit 0, 2.1 s).
- False negatives on P01/P02/P03: 0.

## Observed outside my legs (not counted; route to the P04 and H19 reviewers)
- `bad1` (P04): `check()` compares length only (ref line 234 replaced). Counter P04 mutation (c1-count.py:315) appends `b"x"` (a length change), while docstring line 15 says "one span byte is changed". Counter 20/20 at 3 seeds. Demo: same-length byte change → bad1 `--check` rc 0 `SPANS_ROWS=1 STALE=0`; reference rc 1 `SPANS_FILE_STALE spans/S101-1.txt`.
- `bad3` (H19): entry check reduced to `startswith("../")` (ref line 176 replaced). Counter H19 mutation (c1-count.py:537) only tests `../<hex>`. Counter 20/20 at 3 seeds. Demo: entry `corpus/../../x` → bad3 rc 0; reference rc 2 `must be lane-relative`.
- NOT RUN (INFERENCE from code): H10–H12 (c1-count.py:414, 431, 447) accept any tree when rc≠0 and the victim is unchanged, so a builder that writes spans into `out` and then refuses on a link would pass. Not executed.

## Integrity
- Counter, reference and claims hashes checked against claims.md; nothing under corpus/, tools/, SKILL.md or round61/ edited.
- Installs: none. Python 3.14.8 present; no packages added. Uid 1000, so H17 ran (not skipped).
- Counter runs: 3 seeds × 6 candidates + 3 × 2 later candidates + reference; each `python3 -B`, ~2–3 s per run.

## Recommendation (for L1; no edit made)
Add to P01/P02 fixtures: a quote at form offset < 80, and a paragraph with two runs. Add to P03: a byte-compare of `tools/` files against the copies made at fixture creation, not just names.

VERDICT: LEG_DEFECTS=3 false_negative=0 false_positive=3 legs=P01 TXT, P02 DOCX, P03 NOPYC

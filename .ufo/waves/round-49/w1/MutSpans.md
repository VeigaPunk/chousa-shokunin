# MutSpans — r49 w1 mutation probe: build-spans + C2 CAPTURE_BOUND leg

Seat: MutSpans (leaf, no subagents). Probe ran 2026-10-25 in scratch
`/tmp/chousa-r49-MutSpans/` (deleted at end; only lane write = this file).
Battery: pristine → mutate → `c2-count.py --root` (+ builder `--check`) →
restore → hash-verify. No tool installs (pacman paused; none needed).

## Fixture

Scratch root = copies of the REAL lane files c2-count reads: `corpus/SOURCES.md`,
both `corpus/knowledge/` entries, `corpus/lessons/round-49.md`,
`corpus/evidence/round49/{quotes.tsv,spans.tsv,spans/,build-spans.py}`,
`tools/inference-ground.py`. Captures read-only from the qcache. A first,
synthetic fixture (2 theme ids: S096 nii `.txt`-form, S102 hit `.doc` `.raw`
UTF-16LE; 4 quote rows) was built before the real build landed — see finding F0.

## Baseline (real state, builder 02b2dc83)

`python3 <lane>/c2-count.py --root /tmp/chousa-r49-MutSpans/root` →
`BOUND=8/9 REFUSED=1 QUOTE_ROWS=28 ON_BOUND=28/28 SPAN_IDS=8/8
QUOTES_IN_SPAN=28/28 QUOTES_IN_ENTRY=28/28 QUOTES_IN_LESSON=28/28
QUOTE_SHORT=28/28 SPAN_CONTEXT=28/28 CAPTURE_BOUND=28/28 ANCHOR_BOUND=8/8
INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=5/5 BLOCKED=0 C2=PASS` exit 0.
Builder `--check`: `SPANS_ROWS=28 STALE=0` exit 0. Maximal-signal baseline.
Note: landed lane ids are S096–S103 (ncpssd refused), one off renumber.tsv's
S096–S104 — cosmetic for c2-count (binding is by URL), noted for the ledger.

## F0 — pre-repair builder failed CAPTURE_BOUND on pristine bytes (fixed mid-probe by sibling)

On the synthetic fixture with builder `fed672dd` (pre-repair), baseline gave
`CAPTURE_BOUND=2/4` — both `.raw`-form rows failed on PRISTINE bytes. Diagnosis
(slice idx 74: form_text `'\r'` vs span-file `'\n'`): the UTF-16LE decode keeps
CRLF; `build-spans.py:185` `write_text` (default newline) preserves `\r`, but
`c2-count.py:168` reads span files with universal newlines (`\r\n`→`\n`) while
`c2-count.py:108` `form_text` re-decodes untranslated — any `\r` in a `.raw`
span slice can never satisfy the exact-slice check. `.txt` form immune (both
sides normalize). Builder's own `--check` was also born stale on such output.
Mid-probe a sibling landed the repair (lane `build-spans.py` `fed672dd`→
`02b2dc83`, `git status` shows ` M`): `.raw` context clipped at the nearest CR
each side, comment cites "claims-erratum.md" — that file does NOT exist in the
lane yet (only `round48/controls/before-erratum.txt` matches `*erratum*`);
disclosure still pending. After the repair: baseline `CAPTURE_BOUND=28/28`,
`C2=PASS`. The landed S101 rows record offset 11166 twice — legitimate: both
quotes sit after the same CR at 11165, so both clipped starts coincide;
anchors (char 11189/…) still resolve via `offset + span.find(quote)`.

## Mutant battery (real state, builder 02b2dc83; one row/file each)

(a) **form forced to `.txt` only** (raw leg removed from scratch builder copy):
build refuses all 8 `.doc` rows (`...txt:0x`), exit 1, writes nothing.
- cleaned state → `QUOTE_ROWS=0 SPAN_IDS=0/8 QUOTES_IN_SPAN=0/0
  CAPTURE_BOUND=0/0 C2=FAIL` — caught, but by manifest absence; the named span
  legs are vacuous 0/0.
- stale pristine manifest → build exit 1, nothing overwritten → c2-count
  unchanged: `QUOTE_ROWS=28 ... CAPTURE_BOUND=28/28 C2=PASS` exit 0 —
  **SURVIVOR of c2-count alone**; killed only at the builder boundary
  (`--check` also just refuses, exit 1). Coverage finding: the counter is
  blind to a refused build; it trusts build-spans having run clean.
(b) **offset +1** (S096-1 `3519→3520`): `CAPTURE_BOUND=27/28`,
`ANCHOR_BOUND=7/8` (anchor char 3599 lost), `QUOTES_IN_SPAN=28/28`;
`--check`: `SPANS_ROW_STALE spans/S096-1.txt STALE=1`. KILLED.
(c) **digest of the wrong form** (S096-1 digest → nii `.raw` digest
`5ce63212…`): `CAPTURE_BOUND=27/28`, `ANCHOR_BOUND=8/8`,
`QUOTES_IN_SPAN=28/28`; `--check` `SPANS_ROW_STALE`. KILLED by
CAPTURE_BOUND alone — form_text falls through to the `.raw` decode and the
`.txt`-derived slice mismatches.
(d1) **span file edited by one char inside the quote** (S096-2, char 81):
`QUOTES_IN_SPAN=27/28` + `CAPTURE_BOUND=27/28` + `ANCHOR_BOUND=7/8`;
`--check` `SPANS_FILE_STALE`. KILLED by three legs.
(d2) **span file edited by one char in context only** (S096-1, char 0):
`QUOTES_IN_SPAN=28/28` (blind) but `CAPTURE_BOUND=27/28`; `--check`
`SPANS_FILE_STALE`. KILLED **only by CAPTURE_BOUND** — confirms the tasking's
expectation: QUOTES_IN_SPAN alone cannot see context tampering.

## Restoration evidence

- After each mutant: `rm -rf root && cp -a root.pristine root`; final
  `sha256sum -c pristine.sha` → `restored_non_OK=0` (13/13 files byte-exact).
- Restored rerun: `CAPTURE_BOUND=28/28 QUOTES_IN_SPAN=28/28 C2=PASS` exit 0.
- Lane integrity (probe never wrote lane): `build-spans.py 02b2dc83de1f4971`
  (sibling's post-repair state; was `fed672dd…` at probe start — change is the
  sibling's, my edits hit scratch copies only), `c2-count.py 9d2fb3806e368a34`
  and `inference-ground.py fa2b4eb5fc29b4dd` unchanged from first snapshot.
- Scratch `rm -rf /tmp/chousa-r49-MutSpans` → `SCRATCH_DELETED` (exact path,
  no globs; peer F35MutReceipt's unrelated /tmp/k35f-* loss was not mine).

## Takeaways for the lane

1. CAPTURE_BOUND is the strongest span leg: sole catcher of (c) and (d2);
   QUOTES_IN_SPAN is necessary but not sufficient.
2. c2-count cannot catch a builder that refuses (mutant a survivor shape) —
   the build step's exit code is the guard; keep builder exit 1 in the kill
   chain, and land the pending `claims-erratum.md` disclosure for 02b2dc83.
3. `.raw` spans are CR-fragile by construction; the repair's CR-clipping is
   what makes the frozen counter satisfiable — quote choice for `.doc`
   captures must keep quotes CR-free (clipping handles context).

VERDICT: attacked the r49 span builder + C2 CAPTURE_BOUND leg with 5 mutants
(a–d2) on a C2=PASS real-state baseline — (b)(c)(d1)(d2) killed (CAPTURE_BOUND
sole catcher of c/d2), (a) survives c2-count over a stale manifest and is
killed only at the builder boundary; plus pre-repair finding F0 (CRLF
asymmetry failed CAPTURE_BOUND on pristine bytes, repaired mid-probe by
sibling, erratum disclosure still missing) — all bytes restored hash-exact.

# MutC1ExtraDoc — mutation test of the C1 reference builder (round 61, w1)

Seat: MutC1ExtraDoc (mutation-tester, leaf). Target: `corpus/evidence/round61/controls/ref-build-spans.py`
(sha256 `86d64c31…eccfd`, unchanged). Counter: frozen `corpus/evidence/round61/c1-count.py` (not edited).
Scratch `/fast/scratch/hyaku/chousa-r61/MutC1ExtraDoc/` (deleted before yield). No lane, fleet or git writes.

## Findings

- Reference scores 20/20 at seed 61001 (`LEGS=20/20 C1=PASS`, exit 0) and at seed 61002. Baseline run 1.2 s.
- 24 mutants, each violating one behaviour sentence of the reference docstring (exit-code list, 64 MiB caps,
  `.txt` decode and universal newlines, `.raw`/`.txt` precedence, quote uniqueness, span formula, `--check`,
  `--replace` and identical-rebuild rules, file-tree ordering). Counter at seed 61001: **KILLED 8, SURVIVED 16**.
- The 16 survivors: 1 equivalent for the sentence (X17), 14 coverage gaps, 1 design-limited (X24: only the
  stdout `QUOTE` line changes, which QUALITY 117 forbids the counter to read).
- Each non-equivalent survivor has a smallest fixture, run with `harness.py` (reference vs mutant on identical
  bytes). Every one differs in exit code or file tree; X24 differs in stdout only.
- Reading: the 20 legs measure output safety. They do not pin the docstring's cap boundaries, decoding and
  newline rules, span formula, quote uniqueness, or the exit codes for usage/env. Several survivors (X04, X10,
  X11, X14, X15) are functional rather than safety faults; the C1 predicate does not claim them.

## Table (counter, seed 61001; `KILLED` = legs-failed ≠ ∅ with rc or tree change)

| # | mutant (file) | edit (docstring sentence it falsifies) | legs failed | verdict |
|---|---|---|---|---|
| X01 | cap-double | `size > 2*MAX_CAPTURE` ("size at most 64 MiB") | - (20/20) | SURVIVED, gap |
| X02 | cap-edge | `size >= MAX_CAPTURE` ("at most 64 MiB") | - | SURVIVED, gap |
| X03 | form-cap-double | `len(form) > 2*MAX_FORM` ("over 64 MiB chars refused") | H20 | KILLED |
| X04 | txt-strict | `decode(..., errors="strict")` ("UTF-8 (errors replaced)") | - | SURVIVED, gap |
| X05 | txt-no-lone-CR | drop `.replace("\r","\n")` ("universal newlines") | - | SURVIVED, gap |
| X06 | txt-keep-CRLF | drop `.replace("\r\n","\n")` ("universal newlines") | P01 P06 H08 | KILLED |
| X07 | digest-of-form | `sha256(form)` not `sha256(file)` ("digest of the FILE read") | P01 P02 P06 H08 | KILLED |
| X08 | raw-refused-falls-back | raw capture-text refusal uses `.txt` ("a raw refusal is a refused row") | - | SURVIVED, gap |
| X09 | txt-preferred | `.txt` used when `.raw` is OLE/zip ("`.txt` never used for such a capture") | - | SURVIVED, gap |
| X10 | quote-multi | `if n < 1` ("quote must occur exactly once, else refused") | - | SURVIVED, gap |
| X11 | span-no-clamp | `start = off - CONTEXT` ("span = form[max(0,off-80):...]") | - | SURVIVED, gap |
| X12 | span-end-1 | `off+len(quote)+CONTEXT-1` (span formula) | P01 P02 P06 H08 | KILLED |
| X13 | check-repairs | `--check` also calls `write_out` ("--check ... writing nothing") | - | SURVIVED, gap |
| X14 | header-exit-1 | bad input header exits 1 (exit list: 2 = usage/env) | - | SURVIVED, gap |
| X15 | cache-missing-exit-1 | missing `--cache` exits 1 (exit list: 2 = usage/env) | - | SURVIVED, gap |
| X16 | refuse-no-abort | refusal does not `sys.exit(1)` ("any refusal writes nothing and exits 1") | P05 H13 H14 H15 H17 H18 H20 | KILLED |
| X17 | spans-guard-weak | drop `or not sd.is_dir()` ("spans is a symlink or not the expected kind") | - | SURVIVED, equivalent (see below) |
| X18 | tsv-guard-weak | drop `or not m.is_file()` ("spans.tsv ... not the expected kind") | - | SURVIVED, gap |
| X19 | orphans-first | unlink orphans before writes ("orphan span files removed last") | - | SURVIVED, gap |
| X20 | manifest-first | write `spans.tsv` before span files ("span files first, then spans.tsv") | - | SURVIVED, gap |
| X21 | identical-refused | `differs = m.is_file()` ("an identical rebuild is always allowed") | P06 | KILLED |
| X22 | orphan-ignores-replace | `(differs and not replace) or orphans` ("unless --replace") | H08 | KILLED |
| X23 | check-exit-0 | `--check` always returns 0 ("exit 1 ... STALE>0") | P04 | KILLED |
| X24 | quote-char-off-by-one | stdout `char {c+1}` ("prints QUOTE ... char N") | - | SURVIVED, design-limited |

Killed 8/24: X03, X06, X07, X12, X16, X21, X22, X23. Stability: X06 killed at seeds 61001 (P01 P06 H08),
61002 (P01 P02 P06), 61003 (P06 H08) and 61004 (P01 P06 H08).

## Survivors: class and smallest fixture (harness.py; reference vs mutant, same bytes)

Commands: `python3 -B harness.py mut/<X>.py <fixture>`. Output in scratch `out/h-<X>.txt`.

- **X01 cap-double — gap.** ASCII `.txt` of 64 MiB+1 bytes is `SAME` (MAX_FORM refuses it too, 67108865 chars),
  so the ASCII case is masked. Multibyte fixture kills it: `.txt` of 64 MiB+1 bytes of 3-byte UTF-8 (about
  22 M chars, under MAX_FORM). Reference: rc=1 "is 67108878 bytes, over the 67108864-byte capture cap";
  mutant: rc=0. Counter has only H14/H15 at 192 MiB, which do not pin the 64 MiB edge.
- **X02 cap `>=` — gap.** Exactly `64<<20` bytes `.txt` with the quote: reference rc=0, mutant rc=1.
- **X04 strict decode — gap.** `.txt` with byte `0xff` outside the quote: reference rc=0 (U+FFFD in span),
  mutant rc=1 ("'utf-8' codec can't decode byte 0xff").
- **X05 no lone-CR fold — gap.** `.txt` = `aaa bbb\rccc <Q>\rddd eee`: rc=0 both, tree differs (span holds `\r`).
  Counter never generates a lone CR: `txt_source` joins with `"\r\n"` or `"\n"` only (c1-count.py L163-173);
  X05 PASSES at seeds 61001-61003.
- **X08 raw-refusal falls back to `.txt` — gap.** `.raw` = `PK\x03\x04`+garbage, `.txt` sidecar containing the
  quote: reference rc=1 ("neither a zip package nor an OLE compound file"), mutant rc=0. No counter leg has a
  refused `.raw` with a sidecar.
- **X09 `.txt` preferred over `.raw` — gap.** Valid docx `.raw` containing the quote plus a `.txt` sidecar
  containing it: rc=0 both, tree differs (`capture_sha256` becomes the sidecar's). Counter never has both files.
- **X10 quote may repeat — gap.** `.txt` with the quote twice: reference rc=1 ("quote occurs 2x"), mutant rc=0.
- **X11 span start unclamped — gap.** Quote at form offset 0, `.txt` = `<Q> ` + 300 `x`: rc=0 both, span file
  differs (mutant writes wrong slice). Counter quotes always sit past offset 80 (paragraphs of 14-24 words first).
- **X13 `--check` repairs — gap.** Reference build, one stale span byte, `--check`: reference rc=1 and tree
  unchanged; mutant rc=1 and tree healed. P04 reads only exit codes.
- **X14 bad header exits 1 — gap.** `q.tsv` header `id url quote`: reference rc=2, mutant rc=1. H19 covers only
  a bad row, not the header branch.
- **X15 missing cache exits 1 — gap.** `--cache` nonexistent: reference rc=2, mutant rc=1. No leg uses a bad cache.
- **X17 spans-as-file guard weak — EQUIVALENT (observables).** `out/spans` a regular file: both rc=2, tree equal.
  Stderr differs ("refused output: ... not a directory" vs "write failed ... File exists"), but the sentence
  ("refuses, exit 2 and nothing written") holds for both.
- **X18 spans.tsv-as-directory guard weak — gap.** `out/spans.tsv` an empty dir: both rc=2; mutant writes
  `spans/` before failing on `os.replace` (tree differs, "Is a directory").
- **X19 orphans removed first — gap.** `out` mode 555, orphan `spans/S404-9.txt`, `--replace`: both rc=2
  (`Permission denied` on `spans.tsv`); reference keeps the orphan, mutant has deleted it. Needs non-root (uid 1000).
- **X20 manifest first — gap.** `out/spans` mode 555: both rc=2; mutant leaves `out/spans.tsv` behind,
  reference leaves nothing. Needs non-root.
- **X24 QUOTE offset off by one — design-limited.** stdout `char 12` (reference) vs `char 13` (mutant); rc and
  tree equal. Exit code and tree are the counter's only observables (QUALITY 117), so this cannot be closed
  without reading output. Routed as a counter limit, not a C1 refutation.

## Counter-check of the same mutants (no harness)

Reference alone: `python3 -B c1-count.py --builder controls/ref-build-spans.py --work w/ref --seed 61001`
→ `LEGS=20/20 C1=PASS`. Reference at 61002 → `LEGS=20/20 C1=PASS`. Each mutant: `--work w/<X> --seed 61001`;
legs failed as in the table; output in `out/<X>.txt` (scratch).

## Installs

None. Python 3 stdlib only.

## Limits of this probe

- Single-edit mutants only; no combinations. Each survivor's "smallest fixture" is smallest among those I tried,
  not proven minimal.
- X19 and X20 need a non-root user to be a real permission fault (ran as uid 1000).
- Harness compares exit code and tree, the counter's observables. Stderr text was recorded, not judged.
- Counter edits are out of scope (frozen). Route survivors to L1 as counter limits; the closure decides the
  calibration statement, not this seat.

VERDICT: KILLED=8/24 survivors_that_are_gaps=15

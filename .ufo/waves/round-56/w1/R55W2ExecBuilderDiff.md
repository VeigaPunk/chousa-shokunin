# R55W2ExecBuilderDiff — candidate `tools/build-spans.py` vs the round-54 builder

Seat R55W2ExecBuilderDiff (leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at
`46e1758f3d8a5d1bf30200d2ff7d909b0230feed`; round-54 builder `corpus/evidence/round54/build-spans.py`
(sha256 `e8337aba1ad8859c467a519df9b47ed0010937d9e68e12214c893d71e279b030`), candidate `tools/build-spans.py`
(`1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`), its form reader
`tools/capture-text.py` (`2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`). No network: every
capture is an on-disk `.qcache` file copied to `$S/cache/<key>.raw|.txt`, key = `sha256(url)[:24]` of my own
`example.invalid` URL, so each fixture pins its own capture bytes. Scratch `/fast/scratch/hyaku/chousa-r56/R55W2ExecBuilderDiff`;
the round-54 builder runs from a scratch lane copy `$S/lane54` (`git archive 46e1758 | tar -x`) with its own
`corpus/evidence/round54/quotes.tsv`; no lane file was edited. `PYTHONDONTWRITEBYTECODE=1` for every run.

## The diff

    $ diff corpus/evidence/round54/build-spans.py tools/build-spans.py > builder.diff; echo rc=$?
    rc=1                       # 5 hunks, 318 diff lines, 268 -> 217 source lines

## Behavioural differences, each with a fixture (commands in `$S/final-table.py`, output `$S/final-table.txt`)

1. **Form precedence for OLE/zip captures** (`build-spans.py:77-84` vs round-54 `form_texts:116`/`pick:170`).
   Candidate: when `.raw` is OLE (`D0CF11E0A1B11AE1`) or zip (`PK\x03\x04`) the form is
   `capture-text.text_form(raw)` and **the `.txt` sidecar is never read**; round-54 prefers the `.txt` whenever
   the quote occurs there exactly once.
2. **OLE `.raw` form**: round-54 `raw_form:107` decoded the whole file as UTF-16LE; candidate reads the OLE
   main-document story via `capture-text`.
3. **Zip `.raw` form**: round-54 carried its own `docx_text`; candidate calls `capture-text`. The two renderers are
   *byte-identical* on real captures: `docx_text` vs `capture-text.py` on `3a8b4597…` (19682 chars, `same_bytes
   true`, `first_diff null`) and `b825f17c…` (18841 chars, `same_bytes true`) — so only the precedence in (1) moved.
4. **Unknown `.raw`, no `.txt`** (neither magic): round-54 kept the UTF-16LE fallback and built a row; candidate
   refuses (`no defined text form`, `build-spans.py:90`).
5. **Raw that `capture-text` refuses** (broken OLE, non-Word zip): round-54 fell back to `.txt`/UTF-16LE and built;
   candidate refuses the row (`capture-text refused …`, `build-spans.py:83-84`).
6. **Span context**: round-54 clipped raw-form context at the nearest CR (`:190-192`); candidate clips nothing
   (`:143`). Removing it is safe for defined forms: `capture-text.py` output for the five OLE and two zip captures I
   read has `CR 0` (`54fe0734` 13041 chars/1377 LF, `6dc68fd6` 27012/469, `74ced3e9` 13041/1377, `b539a802` 842/47,
   `bdff491a` 13718/865, `3a8b4597` 19682/1239, `b825f17c` 18841/664), and the `.txt` form is itself newline-normalised.
7. **`--check` comparison**: round-54 compares a span file *read as text with universal newlines* (`:221`); candidate
   compares **bytes** (`:170`).
8. **CLI and wording**: `--root LANE` (`:239`) replaced by required `--quotes`/`--out`; refusal messages reworded
   (quote truncated to 60 chars, `offset`/`char` semantics unchanged: `chars.append(off)`, `offset = start`, `:148-149`).

## Differential table (both builders, same `quotes.tsv` and same cache; `$S/final-table.txt`)

| # | capture fixture | round-54 | candidate |
|---|---|---|---|
| A | OLE `54fe0734` + garbage `.txt` holding the quote once | rc=0, `char 16`, sha `4e451b48…`, offset 0 | rc=0, `char 81`, sha `d341c133…`, offset 1 |
| B | zip docx `3a8b4597` + `.txt` holding the quote | rc=0, `char 8`, sha `9e79357b…` | rc=0, `char 9`, sha `16fc8c55…` |
| C | HTML raw + `.txt` with the quote twice | rc=1 `quote not exactly once in any form (…txt:2x, …raw:0x)` | rc=1 `quote occurs 2x in …txt` |
| D | unknown raw, no `.txt` (UTF-16LE text) | rc=0, built row, `char 4` | rc=1 `no defined text form for 3b3aebfc5609cf2d910cb394 (raw neither OLE nor zip, no .txt)` |
| E | OLE magic + 2048 zero bytes + `.txt` with quote | rc=0, built from `.txt` | rc=1 `capture-text refused e5669344ae23841d2793fb57.raw: ole-malformed: sector shift 0, mini shift 0` |
| G | zip xlsx `cb101e95` + `.txt` with quote | rc=0, built from `.txt` | rc=1 `capture-text refused …: main part 'xl/workbook.xml' is not WordprocessingML …` |
| F | `.txt`-only `271e1a22…` (real capture) | rc=0, `char 3264`, sha `091cadb4…`, offset 3184 | rc=0, identical manifest and span bytes (`identical_manifest=True`) |
| J | `.txt` with CRLF + lone CR + LF + one invalid UTF-8 byte | rc=0, `char 11`, sha `1b69fdec…` | rc=0, identical manifest (`identical_manifest=True`) |
| L | OLE `6dc68fd6`, **no** `.txt` | rc=0, `char 1333`, offset 1327 | rc=0, `char 53`, offset 0 |
| H | `--check`, span file LF→CRLF retouched | rc=0 `SPANS_ROWS=1 STALE=0` (false pass) | rc=1 `SPANS_FILE_STALE spans/S127-1.txt`, `STALE=1` |

Cases C, D, E, G: candidate exits 1 with `row=-` and writes **no** `spans.tsv` (nothing written on refusal, as its
docstring says). A and B: both builders succeed but on *different documents* — the recorded `capture_sha256` is the
digest of the file each actually read (`.txt` for round-54, `.raw` for candidate), and `char` is the offset in each
one's own form.

## No behavioural change for `.txt`-only captures — confirmed

F (real capture, quote at offset 3184) and J (mixed newlines plus an invalid UTF-8 byte, exercising the candidate's
explicit `.replace("\r\n","\n").replace("\r","\n")` at `:87` against round-54's `read_text` universal newlines):
identical `spans.tsv` bytes, identical span files, identical `char` and digest in both runs. A `.txt`-only capture
takes the same branch in both builders (`elif txt.is_file()`, `:85-88`), and `--check` on an untouched tree is
`STALE=0` under both.

## Findings against C1 (frozen predicate untouched; reported, not patched)

- **F1 the diff is what makes the gate's oracle comparison meaningful.** The gate re-derives every expected form
  with its own oracle (`c1-gate.py:150`, used at `:225`, `:240`) and pins `tools/capture-text.py` (`:451`); the
  candidate reads its forms through that same `tools/capture-text.py` (`build-spans.py:41,56-60,77-84`). Measured:
  for fixture A the oracle form's `find` is **81** and the candidate emits `char 81`, round-54 emits `char 16` (its
  garbage `.txt`); for L the oracle form's `find` is **53**, candidate 53, round-54 1333. Round-54's builder therefore
  cannot satisfy the gate on OLE/zip captures; it is a precondition, not a narrowed predicate.
- **F2 acceptance set strictly shrinks** (D, E, G build under round-54, refuse under the candidate). Every candidate
  refusal still starts `build-spans: refused <id>: ` — the prefix `c1-gate.py:331` matches — so no battery entry or
  gate clause I saw is keyed to a message the candidate stopped emitting.
- **F3 `--root` removal**: the only in-lane invocations of `tools/build-spans.py` pass `--quotes/--out/--cache`
  (`c1-gate.py:204,417,440`); `grep -rn 'build-spans.py' --include='*.py' --include='*.sh' .` returns only per-round
  builder files and the round-52/54 counters importing their own sibling, and the two `--root` flags in
  `tools/inference-ground.py:535` and `corpus/evidence/round56/c2-count.py:178` are those tools' own.
- **F4 bytecode deposit (operational)**: because the candidate imports `capture-text` (`:57`), a plain run without
  `PYTHONDONTWRITEBYTECODE` writes `tools/__pycache__/capture-text.cpython-314.pyc` into the lane tree — observed in a
  scratch copy of `tools/` (`ls tools/__pycache__` → `capture-text.cpython-314.pyc`). Gate and counter set the flag
  (`c1-gate.py:153,201,417`, `c1-count.py:125`), and `tools/__pycache__` is untracked (`git ls-files tools/__pycache__`
  empty), so C1's receipts are unaffected; a human invocation leaves an untracked artifact.
- **F5 new runtime dependency**: the builder now requires `tools/capture-text.py` beside it (importlib, `:56-60`);
  battery entries run the builder in-process via `runpy.run_path` (`battery/m1-quote-only-span.py:16-23`), so they
  always import the lane copy — `oracle-m8-unpinned.py` (capture-text plus one comment line) is never the module the
  builder loads. A missing `capture-text.py` is an uncaught traceback, not a refusal — observed in a scratch copy:
  `FileNotFoundError: … tools/capture-text.py`, rc=1, no `build-spans: refused` line — a robustness gap worth a
  clause if the gate is meant to report operability rather than a stack trace.

Tooling: nothing installed or upgraded (no tool was needed; `python3` 3.14.8 as shipped). Scratch removed at the end.

VERDICT: attacked the round-54-vs-candidate `build-spans.py` difference — 8 behavioural differences reproduced on 10
fixtures (OLE/zip precedence, OLE and zip form readers, unknown-raw and refused-raw acceptance, CR clipping, `--check`
byte comparison, CLI); `.txt`-only captures are byte-for-byte unchanged; C1's frozen predicate survived.

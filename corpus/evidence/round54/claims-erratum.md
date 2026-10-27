# Round 54 — claims erratum (post-freeze changes, disclosed)

Freeze `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0` (`claims.md`). No predicate, target, counter, kill rule
or control file of the freeze was changed; everything below was added after it and none of it is a
claim's rule.

## E1 — a C1 supplement and a forge control, added after W1 forged the frozen counter

W1 `R54CritForgeC1` passed `c1-count.py` 6/6 (seed 7 and three unseeded runs) with a tool that never
parses the compound file: GEN read the HTML the counter leaves beside each generated `.doc`
(`doc-<tag>/<name>.doc` → `src-<tag>/<name>.html`), REAL returned LibreOffice exports canned by the
pinned sha256 prefixes, and the refusal legs keyed on byte markers. The L1 rebuilt that shape as
`controls/build-c1-forge.py` and wrote `c1-supplement.py` (ISOLATED: each generated document copied
alone under a random name; RESAVE: each pinned capture round-tripped through LibreOffice to new bytes;
HELDOUT: documents made from lane knowledge files), every run under the frozen audit hook. Receipt
`controls/c1-forge.txt`: the rebuilt forge scores `LEGS=6/6` on the frozen counter and
`SUPPLEMENT_LEGS=0/3` on the supplement; CONST, NAIVE, REFUSEALL and SHELL score 0/3. The candidate's
supplement result is in `measure-after.txt`. The frozen counter remains forgeable; C1's verdict is
judged on it and capped accordingly.

## E2 — the C1 tool changed after the candidate commit

W1 `R54ReviewOleTool` F1: the Clx walk trusted a signed `cbGrpprl`, so a malformed `.doc` hung the
tool or exited 1 with a Traceback instead of `REFUSED ole-malformed`. The landed tool bounds it
(`Prc GrpPrl outside the Clx`). W1 `R54ReviewOleSpec` found the OLE form emitted tracked-deleted text as
live text (its OOXML form drops `w:delText`); the landed tool reads the CHPX FKP pages of the PlcBteChpx and
drops runs carrying sprmCFRMarkDel (fixture `corpus/fixtures/capture-text-ole/tracked.doc`, check
`tracked-deletion-check.py`: candidate FAIL, landed PASS). Hidden text stays emitted in both forms (named in
the docstring). The five pinned captures' text forms are byte-identical before and after both changes
(sha256 of each, L1 run), and the after-measurement in `measure-after.txt` names the tool sha256 it ran on. No frozen leg reaches the Clx
walk (W1 `R54ReviewOleTool` F2), so the frozen counter cannot see this fix either way.

## E3 — the r37 entry's S101 leg cut in round

The W1 draft of `source-type-taxonomy-r37.md` cited the held S101 with four quotes anchored "in the raw
UTF-16LE text form" — the form `## Mistakes` row 2 of the lesson finds undefined. The L1 cut that leg
(no `source: S101` line; S101's `used-by` unchanged). The frozen C2 predicate makes S101 optional, so
this is a narrowing inside the rule, not a change of it.

## E4 — the S123 PDF quotes are cross-checked under NFKC

QUALITY 96 asks every PDF quote to occur in an independent extraction. The round-53 check compared
whitespace-removed strings; the S123 sidecar renders fullwidth Latin (`附录Ａ`, `ＹＹＹＹ`) where pypdf
renders some halfwidth, so `pdf-crosscheck.py` (round 54) compares under NFKC folding and prints the
unfolded miss count too: `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14`. Not a C2 leg.

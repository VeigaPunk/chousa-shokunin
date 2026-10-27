# R55MutC2Counter — mutation test of the frozen C2 counter (`corpus/evidence/round55/c2-count.py`)

date: 2026-10-27 · counter under test sha256 `6fa1e4b4fc55812fff177858a1d2120babf03968263ed368b9dd431817570163`
(committed at the 1fc5d92 freeze and byte-identical at the lane tip 53f1ce6 my clone observed — verified by
hash equality). Method: controls first, then one check removed per scratch copy of the counter, one
shortcut root per mutant that must pass the mutant (`C2=PASS` exit 0) and fail the frozen counter.
No installs (none needed); no network; no LibreOffice (no `soffice.bin` at exit, `pgrep` clean);
scratch `/fast/scratch/hyaku/chousa-r55/R55MutC2Counter/` (removed at end). `c2-count.py` accepts no
`--work`; every counter run passed `--root <scratch root>` instead. Mutant copies need `parents[3]` to
resolve the lane, so they live in a read-only scratch clone `mirror/` (`git rev-parse --show-toplevel`
= the clone; clone only, never written by the counters).

## 1. Controls reproduce

    python3 …/controls/build-c2-controls.py $S/c2c          # → staged rewrite
    python3 …/c2-count.py --root $S/c2c/staged ; echo $?    # → exit=1
    python3 …/c2-count.py --root $S/c2c/rewrite ; echo $?   # → exit=1

Both outputs diff clean (byte-for-byte, all 21 lines + exit) against
`controls/c2-controls.txt`: staged `REF_ID_UNBOUND=12 … C2=FAIL exit=1`; rewrite
`BOUND=2/3 GUIDELINE_BOUND=yes REF_ID_UNBOUND=2 … C2=FAIL exit=1`.

## 2. Pristine baselines (roots my builder drafts in scratch; frozen counter)

To give every mutant a root that fails *only* the removed check, I built two scratch roots from a
`git archive BASE_REV` tree + the read-only package entry + the on-disk captures (defined forms
derived exactly as the counter does: BASE `capture-text.py` on the gcpunion `.raw`
`bdff491a…raw`, `.txt` captures via `read_text(utf-8)`):

- `golden` — entry binds S124 (gcpunion `.doc`, 3 quote rows) + S125 (cnpharm, 3 rows), refuses
  NMPA_EN via a `refused-doc:` lesson line, cites the 梅斯 item as held `S113`, registry anchor
  cells `char 4671` / `char 780`, lesson with the quarantine verdict line →
  `C2=PASS exit 0` (all legs n/n, `CAPTURE_BOUND=6/6 SUBSTANCE=PASS ANCHOR_BOUND=2/2
  QUARANTINE_VERDICTS=1/1 (S125)`).
- `allbound` — same + S126 (NMPA English notice, 3 rows) bound, nothing refused → `C2=PASS exit 0`
  (9/9 everywhere). So the frozen counter is satisfiable and its controls are not vacuous.

## 3. Mutants (one check removed per scratch copy; exact removals in the table)

| check removed | mutant diff (scratch copy) | shortcut root = golden/allbound + one defect | frozen verdict (exit 1) | mutant verdict |
|---|---|---|---|---|
| MUST_BIND | ok: dropped `MUST_BIND in bound.values()` | `b1_mustbind`: allbound with GCP refused (no S124 row/source-line/tokens, `refused-doc:` line) binds S125+S126 | `GUIDELINE_BOUND=no`, all other legs pass | **C2=PASS exit 0** — killed-by-check: check is load-bearing |
| defined-form rule (refuses `.txt` sidecar digest for an OLE raw) | `form_text`: `elif txt.is_file()…` → `if out is None and txt.is_file()…` (R54 `.txt`-first shim) | `a1_sidecar`: golden + a 4th S124 row quoting the sidecar's garbage run `Microsoft Visio`, digest = sha256 of `bdff491a….txt` (`55b4085c…`), span sliced from the sidecar | `CAPTURE_BOUND=6/7` (form is None for a sidecar digest), everything else 7/7 or 2/2 | **C2=PASS exit 0** (`CAPTURE_BOUND=7/7`) |
| OPENED (`r[8] == OPENED`) | binding: dropped `r[8] == OPENED and` | `b2_opened`: allbound with S124 row opened `2026-10-26` | `BOUND=2/3`, `nbound+refused=2≠3` | **C2=PASS exit 0** (3/3) |
| used-by == citing | binding: dropped `used == citing and` | `a2_usedby`: golden with S124 `used-by` naming a second file | `BOUND=1/3`, `REF_ID_UNBOUND=4` | **C2=PASS exit 0** |
| REF_ID_UNBOUND | ok: dropped `and unb == 0` | `a3_refid`: golden + one stray `` `S114` `` token in the entry | `REF_ID_UNBOUND=1`, rest unchanged | **C2=PASS exit 0** |
| SUBSTANCE | ok: dropped `and substance` | `a4_hollow`: golden + 4th S124 row with one-character quote `五` (real form slice) | `SUBSTANCE=FAIL` (HOLLOW_QUOTE), other legs 7/7 | **C2=PASS exit 0** — note it still *prints* `SUBSTANCE=FAIL`; print/ok are decoupled |
| ANCHOR_BOUND | ok: dropped `and anchors == nbound` | `a5_anchor`: golden with S124 anchor cell `char 999999` | `ANCHOR_BOUND=1/2`, rest unchanged | **C2=PASS exit 0** |
| QUOTES_IN_LESSON | ok: dropped `in_lesson == n and` | `a6_lesson`: golden lesson minus one S125 quote line | `QUOTES_IN_LESSON=5/6`, rest unchanged | **C2=PASS exit 0** |
| QUARANTINE | ok: dropped `len(verdicts) == len(reg_ids) and not blocked` | `a7_quar`: golden lesson minus the register-`S125` verdict line | `QUARANTINE_VERDICTS=0/1 (S125)`, rest unchanged | **C2=PASS exit 0** |

Every mutant was also run on its pristine root (golden, or allbound for the two allbound-derived
ones): all `C2=PASS exit 0` — no mutation rejects an honest root, so each shortcut's PASS is
attributable to the removed check alone.

## 4. Verdict per check and coverage

All nine assigned checks have a working shortcut: each removal admits a defect the frozen counter
refuses, i.e. **no dead check among the nine; every one is load-bearing.** No assigned check went
unexercised. Coupling discovered while crafting shortcuts (counter properties, not defects):
`nbound + refused == len(by_doc)` means a row that is present-but-unbindable (wrong `opened`, wrong
`used-by`) cannot pass even the corresponding mutant unless another doc takes its place — so the
OPENED/USED-BY shortcuts had to bind a third document; and `offsets` (ANCHOR) is fed only by rows
passing `quote in span`, so a manifest patch must not clobber an existing span file (my first
a1/a4 attempt reused `S124-1.txt` and failed on QUOTES_IN_SPAN/ANCHOR instead — rebuilt to append
`S124-4.txt`).
`ok` conjuncts this seat's nine shortcuts do **not** isolate: `ENTRIES`/`REFUSED_ENTRIES`,
`nbound >= MIN_BOUND`, `NEW_GROUND`, `n > 0`, `ON_BOUND == n`, `ids_ok` (SPAN_IDS min-3),
`QUOTES_IN_SPAN`, `QUOTES_IN_ENTRY`, `QUOTE_SHORT`, `SPAN_CONTEXT`, `HELD_BAD`, `INFERENCE_GROUNDED`,
the `--lane-only` `CAPTURE_BOUND=skipped` guard, and the refusal sub-check `no_src` (the
`refused-doc` line was exercised, the no-`source:`-line half only as part of b1's refusal).

## 5. Restoration evidence

    sha256 before: 6fa1e4b4fc55812fff177858a1d2120babf03968263ed368b9dd431817570163
    sha256 after:  6fa1e4b4fc55812fff177858a1d2120babf03968263ed368b9dd431817570163
    frozen re-run on golden after all probes: exit=0, output byte-identical to the pre-mutation baseline
      (diff of the two captured outputs: empty)
    the frozen file was never written; all mutants live in scratch `mirror/corpus/evidence/round55/m_*.py`;
    scratch removed after this report.

Side observations (reported, not patched): the lane tip moved 1fc5d92→53f1ce6 (L1 verdict +
C2/C3 after-measurements) while this seat ran; the counter bytes are identical, so probes remain
valid against the frozen counter. The `golden`/`allbound` scratch roots double as proof that C2 is
reachable by document-binding exactly as claimed (S124+S125 bound, NMPA_EN refused, held S113), but
adjudication belongs to the L1, not this seat.

VERDICT: attacked the frozen C2 counter with 9 one-check-removal mutants (MUST_BIND, defined-form
sidecar refusal, OPENED, used-by==citing, REF_ID_UNBOUND, SUBSTANCE, ANCHOR_BOUND, QUOTES_IN_LESSON,
QUARANTINE); every mutant admits a crafted shortcut root it passes and the frozen counter fails
(each `C2=FAIL` exit 1 → mutant `C2=PASS` exit 0, pristine roots unaffected), all 9 checks are
load-bearing, controls reproduce byte-for-byte, and the frozen counter was restored/verified
byte-identical.

# R54ReviewC2Counter — round-54 C2 counter + builder review

## Scope and method
- Attacked only the frozen counter `corpus/evidence/round54/c2-count.py` (sha256 `0b836197…`) and builder
  `corpus/evidence/round54/build-spans.py` (`e8337aba…`) against their round-53 originals. No predicate, target,
  counter or control change; no production write. `git -C <lane> diff --stat HEAD -- corpus/evidence/round54/` is
  empty, so the shas above are the committed files.
- The lane moved while I reviewed: the wave-1 build landed the two entries, lesson, `spans.tsv` and S121–S123 rows
  (22:38–22:56) and the frozen counter on the live tree printed `ENTRIES=2/2 BOUND=3/3 QUOTE_ROWS=33
  CAPTURE_BOUND=33/33 C2=PASS`. That is a sibling's build, not my measurement. Every probe below runs the frozen
  counter on a scratch `--root` copy under `/fast/scratch/hyaku/chousa-r54/R54ReviewC2Counter` (TMPDIR there,
  removed at exit); captures read only from the read-only `.qcache`; no network.

## 1. Diff against round-53 — what actually changed
- Code-only diff (`diff <(sed -n '/^LANE = /,$p' r53) <(sed -n '/^LANE = /,$p' r54)`): BASE_REV, entries, URLs,
  `HELD`, `ALIASES`, `TERMS`, `MIN_BOUND` 3→2, the `_builder`/evidence/lesson paths, the new HELD block (:184-198),
  and the `ENTRIES=` denominator + new `HELD_CITED` print (:272-273). Every other leg is byte-identical logic
  (`short`, `ctx`, `in_span`, `in_entry`, `in_lesson`, `on_bound`, `ids_ok`, `cap_bound`, `anchors`, `substance`,
  `grounded`, `verdicts`).
- Builder: 5 changed lines, all `round53`→`round54` in the docstring and the one path (:243); no logic change.
  `python3 corpus/evidence/round54/build-spans.py --check` prints `SPANS_ROWS=33 STALE=0`, exit 0.

## 2. Findings

### F1 (high) — `held_bad` does not fire when the HIT URL is named outside a `source:` line
`citing` is built only from `^source:` lines (`c2-count.py:187`), so a `note:`/`adopted:`/body mention leaves it
empty, the loop `continue`s (:188-189), and neither `held_bad` nor the `used-by` clause runs. The predicate's
"an entry citing the HIT specification does so only as `source: S101 — <its url>` and S101's `used-by` names it"
is unenforced for a prose mention. Reproduced on a copy of the live tree:
```
T=$(mktemp -d -p "$TMPDIR" H2.XXXX); cp -a corpus tools "$T"/
printf '\nnote: see %s (probe)\n' 'https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc' >> "$T/corpus/knowledge/source-type-taxonomy-r37.md"
python3 corpus/evidence/round54/c2-count.py --root "$T" | grep -E '^(ENTRIES|HELD_|REF_ID|C2)'
```
observed `HELD_CITED=- HELD_BAD=0`, `REF_ID_UNBOUND=0`, `C2=PASS`, exit 0, with S101's `used-by` still
`citation-count-semantics-r37.md`. The same URL inside another `source:` line's annotation *does* fire
(`HELD_BAD=1`, `REF_ID_UNBOUND=1`, `C2=FAIL`). Risk is live: the landed r37 names the host `jc.hit.edu.cn` in its
`adopted:` line — one step from the full URL.

### F2 (medium) — the S101 exemption is global, not per entry
Once any entry cites HIT correctly, `held_ok={"S101"}` and :198 exempts an `S101` token anywhere, including an
entry that cites no HIT row; the predicate allows only "S101 so cited". Probes: correct hold + a stray `S101`
token appended to r36 → `HELD_CITED=S101 HELD_BAD=0 REF_ID_UNBOUND=0 C2=PASS`; the same stray token with no
correct hold → `REF_ID_UNBOUND=1 C2=FAIL`. Recipe: apply the F1 held citation *and* add
`, corpus/knowledge/source-type-taxonomy-r37.md` to S101's `used-by` cell (12th cell), then append
`- probe: stray token S101` to r36 (scratch `probe/H1_correct_hold`, `H3_stray_token_other_entry`,
`H3b_stray_token_no_hold`).

### F3 (low) — the REFUSED "no lane row" test is row-shape- and `url_of`-sensitive
`hits` needs `len(r)==11` *and* `url_of(r[1]) == url_of(doc)` (:170). A registry line for the document with a
literal `|` in a cell (12 cells), or with another URL first in the source cell, is invisible: `registry()` parsed
122 rows from a fixture SOURCES.md, the openstd URL appeared on 1 line, `hits=0`, and the document counted
`BOUND=2/3 REFUSED=1` although a lane row names it — while the claim defines REFUSED as "no lane row". Same class:
`url_of` keeps a trailing `)` for a parenthesised URL (`mirror.example/x)` observed).

### F4 (low) — openstd's `.txt` and `.raw` are byte-identical, so `capture_sha256` cannot name the form
`sha256(b9ca….txt) == sha256(b9ca….raw) == 2d68faf7…` (both 24,185 bytes). `form_text` (:123-131) resolves by
digest and tries `.txt` first, so the counter always reads the `.txt` there; if the builder ever picks the raw
form (its `pick` order is `.txt`, then `raw_form`, so only when the quote is not exactly-once in the `.txt`) the
manifest stays self-consistent while `CAPTURE_BOUND` fails. Fail-closed, but the printed line cannot say why.

### F5 (info, inherited) — accounting scans only the two new entries
`:180` and `:198` iterate `texts` (the two ENTRIES), while the claim says "no `source:` line naming its URL in any
existing entry" / "the existing entries". Round-53 had the same scope, so this is not a round-54 regression; no
effect this round — `grep -rln 'std.samr…\|openstd…\|xuebaobangong…' corpus/knowledge` returns exactly r36/r37.

### F6 (info) — the quarantine count is derived, never asserted
`reg_ids` comes from the read-only register (:257-263), so `QUARANTINE_VERDICTS` is `len(verdicts)/len(reg_ids)`;
today 3 (S080,S088,S096, re-derived by re-running the extraction). A register row lost upstream would shrink the
leg silently while `C2=PASS` (the claim fixes "3 at the freeze"); REGISTER and the cache carry no digest pin.

### F7 (info) — `DOCS`' staged-id column is dead data
`for entry, _sid, url in DOCS` (:166) never uses the staged id, so a wrong staged→lane mapping there would go
uncaught; staged ids are caught only indirectly, as unbound S-tokens.

## 3. The four asked questions
- **ENTRIES 2/2 with min 2 — not weaker.** `len(texts) >= MIN_ENTRIES` plus `len(texts)+len(refused_entries)==2`
  forces both files, matching "both of which exist"; round-53's 3-with-min-2 could refuse one entry. The
  `REFUSED_ENTRIES` path is therefore dead in round 54.
- **BOUND min 2 of 3 — as frozen, and the complement works.** `nbound>=2 and nbound+refused==3` (:291-292) forces
  all three documents to be accounted; a well-formed row that fails the bound tests counts as neither → FAIL.
  Positive control: dropping the S122 row, its source line and its manifest rows and naming its URL on a
  `refused-doc` line printed `BOUND=2/3 (min 2) REFUSED=1` (it then failed only on S122 tokens left in the entry
  body — correct).
- **HELD — weaker than the predicate twice:** F1 (`held_bad` silent on a non-`source:` mention → `C2=PASS`) and
  F2 (a stray `S101` token in a non-citing entry is not unbound once any entry cites HIT). It does fire on a stale
  `used-by` (`HELD_BAD=1 REF_ID_UNBOUND=2 C2=FAIL`) and on a wrong id (`source: S999 — <HIT url>` → same).
- **Predicate text — equals claims.md sentence for sentence.** Extracted the claims.md `**Frozen predicate**`
  paragraph and the docstring's `Predicate R54-C2…` paragraph, collapsed whitespace, `diff` → empty; both 2,205
  chars, sha256 `43c06ca82c766b3246fb3abd0c3a0f37d22b9f81f3f69bf94cebf25b1225614e`, 11/11 `;`-parts identical.

## 4. `form_text` and the SAMR form (asked)
Direct call of the frozen `form_text` with each manifest digest: SAMR `picks_txt=True` (3,591 chars = `.txt`;
`raw_form` 38,126 chars of mojibake), OPENSTD `picks_txt=True` (22,007; `raw_form` 12,093 mojibake), JMU
`picks_txt=True` (83,061; 3,104,042 mojibake) — the `.txt` wins for both HTML captures and the PDF, and the builder
recorded the `.txt` digests for SAMR (`4e46154f…`) and JMU (`13a34aa9…`).
The SAMR `.txt` is the right form: 3,591 characters / 6,626 bytes of rendered text vs 76,252 bytes of HTML in
`.raw`; the fields the S080 row needs survive it (`GB/T 7714-2025` ×2, `发布日期` ×1, `2025-12-02` ×2, `实施日期`
×1, `2026-07-01` ×2), and the register's joined quote occurs 0 times in `.txt` and 0 times in `.raw`-as-UTF-8, so
choosing `.txt` does not manufacture that absence. Correction to the brief: the SAMR `.txt` is 6,626 **bytes** =
3,591 characters, matching the entry's own figure.

## 5. Checks that passed (so they are not re-litigated)
- CAPTURE_BOUND binds: one forged `capture_sha256` gave `CAPTURE_BOUND=32/33 C2=FAIL` in the ordinary run and
  `CAPTURE_BOUND=skipped C2=PASS` under `--lane-only`, exactly as the docstring says.
- The positive held path works but no receipt exercises it: `source: S101 — <HIT url>` with `used-by` gaining r37
  printed `HELD_CITED=S101 HELD_BAD=0 C2=PASS`; both controls show only `HELD_BAD=1` and the build shows `-`.
- `SUBSTANCE`, bound-anchor, `ON_BOUND`, `SPAN_IDS` and inference-ground legs are unchanged from round-53 and
  refused nothing unexpected in my probes.

## 6. Residual risk / what closure must still do
- Adjudicate F1/F2 by hand. With the held leg vacuous in the landed build (r37 cites S123 only), the "does so
  only as `source: S101`" clause has no receipt; if a HIT citation is added later, only the `source:` form is
  checked.
- `ON_BOUND == n` forbids S101/refused-doc span rows although the claim only sets a floor per bound id — a build
  constraint, not a weakening; keep `spans.tsv` to bound ids.
- Hand-check the three quarantine verdicts; the counter parses labels only. The live lesson currently reads
  `absent-as-written` for S080/S088/S096, and the S080 measurement in §4 is consistent with that.

VERDICT: the round-54 C2 counter is not weaker than round-53 on ENTRIES, BOUND or predicate text (the predicate is byte-identical), but its new HELD leg is falsified twice — a HIT URL named outside a `source:` line passes with `C2=PASS`, and a stray `S101` token in a non-citing entry is never unbound — with a lower-severity REFUSED row-shape hole and an openstd form-digest ambiguity left on record.

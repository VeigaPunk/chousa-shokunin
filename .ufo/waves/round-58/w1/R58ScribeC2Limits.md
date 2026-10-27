# R58ScribeC2Limits — C2 entry Limits section (S101 carrier alphabet)

Seat: `R58ScribeC2Limits` (leaf, report-only). Claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`,
freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`. Read: `corpus/evidence/round58/claims.md`,
`c2-count.py`, `c2/quotes.tsv`, `controls/c2-before.txt`, pinned `tools/capture-text.py`,
`tools/build-spans.py`, `tools/inference-ground.py`, `corpus/evidence/round51/quote-substance-check.py`.
No lane file, capture, pin, or counter was modified. No fetch.

## Behaviour

Re-opened the lane-owned S101 bytes, derived the defined text form, rebuilt the 12 spans with
the pinned builder, and mapped every frozen row to its ±80-character window so the Limits
draft can state exactly which source text the twelve rows do and do not reach. Then drafted
the entry's `## Limits` section for `corpus/knowledge/carrier-alphabet-china-r58.md`. That entry
does not exist yet (`ls` → *No such file or directory*), so the C2 counter was **not run**: with
no entry it can only print `ENTRY_MISSING`, already receipted in `controls/c2-before.txt`
(`ENTRIES=0/1 … C2=FAIL EXIT=1`). The draft below is unintegrated text for the entry author.

## Gates exercised (exact)

```
$ sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw tools/build-spans.py tools/capture-text.py
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
   (all three match claims.md)

$ TMPDIR=<scratch> python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > form.txt
RC=0   469 lines / 27012 code points   sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867

$ TMPDIR=<scratch> python3 -B tools/build-spans.py --quotes corpus/evidence/round58/c2/quotes.tsv \
      --out spans --cache corpus/captures
QUOTE S101 char 315 … char 11723 (12 lines)   SPANS_ROWS=12 WRITTEN=12   RC=0
span offsets 235 250 510 603 654 701 717 758 885 913 1380 11643  (each = quote offset −80)
span lengths 173–196 chars; every span ends inside its frozen quote's ±80 window
```

All twelve offsets (`315 330 590 683 734 781 797 838 965 993 1460 11723`) reproduce in
`c2/quotes.tsv` order, so the boundary below is the boundary the predicate will score.

## Boundary map (verified against the span files, not inferred)

- **Inside** the windows but *not* quoted: `对于非纸张型载体的电子文献` (668–680); the electronic
  letters `DB CP EB` (638–644); `磁盘(disk)` / `DK` (755, 764); the tail of the paper-carrier
  exception, truncated mid-character at `…不必注明其载` (span 10 ends at 1106).
- **Outside every window**: the letter run `M C N J D R S P G B O K` (444–466; span 2 ends exactly
  on the first letter, tail `…标识\nM\n`); the `Z` rule (496); `[DB/MT]`, `[CP/DK]`, `[EB/OL]`;
  `15.5文献载体代码，根据GB 3469规定，采用1位字母：P——印刷本，M——缩微制品` (25020);
  the 14.3.4 restatement (13440); the document-code values `A——基础性…` (12045);
  `GB/T 7714` (12802, 21403) and `GB/T 7714-2005` (15169); the title at offset 0.

## Paste-ready draft for the entry (no S-id other than S101)

```markdown
## Limits

Offsets and line numbers are into the defined text form (`tools/capture-text.py`, main story
only: headers, footnotes, text boxes are not in it); they are not offsets into the `.doc`
bytes. The evidence is the twelve rows of `corpus/evidence/round58/c2/quotes.tsv` and the
±80-character window the pinned `tools/build-spans.py` rebuilds per row. Text marked *outside*
below is context, present in the capture but not reached by any frozen row.

1. **Contemporary standard status.** The capture is
   `中国学术期刊(光盘版)检索与评价数据规范（修订本）` (line 1) — a journal data
   specification, not GB 3469. Inside the boundary GB 3469 appears once, as
   `根据GB3469规定` (line 15, offset 338), with no edition, year or issuing body; the form
   carries no 发布/实施 line and no `2015` at all. Every `GB/T 7714` citation — bare at
   12802 and 21403, `GB/T 7714-2005` at 15169 — is outside every window. So these rows say
   nothing about whether any edition of GB 3469 is current, withdrawn or superseded;
   `verified-at:` dates the lane's re-opening of the capture, not the standard. Deciding
   status needs a source outside the frozen set, which this round does not authorise.
2. **Completeness beyond the cited sections.** The rows quote the 1.2 heading and two
   lead-ins, the 1.2.4 carrier passage, three of its six compound examples, one 1.3 template
   line and the heading fragment of section 11. Out of reach: the letter run
   `M C N J D R S P G B O K` (lines 45–56, 444–466 — the text form flattens the table
   column-major and span 2 ends at its first letter, so no row witnesses which letter means
   which type); the `Z` fallback (line 58); `[DB/MT]`, `[CP/DK]`, `[EB/OL]`; section 15.5's
   one-letter carrier codes `P——印刷本，M——缩微制品` (line 404); the 14.3.4 restatement
   (line 261). The carrier list is quoted for MT, OL and CD only; DK occurs in window
   context, never as a quote. This entry therefore reports the sections it cites and does
   not claim the capture's alphabet, carrier set or example list is complete.
3. **Correctness of the standard.** No row witnesses GB 3469's own text: the letter scheme
   arrives as this specification's attribution (`根据GB3469规定`), and the two-letter carrier
   codes are recommended by the capture itself (`本规范建议采用`, line 71, window context),
   not attributed to GB 3469. Outside the windows the same document varies its terms:
   14.3.4 restates the passage with `文献类型标志` / `载体类型标志` and `CD-ROM`, against
   the quoted `标识` and `CD–ROM`, and 15.5 credits GB 3469 with a different one-letter
   carrier coding. The entry reports the capture's wording for the notation
   `[文献类型标识/载体类型标识]` and its examples at the cited offsets; it does not
   adjudicate whether that wording matches GB 3469, whether the restatement is accurate, or
   whether the document is internally consistent.
4. **Whether the types are current.** No row carries a date, an effective date or a
   supersession clause, and no year occurs inside any quote. `M/C/N/J/D/R/S/P/G/B/O/K`,
   `DB/CP/EB` and `MT/DK/CD/OL` are recorded as this capture's set at the cited offsets; the
   entry does not claim they are the present set, that any has been added or retired, or
   that present practice pairs types with two-letter carriers. Quote 11 (line 82) is an
   arrangement-format line from 1.3 and witnesses a template slot, not a type.

**Fragment scope.** Three rows are line-start bound (315, 330, 993 — two of them headings);
the other nine are mid-line substrings. Quotes 3 and 4 drop their sentences' scope clauses
(`对于数据库…等电子文献类型的参考文献`; `对于非纸张型载体的电子文献`), so read as strings
quote 4's annotation duty over-generalises beyond non-paper electronic carriers, and the
paper-carrier exception at line 78 is truncated inside window 10 and quoted nowhere. Quotes
5 and 6 are fragments of one sentence whose modality is 建议.
```

## Findings (no fix applied, predicate untouched)

- **F1 — counter leg weaker than the claim.** `c2-count.py` scores `NEW_GROUND` with
  `git … grep -l '載体类型标识' BASE -- corpus/knowledge` (traditional `載`) while testing the
  simplified `载体类型标识` in the entry. The claim itself holds: `git grep -l '载体类型标识'
  b13ca7b5 -- corpus/knowledge | wc -l` → `0`. But the traditional form matches nothing anywhere
  (`git grep -l '載体类型标识' b13ca7b5 | wc -l` → `0`) while the simplified form matches 6
  base files outside `corpus/knowledge`, so the leg cannot detect pre-existing ground. Reported,
  not a falsification of C2.
- **F2 — anchor floor is met exactly.** Anchors = 315, 330, 993 → `3/3`; two are section headings.
- **F3 — Limits prose is ungated.** `inference-ground.py` checks `#### Inference` bullets only
  (rule 1 of its docstring); entry prose and any `## Limits` section are unjudged, so the draft
  above is written to stay inside the boundary by itself.
- **F4 — flat-form table.** The type table renders as two vertical runs (labels 375–443, letters
  444–466); label↔letter pairing is positional and unwitnessed, and the only letter reachable by
  the boundary is `M` at 444 (span 2 tail).
- **F5 — source-internal variance out of window** (14.3.4 `标志`/`CD-ROM`; 15.5 `P`/`M` carrier
  codes) is the reason limit 3 forbids adjudication rather than resolving it.

## Surfaces

Touched: this report only. Scratch `/fast/scratch/hyaku/chousa-r58/R58ScribeC2Limits/`
(`form.txt`, `spans/`) created with `TMPDIR` set and removed before yield. No install/update,
so no tooling-channel record. Unrun: `c2-count.py` (no entry), `c1-count.py` (not this surface).

VERDICT: Limits section for the C2 S101 entry drafted across all four required axes plus fragment
scope, each limit anchored to a verified offset/line in the defined form and to that row's ±80
span window; the boundary map was reproduced by the pinned tools (12/12 offsets, spans 173–196
chars) and not by assumption — the draft survives as grounded text, the frozen C2 predicate is
unmodified and unrun, and the one leg-level weakness found (`載`/`载` in `NEW_GROUND`) is a
finding against the counter's sensitivity, not a falsification of the C2 claim.

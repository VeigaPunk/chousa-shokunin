# Round 79 corpus text — `corpus/SOURCES.md` candidate rows (drafted, not landed)

Seat `R79ScribeA`, lane `chousa-shokunin`. Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`
(round-78 lane tip); prefreeze instruments, controls and digest-bearing repairs
`e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; lane tip
`b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9` ("round-79: freeze the two claims, register
S196-S198, file the wave spec").

**This file drafts one new registry row and reports on two already-landed ones. It lands
nothing.** `corpus/` and the lane tree are read-only for this seat.

---

## 1. The state this seat found: both requested ids are already taken

```
$ grep -nE '^\| S19[678] ' corpus/SOURCES.md
208:| S196 | chousa QUALITY criterion 147 — corpus/QUALITY.md | own-work | B | the successor requirement an outer battery's subject copy must meet when the salt family is known to a normalizer | ee70e6df19fe43b1b384166cf5d360c3b99dafe2, criterion 147 at line 1056 | A subject-identity salt is a per-channel measurement, not a property of the salt, so the successor copy must not be a textual derivative of a committed file | mined | 2026-11-04 | on-release | corpus/lessons/round-79.md |
209:| S197 | chousa QUALITY criterion 146 — corpus/QUALITY.md | own-work | B | the successor requirement a self-assessment counter must meet when its repair lines are presence-only | ee70e6df19fe43b1b384166cf5d360c3b99dafe2, criterion 146 at line 1054 | A repair line must be validated against the bytes it names, and the pointer audit must cover every block rather than the newest | mined | 2026-11-04 | on-release | corpus/lessons/round-79.md |
210:| S198 | round-78 hollow-mirror receipt — .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt | own-work | C | a defect receipt offered as a source about verification method | 3eb4a3cad8febf75698a017cb6c4441f763b3454, wave file lines 1-20 | REJECTED: a receipt that demonstrates one counter's false green is that counter's own evidence, not a source about how self-assessment should be audited (the S195 class one layer out); flip: admit scoped to what a control receipt must carry if an admitted entry ever rests on receipt format | rejected | 2026-11-04 | on-release | — |
```

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
198
```

The registry's last id is **S198**, so the **next unused id is S199**.

Contract v1 (`CORPUS.md` § *SOURCES.md*, rule 2) says the registry is **append-only** and that
`id` is *"the next unused; never reused"*. The two ids this seat was asked to draft are live, so
neither can be reused.

## 2. The frozen claims file binds the live ids

```
$ git show e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c:corpus/evidence/round79/claims.md | grep -n 'Sourced on S196\|sourced on S197'
28:reports. Sourced on S196.
75:## C2 — calibration (sourced on S197)
```

- **S196** is C1's source. C1 is operability: *"the subject copy stops being a textual
  derivative"*. The requirement that states it is criterion **147** — *"A subject-identity salt
  is defeated by any normalizer that knows its marker family"* — which is what the landed S196
  registers.
- **S197** is C2's source. C2 is calibration: *"the self-assessment counter validates its own
  repairs"*. The requirement that states it is criterion **146** — *"A self-assessment counter
  validates each resolution line against the bytes it claims to repair"* — which is what the
  landed S197 registers.

**The scope assignment in this seat's prompt, read literally, conflicts with the frozen claims
file.** The prompt asks for S196 → "QUALITY 146's successor requirement" and S197 → "the
round-78 non-author spot-check's routed defect 2". Placing criterion 146 on S196 would put the
*calibration* requirement on the id the claims file binds to *C1*, and would leave criterion 147
— the requirement that actually states C1's target — with no row. The landed assignment
(S196 = criterion 147 → C1, S197 = criterion 146 → C2) is the one that satisfies the frozen
claims file, and it is already committed.

## 3. What this seat therefore drafts

| requested scope | already registered? | this seat's action |
|---|---|---|
| **QUALITY 146's successor requirement** (prompt's S196) | **Yes — the landed S197** (`corpus/SOURCES.md:209`), with the right anchor (`ee70e6df…, criterion 146 at line 1054`) and the right `teaches`. | **No new row.** A new row for the same source would be a duplicate. The only defect is in the lesson's `## Gate` line, which states the quote as 24 words when it is 25 — see `draft-mistakes-rows.md` § (b) Correction 2. That is a one-word edit to the lesson, not a registry row. |
| **the round-78 non-author spot-check's routed defect 2** (prompt's S197) | **No.** The registry has no row for the r78 closure record: `grep -n "round-78-verifier-spotcheck" corpus/SOURCES.md` returns nothing. | **One new row, id S199** (the next unused). Drafted below, with its `## Gate` line in `draft-gate-block.md`. |

This mirrors the round-78 shape exactly: r78 registered **S193** (the r77 spot-check's routed
defect 1 — the closure record), **S194** (QUALITY criterion 143 — the requirement) and **S195**
(a rejected receipt row). Round 79 already has its two requirement rows (S196 = criterion 147,
S197 = criterion 146); the closure-record row is the missing third, and S199 is where it goes.

---

## 4. The one new candidate row, contract v1 shape (11 cells, `NF=13` on `|`, no `|` inside a cell)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S199 | chousa round-78 verifier spot-check, routed defect 2 — corpus/lessons/round-78-verifier-spotcheck.md | own-work | B | the r78 counter's lexical escape hatches (`correction:` / `supersedes:` / `erratum:` presence only) and its newest-block-only QUALITY audit window | b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9, routed-defect list lines 189-192 (quote on line 189) | The closure record that names a counter's defect is not independent truth that the successor closes it; the committed counter and its receipts are | mined | 2026-11-04 | on-release | corpus/lessons/round-79.md |

### The row, cell by cell, and why each cell says what it says

- **id `S199`** — the next unused id. The registry's last id is S198 (198 rows,
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 198), so S199 is
  unused and legal under contract v1 rule 2.
- **source** — `chousa round-78 verifier spot-check, routed defect 2 —
  corpus/lessons/round-78-verifier-spotcheck.md`. The r78 spot-check is the closure record of
  round 78; its routed-defect list is section 5, and item 2 is the selfcheck defect. The path
  is the file the row cites, so the `used-by` and the anchor point at the same bytes.
- **kind `own-work`** — the source is this lane's own committed file at a pinned revision, the
  r78 S193 precedent.
- **tier `B`** — a strong secondary account with reproducible detail (the r78 S193 precedent
  gave the r77 spot-check's routed defect tier B). It is not tier A: it is a closure's record
  of a defect, not the truth that the successor repaired it.
- **scope** — what the tier applies to: the two defects the closure names, stated as the
  closure named them. This is deliberately narrow: it does not claim the round-79 counter
  closes them, which is the successor's receipts to show.
- **anchor** — `b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`, routed-defect list lines 189-192,
  quote on line 189. The revision is the lane tip, and the file is byte-identical there and at
  the base `ee70e6df` (`git diff --numstat ee70e6df19fe43b1b384166cf5d360c3b99dafe2 b58a02db --
  corpus/lessons/round-78-verifier-spotcheck.md` is empty), so the pin holds either way.
- **teaches** — one grounded learner benefit, in the r78 S193 shape: a closure record names the
  defect; it is not evidence that the successor closed it. The successor's own instrument and
  its receipts are.
- **status `mined`** — cited by `corpus/lessons/round-79.md`, which is the row's `used-by`
  path; contract v1 defines `mined` as "cited by ≥1 path in `used-by`".
- **opened 2026-11-04** — the date this seat opened the source, matching the round's opened
  date and the r78 rows.
- **recheck `on-release`** — a revision-pinned committed path with no external drift surface;
  every r78 row used `on-release`.
- **used-by `corpus/lessons/round-79.md`** — the lesson this row grounds.

### Anchor, pinned and verified

```
$ git show b58a02db:corpus/lessons/round-78-verifier-spotcheck.md | sed -n '189,192p'
2. **`selfcheck.py`'s escape hatches are lexical** (`correction:` / `supersedes:` / `erratum:`
   presence only) and its QUALITY window is the newest block only. QUALITY 146 carries it; the
   counter is not admissible as a calibration certificate until it validates the bytes each line
   claims to repair.
```

Line 189 carries the item's bold headline; lines 190-192 carry the rest of the item. The
`## 5. Routed defects (owner chousa, next round)` heading is at line 184, so a span starting at
184 would swallow the heading — the anchor starts at 189, the item itself.

The file is unchanged across the base and the tip:

```
$ git diff --numstat ee70e6df19fe43b1b384166cf5d360c3b99dafe2 b58a02db -- corpus/lessons/round-78-verifier-spotcheck.md
(no output)
```

### Measured word count — the `## Gate` quote

| row (id) | quote | `wc -w` | command |
|---|---|---|---|
| S199 (new row) | `` `selfcheck.py`'s escape hatches are lexical (`correction:` / `supersedes:` / `erratum:` `` | **10** | `git show b58a02db:corpus/lessons/round-78-verifier-spotcheck.md \| sed -n '189p' \| sed 's/^[0-9]*\. //; s/\*\*//g' \| wc -w` |

10 words, under the contract's 25-word bound. The quote keeps the line's own backticks and
drops the list numeral and the bold markers (the r78 S193 precedent did the same).

### The required `sed -n <line>p` output, pasted

```
$ git show b58a02db:corpus/lessons/round-78-verifier-spotcheck.md | sed -n '189p'
2. **`selfcheck.py`'s escape hatches are lexical** (`correction:` / `supersedes:` / `erratum:`

$ git show b58a02db:corpus/lessons/round-78-verifier-spotcheck.md | sed -n '189p' | sed 's/^[0-9]*\. //; s/\*\*//g' | wc -w
10
```

### Contract checks, run on a scratch registry

The two drafted rows (S199 and, in the alternative reading, a criterion-146 restatement) were
inserted after S198 on a **scratch copy** of the lane clone — the lane tree was not modified —
and the lane's own census was run over it:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file $S/census/corpus/SOURCES.md --root $S/census
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	$S/census/corpus/SOURCES.md
# exit: 0
```

`E01` (malformed row, `NF!=13`) and `E02` (id not `S[0-9]{3,}`) do not fire; the five `W04`
warnings are the pre-existing ones the round-78 closure already recorded. Receipt:
`receipts/census-validate.txt`.

The drafted row's 11 cells split to `NF=13` on `|`, and no cell contains a `|`.

## 5. What this seat did **not** do, and why

- **No second row for criterion 146.** The prompt's S196 scope is already the landed S197,
  anchor and `teaches` included. Adding a second row for the same source at a new id would
  duplicate a mined row and make the registry cite one requirement twice.
- **No in-place edit of S196, S197 or S198.** Contract v1 rule 2 forbids it; the L1's rows stay
  as they are. The defects this seat found in them are three *lesson-prose* defects (wrong
  word counts, a quote that is not in the file it is attributed to, a title that names the
  wrong receipt) and are reported in `draft-mistakes-rows.md` § (b) for the L1 to fix in the
  lesson or, for S198, to supersede with a new row.

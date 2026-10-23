# D7 — ready-to-paste drafts

Evidence read was local only. The S052 falsify artifact records the prior GET and its result; this seat did not re-open the URL or run a network fetch. Blocks below are drafts, not landed changes.

## 1. `corpus/lessons/round-31.md` — `## Mistakes`

**Insertion point:** Append as the final row of the `## Mistakes` table, after its existing last data row and before the next section heading. `round-31.md` was not present in `corpus/lessons/` when inspected, so there is no current line number to cite; insert at the named section boundary without rewriting prior rows.

```markdown
| A Gate quote was truncated at “socket” and given a period not present in the S052 source | Gate row: `corpus/lessons/round-30.md:47`; correction: `corpus/lessons/round-30.md:77-85`; failed re-open: `.ufo/waves/round-30/falsify/AttackRowS052.md:3-15`; routed as D7 at `corpus/lessons/round-30-verifier-spotcheck.md:190-191` | Round-30 falsify re-open (`AttackRowS052.md`); outside spot-check D7 | Re-open each exact Gate quote with `tools/quote-reopen.py` and admit it only on `VERBATIM`; preserve and correct any other verdict before citing the quote. QUALITY criterion 30. |
```

## 2. `corpus/QUALITY.md` — criterion 30

**Insertion point:** Append after current line 208, the end of criterion 29, under a new round-31 additions heading. Keep criteria 1-29 unchanged.

```markdown
## Round-31 additions (appended 2026-10-23; criteria 1-29 unchanged)

30. **A Gate quote is verbatim before admission.** Every new located quote in a
    Gate row is put, exactly as printed, in a TSV item naming its `S###` source
    and re-opened from the lane root with
    `python3 tools/quote-reopen.py verify --items <tsv>`. Admit the row only
    when its result is `VERBATIM`; preserve every other verdict with the quote
    and its disposition. A tool/input error is not a match. Shown able to fail:
    the S052 input row is
    `S052q1<TAB>S052<TAB>In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket.`;
    the falsify receipt records the exact command
    `timeout 120 python3 tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r30/w2/AttackRowS052/s052.tsv`
    from the lane root returning `QUOTE_REOPEN S052q1 ABSENT`,
    `QUOTE_REOPEN_SUMMARY verbatim=0 absent=1 too_long=0 no_source=0 unreachable=0`,
    exit 1 (`.ufo/waves/round-30/falsify/AttackRowS052.md:7-13`). The source
    capture contains `socket (they raise a timeout exception)` rather than the
    Gate's truncated `socket.` (`https://docs.python.org/3/library/socket.html#socket-timeouts`,
    opened 2026-10-23 in the round-30 evidence). —
    `lessons/round-30-verifier-spotcheck.md:190-191`;
    `lessons/round-30.md:47,77-85`;
    `.ufo/waves/round-30/falsify/AttackRowS052.md`.
```

**Failing-input record:** The TSV row above supplies the actual S052 Gate quote text (without Markdown quote marks). The cited historical command and `ABSENT`/exit-1 result are transcribed from the existing falsify receipt; they were not re-run here because that would fetch the registered page.

## 3. `corpus/lessons/round-30-verifier-spotcheck.md` — append-only correction

**Insertion point:** Append after current line 212, at the end of the file. This preserves all earlier routed-defect text.

```markdown

### 2026-10-23 correction (D7; round 31)

D7 above (`corpus/lessons/round-30-verifier-spotcheck.md:190-191`) is closed by this round's S052 mistake row in `corpus/lessons/round-31.md` and criterion 30 in `corpus/QUALITY.md`. The S052 Gate quote at `corpus/lessons/round-30.md:47` ended at “socket.”; the page text includes “socket (they raise a timeout exception)” (`https://docs.python.org/3/library/socket.html#socket-timeouts`, opened 2026-10-23 as recorded in the round-30 evidence). The existing falsify receipt shows the quote returned `ABSENT`, exit 1 (`.ufo/waves/round-30/falsify/AttackRowS052.md:3-15`). Earlier spot-check text is retained unchanged.
```

## Evidence and command provenance

- D7 says the S052 Gate error was not mined: `corpus/lessons/round-30-verifier-spotcheck.md:190-191`.
- The round-30 Gate quote is at `corpus/lessons/round-30.md:47`; its append-only source correction is at `:77-85`.
- `AttackRowS052.md:3-15` records the original page text, exact command, `ABSENT`, summary, and `EXIT=1`; no command or counter was run by this seat.
- `corpus/QUALITY.md:169-177` gives criterion 25's existing quote-reopen shape; criteria 26-29 end at line 208. No tool was installed or updated.

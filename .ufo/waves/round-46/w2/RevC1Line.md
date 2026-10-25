# RevC1Line — three texts, one rule (docstring vs R46-C1 vs the Gates row)

Item: the numbered rule `tools/inference-ground.py:11-25`, the frozen predicate `corpus/evidence/round46/claims.md:31-37`, the row `SKILL.md:116` (8 cells). Bytes: current tree `3018b1d25d76205496ae002600003f5ddb4294328be4741b9fa58c8ddc223f07` (= `measure-after.txt:6` "tool 3018b1d25d762054"); landing `d09fc8e` `819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc`.

C1 still scores as declared (`POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS`, exit 0) and both adopted entries pass (`tokens=7 grounded=7`, `tokens=5 grounded=5`). Nothing below falsifies the frozen predicate; every item is a rule/text disagreement.

## H1 (high) — fences: current bytes crash on any entry with a fence before the heading — **docstring wins**

The wave-2 bullet-closing edit landed in the *locating* loop, where `cur`/`bullets` do not exist (`:71-73`; the correct copy is `:91-94`).

    $ python3 cur.py --entry fence.md --spans …/spans.tsv --counts …/counts.json --root .
    File "cur.py", line 71, in inference_bullets
        if cur is not None:
    UnboundLocalError: cannot access local variable 'cur' where it is not associated with a value
    EXIT=1
    $ python3 head.py --entry fence.md …            # same entry, landing commit
    GROUND entry=fence.md section=1 bullets=1 tokens=1 grounded=1
    GROUND: PASS
    EXIT=0

Any fence before `#### Inference` hits it, including a document with no Inference section (`noinf_fence.md` → traceback, not `INF_SECTION_ABSENT`). Exit 1 with a traceback carries no `FINDING` and no `GROUND: FAIL`, and `c1-count.py:97-99` scores exit 1 as a kill. Clause 1 says this entry passes; the code crashes → **docstring wins**: delete `:71-73`.

Same rule, both versions: a bullet parked inside a fence **is** counted, yet clause 1 mentions only fenced *headings*.

    $ python3 head.py --entry fencedbullet.md …
    GROUND entry=fencedbullet.md section=1 bullets=2 tokens=2 grounded=1
    FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='invented phrase here'
    GROUND: FAIL
    EXIT=1

**Docstring wins**: state that a fence closes the current bullet and that fenced bullets count — or make the code skip them. Latent, not live: 7 of 61 `corpus/knowledge/*.md` have fences, 0 before `#### Inference`.

## H2 (high) — registry leg is bullet-scoped, not token-scoped — **docstring wins**

Clause 4 grounds a numeral that "appears in the title of a Registry row the bullet cites"; the code grounds a token when **any** designator of a cited title is a substring of the whole bullet (`:277-282`, `any(d in bullet …)`). Mutation of the **adopted** entry (copy in /tmp; true token count 7; appended to bullet 4: "and 4,137 such captures at 1846 repositories"):

    $ python3 cur.py --entry e1_mut.md --spans corpus/evidence/round46/spans.tsv \
        --counts /dev/null --registry corpus/SOURCES.md --root .
    GROUND entry=e1_mut.md section=1 bullets=4 tokens=9 grounded=9
    GROUND: PASS
    EXIT=0

Neither figure is in `spans.tsv`, `/dev/null` counts, or S079's title (`RFC 7089, HTTP Extension …`), so clause 4 refuses both. The leg is load-bearing, not decorative — both admitted entries fail without it:

    $ python3 tools/inference-ground.py --entry corpus/knowledge/evidence-pool-versioning-r39.md \
        --spans corpus/evidence/round46/spans.tsv --counts /dev/null --root .
    GROUND … bullets=4 tokens=7 grounded=6
    FINDING INF_TOKEN_NOT_IN_SPAN bullet=4 token='7089'
    GROUND: FAIL
    EXIT=1                      # amendment entry: bullet=3 token='7089', same shape

→ **docstring wins**: match the token (or its numeral) against the cited row's title/designators; never "a designator exists somewhere in the bullet".

## H3 (medium) — numeral extraction wrong in both directions — **docstring wins**

Clause 3: "a numeral of three or more digits, or a percentage"; `NUM_RE` (`:49`) is `\d[\d,]{2,}(?:\.\d+)?%?|\d+(?:\.\d+)?%`.

    $ python3 cur.py --entry dec.md …      # "The deposit reports 78.7 of the pool (`S901`)."
    GROUND entry=dec.md section=1 bullets=1 tokens=0 grounded=0
    FINDING INF_UNGROUNDED bullet=1 token=''
    EXIT=1
    $ python3 cur.py --entry bogus.md …    # "The pool holds 1,5 answers (`S901`)."
    GROUND … tokens=1 grounded=0
    FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='1,5'
    EXIT=1

`78.7` is a three-digit numeral and an exact `counts.json` value (`archive_share_percent: 78.7`) yet is invisible; `1,5` is not a numeral but is extracted, and `numeral_variants` maps it to `15`, so a mistyped `1,5` grounds whenever counts hold 15. **Docstring wins**: count digits across the decimal point, restrict commas to thousands groups.

## M1 (medium) — exit 2 is not implemented — **docstring wins**

    $ python3 cur.py --entry perm.md …     # chmod 000, is_file() true
    PermissionError: [Errno 13] Permission denied: 'perm.md'
    EXIT=1
    $ python3 cur.py --entry nope.md …     # missing
    inference-ground: no entry nope.md
    EXIT=2

Docstring `:32-33` and row cell 4 both promise exit `2` for "usage or a missing/unreadable entry": unreadable gives a traceback and 1, again scored as `JUNK_KILLED` by `c1-count.py:97-99`. A directory or unwritable `--json` path throws too, instead of "reads as empty". **Docstring wins**: catch the entry read and the `--json` write, one stderr line, exit 2.

## M2 (medium) — bullets=0: rule silent, answer changed — **docstring wins**

    $ python3 cur.py  --entry nobul.md …   # "#### Inference" then prose only
    GROUND … section=1 bullets=0 tokens=0 grounded=0
    FINDING INF_NO_BULLETS bullet=0 token=''
    GROUND: FAIL
    EXIT=1
    $ python3 head.py --entry nobul.md …
    GROUND … section=1 bullets=0 tokens=0 grounded=0
    GROUND: PASS
    EXIT=0

Clauses 2-4 are vacuous at zero bullets → PASS, as at the landing commit. `claims.md` is silent, no fixture exercises it, the row's code list omits `INF_NO_BULLETS`. **Docstring wins**: drop `:285-286`, or make it clause 5 plus a row code plus a fixture — a rule change after scoring, so it belongs in `corpus/lessons/round-46.md`, not a silent edit.

## L1 (low) — provenance sentence is false — **claims wins**

`:11` "Rule (the same sentence as `claims.md`, claim C1)" and `c1-count.py:4-5` repeat it. `claims.md:31-37` is a fixture-exit predicate with no numbered rule (`grep -n "cites at least one\|grounding token\|backticked"` matches only `:35`). **Claims wins**: say the tool *operationalises* what C1 scores.

## L2 (low) — claims class (b) contradicts clause 4 — **docstring wins**

`claims.md:35-36` "a cited bullet whose grounding token is absent from the cited span" would kill `positive-b.md`: its `5,959` is in neither span file and is grounded from `counts.json` (`answers_archived: 5959`), clause 4's counts escape. **Docstring wins**; prose fix only, predicate untouched.

## L3 (low) — row shows the registry as required, docstring as optional

Cell 3 has `--registry corpus/SOURCES.md` unbracketed; docstring `:29` brackets it; `argparse` defaults `None` (`:234`); `c1-count.py:60-63` never passes it, so C1's 3/3 exercises no registry leg — while omitting it fails both admitted entries (H2).

## L4 (low) — "in a span" = "anywhere in the named file"

`span_texts` (`:139-176`) reads the whole `span_file` and ignores the manifest's `quote` column, so clause 4 reads stricter than the code. No live false pass: `CAPTURE_BOUND=11/11` over slice-exact spans. **Docstring wins** (optional).

## Row cells to replace (`SKILL.md:116`)

Cell 3 — `python3 tools/inference-ground.py --entry PATH --spans TSV --counts JSON --registry corpus/SOURCES.md [--root DIR] [--json OUT] [--quiet]`

Cell 4 — `exit `0` grounded, no findings (`GROUND entry=… section={0,1} bullets=N tokens=N grounded=N`, `GROUND: PASS`) · exit `1` findings, zero or more `FINDING` lines, two for one bullet being normal and `bullet=0` for section-level findings (`INF_SECTION_ABSENT`/`INF_NO_BULLETS`/`INF_UNCITED`/`INF_UNGROUNDED`/`INF_TOKEN_NOT_IN_SPAN`) · exit `2` usage, a missing entry, or an entry that cannot be read (an unreadable `--spans`/`--counts`/`--registry` reads as empty and fails closed at exit `1`)`

Cell 5 — append: registry grounding is bullet-scoped (any digit-bearing token in a bullet that contains a cited row's designator is grounded), and two-digit decimals such as `78.7` are invisible while `1,5` is read as a numeral.

Cell 6 — `sha256 `3018b1d25d76…` in the measured after-state (`measure-after.txt`; the landing `d09fc8e` carries `819f83ebdc6c…`); span files named in the manifest must stay inside the manifest's directory; `--registry` is required in practice — omitting it fails both admitted round-46 entries (`INF_TOKEN_NOT_IN_SPAN 7089`)`

## Residual risk / gaps

- Not re-derived here (other seats): C2 census, C3 quote/span/capture binding, fixture pins (C1 passing implies all eight `PINNED` digests match).
- H1/H2/H3/M1 are invisible to C1's three fixtures; `C1=PASS` is no evidence against them.
- Only `.../w2/RevC1Line.md` written; mutated copies lived under `/tmp/chousa-r46w2-RevC1Line` (deleted). No network, no installs, pacman untouched, lane git/jj state untouched.

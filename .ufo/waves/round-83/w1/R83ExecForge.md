# R83ExecForge — C2 kill-rule K2 (spec generalization) battery

Seat: R83ExecForge (leaf). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Attacked revision: `81b81173f19d175e2b2a6b409b2a496d09d0b258` (tree `038256a22bada0aa0cb35f8e0206ad46a9baa80c`).
`tools/gate-records.py` sha256 `d38443769fe7c2ba014ec9d7861c4078cec24d0a193eeadb2cd5222d0d392687`.
Scratch tree: `/fast/scratch/hyaku/chousa-r83/R83ExecForge` (archive of the attacked revision; deleted before yield).
All receipts and all 91 forged files are in `.ufo/waves/round-83/w1/R83ExecForge/`; `pins.txt` there carries the pins.

Exact per-case command (run from the tree root):

```
cd <tree> && python3 tools/gate-records.py verify --root <tree> \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin forge/<file>
```

Aggregate command: `cd <tree> && python3 tools/gate-records.py verify --root <tree> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin forge/*.md` → `GATE_RECORDS files=91 records=88 ok=29 fail=59`, rc 1 (`aggregate-forge-run.txt`).

## Baseline (the claim's own predicate, measured, not assumed)

- Frozen counter `corpus/evidence/round83/gate-records-r83.py` on the attacked tree: `TOOL=present POSITIVE=15/15
  FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3`, `GATE_RECORDS_R83=PASS`, rc 0
  (`frozen-counter-run.txt`).
- Predicate (b) on the round-83 lesson at the tip (`aca2a781…:corpus/lessons/round-83.md`): `records=3 ok=3 fail=0`,
  rc 0 (`positives-round83.txt`).
- The 15 frozen positives: `records=15 ok=15 fail=0`, rc 0 (`positives-15.txt`).

So the tool is present, the frozen battery is refused, and the lane's own records pass. The findings below are
**new in-class lines the frozen 198 do not contain** (the battery mutates `words` by ±1 and `line` by ±1/far; it never
changes a numeral's spelling).

## Finding 1 — K2 FIRED: `line=2٢٢` is accepted as line 222

Exact bytes (`.ufo/waves/round-83/w1/R83ExecForge/forge/c052-line-arabic-222.md`, hex `line=2\xd9\xa2\xd9\xa2`):

```
GATE-RECORD S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=2٢٢ words=12 quote=the battery is fully forgeable through the payload channel on **both** batteries
```

Command and observed output:

```
$ cd <tree> && python3 tools/gate-records.py verify --root <tree> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin forge/c052-line-arabic-222.md
GATE_RECORD forge/c052-line-arabic-222.md:1 S199 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0
rc=0
```

Receipt: `cases.tsv` row 52 / `cases.json` id 52 / `forge/c052-line-arabic-222.md`; the same line is in the aggregate
run as `GATE_RECORD forge/c052-line-arabic-222.md:1 S199 OK`.

**Which docstring check it violates.** PARSE: the rev form is `line=<n>`, and `2٢٢` is not the decimal numeral 222 in a
single script — it is ASCII `2` followed by two ARABIC-INDIC DIGIT TWO (U+0662). The tool's own `INT_RE` is
`0|[1-9]\d{0,6}`: the `[1-9]` lead is ASCII, and `\d` is Python's Unicode-aware class, so the token is admitted; `check()`
then calls `int(kv["line"])`, and Python's `int()` silently reads `2٢٢` as 222 (`numeral-and-git-probes.txt`:
`token='2٢٢' fullmatch=True int=222`). The record's `line` field is therefore a value the documented form cannot express,
and the tool prints OK instead of PARSE. The control `line=222` (the genuine record, `genuine-rev`, id 81) prints OK as
well, so the two different tokens are silently the same line.

**In-class per claims.md K2.** Yes. The line's first text is `GATE-RECORD` (not a mention inside inline code, a list item,
a blockquote or a comment), it is a record line, and it violates the documented `line=<n>` value. The tool prints `OK`,
so K2 fires.

**The counter-reading and the mirror (this is the decisive part).** If `<n>` is read as "any numeral Python's `int()`
accepts", then `2٢٢` *is* 222 and no check is violated — but then the mirror case fires K3:

```
GATE-RECORD S209 … capture_sha256=8581ca1827f4ae13… words=2٠ quote="If changes are made, … final scoping review"
```

(hex `words=2\xd9\xa0`; `.ufo/…/forge/c026-words-arabic-trailing.md`). `INT_RE.fullmatch("2٠")` is True and
`int("2٠") == 20`, and the S209 quote has exactly 20 tokens (`numeral-and-git-probes.txt`), so under the numeric reading
the record meets every check; the tool nevertheless prints `GATE_RECORD forge/c026-words-arabic-trailing.md:1 S209 FAIL
WORDS`, rc 1, because `check()` compares `kv["words"] != str(n)` as **strings** (`str(20) != "2٠"`). The control
`words=20` (`words-arabic-trailing-control`, id 87) prints OK.

The docstring uses one placeholder `<n>` for both `line` and `words`. There is no single reading of `<n>` under which both
behaviours are correct: the ASCII reading makes `line=2٢٢` a K2 fire; the numeric reading makes `words=2٠` a K3 fire.
The two lines differ only in which field carries the Unicode digit, and the tool handles the two fields inconsistently
(`int()` for `line`, string equality for `words`). C2 is falsified under either reading; this seat reports the K2 branch
(the ASCII reading, which the `[1-9]` lead of `INT_RE` implies) as the fire and the K3 branch as the mirror.

## Finding 2 — K3 harm candidates (refusals of lines that meet every check)

K3 is the harm rule; these are listed because the assignment asks for every line that meets every check but is refused.
They do not fire K2 (the tool prints FAIL), but any of them falsifies C2 under K3 if the L1 accepts the reading.

**H1 (strongest): a rev quote whose text begins with `"` is refused as PARSE.** The rev form documents
`quote=<text to end of line>`; nothing forbids the text starting with a double quote. `parse()` has, verbatim:

```
        quote = qraw.rstrip()
        if not quote or quote.startswith('"'):
            return None
```

```
$ … forge/c057-rev-quote-leading-dquote.md
GATE_RECORD forge/c057-rev-quote-leading-dquote.md:1 S199 FAIL PARSE
rc=1
```

Exact bytes: `GATE-RECORD S199 rev=81b81173f19d175e2b2a6b409b2a496d09d0b258 path=tools/gate-records.py line=8 words=2
quote="Location command".` — rev is a commit, the path is a blob at that rev, line 8 is in range and contains
`"Location command".`, and `words=2` matches. The control `rev-dquote-control` (id 85, identical but
`quote=Location command".`, no leading quote) prints `S199 OK`, rc 0. The only difference is the leading `"`.

**H2: `words=2٠` (the mirror above).** Under the numeric reading of `<n>`, the record meets every check and is refused as
WORDS (id 26, rc 1).

**H3: an upper-case or mixed-case 40-hex `rev` is refused.** `HEX40_RE = [0-9a-f]{40}`; git itself resolves the
upper-case id to the commit: `git cat-file -t B7803829922770B890E9F4EFDD30D12C3695439A^{commit}` → `commit`, rc 0
(`numeral-and-git-probes.txt`). The docstring says `rev=<40 hex>`; upper-case hex is hex. Observed:
`GATE_RECORD forge/c043-rev-upper.md:1 S199 FAIL LINE,REV`, rc 1 (id 43), and the mixed-case variant id 44. Weaker than
H1 because the docstring's `SHA_RE` for `capture_sha256` is lower-case-only, which suggests the lane's convention is
lower-case hex.

**H4: `line=011` and `words=+20` are refused as PARSE** (ids 51, 25). `<n>` with a leading zero or a plus sign is a
decimal numeral by the usual reading; `INT_RE` refuses both. Weak: `INT_RE` is a defensible reading of `<n>`.

**H5: two spaces or a tab between keys is refused as PARSE** (ids 70, 71). The class sentence says `GATE-RECORD` is
"followed by whitespace"; the form block shows single spaces, and `head.split(" ")` rejects any other whitespace
between keys. Weak.

**H6: a tab after `GATE-RECORD` is refused as PARSE** (id 69). `REC_RE` puts the line in class (`\s`), then `parse()`
requires a literal space, so an in-class line is refused. Weak.

**H7: an upper-case `capture_sha256` prefix is refused as CAPTURE_SHA** (ids 1, 2). Defensible: the prefix of the
lower-case hex string genuinely fails; listed only for completeness.

## Finding 3 — secondary K2 candidate (weaker): the `...` suffix

`capture_sha256=8581ca1827f4ae13...` (three ASCII dots) prints `S209 OK`, rc 0 (id 3,
`forge/c003-sha-dots3.md`). The docstring's syntax block writes `capture_sha256=<>=16 hex>[…]` — the optional suffix is
shown as the single character `…` — while `SHA_RE` is `([0-9a-f]{16,64})(?:…|\.\.\.)?`, i.e. the code deliberately
accepts `...` as well. Under a strict reading of the syntax block this is extra text and PARSE should fire; under the
reading that the code's regex is the intended language (the docstring's `[…]` is shorthand) it is documented. This is a
docstring/code divergence, not as clean as Finding 1; reported as a candidate, not a second fire.

## Residuals (out of class — listed separately, not counted as fires)

- **Class ambiguity: a record line inside a multi-line HTML comment.** `forge/c076-html-comment-block.md` is
  `<!--` / the genuine S209 record / `-->`; the tool prints `GATE_RECORD forge/c076-html-comment-block.md:2 S209 OK`,
  rc 0. claims.md's frozen class says "Mentions inside inline code, list items, blockquotes or HTML comments are prose,
  not records, and are out of class", which would make this file have **no in-class record**, so the tool's exit 0 would
  be a K4 ("exits 0 on input with no in-class record") violation. The tool's own docstring says the opposite for a line
  whose *first text* is `GATE-RECORD` ("such a line is checked, never skipped"), and its second sentence speaks of a
  mention "elsewhere in a line". The tool follows its docstring; the claims.md compression is broader. The two class
  definitions disagree; I record the input and the output, and do not count it as a fire. The single-line controls
  `<!-- GATE-RECORD … -->`, `- GATE-RECORD …` and `` `GATE-RECORD …` `` are correctly not in class (rc 1, no
  GATE_RECORD line; ids 88–90).
- **`rev` is peeled with `^{commit}`.** `git_blob()` runs `git cat-file -t <rev>^{commit}`, so a 40-hex **annotated-tag
  object** would pass REV though it is not a commit. The lane has no tag objects at the attacked revision:
  `git cat-file --batch-all-objects --batch-check` → 18694 blob, 1806 commit, 8862 tree, 0 tag. No lane line can
  exploit it today; out of class (no lane bytes).
- **`CAPTURE_PATH` via a symlinked `corpus/captures` directory or a hardlink.** `check()` compares
  `dirname(realpath(cap))` with `realpath(root/corpus/captures)`, so a capture reached through a symlinked directory
  would pass, and a hardlink is not `islink`. The lane's `corpus/captures` is a real directory, all 77 captures are
  regular files, none is a symlink and none has `nlink > 1`; no lane instance.
- **`errors="replace"` when reading captures.** A quote containing U+FFFD would match invalid UTF-8 bytes. All 77 lane
  captures decode as valid UTF-8; no lane instance.
- **The failed-attempt refetch probe with a fixture capture.** `forge/c091-refetch-failed-url-fixture.md` uses S208's
  url (whose only refetch row is the failed attempt, rc 22/403) with a capture file this seat wrote into the scratch
  tree. The tool prints `S209 FAIL REFETCH`, rc 1 — the failed-attempt row is refused even when the capture is valid —
  but the capture is not lane bytes, so the line is not a K2 subject. The lane-grounded variant (id 12, S208's url with
  S009's capture) prints `CAPTURE_KEY,REFETCH`.

## Non-findings (tool prints OK and no check is violated)

- `sha-full64`, `sha-full64-ellipsis`, `sha-24hex`: a ≥16-hex prefix of the capture sha (ids 4, 5, 8).
- `decision=reject` in the url/admit form (id 22): the form documents `decision=<admit|reject>`.
- `quote-nbsp`, `quote-tab`, `quote-curly-apostrophe`, `quote-linebreak` (ids 29, 30, 33, 36): the documented
  normalization is `str.split` whitespace plus U+2018/2019/201C/201D folding, so these are genuine.
- `quote-entity-genuine` (id 35): the capture has a literal `&`; the entity variant (id 34) is correctly QUOTE_ABSENT.
- `crlf`, `bom`, `zwsp-prefix` (ids 60–62): universal newlines and the documented Cf strip.
- `dup-id-lines` (id 67): no check forbids a repeated id; both lines print OK, rc 0.
- `path=./corpus/…` (id 46): git resolves `./` to the blob (`cat-file -t` → `blob`, rc 0), and `./x` is still a
  repo-relative path, so REV is not violated. My pre-run expectation of REV was wrong; the observation is recorded.
- Genuine controls: ids 28, 32, 59, 80–85, 87.

## Exit contract (K4) status

Holds on every input I tried: empty file rc 1; prose-only rc 1; `GATE-RECORD` bare rc 1 (FAIL PARSE); one OK + one FAIL
rc 1 with both lines printed (id 79); missing FILE rc 2; missing registry rc 2; no input produced rc 0 together with a
FAIL line (`exit-contract-probes.txt`, `cases.tsv`). The only exit-0-on-no-in-class-record candidate is the HTML-comment
class ambiguity above, which turns on which class definition is adopted.

## Case table (91 forged files; exact bytes in `forge/`, `cases.tsv`, `cases.json`)

| id | case | check targeted | tool output | rc | classification |
|---|---|---|---|---|---|
| 1 | sha-upper16 | CAPTURE_SHA | `S209 FAIL CAPTURE_SHA` | 1 | K3 candidate (weak, refused) |
| 2 | sha-mixed16 | CAPTURE_SHA | `S209 FAIL CAPTURE_SHA` | 1 | K3 candidate (weak, refused) |
| 3 | sha-dots3 | CAPTURE_SHA | `S209 OK` | 0 | K2 candidate (weak): `...` suffix accepted |
| 4 | sha-full64 | CAPTURE_SHA | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 5 | sha-full64-ellipsis | CAPTURE_SHA | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 6 | sha-raw16 | CAPTURE_SHA | `S209 FAIL CAPTURE_SHA` | 1 | refused as documented |
| 7 | sha-15hex | CAPTURE_SHA | `S209 FAIL CAPTURE_SHA` | 1 | refused as documented |
| 8 | sha-24hex | CAPTURE_SHA | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 9 | sha-suffix-x | CAPTURE_SHA | `S209 FAIL CAPTURE_SHA` | 1 | refused as documented |
| 10 | refetch-diff-id-admit | REFETCH | `S210 FAIL REFETCH` | 1 | refused as documented |
| 11 | refetch-diff-id-unreach | REFETCH | `S207 FAIL REFETCH` | 1 | refused as documented |
| 12 | refetch-failed-url-lane | REFETCH | `S209 FAIL CAPTURE_KEY,REFETCH` | 1 | refused as documented |
| 13 | refetch-failed-attempt-time | REFETCH | `S209 FAIL REFETCH` | 1 | refused as documented |
| 14 | url-trailing-slash | CAPTURE_KEY | `S209 FAIL CAPTURE_KEY,REFETCH` | 1 | refused as documented |
| 15 | url-fragment | CAPTURE_KEY | `S209 FAIL CAPTURE_KEY,REFETCH` | 1 | refused as documented |
| 16 | url-http | CAPTURE_KEY | `S209 FAIL CAPTURE_KEY,REFETCH` | 1 | refused as documented |
| 17 | url-upper-scheme | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 18 | tier-lower | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 19 | tier-D | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 20 | decision-maybe | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 21 | decision-ADMIT | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 22 | decision-reject-admit-form | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 23 | tier-missing | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 24 | words-leading-zero | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 25 | words-plus | PARSE | `S209 FAIL PARSE` | 1 | K3 candidate (weak, refused) |
| 26 | words-arabic-trailing | WORDS | `S209 FAIL WORDS` | 1 | **K3 harm candidate** (refused) |
| 27 | words-arabic-leading | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 28 | words-genuine | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 29 | quote-nbsp | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 30 | quote-tab | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 31 | quote-zwsp | QUOTE_ABSENT | `S209 FAIL QUOTE_ABSENT` | 1 | refused as documented |
| 32 | quote-straight-apostrophe | none | `S212 OK` | 0 | accepted / genuine control; no check violated |
| 33 | quote-curly-apostrophe | none | `S212 OK` | 0 | accepted / genuine control; no check violated |
| 34 | quote-entity | QUOTE_ABSENT | `S212 FAIL QUOTE_ABSENT` | 1 | refused as documented |
| 35 | quote-entity-genuine | none | `S212 OK` | 0 | accepted / genuine control; no check violated |
| 36 | quote-linebreak | none | `S212 OK` | 0 | accepted / genuine control; no check violated |
| 37 | quote-other-capture | QUOTE_ABSENT | `S209 FAIL QUOTE_ABSENT` | 1 | refused as documented |
| 38 | quote-case | QUOTE_ABSENT | `S209 FAIL QUOTE_ABSENT` | 1 | refused as documented |
| 39 | rev-short12 | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 40 | rev-tag-name | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 41 | rev-HEAD | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 42 | rev-tree | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 43 | rev-upper | REV | `S199 FAIL LINE,REV` | 1 | **K3 harm candidate** (refused) |
| 44 | rev-mixed | REV | `S199 FAIL LINE,REV` | 1 | **K3 harm candidate** (refused) |
| 45 | path-dotdot | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 46 | path-dot-slash | REV | `S199 OK` | 0 | accepted / genuine control; no check violated |
| 47 | path-trailing-slash | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 48 | path-absolute | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 49 | line-zero | PARSE | `S199 FAIL PARSE` | 1 | refused as documented |
| 50 | line-00 | PARSE | `S199 FAIL PARSE` | 1 | refused as documented |
| 51 | line-011 | PARSE | `S199 FAIL PARSE` | 1 | K3 candidate (weak, refused) |
| 52 | line-arabic-222 | PARSE | `S199 OK` | 0 | **K2 FIRED** (OK on a bad `line=<n>`) |
| 53 | line-arabic-223 | LINE | `S199 FAIL LINE` | 1 | refused as documented |
| 54 | line-plus | PARSE | `S199 FAIL PARSE` | 1 | refused as documented |
| 55 | line-minus | PARSE | `S199 FAIL PARSE` | 1 | refused as documented |
| 56 | line-arabic-only | PARSE | `S199 FAIL PARSE` | 1 | refused as documented |
| 57 | rev-quote-leading-dquote | PARSE | `S199 FAIL PARSE` | 1 | **K3 harm candidate** (refused) |
| 58 | rev-words-arabic | WORDS | `S199 FAIL WORDS` | 1 | refused as documented |
| 59 | rev-genuine-control | none | `S199 OK` | 0 | accepted / genuine control; no check violated |
| 60 | crlf | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 61 | bom | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 62 | zwsp-prefix | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 63 | zwsp-inside-key | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 64 | second-quote-key | QUOTE_ABSENT | `S209 FAIL QUOTE_ABSENT,WORDS` | 1 | refused as documented |
| 65 | keys-after-quote | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 66 | keys-after-quote-quoted | QUOTE_ABSENT | `S209 FAIL QUOTE_ABSENT,WORDS` | 1 | refused as documented |
| 67 | dup-id-lines | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 68 | extra-key | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 69 | tab-after-gate-record | PARSE | `S209 FAIL PARSE` | 1 | K3 candidate (weak, refused) |
| 70 | double-space-keys | PARSE | `S209 FAIL PARSE` | 1 | K3 candidate (weak, refused) |
| 71 | tab-between-keys | PARSE | `S209 FAIL PARSE` | 1 | K3 candidate (weak, refused) |
| 72 | quote-key-first | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 73 | capture-none-admit | CAPTURE_PATH | `S209 FAIL CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH` | 1 | refused as documented |
| 74 | sha-empty | PARSE | `S209 FAIL PARSE` | 1 | refused as documented |
| 75 | bare-gate-record | PARSE | `? FAIL PARSE` | 1 | refused as documented |
| 76 | html-comment-block | class | `S209 OK` | 0 | residual: class ambiguity (K4 candidate under claims.md class) |
| 77 | prose-only | class | `(no GATE_RECORD line)` | 1 | no in-class record, rc 1 (correct) |
| 78 | empty | class | `(no GATE_RECORD line)` | 1 | no in-class record, rc 1 (correct) |
| 79 | mixed-ok-fail | exit | `S209 OK` | 1 | exit contract: rc 1, one OK + one FAIL printed (correct) |
| 80 | genuine-admit | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 81 | genuine-rev | none | `S199 OK` | 0 | accepted / genuine control; no check violated |
| 82 | genuine-unreach | none | `S208 OK` | 0 | accepted / genuine control; no check violated |
| 83 | genuine-s009 | none | `S009 OK` | 0 | accepted / genuine control; no check violated |
| 84 | genuine-s212 | none | `S212 OK` | 0 | accepted / genuine control; no check violated |
| 85 | rev-dquote-control | none | `S199 OK` | 0 | accepted / genuine control; no check violated |
| 86 | rev-blob | REV | `S199 FAIL LINE,REV` | 1 | refused as documented |
| 87 | words-arabic-trailing-control | none | `S209 OK` | 0 | accepted / genuine control; no check violated |
| 88 | html-comment-inline | class | `(no GATE_RECORD line)` | 1 | no in-class record, rc 1 (correct) |
| 89 | list-item | class | `(no GATE_RECORD line)` | 1 | no in-class record, rc 1 (correct) |
| 90 | inline-code | class | `(no GATE_RECORD line)` | 1 | no in-class record, rc 1 (correct) |
| 91 | refetch-failed-url-fixture | REFETCH | `S209 FAIL REFETCH` | 1 | refused; fixture capture (not lane bytes) — behaviour probe |

## Files changed

None in the lane. This seat wrote only:

- `.ufo/waves/round-83/w1/R83ExecForge.md` (this report)
- `.ufo/waves/round-83/w1/R83ExecForge/` — `forge/` (91 forged files), `cases.tsv`, `cases.json`, `driver.py`,
  `aggregate-forge-run.txt`, `positives-15.txt`, `positives-round83.txt`, `exit-contract-probes.txt`,
  `numeral-and-git-probes.txt`, `frozen-counter-run.txt`, `pins.txt`, `round-83-tip.md`
- scratch `/fast/scratch/hyaku/chousa-r83/R83ExecForge` (deleted before yield)

No lane git/jj mutation, no production edits, no network, no tool installs.

## Risks / blockers

- The fire turns on the reading of `<n>`; the mirror K3 (`words=2٠`) is stated so the L1 can decide which rule fires.
  Under either reading C2 is falsified: the two fields are handled inconsistently (`int()` for `line`, string equality
  for `words`).
- The `...` suffix (Finding 3) and the HTML-comment class boundary are reported as a candidate and a residual, not as
  fires.
- The tag-object peel and the symlink/hardlink/U+FFFD residuals have no lane instance at the attacked revision; they are
  recorded so a later round can test them if the lane ever gains a tag object or a non-regular capture.
- No blocker prevented the assigned work; the scratch tree is removed and every cited receipt is copied into the wave
  output folder.

VERDICT: R83ExecForge C2 fired — the landed tool prints `OK` on `line=2٢٢` (a mixed ASCII/Arabic-Indic numeral it silently converts to 222), violating the documented `line=<n>` value, and its mirror `words=2٠` is refused under the same numeral reading, so one of K2/K3 must fire.
VERDICT: R83ExecForge C1 n/a — this seat attacked only the C2 tool; no C1 entry, counter or capture was measured.

# R52DraftQuality — QUALITY.md criteria 87–89 (chousa round 52, wave 1)

seat: `R52DraftQuality` (scribe; leaf, no dispatch)
item: draft `corpus/QUALITY.md` criteria 87–89, append-only, in the shape of 81–86
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`; tip measured `13bc28063b4bd7ea2e521167413ee9829202a420`
frozen claims: `37468eadd8d098e80289b2f31a22de3872d4a1f6` (`claims.md` blob `8bb5d3ef…` = working tree, `sha256sum` equal)
base: `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`; C1 candidate `804a45370dc992bfe714817281535055c2f9b032` (both ancestors of the tip)
tools measured: `corpus/evidence/round52/c1-count.py` blob `1a389852…` (unchanged `37468ea..HEAD`), `tools/capture-text.py` blob `07401e12…`
scratch: `/fast/scratch/hyaku/chousa-r52/R52DraftQuality` (TMPDIR; removed on exit); installs: none

## 1. Checks run (read-only; every number below is from one of these)

| # | command | observed |
|---|---|---|
| 1 | `sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw` | `16fc8c55ee856fef…adeb09763`, equals `REAL_SHA` at `c1-count.py:47` |
| 2 | `python3 tools/capture-text.py <raw> --locate 'SRにおける文献検索期間について明記する'` | `LOCATED count=1 offset=8996`, rc 0 |
| 3 | `python3 tools/capture-text.py <raw> \| python3 -c 'import sys;t=sys.stdin.read();print(len(t),t.count(chr(9)),t.count(chr(10)))'` and a 2-line `find`/`count` probe on the same text | form `19682` chars, `49` tabs, `1239` newlines; `text.find` = `8996`, `count` = 1 |
| 4 | `.txt` sidecar probe (Python) | `319599` bytes, `equal=True` to `raw.decode("utf-8","replace").encode("utf-8")`, first bytes `PK\x03\x04`, binary decode `168953` chars, text mode `168952` (`cr=609 crlf=1`), `U+FFFD=72117`, phrase occurrences `0` |
| 5 | element counts in `word/document.xml` (zipfile + regex) | `w:instrText` open 50 / close 50; `mc:Fallback` 60 / 60; `w:delText` 0; `w:tabs` 13; tab stop `<w:tab w:` 13; bare `<w:tab/>` 49; `<w:br` 20; `<w:cr` 0; `</w:p>` 1238 |
| 6 | `python3 corpus/evidence/round52/c1-count.py --seed 52` | `LEGS=9/9`, `C1=PASS`, rc 0, `REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682`, 1.4 s |
| 7 | `python3 corpus/evidence/round52/c1-count.py --tool …/controls/naive-tool.py` (fresh nonce) | `PARAS=PASS RUNS_ENTITIES=PASS REVISIONS=FAIL(text differs at 7) LAYOUT=FAIL(at 0) ALTCONTENT=FAIL(at 41) MAIN_PART=FAIL(at 0) LOCATE=PASS REFUSE=FAIL(norel not refused) REAL=PASS chars=21910`, `LEGS=4/9`, rc 1 |
| 8 | `python3 corpus/evidence/round52/c1-count.py --tool …/controls/cache-txt-tool.py --seed 52` | `REAL=FAIL rc=0 count=0 locate=(1, 0, -1) chars=168953`, `LEGS=0/9`, rc 1 |
| 9 | `grep -nE '"d1"\|"d2"\|renamed-heading\|out\.parent\.name\|--out' corpus/evidence/round52/c1-count.py` | no output, rc 1; the same pattern on `corpus/evidence/round51/c1-count.py` prints `81,167,174,189` |
| 10 | argv probe: a 6-line wrapper writes `sys.argv[1:]` to `$ARGV_LOG`, then `os.execv`s `naive-tool.py`; `c1-count.py --tool <wrapper> --per-leg 1 --seed 52` | `calls=14`, `12` scratch paths (`10` distinct names) in one directory `c1r52-_f_bxgn9`, `2` calls name the pinned capture, extensions `['', '.bin', '.docx', '.raw']`; no leg name in any path |
| 11 | `git diff --stat HEAD -- corpus/evidence/round52 tools` | empty at measurement time (measured blobs = committed blobs; see the drift note in §3) |
| 12 | `python3 corpus/evidence/round29/prose-check.py <draft>` | `digit-glued tokens: 1` (`round52`, a path, line 34), `custody vocabulary: 0`; baseline `corpus/QUALITY.md` at the tip carries `TOTAL hits=23` (incl. `round51 x3` path hits), so a path token is the existing 81–86 shape |

Citations used by the draft, opened: `corpus/lessons/round-51.md:55` (NIPH `.txt` "168952 characters, 72117 of them
U+FFFD … 0 times"), `:57` (refused "for its capture form"), `corpus/evidence/round51/controls/c1-supplement-controls.txt:77-82`
(`forge-dirname` → `LEGS=5/5 C1=PASS`), `corpus/evidence/round51/controls/forge-dirname.py:30` (`scene = out.parent.name`),
`corpus/lessons/round-51-verifier-spotcheck.md` §6 defects 1 and 3.

Reconciliation of the one number that differs from round 51: the lesson says the sidecar is `168952` characters, my binary
decode gives `168953`. The file holds one CRLF (`cr=609 crlf=1`); text-mode read collapses it → `168952`. Both counts are of
the same bytes; the criterion states the form of each.

## 2. Draft — append to `corpus/QUALITY.md` after line 915 (nothing above is edited)

```markdown
## Round-52 additions (appended 2026-10-26; criteria 1–86 unchanged)

87. **A capture is read through its text form before a quote is located in it or the source is refused for its
    capture form.** Round 51 refused the NIPH `.docx` because neither text form the lane read (the cache `.txt` as
    UTF-8, the `.raw` as UTF-16LE) contains one of its phrases, though the phrases sit in the DEFLATE member
    `word/document.xml` (`corpus/lessons/round-51.md:55,57`; round-51 spot-check routed defect 3). The cache's
    `.txt` for that capture is the container's bytes decoded `errors="replace"` and re-encoded — `319599` bytes,
    equal to `raw.decode("utf-8","replace").encode()`, with first bytes `PK\x03\x04` — `168953` characters in a
    binary decode (`168952` in text mode: one CRLF), `72117` of them U+FFFD, and the phrase
    `SRにおける文献検索期間について明記する` occurs `0` times in it. `tools/capture-text.py` states the form
    (`19682` characters) and locates that phrase once at offset `8996`. Check:
    `python3 tools/capture-text.py <raw> --locate '<quote>'` — `LOCATED count=1 offset=8996` exit 0; a sidecar
    that holds U+FFFD, or whose first bytes are a container signature (`PK\x03\x04` for zip, `\xd0\xcf\x11\xe0`
    for OLE), is not a text form, and no count or offset taken in it is evidence. Shown able to fail
    (`corpus/evidence/round52/controls/c1-before.txt`): `controls/cache-txt-tool.py`, which reads the `.txt`
    sidecar as the text form, prints `LEGS=0/9 C1=FAIL` exit 1 with `REAL=FAIL … count=0 … chars=168953`, and
    the sidecar itself holds the phrase `0` times. Named limits: the form is defined for OOXML only — an OLE
    `.doc` or a PDF capture needs its own form and this criterion does not supply one; offsets are code points
    in the printed form, not bytes, and the same sidecar counts one character fewer in text mode than in a
    binary decode; neither signature test fires on a `.txt` that decoded losslessly and is the right reading. —
    `corpus/lessons/round-52.md` `## Mistakes` row 1; `corpus/evidence/round52/claims.md` R52-C1;
    `corpus/lessons/round-51-verifier-spotcheck.md` §6 defect 3.

88. **A capability counter hands its tool no name that names the test.** The frozen round-51 counter named its
    subtests `s`, `d1`, `d2`, `renamed-heading` and passed an output directory, so a 94-line tool that read
    `out.parent.name` and printed canned shapes passed it `LEGS=5/5`
    (`corpus/evidence/round51/controls/forge-dirname.py`; `controls/c1-supplement-controls.txt:77-82`;
    round-51 spot-check routed defect 1). The round-52 counter draws its scratch directory from
    `tempfile.mkdtemp` (`corpus/evidence/round52/c1-count.py:258`), each package's file name and extension
    (`:262-263`) and the main-part member name (`:202`) from its own randomness, and hands the tool only `RAW`
    or `--locate` (`call` `:213`); observed through a wrapper that logs argv, `14` calls name `10` distinct
    files in one random directory, with extensions `.raw`, `.docx`, `.bin` and none, and `2` calls name the
    pinned capture. Check: `grep -nE '"d1"|"d2"|renamed-heading|out\.parent\.name|--out'
    corpus/evidence/round52/c1-count.py` exits 1 with no output, while the same pattern on
    `corpus/evidence/round51/c1-count.py` prints lines `81,167,174,189` (its `--out` argument and its three
    fixed subtest names); `python3 corpus/evidence/round52/c1-count.py --seed N` exits 0 `LEGS=9/9 C1=PASS`.
    Shown able to fail: the round-51 receipt above (`LEGS=5/5 C1=PASS` for a tool that implements none of the
    behaviour), and at the round-52 counter the one fixed member a key can name is killed by `MAIN_PART` —
    `corpus/evidence/round52/controls/naive-tool.py` (fixed member `word/document.xml`) prints
    `MAIN_PART=FAIL text differs at 0` and `LEGS=4/9`. Named limits: a tool keyed on the `c1r52-` scratch
    prefix or on the pinned capture's path learns "generated" or "the pinned capture" and no expected text; a
    tool that reimplements the thing passes by definition; the OOXML-mandated members (`[Content_Types].xml`,
    `_rels/.rels`, `docProps/core.xml`, the default main part `word/document.xml`) are fixed in every leg by
    the format, so this rule forbids a name that varies by leg, not a name the input format fixes. —
    `corpus/lessons/round-52.md` `## Mistakes` row 2; `corpus/evidence/round52/claims.md` R52-C1.

89. **A `.docx` text form drops `mc:Fallback`, `w:delText`, `w:instrText` and the tab stops of
    `w:pPr/w:tabs`, and emits a tab, or a newline beyond the one at each `w:p` end, only for a run-level `w:tab`,
    `w:br` or `w:cr`.** A member-strip
    reading is not a text form: on the real NIPH main part it keeps `50` `w:instrText` elements (`100` tags,
    `TOC` and `PAGEREF` field codes), `60` `mc:Fallback` containers (`120` tags) and `13` `w:tab` stops in `13`
    `w:tabs` blocks, so it prints `21910` characters where the defined form prints `19682` (`49` tabs, `1239`
    newlines). Check: `python3 corpus/evidence/round52/c1-count.py` — the `REVISIONS`, `LAYOUT` and
    `ALTCONTENT` legs generate the shapes at counting time, and every package draws each sub-kind at least
    once: deleted text beside its insertion and a field instruction beside its result, run-level tabs and
    breaks beside a `w:pPr/w:tabs` block, and an `mc:Fallback` duplicate of an `mc:Choice`, so one extra tab,
    break, field path or Fallback copy fails the leg. Shown able to fail
    (`corpus/evidence/round52/controls/c1-before.txt`): `corpus/evidence/round52/controls/naive-tool.py`
    prints `REVISIONS=FAIL`, `LAYOUT=FAIL`, `ALTCONTENT=FAIL` and `LEGS=4/9`, against `LEGS=9/9` for
    `tools/capture-text.py`; re-run at the tip the same three legs differ at offset `7`, `0` and `41` of
    packages drawn that run, so the offsets move and the leg verdicts do not. Named limits: a form that drops
    the right elements and misplaces a newline in a shape no leg draws is not caught; `w:delText` occurs `0`
    times in the NIPH capture, so the real capture exercises three of the four rules and the `REVISIONS` leg
    supplies the fourth; the legs hold the shape count per package, not the number of packages beyond
    `--per-leg`. — `corpus/lessons/round-52.md` `## Mistakes` row 1; `corpus/evidence/round52/claims.md`
    R52-C1; `corpus/lessons/round-51-verifier-spotcheck.md` §6 defect 3.
```

Integration notes for the L1, not part of the draft:

- `corpus/lessons/round-52.md` does **not** exist at the tip (`read` fails; `corpus/lessons/` ends at `round-51.md`), so the
  row numbers above are the planned rows from the wave spec: row 1 = capture form (NIPH refusal, naive member-strip), row 2 =
  attribution/vacuous (round-51 fixed directory names). Confirm the rows land with those numbers, or renumber at append.
- Criteria 87 and 89 share row 1 because the Mistakes item (1) asks for both the refusal and the naive-strip counts; 88 cites
  row 2 only.
- The `Shown able to fail` parentheticals cite `controls/<file>` relative to the evidence directory named at the start of
  the same sentence (`round52` in 87 and 89, `round51` in 88), the shape criteria 80–86 use; the absolute path follows where
  the sentence needs it.

## 3. Observations for the judge (not claims I was asked to make)

1. **The REAL leg does not discriminate the cheap reading.** `naive-tool.py` passes `REAL` (`count=1`, `chars=21910`) and
   `LOCATE`, `PARAS`, `RUNS_ENTITIES`; the legs that separate it are `REVISIONS`, `LAYOUT`, `ALTCONTENT`, `MAIN_PART`,
   `REFUSE` (check 7). A leakage claim resting on the pinned capture alone would be wrong.
2. **A fixed name still exists inside six legs.** the six generated-shape legs use the default main part `word/document.xml`
   (`c1-count.py:205,291,307`); only `MAIN_PART` draws a random member and plants a `word/document.xml` decoy. Criterion 88 is
   therefore drafted to forbid *leg-varying* names, not format-mandated ones — the naive tool's `MAIN_PART=FAIL` is the proof
   that the decoy works.
3. **Two fixed strings remain visible to the tool**: the `c1r52-` mkdtemp prefix and the pinned `.qcache` path (check 10).
   Neither names a leg; a tool keyed on them can win `REAL` only.
4. **The `.txt` sidecar is a re-encode, not raw bytes**: `319599` bytes = `raw.decode("utf-8","replace").encode("utf-8")`
   exactly, first bytes `PK\x03\x04` (check 4), which is why the container signature survives into it.
5. **Form counts differ from element counts**: `1239` newlines against `1238` `</w:p>` + `20` `w:br` + `0` `w:cr`, because
   `19` of the `w:br` sit inside `mc:Fallback` copies. The criterion states measured form values only and does not derive
   the newline count.
6. `w:delText` is absent from the real capture (check 5); only the `REVISIONS` leg exercises that rule.
7. **Tree drift after my measurements:** a sibling seat then modified `tools/capture-text.py` (` M` in `git status`;
   working blob `3bcccac…`, adding a root-not-`w:document` refusal and `el.clear()`), and added
   `corpus/evidence/round52/c1-supplement.py` plus `controls/forge-shape.py`. My numbers are of blob `07401e12…` =
   `HEAD:tools/capture-text.py` = the C1 candidate's blob, and the drift does not move them: the text form is
   byte-identical between the two blobs (`python3 <HEAD blob> <raw> | sha256sum` = `python3 tools/capture-text.py <raw>
   | sha256sum` = `754aae42…`), and `c1-count.py --seed 52` against the drifted tool still prints `LEGS=9/9 C1=PASS`,
   `REAL=PASS … chars=19682`. `corpus/QUALITY.md`, `corpus/evidence/round52/claims.md` and `c1-count.py` are unchanged.

## 4. Not done / out of scope

- No production file edited by this seat: `git status --porcelain corpus/QUALITY.md corpus/evidence/round52/claims.md
  corpus/evidence/round52/c1-count.py` is empty; the sibling edits named in §3.7 are not mine. Draft text is above;
  integration is the L1's.
- `c2-count.py`, `build-spans.py` and the lane gate were not run (not this item; the counters were not modified).
- No commit, no jj, no gate, no fetch, no install. Scratch removed after the receipts above were copied here.

VERDICT: built the 87–89 append draft on checks I ran — NIPH form `19682` chars at `--locate` offset `8996` against a sidecar of `72117` U+FFFD and `0` phrase occurrences, the counter's name draws with no leg name in any argv (`LEGS=9/9`), and the member-strip failure (`4/9`) — attacking nothing in the frozen claim; unverified: the `round-52.md` Mistakes row numbers, because that file does not exist yet.

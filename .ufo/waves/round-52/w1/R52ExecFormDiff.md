# R52ExecFormDiff — differential of the two round-52 `.docx` readers

seat R52ExecFormDiff (leaf, chousa round 52 w1) · 2026-10-26 · lane head `13bc280`; claims frozen at `37468ea`
(the only commit touching `claims.md`); C1 tool `tools/capture-text.py` at `804a453`, unmodified at HEAD
(`git diff --stat 37468ea…HEAD` → `tools/capture-text.py | 115 +++` only). No install, no pacman, no network.
Scratch `/fast/scratch/hyaku/chousa-r52/R52ExecFormDiff/`, removed at exit. Wrote only this file.
Axes: **operability** (does the C1 tool's text form match C2's own reader, and does each refuse where the rule says refuse) and **depth** (where can two implementations of one rule diverge on a producible document).

## 1. Selection (computed, not assumed)

```console
$ # magic sniff, not extension:
$ python3 -c '… for p in sorted(C.glob("*.raw")): if p.open("rb").read(4)==b"PK\x03\x04": zips…'
zip raws: 8
3a8b45977cd111e45e3980a5 178056   68a1f5a90ad0edb9e9839840 5606635   6fef2cd89a58578c656ed44f 67697
9990f37099e6b98e68f1ecb0 2441966  b825f17cafd08636a278e6c1 242116    bcaebc1a0c6244100bd90d6c 6521217
cb101e95f5f5e98d019eeca1 35134     e9761e99ba404f708f97c4eb 47273
```

Composition from `namelist()` + `_rels/.rels`: **2 WordprocessingML** (`3a8b…`, `b825…`), **2 SpreadsheetML**
(`cb101e…`, `e9761e…` → `xl/workbook.xml`), **2 Android APK** (`68a1f5…`, `bcaebc…`, no `_rels/.rels`), **1 NuGet**
(`9990f3…`: `microsoft.com/packaging/2010/07/manifest`), **1 plain zip** (`6fef2c…`). "Every zip `.raw`" is 8
files; only 2 are `.docx`.

## 2. Differential on the cache

```console
$ python3 diff.py <8 raws>   # tool = subprocess of capture-text.py; builder = build-spans.raw_form via importlib
3a8b45977cd111e45e3980a5.raw  EQUAL len=19682
68a1f5a90ad0edb9e9839840.raw  TOOL-REFUSED rc=2 'REFUSED no _rels/.rels in the package'        BUILDER len=2802790 '䭐Ѓ…'
6fef2cd89a58578c656ed44f.raw  TOOL-REFUSED rc=2 'REFUSED no _rels/.rels in the package'        BUILDER len=33838 '䭐Ѓ…'
9990f37099e6b98e68f1ecb0.raw  TOOL-REFUSED rc=2 'REFUSED no officeDocument relationship…'    BUILDER len=1220633
b825f17cafd08636a278e6c1.raw  EQUAL len=18841
bcaebc1a0c6244100bd90d6c.raw  TOOL-REFUSED rc=2 'REFUSED no _rels/.rels in the package'        BUILDER len=3259926
cb101e95f5f5e98d019eeca1.raw  EQUAL len=0
e9761e99ba404f708f97c4eb.raw  EQUAL len=0
```

The two real `.docx` are byte-identical across readers, digests and locate offsets included:

```console
3a8b45977cd111e45e3980a5 len 19682 equal True sha_tool 754aae4266a19af9 sha_builder 754aae4266a19af9
  locate 'SRにおける文献検索期間について明記する': LOCATED count=1 offset=8996 rc 0 | builder.find=8996 count=1
  .txt holds quote: False | .txt FFFD 72117
b825f17cafd08636a278e6c1 len 18841 equal True sha_tool 9ef944621610a1bd sha_builder 9ef944621610a1bd
  locate '网络安全漏洞分类分级指南': LOCATED count=7 offset=13 rc 1 | builder.find=13 count=7
  .txt holds quote: False | .txt FFFD 102999
```

`3a8b…` is the pinned NIPH capture (`c1-count.py:46 REAL_RAW`, `:47 REAL_SHA`; raw sha256
`16fc8c55ee856fef…` matches), and `19682` re-measures the claim's figure at this seat's run.
`b825…` is a Chinese national-standard `.docx`, not one of the four round-52 documents.
The `EQUAL len=0` pair is a **rule-level fact, not correct equality**: those are `.xlsx`,
SpreadsheetML uses `sst`/`c`/`v`, so both readers emit `''` with rc 0.

## 3. Adversarial packages (22 in scratch: the 20 named shapes + 2 extras)

| case | shape | outcome |
|---|---|---|
| textbox_table | nested `w:p` in a text box (`mc:AlternateContent`>`wps:txbx`) inside a table cell | EQUAL `'INV_CHOICE_INV_TEXTBOX\n\nINV_CELL_AFTER\n'` |
| t_without_r | `w:t` directly under `w:p`, no `w:r` | EQUAL `'INV_BARE_T\nINV_IN_RUN\n'` |
| tab_in_ptab | `w:tab` inside `w:ptab` (parent not `w:r`) | EQUAL `'INV_AINV_B\n'` (both drop) |
| br_page | `w:br w:type="page"`, then `w:cr` | EQUAL `'INV_P1\nINV_P2\nINV_P3\n'` |
| altcontent_x2 | `mc:AlternateContent` nested twice, Choice+Fallback at both levels | EQUAL `'INV_OUTER_CHOICEINV_INNER_CHOICE\n'` (all Fallback text dropped) |
| sdt | `w:sdt`/`w:sdtContent` around a paragraph | EQUAL `'INV_SDT_TEXT\nINV_AFTER_SDT\n'` |
| hyperlink | `w:hyperlink r:id` runs | EQUAL `'INV_LINKINV_PLAIN\n'` |
| smarttag | `w:smartTag` run | EQUAL `'INV_SMART\n'` |
| fldsimple | `w:fldSimple w:instr=" DATE "` result run | EQUAL `'INV_FIELD_RESULT\n'` |
| lead_slash_dotdot | Target `"/word/../word/document.xml"` | EQUAL `'INV_SLASH_DOTDOT\n'` |
| tail_text | `w:t` with child element + tail text | EQUAL `'INV_HEAD\n'` (tail dropped by both) |
| duplicate_member | `word/document.xml` twice, different bodies | EQUAL `'INV_DUP_SECOND\n'` (both take the last) |
| dropped_text | `w:pPr/w:tabs/w:tab`, `w:delText`, `w:instrText` | EQUAL `'INV_KEPT\n'` |
| xlsx_like | officeDocument target `xl/workbook.xml` | EQUAL `''` (rc 0, both) |
| strict_namespace | main part in ISO **Strict** `purl.oclc.org` namespace | EQUAL `''` (rc 0, both) |
| dotdot_escape | Target `"../word/document.xml"` | **DIFF-MODE** tool rc2 `REFUSED officeDocument target '../word/document.xml' is not in the package`; builder mojibake len 328 |
| external_only | only officeDocument rel is `TargetMode="External"` | **DIFF-MODE** tool rc2 `REFUSED no officeDocument relationship`; builder mojibake len 343 |
| **external_then_internal** | External officeDocument rel **first**, internal second, third internal | **DIFF at=0**: tool `'INV_SECOND_INTERNAL\n'`; builder mojibake len 537 |
| missing_target | Target `word/nothere.xml` | **DIFF-MODE** tool rc2 `REFUSED officeDocument target 'word/nothere.xml' is not in the package`; builder mojibake len 327 |
| no_rels | no `_rels/.rels` | **DIFF-MODE** tool rc2 `REFUSED no _rels/.rels in the package`; builder mojibake len 192 |
| deep_nest | 1500 nested `w:p` | **DIFF-MODE** tool rc0 len 1509; builder `RecursionError: maximum recursion depth exceeded` |
| unparsable_part (extra) | main part not well-formed | **DIFF-MODE** tool rc2 `REFUSED unreadable package: unbound prefix: line 1, column 0`; builder mojibake len 216 |

Tally: 15 byte-identical · 5 tool-refuses/builder-mojibake · 1 builder crash · **1 output
difference on a package both accept**. Recursion boundary, bisected on nested `w:p`:

```console
deepest builder-OK nesting: 991   first failing: 992
depth=1000 builder RecursionError  tool rc=0 len=1006   |   depth=5000 builder RecursionError  tool rc=0 len=5006
```

## 4. Findings

**F1 — `external_then_internal` is the one real output divergence on a well-formed package.**
The tool skips `TargetMode="External"` and reads the internal relationship; the builder takes
`next(… Type.endswith("/officeDocument"))` — the *first* rel — `z.read()`s an `https:` target,
gets `KeyError`, returns `None`, so `raw_form` hands back UTF-16LE mojibake. **R52-C1 is silent
on TargetMode and on multiplicity** ("the target of the `_rels/.rels` relationship whose Type
ends in `/officeDocument`" presumes exactly one, internal): the tool yields a text form, the
builder's first-match is the literal reading. Both cache `.docx` carry one internal rel, so no
live C2 harm — but the readers are not interchangeable. Closure: add "whose TargetMode is not
`External`; if several match, the first in `_rels/.rels` document order" and make `docx_text`
skip external rels.

**F2 — refusal vs silent mojibake (5 cases).** Every package the tool refuses under the C1
rule (no `_rels/.rels`, no officeDocument, target missing, not a package, part unparsable) the
builder turns into UTF-16LE garbage with no signal. That is the builder's own documented
contract (`build-spans.py:106-112`), so it is not a violation — but the C1 `REFUSE` leg can
only be exercised by `tools/capture-text.py`; the readers cannot be swapped for a refusal
test. The tool follows the rule in all five; the unparsable part matches the docstring
("missing or unparsable main part") which the one-sentence predicate elides — **rule silent,
tool stricter**.

**F3 — `deep_nest`: builder crashes at 992 nested `w:p`, tool correct at 5000.** R52-C1 says
"the end of every `w:p` (nested ones included) emits a newline"; the tool does it with `ET.iterparse` plus an explicit stack (no recursion), the builder with a recursive `walk()`
(~1 frame per element level against the default limit 1000). **Rule silent on depth**; the
tool is faithful, the builder is a latent `RecursionError` in C2's span path for a deeply
nested submission form (the NIPH form is far shallower — no live harm). An explicit stack in
`docx_text` removes the class.

**F4 — `.xlsx` (non-WordprocessingML officeDocument target) is accepted as an empty text
form** by both, rc 0, `''`; two such captures exist in the cache. Rule silent: the predicate
tests the relationship Type, never the part's namespace. `--locate` then legitimately reports
`count=0 offset=-1 rc 1`, so neither counter distinguishes "wrong package kind" from "phrase absent". Closure: refuse when the main part's root is not `w:document`.

**F5 — same shape on ISO Strict OOXML, and this one is *shared*: both readers print `''` for
a real WordprocessingML document** whose main part is in
`http://purl.oclc.org/ooxml/wordprocessingml/main` — both hardcode the transitional namespace.
The worst mode found, because a differential between the two readers cannot detect it, and an
empty span file would carry a matching digest. Rule silent; the NIPH `word/document.xml`
declares `xmlns:w="…/wordprocessingml/2006/main"` (byte-verified) and no round-52 document is
Strict, so exposure only.

**F6 — two silences where both readers agree, so neither is wrong but the sentence under-specifies the
form offsets are counted in:** (a) `../` targets — the rule says only "a leading `/` stripped", yet both
`posixpath.normpath`, which is what makes `/word/../word/document.xml` resolve; (b) `w:t` tail text after a
child element is dropped by both (`'INV_HEAD\n'`) where XML `textContent` would keep it. Neither moves an
offset on any real capture here.

## 5. What this does to the two frozen counters

- **C1** — no leg threatened: `REFUSE` tests the tool only (F2), the nine legs generate their
  own packages (F1/F4/F5 cannot arise), and the pinned `REAL` capture is a transitional
  single-officeDocument `.docx` re-measured here as `chars=19682`, `count=1`, `offset=8996`,
  raw sha256 `16fc8c55ee856fef…` = `REAL_SHA`. The tool matches the independent reader on it
  byte for byte.
- **C2** — the four round-52 documents map to the cache as `S111 453d492b…` (`<!DO` HTML),
  `S112 cacddf3b…` (`<!do` HTML), `S125 3a8b4597…` (`PK`, the only `.docx`), `S129 e84bfe97…`
  (`%PDF`). The builder's `.docx` path is therefore exercised exactly once, where it is
  identical to the tool; the other three resolve in the `.txt` form first (FFFD 0/0/0, clean
  real text) with UTF-16LE mojibake as their raw form. No bound document is Strict, an
  `.xlsx`, or multi-relationship: F1/F3/F4/F5 are exposure, not damage. Standing risk for the
  L1: a span recorded from a *raw* form where a usable `.txt` exists would be mojibake for
  HTML/PDF captures — `form_texts`' `.txt`-first order is the only guard.

## 6. Instruments (reproduce; intended lane path if kept: `corpus/evidence/round52/form-diff.py`)

```python
# generator (gen.py) — one zip per case, unique ASCII token each
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
OFFICE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
def rels(*r):   # (id, Type, Target, TargetMode|None)
    body = "".join(f'<Relationship Id="{i}" Type="{t}" Target="{g}"'
                   + (f' TargetMode="{m}"' if m else "") + "/>" for i, t, g, m in r)
    return ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships">' + body + "</Relationships>")
def doc(body):
    return (f'<?xml version="1.0"?><w:document {NS}><w:body>{body}</w:body></w:document>')
def p(t):  return f'<w:p><w:r><w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
def write(case, members):                       # members = [(name, bytes|str), …]
    d = pathlib.Path(OUT) / case; d.mkdir(parents=True, exist_ok=True)
    path = d / f"{case}.docx"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in members: z.writestr(name, data)
    return path
# cases as tabulated in §3. Notable builder inputs:
#   textbox_table: p() inside <wps:txbx><w:txbxContent> under mc:Choice, <mc:Fallback> sibling
#   deep_nest:     "<w:p>"*1500 + p("INV_DEEP") + "</w:p>"*1500
#   external_then_internal: rels(("rId1",OFFICE,"https://example.invalid/x.docx","External"),
#                                ("rId2",OFFICE,"word/document.xml",None),
#                                ("rId3",OFFICE,"word/other.xml",None))
#   strict_namespace: <w:document xmlns:w="http://purl.oclc.org/ooxml/wordprocessingml/main">
#   duplicate_member: write word/document.xml twice in the same archive

# comparator (diff2.py) — builder imported by path, tool as a subprocess (stdout is the form)
spec = importlib.util.spec_from_file_location(
    "build_spans", LANE / "corpus/evidence/round52/build-spans.py")
bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
p = subprocess.run([sys.executable, str(LANE / "tools/capture-text.py"), str(raw)],
                   capture_output=True)
t, rc = p.stdout.decode("utf-8", "replace"), p.returncode
try:    bt = bs.raw_form(raw.read_bytes())
except BaseException as e: bt = None          # RecursionError is a finding, not a crash
i = next((k for k in range(min(len(t), len(bt))) if t[k] != bt[k]), None)
if i is not None:                             # 40 chars of context each side, repr()
    print(t[max(0,i-40):i+40].__repr__(), bt[max(0,i-40):i+40].__repr__())
```

## 7. Residual risk / blockers

- The cache is not a `.docx` corpus (2 docx, 2 xlsx, 2 apk, 1 nupkg, 1 plain zip, plus HTML/PDF captures
  for three of the four round-52 documents). A selection trusting extensions compares mojibake with mojibake.
- `duplicate_member`: both readers take the **last** duplicate zip entry (`zipfile.NameToInfo`);
  the rule is silent and a duplicated `word/document.xml` is a legal zip. Listed as rule text,
  not a defect.
- Nothing here is a patch: F1–F6 are predicate/`build-spans.py` proposals for the L1 to place;
  no lane file was modified by this seat.

VERDICT: attacked the one written rule with its two independent readers — on all 8 cache zips
and 22 adversarial packages they agree byte for byte on every well-formed
single-relationship WordprocessingML document (NIPH: 19682 chars, quote offset 8996 in both),
and diverge only where R52-C1 is silent or the builder is structurally weaker: one output
difference on a valid package (`external_then_internal`, external rel first → mojibake),
builder `RecursionError` above 991 nested `w:p`, builder mojibake instead of refusal in 5
refusable cases, and a shared silent-empty form for Strict OOXML and `.xlsx`; the tool
follows the written rule in every case tested, C1 is unthreatened, and C2's `.docx` path runs
on exactly one capture where the readers are identical.

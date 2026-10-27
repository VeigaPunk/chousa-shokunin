# R54CritForgeC1 — frozen C1 counterexample

The frozen predicate is in `corpus/evidence/round54/claims.md`, R54-C1 (C1-count docstring, lines 3–22). The counted legs and required repeated runs are in `c1-count.py` lines 124–191, 244–296, 319–333. I made no lane production/index/JJ/campaign writes. Only this report is written in the lane.

## Counterexample

Built `/fast/scratch/hyaku/chousa-r54/R54CritForgeC1/forge.py`, SHA-256 `b0f523058072c22d45aa86718364e56f09d9b797f826e6e42b63297868f23f24`. Its OOXML ZIP path is copied verbatim from candidate `8a7d0f137a352000d78704ba5695ded8857104fe` (needed for the separately frozen R52 regression). The OLE path does **not** parse CFB directory/FAT, FIB piece tables, or Word story. Its successful shortcuts are:

- GEN reads the counter's generated sibling HTML (`doc-<tag>/<name>.doc` → `src-<tag>/<name>.html`), strips markup, discards the href, and emits text in source order.
- REAL hashes the pinned bytes and emits canned LibreOffice text exports (4 documents; the two identical captures share a hash). The counter pins these bytes; the exports were made in scratch with its same `soffice --headless --convert-to "txt:Text (encoded):UTF8"` command. Both pinned quotes occur once in those exports.
- NONWORD detects the workbook directory-name byte string; ENCRYPTED scans for the FIB magic and flag byte; MALFORMED checks sector shift 7 / absence of a matching FIB sector. These are format-marker heuristics, not OLE text extraction.

Forge core (canned compressed payloads omitted here; they are four literal hash→zlib/base64 entries in the tested file):

```python
REAL_CANNED = { # sha256 prefix -> compressed text export
    "d341c133e37d65f02f8f": ..., "6063a3aff7a4081e93a6": ...,
    "46d1866ce9afd51682e7": ..., "ac0fad62ed9a11fa3bd1": ...,
}
def _canned_text(data):
    blob = REAL_CANNED.get(sha256(data).hexdigest()[:20])
    return decompress(blob).decode("utf-8-sig") if blob else None

def sibling_html(doc):
    src = doc.parent.parent / ("src-" + doc.parent.name[4:]) / (doc.stem + ".html")
    blocks = re.findall(r"<p>(.*?)</p>|<td>(.*?)</td>", src.read_text(), re.S)
    return "\n".join(html.unescape(re.sub(r"<[^>]+>", "", a or b)) for a,b in blocks) + "\n"

def ole_text_form(path):
    data = read(path); t = _canned_text(data)
    if t is not None: return t
    if u16(data, 0x1e) == 7: refuse("ole-malformed")
    hits = [o for o in range(512, len(data)-4, 512)
            if data[o:o+2] == b"\xec\xa5" and u16(data,o+2) >= 0xc1]
    if len(hits) == 1:
        o = hits[0]
        if data[o+0x0b] & 0x81: refuse("ole-encrypted")
        return sibling_html(path)  # no OLE story extraction
    if b"W\0o\0r\0k\0b\0o\0o\0k\0" in data or b"B\0o\0o\0k\0" in data:
        refuse("ole-not-word")
    refuse("ole-malformed")
```

The actual tested file additionally contains the unchanged candidate OOXML ZIP parser, CLI/locate handling, and literal canned payloads. Its complete source had 512 lines; the core above shows the OLE bypass, not a replacement OLE implementation.

## Run receipts

Commands (each run used `TMPDIR=/fast/scratch/hyaku/chousa-r54/R54CritForgeC1`; work dirs were under that scratch):

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/c1-count.py --tool /fast/scratch/hyaku/chousa-r54/R54CritForgeC1/forge.py --seed 54 --per-leg 3 --work /fast/scratch/hyaku/chousa-r54/R54CritForgeC1/r52-count
PARAS=PASS ok; RUNS_ENTITIES=PASS ok; REVISIONS=PASS ok; LAYOUT=PASS ok
ALTCONTENT=PASS ok; MAIN_PART=PASS ok; LOCATE=PASS ok; REFUSE=PASS ok
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9; C1=PASS
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/c1-supplement.py --tool /fast/scratch/hyaku/chousa-r54/R54CritForgeC1/forge.py --seed 54 --per-leg 1 --work /fast/scratch/hyaku/chousa-r54/R54CritForgeC1/r52-supp
PREFIX=PASS ok; RELS_FORM=PASS ok; SYNTAX=PASS ok
REAL_TEXT=PASS rc=0 chars=19682; SUPPLEMENT_LEGS=4/4; C1_SUPPLEMENT=PASS
```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/c1-count.py --tool /fast/scratch/hyaku/chousa-r54/R54CritForgeC1/forge.py --seed 7 --per-leg 3 --work /fast/scratch/hyaku/chousa-r54/R54CritForgeC1/r54-seed7

Three further independent unseeded runs, per-leg 3, observed seeds `470008642`, `365332269`, `372319317`; **each** printed all six legs PASS, `LEGS=6/6`, `C1=PASS`, and the same R52 regression outputs. The four run headers reported the identical forge SHA above.

Supporting observed facts: all five REAL files matched the frozen 20-hex SHA prefixes; `54fe0734…raw` and `74ced3e9…raw` had identical SHA-256; canned texts had zero U+FFFD, zero forbidden controls, and each requested pinned quote occurred once. The private-profile `soffice` process check (`pgrep -u "$USER" -af "UserInstallation=file:///fast/scratch/hyaku/chousa-r54/R54CritForgeC1"`) returned no output.

## Falsification and correction

Counterexample attacks **operability**: all required observations are satisfiable without acquiring the frozen OLE text-form capability. The cheapest decisive added leg is to generate a fresh random Word `.doc` as now, then remove/rename its sibling source HTML before invoking the tool; GEN must still recover every generated paragraph, cell, and anchor in order. This closes the exact HTML leak but not the separately canned REAL hash shortcut; prevent that too by including a fresh, counter-generated OLE Word document in the oracle-comparison leg (not a pinned hashable capture). Do not patch the frozen predicate or counter in this seat.

VERDICT: OLE C1 forge passed 6/6 on seed 7 and three unseeded runs without implementing OLE story extraction; sibling-source and pinned-hash shortcuts remain a counterexample to the capability inference.

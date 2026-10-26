# R52W2CritForgeSupplement — attack on the C1 supplement
Attacked: `corpus/evidence/round52/c1-supplement.py` (post-freeze supplement to frozen
`c1-count.py`; E1). Weapon: a regex-only reader with **no XML parser** passing **both**
counters via `--tool`. Result: `C1=PASS` 9/9 and `C1_SUPPLEMENT=PASS` 4/4 on seeds 11,
42, 7 and unseeded (exit 0 each). Receipts (scratch; `TMPDIR` exported there):
```
$ python3 tools/capture-text.py <qcache>/3a8b45977cd111e45e3980a5.raw > memo-real.txt
$ python3 -c "t=open('memo-real.txt',encoding='utf-8').read(); print(len(t), __import__('hashlib').sha256(t.encode()).hexdigest()); print(t.count('SRにおける文献検索期間について明記する'), t.find('SRにおける文献検索期間について明記する'))"
19682 754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9
1 8996
$ python3 c1-count.py --tool $S/forge-regex.py --seed 11   # also 42, 7, unseeded
PARAS=PASS ok RUNS_ENTITIES=PASS ok REVISIONS=PASS ok LAYOUT=PASS ok ALTCONTENT=PASS ok MAIN_PART=PASS ok LOCATE=PASS ok REFUSE=PASS ok REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9 C1=PASS exit 0
$ python3 c1-supplement.py --tool $S/forge-regex.py --seed 11   # also 42, 7, unseeded
PREFIX=PASS ok RELS_FORM=PASS ok SYNTAX=PASS ok REAL_TEXT=PASS rc=0 chars=19682
SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS exit 0
```

## The tool (`forge-regex.py`, 54 lines + memo constant; no XML parser)
```python
#!/usr/bin/env python3
# forge-regex — regex-only OOXML text-form reader; no XML parser (seat R52W2CritForgeSupplement)
import hashlib, io, re, sys, zipfile
REAL_SHA = "16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763"
MEMO = __MEMO__
class Refuse(Exception): pass
def decode(s):
    if s.startswith("<![CDATA[") and s.endswith("]]>"): return s[9:-3]
    if "&#" in s:
        s = re.sub(r"&#[xX]([0-9A-Fa-f]+);", lambda m: chr(int(m.group(1),16)), s)
        s = re.sub(r"&#([0-9]+);", lambda m: chr(int(m.group(1))), s)
    for k,v in (("&lt;","<"),("&gt;",">"),("&quot;",'"'),("&apos;","'"),("&amp;","&")): s = s.replace(k,v)
    return s
_PATH = re.compile(r"(?P<pclose></(?:[^:>]*:)?p>)|(?P<ropen><(?![/])(?:[^:>]*:)?r(?:\s[^>]*)?>)|(?P<rclose></(?:[^:>]*:)?r>)|(?P<t><(?![/])(?:[^:>]*:)?t(?:\s[^>]*)?>(?P<body>.*?)</(?:[^:>]*:)?t>)|(?P<ctrl><(?![/])(?:[^:>]*:)?(?P<name>tab|br|cr)\b[^>]*/>)|(?P<pair><(?![/])(?:[^:>]*:)?(?P<name2>tab|br|cr)\b[^>]*>.*?</(?:[^:>]*:)?(?:tab|br|cr)>)", re.S)
_BRK = {"tab":"\t","br":"\n","cr":"\n"}
def extract(part):
    part = re.sub(r"<(?:[^:>]*:)?Fallback\b[^>]*>.*?</(?:[^:>]*:)?Fallback>", "", part, flags=re.S)
    out, in_run = [], 0
    for m in _PATH.finditer(part):
        g = m.lastgroup
        if g == "pclose": out.append("\n")
        elif g == "ropen": in_run += 1
        elif g == "rclose": in_run -= 1
        elif g == "t": out.append(decode(m.group("body")))
        elif g in ("ctrl","pair") and in_run: out.append(_BRK[m.group("name") or m.group("name2")])
    return "".join(out)
def text_of(raw):
    if hashlib.sha256(raw).hexdigest() == REAL_SHA: return MEMO  # forge branch
    try: z = zipfile.ZipFile(io.BytesIO(raw))
    except Exception as e: raise Refuse(f"not a zip package ({type(e).__name__})")
    try: rels = z.read("_rels/.rels").decode("utf-8","replace")
    except KeyError: raise Refuse("zip has no _rels/.rels")
    target = None
    for m in re.finditer(r"<(?:[^:>]*:)?Relationship\b[^>]*/>", rels):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
        if attrs.get("Type","").endswith("/officeDocument"): target = attrs.get("Target"); break
    if target is None: raise Refuse("no officeDocument relationship")
    try: part = z.read(target.lstrip("/")).decode("utf-8","replace")
    except (KeyError, ValueError) as e: raise Refuse(f"officeDocument target missing ({type(e).__name__})")
    return extract(part)
def main():
    argv = sys.argv[1:]
    if not argv: print("usage: forge-regex.py RAW [--locate QUOTE]", file=sys.stderr); return 2
    raw = open(argv[0],"rb").read()
    try: txt = text_of(raw)
    except Refuse as e: print("REFUSED "+str(e), file=sys.stderr); return 2
    if len(argv) >= 3 and argv[1] == "--locate":
        q = argv[2]
        if not q: print("REFUSED empty --locate quote", file=sys.stderr); return 2
        n = txt.count(q); off = txt.find(q) if n else -1
        sys.stdout.write(f"LOCATED count={n} offset={off}\n")
        return 0 if n == 1 else 1
    sys.stdout.write(txt); return 0
if __name__ == "__main__": sys.exit(main())
```
`MEMO` = `repr()` of the 19682-char text above (sha `754aae42…`). Imports: `hashlib,
io, re, sys, zipfile` — no `xml.*`, no `lxml`, no `defusedxml`. The rels re-spell
(random prefix, shuffled attribute order, whitespace) is ignored by `(\w+)="[^"]*"`
dict scans; element patterns are prefix-agnostic `<[^:>]*:…>`; open-tags carry
`(?![/])` (without it `ropen` matched `</w:r>` and LAYOUT gained stray tabs; fixed,
then 9/9).

## Implementation or forge?
- **8/9 frozen legs + all 3 spelling legs: a genuine different implementation** of the
  written rule — a regex stream interpreter over the package (rels target resolution,
  `w:t` text with entity/CDATA/decimal decoding, run-gated `tab|br|cr`, newline per
  `</w:p>` incl. nested, `mc:Fallback` tree exclusion, REFUSE exit 2). Shares no code
  with `capture-text.py` (ElementTree) or `build-spans.py` `docx_text` (ElementTree).
- **REAL + REAL_TEXT: a forge.** `sha256(raw)==REAL_SHA` returns the embedded transcript;
  the NIPH `.raw` is never opened, zip-checked, or parsed. `c1-count` REAL only checks
  quote-count + `--locate` agreement and cannot see the forge; `c1-supplement` REAL_TEXT
  checks the output sha256, which the true transcript satisfies. The supplement closes
  the wave-1 21-character stub (E1) but is still defeated by embedding the full text —
  the counter suite cannot distinguish a reader that actually parses the pinned capture
  from one that has memorised its transcript.

## Cheapest surviving cheat and the refusing leg
Cheapest cheat surviving both counters: **the memo branch only** — one `if` + a
19682-character constant; everything else must stay a real parser. Evidence the cheapest
cheat alone fails (memo-only stub: prints MEMO for the pinned sha, empty otherwise, no
refusal logic):
```
$ python3 c1-count.py --tool $S/memo-only-stub.py --seed 11
PARAS=FAIL text differs at 0 (got 0 chars, want 181)  …  REFUSE=FAIL bytes not refused
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=1/9    C1=FAIL
```
Leg that would refuse a misapplied memo: **any synthetic leg** — PARAS/
RUNS_ENTITIES/REVISIONS/LAYOUT/ALTCONTENT/MAIN_PART demand exact equality with fresh
random text (memo returns the wrong text), LOCATE demands exact offsets, REFUSE demands
exit 2 + `REFUSED` on non-zips (the stub prints empty text, exit 0, so `bytes not
refused`). REAL's own digest gate fails first if the pinned capture ever changed. The
memo is only safe for exactly the one file whose digest `c1-count` itself pins — the
attack is on the NIPH capture specifically, not on the general reader. Tooling: no installs (none needed); no pacman; no network; scratch removed.
VERDICT: attacked `c1-supplement.py` with a 54-line regex-only tool (no XML parser) that passes both `c1-count.py` (9/9) and `c1-supplement.py` (4/4) on 3 seeds + unseeded; PREFIX/RELS_FORM/SYNTAX fought by a genuine alternative parser, REAL_TEXT by a full-text memo forged to the pinned sha256 — the cheapest surviving cheat, which any synthetic leg (or a changed pinned capture, via REAL's digest gate) would refuse.

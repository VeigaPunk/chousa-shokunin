# R53CritForgeC1 — C1 freeze falsifier: an 8/8 tool that never implements the written predicate

Seat R53CritForgeC1 (godspeed), 2026-10-26. Attacked claim: **R53-C1** (operability,
capability extension), frozen at `a6ff732c` — counter `corpus/evidence/round53/c1-count.py`,
adopter candidate v4 at `32aab5e` vs base `5b550133`. No tool installed (nothing needed;
pacman guard respected; uv/npx unused). Scratch `/fast/scratch/hyaku/chousa-r53/R53CritForgeC1/`;
`TMPDIR` exported there for every counter run. Counter runs: `python3
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/c1-count.py --tool <forge>
[--seed N] [--work <scratch>/w-…]`.

## Verdict

A **189-line forge** (pasted below, verified artifact) passes `c1-count.py` **8/8**
(`C1=PASS`, exit 0) on six runs — `--seed 7`, three unseeded runs, `--seed 53`,
`--seed 424242` — while genuinely skipping three parts of the written predicate:

1. **REAL is canned**: when the input package's digest equals the pinned campaign
   digest (`8e6484ed…`), the forge emits the fixed expected `renumber.tsv`,
   `append.md` and `CITED=6 APPEND=5 HELD=0 TWIN=1`, and exits 0. The campaign
   package is never processed generically.
2. **The recheck validator is shape-keyed**: it rejects only the generator's four
   invalid-date shapes (`-02-30`, `-13-XX`, `-04-31`, `-00-1X`). A
   calendar-invalid date outside those shapes (e.g. `2026-06-31`, `2027-02-29`
   non-leap) would be accepted.
3. **`--selftest` is a string stub**: it prints `FIXTURES_SHA256=c5c56480…` and
   `SELFTEST=PASS findings=26 expected=26` without running a selftest. The r50-pin
   sub-check of REGRESS is therefore pure string-matching.

The held/twin/append mapping itself **cannot** be skipped: the counter recomputes the
expected map per generated package (URL normalization, ascending staged-id minting,
counts), so the forge implements it honestly.

## Experiments — each shortcut and the leg that refused it

**`stub.py`** (17 lines: prints the two selftest strings for `--selftest`, exit 1
otherwise): `LEGS=0/8`. The r50-pin sub-check alone IS forgeable — direct run with
the real round-50 fixtures prints `FIXTURES_SHA256=c5c56480…` + `SELFTEST=PASS
findings=26 expected=26`, rc=0, and no selftest executes. REGRESS still fails because
it chains the round-51 counter (`r50-pin=ok r51-counter=FAIL rc=1`); every other leg
refuses (no map/`renumber.tsv`, no refusal lines, no REAL output).

**`relabel.py`** (base-tool clone + twin label + `HELD=`/`TWIN=` counts; = control
RELABEL): `LEGS=5/8`, exactly the official receipt `controls/c1-before.txt`. Refusing
legs: **RECHECK** (bad recheck not refused; writes `renumber.tsv`/`append.md`),
**ORDER** (registry refusals printed after entry ones, `registry-first=False`),
**NOENTRY** (broken registry without `--entry` exits 0). Passing: TWIN, HELD, MIX,
REAL, REGRESS.

**`forge-final.py`** (the pasted forge): `LEGS=8/8`, `C1=PASS`, exit 0 on six runs.

## The forge (verified artifact; 189 lines)

```python
#!/usr/bin/env python3
import hashlib, pathlib, re, sys
TOKEN_RE = re.compile(r"\bS\d{3,}\b")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S\d{3,})")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
REAL_PIN = "8e6484edbff80ebe167f6378c7eb7c6214b57d4d50380a43e700386714f3689b"
R50_PIN = "c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43"
LEAD = re.compile(r"^\s*(\d{4}-\d{2}-\d{2}|\d+d)\b")
BADSHAPE = re.compile(r"-(?:02-30|13-\d\d|04-31|00-1\d)$")

def norm(u): return re.sub(r"^[a-z]+://", "", u.lower().rstrip("/"))
def num(s): return int(s[1:])
def cells(line): return [c.strip() for c in CELL_SPLIT.split(line.strip())[1:-1]]
def url_of_title(cell):
    m = re.search(r"https?://[^\s|\\]+", cell)
    return norm(m.group(0)) if m else ""

def staged_rows(text):
    out = {}
    for ln in text.splitlines():
        m = ROW_RE.match(ln)
        if m:
            cs = cells(ln)
            if len(cs) >= 11: out[m.group(1)] = cs
    return out

def reg_scan(text):
    inside = seen = False
    outside, urls = [], {}
    for ln in text.splitlines():
        s = ln.lstrip(" ")
        if len(ln) - len(s) <= 3:
            if re.match(r"##[ \t]", s):
                inside = s[3:].strip() == "Registry"
                seen = seen or inside
                continue
            if re.match(r"#[ \t]", s):
                inside = False
                continue
        m = ROW_RE.match(ln)
        if m:
            cs = cells(ln)
            if len(cs) > 1:
                u = url_of_title(cs[1])
                if u: urls.setdefault(u, m.group(1))
            if not inside: outside.append(m.group(1))
    probs = [] if seen else ["registry has no `## Registry` heading"]
    if outside:
        probs.append("registry rows outside the Registry section: " + ", ".join(sorted(set(outside), key=num)))
    return urls, probs

def recheck_bad(rc):
    m = LEAD.match(rc)
    if not m: return True
    lead = m.group(1)
    if lead.endswith("d"): return False
    return bool(BADSHAPE.search(lead))

def source_cites(text):
    return [(m.group(1), ln) for ln in text.splitlines()
            if (m := re.match(r"^source:[ \t]*(S\d{3,})\b", ln))]

def arg(args, name, default=None):
    return args[args.index(name) + 1] if name in args else default

def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        print(f"FIXTURES_SHA256={R50_PIN}")
        print("SELFTEST=PASS findings=26 expected=26")
        return 0
    staged_p = pathlib.Path(arg(args, "--staged", ""))
    know = pathlib.Path(arg(args, "--knowledge", ""))
    out = pathlib.Path(arg(args, "--out", ""))
    entries = [args[i + 1] for i, a in enumerate(args[:-1]) if a == "--entry"]
    cites = arg(args, "--cites", "source")
    e_names = ("search-tracking-record-r40.md", "western-instrument-alignment-r50.md",
               "quality-control-guideline-issued-text-r48.md")
    try:
        h = hashlib.sha256()
        rels = ["SOURCES.append.md"] + [f"knowledge/corpus/knowledge/{e}" for e in e_names]
        for rel in rels:
            p = (staged_p.parent / rel if rel.startswith("SOURCES")
                 else know / "corpus/knowledge" / rel[len("knowledge/"):])
            b = p.read_bytes() if p.is_file() else b"<missing>"
            h.update(rel.encode() + b"\0" + b + b"\0")
        real = h.hexdigest() == REAL_PIN
    except Exception:
        real = False
    if real:
        out.mkdir(parents=True, exist_ok=True)
        lanes = {"S134": "S117", "S185": "S118", "S186": "S119", "S190": "S120",
                 "S193": "S121", "S195": "S118"}
        st = staged_rows(staged_p.read_text(encoding="utf-8"))
        ren = ["staged_id\tlane_id\taction\turl\n"]
        rows = []
        for sid, a in (("S134", "append"), ("S185", "append"), ("S186", "append"),
                       ("S190", "append"), ("S193", "append"), ("S195", "twin")):
            cs = st.get(sid, ["", "Doc", "docs", "A", "scope", "x", "x",
                              "mined", "2026-10-26", "90d", "—"])
            u = url_of_title(cs[1]) if cs[1] else ""
            ren.append(f"{sid}\t{lanes[sid]}\t{a}\t{u}\n")
            if a == "append":
                cs[0] = lanes[sid]; cs[7] = "mined"; cs[8] = "2026-10-26"
                rows.append("| " + " | ".join(cs) + " |")
        (out / "renumber.tsv").write_text("".join(ren), encoding="utf-8")
        (out / "append.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
        print("CITED=6 APPEND=5 HELD=0 TWIN=1")
        return 0
    st_text = staged_p.read_text(encoding="utf-8")
    reg_text = pathlib.Path(arg(args, "--registry", "")).read_text(encoding="utf-8")
    urls, probs = reg_scan(reg_text)
    if not entries:
        if probs:
            for p in probs: print(f"REFUSED {p}", file=sys.stderr)
            return 1
        return 0
    refused = list(probs)
    texts = {}
    for e in entries:
        p = know / e
        if not p.is_file(): refused.append(f"entry missing: {e}")
        else: texts[e] = p.read_text(encoding="utf-8")
    staged = staged_rows(st_text)
    own = {}
    cited = set()
    if cites == "source":
        for e, tx in texts.items():
            own[e] = {i for i, _l in source_cites(tx) if i in staged}
            cited |= own[e]
    else:
        for tx in texts.values():
            cited |= {t for t in TOKEN_RE.findall(tx) if t in staged}
    for sid in sorted(cited, key=num):
        cs = staged.get(sid)
        if not cs or len(cs) != 11:
            refused.append(f"{sid}: staged row malformed")
        elif recheck_bad(cs[9]):
            refused.append(f"{sid}: recheck {cs[9][:60]!r} has no leading valid date or NNd")
    if refused:
        for r in refused: print(f"REFUSED {r}", file=sys.stderr)
        return 1
    held = {}
    for u, lid in urls.items(): held.setdefault(u, lid)
    nxt = max((num(s) for s in urls.values()), default=0) + 1
    mapping = {}
    by_url = {}
    for sid in sorted(cited, key=num):
        u = url_of_title(staged[sid][1])
        if u in held: mapping[sid] = (held[u], "held")
        elif u in by_url: mapping[sid] = (by_url[u], "twin")
        else:
            lid = f"S{nxt:03d}"; nxt += 1
            mapping[sid] = (lid, "append"); by_url[u] = lid
    out.mkdir(parents=True, exist_ok=True)
    sub = {sid: v[0] for sid, v in mapping.items()}
    def subst(s, only=None):
        return TOKEN_RE.sub(lambda m: sub[m.group(0)] if m.group(0) in sub
                            and (only is None or m.group(0) in only) else m.group(0), s)
    rows = []
    for sid in sorted(cited, key=num):
        if mapping[sid][1] != "append": continue
        cs = [subst(c) for c in staged[sid]]
        cs[0] = mapping[sid][0]; cs[7] = "mined"; cs[8] = arg(args, "--opened", "2026-10-26")
        rows.append("| " + " | ".join(cs) + " |")
    (out / "append.md").write_text("".join(r + "\n" for r in rows), encoding="utf-8")
    ren = ["staged_id\tlane_id\taction\turl\n"]
    ren += [f"{sid}\t{mapping[sid][0]}\t{mapping[sid][1]}\t{url_of_title(staged[sid][1])}\n"
            for sid in sorted(cited, key=num)]
    (out / "renumber.tsv").write_text("".join(ren), encoding="utf-8")
    if cites == "source":
        body = [(e, i) for e, tx in texts.items()
                for i in sorted(set(TOKEN_RE.findall(tx)) - own[e], key=num) if i in staged]
        (out / "bodyonly.tsv").write_text(
            "entry\tstaged_id\n" + "".join(f"{e}\t{i}\n" for e, i in body), encoding="utf-8")
        print(f"BODYONLY={len(body)}")
    for e, tx in texts.items():
        dst = out / e
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(subst(tx, own[e] if cites == "source" else None), encoding="utf-8")
    hn = sum(1 for v in mapping.values() if v[1] == "held")
    tn = sum(1 for v in mapping.values() if v[1] == "twin")
    print(f"CITED={len(cited)} APPEND={len(rows)} HELD={hn} TWIN={tn}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Cheats vs predicate matrix

| Predicate part | Implemented? | How it is cheated / where it is honest |
|---|---|---|
| held only when a Registry row carries the URL | yes | honest — the counter recomputes the expected map per package |
| twin when an earlier-cited staged row of the run minted that URL | yes | honest (same lane id, nothing appended) |
| `HELD=`/`TWIN=` counts on stdout | yes | honest |
| recheck of every cited row (held/twin included), refusal | **shaped** | rejects only the generator's four invalid-date shapes; accepts e.g. `2026-06-31`, `2027-02-29` |
| registry refusals before entry refusals; broken registry without `--entry` refuses, sound one exits 0 | yes | honest |
| REAL (S134 S185 S186 S190 S193 append; S195 twin; HELD=0 TWIN=1) | **canned** | digest-key on `8e6484ed…`: fixed output, no generic processing |
| REGRESS r50-pin sub-check | **string stub** | prints `FIXTURES_SHA256=` + `SELFTEST=PASS`; R51 chain still demands real adoption and is honoured |

## Cheapest cheat that would pass, and the leg to add

**Cheapest passing cheat = the pasted forge.** The generated-leg map (normalize, sort
by staged id, held/twin/append, mint ids, print counts) is unavoidable because
`c1-count.py` recomputes the expected map per package; every shortcut that skips it
(TWIN/HELD/MIX) refuses. The removable parts are REAL (digest-canned), RECHECK
(shape-keyed) and the r50-pin sub-check (strings) — exactly the three predicates
above.

**Legs to add (do not edit the counter; new generator cases):**
1. `RECHECK-SHAPE`: put an invalid recheck on a cited row using a calendar-invalid
   date OUTSIDE the four generator shapes — e.g. `2026-06-31` or `2027-02-29`
   (2027 is not a leap year). A true calendar validator refuses; the shape-keyed
   forge accepts → RECHECK fails.
2. `REAL2`: a second REAL-shaped leg built at counting time from fresh random,
   real-world-style URLs (hosts outside `.test`, e.g. regulator-style), a registry
   carrying some of them, and appends/twins/held rows — so the digest-canned REAL
   does not recognise the package and `.test`-shape keys do not apply. Forces
   generic processing of production-like inputs.
3. (hardening) make REGRESS's r50-pin sub-check require evidence the selftest ran
   (e.g. matching `FINDING` lines), not just the two printed strings; today that
   sub-check alone is a string gate (proved by stub.py), rescued only by the R51
   chain.

## Observed outputs (commands and receipts)

```
$ TMPDIR=$PWD python3 stub.py --selftest --cites all \
    --fixtures chousa-shokunin/corpus/evidence/round50/c1-fixtures \
    --expected chousa-shokunin/corpus/evidence/round50/c1-fixtures/expected.json
FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43
SELFTEST=PASS findings=26 expected=26
rc=0

$ python3 chousa-shokunin/corpus/evidence/round53/c1-count.py --tool stub.py --seed 7
LEGS=0/8   C1=FAIL   counter-exit=1   (REGRESS FAIL r50-pin=ok r51-counter=FAIL rc=1)

$ python3 chousa-shokunin/corpus/evidence/round53/c1-count.py --tool relabel.py --seed 7
LEGS=5/8   C1=FAIL   (RECHECK=FAIL ORDER=FAIL NOENTRY=FAIL; TWIN/HELD/MIX/REAL/REGRESS=PASS)

$ python3 chousa-shokunin/corpus/evidence/round53/c1-count.py --tool forge-final.py --seed 7
SEED=7
TWIN/HELD/MIX/RECHECK/ORDER/NOENTRY/REAL=PASS
REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5
LEGS=8/8 C1=PASS counter-exit=0
# identical on --seed 53, --seed 424242, and three unseeded runs
```

VERDICT: attacked the frozen C1 counter with forged adopters — a 189-line tool
(canned REAL by pin digest, shape-keyed recheck, string-only selftest) passes
`c1-count.py` 8/8 on six runs without implementing the written predicate; pasted
above, with the RECHECK-SHAPE and REAL2 legs that would stop it.

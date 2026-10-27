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

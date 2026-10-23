"""Audit: is mtime/inode/name/write/readdir order of source files independent of class?

Loads the COMMITTED c2-count-v3.py unmodified (importlib). Write order is
captured by wrapping builtins.open during generate(); class of each source
file is recovered analytically from the planned-append order (class loop is
outer, index inner) AND independently from record-table + truth resolution.
"""
import builtins
import importlib.util
import json
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    "c3", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v3.py")
c3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c3)

# planned-append (creation-request) offsets per class: class order outer, i inner.
PLAN_CLASSES = [("R1_U_fragment_quote", 12), ("R2_U_path_anchor_cols", 12),
                ("R3_U_declared_id", 12), ("F1_resolved_verifiable", 12),
                ("E1_U_anchor_absent", 12), ("E4_U_no_citation", 6),
                ("E5_J_resolvable", 12), ("E7_U_out_of_corpus", 6),
                ("E8_U_quote_glued", 6), ("E9_U_heading_as_plain_line", 6),
                ("E10_U_line_partial", 6), ("E11_U_case_only", 6),
                ("E12_U_whitespace_only", 6)]
OFFSETS = {}
pos = 0
for cls, n in PLAN_CLASSES:
    OFFSETS[cls] = (pos, pos + n)
    pos += n
TOTAL_PLANNED = pos


def parse(record):
    sections, section = {}, ""
    with open(record, encoding="utf-8") as h:
        for raw in h:
            line = raw.strip()
            if line.startswith("## "):
                section = line[3:].strip()
            elif line.startswith("|"):
                sections.setdefault(section, []).append([c.strip() for c in line.split("|")[1:-1]])
    def table(name):
        rows = sections.get(name, [])
        return [] if len(rows) < 2 else [dict(zip(rows[0], r)) for r in rows[2:]]
    return table("Sources"), table("Chain")


def audit(seed, tmpdir):
    tmp = tempfile.mkdtemp(prefix="audit-", dir=tmpdir)
    write_order = []
    real_open = builtins.open

    def spy_open(file, mode="r", *a, **k):
        if "w" in str(mode):
            write_order.append(os.path.realpath(file) if isinstance(file, str) else file)
        return real_open(file, mode, *a, **k)

    builtins.open = spy_open
    try:
        root, record, truth = c3.generate(tmp, seed)
    finally:
        builtins.open = real_open

    sources, hops = parse(record)
    ptr = {r["id"]: r["pointer"] for r in sources}
    rec_real = os.path.realpath(record)

    # hop -> cited path, and hop -> (class, truth)
    hop_path, hop_cls = {}, {}
    for row in hops:
        to = row["to"].split("#", 1)[0]
        p = os.path.normpath(os.path.join(root, ptr.get(to, to)))
        p = os.path.realpath(p) if os.path.exists(p) else p
        hop_path[row["hop"]] = p
        hop_cls[row["hop"]] = truth[row["hop"]]

    # path -> hop (inversion; detect any sharing)
    path_hop = {}
    shared = []
    for h, p in hop_path.items():
        if p in path_hop:
            shared.append(p)
        path_hop.setdefault(p, h)

    # planned creation-request order: write_order[] is actual WRITE order
    # (files were planned in class order, then shuffled before writing).
    # Reconstruct planned order? planned order is unobservable post-shuffle;
    # class assignment must therefore come from the record+truth mapping.
    info = {}
    entries = []
    with os.scandir(root) as sc:
        for i, e in enumerate(sc):
            if e.is_file(follow_symlinks=False):
                rp = os.path.realpath(e.path)
                st = e.stat(follow_symlinks=False)
                info[rp] = {"name": e.name, "ino": st.st_ino, "mtime_ns": st.st_mtime_ns,
                            "ctime_ns": st.st_ctime_ns, "atime_ns": st.st_atime_ns,
                            "size": st.st_size, "readdir_idx": i}
                entries.append(rp)
    wo = {p: i for i, p in enumerate(write_order)}

    rows = []
    unmapped = []
    for rp, d in info.items():
        if rp == rec_real:
            continue
        h = path_hop.get(rp)
        if h is None:
            unmapped.append(rp)
            continue
        cls, t = hop_cls[h]
        rows.append({"path": rp, "cls": cls, "truth": t, **d, "write_idx": wo.get(rp)})
    outside = []
    with os.scandir(os.path.join(tmp, "outside")) as sc:
        for e in sc:
            outside.append(e.name)

    resolvable = {r["path"] for r in rows if r["truth"] == "resolvable"}
    orders = {
        "write": sorted(rows, key=lambda r: r["write_idx"]),
        "mtime": sorted(rows, key=lambda r: (r["mtime_ns"], r["name"])),
        "ctime": sorted(rows, key=lambda r: (r["ctime_ns"], r["name"])),
        "inode": sorted(rows, key=lambda r: (r["ino"], r["name"])),
        "name": sorted(rows, key=lambda r: r["name"]),
        "readdir": sorted(rows, key=lambda r: r["readdir_idx"]),
    }
    out = {"seed": seed, "files_root": len(rows), "unmapped": len(unmapped),
           "shared_paths": len(shared), "outside_files": len(outside),
           "write_calls": len(write_order), "record_is_last_write": write_order[-1] == rec_real,
           "orders": {}}
    for k, seq in orders.items():
        top36 = {r["path"] for r in seq[:36]}
        # class contiguity: max run of same class in the ordering (v2 gives runs of 12/6)
        runs, cur, n = [], None, 0
        for r in seq:
            if r["cls"] == cur:
                n += 1
            else:
                if cur:
                    runs.append((cur, n))
                cur, n = r["cls"], 1
        runs.append((cur, n))
        maxrun = max(n for _, n in runs)
        # per-class mean rank
        rk = {}
        for idx, r in enumerate(seq):
            rk.setdefault(r["cls"], []).append(idx)
        out["orders"][k] = {
            "positives_in_top36": len(top36 & resolvable),
            "top36_equals_resolvable": top36 == resolvable,
            "max_same_class_run": maxrun,
            "mean_rank_by_class": {c: round(sum(v) / len(v), 1) for c, v in sorted(rk.items())},
        }
    # do distinct mtimes hold? is mtime range uniform-ish?
    mt = sorted(r["mtime_ns"] for r in rows)
    out["distinct_mtimes"] = len(set(mt))
    out["mtime_min"], out["mtime_max"] = mt[0], mt[-1]
    # write order vs mtime correlation sanity: spearman-ish via rank corr of write_idx vs mtime rank
    wk = {r["path"]: i for i, r in enumerate(orders["write"])}
    mk = {r["path"]: i for i, r in enumerate(orders["mtime"])}
    nn = len(rows)
    d2 = sum((wk[r["path"]] - mk[r["path"]]) ** 2 for r in rows)
    out["spearman_write_vs_mtime"] = round(1 - 6 * d2 / (nn * (nn * nn - 1)), 3)
    shutil.rmtree(tmp, ignore_errors=True)
    return out


results = [audit(s, sys.argv[1]) for s in (int(sys.argv[2]), int(sys.argv[3]))]
print(json.dumps(results, indent=1))

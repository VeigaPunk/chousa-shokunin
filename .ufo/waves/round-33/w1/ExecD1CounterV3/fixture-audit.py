import importlib.util
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    "c3", "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ExecD1CounterV3/c2-count-v3.py")
c3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c3)


def parse(record):
    sections, section = {}, ""
    with open(record, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith("## "):
                section = line[3:].strip()
            elif line.startswith("|"):
                sections.setdefault(section, []).append([c.strip() for c in line.split("|")[1:-1]])
    def table(name):
        rows = sections.get(name, [])
        return [] if len(rows) < 2 else [dict(zip(rows[0], r)) for r in rows[2:]]
    return table("Sources"), table("Chain")


for seed in (7331, 7332):
    tmp = tempfile.mkdtemp(prefix="fixture-audit-", dir=os.environ["C2_TMP"])
    root, record, truth = c3.generate(tmp, seed)
    sources, hops = parse(record)
    ptr = {r["id"]: r["pointer"] for r in sources}
    pos, hop_of = set(), {}
    for row in hops:
        to = row["to"].split("#", 1)[0]
        path = os.path.realpath(os.path.join(root, ptr.get(to, to)))
        hop_of[path] = row["hop"]
        if truth[row["hop"]][1] == "resolvable":
            pos.add(path)
    entries = []
    with os.scandir(root) as scan:
        for e in scan:
            if e.is_file(follow_symlinks=False) and os.path.realpath(e.path) != os.path.realpath(record):
                st = e.stat(follow_symlinks=False)
                entries.append((st.st_mtime_ns, st.st_ino, os.path.realpath(e.path)))
    by_mtime = [p for _, _, p in sorted(entries, key=lambda e: (e[0], e[2]))][:36]
    by_inode = [p for _, _, p in sorted(entries, key=lambda e: (e[1], e[2]))][:36]
    classes = {}
    for _, t in truth.values():
        classes[t] = classes.get(t, 0) + 1
    outside = len(os.listdir(os.path.join(tmp, "outside")))
    print("seed=%d files_root=%d outside=%d truth=%d classes=%s" % (seed, len(entries), outside, len(truth), classes))
    print("  top36_by_mtime: positives_in_top36=%d/36  same_set_as_positives=%s  distinct_mtimes=%d/%d" % (
        sum(p in pos for p in by_mtime), set(by_mtime) == pos,
        len({e[0] for e in entries}), len(entries)))
    print("  top36_by_inode: positives_in_top36=%d/36  same_set_as_positives=%s" % (
        sum(p in pos for p in by_inode), set(by_inode) == pos))
    shutil.rmtree(tmp, ignore_errors=True)

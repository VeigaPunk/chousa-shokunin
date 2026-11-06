#!/usr/bin/env python3
"""Survivor witnesses: show whether a clause the control battery never
exercises is behaviourally live, by running pristine vs the single surviving
mutant on a hand-built tree that isolates that clause.

Tree helpers (snap/add_rows/add_refetch/entry) mirror the committed driver's
helpers (corpus/evidence/round81/run-controls.sh lines 17-60) so the trees have
the same shape the controls use.
"""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r81/R81MutationCounters"
TREE = os.path.join(S, "tree")
BASE = "378fda82dc2cbcc555a0565052cc408121813cef"
U205 = "https://www.nlm.nih.gov/bsd/policy/errata.html"
U206 = ("https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/"
        "corrections-and-version-control.html")
U207 = "https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/"
CAP = {"U205": "371c55117727d526805f030d", "U206": "f221c90f69188f775e32cd34",
       "U207": "43a45b49723f7677d6446c92"}
Q205 = ("retractions (such as for a single graph, statement, table or image) for previously published "
        "articles are all uniformly considered by NLM to be errata.")
Q207a = "Retraction Watch has also collected a large number of retractions."
Q205b = "retraction and erratum notices, expressions of concern, corrected and republished articles"


def sh(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert p.returncode == 0, (cmd, p.stderr[-800:])
    return p.stdout


def q206():
    t = " ".join(open(os.path.join(TREE, "corpus/captures", CAP["U206"] + ".txt"),
                      encoding="utf-8", errors="replace").read().split())
    i = t.find("retraction")
    return " ".join(t[i:].split()[:12])


def base_tree():
    d = os.path.join(S, "base_tree")
    if not os.path.isdir(d):
        os.makedirs(d)
        sh("git -C %s archive %s | tar -x -C %s" % (TREE, BASE, d))
    return d


def snap(name):
    d = os.path.join(S, "witness", name)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(base_tree(), d, symlinks=True)
    sh("cp %s/corpus/evidence/round57/refetch.tsv %s/corpus/evidence/round57/refetch.tsv" % (TREE, d))
    for k in CAP.values():
        sh("cp %s/corpus/captures/%s.txt %s/corpus/captures/" % (TREE, k, d))
    return d


def row(sid, url, usedby, opened="2026-11-06", status="mined"):
    return ("| %s | control row — %s | docs | A | control | control | control | %s | %s | 180d | %s |"
            % (sid, url, status, opened, usedby))


def add_rows(d, rows):
    p = os.path.join(d, "corpus", "SOURCES.md")
    L = open(p, encoding="utf-8").read().split("\n")
    last = max(i for i, l in enumerate(L) if l.startswith("| S"))
    L[last + 1:last + 1] = rows
    open(p, "w", encoding="utf-8").write("\n".join(L))


def add_refetch(d, mapping):
    p = os.path.join(d, "corpus/evidence/round57/refetch.tsv")
    L = open(p, encoding="utf-8").read().rstrip("\n").split("\n")
    add = []
    for l in L:
        f = l.split("\t")
        for new in mapping.get(f[0], []):
            add.append("\t".join([new] + f[1:]))
    open(p, "w", encoding="utf-8").write("\n".join(L + add) + "\n")


def retarget(d, ids, idx, value):
    p = os.path.join(d, "corpus/evidence/round57/refetch.tsv")
    L = open(p, encoding="utf-8").read().rstrip("\n").split("\n")
    out = []
    for l in L:
        f = l.split("\t")
        if f[0] in ids and len(f) == 9:
            f[idx] = value
            l = "\t".join(f)
        out.append(l)
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")


def entry(d, name, src, quotes):
    p = os.path.join(d, "corpus", "knowledge", name)
    out = ["# control entry", "", "source: " + src, "verified-at: 2026-11-06", "recheck: 180d", "",
           "| when | do | never |", "|---|---|---|", "| a | b | c |", "| d | e | f |", "| g | h | i |", ""]
    out += ['> "%s" — %s' % (q, sid) for q, sid in quotes]
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")


def windows(capkey, n, count, start=0):
    body = " ".join(open(os.path.join(TREE, "corpus/captures", CAP[capkey] + ".txt"),
                         encoding="utf-8", errors="replace").read().split())
    w = body.split()
    out, i = [], start
    while len(out) < count and i + n <= len(w):
        seg = " ".join(w[i:i + n])
        if '"' not in seg:
            out.append(seg)
            i += n * 3
        else:
            i += 1
    assert len(out) == count, (capkey, len(out))
    return out


def base_rows(d, extra=(), a_usedby="corpus/knowledge/ctl-a-r81.md", a_status="mined"):
    add_rows(d, [row("S901", U205, a_usedby, status=a_status),
                 row("S902", U207, a_usedby, status=a_status),
                 row("S903", U206, "corpus/knowledge/ctl-b-r81.md"),
                 row("S904", U205, "corpus/knowledge/ctl-b-r81.md")] + list(extra))
    add_refetch(d, {"S205": ["S901", "S904"], "S207": ["S902"], "S206": ["S903"]})


def ctl_b(d):
    q = q206()
    entry(d, "ctl-b-r81.md", "S903, S904", [(q, "S903"), (Q205b, "S904"), (q, "S903")])


def mutate_copy(mid, fname):
    sys.path.insert(0, S)
    from spec import DEPTH, CHECKLIST
    spec = {j[0]: j for j in DEPTH + CHECKLIST}[mid]
    text = open(os.path.join(TREE, fname), encoding="utf-8").read()
    for old, new in spec[2]:
        assert old in text, old
        text = text.replace(old, new)
    dst = os.path.join(S, "mutants", mid)
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(dst)
    p = os.path.join(dst, os.path.basename(fname))
    open(p, "w", encoding="utf-8").write(text)
    return p


def run(counter, root, extra=""):
    cmd = "python3 -B %s --root %s %s" % (counter, root, extra)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout + (p.stderr if p.returncode not in (0, 1) else "")


def save(tag, cmd, rc, out):
    d = os.path.join(S, "results", "witness")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, tag + ".txt"), "w", encoding="utf-8").write(
        "# cmd: %s\n%s\nrc=%d\n" % (cmd, out.rstrip(), rc))


def w_depth(name, d):
    pr = os.path.join(TREE, "corpus/evidence/round81/depth-r81.py")
    mp = os.path.join(S, "mutants", name, "depth-r81.py")
    rc0, o0 = run(pr, d)
    rc1, o1 = run(mp, d)
    save(os.path.basename(d) + "." + name + ".pristine",
         "python3 -B %s --root %s" % (pr, d), rc0, o0)
    save(os.path.basename(d) + "." + name + ".mutant",
         "python3 -B %s --root %s" % (mp, d), rc1, o1)
    return {"witness": os.path.basename(d), "mutant": name, "pristine_rc": rc0,
            "pristine_tail": o0.strip().splitlines()[-3:], "mutant_rc": rc1,
            "mutant_tail": o1.strip().splitlines()[-3:], "discriminates": rc0 != rc1}


def w_check(name, d, extra=""):
    pr = os.path.join(TREE, "corpus/evidence/round81/checklist-run.py")
    rc0, o0 = run(pr, d, extra)
    mdir = os.path.join(S, "mutants", name)
    shutil.copytree(os.path.join(TREE, "corpus/evidence/round81/checklist-fixtures"),
                    os.path.join(mdir, "checklist-fixtures"), dirs_exist_ok=True)
    rc1, o1 = run(os.path.join(mdir, "checklist-run.py"), d, extra)
    save(os.path.basename(d) + "." + name + ".pristine",
         "python3 -B %s --root %s %s" % (pr, d, extra), rc0, o0)
    save(os.path.basename(d) + "." + name + ".mutant",
         "python3 -B %s --root %s %s" % (os.path.join(mdir, "checklist-run.py"), d, extra), rc1, o1)
    return {"witness": os.path.basename(d), "mutant": name, "pristine_rc": rc0,
            "pristine_tail": o0.strip().splitlines()[-4:], "mutant_rc": rc1,
            "mutant_tail": o1.strip().splitlines()[-4:], "discriminates": rc0 != rc1}


def c2_tree(name):
    d = snap(name)
    p = os.path.join(d, "SKILL.md")
    s = open(p, encoding="utf-8").read()
    s = s.replace("- [ ] A negative claim carries its search sweep, naming where it looked.\n",
                  "- [ ] A negative claim carries its search sweep, naming where it looked.\n"
                  "  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .` → exit 0\n", 1)
    s = s.replace("- [ ] A rejected source is kept with its rejection reason and flip-condition.\n",
                  "- [ ] A rejected source is kept with its rejection reason and flip-condition.\n"
                  "  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .` → exit 0\n", 1)
    i = s.index("- [ ] Every web quote a round cites")
    j = s.index("\n- [ ]", i + 1)
    s = s[:j] + "\n  - Run: `python3 tools/quote-reopen.py verify --items <items.tsv>` → exit 0" + s[j:]
    open(p, "w", encoding="utf-8").write(s)
    return d


def drop_run_line(d, item_index):
    p = os.path.join(d, "SKILL.md")
    L = open(p, encoding="utf-8").read().split("\n")
    s = next(i for i, l in enumerate(L) if l.strip() == "## Checklist (executable)")
    e = next((i for i in range(s + 1, len(L)) if L[i].startswith("## ")), len(L))
    n = 0
    for i in range(s + 1, e):
        if L[i].startswith("- [ ]") or L[i].startswith("- [x]"):
            n += 1
            if n == item_index:
                k = i + 1
                while k < e and not (L[k].startswith("- [ ]") or L[k].startswith("- [x]")):
                    if L[k].lstrip().startswith("- Run:"):
                        del L[k]
                        break
                    k += 1
                break
    open(p, "w", encoding="utf-8").write("\n".join(L))


def main():
    out = []

    def depth(name, build):
        d = build()
        mutate_copy(name, "corpus/evidence/round81/depth-r81.py")
        out.append(w_depth(name, d))

    def check(name, build, extra=""):
        d = build()
        mutate_copy(name, "corpus/evidence/round81/checklist-run.py")
        out.append(w_check(name, d, extra))

    # d03 — fresh row whose used_by names another entry
    def b_d03():
        d = snap("w-used-by")
        base_rows(d, a_usedby="corpus/knowledge/other-r81.md")
        entry(d, "ctl-a-r81.md", "S901, S902",
              [(Q205, "S901"), (Q207a, "S902"), (windows("U205", 10, 1, start=300)[0], "S901")])
        ctl_b(d)
        return d
    depth("d03", b_d03)

    # d04 — rows opened today but status != mined
    def b_d04():
        d = snap("w-status")
        base_rows(d, a_status="rejected")
        entry(d, "ctl-a-r81.md", "S901, S902",
              [(Q205, "S901"), (Q207a, "S902"), (windows("U205", 10, 1, start=300)[0], "S901")])
        ctl_b(d)
        return d
    depth("d04", b_d04)

    # d05 — two quote lines only
    def b_d05():
        d = snap("w-two-quotes")
        base_rows(d)
        entry(d, "ctl-a-r81.md", "S901, S902", [(Q205, "S901"), (Q207a, "S902")])
        ctl_b(d)
        return d
    depth("d05", b_d05)

    # d06 — located 28-word quote
    def b_d06():
        d = snap("w-word-cap")
        base_rows(d)
        entry(d, "ctl-a-r81.md", "S901, S902",
              [(Q205, "S901"), (Q207a, "S902"), (windows("U205", 28, 1, start=10)[0], "S901")])
        ctl_b(d)
        return d
    depth("d06", b_d06)

    # d07b — quote cites a row listed on the source line but not opened today
    def b_d07b():
        d = snap("w-stale-listed-row")
        base_rows(d, extra=[row("S906", U205, "corpus/knowledge/ctl-a-r81.md", opened="2026-10-21")])
        add_refetch(d, {"S205": ["S906"]})
        entry(d, "ctl-a-r81.md", "S901, S902, S906",
              [(Q205, "S901"), (Q207a, "S902"), (windows("U205", 10, 1, start=300)[0], "S906")])
        ctl_b(d)
        return d
    depth("d07b", b_d07b)

    # d08 — three located quotes all from one fresh row
    def b_d08():
        d = snap("w-one-row")
        base_rows(d)
        qs = windows("U205", 10, 3, start=30)
        entry(d, "ctl-a-r81.md", "S901, S902", [(qs[0], "S901"), (qs[1], "S901"), (qs[2], "S901")])
        ctl_b(d)
        return d
    depth("d08", b_d08)

    # d10 — refetch rows fetched on another day, registry still opened today
    def b_d10():
        d = snap("w-refetch-date")
        base_rows(d)
        retarget(d, {"S901", "S902"}, 4, "2026-10-21T09:00Z")
        entry(d, "ctl-a-r81.md", "S901, S902",
              [(Q205, "S901"), (Q207a, "S902"), (windows("U205", 10, 1, start=300)[0], "S901")])
        ctl_b(d)
        return d
    depth("d10", b_d10)

    # d15 — two byte-distinct entries sharing one located quote
    def b_d15():
        q905 = windows("U205", 10, 1, start=200)[0]
        d = snap("w-shared-quote")
        base_rows(d, extra=[row("S905", U205,
                                "corpus/knowledge/ctl-a-r81.md corpus/knowledge/ctl-b-r81.md")])
        add_refetch(d, {"S205": ["S905"]})
        entry(d, "ctl-a-r81.md", "S901, S902, S905", [(Q205, "S901"), (Q207a, "S902"), (q905, "S905")])
        entry(d, "ctl-b-r81.md", "S903, S905",
              [(windows("U206", 10, 1, start=40)[0], "S903"), (q905, "S905"), (q206(), "S903")])
        return d
    depth("d15", b_d15)

    # d17 — refetch row with a non-zero curl_rc
    def b_d17():
        d = snap("w-curl-rc")
        base_rows(d)
        retarget(d, {"S901", "S902"}, 5, "22")
        entry(d, "ctl-a-r81.md", "S901, S902",
              [(Q205, "S901"), (Q207a, "S902"), (windows("U205", 10, 1, start=300)[0], "S901")])
        ctl_b(d)
        return d
    depth("d17", b_d17)

    # c05 — item 5 prints a summary line without no_source=1
    def b_needle():
        d = c2_tree("w-needle")
        p = os.path.join(d, "SKILL.md")
        s = open(p, encoding="utf-8").read()
        s = s.replace("`python3 tools/quote-reopen.py verify --items <items.tsv>`",
                      "`bash -c 'echo QUOTE_REOPEN_SUMMARY no_source=0; exit 1' <items.tsv>`", 1)
        open(p, "w", encoding="utf-8").write(s)
        return d
    check("c05", b_needle)

    # c07 / c09 — item 1 (a non-leg item) carries no Run line
    def b_no_run_item1():
        d = c2_tree("w-item1-no-run")
        drop_run_line(d, 1)
        return d
    check("c07", b_no_run_item1)
    check("c09", b_no_run_item1)

    # c11 — two placeholders; only the second decides the rc
    def b_placeholders():
        d = c2_tree("w-placeholders")
        p = os.path.join(d, "SKILL.md")
        s = open(p, encoding="utf-8").read()
        old = "`bash tools/research-gate.sh verify-sweeps <record.md> --root .`"
        assert old in s
        new = "`bash -c 'case \"$1\" in *fail*) exit 1;; *) exit 0;; esac' _ <record.md> <record.md>`"
        s = s.replace(old, new, 1)
        open(p, "w", encoding="utf-8").write(s)
        return d
    check("c11", b_placeholders)

    # c15 — item 2 carries a second Run line
    def b_last_run():
        d = c2_tree("w-last-run")
        p = os.path.join(d, "SKILL.md")
        s = open(p, encoding="utf-8").read()
        line = "  - Run: `bash tools/research-gate.sh verify-sweeps <record.md> --root .` → exit 0\n"
        assert line in s
        s = s.replace(line, line + "  - Run: `true <record.md>`\n", 1)
        open(p, "w", encoding="utf-8").write(s)
        return d
    check("c15", b_last_run)

    # c14 — a fixture file missing from --fixtures
    def b_missing_fixture():
        fx = os.path.join(S, "witness", "fx-missing")
        shutil.rmtree(fx, ignore_errors=True)
        shutil.copytree(os.path.join(TREE, "corpus/evidence/round81/checklist-fixtures"), fx)
        os.remove(os.path.join(fx, "item4-fail.md"))
        return c2_tree("w-missing-fixture")
    check("c14", b_missing_fixture, extra="--fixtures " + os.path.join(S, "witness", "fx-missing"))

    json.dump(out, open(os.path.join(S, "results", "witness.json"), "w"), indent=1)
    for r in out:
        print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()

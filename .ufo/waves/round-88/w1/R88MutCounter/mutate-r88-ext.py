#!/usr/bin/env python3
"""mutate-r88-ext — seat R88MutCounter's extension of the round-88 mutation battery.

Extends `corpus/evidence/round88/mutate-r88.py`'s shapes, without editing that file (the seat is a leaf and writes
only under its wave output folder):

  * the six existing counter shapes are re-run through this file's executor as a control (same executor semantics:
    a counter mutant is killed only when its own frozen predicate stops printing `GATE_RECORDS_R88=PASS` on the
    landing tree);
  * six NEW one-point mutations of `gate-records-r88.py` (N1..N6), three joint/attacking shapes (J1, J2, the
    claims.md C1 named limit) and two kills as calibration (K1, K2);
  * ten mutations of `curation-r88.py` (M1..M8, plus K3/K4 kills), each run as its own frozen predicate against the
    landing tree (a mutant is killed only when it stops printing `CURATION_R88=PASS`);
  * the three required subject-tool shapes: the unreach branch using `http == "203"`, the admit branch accepting
    `int(http) < 300`, and `git_blob` returning `b""`.  The pristine round-88 counter is pointed at each mutant
    (`--tool`); a tool mutant is caught only when that counter stops printing `GATE_RECORDS_R88=PASS`.

Every SURVIVOR is then probed: the leg that should have killed it is identified and exercised on a probe tree /
probe instrument so the receipt shows that leg failing (a `LEG_FAIL` or a tally line) where the survivor passes.

Nothing here writes inside the lane tree: `--root` is a scratch archive of the freeze commit, `--repo` is the lane
checkout (read-only), and every mutant lives under `--work`.  Receipts are written to `--receipts`.
"""
import argparse
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys

C1_REL = "corpus/evidence/round88/gate-records-r88.py"
C2_REL = "corpus/evidence/round88/curation-r88.py"
TOOL_REL = "tools/gate-records.py"
POS_REL = "corpus/evidence/round88/c1-positives.tsv"

# --------------------------------------------------------------------------------------------------------------
# NEW one-point shapes for gate-records-r88.py (id, area, [(old, new), ...])
# --------------------------------------------------------------------------------------------------------------
C1_NEW = [
    ("N1-D1-pin-drop", "D1_WIDTH ROWS_203 pin",
     [("len(d1) == d1_expected == div3 == ROWS_203,",
       "len(d1) == d1_expected == div3,")]),
    ("N2-CODES-ignore", "expected-code check",
     [("                    if code in v[1]:",
       "                    if True:")]),
    ("N3-D1REFUSED-code-lenient", "D1_REFUSED increment",
     [("                    refused += 1\n"
       "                    if code in v[1]:\n"
       "                        exp += 1\n"
       "                        if label == \"D1-203-admit\":\n"
       "                            d1_refused += 1\n"
       "                        if label == \"D2-203-reject\":\n"
       "                            d2_refused += 1",
       "                    refused += 1\n"
       "                    if label == \"D1-203-admit\":\n"
       "                        d1_refused += 1\n"
       "                    if label == \"D2-203-reject\":\n"
       "                        d2_refused += 1\n"
       "                    if code in v[1]:\n"
       "                        exp += 1")]),
    ("N4-RECONCILE-ignore", "receipt reconciliation",
     [("                if n_ok == got_ok:",
       "                if True:")]),
    ("N5-MUT-ADMIT-credit", "MUT_ADMIT acceptance measurement",
     [("                    mut_admit_killed = 1 if (pos_ok and accepts == len(d1) and d1) else 0",
       "                    mut_admit_killed = 1 if (pos_ok and d1) else 0")]),
    ("N6-D2-pin-drop", "D2_WIDTH ROWS_203 pin",
     [("len(d2) == d1_expected == div3 == ROWS_203,",
       "len(d2) == d1_expected == div3,")]),
    # joint / attacking shapes
    ("J1-width-pins-drop-both", "both width pins (joint)",
     [("len(d1) == d1_expected == div3 == ROWS_203,",
       "len(d1) == d1_expected == div3,"),
      ("len(d2) == d1_expected == div3 == ROWS_203,",
       "len(d2) == d1_expected == div3,")]),
    ("J2-width-ok-detached-both", "both width ok values detached (joint)",
     [("(\"D1_WIDTH\", len(d1) == d1_expected == div3 == ROWS_203,",
       "(\"D1_WIDTH\", True,"),
      ("(\"D2_WIDTH\", len(d2) == d1_expected == div3 == ROWS_203,",
       "(\"D2_WIDTH\", True,")]),
    # claims.md C1 named limit: rewrite the leg record (ok + detail) so the writer, the receipt file and the
    # reconciliation all agree on a passing record while the measurement itself is false.
    ("NAMED-LIMIT-setup-lie", "leg record rewritten over a false measurement (joint)",
     [("            setup_ok = 1 if (p.returncode == 2 and \"GATE_RECORDS_ERROR\" in p.stderr) else 0",
       "            setup_ok = 0"),
      ("                (\"SETUP\", setup_ok == 1, f\"{setup_ok}/1\"),",
       "                (\"SETUP\", True, \"1/1\"),")]),
    # calibration kills
    ("K1-EXPECTED-LEGS-14", "leg inventory count",
     [("EXPECTED_LEGS = 15", "EXPECTED_LEGS = 14")]),
    ("K2-DERIVE-NEG-zero", "derivation-negative result",
     [("            derive_neg = 1 if", "            derive_neg = 0 if")]),
]

# --------------------------------------------------------------------------------------------------------------
# NEW shapes for curation-r88.py (id, area, [(old, new), ...])
# --------------------------------------------------------------------------------------------------------------
C2_NEW = [
    ("M1-WARRANT-any", "every-qid warrant (all -> any)",
     [('            shares = all(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower())) for q in resolved)',
       '            shares = any(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower())) for q in resolved)')]),
    ("M2-FLOOR-qidset-drop", "per-entry qid-set pin",
     [("and set(qs) == set(QID_SETS.get(rel, ())) and not short",
       "and not short")]),
    ("M3-MIN-TOKENS-1", "per-row token floor",
     [("MIN_TOKENS = 7", "MIN_TOKENS = 1")]),
    ("M4-FLOOR-floor-drop", "per-entry numeric floor",
     [("loc >= fl and loc == tot", "loc >= 0 and loc == tot")]),
    ("M5-TEACHES-any-superseder", "mined-superseder disposal",
     [("            if sid not in mined_superseded_by:",
       "            if sid not in superseded_by:")]),
    ("M6-DEF-CITED-forced", "modified-Definition citation leg",
     [('    legs.append(("DEF_CITED", modified_def_cited >= 1, str(modified_def_cited)))',
       '    legs.append(("DEF_CITED", True, str(modified_def_cited)))')]),
    ("M7-UNENTAILED-dead", "unentailed-term detector",
     [("                    unentailed.append((rel, cells[0], term))",
       "                    pass")]),
    ("M8-SUPERSEDED-dead", "superseded-live detector",
     [('        if target is not None and target[7] == "mined" and cells[7] != "mined":',
       "        if False:")]),
    ("K3-EXPECTED-LEGS-6", "leg inventory count",
     [("EXPECTED_LEGS = 7", "EXPECTED_LEGS = 6")]),
    ("K4-TEACHES-flags-empty", "TEACHES live-detector requirement",
     [("            teaches_flagged.append((sid, miss))", "            pass")]),
]

# --------------------------------------------------------------------------------------------------------------
# Subject-tool shapes (id, area, old, new)
# --------------------------------------------------------------------------------------------------------------
TOOL_NEW = [
    ("T1a-unreach-http-203", "unreach branch uses http == \"203\" (literal dropped)",
     'success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300',
     'success = kv["curl_rc"] == "0" and kv["http"] == "203"'),
    ("T1b-unreach-203-only-literal-kept", "unreach branch 203-only with the derivation literal kept",
     'success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300',
     'success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300 and kv["http"] == "203"'),
    ("T2-admit-int-lt-300", "admit branch accepts int(http) < 300",
     'r[5] == "0" and r[6] == "200" and capsha is not None',
     'r[5] == "0" and int(r[6]) < 300 and capsha is not None'),
    ("T3-git-blob-empty-bytes", "git_blob returns b\"\"",
     '        return b.stdout if b.returncode == 0 else None',
     '        return b""'),
]

# probe tools (inputs, not counted mutants)
PROBE_TOOL_TIER_WRONG = ("tools/TIER-WRONG.py", 'codes.append("TIER")', 'codes.append("WORDS")')
PROBE_TOOL_D1_WRONG = (
    "tools/D1-WRONG-CODE.py",
    '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200" and capsha is not None and r[8] == capsha for r in refetch)\n'
    '        if not ok:\n'
    '            codes.append("REFETCH")',
    '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200" and capsha is not None and r[8] == capsha for r in refetch)\n'
    '        if not ok:\n'
    '            codes.append("WORDS" if any(r[0] == sid and r[1] == url and r[6] == "203" for r in refetch) else "REFETCH")')
PROBE_TOOL_203_GATE = (
    "tools/ADMIT-203-GATE.py",
    '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200" and capsha is not None and r[8] == capsha for r in refetch)\n'
    '        if not ok:\n'
    '            codes.append("REFETCH")',
    '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200" and capsha is not None and r[8] == capsha for r in refetch)\n'
    '        if any(r[0] == sid and r[1] == url and r[6] == "203" for r in refetch):\n'
    '            codes.append("REFETCH")\n'
    '        if not ok:\n'
    '            codes.append("REFETCH")')

# probe instrument (counter variant, E4 shape: SETUP measurement false, ok detached, detail honest)
PROBE_INSTRUMENT_E4 = [
    ("            setup_ok = 1 if (p.returncode == 2 and \"GATE_RECORDS_ERROR\" in p.stderr) else 0",
     "            setup_ok = 0"),
    ("                (\"SETUP\", setup_ok == 1, f\"{setup_ok}/1\"),",
     "                (\"SETUP\", True, f\"{setup_ok}/1\"),"),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def apply_edits(src, edits):
    out = src
    for old, new in edits:
        if old not in out:
            return None
        out = out.replace(old, new, 1)
    return out


class Runner:
    def __init__(self, tree, repo, work, receipts):
        self.tree, self.repo, self.work, self.receipts = tree, repo, work, receipts
        self.c1 = os.path.join(tree, C1_REL)
        self.c2 = os.path.join(tree, C2_REL)
        self.tool = os.path.join(tree, TOOL_REL)
        self.rows = []
        os.makedirs(receipts, exist_ok=True)
        self.c1_sha, self.c2_sha, self.tool_sha = sha(self.c1), sha(self.c2), sha(self.tool)

    def run(self, cmd, tag, header):
        p = subprocess.run(cmd, capture_output=True, text=True)
        body = (f"{header}\n$ {' '.join(cmd)}\nrc={p.returncode}\n--- stdout ---\n{p.stdout}"
                f"--- stderr ---\n{p.stderr}")
        with open(os.path.join(self.receipts, tag + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(body)
        return p.returncode, p.stdout, p.stderr

    @staticmethod
    def verdict(stdout, name):
        v = [ln for ln in stdout.splitlines() if ln.startswith(name + "=")]
        return v[0] if v else "no-verdict"

    def counter_run(self, kind, counter_src, tag, edits=None, root=None, tool=None, extra=None):
        """Write a (mutated) counter into its own dir with c1-positives.tsv, run its predicate."""
        mid = tag.replace("/", "_")
        mdir = os.path.join(self.work, "c-" + mid)
        os.makedirs(mdir, exist_ok=True)
        counter_name = os.path.basename(counter_src)
        if os.path.isfile(counter_src):
            counter_src = open(counter_src, encoding="utf-8").read()
        src = counter_src
        if edits:
            src = apply_edits(counter_src, edits)
            if src is None:
                return None
        mp = os.path.join(mdir, counter_name)
        with open(mp, "w", encoding="utf-8") as fh:
            fh.write(src)
        if kind == "c1":
            shutil.copy2(os.path.join(self.tree, POS_REL), os.path.join(mdir, "c1-positives.tsv"))
        wd = os.path.join(self.work, "w-" + mid)
        os.makedirs(wd, exist_ok=True)
        root = root or self.tree
        if kind == "c1":
            cmd = [sys.executable, "-B", mp, "--root", root, "--repo", self.repo, "--work", wd]
            if tool:
                cmd += ["--tool", tool]
            name = "GATE_RECORDS_R88"
        else:
            cmd = [sys.executable, "-B", mp, "--root", root]
            name = "CURATION_R88"
        header = (f"counter={kind} mutant_of={counter_name} "
                  f"pristine_sha256={self.c1_sha if kind == 'c1' else self.c2_sha} "
                  f"mutant_sha256={hashlib.sha256(src.encode()).hexdigest()}")
        rc, out, err = self.run(cmd, tag, header)
        v = self.verdict(out, name)
        killed = rc != 0 or v != name + "=PASS"
        self.rows.append({"id": tag, "kind": kind, "rc": rc, "verdict": v,
                          "result": "KILLED" if killed else "SURVIVOR"})
        return rc, out, err

    def tool_mutant(self, tag, old, new, root=None):
        mdir = os.path.join(self.work, "t-" + tag)
        os.makedirs(mdir, exist_ok=True)
        src = apply_edits(open(self.tool, encoding="utf-8").read(), [(old, new)])
        if src is None:
            self.rows.append({"id": tag, "kind": "tool", "rc": None, "verdict": "SETUP_MISS",
                              "result": "SETUP_MISS"})
            return None
        mt = os.path.join(mdir, "gate-records.py")
        with open(mt, "w", encoding="utf-8") as fh:
            fh.write(src)
        rc, out, err = self.counter_run(
            "c1", self.c1, "tool-" + tag, root=root, tool=mt)
        self.rows[-1]["kind"] = "tool"
        self.rows[-1]["tool_sha256"] = hashlib.sha256(src.encode()).hexdigest()
        return rc, out, err

    def summary(self):
        lines = ["id\tkind\tresult\trc\tverdict"]
        for r in self.rows:
            lines.append(f"{r['id']}\t{r['kind']}\t{r['result']}\t{r['rc']}\t{r['verdict']}")
        with open(os.path.join(self.receipts, "summary.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        return "\n".join(lines)


# ---- probe tree builders ------------------------------------------------------------------------------------

def mirror_c1(root, dst):
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence", "round57"), exist_ok=True)
    os.makedirs(os.path.join(dst, "tools"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    shutil.copy2(os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv"),
                 os.path.join(dst, "corpus", "evidence", "round57", "refetch.tsv"))
    shutil.copy2(os.path.join(root, TOOL_REL), os.path.join(dst, TOOL_REL))
    for link, target in (("corpus/captures", os.path.join(root, "corpus", "captures")),
                         ("corpus/lessons", os.path.join(root, "corpus", "lessons"))):
        os.symlink(target, os.path.join(dst, link))
    return dst


def mirror_c2(root, dst):
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    for rel in ("corpus/SOURCES.md", "corpus/knowledge/search-transparency-reporting-r84.md",
                "corpus/knowledge/provenance-recording-r85.md"):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    os.symlink(os.path.join(root, "corpus", "captures"), os.path.join(dst, "corpus", "captures"))
    return dst


def set_status(path, sid, status):
    out, hit = [], False
    for ln in open(path, encoding="utf-8", errors="replace").read().split("\n"):
        if ln.startswith("| " + sid + " |"):
            parts = ln.split("|")
            assert len(parts) == 13, (sid, len(parts), ln[:80])
            parts[8] = " " + status + " "
            ln = "|".join(parts)
            hit = True
        out.append(ln)
    assert hit, "SETUP_MISS status row " + sid
    open(path, "w", encoding="utf-8").write("\n".join(out))


def caseg(d):
    path = os.path.join(d, "corpus", "knowledge", "search-transparency-reporting-r84.md")
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")

    def span(ls):
        on, s, e = False, None, None
        for i, ln in enumerate(ls):
            if ln.startswith("## "):
                if on and s is not None:
                    e = i
                    break
                on = ln.strip() == "## Located quotes"
                if on:
                    s = i + 1
        return s, (e if e is not None else len(ls))

    s_, e_ = span(lines)
    q13, out = None, []
    for i, ln in enumerate(lines):
        if s_ is not None and s_ <= i < e_ and re.match(r"^\s*\|\s*(Q\d+)", ln):
            if re.match(r"^\s*\|\s*Q10\s*\|", ln):
                continue
            if re.match(r"^\s*\|\s*Q13\s*\|", ln):
                q13 = ln
        out.append(ln)
    assert q13 is not None, "SETUP_MISS caseG Q13"
    s2, e2 = span(out)
    out[e2:e2] = [re.sub(r"Q13", "Q14", q13, count=1)]
    open(path, "w", encoding="utf-8").write("\n".join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--receipts", required=True)
    a = ap.parse_args()
    r = Runner(os.path.abspath(a.tree), os.path.abspath(a.repo),
               os.path.abspath(a.work), os.path.abspath(a.receipts))

    # pinned bytes
    r.run([sys.executable, "-B", "-c",
           "import hashlib,sys\n"
           "for p in sys.argv[1:]:\n"
           "    print(hashlib.sha256(open(p,'rb').read()).hexdigest(), p)\n",
           r.c1, r.c2, r.tool], "pinned-bytes",
          "pristine instrument bytes at the tree under test (compare corpus/evidence/round88/instrument-pins.txt)")

    # baselines
    r.counter_run("c1", r.c1, "base-c1")
    r.counter_run("c2", r.c2, "base-c2")

    # the six existing shapes of mutate-r88.py, re-run through this executor (control)
    spec = importlib.util.spec_from_file_location("mutate_r88", os.path.join(r.tree, "corpus", "evidence",
                                                                             "round88", "mutate-r88.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for mid, area, old, new in mod.COUNTER_MUTANTS:
        r.counter_run("c1", r.c1, "existing-" + mid, edits=[(old, new)])

    # NEW counter shapes
    for mid, area, edits in C1_NEW:
        got = r.counter_run("c1", r.c1, "c1-" + mid, edits=edits)
        if got is None:
            print(f"SETUP_MISS {mid} ({area}): anchor not found")
    for mid, area, edits in C2_NEW:
        got = r.counter_run("c2", r.c2, "c2-" + mid, edits=edits)
        if got is None:
            print(f"SETUP_MISS {mid} ({area}): anchor not found")

    # subject-tool shapes against the pristine counter
    for mid, area, old, new in TOOL_NEW:
        r.tool_mutant(mid, old, new)

    # ---------------- probes ----------------
    pdir = os.path.join(r.work, "probes")
    os.makedirs(pdir, exist_ok=True)

    # C1 probe: a mirror of the landing tree with the S022 203 row demoted to 204 (two 203 pairs remain)
    p1 = mirror_c1(r.tree, os.path.join(pdir, "P1-narrow-203"))
    ref = os.path.join(p1, "corpus", "evidence", "round57", "refetch.tsv")
    txt = open(ref, encoding="utf-8").read().split("\n")
    for i, ln in enumerate(txt):
        if ln.startswith("S022\t") and "\t203\t" in ln:
            txt[i] = ln.replace("\t203\t", "\t204\t", 1)
    open(ref, "w", encoding="utf-8").write("\n".join(txt))
    r.counter_run("c1", r.c1, "probe-P1-base", root=p1)
    r.counter_run("c1", r.c1, "probe-P1-J1-pins-both", edits=C1_NEW[6][2], root=p1)
    r.counter_run("c1", r.c1, "probe-P1-J2-ok-detached", edits=C1_NEW[7][2], root=p1)
    r.counter_run("c1", r.c1, "probe-P1-N1-pin-drop", edits=C1_NEW[0][2], root=p1)
    r.counter_run("c1", r.c1, "probe-P1-N6-pin-drop", edits=C1_NEW[5][2], root=p1)

    # C1 probe tools
    tier = os.path.join(r.work, PROBE_TOOL_TIER_WRONG[0])
    os.makedirs(os.path.dirname(tier), exist_ok=True)
    src = apply_edits(open(r.tool, encoding="utf-8").read(), [(PROBE_TOOL_TIER_WRONG[1], PROBE_TOOL_TIER_WRONG[2])])
    assert src is not None, "SETUP_MISS probe TIER-WRONG"
    open(tier, "w", encoding="utf-8").write(src)
    r.counter_run("c1", r.c1, "probe-P2-tier-wrong-base", tool=tier)
    r.counter_run("c1", r.c1, "probe-P2-tier-wrong-N2", edits=C1_NEW[1][2], tool=tier)

    d1w = os.path.join(r.work, PROBE_TOOL_D1_WRONG[0])
    src = apply_edits(open(r.tool, encoding="utf-8").read(), [(PROBE_TOOL_D1_WRONG[1], PROBE_TOOL_D1_WRONG[2])])
    assert src is not None, "SETUP_MISS probe D1-WRONG-CODE"
    open(d1w, "w", encoding="utf-8").write(src)
    r.counter_run("c1", r.c1, "probe-P2b-d1-wrong-base", tool=d1w)
    r.counter_run("c1", r.c1, "probe-P2b-d1-wrong-N2", edits=C1_NEW[1][2], tool=d1w)
    r.counter_run("c1", r.c1, "probe-P2b-d1-wrong-N3", edits=C1_NEW[2][2], tool=d1w)

    gate203 = os.path.join(r.work, PROBE_TOOL_203_GATE[0])
    src = apply_edits(open(r.tool, encoding="utf-8").read(), [(PROBE_TOOL_203_GATE[1], PROBE_TOOL_203_GATE[2])])
    assert src is not None, "SETUP_MISS probe ADMIT-203-GATE"
    open(gate203, "w", encoding="utf-8").write(src)
    r.counter_run("c1", r.c1, "probe-P4-admit-203-gate-base", tool=gate203)
    r.counter_run("c1", r.c1, "probe-P4-admit-203-gate-N5", edits=C1_NEW[4][2], tool=gate203)

    # P3 probe instrument: E4-detached SETUP leg, base vs N4 reconcile-ignore
    r.counter_run("c1", r.c1, "probe-P3-detached-instrument-base", edits=PROBE_INSTRUMENT_E4)
    r.counter_run("c1", r.c1, "probe-P3-detached-instrument-N4",
                  edits=PROBE_INSTRUMENT_E4 + C1_NEW[3][2])

    # ---------------- C2 probes ----------------
    def c2_probe(tag, edits):
        d = mirror_c2(r.tree, os.path.join(pdir, tag))
        edits(d)
        return d

    def b1b(d):
        p = os.path.join(d, "corpus", "knowledge", "provenance-recording-r85.md")
        s = open(p, encoding="utf-8").read()
        assert "| Q1 (S215) |" in s
        open(p, "w", encoding="utf-8").write(s.replace("| Q1 (S215) |", "| Q1, Q3 (S215) |", 1))

    def a1d(d):
        p = os.path.join(d, "corpus", "knowledge", "search-transparency-reporting-r84.md")
        s = open(p, encoding="utf-8").read()
        n = re.sub(r'^\|\s*Q11\s*\|.*$', '| Q11 | S023 | "range" |', s, count=1, flags=re.M)
        assert n != s
        open(p, "w", encoding="utf-8").write(n)

    def emptyq10(d):
        p = os.path.join(d, "corpus", "knowledge", "search-transparency-reporting-r84.md")
        s = open(p, encoding="utf-8").read()
        n = re.sub(r'^\|\s*Q10\s*\|.*$', '| Q10 | S023 | |', s, count=1, flags=re.M)
        assert n != s
        open(p, "w", encoding="utf-8").write(n)

    def q13_other(d):
        p = os.path.join(d, "corpus", "knowledge", "search-transparency-reporting-r84.md")
        s = open(p, encoding="utf-8").read()
        old = '| Q13 | S023 | "Date on which the resource was changed." |'
        new = ('| Q13 | S023 | "Recommended practice is to describe the date, date/time, or period of time '
               'as recommended for the property Date, of which this is a subproperty." |')
        assert old in s
        s = s.replace(old, new, 1)
        oldd = "| state the date on which the resource was changed |"
        newd = "| state the date on which the property was changed |"
        assert oldd in s
        open(p, "w", encoding="utf-8").write(s.replace(oldd, newd, 1))

    def prov_modified(d):
        p = os.path.join(d, "corpus", "knowledge", "provenance-recording-r85.md")
        s = open(p, encoding="utf-8").read()
        old = "| record a resource with no derivation link when the chain's entities are known |"
        new = "| record a resource with no derivation link when the chain's entities are known, or one that was modified |"
        assert old in s
        open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))

    def f2(d):
        set_status(os.path.join(d, "corpus", "SOURCES.md"), "S031", "rejected")

    def f2b(d):
        set_status(os.path.join(d, "corpus", "SOURCES.md"), "S024", "rejected")
        set_status(os.path.join(d, "corpus", "SOURCES.md"), "S031", "rejected")

    def sup(d):
        set_status(os.path.join(d, "corpus", "SOURCES.md"), "S021", "mined")
        set_status(os.path.join(d, "corpus", "SOURCES.md"), "S032", "rejected")

    cases = [
        ("P-B1b", b1b, [("base", None), ("M1", C2_NEW[0][2])]),
        ("P-caseG", caseg, [("base", None), ("M2", C2_NEW[1][2])]),
        ("P-A1d", a1d, [("base", None), ("M3", C2_NEW[2][2])]),
        ("P-emptyQ10", emptyq10, [("base", None), ("M4", C2_NEW[3][2])]),
        ("P-F2", f2, [("base", None), ("M5", C2_NEW[4][2])]),
        ("P-F2b", f2b, [("base", None), ("M5", C2_NEW[4][2])]),
        ("P-defcited", q13_other, [("base", None), ("M6", C2_NEW[5][2])]),
        ("P-provmodified", prov_modified, [("base", None), ("M7", C2_NEW[6][2])]),
        ("P-sup", sup, [("base", None), ("M8", C2_NEW[7][2])]),
    ]
    for tag, edit, muts in cases:
        d = c2_probe(tag, edit)
        for label, me in muts:
            r.counter_run("c2", r.c2, f"probe-{tag}-{label}",
                          edits=me, root=d)

    print(r.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""gate-records-r83 — round-83 C2 (operability) counter, frozen before the candidate tool is committed.

Usage:
    python3 -B corpus/evidence/round83/gate-records-r83.py --root DIR --repo GITDIR [--tool PATH] [--work DIR]

DIR is a lane tree (`git archive <rev>` extracted). GITDIR is a git repository holding the lane's history (the lane
checkout; read-only `git cat-file` by the tool only). --tool defaults to DIR/tools/gate-records.py; the override exists
only to score the frozen stub controls. --work (default $TMPDIR, else $HYAKU_SCRATCH, else /fast/scratch/hyaku) holds
the generated forgery files in a fresh mkdtemp directory, removed on exit.

Subject: `python3 <tool> verify --root DIR --repo GITDIR FILE...`, whose output contract is
    GATE_RECORD <file>:<line> <S-id|?> OK | FAIL <CODE>[,<CODE>...]     and exit 0 / 1 / 2.

Battery (all frozen here or in corpus/evidence/round83/c2-positives.tsv):
  P  positives — the 15 GATE-RECORD lines of corpus/lessons/round-80.md, -81.md, -82.md listed in c2-positives.tsv.
     The tool is run on those three lesson files in DIR. A positive scores when the lesson line in DIR is byte-equal
     to the frozen copy and the tool prints `OK` for that file:line. Tool exit must be 0.
  F  forgeries — every mutation below applied to every positive of its form, each forged line written alone into its
     own file f<index>.md (neutral names, no class in the name), all files given to one tool run. A forgery scores
     REFUSED when the tool prints FAIL for that file:line, and EXPECTED_CODE when the printed code list contains the
     mutation's expected code. Tool exit must be 1.
  E  empty — one file with no GATE-RECORD line; the tool must exit 1 (no records is not a pass).

Output:
    TOOL=present|absent POSITIVE=a/15 FORGED_REFUSED=b/N EXPECTED_CODE=c/N EMPTY_REFUSED=e/1 RC=r/3
    GATE_RECORDS_R83=PASS|FAIL
PASS iff POSITIVE=15/15, FORGED_REFUSED=N/N, EXPECTED_CODE=N/N, EMPTY_REFUSED=1/1 and RC=3/3. Exit 0 PASS, 1 FAIL,
2 usage. Writes only inside its own --work mkdtemp directory.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
POS_TSV = os.path.join(HERE, "c2-positives.tsv")


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def form_of(line):
    if " rev=" in line:
        return "rev"
    if " capture=none " in line:
        return "unreach"
    return "admit"


def kv_set(line, key, val):
    return re.sub(r"(?<= )" + re.escape(key) + r"=\S+", key + "=" + val, line, count=1)


def kv_get(line, key):
    m = re.search(r"(?<= )" + re.escape(key) + r"=(\S+)", line)
    return m.group(1) if m else None


def quote_of(line, form):
    q = line.split(" quote=", 1)[1]
    return q[1:-1] if form == "admit" else q


def with_quote(line, form, q):
    head = line.split(" quote=", 1)[0]
    return head + " quote=" + ('"' + q + '"' if form == "admit" else q)


def flip_hex(h):
    return ("0" if h[0] != "0" else "1") + h[1:]


def mutations(pos, root):
    """Yield (label, forged_line, expected_code) for one positive (file, line, sid, raw)."""
    _, _, sid, raw = pos
    form = form_of(raw)
    out = []
    if form == "admit":
        q = quote_of(raw, form)
        words = q.split()
        out.append(("M01-unknown-id", raw.replace("GATE-RECORD " + sid, "GATE-RECORD S999", 1), "REGISTRY"))
        tier = kv_get(raw, "tier")
        out.append(("M02-tier", kv_set(raw, "tier", "B" if tier != "B" else "A"), "TIER"))
        out.append(("M03-other-capture", None, "CAPTURE_KEY"))  # filled by caller
        out.append(("M04-capture-traversal", kv_set(raw, "capture", "corpus/captures/../SOURCES.md"), "CAPTURE_PATH"))
        cs = kv_get(raw, "capture_sha256")
        out.append(("M05-sha-flip", kv_set(raw, "capture_sha256", flip_hex(cs)), "CAPTURE_SHA"))
        out.append(("M06-sha-short", kv_set(raw, "capture_sha256", cs[:8]), "CAPTURE_SHA"))
        ts = kv_get(raw, "fetched")
        sec = int(ts[17:19])
        out.append(("M07-fetched", kv_set(raw, "fetched", ts[:17] + "%02d" % ((sec + 1) % 60) + "Z"), "REFETCH"))
        out.append(("M08-quote-word", with_quote(raw, form, " ".join(["Zyzzyva"] + words[1:])), "QUOTE_ABSENT"))
        out.append(("M09-words-plus", kv_set(raw, "words", str(len(words) + 1)), "WORDS"))
        out.append(("M10-quote-drop-last", with_quote(raw, form, " ".join(words[:-1])), "WORDS"))
        cap = os.path.join(root, kv_get(raw, "capture"))
        text = norm(open(cap, encoding="utf-8", errors="replace").read())
        i = text.find(norm(q))
        tail = text[i + len(norm(q)):].split() if i >= 0 else []
        long_q = " ".join(norm(q).split() + tail[: max(0, 26 - len(words))])
        out.append(("M11-quote-26", kv_set(with_quote(raw, form, long_q), "words", str(len(long_q.split()))),
                    "QUOTE_LEN"))
        out.append(("M12-quote-empty", kv_set(with_quote(raw, form, ""), "words", "0"), "QUOTE_LEN"))
        out.append(("M13-url-changed", kv_set(raw, "url", kv_get(raw, "url") + "?x=1"), "CAPTURE_KEY"))
        out.append(("M14-indented-bad-quote", "  " + with_quote(raw, form, " ".join(["Zyzzyva"] + words[1:])),
                    "QUOTE_ABSENT"))
        out.append(("M15-no-quote-key", raw.split(" quote=", 1)[0], "PARSE"))
        out.append(("M16-dup-key", raw.replace(" tier=", " tier=%s tier=" % tier, 1), "PARSE"))
        out.append(("M17-id-swap", None, "REFETCH"))  # filled by caller
    elif form == "unreach":
        out.append(("U01-success-claimed", kv_set(kv_set(raw, "http", "200"), "curl_rc", "0"), "REFETCH"))
        ts = kv_get(raw, "fetched")
        sec = int(ts[17:19])
        out.append(("U02-fetched", kv_set(raw, "fetched", ts[:17] + "%02d" % ((sec + 1) % 60) + "Z"), "REFETCH"))
        out.append(("U03-http", kv_set(raw, "http", "404" if kv_get(raw, "http") != "404" else "410"), "REFETCH"))
        out.append(("U04-admit-without-capture", kv_set(raw, "decision", "admit"), "PARSE"))
    else:
        q = quote_of(raw, form)
        words = q.split()
        ln = int(kv_get(raw, "line"))
        out.append(("R01-line-next", kv_set(raw, "line", str(ln + 1)), "LINE"))
        out.append(("R02-rev-zero", kv_set(raw, "rev", "0" * 40), "REV"))
        out.append(("R03-path-absent", kv_set(raw, "path", "corpus/no-such-file-r83.md"), "REV"))
        out.append(("R04-quote-word", with_quote(raw, form, " ".join(["Zyzzyva"] + words[1:])), "LINE"))
        out.append(("R05-words-plus", kv_set(raw, "words", str(len(words) + 1)), "WORDS"))
        out.append(("R06-line-far", kv_set(raw, "line", "99999"), "LINE"))
    return out


def run(tool, root, repo, files):
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", repo] + files,
                       capture_output=True, text=True)
    res = {}
    for ln in p.stdout.splitlines():
        m = re.match(r"^GATE_RECORD (\S+):(\d+) (\S+) (OK|FAIL)(?: (\S+))?$", ln)
        if m:
            res[(m.group(1), int(m.group(2)))] = (m.group(4), set((m.group(5) or "").split(",")) - {""})
    return p.returncode, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tool")
    ap.add_argument("--work")
    a = ap.parse_args()
    root, repo = os.path.abspath(a.root), os.path.abspath(a.repo)
    tool = os.path.abspath(a.tool) if a.tool else os.path.join(root, "tools", "gate-records.py")
    pos = []
    for ln in open(POS_TSV, encoding="utf-8"):
        f, n, raw = ln.rstrip("\n").split("\t", 2)
        sid = re.match(r"^\s*GATE-RECORD (S\d+)", raw).group(1)
        pos.append((f, int(n), sid, raw))
    total_forged = None
    work = a.work or os.environ.get("TMPDIR") or os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="gr83-", dir=work)
    try:
        # forgeries (built from the frozen positive copies; capture reads use DIR)
        forged = []
        admits = [p for p in pos if form_of(p[3]) == "admit"]
        for k, p in enumerate(pos):
            for label, line, code in mutations(p, root):
                if label == "M03-other-capture":
                    other = admits[(admits.index(p) + 1) % len(admits)][3]
                    line = kv_set(p[3], "capture", kv_get(other, "capture"))
                if label == "M17-id-swap":
                    other = admits[(admits.index(p) + 1) % len(admits)]
                    line = p[3].replace("GATE-RECORD " + p[2], "GATE-RECORD " + other[2], 1)
                    line = kv_set(line, "tier", kv_get(other[3], "tier"))
                forged.append((label, p[2], line, code))
        total_forged = len(forged)
        if not os.path.isfile(tool):
            print(f"TOOL=absent POSITIVE=0/{len(pos)} FORGED_REFUSED=0/{total_forged} EXPECTED_CODE=0/{total_forged} "
                  f"EMPTY_REFUSED=0/1 RC=0/3")
            print("GATE_RECORDS_R83=FAIL")
            return 1
        rc_ok = 0
        # P
        lessons = sorted({p[0] for p in pos})
        files = [os.path.join(root, f) for f in lessons]
        rc, res = run(tool, root, repo, files)
        rc_ok += rc == 0
        p_ok = 0
        for f, n, sid, raw in pos:
            path = os.path.join(root, f)
            try:
                cur = open(path, encoding="utf-8").read().split("\n")[n - 1]
            except (OSError, IndexError):
                cur = None
            if cur == raw and res.get((path, n), ("", set()))[0] == "OK":
                p_ok += 1
        # F
        ffiles = []
        for i, (label, sid, line, code) in enumerate(forged):
            fp = os.path.join(tmp, "f%03d.md" % i)
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(line + "\n")
            ffiles.append(fp)
        rc, res = run(tool, root, repo, ffiles)
        rc_ok += rc == 1
        refused = exp = 0
        for (label, sid, line, code), fp in zip(forged, ffiles):
            v = res.get((fp, 1))
            if v and v[0] == "FAIL":
                refused += 1
                if code in v[1]:
                    exp += 1
                else:
                    print(f"WRONG_CODE {os.path.basename(fp)} {label} {sid} expected={code} got={','.join(sorted(v[1]))}")
            else:
                print(f"NOT_REFUSED {os.path.basename(fp)} {label} {sid}")
        # E
        ep = os.path.join(tmp, "empty.md")
        with open(ep, "w", encoding="utf-8") as fh:
            fh.write("# no records here\n\nGATE-RECORDS are described in prose only.\n")
        rc, _ = run(tool, root, repo, [ep])
        e_ok = 1 if rc == 1 else 0
        rc_ok += rc == 1
        print(f"TOOL=present POSITIVE={p_ok}/{len(pos)} FORGED_REFUSED={refused}/{total_forged} "
              f"EXPECTED_CODE={exp}/{total_forged} EMPTY_REFUSED={e_ok}/1 RC={rc_ok}/3")
        passed = p_ok == len(pos) and refused == exp == total_forged and e_ok == 1 and rc_ok == 3
        print(f"GATE_RECORDS_R83={'PASS' if passed else 'FAIL'}")
        return 0 if passed else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

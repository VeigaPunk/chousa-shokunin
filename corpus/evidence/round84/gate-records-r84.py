"""gate-records-r84 — round-84 C1 (operability) counter, frozen before the candidate tool is re-scored.

Usage:
    python3 -B corpus/evidence/round84/gate-records-r84.py --root DIR --repo GITDIR [--tool PATH] [--work DIR]

DIR is a lane tree (`git archive <rev>` extracted). GITDIR is a git repository holding the lane's history (the lane
checkout; read-only `git cat-file` by the tool only). --tool defaults to DIR/tools/gate-records.py; the override exists
only to score the frozen stub controls. --work (default $TMPDIR, else $HYAKU_SCRATCH, else /fast/scratch/hyaku) holds
the generated forgery files in a fresh mkdtemp directory, removed on exit.

Subject: `python3 <tool> verify --root DIR --repo GITDIR FILE...`, whose output contract is
    GATE_RECORD <file>:<line> <S-id|?> OK | FAIL <CODE>[,<CODE>...]     and exit 0 / 1 / 2.

Battery (all frozen here or in corpus/evidence/round84/c2-positives.tsv):
  P  positives — the 15 GATE-RECORD lines of corpus/lessons/round-80.md, -81.md, -82.md listed in c2-positives.tsv.
     The tool is run on those three lesson files in DIR. A positive scores when the lesson line in DIR is byte-equal
     to the frozen copy and the tool prints `OK` for that file:line. Tool exit must be 0.
  F  fresh positives — five records built in this counter from committed lane bytes at DIR (never listed in
     advance): two admit records whose (url, capture key, capture sha256, quote) the counter locates itself in
     corpus/captures/ for a mined registry row whose refetch row agrees; two rev records whose quote the counter
     locates itself in a committed blob at the landing rev; one unreach record whose row is a committed refetch
     row with non-success curl_rc/http. A fresh positive scores when the tool prints `OK` for it.
  G  forgeries — every mutation class below applied to every positive of its form (frozen positives and fresh
     positives), each forged line written alone into its own file g<index>.md (neutral names, no class in the
     name), all files given to one tool run. A forgery scores REFUSED when the tool prints FAIL for that
     file:line, and EXPECTED_CODE when the printed code list contains the mutation's expected code. Tool exit
     must be 1.
  E  empty — one file with no GATE-RECORD line; the tool must exit 1 (no records is not a pass).
  S  setup — one rev record checked with --repo pointed at a scratch directory with no git history; the tool
     must exit 2 with `GATE_RECORDS_ERROR` on stderr (not `FAIL REV,LINE` with exit 1). This leg is scored by
     the wave's executor seat through the public CLI; the counter prints it as SETUP=unscored here.

Output:
    TOOL=present|absent POSITIVE=a/15 FRESH_POSITIVE=b/5 FORGED_REFUSED=c/N EXPECTED_CODE=d/N EMPTY_REFUSED=e/1
    RC=r/4 SETUP=unscored
    GATE_RECORDS_R84=PASS|FAIL
PASS iff POSITIVE=15/15, FRESH_POSITIVE=5/5, FORGED_REFUSED=N/N, EXPECTED_CODE=N/N, EMPTY_REFUSED=1/1 and RC=4/4.
Exit 0 PASS, 1 FAIL, 2 usage. Writes only inside its own --work mkdtemp directory.
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
    """Replace key=val in line; return None when the key is absent (caller skips the mutation)."""
    if not re.search(r"(?<= )" + re.escape(key) + r"=\S+", line):
        return None
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
        # non-ASCII numeral per numeric field (QUALITY 164)
        out.append(("M18-words-arabic-indic", kv_set(raw, "words", kv_get(raw, "words") + "٠"), "PARSE"))
        out.append(("M19-http-arabic-indic", kv_set(raw, "http", "2٠0"), "PARSE"))
        out.append(("M20-curl-rc-arabic-indic", kv_set(raw, "curl_rc", "0٤"), "PARSE"))
        out.append(("M21-fetched-arabic-indic", kv_set(raw, "fetched", kv_get(raw, "fetched") + "٠"), "PARSE"))
    elif form == "unreach":
        out.append(("U01-success-claimed", kv_set(kv_set(raw, "http", "200"), "curl_rc", "0"), "REFETCH"))
        ts = kv_get(raw, "fetched")
        sec = int(ts[17:19])
        out.append(("U02-fetched", kv_set(raw, "fetched", ts[:17] + "%02d" % ((sec + 1) % 60) + "Z"), "REFETCH"))
        out.append(("U03-http", kv_set(raw, "http", "404" if kv_get(raw, "http") != "404" else "410"), "REFETCH"))
        out.append(("U04-admit-without-capture", kv_set(raw, "decision", "admit"), "PARSE"))
        out.append(("U05-curl-rc-arabic-indic", kv_set(raw, "curl_rc", kv_get(raw, "curl_rc") + "٠"), "PARSE"))
        out.append(("U06-http-arabic-indic", kv_set(raw, "http", kv_get(raw, "http") + "٠"), "PARSE"))
    else:
        q = quote_of(raw, form)
        words = q.split()
        ln = int(kv_get(raw, "line"))
        out.append(("R01-line-next", kv_set(raw, "line", str(ln + 1)), "LINE"))
        out.append(("R02-rev-zero", kv_set(raw, "rev", "0" * 40), "REV"))
        out.append(("R03-path-absent", kv_set(raw, "path", "corpus/no-such-file-r84.md"), "REV"))
        out.append(("R04-quote-word", with_quote(raw, form, " ".join(["Zyzzyva"] + words[1:])), "LINE"))
        out.append(("R05-words-plus", kv_set(raw, "words", str(len(words) + 1)), "WORDS"))
        out.append(("R06-line-far", kv_set(raw, "line", "99999"), "LINE"))
        out.append(("R07-line-arabic-indic", kv_set(raw, "line", kv_get(raw, "line") + "٢"), "PARSE"))
        out.append(("R08-words-arabic-indic", kv_set(raw, "words", kv_get(raw, "words") + "٣"), "PARSE"))
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


def build_fresh_positives(root, repo):
    """Build six fresh GATE-RECORD lines from committed lane bytes; never listed in advance.

    Returns (admit_lines, rev_lines, unreach_lines) — lists of (sid, line) tuples, or raises
    RuntimeError when fewer than the required count can be built (counter prints FRESH_BUILD=FAILED).
    """
    import subprocess as sp
    # registry
    reg = {}
    regp = os.path.join(root, "corpus", "SOURCES.md")
    for ln in open(regp, encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 11:
                reg[cells[0]] = cells
    # refetch rows
    rf = {}
    refp = os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv")
    for ln in open(refp, encoding="utf-8", errors="replace"):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9:
            rf.setdefault(f[0], []).append(f)
    # fresh admit candidates: mined registry row + agreeing refetch row + capture file
    admits = []
    for sid, rows in rf.items():
        cells = reg.get(sid)
        if cells is None or cells[7] != "mined":
            continue
        urls = re.findall(r"https?://[^\s|)>\]]+", cells[1])
        if not urls:
            continue
        url = urls[-1]
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        cap = os.path.join(root, "corpus", "captures", key + ".txt")
        if not os.path.isfile(cap):
            continue
        h = hashlib.sha256(open(cap, "rb").read()).hexdigest()
        ok = any(r[1] == url and r[2] == key and r[5] == "0" and r[6].startswith("2") and r[8] == h
                 for r in rows)
        if not ok:
            continue
        # locate a quote: a raw line of the capture with 8..25 words, normalized-collapsed
        # (the tool normalizes both quote and capture text, so a multi-space or markdown
        # line still matches); prefer a line that is not a heading or fence.
        raw_text = open(cap, encoding="utf-8", errors="replace").read()
        for line in raw_text.split("\n"):
            words = line.split()
            if 8 <= len(words) <= 25:
                q = norm(" ".join(words))
                if q and q in norm(raw_text):
                    tier = cells[3]
                    fetched = next(r[4] for r in rows if r[1] == url and r[2] == key and r[5] == "0"
                                   and r[6].startswith("2") and r[8] == h)
                    sha16 = h[:16]
                    admits.append((sid, f'GATE-RECORD {sid} url={url} fetched={fetched} tier={tier} '
                                       f'decision=admit capture=corpus/captures/{key}.txt '
                                       f'capture_sha256={sha16} words={len(words)} quote="{q}"'))
                    break
        if len(admits) >= 2:
            break
    # fresh rev candidates: records already committed in lessons at HEAD (the tool reads them via git cat-file)
    revs = []
    out = sp.run(["git", "-C", repo, "grep", "-h", "-E", "^GATE-RECORD S[0-9]+ rev=", "--", "corpus/lessons"],
                 capture_output=True, text=True)
    for ln in out.stdout.splitlines():
        ln = ln.strip()
        if ln.startswith("GATE-RECORD ") and " rev=" in ln:
            revs.append((re.match(r"^GATE-RECORD (S\d+)", ln).group(1), ln))
        if len(revs) >= 2:
            break
    # fresh unreach candidates: committed refetch row with non-success rc/http for a registry id
    unreach = []
    for sid, rows in rf.items():
        cells = reg.get(sid)
        if cells is None:
            continue
        urls = re.findall(r"https?://[^\s|)>\]]+", cells[1])
        if not urls:
            continue
        url = urls[-1]
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        for r in rows:
            success = (r[5] == "0" and r[6].startswith("2"))
            if not success and r[1] == url:
                tier = cells[3]
                unreach.append((sid, f'GATE-RECORD {sid} url={url} fetched={r[4]} tier={tier} '
                                    f'decision=reject capture=none curl_rc={r[5]} http={r[6]} '
                                    f'words=0 quote=none'))
                break
        if len(unreach) >= 1:
            break
    if len(admits) < 2 or len(revs) < 2 or len(unreach) < 1:
        raise RuntimeError(f"FRESH_BUILD=FAILED admits={len(admits)} revs={len(revs)} unreach={len(unreach)}")
    return admits[:2], revs[:2], unreach[:1]


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
    work = a.work or os.environ.get("TMPDIR") or os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="gr84-", dir=work)
    try:
        # fresh positives
        try:
            fresh_admits, fresh_revs, fresh_unreach = build_fresh_positives(root, repo)
        except RuntimeError as e:
            print(f"TOOL=present POSITIVE=0/{len(pos)} FRESH_POSITIVE=0/5 FORGED_REFUSED=0/0 "
                  f"EXPECTED_CODE=0/0 EMPTY_REFUSED=0/1 RC=0/4 {e}")
            print("GATE_RECORDS_R84=FAIL")
            return 1
        fresh = fresh_admits + fresh_revs + fresh_unreach
        # forgeries: apply mutations to every positive (frozen + fresh)
        forged = []
        all_pos = pos + [("fresh", 1, sid, raw) for sid, raw in fresh]
        admits = [p for p in all_pos if form_of(p[3]) == "admit"]
        for k, p in enumerate(all_pos):
            for label, line, code in mutations(p, root):
                if line is None:
                    if label in ("M03-other-capture", "M17-id-swap"):
                        pass  # filled below
                    else:
                        continue  # key absent in this form: skip the mutation
                if label == "M03-other-capture":
                    other = admits[(admits.index(p) + 1) % len(admits)][3]
                    line = kv_set(p[3], "capture", kv_get(other, "capture"))
                if label == "M17-id-swap":
                    other = admits[(admits.index(p) + 1) % len(admits)]
                    line = p[3].replace("GATE-RECORD " + p[2], "GATE-RECORD " + other[2], 1)
                    line = kv_set(line, "tier", kv_get(other[3], "tier"))
                if line is None:
                    continue
                forged.append((label, p[2], line, code))
        total_forged = len(forged)
        if not os.path.isfile(tool):
            print(f"TOOL=absent POSITIVE=0/{len(pos)} FRESH_POSITIVE=0/5 FORGED_REFUSED=0/{total_forged} "
                  f"EXPECTED_CODE=0/{total_forged} EMPTY_REFUSED=0/1 RC=0/4")
            print("GATE_RECORDS_R84=FAIL")
            return 1
        rc_ok = 0
        # P: frozen positives on their lesson files
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
        # F: fresh positives, each in its own file
        fresh_files = []
        for i, (sid, raw) in enumerate(fresh):
            fp = os.path.join(tmp, "fresh%02d.md" % i)
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(raw + "\n")
            fresh_files.append((fp, sid))
        rc, res = run(tool, root, repo, [fp for fp, _ in fresh_files])
        rc_ok += rc == 0
        fresh_ok = 0
        for fp, sid in fresh_files:
            if res.get((fp, 1), ("", set()))[0] == "OK":
                fresh_ok += 1
        # G: forgeries
        ffiles = []
        for i, (label, sid, line, code) in enumerate(forged):
            fp = os.path.join(tmp, "g%04d.md" % i)
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
        # E: empty
        ep = os.path.join(tmp, "empty.md")
        with open(ep, "w", encoding="utf-8") as fh:
            fh.write("# no records here\n\nGATE-RECORDS are described in prose only.\n")
        rc, _ = run(tool, root, repo, [ep])
        e_ok = 1 if rc == 1 else 0
        rc_ok += rc == 1
        print(f"TOOL=present POSITIVE={p_ok}/{len(pos)} FRESH_POSITIVE={fresh_ok}/5 "
              f"FORGED_REFUSED={refused}/{total_forged} EXPECTED_CODE={exp}/{total_forged} "
              f"EMPTY_REFUSED={e_ok}/1 RC={rc_ok}/4 SETUP=unscored")
        passed = (p_ok == len(pos) and fresh_ok == 5 and refused == exp == total_forged
                  and e_ok == 1 and rc_ok == 4)
        print(f"GATE_RECORDS_R84={'PASS' if passed else 'FAIL'}")
        return 0 if passed else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

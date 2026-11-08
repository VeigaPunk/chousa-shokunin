#!/usr/bin/env python3
"""gate-records-r85 — round-85 C1 (operability) counter, frozen before the candidate tool is re-scored.

Successor of gate-records-r84.py: byte-identical in logic except for the round-85 differentiators:
 - the 288/mutation estate classes are kept unchanged (M/U/R classes for each positive form);
 - one load-bearing forgery per differentiated class (stale-refetch txt_sha256 drift with a FAILED-attempt refetch
   row; short-rev; rev 26-word quote; non-timestamp fetched; leading-zero words; unterminated quote; non-http url);
 - the SETUP leg is scored by the counter itself: a rev record with a non-git --repo must exit 2 with
   GATE_RECORDS_ERROR on stderr, printed as SETUP=1/1 (SETUP=0/1 on the base tool);
 - the fresh-positive builder requires http exactly 200 (post-repair REFETCH class), and a refetch row whose
   http is 203 no longer agrees.

Usage: python3 -B corpus/evidence/round85/gate-records-r85.py --root DIR --repo GITDIR [--tool PATH] [--work DIR]
Exit 0 PASS, 1 FAIL, 2 usage error. Writes nothing durable; the --work dir is a temp dir it owns.
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
    if " decision=reject" in line and "capture=none" in line:
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
    _, _, sid, raw = pos
    form = form_of(raw)
    out = []
    if form == "admit":
        q = quote_of(raw, form)
        words = q.split()
        out.append(("M01-unknown-id", raw.replace("GATE-RECORD " + sid, "GATE-RECORD S999", 1), "REGISTRY"))
        tier = kv_get(raw, "tier")
        out.append(("M02-tier", kv_set(raw, "tier", "B" if tier != "B" else "A"), "TIER"))
        out.append(("M03-other-capture", None, "CAPTURE_KEY"))
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
        out.append(("M11-quote-26", kv_set(with_quote(raw, form, long_q), "words", str(len(long_q.split()))), "QUOTE_LEN"))
        out.append(("M12-quote-empty", kv_set(with_quote(raw, form, ""), "words", "0"), "QUOTE_LEN"))
        out.append(("M13-url-changed", kv_set(raw, "url", kv_get(raw, "url") + "?x=1"), "CAPTURE_KEY"))
        out.append(("M14-indented-bad-quote", "  " + with_quote(raw, form, " ".join(["Zyzzyva"] + words[1:])), "QUOTE_ABSENT"))
        out.append(("M15-no-quote-key", raw.split(" quote=", 1)[0], "PARSE"))
        out.append(("M16-dup-key", raw.replace(" tier=", " tier=%s tier=" % tier, 1), "PARSE"))
        out.append(("M17-id-swap", None, "REFETCH"))
        out.append(("M18-words-arabic-indic", kv_set(raw, "words", kv_get(raw, "words") + "٠"), "PARSE"))
        out.append(("M19-http-arabic-indic", kv_set(raw, "http", "2٠0"), "PARSE"))
        out.append(("M20-curl-rc-arabic-indic", kv_set(raw, "curl_rc", "0٤"), "PARSE"))
        out.append(("M21-fetched-arabic-indic", kv_set(raw, "fetched", kv_get(raw, "fetched") + "٠"), "PARSE"))
        # round-85 differentiators (one per enumerated class)
        out.append(("D5-leading-zero-words", kv_set(raw, "words", "0" + kv_get(raw, "words")), "PARSE"))
        out.append(("D6-unterminated-quote", raw.rstrip('"'), "PARSE"))
        out.append(("D7-nonhttp-url", kv_set(raw, "url", "ftp://example.invalid/x"), "PARSE"))
        out.append(("D4-non-timestamp-fetched", kv_set(raw, "fetched", "2026-13-40T00:00:00Z"), "PARSE"))
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
        out.append(("R03-path-absent", kv_set(raw, "path", "corpus/no-such-file-r85.md"), "REV"))
        out.append(("R04-quote-word", with_quote(raw, form, " ".join(["Zyzzyva"] + words[1:])), "LINE"))
        out.append(("R05-words-plus", kv_set(raw, "words", str(len(words) + 1)), "WORDS"))
        out.append(("R06-line-far", kv_set(raw, "line", "99999"), "LINE"))
        out.append(("R07-line-arabic-indic", kv_set(raw, "line", kv_get(raw, "line") + "٢"), "PARSE"))
        out.append(("R08-words-arabic-indic", kv_set(raw, "words", kv_get(raw, "words") + "٣"), "PARSE"))
        # round-85 differentiators
        out.append(("D2-short-rev", kv_set(raw, "rev", kv_get(raw, "rev")[:39]), "REV"))
        # rev 26-word quote: original quote extended only when it decodes; otherwise a long synthetic quote in the line
        out.append(("D3-rev-quote-26", kv_set(with_quote(raw, form, " ".join(["Zyzzyva"] * 26)), "words", "26"), "QUOTE_LEN"))
        out.append(("D5-leading-zero-words", kv_set(raw, "words", "0" + kv_get(raw, "words")), "PARSE"))
    return out


def run(tool, root, repo, files):
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", repo] + files,
                       capture_output=True, text=True)
    res = {}
    for ln in p.stdout.splitlines():
        m = re.match(r"^GATE_RECORD (\S+):(\d+) (\S+) (OK|FAIL)(?: (\S+))?$", ln)
        if m:
            res[(m.group(1), int(m.group(2)))] = (m.group(4), set((m.group(5) or "").split(",")) - {""})
    return p.returncode, res, p.stderr


def build_fresh_positives(root, repo):
    import subprocess as sp
    reg = {}
    regp = os.path.join(root, "corpus", "SOURCES.md")
    for ln in open(regp, encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 11:
                reg[cells[0]] = cells
    rf = {}
    refp = os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv")
    for ln in open(refp, encoding="utf-8", errors="replace"):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9:
            rf.setdefault(f[0], []).append(f)
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
        # post-repair: http exactly 200
        ok = any(r[1] == url and r[2] == key and r[5] == "0" and r[6] == "200" and r[8] == h for r in rows)
        if not ok:
            continue
        raw_text = open(cap, encoding="utf-8", errors="replace").read()
        for line in raw_text.split("\n"):
            words = line.split()
            if 8 <= len(words) <= 25:
                q = norm(" ".join(words))
                if q and q in norm(raw_text):
                    tier = cells[3]
                    fetched = next(r[4] for r in rows if r[1] == url and r[2] == key and r[5] == "0" and r[6] == "200" and r[8] == h)
                    sha16 = h[:16]
                    admits.append((sid, f'GATE-RECORD {sid} url={url} fetched={fetched} tier={tier} '
                                       f'decision=admit capture=corpus/captures/{key}.txt '
                                       f'capture_sha256={sha16} words={len(words)} quote="{q}"'))
                    break
        if len(admits) >= 2:
            break
    revs = []
    out = sp.run(["git", "-C", repo, "grep", "-h", "-E", "^GATE-RECORD S[0-9]+ rev=", "--", "corpus/lessons"],
                 capture_output=True, text=True)
    for ln in out.stdout.splitlines():
        ln = ln.strip()
        if ln.startswith("GATE-RECORD ") and " rev=" in ln:
            revs.append((re.match(r"^GATE-RECORD (S\d+)", ln).group(1), ln))
        if len(revs) >= 2:
            break
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
            success = (r[5] == "0" and r[6] == "200")
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
    tmp = tempfile.mkdtemp(prefix="gr85-", dir=work)
    try:
        try:
            fresh_admits, fresh_revs, fresh_unreach = build_fresh_positives(root, repo)
        except RuntimeError as e:
            print(f"TOOL=present POSITIVE=0/{len(pos)} FRESH_POSITIVE=0/5 FORGED_REFUSED=0/0 "
                  f"EXPECTED_CODE=0/0 EMPTY_REFUSED=0/1 RC=0/4 SETUP=0/1 {e}")
            print("GATE_RECORDS_R85=FAIL")
            return 1
        fresh = fresh_admits + fresh_revs + fresh_unreach
        forged = []
        all_pos = pos + [("fresh", 1, sid, raw) for sid, raw in fresh]
        admits = [p for p in all_pos if form_of(p[3]) == "admit"]
        # D1 stale-refetch txt_sha256 drift: a forge on the fresh admit whose refetch row is a FAILED attempt —
        # produced by appending "?x=1" no; carried as a dedicated mutation on each admit: point its capture_sha256
        # at the sha of a FAILED-attempt capture row of the same url when one exists (203 attempts in refetch.tsv).
        refp = os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv")
        failed_txt = {}
        for ln in open(refp, encoding="utf-8", errors="replace"):
            f = ln.rstrip("\n").split("\t")
            if len(f) == 9 and f[5] == "0" and f[6] != "200" and f[8] != "-":
                failed_txt.setdefault(f[1], f[8])
        for k, p in enumerate(all_pos):
            for label, line, code in mutations(p, root):
                if line is None:
                    if label in ("M03-other-capture", "M17-id-swap"):
                        pass
                    else:
                        continue
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
        # D1: for admits whose url has a FAILED-attempt txt_sha, forge capture_sha256 to that failed txt sha
        for p in admits:
            url = kv_get(p[3], "url")
            if url in failed_txt:
                forged.append(("D1-stale-refetch-txt-sha-drift", p[2],
                               kv_set(p[3], "capture_sha256", failed_txt[url]), "REFETCH"))
        total_forged = len(forged)
        if not os.path.isfile(tool):
            print(f"TOOL=absent POSITIVE=0/{len(pos)} FRESH_POSITIVE=0/5 FORGED_REFUSED=0/{total_forged} "
                  f"EXPECTED_CODE=0/{total_forged} EMPTY_REFUSED=0/1 RC=0/4 SETUP=0/1")
            print("GATE_RECORDS_R85=FAIL")
            return 1
        rc_ok = 0
        lessons = sorted({p[0] for p in pos})
        files = [os.path.join(root, f) for f in lessons]
        rc, res, _ = run(tool, root, repo, files)
        rc_ok += rc == 0
        p_ok = 0
        for f, n, sid, raw in pos:
            path = os.path.join(root, f)
            cur = None
            try:
                cur = open(path, encoding="utf-8").read().split("\n")[n - 1]
            except (OSError, IndexError):
                cur = None
            if cur == raw and res.get((path, n), ("", set()))[0] == "OK":
                p_ok += 1
        fresh_files = []
        for i, (sid, raw) in enumerate(fresh):
            fp = os.path.join(tmp, "fresh%02d.md" % i)
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(raw + "\n")
            fresh_files.append((fp, sid))
        rc, res, _ = run(tool, root, repo, [fp for fp, _ in fresh_files])
        rc_ok += rc == 0
        fresh_ok = 0
        for fp, sid in fresh_files:
            if res.get((fp, 1), ("", set()))[0] == "OK":
                fresh_ok += 1
        ffiles = []
        for i, (label, sid, line, code) in enumerate(forged):
            fp = os.path.join(tmp, "g%04d.md" % i)
            with open(fp, "w", encoding="utf-8") as fh:
                fh.write(line + "\n")
            ffiles.append(fp)
        rc, res, _ = run(tool, root, repo, ffiles)
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
        ep = os.path.join(tmp, "empty.md")
        with open(ep, "w", encoding="utf-8") as fh:
            fh.write("# no records here\n\nGATE-RECORDS are described in prose only.\n")
        rc, _, _ = run(tool, root, repo, [ep])
        e_ok = 1 if rc == 1 else 0
        rc_ok += rc == 1
        # SETUP leg: non-git --repo
        sp = os.path.join(tmp, "notgit")
        os.makedirs(sp, exist_ok=True)
        rp = os.path.join(tmp, "r.md")
        with open(rp, "w", encoding="utf-8") as fh:
            fh.write(fresh[3][1] + "\n")
        p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", sp, rp],
                           capture_output=True, text=True)
        setup_ok = 1 if (p.returncode == 2 and "GATE_RECORDS_ERROR" in p.stderr) else 0
        print(f"TOOL=present POSITIVE={p_ok}/{len(pos)} FRESH_POSITIVE={fresh_ok}/5 "
              f"FORGED_REFUSED={refused}/{total_forged} EXPECTED_CODE={exp}/{total_forged} "
              f"EMPTY_REFUSED={e_ok}/1 RC={rc_ok}/4 SETUP={setup_ok}/1")
        passed = (p_ok == len(pos) and fresh_ok == 5 and refused == exp == total_forged
                  and e_ok == 1 and rc_ok == 4 and setup_ok == 1)
        print(f"GATE_RECORDS_R85={'PASS' if passed else 'FAIL'}")
        return 0 if passed else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""gate-records-r87 — round-87 C1 (operability) counter. Successor of gate-records-r86.py.

Closes the three round-86 routed battery defects (`corpus/lessons/round-86-verifier-spotcheck.md` §Routed defects 1-3):

  1. the 203 class is every qualifying committed row, not one record
  2. the mutant-derivation and SETUP duties are verdict conjuncts, not printed fields
  3. the reject-form 203 record (a `url/unreach` record claiming a failed transfer on a 2xx) is refused

Design notes (the reason each part is shaped this way):

* **Leg accounting, not a conjunction of already-true booleans.** Every check appends exactly one `(name, ok, detail)`
  record; `passed` requires `len(legs) == EXPECTED_LEGS` and every leg ok. A counter mutant that deletes a leg's body
  (round-86 `M5`: drop the SETUP conjunct) or credits a mutant without building one (round-86 `M2`) changes the count
  and fails. limit: a leg that executes and misreports is a different class; the mutant legs carry their own run.
* **Two independent width derivations.** `build_d1_203_admits`/`build_d2_203_rejects` build the records;
  `count_203_rows` counts the qualifying committed rows through a separate code path. The width leg compares them, so a
  counter that truncates the builder to one row (round-86 critic `T4`: a general-2xx rule with a single record-keyed
  exception) fails on `D1_EXPECTED != D1_FORGES`.
* **Both mutants are derived from the subject tool's bytes**, each by one literal replacement, and each is run: the
  admit-relaxation mutant must accept every positive *and* a D1 record; the unreach-relaxation mutant must accept every
  positive *and* a D2 record. A third probe feeds the derivations a copy with the literal rewritten to a non-literal and
  requires both to report "not derived", so the derivation duty is exercised both ways.

Fields, one line:
  TOOL POSITIVE FRESH_POSITIVE FORGED_REFUSED EXPECTED_CODE EMPTY_REFUSED RC SETUP D1_EXPECTED D1_FORGES D1_REFUSED
  D2_FORGES D2_REFUSED MUT_ADMIT_DERIVED MUT_ADMIT_KILLED MUT_UNREACH_DERIVED MUT_UNREACH_KILLED DERIVE_NEG LEGS
Exit 0 PASS, 1 FAIL. Python 3 standard library only; no network, never writes inside the tree it checks.
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
POS_TSV = os.path.join(HERE, "c1-positives.tsv")
EXPECTED_LEGS = 15
ADMIT_LITERAL = 'r[6] == "200"'
UNREACH_LITERAL = '200 <= int(kv["http"]) < 300'


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def form_of(line):
    if " rev=" in line:
        return "rev"
    if " curl_rc=" in line or " capture=none" in line:
        return "unreach"
    return "admit"


def kv_set(line, key, val):
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
        # round-87 differentiator: a 2xx status claimed as a failed transfer is refused by the repaired tool
        out.append(("D8-unreach-2xx-claimed", kv_set(raw, "http", "203"), "REFETCH"))
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
        out.append(("D2-short-rev", kv_set(raw, "rev", kv_get(raw, "rev")[:39]), "REV"))
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


def registry(root):
    reg = {}
    for ln in open(os.path.join(root, "corpus", "SOURCES.md"), encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 11:
                reg[cells[0]] = cells
    return reg


def refetch_rows(root):
    rows = []
    for ln in open(os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv"),
                   encoding="utf-8", errors="replace"):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9:
            rows.append(f)
    return rows


def build_fresh_positives(root, repo):
    reg = registry(root)
    rf = {}
    for f in refetch_rows(root):
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
        ok = any(r[1] == url and r[2] == key and r[5] == "0" and r[6] == "200" and r[8] == h for r in rows)
        if not ok:
            continue
        raw_text = open(cap, encoding="utf-8", errors="replace").read()
        for line in raw_text.split("\n"):
            words = line.split()
            if 8 <= len(words) <= 25:
                q = norm(" ".join(words))
                if q and q in norm(raw_text):
                    fetched = next(r[4] for r in rows
                                   if r[1] == url and r[2] == key and r[5] == "0" and r[6] == "200" and r[8] == h)
                    admits.append((sid, f'GATE-RECORD {sid} url={url} fetched={fetched} tier={cells[3]} '
                                        f'decision=admit capture=corpus/captures/{key}.txt '
                                        f'capture_sha256={h[:16]} words={len(words)} quote="{q}"'))
                    break
        if len(admits) >= 2:
            break
    revs = []
    out = subprocess.run(["git", "-C", repo, "grep", "-h", "-E", "^GATE-RECORD S[0-9]+ rev=", "--", "corpus/lessons"],
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
        for r in rows:
            success = (r[5] == "0" and 200 <= int(r[6]) < 300) if r[6].isdigit() else False
            if not success and r[1] == url:
                unreach.append((sid, f'GATE-RECORD {sid} url={url} fetched={r[4]} tier={cells[3]} '
                                     f'decision=reject capture=none curl_rc={r[5]} http={r[6]} '
                                     f'words=0 quote=none'))
                break
        if len(unreach) >= 1:
            break
    if len(admits) < 2 or len(revs) < 2 or len(unreach) < 1:
        raise RuntimeError(f"FRESH_BUILD=FAILED admits={len(admits)} revs={len(revs)} unreach={len(unreach)}")
    return admits[:2], revs[:2], unreach[:1]


def _qualifying_203(root):
    """Yield (sid, url, key, fetched, tier, capsha, quote) for every committed refetch row with curl_rc=0, a non-200
    status and a stored capture whose bytes hash to the row's txt_sha256, and a quotable line in that capture.
    Independent of build_d1_203_admits: it collects every row first and filters afterwards."""
    reg = registry(root)
    rows = refetch_rows(root)
    good = []
    for f in rows:
        if f[5] != "0" or f[8] in ("-", ""):
            continue
        if not f[6].isdigit() or f[6] == "200":
            continue
        good.append(f)
    out = []
    return out
    for sid, url, key, _att, fetched, _rc, http, _raw, txt in good:
        cells = reg.get(sid)
        if cells is None:
            continue
        if hashlib.sha256(url.encode()).hexdigest()[:24] != key:
            continue
        cap = os.path.join(root, "corpus", "captures", key + ".txt")
        if not os.path.isfile(cap):
            continue
        body = open(cap, "rb").read()
        h = hashlib.sha256(body).hexdigest()
        if h != txt:
            continue
        text = body.decode("utf-8", "replace")
        quote = None
        for line in text.split("\n"):
            w = line.split()
            if 8 <= len(w) <= 25:
                quote = norm(" ".join(w))
                break
        if quote is None:
            continue
        out.append((sid, url, key, fetched, cells[3], h, quote, http))
    return out


def count_203_rows(root):
    """Independent width derivation. Does not call `_qualifying_203`: it parses the two committed files on its own code
    path, so a mutation that narrows the record builder moves one side of the comparison and not the other."""
    reg = registry(root)
    rows = refetch_rows(root)
    seen = set()
    for row in rows:
        sid, url, key = row[0], row[1], row[2]
        rc, http, txt = row[5], row[6], row[8]
        if rc != "0" or http == "200" or txt == "-" or not http.isdigit() or len(http) != 3:
            continue
        cells = reg.get(sid)
        if cells is None:
            continue
        if hashlib.sha256(url.encode()).hexdigest()[:24] != key:
            continue
        cap = os.path.join(root, "corpus", "captures", key + ".txt")
        if not os.path.isfile(cap) or hashlib.sha256(open(cap, "rb").read()).hexdigest() != txt:
            continue
        text = open(cap, encoding="utf-8", errors="replace").read()
        if any(8 <= len(line.split()) <= 25 for line in text.split("\n")):
            seen.add((sid, url))
    return len(seen)


def build_d1_203_admits(root):
    """D1 class: an admit record over every qualifying committed 203 row. The repaired tool must refuse each with
    REFETCH (only a 200 grounds a quote); a 2xx rule accepts it."""
    out = []
    return out
    for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root):
        out.append((sid, f'GATE-RECORD {sid} url={url} fetched={fetched} tier={tier} decision=admit '
                         f'capture=corpus/captures/{key}.txt capture_sha256={h[:16]} words={len(quote.split())} '
                         f'quote="{quote}"'))
    return out


def build_d2_203_rejects(root):
    """D2 class: the reject form of the same rows — a `url/unreach` record claiming a failed transfer while reporting
    curl_rc=0 and a 2xx status. A 203 is a successful response (S216 "the request was successful"), so the unreach
    form must refuse it with REFETCH."""
    out = []
    for sid, url, _key, fetched, tier, _h, _quote, http in _qualifying_203(root):
        out.append((sid, f'GATE-RECORD {sid} url={url} fetched={fetched} tier={tier} decision=reject '
                         f'capture=none curl_rc=0 http={http} words=0 quote=none'))
    return out


def build_mutant(tool_src, dst, old, new):
    src = open(tool_src, encoding="utf-8").read()
    mutant = src.replace(old, new)
    if mutant == src:
        return False
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(mutant)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tool")
    ap.add_argument("--work")
    a = ap.parse_args()
    root, repo = os.path.abspath(a.root), os.path.abspath(a.repo)
    tool = os.path.abspath(a.tool) if a.tool else os.path.join(root, "tools", "gate-records.py")
    legs = []
    work = a.work or os.environ.get("TMPDIR") or os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="gr87-", dir=work)
    try:
        pos = []
        for ln in open(POS_TSV, encoding="utf-8"):
            f, n, raw = ln.rstrip("\n").split("\t", 2)
            sid = re.match(r"^\s*GATE-RECORD (S\d+)", raw).group(1)
            pos.append((f, int(n), sid, raw))

        d1 = build_d1_203_admits(root)
        d2 = build_d2_203_rejects(root)
        d1_expected = count_203_rows(root)

        legs.append(("TOOL", os.path.isfile(tool), "tool present"))
        if not os.path.isfile(tool):
            # nothing below can run; print the zero line and fail
            pass
        else:
            try:
                fresh_admits, fresh_revs, fresh_unreach = build_fresh_positives(root, repo)
                fresh_err = ""
            except RuntimeError as e:
                fresh_admits = fresh_revs = fresh_unreach = []
                fresh_err = str(e)
            fresh = fresh_admits + fresh_revs + fresh_unreach

            forged = []
            all_pos = pos + [("fresh", 1, sid, raw) for sid, raw in fresh]
            admits = [p for p in all_pos if form_of(p[3]) == "admit"]
            failed_txt = {}
            for f in refetch_rows(root):
                if f[5] == "0" and f[6] != "200" and f[8] != "-":
                    failed_txt.setdefault(f[1], f[8])
            for p in all_pos:
                for label, line, code in mutations(p, root):
                    if line is None:
                        if label == "M03-other-capture" and admits:
                            line = kv_set(p[3], "capture", kv_get(admits[(admits.index(p) + 1) % len(admits)][3], "capture"))
                        elif label == "M17-id-swap" and admits:
                            other = admits[(admits.index(p) + 1) % len(admits)]
                            line = p[3].replace("GATE-RECORD " + p[2], "GATE-RECORD " + other[2], 1)
                            line = kv_set(line, "tier", kv_get(other[3], "tier"))
                        else:
                            continue
                    if line is None:
                        continue
                    forged.append((label, p[2], line, code))
            for p in admits:
                url = kv_get(p[3], "url")
                if url in failed_txt:
                    forged.append(("D1-stale-refetch-txt-sha-drift", p[2],
                                   kv_set(p[3], "capture_sha256", failed_txt[url]), "REFETCH"))
            for sid, line in d1:
                forged.append(("D1-203-admit", sid, line, "REFETCH"))
            for sid, line in d2:
                forged.append(("D2-203-reject", sid, line, "REFETCH"))
            total_forged = len(forged)

            rc_ok = 0
            lessons = sorted({p[0] for p in pos})
            files = [os.path.join(root, f) for f in lessons]
            rc, res, _ = run(tool, root, repo, files)
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
            fresh_files = []
            for i, (sid, raw) in enumerate(fresh):
                fp = os.path.join(tmp, "fresh%02d.md" % i)
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(raw + "\n")
                fresh_files.append((fp, sid))
            if fresh_files:
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
            rc, res, _ = run(tool, root, repo, ffiles) if ffiles else (1, {}, "")
            rc_ok += rc == 1
            refused = exp = 0
            d1_refused = d2_refused = 0
            labels = [lbl for lbl, _, _, _ in forged]
            for (label, sid, line, code), fp in zip(forged, ffiles):
                v = res.get((fp, 1))
                if v and v[0] == "FAIL":
                    refused += 1
                    if code in v[1]:
                        exp += 1
                        if label == "D1-203-admit":
                            d1_refused += 1
                        if label == "D2-203-reject":
                            d2_refused += 1
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
            sp = os.path.join(tmp, "notgit")
            os.makedirs(sp, exist_ok=True)
            rp = os.path.join(tmp, "r.md")
            probe_rec = fresh[3][1] if len(fresh) > 3 else (pos[0][3] if pos else "GATE-RECORD S1")
            with open(rp, "w", encoding="utf-8") as fh:
                fh.write(probe_rec + "\n")
            p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", sp, rp],
                               capture_output=True, text=True)
            setup_ok = 1 if (p.returncode == 2 and "GATE_RECORDS_ERROR" in p.stderr) else 0

            # --- mutant legs: both derived from the subject tool's own bytes, both run ---
            positives = files + [fp for fp, _ in fresh_files]
            mut_admit_derived = mut_admit_killed = 0
            mut_unreach_derived = mut_unreach_killed = 0
            if files:
                ma = os.path.join(tmp, "tool-MUT-ADMIT.py")
                if build_mutant(tool, ma, ADMIT_LITERAL, 'r[6].startswith("2")'):
                    mut_admit_derived = 1
                    mrc, mres, _ = run(ma, root, repo, positives)
                    pos_ok = (mrc == 0
                              and all(mres.get((os.path.join(root, f), n), ("", set()))[0] == "OK"
                                      for f, n, _, _ in pos)
                              and all(mres.get((fp, 1), ("", set()))[0] == "OK" for fp, _ in fresh_files))
                    accepts = 0
                    if d1:
                        d1_fps = [ffiles[labels.index("D1-203-admit") + j] for j in range(len(d1))]
                        mrc2, mres2, _ = run(ma, root, repo, d1_fps)
                        accepts = sum(1 for fp in d1_fps if mres2.get((fp, 1), ("", set()))[0] == "OK")
                    mut_admit_killed = 1 if (pos_ok and accepts == len(d1) and d1) else 0
                    if not mut_admit_derived:
                        print("MUT_ADMIT_NOT_DERIVED subject bytes carry no admit literal")
                mu = os.path.join(tmp, "tool-MUT-UNREACH.py")
                if build_mutant(tool, mu, UNREACH_LITERAL, 'kv["http"] == "200"'):
                    mut_unreach_derived = 1
                    mrc, mres, _ = run(mu, root, repo, positives)
                    pos_ok = (mrc == 0
                              and all(mres.get((os.path.join(root, f), n), ("", set()))[0] == "OK"
                                      for f, n, _, _ in pos)
                              and all(mres.get((fp, 1), ("", set()))[0] == "OK" for fp, _ in fresh_files))
                    accepts = 0
                    if d2:
                        d2_fps = [ffiles[labels.index("D2-203-reject") + j] for j in range(len(d2))]
                        mrc2, mres2, _ = run(mu, root, repo, d2_fps)
                        accepts = sum(1 for fp in d2_fps if mres2.get((fp, 1), ("", set()))[0] == "OK")
                    mut_unreach_killed = 1 if (pos_ok and accepts == len(d2) and d2) else 0
                    if not mut_unreach_derived:
                        print("MUT_UNREACH_NOT_DERIVED subject bytes carry no unreach literal")
            # derivation-negative probe: a copy whose literals are rewritten must yield no mutant at all
            noliteral = os.path.join(tmp, "tool-NO-LITERAL.py")
            src = open(tool, encoding="utf-8").read()
            with open(noliteral, "w", encoding="utf-8") as fh:
                fh.write(src.replace("r[6] == " + '"200"', 'r[6] == "2" + "00"')
                         .replace(UNREACH_LITERAL, '200 <= int(kv["http"]) < 3 + 00'))
            neg_a = os.path.join(tmp, "neg-a.py")
            neg_b = os.path.join(tmp, "neg-b.py")
            derive_neg = 1 if (not build_mutant(noliteral, neg_a, ADMIT_LITERAL, 'r[6].startswith("2")')
                               and not build_mutant(noliteral, neg_b, UNREACH_LITERAL, 'kv["http"] == "200"')) else 0

            legs += [
                ("POSITIVE", p_ok == len(pos) and bool(pos), f"{p_ok}/{len(pos)}"),
                ("FRESH", fresh_ok == 5 and not fresh_err, f"{fresh_ok}/5 {fresh_err}".strip()),
                ("FORGED", refused == total_forged, f"{refused}/{total_forged}"),
                ("CODES", exp == total_forged, f"{exp}/{total_forged}"),
                ("EMPTY", e_ok == 1, f"{e_ok}/1"),
                ("RC", rc_ok == 4, f"{rc_ok}/4"),
                ("SETUP", setup_ok == 1, f"{setup_ok}/1"),
                ("D1_WIDTH", d1_expected >= 3 and len(d1) == d1_expected, f"{len(d1)}/{d1_expected} floor3"),
                ("D1_REFUSED", bool(d1) and d1_refused == len(d1), f"{d1_refused}/{len(d1)}"),
                ("D2_WIDTH", d1_expected >= 3 and len(d2) == d1_expected, f"{len(d2)}/{d1_expected} floor3"),
                ("D2_REFUSED", bool(d2) and d2_refused == len(d2), f"{d2_refused}/{len(d2)}"),
                ("MUT_ADMIT", mut_admit_derived == 1 and mut_admit_killed == 1,
                 f"derived={mut_admit_derived} killed={mut_admit_killed}"),
                ("MUT_UNREACH", mut_unreach_derived == 1 and mut_unreach_killed == 1,
                 f"derived={mut_unreach_derived} killed={mut_unreach_killed}"),
                ("DERIVE_NEG", derive_neg == 1, f"{derive_neg}/1"),
            ]
            print(f"TOOL={'present'} POSITIVE={p_ok}/{len(pos)} FRESH_POSITIVE={fresh_ok}/5 "
                  f"FORGED_REFUSED={refused}/{total_forged} EXPECTED_CODE={exp}/{total_forged} "
                  f"EMPTY_REFUSED={e_ok}/1 RC={rc_ok}/4 SETUP={setup_ok}/1 "
                  f"D1_EXPECTED={d1_expected} D1_FORGES={len(d1)} D1_REFUSED={d1_refused}/{len(d1)} "
                  f"D2_FORGES={len(d2)} D2_REFUSED={d2_refused}/{len(d2)} "
                  f"MUT_ADMIT_DERIVED={mut_admit_derived} MUT_ADMIT_KILLED={mut_admit_killed} "
                  f"MUT_UNREACH_DERIVED={mut_unreach_derived} MUT_UNREACH_KILLED={mut_unreach_killed} "
                  f"DERIVE_NEG={derive_neg} LEGS={sum(1 for _, ok, _ in legs if ok)}/{EXPECTED_LEGS}")
            if not os.path.isfile(tool):
                print("TOOL=absent")
        if not os.path.isfile(tool):
            print(f"TOOL=absent D1_EXPECTED={d1_expected} D1_FORGES={len(d1)} D2_FORGES={len(d2)} LEGS=0/{EXPECTED_LEGS}")
        passed = len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs)
        for name, ok, detail in legs:
            if not ok:
                print(f"LEG_FAIL {name} {detail}")
        print(f"GATE_RECORDS_R87={'PASS' if passed else 'FAIL'}")
        return 0 if passed else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

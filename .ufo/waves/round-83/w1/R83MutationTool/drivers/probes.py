#!/usr/bin/env python3
"""Kill probes, corrected: build the forged input class that should kill each survivor,
run the LANDED tool and the MUTANT on the same probe file, record both outputs."""
import hashlib
import os
import re
import shutil
import subprocess
import sys

TREE = "/fast/scratch/hyaku/chousa-r83/R83MutationTool"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
LANDED = os.path.join(TREE, "tools/gate-records.py")
PROBES = os.path.join(TREE, "probes")
LOGS = os.path.join(TREE, "logs")
os.makedirs(PROBES, exist_ok=True)


def run(tool, root, files):
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", LANE] + files,
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def row(sid, fetched):
    for ln in open(os.path.join(TREE, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9 and f[0] == sid and f[4] == fetched:
            return f
    raise SystemExit("no row %s %s" % (sid, fetched))


def tier(sid):
    for ln in open(os.path.join(TREE, "corpus/SOURCES.md"), encoding="utf-8"):
        m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", ln)
        if m and m.group(1) == sid:
            return [c.strip() for c in ln.strip().strip("|").split("|")][3]
    raise SystemExit("no registry row " + sid)


def capsha_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def phrase(path, start, n):
    toks = " ".join(open(path, encoding="utf-8", errors="replace").read().split()).split()
    q = " ".join(toks[start:start + n])
    assert '"' not in q
    return q


def probe(label, text, mutant, root=None):
    root = root or TREE
    fp = os.path.join(PROBES, label + ".md")
    with open(fp, "w", encoding="utf-8") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")
    lrc, lout, lerr = run(LANDED, root, [fp])
    mrc, mout, merr = run(os.path.join(TREE, "mutants", mutant + ".py"), root, [fp])
    with open(os.path.join(LOGS, "probe-" + label + ".out"), "w", encoding="utf-8") as fh:
        fh.write(f"# probe {label} vs mutant {mutant}\n## input\n{text}\n## landed rc={lrc}\n{lout}\n{lerr}\n"
                 f"## mutant rc={mrc}\n{mout}\n{merr}\n")
    print(f"{label}\t{mutant}\tlanded_rc={lrc}\t{(lout.splitlines() or [lerr])[0]}\t"
          f"mutant_rc={mrc}\t{(mout.splitlines() or [merr])[0]}")


def main():
    r113 = row("S113", "2026-10-27T08:30:59Z")
    cap113 = os.path.join(TREE, "corpus/captures", r113[2] + ".txt")
    sha113 = capsha_of(cap113)
    q113 = phrase(cap113, 6, 12)

    # --- M03: S113 stale refetch row (committed bytes only) -------------------
    r = row("S113", "2026-10-27T08:07:08Z")
    line = (f'GATE-RECORD S113 url={r[1]} fetched={r[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r[2]}.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}"')
    probe("P03-stale-refetch-row", line, "M03-drop-refetch-txtsha")

    # --- M24: unreach record for a row that is a success ---------------------
    line = (f'GATE-RECORD S113 url={r113[1]} fetched={r113[4]} tier={tier("S113")} decision=reject '
            f'capture=none curl_rc=0 http=200 words=0 quote=none')
    probe("P24-unreach-claims-success", line, "M24-unreach-accept-success")

    # --- M11: abbreviated rev ------------------------------------------------
    rev = "b7803829922770b890e9f4efdd30d12c3695439a"
    line = (f'GATE-RECORD S199 rev={rev[:7]} path=corpus/lessons/round-79-verifier-spotcheck.md line=222 '
            f'words=12 quote=the battery is fully forgeable through the payload channel on **both** batteries')
    probe("P11-short-rev", line, "M11-rev-short")

    # --- M27: rev quote with 26 words ---------------------------------------
    blob = subprocess.run(["git", "-C", LANE, "cat-file", "blob", rev + ":corpus/QUALITY.md"],
                          capture_output=True).stdout.decode("utf-8", "replace").split("\n")
    i = next(k for k, l in enumerate(blob, 1) if len(l.split()) >= 28 and l.strip())
    q26 = " ".join(blob[i - 1].split()[:26])
    line = f'GATE-RECORD S200 rev={rev} path=corpus/QUALITY.md line={i} words=26 quote={q26}'
    probe("P27-rev-26-words", line, "M27-quote-len-admit-only")

    # --- M28: capture name not 24 hex, real file inside captures ------------
    shutil.copyfile(cap113, os.path.join(TREE, "corpus/captures/zz-not-hex.txt"))
    line = (f'GATE-RECORD S113 url={r113[1]} fetched={r113[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/zz-not-hex.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}"')
    probe("P28-nonhex-capture-name", line, "M28-cap-re-loose")
    os.unlink(os.path.join(TREE, "corpus/captures/zz-not-hex.txt"))

    # --- M30 / M36: malformed fetched ---------------------------------------
    line = (f'GATE-RECORD S113 url={r113[1]} fetched=2026-11-06 tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r113[2]}.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}"')
    probe("P30-bad-timestamp", line, "M30-ts-loose")
    probe("P36-bad-timestamp", line, "M36-drop-ts-check")

    # --- M31: words with leading zero ---------------------------------------
    line = (f'GATE-RECORD S113 url={r113[1]} fetched={r113[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r113[2]}.txt capture_sha256={sha113} '
            f'words=0{len(q113.split())} quote="{q113}"')
    probe("P31-words-leading-zero", line, "M31-int-loose")

    # --- M34: unterminated quote --------------------------------------------
    line = (f'GATE-RECORD S113 url={r113[1]} fetched={r113[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r113[2]}.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}')
    probe("P34-unterminated-quote", line, "M34-admit-quote-unterminated")

    # --- M35: url not http(s) ------------------------------------------------
    line = (f'GATE-RECORD S113 url=ftp://example.org/x fetched={r113[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r113[2]}.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}"')
    probe("P35-ftp-url", line, "M35-drop-url-regex")

    # --- M32: rev line = len+1 (equivalence probe) --------------------------
    if blob and blob[-1] == "":
        blob.pop()
    n = len(blob)
    q8 = " ".join(blob[n - 1].split()[:8])
    line = f'GATE-RECORD S200 rev={rev} path=corpus/QUALITY.md line={n + 1} words={len(q8.split())} quote={q8}'
    probe("P32-line-past-eof", line, "M32-rev-no-pop")

    # --- M05 / M06: closest in-class attempt (unreachable classes) ----------
    r103 = row("S103", "2026-10-27T08:05:52Z")
    cap103 = os.path.join(TREE, "corpus/captures", r103[2] + ".txt")
    q103 = phrase(cap103, 4, 10)
    line = (f'GATE-RECORD S103 url={r103[1]} fetched={r103[4]} tier={tier("S103")} decision=admit '
            f'capture=corpus/captures/{r103[2]}.txt capture_sha256={capsha_of(cap103)} '
            f'words={len(q103.split())} quote="{q103}"')
    probe("P05-curl28-2xx-row", line, "M05-accept-curl-nonzero")
    probe("P06-non2xx-row", line, "M06-accept-non2xx")

    # --- M22: url changed, capture kept (co-firing CAPTURE_KEY) -------------
    r114 = row("S114", "2026-10-27T08:31:03Z")
    line = (f'GATE-RECORD S113 url={r114[1]} fetched={r113[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r113[2]}.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}"')
    probe("P22-url-swap-keeps-capture", line, "M22-drop-refetch-url")

    # --- M29: symlink capture (separate root copy) --------------------------
    sym = os.path.join(TREE, "tree-sym")
    if os.path.isdir(sym):
        shutil.rmtree(sym)
    os.makedirs(sym)
    shutil.copytree(os.path.join(TREE, "corpus"), os.path.join(sym, "corpus"))
    real = os.path.join(sym, "corpus/captures", r113[2] + ".txt")
    os.rename(real, os.path.join(sym, "corpus/captures/target-" + r113[2] + ".txt"))
    os.symlink("target-" + r113[2] + ".txt", real)
    line = (f'GATE-RECORD S113 url={r113[1]} fetched={r113[4]} tier={tier("S113")} decision=admit '
            f'capture=corpus/captures/{r113[2]}.txt capture_sha256={sha113} '
            f'words={len(q113.split())} quote="{q113}"')
    probe("P29-symlink-capture", line, "M29-no-islink", root=sym)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Engine-agreement probe v2: one record per probe, grep values filed, real tool CLI verifies each record.

grep side: `bash -c 'set -o pipefail; cd FX && [LC_ALL=C] /usr/bin/grep -l -F|-P -e EXPR GLOB | LC_ALL=C sort'`
(bash, so the glob expands exactly as the record's 'As run' line does: no dotglob, no globstar).
tool side: `python3 -B tools/search-rerun.py verify REC --root FX` (exit code + SEARCH_RERUN line).
"""
import importlib.util
import os
import shlex
import shutil
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/chousa-r95/R95ExecEngine"
TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/search-rerun.py"
RECEIPTS = os.path.join(S, "receipts")
os.makedirs(RECEIPTS, exist_ok=True)

FILES = {
    "data/a_plain.txt": b"hello token world\nsecond line token\n",
    "data/b_crlf.txt": b"hello token world\r\nsecond line\r\n",
    "data/c_nul.txt": b"hel\x00lo token\n",
    "data/d_badutf8.txt": b"\xff token \xfe\n",
    "data/e_notrail.txt": b"hello token",
    "data/f_lastline.txt": b"first line\nhello token",
    "data/g_case.txt": b"HELLO TOKEN\n",
    "data/h_jp.txt": "検索者は token を探す\n".encode("utf-8"),
    "data/i_space.txt": b"a token\tb c\n",
    "data/j_empty.txt": b"",
    "data/j_vtab.txt": b"x\x0by token\n",
    "data/k_digits.txt": b"order 12345 token\n",
    "data/k_nbsp.txt": "x\u00a0token\n".encode("utf-8"),
    "data/m_wall.txt": b"foobar\n",
    "data/n_span.txt": b"foo\nbar\n",
    "data/o_embed.txt": b"xtokenx\n",
    "data/p_dot.txt": b"foo.bar\n",
    "data/r_cjkonly.txt": "検索者\n".encode("utf-8"),
    "data/.x.txt": b"token dotfile\n",
    "data/sub/k_sub.txt": b"token subdir\n",
}

# id, engine, expression, bash glob (as the record's where), LC_ALL for grep (None = host UTF-8 default; 'C' = C)
PROBES = [
    ("P01", "fixed", "token", "data/*.txt", None),
    ("P02", "fixed", "HELLO TOKEN", "data/*.txt", None),
    ("P03", "fixed", "検索者", "data/*.txt", None),
    ("P04", "regex", r"\w", "data/r_cjkonly.txt", None),
    ("P04c", "regex", r"\w", "data/r_cjkonly.txt", "C"),
    ("P05", "regex", r"\b検索者\b", "data/*.txt", None),
    ("P06", "regex", "world$", "data/*.txt", None),
    ("P07", "regex", r"world\r$", "data/*.txt", None),
    ("P08", "regex", "^second", "data/*.txt", None),
    ("P09", "regex", r"\t", "data/*.txt", None),
    ("P10", "regex", r"\s", "data/j_vtab.txt", None),
    ("P11", "regex", r"\s", "data/k_nbsp.txt", None),
    ("P11c", "regex", r"\s", "data/k_nbsp.txt", "C"),
    ("P12", "regex", r"foo\nbar", "data/*.txt", None),
    ("P13", "regex", r"(?<=foo)bar", "data/*.txt", None),
    ("P14", "regex", r"\Ktoken", "data/*.txt", None),
    ("P15", "regex", "[[:alpha:]]+", "data/*.txt", None),
    ("P16", "regex", ".", "data/*.txt", None),
    ("P17", "regex", r"\btoken\b", "data/*.txt", None),
    ("P18", "fixed", "token", "data/sub/*.txt", None),
    ("P19", "fixed", "token", "data/**/*.txt", None),
    ("P20", "regex", r"token\Z", "data/*.txt", None),
    ("P21", "regex", "^$", "data/*.txt", None),
    ("P22", "regex", "x*", "data/*.txt", None),
    ("P23", "regex", "hel\\x00lo", "data/*.txt", None),
    ("P24", "regex", "^$", "data/j_empty.txt", None),
    ("P25", "fixed", "token", "data/.x.txt", None),
]


def sh(script, cwd=None):
    p = subprocess.run(["bash", "-c", script], capture_output=True, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def run(argv, cwd=None):
    p = subprocess.run(argv, capture_output=True, cwd=cwd)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


# ---- fixture (scratch git repo; toplevel asserted before any mutating git call) ----
FX = tempfile.mkdtemp(prefix="fx-", dir=S)
try:
    rc, top, _ = run(["git", "-C", FX, "init", "-q"])
    rc, top, _ = run(["git", "-C", FX, "rev-parse", "--show-toplevel"])
    assert os.path.realpath(top.strip()) == os.path.realpath(FX), (top, FX)
    os.makedirs(os.path.join(FX, "data", "sub"), exist_ok=True)
    for rel, content in FILES.items():
        with open(os.path.join(FX, rel), "wb") as fh:
            fh.write(content)
    assert run(["git", "-C", FX, "add", "-A"])[0] == 0
    rc, out, err = run(["git", "-C", FX, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                        "commit", "-q", "-m", "engine probe fixture"])
    assert rc == 0, err
    rc, rev, _ = run(["git", "-C", FX, "rev-parse", "HEAD"])
    REV = rev.strip()

    # tool module for the at-rev set when a record disagrees
    spec = importlib.util.spec_from_file_location("sr", TOOL)
    sr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sr)

    rows = []
    for pid, engine, expr, glob, lc in PROBES:
        flag = "-F" if engine == "fixed" else "-P"
        lcpref = "LC_ALL=C " if lc == "C" else ""
        script = (f"set -o pipefail; cd {shlex.quote(FX)} && {lcpref}/usr/bin/grep -l {flag} -e "
                  f"{shlex.quote(expr)} {glob} | LC_ALL=C sort")
        grc, gout, gerr = sh(script)
        gerr = gerr.decode("utf-8", "replace").strip()
        if grc == 1:
            gset, gstatus = [], "NOMATCH"
        elif grc == 0:
            gset, gstatus = [l for l in gout.decode("utf-8", "surrogateescape").split("\n") if l], "MATCH"
        else:
            gset, gstatus = [], f"GREP_ERROR rc={grc}"
        if gstatus.startswith("GREP_ERROR"):
            rows.append(dict(pid=pid, engine=engine, expr=expr, glob=glob, lc=lc, grep_rc=grc, gset=None,
                             gerr=gerr, tool_rc=None, tool_line="(not run: grep error)", agree="N/A",
                             tool_set=None))
            continue
        hs = "-" if not gset else ", ".join(gset)
        rec_path = os.path.join(S, f"rec-{pid}.md")
        with open(rec_path, "w", encoding="utf-8") as fh:
            fh.write(f"# probe record {pid}\n\n## Searches\n\n"
                     "| id | engine | where | expression | rev | searched | hits | hit_set |\n"
                     "|---|---|---|---|---|---|---|---|\n"
                     f"| Q1 | {engine} | {glob} | `{expr}` | {REV} | 2026-11-08 | {len(gset)} | {hs} |\n")
        trc, tout, terr = run(["python3", "-B", TOOL, "verify", rec_path, "--root", FX])
        line = next((l for l in tout.splitlines() if l.startswith("SEARCH_RERUN Q1 ")), "")
        if trc == 2:
            tool_line = terr.strip()
            agree = "REFUSED"
            tool_set = None
        else:
            tool_line = line
            agree = "AGREE" if (trc == 0 and " rev=MATCH" in line) else "DISAGREE"
            tool_set = None
        if agree == "DISAGREE" and engine == "regex":
            try:
                r = {"id": "Q1", "engine": "regex", "globs": [glob], "rev": REV,
                     "pattern": sr.re.compile(expr), "n": len(gset)}
                tool_set = sr.run_at_rev(FX, r, {})
            except (sr.re.error, sr.Setup) as exc:
                tool_set = f"ERR {exc}"
        elif agree == "DISAGREE":
            r = {"id": "Q1", "engine": "fixed", "globs": [glob], "rev": REV,
                 "needle": expr.encode("utf-8"), "n": len(gset)}
            tool_set = sr.run_at_rev(FX, r, {})
        rows.append(dict(pid=pid, engine=engine, expr=expr, glob=glob, lc=lc, grep_rc=grc, gset=gset,
                         gerr=gerr, tool_rc=trc, tool_line=tool_line, agree=agree, tool_set=tool_set,
                         tool_out=tout, tool_err=terr))

    # ---- receipts ----
    with open(os.path.join(RECEIPTS, "R95ExecEngine-probe-table.txt"), "w", encoding="utf-8") as fh:
        fh.write("probe\tengine\texpr\twhere\tLC_ALL(grep)\tgrep_rc\tgrep_set\ttool_rc\ttool_set_or_note\tagree\n")
        for r in rows:
            gs = "-" if r["gset"] is None else (", ".join(r["gset"]) if r["gset"] else "-")
            if r["agree"] == "REFUSED":
                ts = r["tool_line"]
            elif r["agree"] == "N/A":
                ts = "-"
            elif r.get("tool_set") is not None:
                ts = ", ".join(r["tool_set"]) if isinstance(r["tool_set"], list) and r["tool_set"] else (
                    r["tool_set"] if isinstance(r["tool_set"], str) else "-")
            else:
                ts = "(agrees: same as grep)"
            fh.write(f"{r['pid']}\t{r['engine']}\t{r['expr']}\t{r['glob']}\t{r['lc'] or 'host(UTF-8)'}\t"
                     f"{r['grep_rc']}\t{gs}\t{r['tool_rc']}\t{ts}\t{r['agree']}\n")
    with open(os.path.join(RECEIPTS, "R95ExecEngine-probe-tool-runs.txt"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(f"== {r['pid']} expr={r['expr']!r} glob={r['glob']} LC_ALL(grep)={r['lc'] or 'host'}\n")
            fh.write(f"grep_rc={r['grep_rc']} grep_set={r['gset']} grep_err={r['gerr']!r}\n")
            fh.write(f"tool_rc={r['tool_rc']} tool_line={r['tool_line']!r} agree={r['agree']}\n")
            if r.get("tool_out") is not None:
                fh.write(f"tool_stdout:\n{r['tool_out']}")
            if r.get("tool_err"):
                fh.write(f"tool_stderr: {r['tool_err'].strip()}\n")
            fh.write("\n")

    for r in rows:
        print(f"{r['pid']:<5} {r['agree']:<9} grep_rc={r['grep_rc']} tool_rc={r['tool_rc']} "
              f"grep={r['gset'] if r['gset'] is None else len(r['gset'])} :: {r['tool_line'][:110]}")
    print("FIXTURE_REV", REV)
finally:
    shutil.rmtree(FX, ignore_errors=True)

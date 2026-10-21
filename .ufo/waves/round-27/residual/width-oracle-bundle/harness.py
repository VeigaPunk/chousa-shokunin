#!/usr/bin/env python3
"""Round-27 residual review: attack change (a) GFM escaped-pipe header width.

Runs synthetic registry tables against three gate revisions (base 64eec5d,
dd72641e, cb895a2) and compares each verdict with a GFM oracle.

GFM oracle: cmark-gfm (cmarkgfm 2025.10.22, reference GFM implementation,
table extension) cross-checked against markdown-it-py (table rule enabled).
Both oracles must agree before a fixture is scored.
"""
import html.parser
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

SANDBOX = "/tmp/chousa-r27-residual-ResWidthFix"
WORK = os.path.join(SANDBOX, "work")
ENTRY_REL = "corpus/knowledge/entry.md"
SOURCE_ID = "S001"
ENTRY_ABS = os.path.join(WORK, ENTRY_REL)
NOW_EPOCH = "1790000000"  # 2026-09-21T05:33:20Z, same clock family as selftest
REVS = {
    "base64eec5d": os.path.join(SANDBOX, "64eec5d"),
    "dd72641e": os.path.join(SANDBOX, "dd72641e"),
    "cb895a2": os.path.join(SANDBOX, "cb895a2"),
    "cand": os.path.join(SANDBOX, "cand"),
}

# ---------------------------------------------------------------- oracle ----
class TableParser(HTMLParser):
    """Extract GFM table structure (header cells, body rows) from cmark-gfm HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self._table = None
        self._row = None
        self._cell = None
        self._in_head = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._table = {"header": [], "rows": []}
            self.tables.append(self._table)
        elif tag == "thead":
            self._in_head = True
        elif tag == "tr":
            self._row = []
        elif tag in ("th", "td"):
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("th", "td"):
            if self._row is not None and self._cell is not None:
                self._row.append("".join(self._cell))
            self._cell = None
        elif tag == "tr":
            if self._row is not None and self._table is not None:
                if self._in_head:
                    self._table["header"] = self._row
                else:
                    self._table["rows"].append(self._row)
            self._row = None
        elif tag == "thead":
            self._in_head = False
        elif tag == "table":
            self._table = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def oracle_cmark(text):
    import cmarkgfm

    html = cmarkgfm.github_flavored_markdown_to_html(text)
    p = TableParser()
    p.feed(html)
    if not p.tables:
        return None
    t = p.tables[0]
    return {"header": t["header"], "rows": t["rows"]}


def oracle_mdit(text):
    from markdown_it import MarkdownIt

    md = MarkdownIt("commonmark").enable("table")
    toks = md.parse(text)
    header, rows = None, []
    cur = None
    in_head = False
    for t in toks:
        if t.type == "thead_open":
            in_head = True
        elif t.type == "thead_close":
            in_head = False
        elif t.type == "tr_open":
            cur = []
        elif t.type == "inline":
            if cur is not None:
                cur.append(t.content)
        elif t.type == "tr_close":
            if cur is None:
                continue
            if in_head:
                header = cur
            else:
                rows.append(cur)
            cur = None
    if header is None:
        return None
    return {"header": header, "rows": rows}


def oracle_verdict(table):
    """Expected gate verdict under GFM semantics for the fixed fixture entry."""
    if table is None:
        return ("usage", "no-table")
    hdr = [c.strip() for c in table["header"]]
    need = ("id", "status", "used-by")
    if not all(n in hdr for n in need):
        return ("usage", "missing-columns")
    idx = {n: hdr.index(n) for n in need}
    findings = []
    seen = None
    for row in table["rows"]:
        cells = [c.strip() for c in row]
        if len(cells) < len(hdr):
            cells += [""] * (len(hdr) - len(cells))
        rid = cells[idx["id"]]
        if not re.fullmatch(r"S[0-9]{3,}", rid):
            continue
        if rid != SOURCE_ID:
            continue
        seen = (cells[idx["status"]], cells[idx["used-by"]])
        break
    if seen is None:
        findings.append("META_SOURCE_ROW_MISSING")
    else:
        status, usedby = seen
        tokens = [t.strip() for t in usedby.split(",")]
        tokens = [t[2:] if t.startswith("./") else t for t in tokens]
        if status != "mined":
            findings.append("META_SOURCE_NOT_MINED")
        elif ENTRY_REL not in tokens:
            findings.append("META_SOURCE_USEDBY_MISSING")
    if findings:
        return ("findings", ",".join(sorted(set(findings))))
    return ("clean", "")


# ---------------------------------------------------------------- runner ----
def run_gate(rev_root, registry_path):
    env = dict(os.environ)
    for k in ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE"):
        env.pop(k, None)
    env["CHOUSA_STRICT"] = "0"
    env["CHOUSA_ROOT"] = WORK
    env["CHOUSA_NOW_EPOCH"] = NOW_EPOCH
    gate = os.path.join(rev_root, "tools", "research-gate.sh")
    p = subprocess.run(
        ["bash", gate, "verify-metadata", ENTRY_ABS, "--root", WORK,
         "--registry", registry_path],
        env=env, capture_output=True, text=True, timeout=120)
    out = p.stdout + p.stderr
    findings = sorted(set(re.findall(r"FINDING (\w+)", out)))
    verdict = ""
    for line in out.splitlines():
        if line.startswith("RESEARCH_GATE: "):
            verdict = line.split("RESEARCH_GATE: ", 1)[1].split(" ")[0]
    usage = ""
    for line in out.splitlines():
        if "usage:" in line or "no table" in line or "metadata registry" in line:
            usage = line.strip()
    return {"rc": p.returncode, "findings": findings, "verdict": verdict,
            "usage": usage, "out": out}


def gate_verdict(r):
    if r["rc"] == 2:
        return ("usage", "no-table")
    if r["rc"] == 0:
        return ("clean", "")
    if r["rc"] == 1:
        return ("findings", ",".join(r["findings"]))
    return ("crash", "rc=%d" % r["rc"])


# ------------------------------------------------------------- fixtures ----
FIXTURES = []


def fx(name, group, header, delim, body, eol="\n", note="", no_final_nl=False):
    FIXTURES.append({"name": name, "group": group, "header": header,
                     "delim": delim, "body": body, "eol": eol, "note": note,
                     "no_final_nl": no_final_nl})


def build():
    # --- A: plain baselines, widths 3..6 (no escapes at all)
    fx("A1-w3-plain", "A", "| id | status | used-by |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="3 columns, no escapes")
    fx("A2-w4-plain", "A", "| id | status | used-by | note |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | n |"],
       note="4 columns, no escapes")
    fx("A3-w5-plain", "A", "| id | status | used-by | note | extra |",
       "|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | n | e |"], note="5 columns")
    fx("A4-w6-plain", "A", "| id | status | used-by | note | extra | more |",
       "|---|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | n | e | m |"], note="6 columns")

    # --- B: escaped pipe in header AFTER the key columns (the r27 fix target)
    fx("B1-esc-in-header-tail", "B", "| id | status | used-by | note \\| alt |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | x |"],
       note="GFM header=4 cells; naive split=5")
    fx("B2-esc-in-header-and-body", "B", "| id | status | used-by | note \\| alt |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a \\| b |"],
       note="escape in header and body cell")
    fx("B3-two-escapes-header", "B",
       "| id | status | used-by | a \\| b \\| c |", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | z |"], note="2 escapes")
    fx("B4-esc-header-w3", "B", "| id \\| x | status | used-by |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="escaped pipe inside the id header cell -> no plain 'id' column")
    fx("B5-esc-in-status-header", "B", "| id | status \\| s | used-by |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="escaped pipe inside the status header cell")

    # --- C: escaped pipe BEFORE / BETWEEN key columns (misalignment probes)
    fx("C1-esc-before-id", "C", "| x \\| y | id | status | used-by |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="GFM=4 cols (id,status,used-by at 1,2,3); naive id_col=2")
    fx("C2-esc-between-id-status", "C", "| id | note \\| x | status | used-by |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="GFM=4 cols; naive status_col=3 usedby_col=4")
    fx("C3-esc-between-status-usedby", "C",
       "| id | status | note \\| x | used-by |", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="GFM=4 cols; naive usedby_col=3 status_col=1")
    fx("C4-esc-after-usedby-w5", "C",
       "| id | status | used-by | a \\| b | c |", "|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | p | q |"],
       note="GFM=5 cols")

    # --- D: double backslash (backslash-escape parity)
    fx("D1-double-bslash-header", "D",
       "| id | status | used-by | a \\\\ b |", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | y |"],
       note="GFM: '\\\\' is an escaped backslash, '|' is a real delimiter -> 4 cells")
    fx("D2-triple-bslash-header", "D",
       "| id | status | used-by | a \\\\\\| b |", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | y |"],
       note="GFM: '\\\\\\|' -> literal backslash + literal pipe -> 4 cells")
    fx("D3-quad-bslash-header", "D",
       "| id | status | used-by | a \\\\\\\\ b |", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | y |"],
       note="GFM: 4 backslashes -> 2 literal backslashes then a delimiter -> 4 cells")
    fx("D4-double-bslash-before-id", "D",
       "| a \\\\ b | id | status | used-by |", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="double backslash ahead of the key columns")
    fx("D5-double-bslash-in-body", "D", "| id | status | used-by | note |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a \\\\ b |"],
       note="double backslash only in a body cell")

    # --- E: escaped pipe adjacent to an outer pipe
    fx("E1-esc-at-row-start", "E", "| \\| id | status | used-by |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="escaped pipe right after the leading outer pipe")
    fx("E2-esc-at-row-end", "E", "| id | status | used-by | x \\|",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | x |"],
       note="escaped pipe right before the trailing outer pipe")
    fx("E3-esc-outer-adjacent-body", "E", "| id | status | used-by | note |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | \\| end |"],
       note="escaped pipe adjacent to the outer pipe in a body row")
    fx("E4-esc-only-cell", "E", "| id | status | used-by | \\| |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       note="a cell that is exactly an escaped pipe")
    fx("E5-esc-pipe-pipe", "E", "| id | status | used-by | a \\|| b |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | z |"],
       note="escaped pipe immediately followed by a real delimiter")

    # --- F: mixed outer pipes (rows without leading/trailing pipe)
    fx("F1-header-no-outer", "F", "id | status | used-by",
       "---|---|---", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="header without outer pipes")
    fx("F2-body-no-outer", "F", "| id | status | used-by |",
       "|---|---|---|", ["S001 | mined | corpus/knowledge/entry.md"],
       note="body row without outer pipes")
    fx("F3-header-esc-body-plain", "F", "| id | status | used-by | n \\| m |",
       "|---|---|---|---|", ["S001 | mined | corpus/knowledge/entry.md | q |"],
       note="escaped pipe in header, body without outer pipes")
    fx("F4-trailing-space-only", "F", "| id | status | used-by |   ",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="trailing whitespace after the last outer pipe")

    # --- G: aligned delimiter rows
    fx("G1-align-left", "G", "| id | status | used-by |",
       "|:---|:---|:---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="left aligned delimiter cells")
    fx("G2-align-right", "G", "| id | status | used-by |",
       "|---:|:---:|---:|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="right/center aligned delimiter cells")
    fx("G3-align-with-escape", "G", "| id | status | used-by | n \\| m |",
       "|:---|:---|:---|:---|", ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       note="aligned delimiter + escaped pipe header")
    fx("G4-align-escape-only-key-cols", "G", "| id | status | used-by |",
       "|:---|:---|:---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="aligned delimiter, plain header (control)")

    # --- H: CRLF
    fx("H1-crlf-plain", "H", "| id | status | used-by |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |"], eol="\r\n",
       note="CRLF, plain")
    fx("H2-crlf-escaped-header", "H", "| id | status | used-by | n \\| m |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       eol="\r\n", note="CRLF + escaped pipe header")
    fx("H3-crlf-double-bslash", "H", "| id | status | used-by | a \\\\ b |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | y |"],
       eol="\r\n", note="CRLF + double backslash")
    fx("H4-crlf-body", "H", "| id | status | used-by | note |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | n |"],
       eol="\r\n", note="CRLF body row")

    # --- I: wider tables with escapes
    fx("I1-w5-esc-mid", "I", "| id | a \\| b | status | used-by | note |",
       "|---|---|---|---|---|",
       ["| S001 | q | mined | corpus/knowledge/entry.md | z |"],
       note="5 GFM columns, escape in 2nd column")
    fx("I2-w6-esc-mid", "I",
       "| id | a \\| b | status | used-by | note | more |",
       "|---|---|---|---|---|---|",
       ["| S001 | q | mined | corpus/knowledge/entry.md | z | w |"],
       note="6 GFM columns, escape in 2nd column")
    fx("I3-w6-plain-esc-tail", "I",
       "| id | status | used-by | note | extra | m \\| n |",
       "|---|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | n | e | f |"],
       note="6 GFM columns, escape in last column")

    # --- J: separator-row and structural probes
    fx("J1-escape-in-delimiter", "J", "| id | status | used-by |",
       "|---|---|---\\|---|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="escaped pipe inside the delimiter row")
    fx("J2-delimiter-too-narrow", "J", "| id | status | used-by | n \\| m |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       note="delimiter narrower than the GFM header")
    fx("J3-delimiter-too-wide", "J", "| id | status | used-by | n \\| m |",
       "|---|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       note="delimiter wider than the GFM header")
    fx("J4-no-final-newline", "J", "| id | status | used-by | n \\| m |",
       "|---|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       no_final_nl=True, note="no trailing newline at EOF")
    fx("J5-two-tables", "J", "| id | status | used-by | n \\| m |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | q |",
        "| id | status | used-by |",
        "|---|---|---|",
        "| S001 | mined | corpus/knowledge/entry.md |"],
       note="two candidate tables, second one plain")
    fx("J6-escaped-pipe-only-row", "J", "| id | status | used-by |",
       "|---|---|---|", ["| S001 | mined | corpus/knowledge/entry.md |",
                        "| \\| | | |"],
       note="a body row that is only an escaped pipe")



    # --- P: backslash-parity before a pipe (the decisive parity cases).
    # B = one backslash; the file must literally contain B*n followed by '|'.
    P = chr(92)
    fx("P1-double-bslash-pipe-mid", "P",
       "| id | status | used-by | a " + P + P + "| b |",
       "|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a " + P + P + "| b |"],
       note="GFM: '\\\\' is an escaped backslash, the pipe is a REAL delimiter -> 5 cells")
    fx("P2-double-bslash-pipe-wrong-delim", "P",
       "| id | status | used-by | a " + P + P + "| b |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a " + P + P + "| b |"],
       note="GFM header=5 cells, delimiter=4 -> not a table")
    fx("P3-triple-bslash-pipe-mid", "P",
       "| id | status | used-by | a " + P + P + P + "| b |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a " + P + P + P + "| b |"],
       note="GFM: '\\\\\\|' -> literal backslash + literal pipe -> 4 cells")
    fx("P4-quad-bslash-pipe-mid", "P",
       "| id | status | used-by | a " + P + P + P + P + "| b |",
       "|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a " + P + P + P + P + "| b |"],
       note="GFM: 4 backslashes -> 2 literal backslashes then a REAL delimiter -> 5 cells")
    fx("P5-double-bslash-before-id", "P",
       "| a " + P + P + "| b | id | status | used-by |",
       "|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="even-parity pipe ahead of the key columns")
    fx("P6-double-bslash-in-body-only", "P",
       "| id | status | used-by | note |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | a " + P + P + "| b |"],
       note="even-parity pipe only in a body cell")
    fx("P7-double-bslash-in-delimiter", "P",
       "| id | status | used-by | note |",
       "|---|---|---|---" + P + P + "|",
       ["| S001 | mined | corpus/knowledge/entry.md | n |"],
       note="even-parity pipe inside the delimiter row")
    fx("P8-escaped-pipe-in-code-span", "P",
       "| id | status | used-by | `a" + P + "|b` |",
       "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | q |"],
       note="escaped pipe inside a code span in the header")
    fx("P9-double-bslash-w6", "P",
       "| id | status | used-by | n | e | m " + P + P + "| x |",
       "|---|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | n | e | m " + P + P + "| x |"],
       note="6 GFM columns, even-parity pipe in the last column")
    fx("P10-double-bslash-between-key", "P",
       "| id | n " + P + P + "| x | status | used-by |",
       "|---|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="even-parity pipe between id and status (width + index)")

    # --- Q: the parent's four new falsify controls (round27-falsify-controls.py)
    fx("Q1-escaped-before-status-queued", "Q",
       "| id | note \\| x | status | used-by |", "|---|---|---|---|",
       ["| S001 | n | queued | mined | corpus/knowledge/entry.md |"],
       note="GFM status cell = 'queued' -> not mined")
    fx("Q2-escaped-before-status-mined", "Q",
       "| id | note \\| x | status | used-by |", "|---|---|---|---|",
       ["| S001 | n | mined | corpus/knowledge/entry.md |"],
       note="GFM status cell = 'mined' -> clean")
    fx("Q3-escaped-body-cell-before-status", "Q",
       "| id | note \\| x | status | used-by |", "|---|---|---|---|",
       ["| S001 | n \\| queued | mined | corpus/knowledge/entry.md |"],
       note="escaped pipe inside the body cell that precedes status")
    fx("Q4-escaped-final-header-cell-no-outer-pipe", "Q",
       "| id | status | used-by | note \\|", "|---|---|---|---|",
       ["| S001 | mined | corpus/knowledge/entry.md | n |"],
       note="escaped pipe as the final header cell, no trailing outer pipe")

    # --- R: GFM delimiter-row rules the gate inherits wrongly
    fx("R1-single-dash-delimiter", "R", "| id | status | used-by |",
       "|-|-|-|", ["| S001 | mined | corpus/knowledge/entry.md |"],
       note="GFM allows one dash per delimiter cell; the gate regex needs 3+")

def main():
    build()
    os.makedirs(os.path.join(WORK, "corpus", "knowledge"), exist_ok=True)
    with open(ENTRY_ABS, "w") as fh:
        fh.write("source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\n")

    rows = []
    for f in FIXTURES:
        lines = [f["header"], f["delim"]] + f["body"]
        text = f["eol"].join(lines)
        if not f["no_final_nl"]:
            text += f["eol"]
        reg = os.path.join(WORK, "reg-%s.md" % f["name"])
        with open(reg, "wb") as fh:
            fh.write(text.encode("utf-8"))

        oc = oracle_cmark(text)
        om = oracle_mdit(text)
        agree = (oc == om)
        ov = oracle_verdict(oc)
        res = {}
        for key, root in REVS.items():
            res[key] = run_gate(root, reg)
        rows.append({"fx": f, "oracle": ov, "oracle_cmark": oc,
                     "oracle_mdit": om, "oracles_agree": agree, "runs": res})

    # ---- report
    hdr = ("fixture", "group", "oracles", "oracle", "base64eec5d", "dd72641e",
           "cb895a2", "cand")
    print("\t".join(hdr))
    for r in rows:
        f = r["fx"]
        cells = []
        for key in ("base64eec5d", "dd72641e", "cb895a2", "cand"):
            g = gate_verdict(r["runs"][key])
            cells.append("rc=%d/%s%s" % (r["runs"][key]["rc"], g[0],
                                         ("[" + g[1] + "]") if g[1] else ""))
        ov = r["oracle"]
        print("\t".join([f["name"], f["group"],
                         "agree" if r["oracles_agree"] else "DISAGREE",
                         ov[0] + (("/" + ov[1]) if ov[1] else "")] + cells))
    print()
    # divergence summary
    print("== divergences (gate verdict != oracle verdict) ==")
    for r in rows:
        f = r["fx"]
        ov = r["oracle"]
        for key in ("base64eec5d", "dd72641e", "cb895a2", "cand"):
            g = gate_verdict(r["runs"][key])
            if g != ov:
                print("  %-30s %-12s gate=%-40s oracle=%s" % (
                    f["name"], key, "%s/%s" % g, "%s/%s" % ov))
    print()
    print("== new-harm candidates: cb895a2 differs from oracle AND dd72641e ==")
    for r in rows:
        f = r["fx"]
        ov = r["oracle"]
        g_cb = gate_verdict(r["runs"]["cb895a2"])
        g_dd = gate_verdict(r["runs"]["dd72641e"])
        g_bs = gate_verdict(r["runs"]["base64eec5d"])
        if g_cb != ov and g_cb != g_dd:
            print("  %-30s cb=%-38s dd=%-24s base=%-24s oracle=%s" % (
                f["name"], "%s/%s" % g_cb, "%s/%s" % g_dd, "%s/%s" % g_bs,
                "%s/%s" % ov))
    print()
    print("== cb895a2 vs dd72641e disagreements ==")
    for r in rows:
        g_cb = gate_verdict(r["runs"]["cb895a2"])
        g_dd = gate_verdict(r["runs"]["dd72641e"])
        if g_cb != g_dd:
            print("  %-30s cb=%-38s dd=%-24s oracle=%s" % (
                r["fx"]["name"], "%s/%s" % g_cb, "%s/%s" % g_dd,
                "%s/%s" % r["oracle"]))
    print()
    print("== fixture notes ==")
    for r in rows:
        print("  %-30s %s" % (r["fx"]["name"], r["fx"]["note"]))
    with open(os.path.join(SANDBOX, "results.json"), "w") as fh:
        import json
        json.dump([{"fixture": r["fx"], "oracle": r["oracle"],
                    "oracles_agree": r["oracles_agree"],
                    "oracle_cmark": r["oracle_cmark"],
                    "oracle_mdit": r["oracle_mdit"],
                    "runs": {k: {kk: vv for kk, vv in v.items() if kk != "out"}
                             for k, v in r["runs"].items()}} for r in rows],
                  fh, indent=1)


if __name__ == "__main__":
    main()

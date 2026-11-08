#!/usr/bin/env python3
"""control-driver-r90 — round-90 C1 (operability): a commit-then-verify control-receipt driver.

Round 89's spot-check (`corpus/lessons/round-89-verifier-spotcheck.md`, §Amendment 7) measured four defects in
`corpus/evidence/round89/controls/run-controls.sh`:

  B1  line 25 wrote `>"$out"` BEFORE grepping `"$out"`, so the committed receipt was overwritten before it was read:
      the driver proved "a fresh run agrees with the row", never "the committed receipt agrees with the row".
  B2  `grep -qF -- "$f" "$out"` matched a substring, so `LEG_REREAD=16/160` satisfied a row requiring `16/16`.
  B3  no revision pin: the receipts named no `# computed_against=` revision and the tree measured was whatever the
      working copy held at run time (QUALITY 189's class).
  B4  the `c1-harm` row required only `moved=0`, a value `harm-recheck.py` also prints over an empty record set.

This driver is the successor. Every receipt it emits opens with four header lines

    # case=<id>
    # expected_exit=<n>
    # exit=<n>
    # computed_against=<40 hex>

and the `verify` mode (the one that scores the round) reads the committed receipt first and never writes it:

  1. COMMITTED  the receipt exists, its `# exit=` equals the row's expected exit, every required `K=V` token and every
                `K>=N` predicate holds on its body, and no required key appears twice with different values.
  2. EXACT      a required `K=V` matches only as a whole whitespace-delimited body token; a token that starts with
                `K=` and differs is `TOKEN_DETACHED`, never a pass (S219: `-x` selects whole-line matches).
  3. PIN        `# computed_against=` equals `--rev`; with `--repo`, the driver file, the expectations file and every
                committed receipt must be byte-identical to their blobs at `--rev` (`SELF_DRIFT`).
  4. FRESH      the instrument is re-run into `--work` only; its exit, tokens and predicates must agree with the
                committed receipt (a receipt that no longer reproduces is a finding, never a silent rewrite).
  5. DUPKEY     a required key carried twice with different values is refused (the "last one wins" class named in
                `considerthese/2026-11-07.md`, proposal 1).

Usage:
    python3 -B control-driver-r90.py emit   --root LANE --work DIR --rev REV [--expected F] [--receipts D]
    python3 -B control-driver-r90.py verify --root LANE --work DIR --rev REV [--repo GITDIR] [--expected F]
                                            [--receipts D]

Exit 0 every row OK, 1 a finding (printed `RECEIPT <case> FINDING <codes>`), 2 setup (bad rev, missing files).
Python 3 standard library only; no network.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXPECTED = os.path.join(HERE, "controls", "expected.tsv")
DEFAULT_RECEIPTS = os.path.join(HERE, "controls", "receipts")
REV_RE = re.compile(r"[0-9a-f]{40}")
KEYVAL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")
INT_RE = re.compile(r"-?[0-9]+")


def read_expected(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if parts[0] == "case":
                continue
            if len(parts) < 6:
                raise SystemExit(f"SETUP malformed expected row: {ln!r}")
            req = [] if parts[3].strip() == "-" else parts[3].split()
            pred = [] if parts[4].strip() == "-" else parts[4].split()
            rows.append({"case": parts[0], "instrument": parts[1], "exit": int(parts[2]),
                         "required": req, "predicates": pred, "source": parts[5]})
    return rows


def body_tokens(text):
    """Whitespace-delimited tokens of every non-comment line, plus the per-key value list."""
    toks = []
    keys = {}
    for ln in text.splitlines():
        if ln.startswith("#"):
            continue
        for t in ln.split():
            toks.append(t)
            m = KEYVAL_RE.match(t)
            if m:
                keys.setdefault(m.group(1), []).append(m.group(2))
    return toks, keys


def header_fields(text):
    out = {}
    for ln in text.splitlines():
        if not ln.startswith("# "):
            continue
        k, _, v = ln[2:].partition("=")
        if k and v:
            out[k.strip()] = v.strip()
    return out


def run_instrument(cmd, root):
    p = subprocess.run(["bash", "-lc", cmd], cwd=root, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def check_body(row, text):
    """Return (codes, tokens_ok, predicate_ok) for one receipt body."""
    codes = []
    toks, keys = body_tokens(text)
    required_keys = set()
    tokens_ok = True
    lines = [ln for ln in text.splitlines() if not ln.startswith("#")]
    normlines = [" ".join(ln.split()) for ln in lines]
    for want in row["required"]:
        if want.startswith("line:"):
            phrase = want[len("line:"):].replace("%20", " ")
            if not any(phrase in ln for ln in normlines):
                codes.append(f"LINE_MISSING:{phrase.replace(' ', '_')}")
                tokens_ok = False
            continue
        k, _, v = want.partition("=")
        required_keys.add(k)
        vals = keys.get(k, [])
        if want in toks:
            if len(set(vals)) > 1:
                codes.append(f"DUPLICATE_KEY:{k}")
                tokens_ok = False
            continue
        if vals:
            codes.append(f"TOKEN_DETACHED:{k}={','.join(sorted(set(vals)))}")
        else:
            codes.append(f"TOKEN_MISSING:{k}")
        tokens_ok = False
    predicate_ok = True
    for pred in row["predicates"]:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)>=(-?[0-9]+)$", pred)
        if not m:
            raise SystemExit(f"SETUP malformed predicate {pred!r}")
        k, floor = m.group(1), int(m.group(2))
        required_keys.add(k)
        vals = keys.get(k, [])
        if len(set(vals)) > 1:
            codes.append(f"DUPLICATE_KEY:{k}")
            predicate_ok = False
            continue
        if not vals:
            codes.append(f"PREDICATE_MISSING:{k}")
            predicate_ok = False
            continue
        if not INT_RE.fullmatch(vals[0]) or int(vals[0]) < floor:
            codes.append(f"PREDICATE_SHORT:{k}={vals[0]}<{floor}")
            predicate_ok = False
    return codes, tokens_ok, predicate_ok


def git_blob(repo, rev, relpath):
    p = subprocess.run(["git", "-C", repo, "show", f"{rev}:{relpath}"], capture_output=True)
    return p.returncode, p.stdout


def self_pin(repo, rev, receipts_rev, expected, receipts):
    """Scoring bytes equal their blobs: driver+expectations at rev, receipts at receipts_rev.

    The receipts cannot pin their own carrier commit (they are generated from a tree before that commit exists), so
    they pin the instrument-measurement revision (`rev`) and this leg checks their bytes at the commit that carries
    them (`receipts_rev`). Both are explicit; a moved byte is `SELF_DRIFT`."""
    base = [(rel, rev) for rel in
            [os.path.relpath(os.path.abspath(__file__), os.path.abspath(repo)),
             os.path.relpath(os.path.abspath(expected), os.path.abspath(repo))]]
    base += [(os.path.relpath(os.path.join(receipts, f), os.path.abspath(repo)), receipts_rev)
             for f in sorted(os.listdir(receipts)) if f.endswith(".txt")]
    drift = []
    for rel, rv in base:
        rc, blob = git_blob(repo, rv, rel)
        disk = os.path.join(os.path.abspath(repo), rel)
        if rc != 0 or not os.path.isfile(disk):
            drift.append(rel)
            continue
        if open(disk, "rb").read() != blob:
            drift.append(rel)
    return drift


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("emit", "verify"))
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo")
    ap.add_argument("--receipts-rev", help="commit that carries the receipts (defaults to --rev)")
    ap.add_argument("--expected", default=DEFAULT_EXPECTED)
    ap.add_argument("--receipts", default=DEFAULT_RECEIPTS)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    if not REV_RE.fullmatch(a.rev):
        print("CONTROL_DRIVER_R90=SETUP --rev is not a 40-hex revision")
        return 2
    if not os.path.isfile(a.expected):
        print(f"CONTROL_DRIVER_R90=SETUP missing {a.expected}")
        return 2
    rows = read_expected(a.expected)
    if not rows:
        print("CONTROL_DRIVER_R90=SETUP no rows")
        return 2
    os.makedirs(work, exist_ok=True)

    if a.mode == "emit":
        os.makedirs(a.receipts, exist_ok=True)
        bad = 0
        for row in rows:
            cmd = row["instrument"].replace("@ROOT@", root).replace("@WORK@", work)
            rc, text = run_instrument(cmd, root)
            body = (f"# case={row['case']}\n# expected_exit={row['exit']}\n# exit={rc}\n"
                    f"# computed_against={a.rev}\n") + text
            with open(os.path.join(a.receipts, row["case"] + ".txt"), "w", encoding="utf-8") as fh:
                fh.write(body)
            ok = rc == row["exit"]
            bad += 0 if ok else 1
            print(f"EMIT {row['case']} exit={rc} want={row['exit']} {'OK' if ok else 'MISMATCH'}")
        print(f"EMITTED={len(rows)} MISMATCH={bad}")
        return 0 if bad == 0 else 1

    # verify: read the committed receipt first, never write it
    if not os.path.isdir(a.receipts):
        print(f"CONTROL_DRIVER_R90=SETUP missing receipts dir {a.receipts}")
        return 2
    committed_ok = pin_ok = fresh_ok = 0
    findings = 0
    for row in rows:
        codes = []
        path = os.path.join(a.receipts, row["case"] + ".txt")
        if not os.path.isfile(path):
            codes.append("MISSING_RECEIPT")
            text, header = "", {}
        else:
            text = open(path, encoding="utf-8").read()
            header = header_fields(text)
        if not header.get("case"):
            codes.append("MISSING_HEADER:case")
        elif header.get("case") != row["case"]:
            codes.append("HEADER_CASE")
        if "exit" not in header:
            codes.append("MISSING_HEADER:exit")
        elif not INT_RE.fullmatch(header["exit"]) or int(header["exit"]) != row["exit"]:
            codes.append(f"EXIT_MISMATCH:{header['exit']}!={row['exit']}")
        body_codes, tok_ok, pred_ok = check_body(row, text) if text else ([], False, False)
        codes += body_codes
        this_committed = not codes
        committed_ok += 1 if this_committed else 0
        # PIN
        pin = header.get("computed_against", "")
        if not REV_RE.fullmatch(pin):
            codes.append("PIN_MISSING")
            this_pin = False
        elif pin != a.rev:
            codes.append(f"PIN_MISMATCH:{pin}")
            this_pin = False
        else:
            this_pin = True
        pin_ok += 1 if this_pin else 0
        # FRESH
        cmd = row["instrument"].replace("@ROOT@", root).replace("@WORK@", work)
        frc, ftext = run_instrument(cmd, root)
        fresh_file = os.path.join(work, "fresh-" + row["case"] + ".out")
        with open(fresh_file, "w", encoding="utf-8") as fh:
            fh.write(ftext)
        this_fresh = True
        fresh_ok += 1 if this_fresh else 0
        if codes:
            findings += 1
            print(f"RECEIPT {row['case']} FINDING {','.join(codes)}")
        else:
            print(f"RECEIPT {row['case']} OK committed+exact+pin+fresh")
    if a.repo:
        drift = self_pin(a.repo, a.rev, a.receipts_rev or a.rev, a.expected, a.receipts)
        if drift:
            findings += 1
            print("RECEIPT SELF_PIN FINDING SELF_DRIFT " + ",".join(drift))
        else:
            print("RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev")
    exact_only = 0
    for row in rows:
        path = os.path.join(a.receipts, row["case"] + ".txt")
        if not os.path.isfile(path):
            continue
        _codes, tok_ok, pred_ok = check_body(row, open(path, encoding="utf-8").read())
        if tok_ok and pred_ok:
            exact_only += 1
    passed = findings == 0 and committed_ok == len(rows) and pin_ok == len(rows) and fresh_ok == len(rows)
    print(f"COMMITTED_OK={committed_ok}/{len(rows)} EXACT_OK={exact_only}/{len(rows)} "
          f"PIN_OK={pin_ok}/{len(rows)} FRESH_OK={fresh_ok}/{len(rows)} "
          f"CONTROL_DRIVER_R90={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

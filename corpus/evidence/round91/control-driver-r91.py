#!/usr/bin/env python3
"""control-driver-r91 — round-91 C1 (operability): the committed control-receipt driver, hardened.

Round 90's driver (`corpus/evidence/round90/control-driver-r90.py`) closed the four B1-B4 receipt defects and the
`considerthese/2026-11-07.md` proposal-1 duplicate-key class for BODY keys. Its own non-author spot-check
(`corpus/lessons/round-90-verifier-spotcheck.md`, routed defects 2 and 3) measured what it still accepts:

  R1  header lines are read last-wins (`header_fields()` keeps the last value), so a receipt carrying `# exit=1`
      beside `# exit=0`, or a second `# computed_against=` naming another tree, passes;
  R2  `# expected_exit=` is never read, so a receipt without it passes;
  R3  nothing binds the bytes of the instrument a row executes: a 9-line stub that prints the required tokens
      passes `FRESH_OK` (r90 `FRESH_OK=6/6`), and `instrument-pins.txt` is never read;
  R4  `SELF_PIN` printed only `at --rev`, never the receipts carrier it also pins;
  R5  `self_pin()` computed each scoring path relative to `--repo` while the files were read from `--root`
      (QUALITY 202), so the dispatch form `--root <lane> --repo <clone>` failed on correct bytes;
  R6  an extra receipt file in the receipts directory is invisible (only expected rows are read), and the
      expectations file itself is unpinned without `--repo`.

This driver is the successor. Repair map: R1 -> `HEADER_DUPLICATE` (every required header key may appear once);
R2 -> `MISSING_HEADER:expected_exit` plus an equality check; R3 -> `INSTRUMENT_PIN_MISMATCH` /
`INSTRUMENT_UNPINNED` from `instrument-pins.txt` (the pinned bytes must equal the on-disk bytes and, with `--repo`,
the blob at `--rev`); R4 -> `SELF_PIN OK ... rev=<rev> receipts_rev=<rev>`; R5 -> one `rel_for(base, path)` helper
whose base is explicit and a `BASES root=... repo=...` line; R6 -> `UNSCORED_RECEIPT` and `EXPECTED_UNPINNED`.

Usage:
    python3 -B control-driver-r91.py emit   --root LANE --work DIR --rev REV [--expected F] [--receipts D]
    python3 -B control-driver-r91.py verify --root LANE --work DIR --rev REV [--repo GITDIR] [--expected F]
                                            [--receipts D] [--pins F] [--receipts-rev REV]

Exit 0 every row OK, 1 a finding (`RECEIPT <case> FINDING <codes>`), 2 setup (bad rev, missing files).
Python 3 standard library only; no network.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXPECTED = os.path.join(HERE, "controls", "expected.tsv")
DEFAULT_RECEIPTS = os.path.join(HERE, "controls", "receipts")
DEFAULT_PINS = os.path.join(HERE, "instrument-pins.txt")
REV_RE = re.compile(r"[0-9a-f]{40}")
SHA_RE = re.compile(r"[0-9a-f]{64}")
KEYVAL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")
INT_RE = re.compile(r"-?[0-9]+")
HEADER_KEYS = ("case", "expected_exit", "exit", "computed_against")


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


def read_pins(path):
    """`<sha256>  <repo-relative path>` rows; the r90-format file is read unchanged."""
    pins = {}
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split(None, 1)
            if len(parts) != 2 or not SHA_RE.fullmatch(parts[0]):
                raise SystemExit(f"SETUP malformed pin row: {ln!r}")
            pins[parts[1].strip()] = parts[0]
    return pins


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


def header_multi(text):
    """Every `# key=value` header line in order; duplicates are visible to the caller, never collapsed."""
    out = {}
    for ln in text.splitlines():
        if not ln.startswith("# "):
            continue
        k, _, v = ln[2:].partition("=")
        if k:
            out.setdefault(k.strip(), []).append(v.strip())
    return out


def rel_for(base, path):
    """Repo-relative path of `path` under the explicit base it was READ from (QUALITY 202)."""
    return os.path.relpath(os.path.abspath(path), os.path.abspath(base))


def instrument_rel(row, root):
    """The repo-relative source file a row executes, or None when the row runs no file."""
    for tok in row["instrument"].split():
        t = tok.replace("@ROOT@", os.path.abspath(root))
        if (t.endswith(".py") or t.endswith(".sh")) and os.path.isabs(t):
            rel = rel_for(root, t)
            if not rel.startswith(".."):
                return rel
    return None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_instrument(cmd, root):
    p = subprocess.run(["bash", "-lc", cmd], cwd=root, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def check_body(row, text):
    """Return (codes, tokens_ok, predicate_ok) for one receipt body (r90 semantics for body keys)."""
    codes = []
    toks, keys = body_tokens(text)
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


def check_headers(row, header):
    """R1/R2: every required header key appears exactly once and carries the row's value."""
    codes = []
    for k in HEADER_KEYS:
        vals = header.get(k, [])
        if len(vals) > 1:
            codes.append(f"HEADER_DUPLICATE:{k}={','.join(sorted(set(vals)))}")
        elif not vals:
            codes.append(f"MISSING_HEADER:{k}")
    if len(header.get("case", [])) == 1 and header["case"][0] != row["case"]:
        codes.append(f"HEADER_CASE:{header['case'][0]}")
    if len(header.get("exit", [])) == 1:
        v = header["exit"][0]
        if not INT_RE.fullmatch(v) or int(v) != row["exit"]:
            codes.append(f"EXIT_MISMATCH:{v}!={row['exit']}")
    if len(header.get("expected_exit", [])) == 1:
        v = header["expected_exit"][0]
        if not INT_RE.fullmatch(v) or int(v) != row["exit"]:
            codes.append(f"EXPECTED_EXIT_MISMATCH:{v}!={row['exit']}")
    return codes


def pin_report(rows, root, expected, pins_path):
    """R3/R6: every instrument a row executes, and the expectations file, are pinned and unchanged on disk."""
    codes = []
    pins = read_pins(pins_path)
    if pins is None:
        return ["PINS_MISSING"], 0
    wanted = {}
    for row in rows:
        rel = instrument_rel(row, root)
        if rel is None:
            codes.append(f"INSTRUMENT_UNPINNED:{row['case']}")
            continue
        wanted[rel] = row["case"]
    wanted[rel_for(root, expected)] = "expectations"
    checked = 0
    for rel in sorted(wanted):
        disk = os.path.join(os.path.abspath(root), rel)
        if rel not in pins:
            codes.append(f"INSTRUMENT_UNPINNED:{rel}")
            continue
        if not os.path.isfile(disk):
            codes.append(f"INSTRUMENT_ABSENT:{rel}")
            continue
        if sha256_file(disk) != pins[rel]:
            codes.append(f"INSTRUMENT_PIN_MISMATCH:{rel}")
            continue
        checked += 1
    return codes, checked


def pin_at_rev(repo, rev, rels):
    """R3: the pinned bytes are the bytes the named revision carries."""
    drift = []
    for rel in rels:
        p = subprocess.run(["git", "-C", repo, "show", f"{rev}:{rel}"], capture_output=True)
        if p.returncode != 0:
            drift.append(rel)
            continue
        if hashlib.sha256(p.stdout).hexdigest() != rels[rel]:
            drift.append(rel)
    return drift


def self_pin(repo, root, rev, receipts_rev, expected, receipts, pins):
    """R4/R5: scoring bytes equal their blobs; each path is resolved against the base it is read from."""
    base = [(rel_for(root, __file__), rev), (rel_for(root, expected), rev)]
    base += [(rel_for(root, os.path.join(receipts, f)), receipts_rev)
             for f in sorted(os.listdir(receipts)) if f.endswith(".txt")]
    drift = []
    for rel, rv in base:
        p = subprocess.run(["git", "-C", repo, "show", f"{rv}:{rel}"], capture_output=True)
        disk = os.path.join(os.path.abspath(root), rel)
        if p.returncode != 0 or not os.path.isfile(disk):
            drift.append(f"{rel}@{rv}")
            continue
        if open(disk, "rb").read() != p.stdout:
            drift.append(f"{rel}@{rv}")
    pinned = {rel: sha for rel, sha in pins.items()}
    drift += [f"{rel}@{rev}" for rel in pin_at_rev(repo, rev, pinned)]
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
    ap.add_argument("--pins", default=DEFAULT_PINS)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    if not REV_RE.fullmatch(a.rev):
        print("CONTROL_DRIVER_R91=SETUP --rev is not a 40-hex revision")
        return 2
    if not os.path.isfile(a.expected):
        print(f"CONTROL_DRIVER_R91=SETUP missing {a.expected}")
        return 2
    if not os.path.isfile(a.pins) and a.mode == "verify":
        print(f"CONTROL_DRIVER_R91=SETUP missing {a.pins}")
        return 2
    rows = read_expected(a.expected)
    if not rows:
        print("CONTROL_DRIVER_R91=SETUP no rows")
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
        print(f"CONTROL_DRIVER_R91=SETUP missing receipts dir {a.receipts}")
        return 2
    print(f"BASES root={root} repo={os.path.abspath(a.repo) if a.repo else root}")
    pins = read_pins(a.pins)
    if pins is None:
        print(f"CONTROL_DRIVER_R91=SETUP missing pins {a.pins}")
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
            header = header_multi(text)
        codes += check_headers(row, header)
        body_codes, tok_ok, pred_ok = check_body(row, text) if text else ([], False, False)
        codes += body_codes
        this_committed = not codes
        committed_ok += 1 if this_committed else 0
        # PIN of the receipt's own revision header
        pinv = header.get("computed_against", [])
        if len(pinv) == 1 and REV_RE.fullmatch(pinv[0]) and pinv[0] == a.rev:
            this_pin = True
        else:
            codes.append("PIN_MISSING" if not pinv else "PIN_MISMATCH:" + ",".join(pinv))
            this_pin = False
        pin_ok += 1 if this_pin else 0
        # FRESH
        cmd = row["instrument"].replace("@ROOT@", root).replace("@WORK@", work)
        frc, ftext = run_instrument(cmd, root)
        fresh_file = os.path.join(work, "fresh-" + row["case"] + ".out")
        with open(fresh_file, "w", encoding="utf-8") as fh:
            fh.write(ftext)
        this_fresh = frc == row["exit"]
        if not this_fresh:
            codes.append(f"FRESH_EXIT:{frc}")
        fbody = f"# case={row['case']}\n# expected_exit={row['exit']}\n# exit={frc}\n" + ftext
        fcodes, _ftok, _fpred = check_body(row, fbody)
        if fcodes:
            codes += [f"FRESH_{c}" for c in fcodes]
            this_fresh = False
        fresh_ok += 1 if this_fresh else 0
        if codes:
            findings += 1
            print(f"RECEIPT {row['case']} FINDING {','.join(codes)}")
        else:
            print(f"RECEIPT {row['case']} OK committed+exact+pin+fresh")
    # R6: a receipt that no expected row scores is a finding, not an invisible file.
    scored = {row["case"] for row in rows}
    for f in sorted(os.listdir(a.receipts)):
        if not f.endswith(".txt") or f[:-4] in scored:
            continue
        body = open(os.path.join(a.receipts, f), encoding="utf-8", errors="replace").read()
        if "# case=" not in body:
            continue  # raw instrument evidence, not a receipt
        findings += 1
        print(f"RECEIPT {f[:-4]} FINDING UNSCORED_RECEIPT")
    # R3/R6 at the tree: instruments and the expectations file are pinned; with --repo also at --rev.
    pcodes, checked = pin_report(rows, root, a.expected, a.pins)
    if pcodes:
        findings += 1
        print("RECEIPT PINS FINDING " + ",".join(pcodes))
    else:
        print(f"RECEIPT PINS OK {checked}/{len(pins)} pinned files byte-identical")
    if a.repo:
        drift = self_pin(a.repo, root, a.rev, a.receipts_rev or a.rev, a.expected, a.receipts, pins)
        if drift:
            findings += 1
            print("RECEIPT SELF_PIN FINDING SELF_DRIFT " + ",".join(drift))
        else:
            print(f"RECEIPT SELF_PIN OK rev={a.rev} receipts_rev={a.receipts_rev or a.rev}")
    exact_only = 0
    for row in rows:
        path = os.path.join(a.receipts, row["case"] + ".txt")
        if not os.path.isfile(path):
            continue
        _codes, tok_ok, pred_ok = check_body(row, open(path, encoding="utf-8").read())
        if tok_ok and pred_ok:
            exact_only += 1
    passed = (findings == 0 and committed_ok == len(rows) and pin_ok == len(rows)
              and fresh_ok == len(rows))
    print(f"COMMITTED_OK={committed_ok}/{len(rows)} EXACT_OK={exact_only}/{len(rows)} "
          f"PIN_OK={pin_ok}/{len(rows)} FRESH_OK={fresh_ok}/{len(rows)} PINNED_FILES={checked} "
          f"CONTROL_DRIVER_R91={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

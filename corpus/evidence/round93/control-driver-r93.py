#!/usr/bin/env python3
"""control-driver-r93 — round-93 C1 (operability): the committed control-receipt driver, hardened.

Successor of `control-driver-r92.py`. Round 92's landed receipt prints `PINNED_FILES=7` — only 7 of the 16
rows of `instrument-pins.txt` are byte-checked, because `pin_report` walks only the instruments the
expected rows execute plus the expectations and pins files (`RECEIPT PINS OK 7/16 pinned files
byte-identical`). The other nine pinned instruments are never compared on disk, and the committed receipts
under `--receipts` are read but pinned nowhere — a tampered instrument copy verifies the same as a blob
change.

Repair map: T1 -> `pin_report` walks every row of the pins file and byte-checks each pinned path on disk
(`PIN_DISK_MISMATCH path=<rel>` fired per row, so `PINNED_FILES=16/16`), the pins file's own self row
staying on the minus-self digest; T2 -> every committed receipt under `--receipts` is byte-checked
against a minus-self digest pinned in the pins table (`RECEIPT_MISMATCH <case>` /
`RECEIPT_UNPINNED <case>`, 6 rows, `RECEIPT_DOWNLOAD_OK=6/6`). T3 path derivation: `--expected`,
`--receipts` and `--pins` default under `corpus/evidence/round93/` relative to the `--root` tree, never
relative to the driver file's own directory; the driver's own directory stays for the scorer's own
hash (`__file__` self-pin only). `emit`'s receipts directory is NOT silently defaulted: the procedure
always names `--receipts` for `emit` (see `corpus/evidence/round93/after/c1-procedure.txt`), and
`verify` never writes under the receipts directory.

Forgeries are named by the new codes: `PIN_DISK_MISMATCH`, `RECEIPT_MISMATCH`,
`RECEIPT_UNPINNED`, `EMPTY_RECEIPTS`, `PINS_LINE_AFFECTED`, `HEADER_PROVEN` (see
`corpus/evidence/round93/forgeries-r93.py`).

Usage:
    python3 -B control-driver-r93.py emit   --root LANE --work DIR --rev REV [--expected F] [--receipts D]
    python3 -B control-driver-r93.py verify --root LANE --work DIR --rev REV [--repo GITDIR] [--expected F]
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
# T3: no DEFAULT_* paths are taken from HERE. Every input is derived from --root in main(), so the
# driver file's own directory can never decide which fixture is scored; HERE survives only for
# this file's own self-pin (rel_for(root, __file__)).
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
            path = parts[1].strip()
            if path in pins:
                print(f"SETUP PIN_DUPLICATE path={path}")
                raise SystemExit(2)
            pins[path] = parts[0]
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
        stripped = ln.lstrip()
        if not stripped.startswith("# ") and stripped != "#":
            continue
        k, _, v = stripped[2:].partition("=") if stripped.startswith("# ") else ("", "", "")
        if k:
            out.setdefault(k.strip(), []).append(v.strip())
    return out


def rel_for(base, path):
    """Repo-relative path of `path` under the explicit base it was READ from (QUALITY 202).
    A path outside the base is a setup error, never a scoreable byte (r92 sentinel F4)."""
    rel = os.path.relpath(os.path.abspath(path), os.path.abspath(base))
    if rel == ".." or rel.startswith(".." + os.sep):
        raise SystemExit(f"SETUP path escapes base: {path} vs {base}")
    return rel


def instrument_rels(row, root):
    """Repo-relative source files a row executes (every in-tree .py/.sh token, in order)."""
    rels = []
    for tok in row["instrument"].split():
        t = tok.replace("@ROOT@", os.path.abspath(root))
        if (t.endswith(".py") or t.endswith(".sh")) and os.path.isabs(t):
            rel = rel_for(root, t)
            if not rel.startswith(".."):
                rels.append(rel)
    return rels


def instrument_rel(row, root):
    """The first source file a row executes (kept for compatibility; pinning uses instrument_rels)."""
    rels = instrument_rels(row, root)
    return rels[0] if rels else None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pins_file_sha_minus_self(pins_path, self_rel):
    """sha256 of the pins file's rows with its own self row removed (S5 self-pin)."""
    import hashlib as _h
    h = _h.sha256()
    with open(pins_path, encoding="utf-8") as fh:
        for ln in fh:
            if not ln.strip() or ln.startswith("#"):
                continue
            parts = ln.split(None, 1)
            if len(parts) == 2 and parts[1].strip() == self_rel:
                continue
            h.update(ln.encode("utf-8"))
    return h.hexdigest()

def receipt_pins(root, receipts_dir, pins):
    """T2: every committed receipt is pinned by its own row; a changed or unlisted body is a finding.

    Returns (codes, checked). A receipt file with no pin row is `RECEIPT_UNPINNED <case>`; a body whose
    sha256 differs from its row is `RECEIPT_MISMATCH <case>`; a pin row naming a receipt that is gone is
    `RECEIPT_MISSING <case>`. `checked` counts receipt rows verified byte-identical.
    """
    codes = []
    checked = 0
    disk_files = sorted(f for f in os.listdir(receipts_dir) if f.endswith(".txt"))
    disk_rels = {rel_for(root, os.path.join(receipts_dir, f)): f for f in disk_files}
    for rel, f in sorted(disk_rels.items()):
        if rel not in pins:
            codes.append(f"RECEIPT_UNPINNED:{f[:-4]}")
            continue
        if sha256_file(os.path.join(os.path.abspath(root), rel)) != pins[rel]:
            codes.append(f"RECEIPT_MISMATCH:{f[:-4]}")
            continue
        checked += 1
    receipts_prefix = rel_for(root, receipts_dir) + os.sep
    for rel in sorted(pins):
        if not rel.startswith(receipts_prefix):
            continue
        if rel not in disk_rels:
            codes.append(f"RECEIPT_MISSING:{os.path.basename(rel)[:-4]}")
    return codes, checked, len(disk_files)



def scrub_env(root):
    """Minimal env for fresh legs: PATH from this process, HOME the tree root (no rc/profile reads)."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.path.abspath(root)}
    return env


def run_instrument(cmd, root):
    p = subprocess.run(["bash", "-c", cmd], cwd=root, capture_output=True, text=True, env=scrub_env(root))
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


def pin_report(rows, root, expected, pins_path, receipts_dir):
    """T1/T2: every row of the pins file is byte-checked on disk, and every committed receipt is pinned.

    The r92 driver walked only the instruments the expected rows execute plus the expectations and pins
    files (7 of 16 rows), so nine pinned instruments could be tampered with unnoticed. The r93 walk takes
    the pins table as the population: each row is one sha256 over its file (the pins file's own row stays
    the minus-self digest, S5), and the receipts directory contributes one row per committed receipt.
    """
    codes = []
    pins = read_pins(pins_path)
    if pins is None:
        return ["PINS_MISSING"], 0, 0, 0
    pins_rel = rel_for(root, pins_path)
    wanted = {}
    for row in rows:
        rels = instrument_rels(row, root)
        if not rels:
            codes.append(f"INSTRUMENT_UNPINNED:{row['case']}")
            continue
        for rel in rels:
            wanted[rel] = row["case"]
    wanted[rel_for(root, expected)] = "expectations"
    for rel in sorted(wanted):
        if rel not in pins:
            codes.append(f"INSTRUMENT_UNPINNED:{rel}")
    checked = 0
    for rel in sorted(pins):
        disk = os.path.join(os.path.abspath(root), rel)
        if not os.path.isfile(disk):
            codes.append(f"PIN_MISSING path={rel}")
            continue
        if rel == pins_rel:
            if pins_file_sha_minus_self(disk, rel) != pins[rel]:
                codes.append(f"INSTRUMENT_PIN_MISMATCH:{rel}")
                continue
        elif sha256_file(disk) != pins[rel]:
            codes.append(f"PIN_DISK_MISMATCH path={rel}")
            continue
        checked += 1
    rcodes, rchecked, rtotal = receipt_pins(root, receipts_dir, pins)
    codes += rcodes
    return codes, checked, rchecked, rtotal



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


def self_pin(repo, root, rev, receipts_rev, expected, receipts, pins_rows, pins_path):
    """R4/R5/T3: scoring bytes equal their blobs; each pin is checked at the base it is read from.

    `--rev` carries the instruments and the expectations file; `--receipts-rev` carries the committed
    receipts and the pins table itself (the table is cut once the receipts exist, so it lives at the
    carrier). Receipt rows are compared at `receipts_rev`, never at `rev` — the r92 driver would report a
    receipt as drifted at a revision that never held it.
    """
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
    # The pins file's own pin is the minus-self digest (S5), not the whole-file sha, so it must not go
    # through pin_at_rev's whole-blob comparison. Every other row does, at the base that carries it.
    receipts_rel = rel_for(root, receipts)
    pins_rel = rel_for(root, pins_path)
    at_rev = {rel: sha for rel, sha in pins_rows.items()
              if rel != pins_rel and not rel.startswith(receipts_rel + os.sep)}
    at_carrier = {rel: sha for rel, sha in pins_rows.items()
                  if rel != pins_rel and rel.startswith(receipts_rel + os.sep)}
    drift += [f"{rel}@{rev}" for rel in pin_at_rev(repo, rev, at_rev)]
    drift += [f"{rel}@{receipts_rev}" for rel in pin_at_rev(repo, receipts_rev, at_carrier)]
    # S5 revival check: the blob at the carrier must satisfy the stored minus-self digest too.
    if pins_rel in pins_rows:
        blob = subprocess.run(["git", "-C", repo, "show", f"{receipts_rev}:{pins_rel}"], capture_output=True)
        if blob.returncode != 0:
            drift.append(f"{pins_rel}@{receipts_rev}")
        else:
            import io as _io
            h = hashlib.sha256()
            for ln in _io.BytesIO(blob.stdout).read().splitlines():
                if ln.endswith(pins_rel.encode()):
                    continue
                h.update(ln + b"\n")
            if h.hexdigest() != pins_rows[pins_rel]:
                drift.append(f"{pins_rel}@{receipts_rev}")
    return drift



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("emit", "verify"))
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or "/fast/scratch/hyaku",
                    help="scratch root for fresh-leg outputs (default: $TMPDIR, else /fast/scratch/hyaku)")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo")
    ap.add_argument("--receipts-rev", help="commit that carries the receipts (defaults to --rev)")
    ap.add_argument("--expected", help="default: <root>/corpus/evidence/round93/controls/expected.tsv")
    ap.add_argument("--receipts", help="default: <root>/corpus/evidence/round93/controls/receipts")
    ap.add_argument("--pins", help="default: <root>/corpus/evidence/round93/instrument-pins.txt")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    # T3: every input defaults under the tree named by --root, never under this file's directory, so the
    # `--root <clone>` dispatch form cannot hit rel_for's escape class on its own defaults.
    a.expected = a.expected or os.path.join(root, "corpus/evidence/round93/controls/expected.tsv")
    a.receipts = a.receipts or os.path.join(root, "corpus/evidence/round93/controls/receipts")
    a.pins = a.pins or os.path.join(root, "corpus/evidence/round93/instrument-pins.txt")

    if not REV_RE.fullmatch(a.rev):
        print("CONTROL_DRIVER_R93=SETUP --rev is not a 40-hex revision")
        return 2
    if not os.path.isfile(a.expected):
        print(f"CONTROL_DRIVER_R93=SETUP missing {a.expected}")
        return 2
    if not os.path.isfile(a.pins) and a.mode == "verify":
        print(f"CONTROL_DRIVER_R93=SETUP missing {a.pins}")
        return 2
    rows = read_expected(a.expected)
    if not rows:
        print("CONTROL_DRIVER_R93=SETUP no rows")
        return 2
    os.makedirs(work, exist_ok=True)

    if a.mode == "emit":
        if "--receipts" not in sys.argv:
            print("CONTROL_DRIVER_R93=SETUP emit requires an explicit --receipts")
            return 2
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
        print(f"CONTROL_DRIVER_R93=SETUP missing receipts dir {a.receipts}")
        return 2
    print(f"BASES root={root} repo={os.path.abspath(a.repo) if a.repo else root}")
    pins = read_pins(a.pins)
    if pins is None:
        print(f"CONTROL_DRIVER_R93=SETUP missing pins {a.pins}")
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
    # T1/T2 at the tree: every row of the pins file and every committed receipt are byte-checked;
    # with --repo the same bytes are checked against the blobs at --rev / --receipts-rev.
    pcodes, checked, rchecked, rtotal = pin_report(rows, root, a.expected, a.pins, a.receipts)
    if pcodes:
        findings += 1
        print("RECEIPT PINS FINDING " + ",".join(pcodes))
    else:
        print(f"RECEIPT PINS OK {checked}/{len(pins)} pinned files byte-identical "
              f"RECEIPT_PINS_OK={rchecked}/{rtotal}")

    if a.repo:
        drift = self_pin(a.repo, root, a.rev, a.receipts_rev or a.rev, a.expected, a.receipts, pins, a.pins)
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
    passed = (findings == 0 and committed_ok == len(rows) and exact_only == len(rows)
              and pin_ok == len(rows) and fresh_ok == len(rows)
              and checked == len(pins) and rchecked == rtotal and rtotal > 0)
    print(f"COMMITTED_OK={committed_ok}/{len(rows)} EXACT_OK={exact_only}/{len(rows)} "
          f"PIN_OK={pin_ok}/{len(rows)} FRESH_OK={fresh_ok}/{len(rows)} "
          f"PINNED_FILES={checked}/{len(pins)} RECEIPT_PINS={rchecked}/{rtotal} "
          f"CONTROL_DRIVER_R93={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

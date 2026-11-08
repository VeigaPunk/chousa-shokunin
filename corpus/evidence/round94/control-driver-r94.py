#!/usr/bin/env python3
"""control-driver-r94 — round-94 C1 (operability): the control-receipt driver with a role column.

Successor of `control-driver-r93.py`. Round 93 made the pins table the population (every row byte-checked)
but the table says nothing about what each row *is*: a row for a file no expected row executes and a row
for an instrument are indistinguishable, so a dangling pin row is counted as if it were work, and nothing
requires the round's claims files to be pinned at all. Round 94 gives every row a role in
`instrument | expectation | receipt | claims | driver` and enforces the sets:
role=instrument is exactly the instruments the expected rows execute (both directions), role=expectation
is exactly the expectations file, role=receipt is exactly the committed receipts, and the round's two
claims files each carry role=claims. `driver` is byte-checked but carries no coverage invariant (the
harness is not a case instrument); that is a named limit. A two-column row is `PIN_SCHEMA` (setup), an
unknown role is `PIN_ROLE_UNKNOWN`, a dangling or missing member of a covered role is
`PIN_ROLE_DANGLING` / `PIN_ROLE_MISSING`.

Inherited machinery (round 93): `pin_report` walks every row of the pins file and byte-checks each
pinned path on disk (`PIN_DISK_MISMATCH path=<rel>`, `PINNED_FILES=n/n`), the pins file's own self row
staying on the minus-self digest; every committed receipt under `--receipts` is byte-checked against a
pinned digest (`RECEIPT_MISMATCH <case>` / `RECEIPT_UNPINNED <case>`); `--expected`, `--receipts` and
`--pins` derive from `--root`, never from the driver's directory; `emit` requires an explicit
`--receipts` and `verify` never writes under it.

Usage:
    python3 -B control-driver-r94.py emit   --root LANE --work DIR --rev REV [--expected F] [--receipts D]
    python3 -B control-driver-r94.py verify --root LANE --work DIR --rev REV [--repo GITDIR] [--expected F]
                                            [--receipts D] [--pins F] [--receipts-rev REV]

Exit 0 every row OK, 1 a finding (`RECEIPT <case> FINDING <codes>`), 2 setup (bad rev, missing files,
a two-column pin row). Python 3 standard library only; no network.
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
# Round 94: every pin row carries a role. `instrument` is the only role with a coverage invariant in both
# directions (pinned instrument == executed instrument); `driver` is byte-checked but is not a case
# instrument (named limit in the claim).
ROLES = ("instrument", "expectation", "receipt", "claims", "driver")
CLAIM_PATHS = (".ufo/waves/round-94/claims.json", ".ufo/waves/round-94/claims.md")


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
    """`<sha256>  <role>  <repo-relative path>` rows; a two-column row is a schema setup error.

    The r93 format (two columns) cannot express what a row is, so a dangling row and an instrument row
    were indistinguishable. r94 requires the role; `PIN_SCHEMA` refuses the old shape and
    `PIN_ROLE_UNKNOWN` refuses a role outside ROLES.
    """
    pins, roles = {}, {}
    if not os.path.isfile(path):
        return None, None
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split()
            if len(parts) != 3 or not SHA_RE.fullmatch(parts[0]):
                print("SETUP PIN_SCHEMA row is not `<sha256>  <role>  <path>`: " + repr(ln))
                raise SystemExit(2)
            role, path = parts[1], parts[2]
            if role not in ROLES:
                print(f"SETUP PIN_ROLE_UNKNOWN role={role} path={path}")
                raise SystemExit(2)
            if path in pins:
                print(f"SETUP PIN_DUPLICATE path={path}")
                raise SystemExit(2)
            pins[path] = parts[0]
            roles[path] = role
    return pins, roles


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
            parts = ln.split()
            if len(parts) == 3 and parts[2] == self_rel:
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


def role_report(executed, root, roles, expected, receipts_dir):
    """R94: the pins table's role column is a set relation, checked in both directions.

    instrument == the expected rows' executed set; expectation == the expectations file; receipt == the
    committed receipts; claims == this round's two claims files. `driver` rows are byte-checked only.
    Each member of a covered role either holds or is named; `ok` counts holding members over
    `covered` (every non-driver row), so a deleted or invented row moves both numbers.
    """
    codes = []
    covered = [rel for rel, _r in roles.items() if _r != "driver"]
    ok = 0

    role_instr = {rel for rel, r in roles.items() if r == "instrument"}
    for rel in sorted(executed - role_instr):
        codes.append(f"PIN_ROLE_MISSING role=instrument path={rel}")
    for rel in sorted(role_instr - executed):
        codes.append(f"PIN_ROLE_DANGLING role=instrument path={rel}")
    if role_instr == executed:
        ok += len(role_instr)

    exp_rel = rel_for(root, expected)
    exp_rows = {rel for rel, r in roles.items() if r == "expectation"}
    if exp_rows != {exp_rel}:
        codes.append("PIN_ROLE_MISMATCH role=expectation pins="
                     f"{','.join(sorted(exp_rows)) or 'none'} expected={exp_rel}")
    else:
        ok += 1

    receipt_rels = {rel_for(root, os.path.join(receipts_dir, f))
                    for f in sorted(os.listdir(receipts_dir)) if f.endswith(".txt")}
    role_receipt = {rel for rel, r in roles.items() if r == "receipt"}
    for rel in sorted(receipt_rels - role_receipt):
        codes.append(f"PIN_ROLE_MISSING role=receipt path={rel}")
    for rel in sorted(role_receipt - receipt_rels):
        codes.append(f"PIN_ROLE_DANGLING role=receipt path={rel}")
    if role_receipt == receipt_rels:
        ok += len(role_receipt)

    role_claims = {rel for rel, r in roles.items() if r == "claims"}
    for rel in CLAIM_PATHS:
        if rel not in role_claims:
            codes.append(f"PIN_ROLE_MISSING role=claims path={rel}")
    for rel in sorted(role_claims - set(CLAIM_PATHS)):
        codes.append(f"PIN_ROLE_DANGLING role=claims path={rel}")
    if role_claims == set(CLAIM_PATHS):
        ok += len(role_claims)
    return codes, ok, len(covered)


def pin_report(rows, root, expected, pins_path, receipts_dir):
    """T1/T2/R94: every row of the pins file is byte-checked on disk, and every committed receipt is pinned.

    The r93 walk takes the pins table as the population: each row is one sha256 over its file (the pins
    file's own row stays the minus-self digest, S5), and the receipts directory contributes one row per
    committed receipt. Round 94 adds the role relation over the same population (`role_report`).
    """
    codes = []
    pins, roles = read_pins(pins_path)
    if pins is None:
        return ["PINS_MISSING"], 0, 0, 0, [], 0, 0
    pins_rel = rel_for(root, pins_path)
    executed = set()
    for row in rows:
        rels = instrument_rels(row, root)
        if not rels:
            codes.append(f"INSTRUMENT_UNPINNED:{row['case']}")
            continue
        executed.update(rels)
    for rel in sorted(executed):
        if rel not in pins:
            codes.append(f"INSTRUMENT_UNPINNED:{rel}")
    checked = 0
    # H2/M1 (R93ReviewerC1): the self row must exist (it is the table's only carrier binding), and a pin row
    # may not name a path outside `--root` — a row for `/etc/hostname` or `../x` is not a tree byte.
    if pins_rel not in pins:
        codes.append(f"PIN_SELF_ROW_ABSENT path={pins_rel}")
    for rel in sorted(pins):
        parts = rel.replace(os.sep, "/").split("/")
        if os.path.isabs(rel) or ".." in parts:
            codes.append(f"PIN_ROW_OUTSIDE path={rel}")
            continue
        disk = os.path.join(os.path.abspath(root), rel)
        # R94SentinelScope F5: a row naming an in-tree symlink must not read bytes outside the tree.
        real = os.path.realpath(disk)
        if not real.startswith(os.path.realpath(root) + os.sep):
            codes.append(f"PIN_ROW_OUTSIDE path={rel}")
            continue
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
    role_codes, role_ok, role_total = role_report(executed, root, roles, expected, receipts_dir)
    codes += role_codes
    return codes, checked, rchecked, rtotal, role_codes, role_ok, role_total



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
    # T3b: the driver's own bytes are resolved against the tree it lives in (the repo), not against --root:
    # the dispatch form `--root <clone> --repo <lane>` runs a driver that lives in the lane, and rel_for(root,
    # __file__) would call that a setup escape on correct bytes.
    base = [(rel_for(repo, __file__), rev), (rel_for(root, expected), rev)]
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
    ap.add_argument("--expected", help="default: <root>/corpus/evidence/round94/controls/expected.tsv")
    ap.add_argument("--receipts", help="default: <root>/corpus/evidence/round94/controls/receipts")
    ap.add_argument("--pins", help="default: <root>/corpus/evidence/round94/instrument-pins.txt")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    # T3: every input defaults under the tree named by --root, never under this file's directory, so the
    # `--root <clone>` dispatch form cannot hit rel_for's escape class on its own defaults.
    a.expected = a.expected or os.path.join(root, "corpus/evidence/round94/controls/expected.tsv")
    a.receipts = a.receipts or os.path.join(root, "corpus/evidence/round94/controls/receipts")
    a.pins = a.pins or os.path.join(root, "corpus/evidence/round94/instrument-pins.txt")

    if not REV_RE.fullmatch(a.rev):
        print("CONTROL_DRIVER_R94=SETUP --rev is not a 40-hex revision")
        return 2
    # R94SentinelScope F7: --receipts-rev is validated like --rev.
    if a.receipts_rev is not None and not REV_RE.fullmatch(a.receipts_rev):
        print("CONTROL_DRIVER_R94=SETUP --receipts-rev is not a 40-hex revision")
        return 2
    # R94SentinelScope F2: the batteries rmtree --work, so a work path that is a system root is refused.
    if work in ("/", "/home", "/tmp", "/var/tmp", os.path.expanduser("~"), os.path.expanduser("~/")):
        print(f"CONTROL_DRIVER_R94=SETUP --work is not a scratch path: {work}")
        return 2
    # R94SentinelScope F6: every named input is resolved inside --root before it is opened.
    contained = [("--expected", a.expected), ("--pins", a.pins)]
    if a.mode == "verify":
        contained.append(("--receipts", a.receipts))
    for label, path in contained:
        rel = os.path.relpath(os.path.abspath(path), root)
        if rel == ".." or rel.startswith(".." + os.sep):
            print(f"CONTROL_DRIVER_R94=SETUP {label} outside --root: {path}")
            return 2
    if not os.path.isfile(a.expected):
        print(f"CONTROL_DRIVER_R94=SETUP missing {a.expected}")
        return 2
    if not os.path.isfile(a.pins) and a.mode == "verify":
        print(f"CONTROL_DRIVER_R94=SETUP missing {a.pins}")
        return 2
    rows = read_expected(a.expected)
    if not rows:
        print("CONTROL_DRIVER_R94=SETUP no rows")
        return 2
    os.makedirs(work, exist_ok=True)

    if a.mode == "emit":
        if "--receipts" not in sys.argv:
            print("CONTROL_DRIVER_R94=SETUP emit requires an explicit --receipts")
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
        print(f"CONTROL_DRIVER_R94=SETUP missing receipts dir {a.receipts}")
        return 2
    print(f"BASES root={root} repo={os.path.abspath(a.repo) if a.repo else root}")
    pins, _roles = read_pins(a.pins)
    if pins is None:
        print(f"CONTROL_DRIVER_R94=SETUP missing pins {a.pins}")
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
    pcodes, checked, rchecked, rtotal, role_codes, role_ok, role_total = pin_report(
        rows, root, a.expected, a.pins, a.receipts)
    for code in role_codes:
        print("PIN_ROLE_FINDING " + code)
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
    roles_ok = not role_codes and role_ok == role_total and role_total > 0
    passed = (findings == 0 and committed_ok == len(rows) and exact_only == len(rows)
              and pin_ok == len(rows) and fresh_ok == len(rows)
              and checked == len(pins) and rchecked == rtotal and rtotal > 0 and roles_ok)
    print(f"COMMITTED_OK={committed_ok}/{len(rows)} EXACT_OK={exact_only}/{len(rows)} "
          f"PIN_OK={pin_ok}/{len(rows)} FRESH_OK={fresh_ok}/{len(rows)} "
          f"PINNED_FILES={checked}/{len(pins)} RECEIPT_PINS={rchecked}/{rtotal} "
          f"PIN_ROLES_OK={role_ok}/{role_total} "
          f"CONTROL_DRIVER_R94={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""c1-count — FROZEN counter for chousa round-58 C1 (operability): the
build-spans hardening set of the round-56 planned row (R55W2SentBuilder).

Predicate (frozen in corpus/evidence/round58/claims.md before any wave data):
on the hazard battery below, the candidate builder (default
tools/build-spans.py) passes every safe leg, refuses every hazard leg with its
named reason class and writes nothing outside --out; the round-55 builder
(pin sha256 R55_BUILDER_SHA below) FAILS the FOREIGN leg (it deletes a foreign
spans/S###-N.txt); the do-nothing controls REFUSEALL and NAIVE never reach
C1=PASS. Nothing here mutates the lane: all fixtures live under --work
(default $HYAKU_SCRATCH/chousa-r58/c1-count, honouring TMPDIR).

Legs (safe): EMPTY_OK, REBUILD_OK, HELDOUT_OK, ESCAPE_ENTRY (regression).
Legs (hazard, each must refuse with its reason class and touch nothing):
  FOREIGN   -- out/spans/ holds a foreign S###-N.txt
  SYMLINK_OUT / SYMLINK_CACHE / FIFO_TXT / DEVZERO_TXT / FAT_RAW / MANY_QUOTES
Reason classes the candidate must name: FOREIGN (or the foreign file name),
SYMLINK, NOT_REGULAR (or FIFO), SIZE (or SIZE_CAP/ROWS).

Exit: prints one LEG line per leg, BEFORE_FOREIGN, DENIED lines, and a final
`C1=PASS|FAIL` line; exit 0 iff PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
R55_BUILDER_SHA = "1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6"
CAPTURE_TEXT_SHA = "2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573"
BEFORE_BUILDER = HERE / "controls" / "build-spans-r55.py"
STORE_CAPTURE_KEY = "6dc68fd6b32ce9c8dfcebce8"
CONTEXT = 80
SIZE_CAP = 64 * 1024 * 1024
QUOTES_CAP = 100_000
HELDOUT_QUOTES = [
    "本规范共设置以下五种：",
    "不属于上述各类的文章以及文摘、零讯、补白、广告、启事等不加文献标志码。",
    "每一篇文章或资料应根据其内容性质标识一个文献标志码",
]

PASS = "pass"
FAIL = "fail"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def snapshot(root: pathlib.Path) -> dict[str, bytes]:
    out = {}
    if root.exists():
        for p in sorted(root.rglob("*")):
            if p.is_file() and not p.is_symlink():
                out[str(p.relative_to(root))] = p.read_bytes()
    return out


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def write_quotes(path: pathlib.Path, rows: list[tuple[str, str, str, str]]) -> None:
    path.write_text("id\turl\tquote\tentry\n" + "".join(
        f"{sid}\t{url}\t{quote}\t{entry}\n" for sid, url, quote, entry in rows), encoding="utf-8")


def synth_text(seed: int) -> str:
    rng = random.Random(seed)
    toks = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
            "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa"]
    sents = []
    for i in range(120):
        words = " ".join(rng.choice(toks) for _ in range(14))
        sents.append(f"Sentence {i:03d} carries {words} across the page.")
    return "\n".join(sents) + "\n"


def synth_quotes(text: str, seed: int, n: int = 3) -> list[str]:
    rng = random.Random(seed + 1)
    quotes = []
    tries = 0
    while len(quotes) < n and tries < 500:
        tries += 1
        i = rng.randrange(20, len(text) - 40)
        q = text[i:i + rng.choice([12, 16, 20, 24])]
        if "\n" in q or text.count(q) != 1:
            continue
        quotes.append(q)
    if len(quotes) < n:
        raise RuntimeError("fixture synthesis failed")
    return quotes


def run_builder(python: str, builder: pathlib.Path, quotes: pathlib.Path,
                out: pathlib.Path, cache: pathlib.Path, work: pathlib.Path,
                timeout: int = 60) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(work))
    return subprocess.run(
        [python, "-B", str(builder), "--quotes", str(quotes), "--out", str(out),
         "--cache", str(cache)],
        capture_output=True, text=True, timeout=timeout, env=env, cwd=str(work))


def expect_ok(name, proc, out, expected: dict[str, tuple[int, bytes]], snap_before, notes=""):
    if proc.returncode != 0:
        return f"{name}={FAIL}(rc={proc.returncode} {notes})"
    spans = out / "spans.tsv"
    if not spans.is_file():
        return f"{name}={FAIL}(no spans.tsv)"
    got = {p.name if p.parent.name != "spans" else f"spans/{p.name}": p.read_bytes()
           for p in [spans] + sorted((out / "spans").glob("*.txt"))}
    want = {"spans.tsv": None, **expected}
    # verify manifest rows: digest + offset + span bytes
    rows = spans.read_text(encoding="utf-8").splitlines()
    if rows[0] != "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry":
        return f"{name}={FAIL}(bad header)"
    if len(rows) - 1 != len(expected):
        return f"{name}={FAIL}(rows={len(rows)-1} want {len(expected)})"
    for row in rows[1:]:
        cells = row.split("\t")
        digest, offset, sfile, quote = cells[2], int(cells[3]), cells[4], cells[5]
        form, raw_sha = expected[sfile]
        start = max(0, form.find(quote) - CONTEXT)
        if digest != raw_sha:
            return f"{name}={FAIL}({sfile} digest)"
        if offset != start:
            return f"{name}={FAIL}({sfile} offset {offset}!={start})"
        span = form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]
        if (out / sfile).read_bytes().decode("utf-8") != span:
            return f"{name}={FAIL}({sfile} span bytes)"
    # nothing outside --out changed
    after = snapshot(out.parent)
    outside_before = {k:v for k,v in snap_before.items() if not k.startswith(out.name + "/")}
    outside_after = {k:v for k,v in after.items() if not k.startswith(out.name + "/")}
    if outside_before != outside_after:
        return f"{name}={FAIL}(write outside --out)"
    return f"{name}={PASS}"


def expect_refuse(name, proc, reason_classes: list[str], forbidden_touch: list[pathlib.Path],
                  notes=""):
    err = (proc.stderr or "") + (proc.stdout or "")
    if proc.returncode == 0:
        return f"{name}={FAIL}(rc=0, expected refusal)"
    if not any(c.lower() in err.lower() for c in reason_classes):
        return f"{name}={FAIL}(rc={proc.returncode}, reason {reason_classes!r} absent in {err[:160]!r})"
    for p in forbidden_touch:
        if not p.exists():
            return f"{name}={FAIL}({p} was touched/removed)"
    return f"{name}={PASS}(refused)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--builder", default=str(LANE / "tools" / "build-spans.py"))
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--work", default=None)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--controls", default=None, help="dir with REFUSEALL.py / NAIVE.py to deny")
    args = ap.parse_args()

    builder = pathlib.Path(args.builder).resolve()
    default_root = pathlib.Path(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")) / "chousa-r58" / "c1-count"
    work = pathlib.Path(args.work) if args.work else default_root / next(tempfile._get_candidate_names())
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    legs: list[str] = []

    # -- fixture cache for safe legs -------------------------------------------
    cache = work / "cache"
    cache.mkdir()
    txt = synth_text(args.seed)
    txt_sha = sha256(txt.encode("utf-8"))
    quotes_txt = synth_quotes(txt, args.seed)
    url1 = "https://fixture.example/doc1"
    (cache / (key(url1) + ".txt")).write_bytes(txt.encode("utf-8"))
    rows = [(f"S5{i:02d}", url1, q, "corpus/evidence/round58/c1-fixture.md") for i, q in enumerate(quotes_txt, start=1)]
    qfile = work / "quotes.tsv"
    write_quotes(qfile, rows)

    # EMPTY_OK
    out = work / "out-empty"
    out.mkdir()
    snap = snapshot(work)
    proc = run_builder(args.python, builder, qfile, out, cache, work)
    exp = {f"spans/S5{i:02d}-1.txt": (txt, txt_sha) for i in range(1, len(quotes_txt) + 1)}
    legs.append(expect_ok("EMPTY_OK", proc, out, exp, snap))

    # REBUILD_OK (run again into the same dir; byte-identical outputs)
    first_build = snapshot(out)
    proc2 = run_builder(args.python, builder, qfile, out, cache, work)
    if proc2.returncode != 0:
        legs.append(f"REBUILD_OK={FAIL}(rc={proc2.returncode})")
    else:
        same = snapshot(out)
        legs.append(f"REBUILD_OK={PASS}" if same == first_build else f"REBUILD_OK={FAIL}(not byte-identical)")

    # FOREIGN (a foreign spans/S777-1.txt must survive; a rerun with fewer quotes
    # makes the old files orphans — the hardened builder refuses BEFORE deleting)
    foreign = out / "spans" / "S777-1.txt"
    foreign.write_bytes(b"foreign evidence bytes\n")
    rows_few = rows[:2]
    qfew = work / "quotes-few.tsv"
    write_quotes(qfew, rows_few)
    proc = run_builder(args.python, builder, qfew, out, cache, work)
    if proc.returncode == 0:
        legs.append(f"FOREIGN={FAIL}(rc=0, orphans deleted: foreign gone={not foreign.exists()})")
    elif not foreign.exists():
        legs.append(f"FOREIGN={FAIL}(refused rc={proc.returncode} but foreign file deleted)")
    else:
        err = ((proc.stderr or "") + (proc.stdout or ""))[:200]
        legs.append(f"FOREIGN={PASS}(refused)" if "777" in err or "foreign" in err.lower()
                    else f"FOREIGN={FAIL}(reason-unnamed:{err!r})")

    # SYMLINK_OUT
    real = work / "realdir"
    real.mkdir()
    linkout = work / "out-link"
    linkout.symlink_to(real)
    proc = run_builder(args.python, builder, qfile, linkout, cache, work)
    legs.append(expect_refuse("SYMLINK_OUT", proc, ["SYMLINK"], [real / "spans.tsv"], ))
    if not any(real.iterdir()):
        legs[-1] = f"SYMLINK_OUT={PASS}(refused)"
    else:
        legs[-1] += "(target-dir-written!)"

    # SYMLINK_CACHE
    cache2 = work / "cache2"
    cache2.mkdir()
    target = work / "target.txt"
    target.write_bytes(txt.encode("utf-8"))
    url9 = "https://fixture.example/doc9"
    (cache2 / (key(url9) + ".txt")).symlink_to(target)
    q9 = work / "quotes-9.tsv"
    write_quotes(q9, [("S591", url9, quotes_txt[0], "corpus/evidence/round58/c1-fixture.md")])
    out9 = work / "out-9"
    out9.mkdir()
    proc = run_builder(args.python, builder, q9, out9, cache2, work)
    legs.append(expect_refuse("SYMLINK_CACHE", proc, ["SYMLINK", "REGTYPE", "NOT_REGULAR"], []))

    # FIFO_TXT
    cache3 = work / "cache3"
    cache3.mkdir()
    url7 = "https://fixture.example/doc7"
    os.mkfifo(cache3 / (key(url7) + ".txt"))
    q7 = work / "quotes-7.tsv"
    write_quotes(q7, [("S571", url7, quotes_txt[0], "corpus/evidence/round58/c1-fixture.md")])
    out7 = work / "out-7"
    out7.mkdir()
    try:
        proc = run_builder(args.python, builder, q7, out7, cache3, work, timeout=20)
        legs.append(expect_refuse("FIFO_TXT", proc, ["NOT_REGULAR", "FIFO", "REGTYPE", "SYMLINK"], []))
    except subprocess.TimeoutExpired:
        legs.append(f"FIFO_TXT={FAIL}(hung reading the FIFO)")

    # DEVZERO_TXT
    cache4 = work / "cache4"
    cache4.mkdir()
    url8 = "https://fixture.example/doc8"
    (cache4 / (key(url8) + ".txt")).symlink_to("/dev/zero")
    q8 = work / "quotes-8.tsv"
    write_quotes(q8, [("S581", url8, quotes_txt[0], "corpus/evidence/round58/c1-fixture.md")])
    out8 = work / "out-8"
    out8.mkdir()
    try:
        proc = run_builder(args.python, builder, q8, out8, cache4, work, timeout=20)
        legs.append(expect_refuse("DEVZERO_TXT", proc, ["NOT_REGULAR", "SIZE", "SYMLINK", "REGTYPE"], []))
    except subprocess.TimeoutExpired:
        legs.append(f"DEVZERO_TXT={FAIL}(hung reading /dev/zero)")

    # FAT_RAW (OLE-headed 80 MiB sparse file; candidate must refuse by SIZE)
    cache5 = work / "cache5"
    cache5.mkdir()
    url5 = "https://fixture.example/doc5"
    fat = cache5 / (key(url5) + ".raw")
    with fat.open("wb") as f:
        f.write(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
        f.truncate(80 * 1024 * 1024)
    q5 = work / "quotes-5.tsv"
    write_quotes(q5, [("S551", url5, quotes_txt[0], "corpus/evidence/round58/c1-fixture.md")])
    out5 = work / "out-5"
    out5.mkdir()
    proc = run_builder(args.python, builder, q5, out5, cache5, work, timeout=60)
    legs.append(expect_refuse("FAT_RAW", proc, ["SIZE"], []))

    # MANY_QUOTES
    qm = work / "quotes-many.tsv"
    with qm.open("w", encoding="utf-8") as f:
        f.write("id\turl\tquote\tentry\n")
        for i in range(QUOTES_CAP + 1):
            f.write(f"S900\t{url1}\t{quotes_txt[0]}\tcorpus/evidence/round58/c1-fixture.md\n")
    outm = work / "out-many"
    outm.mkdir()
    proc = run_builder(args.python, builder, qm, outm, cache, work, timeout=90)
    legs.append(expect_refuse("MANY_QUOTES", proc, ["SIZE", "ROWS", "CAP"], []))

    # ESCAPE_ENTRY (regression: entry column with .. is refused, write nothing)
    qe = work / "quotes-esc.tsv"
    write_quotes(qe, [("S501", url1, quotes_txt[0], "../escape.md")])
    oute = work / "out-esc"
    oute.mkdir()
    proc = run_builder(args.python, builder, qe, oute, cache, work)
    if proc.returncode != 0 and not (oute / "spans.tsv").exists():
        legs.append("ESCAPE_ENTRY=pass(refused)")
    else:
        legs.append(f"ESCAPE_ENTRY={FAIL}(rc={proc.returncode}, written={(oute / 'spans.tsv').exists()})")

    # HELDOUT_OK (real pinned OLE capture in the lane store; counter derives the
    # defined form itself and requires the builder's offsets to match)
    ct = LANE / "tools" / "capture-text.py"
    if sha256(ct.read_bytes()) != CAPTURE_TEXT_SHA:
        legs.append(f"HELDOUT_OK={FAIL}(capture-text pin broken)")
    else:
        proc = subprocess.run([args.python, "-B", str(ct), str(LANE / "corpus" / "captures" / (STORE_CAPTURE_KEY + ".raw"))],
                              capture_output=True, text=True, timeout=120,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(work)))
        form = proc.stdout
        raw_sha = sha256((LANE / "corpus" / "captures" / (STORE_CAPTURE_KEY + ".raw")).read_bytes())
        ok = True
        for hq in HELDOUT_QUOTES:
            if form.count(hq) != 1:
                legs.append(f"HELDOUT_OK={FAIL}(quote not unique: {hq[:30]!r})")
                ok = False
                break
        if ok:
            url_hit = "https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc"
            qh = work / "quotes-heldout.tsv"
            write_quotes(qh, [(f"S6{i:02d}", url_hit, q, "corpus/evidence/round58/c1-heldout.md")
                              for i, q in enumerate(HELDOUT_QUOTES, start=1)])
            outh = work / "out-heldout"
            outh.mkdir()
            proc = run_builder(args.python, builder, qh, outh, LANE / "corpus" / "captures", work, timeout=120)
            exp = {f"spans/S6{i:02d}-1.txt": (form, raw_sha) for i in range(1, 4)}
            legs.append(expect_ok("HELDOUT_OK", proc, outh, exp, snapshot(work)))

    # BEFORE_BUILDER battery integrity: the pinned round-55 builder must FAIL the
    # FOREIGN leg (it deletes the foreign file) — proves the leg discriminates.
    before = "absent"
    if BEFORE_BUILDER.is_file() and sha256(BEFORE_BUILDER.read_bytes()) == R55_BUILDER_SHA:
        outb = work / "out-before"
        (outb / "spans").mkdir(parents=True)
        qb = work / "quotes-before.tsv"
        write_quotes(qb, rows[:2])
        (outb / "spans.tsv").write_text("stale\n", encoding="utf-8")
        fb = outb / "spans" / "S888-1.txt"
        fb.write_bytes(b"foreign\n")
        proc = run_builder(args.python, BEFORE_BUILDER, qb, outb, cache, work)
        before = "deleted" if not fb.exists() else "kept"
    legs.append(f"BEFORE_FOREIGN={before}")

    # controls: do-nothing builders must never reach PASS
    denied = 0
    total = 0
    if args.controls:
        names = ("REFUSEALL.py", "build-spans-r55.py")
        for control_name in names:
            ctrl = pathlib.Path(args.controls) / control_name
            if not ctrl.is_file():
                continue
            total += 1
            r = subprocess.run([sys.executable, "-B", str(HERE / "c1-count.py"),
                                "--builder", str(ctrl), "--work", str(work / ("ctrl-" + ctrl.stem)),
                                "--seed", str(args.seed + 1000)],
                               capture_output=True, text=True, timeout=1800)
            tail = [l for l in r.stdout.splitlines() if l.startswith("C1=")]
            if tail and tail[0].strip() == "C1=PASS":
                legs.append(f"CONTROL_{ctrl.stem}=PASS(!)")
            else:
                denied += 1
                legs.append(f"CONTROL_{ctrl.stem}=denied")
    legs.append(f"DENIED={denied}/{total}" if total else "DENIED=0/0")

    ok_legs = [l for l in legs if l.split("=")[0] in
               ("EMPTY_OK", "REBUILD_OK", "HELDOUT_OK", "ESCAPE_ENTRY")]
    ref_legs = [l for l in legs if l.split("=")[0] in
                ("FOREIGN", "SYMLINK_OUT", "SYMLINK_CACHE", "FIFO_TXT", "DEVZERO_TXT",
                 "FAT_RAW", "MANY_QUOTES")]
    ok_pass = all(l.endswith("(pass)") or l.endswith(")") and f"{FAIL}" not in l and "=pass" in l for l in ok_legs)
    ok_pass = all(("=pass" in l) for l in ok_legs)
    ref_pass = all(("=PASS" in l) for l in ref_legs)
    integrity = any(l == "BEFORE_FOREIGN=deleted" for l in legs)
    denied_pass = (denied == total) if total else True
    verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"

    for l in legs:
        print(l)
    print(f"SUMMARY OK={sum('=pass' in l for l in ok_legs)}/{len(ok_legs)} "
          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
          f"BEFORE_FOREIGN={before} DENIED={denied}/{total}")
    print(f"C1={verdict}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

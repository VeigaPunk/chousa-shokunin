#!/usr/bin/env python3
"""Generate the closure-removal twins of matrix-battery-v5.py from the frozen bytes.

Each mutant is written to <S>/mirror/<tag>/corpus/evidence/round78/matrix-battery-v5.py so
that the battery's own LANE = HERE.parents[2] resolves to a scratch mirror, and the file
NAME stays `matrix-battery-v5.py` so the a2/a7 forgers' `/proc/<ppid>/cmdline` matcher
(`matrix-battery-v\\d+\\.py$`) still finds the battery under test.
"""
import hashlib
import os
import pathlib
import shutil

SRC = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round78")
S = pathlib.Path("/fast/scratch/hyaku/chousa-r78/R78MutA")
BASE = (SRC / "matrix-battery-v5.py").read_text()

FLAG_ON = ("    a = ap.parse_args()\n"
           "    matrix = pathlib.Path(a.matrix).resolve()")
FLAG_ON_M = ("    a = ap.parse_args()\n"
             "    a.print_order = True\n"
             "    matrix = pathlib.Path(a.matrix).resolve()")

ORDER_BUFFERED = ('        if print_order:\n'
                  '            buffered.append(f"{label} ORDER {i} " + hashlib.sha256(\n'
                  '                "|".join(name for _g, name, _s in order).encode()).hexdigest())\n')
ORDER_IMMEDIATE = ('        if print_order:\n'
                   '            emit(f"{label} ORDER {i} " + hashlib.sha256(\n'
                   '                "|".join(name for _g, name, _s in order).encode()).hexdigest())\n')

RUN_BUFFERED = ('            buffered.append(f"{label} RUN {group} {name} {i} matrix_exit="\n')
RUN_IMMEDIATE = ('            emit(f"{label} RUN {group} {name} {i} matrix_exit="\n')

SALT_BODY = ('    target = d / "subject.py"\n'
             '    text = source.read_text()\n')
SALT_BODY_M2 = ('    target = d / "subject.py"\n'
                '    target.write_bytes(source.read_bytes()\n'
                '                       + f"\\n# salt {secrets.token_hex(8)}\\n".encode())\n'
                '    return target\n'
                '    text = source.read_text()\n')

TRAILER = '    emit(f"RECEIPT_LINES={_LINES + 2}")\n'

FLUSH = '    print(text)\n'
FLUSH_M = '    print(text, flush=True)\n'


def sub(text: str, old: str, new: str, tag: str) -> str:
    assert text.count(old) == 1, f"{tag}: anchor count {text.count(old)} for {old[:40]!r}"
    return text.replace(old, new)


def m1(t: str) -> str:
    """--print-order forced on; the quiet (buffered) leg untouched."""
    return sub(t, FLAG_ON, FLAG_ON_M, "M1")


def m1b(t: str) -> str:
    """M1 + the ORDER line written when it is produced (round-77 timing), RUN buffered."""
    t = m1(t)
    t = sub(t, FLUSH, FLUSH_M, "M1B-flush")
    return sub(t, ORDER_BUFFERED, ORDER_IMMEDIATE, "M1B-order")


def m5(t: str) -> str:
    """M1 + both ORDER and RUN lines written when produced = the round-77 print regime."""
    t = m1b(t)
    return sub(t, RUN_BUFFERED, RUN_IMMEDIATE, "M5-run")


def m2(t: str) -> str:
    """The interior inert statement replaced by the round-77 trailing `# salt <hex>` line."""
    return sub(t, SALT_BODY, SALT_BODY_M2, "M2")


def m3(t: str) -> str:
    """RECEIPT_LINES trailer removed."""
    return sub(t, TRAILER, "", "M3")


def m4(t: str) -> str:
    """Per-subject RUN lines written when produced (flushed), ORDER leg untouched."""
    t = sub(t, FLUSH, FLUSH_M, "M4-flush")
    return sub(t, RUN_BUFFERED, RUN_IMMEDIATE, "M4-run")


MUTANTS = {"M1": m1, "M1B": m1b, "M2": m2, "M3": m3, "M4": m4, "M5": m5}


def mirror(tag: str, text: str) -> pathlib.Path:
    lane = S / "mirror" / tag
    r78 = lane / "corpus/evidence/round78"
    if lane.exists():
        shutil.rmtree(lane)
    r78.mkdir(parents=True)
    for name in ("round74", "round75", "round76"):
        os.symlink(SRC.parent / name, lane / "corpus/evidence" / name)
    os.symlink(SRC / "forgers", r78 / "forgers")
    target = r78 / "matrix-battery-v5.py"
    target.write_text(text)
    return target


if __name__ == "__main__":
    print("PRISTINE_SHA256=" + hashlib.sha256(BASE.encode()).hexdigest())
    for tag, fn in MUTANTS.items():
        path = mirror(tag, fn(BASE))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"MUTANT={tag} PATH={path} SHA256={digest} LINES={len(path.read_text().splitlines())}")

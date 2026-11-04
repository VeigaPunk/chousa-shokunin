#!/usr/bin/env python3
"""R76Review2 — structural forgeries against the frozen C2 counter and battery."""
import hashlib
import importlib.util
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
EV = LANE / "corpus/evidence/round76"
COUNTER = EV / "correction-count-v2.py"
BATTERY = EV / "c2-battery.py"
WORK = pathlib.Path("/fast/scratch/hyaku/chousa-r76/R76Review2/fixtures")
import secrets
LESSON = "corpus/lessons/round-74.md"
FROZEN = "da9ac7ec684fe9fe9ad5554cab6180057255b76b"

spec = importlib.util.spec_from_file_location("c2b", BATTERY)
c2b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2b)
HEAD, BASE_LESSON, GOOD_BLOCK = c2b.HEAD, c2b.BASE_LESSON, c2b.GOOD_BLOCK


def g(root, *a):
    p = subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(f"git {a} rc={p.returncode} {p.stderr[:300]}")
    return p.stdout.strip()


def commit(root, msg):
    assert pathlib.Path(g(root, "rev-parse", "--show-toplevel")).resolve() == root.resolve()
    g(root, "add", "--", LESSON)
    g(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
      "commit", "-qm", msg)
    return g(root, "rev-parse", "HEAD")


def fixture(name, states, base_text=None):
    root = WORK / secrets.token_hex(16)
    (root / "corpus/lessons").mkdir(parents=True)
    cur = BASE_LESSON if base_text is None else base_text
    (root / LESSON).write_text(cur)
    g(root, "init", "-q")
    base = commit(root, "base")
    rev = base
    for i, st in enumerate(states):
        cur = st(cur) if callable(st) else st
        (root / LESSON).write_text(cur)
        rev = commit(root, "case")
    return root, base, rev


def run_counter(root, base, rev):
    p = subprocess.run([sys.executable, "-B", str(COUNTER), "--lane", str(root),
                        "--base", base, "--rev", rev],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def report(tag, note, root, base, rev, block):
    rc, out, err = run_counter(root, base, rev)
    print(f"\n===== {tag} =====")
    print(f"NOTE: {note}")
    print("BLOCK:")
    print(block.strip("\n") if block else "(no block text; see mutation)")
    print(f"CMD: python3 -B {COUNTER} --lane {root} --base {base[:12]} --rev {rev[:12]}")
    print("STDOUT:")
    print(out.rstrip() or "(empty)")
    if err.strip():
        print("STDERR:", err.strip()[:400])
    print(f"RC={rc}")
    verdict = [l for l in out.splitlines() if l.startswith("C2V=")]
    survived = bool(verdict) and "C2V=PASS checks=9/9" in verdict[-1]
    failed = [l.split()[1] for l in out.splitlines()
              if l.startswith("CHECK ") and " FAIL " in l]
    print(f"RESULT: {'SURVIVOR(bogus scored PASS 9/9)' if survived else 'REJECTED'}"
          + (f" failed_checks={','.join(failed)}" if failed else ""))
    return survived, rc, out


BLOCK_VALID = ("Superseded: 18 words and 13 whitespace tokens. The quoted strings "
               "carry 16 and 11 whitespace tokens.")

# ---------- A1: HTML comment opened BELOW the heading (body hidden, V9 blind) ----------
def a1(t):
    return t + (f"\n{HEAD}\n\n<!--\n{BLOCK_VALID}\n-->\n")

# ---------- A2: correction block followed by a level-1 section (V6 sees only '## ') ----
def a2(t):
    return t + (f"\n{HEAD}\n\n{BLOCK_VALID}\n\n# Boundaries\n\n"
                "Appended h1 section: the document continues after the block.\n")

# ---------- A3: bogus magnitude 161 hidden behind markdown emphasis (V5 regex gap) -----
def a3(t):
    return t + (f"\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. "
                "Correction: 16 and 11. The quoted strings carry **161** whitespace tokens.\n")

# ---------- A3b: bogus magnitude via hyphenated unit -------------------------------
def a3b(t):
    return t + (f"\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. "
                "Correction: 16 and 11. The quoted strings carry 161 whitespace-token units.\n")

# ---------- A4: negation using a cue outside the NEGATIONS denylist ------------------
def a4(t):
    return t + (f"\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. "
                "The counts 16 and 11 are false and must be disregarded as corrected values.\n")

# ---------- A5: decoy authored bullet above the real one rebinds derive --------------
DECOY_BULLET = ("- Admit S182, decoy row. Opened 2026-11-04. Located quote: "
                "\u201cone two three four five six seven eight nine ten eleven\u201d (13 words).\n")
A5_BLOCK = (f"\n{HEAD}\n\nSuperseded: the authored bullets now record 13 words and "
            "13 whitespace tokens. The quoted strings carry 11 and 11 whitespace tokens.\n")

def a5(t):
    return t.replace("- Admit S182", DECOY_BULLET + "- Admit S182") + A5_BLOCK

# ---------- A7: delete-then-restore inside the base..rev range (V8 is a net diff) ----
A7_STATES = [BASE_LESSON.replace("removable line\n\n", ""), BASE_LESSON + GOOD_BLOCK]


def main():
    print("INSTRUMENT HASH CHECK vs frozen", FROZEN)
    for rel in ("corpus/evidence/round76/correction-count-v2.py",
                "corpus/evidence/round76/c2-battery.py"):
        live = hashlib.sha256((LANE / rel).read_bytes()).hexdigest()
        frozen = subprocess.run(["git", "-C", str(LANE), "show", f"{FROZEN}:{rel}"],
                                capture_output=True).stdout
        print(f"  {rel} live={live} frozen={hashlib.sha256(frozen).hexdigest()} "
              f"match={live == hashlib.sha256(frozen).hexdigest()}")

    survivors = []
    WORK.mkdir(parents=True, exist_ok=True)

    cases = [
        ("A1", "HTML comment opened BELOW the heading: the whole block body is "
               "commented out (renders invisible) yet V9 only inspects lines above the heading",
         [a1], None, a1(BASE_LESSON)),
        ("A2", "valid block is NOT the last section: an h1 '# Boundaries' section follows it; "
               "V6 only compares '## '-prefixed headings",
         [a2], None, a2(BASE_LESSON)),
        ("A3", "magnitude 161 stated in the block but written '**161** whitespace tokens': "
               "MAGNITUDE needs whitespace immediately after the digits, so 161 is unmeasured",
         [a3], None, a3(BASE_LESSON)),
        ("A3b", "magnitude 161 stated with a hyphenated unit ('161 whitespace-token units'): "
                "MAGNITUDE only matches 'whitespace tokens'/'tokens'/'words'",
         [a3b], None, a3b(BASE_LESSON)),
        ("A4", "negation stated with cues outside NEGATIONS ('false', 'disregarded'): "
               "V4 is a denylist of seven spellings",
         [a4], None, a4(BASE_LESSON)),
        ("A5", "decoy 'Admit S182' bullet inserted ABOVE the authored one: bullet_line takes the "
               "first prefix match, so derive rebinds to the decoy and the block states the decoy's counts",
         [a5], None, A5_BLOCK),
        ("A6", "block present already at base; the only change at rev is one blank line, "
               "so V7 ancestry + V8 zero-removals hold with no correction append at all",
         [lambda t: t + "\n"], BASE_LESSON + GOOD_BLOCK,
         "base = BASE_LESSON + GOOD_BLOCK; case = base + one blank line"),
        ("A7", "deletion-history: commit1 deletes 'removable line', commit2 restores it and "
               "appends the block; base..rev numstat is a NET diff and shows 0 removals",
         A7_STATES, None,
         "base=BASE_LESSON; case1=BASE_LESSON minus 'removable line'; case2=BASE_LESSON+GOOD_BLOCK"),
        ("A8", "block placed inside a fenced code sample: the '## ' line is literal text, not a "
               "heading, but last_section_heading() matches any line starting '## '",
         [lambda t: (t + f"\n# Appendix\n\n```markdown\n{HEAD}\n\n{BLOCK_VALID}\n```\n")], None,
         f"```markdown\n{HEAD}\n\n{BLOCK_VALID}\n```"),
    ]

    secrets.SystemRandom().shuffle(cases)
    for tag, note, muts, base_override, block in cases:
        root, base, rev = fixture(tag, muts, base_override)
        ok, rc, out = report(tag, note, root, base, rev, block)
        if ok:
            survivors.append(tag)

    print("\nSURVIVORS=" + ",".join(survivors))
    print(f"SURVIVOR_COUNT={len(survivors)}/{len(cases)}")
    if len(survivors) != len(cases):
        raise SystemExit("fail-closed: at least one claimed survivor was rejected")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""R61-C1 controls — shows the frozen counter `../c1-count.py` discriminates.

Builds, under --work, the do-nothing stubs, the base builder (git base revision file passed as
--base), the reference builder `ref-build-spans.py`, a naive-guard builder and mutants of the
reference, runs the counter on each at one seed, and prints one row per control:
`NAME legs=k/20 failing=<leg ids>`. Expectations (exit 1 when any is not met):
  stubs/base/naive/forge: not 20/20; reference: 20/20; every mutant: fails the leg(s) listed.
`--seed N` default 61001. Usage: python3 run-c1-controls.py --base PATH --work DIR [--seed N]
"""
import argparse, pathlib, subprocess, sys, re, shutil

HERE = pathlib.Path(__file__).resolve().parent
COUNTER = HERE.parent / "c1-count.py"
REF = HERE / "ref-build-spans.py"

MUT = [  # name, [(anchor, replacement)], expected failing legs (all must fail)
    ("M01-pyc", [("old, sys.dont_write_bytecode = sys.dont_write_bytecode, True", "old = sys.dont_write_bytecode")], ["P03"]),
    ("M02-capsize", [("if size > MAX_CAPTURE:", "if False:")], ["H14", "H15"]),
    ("M03-inside", [("if os.path.commonpath([real, self.root]) != self.root:", "if False:")], ["H13"]),
    ("M04-spanslink", [("if os.path.lexists(sd) and (sd.is_symlink() or not sd.is_dir()):", "if False:")], ["H10"]),
    ("M05-filelink", [("            if p.is_symlink():\n                return _refuse", "            if False:\n                return _refuse"),
                      ('_atomic_write(out / name, body.encode("utf-8"))', '(out / name).write_bytes(body.encode("utf-8"))')], ["H11"]),
    ("M06-tsvlink", [("if os.path.lexists(m) and (m.is_symlink() or not m.is_file()):", "if False:"),
                     ('_atomic_write(out / "spans.tsv", manifest)', '(out / "spans.tsv").write_bytes(manifest)')], ["H12"]),
    ("M07-differs", [("differs = m.is_file() and m.read_bytes() != manifest", "differs = False")], ["H07"]),
    ("M08-orphans", [("                orphans.append(p)", "                pass")], ["H09"]),
    ("M09-noguard", [("if (differs or orphans) and not replace:", "if False:")], ["H07", "H09"]),
    ("M10-replace-ignored", [("if (differs or orphans) and not replace:", "if (differs or orphans):")], ["H08"]),
    ("M11-no-unlink", [("            p.unlink()\n    except OSError", "            pass\n    except OSError")], ["H08"]),
    ("M12-outfile", [("if os.path.lexists(out) and not out.is_dir():", "if False:"),
                     ('    except OSError as e:\n        print(f"build-spans: write failed', '    except KeyError as e:\n        print(f"build-spans: write failed')], ["H16"]),
    ("M13-unreadable", [('        except OSError as e:\n            return None, "", f"unreadable capture', '        except KeyError as e:\n            return None, "", f"unreadable capture')], ["H17"]),
    ("M14-bigform", [("if len(form) > MAX_FORM:", "if False:")], ["H20"]),
]


def run(builder, work, seed):
    w = work / "run"
    if w.exists():
        shutil.rmtree(w)
    p = subprocess.run([sys.executable, str(COUNTER), "--builder", str(builder), "--work", str(w), "--seed", str(seed)],
                       capture_output=True, text=True)
    legs = re.findall(r"^LEG (\w+) (\w+) (pass|fail)", p.stdout, re.M)
    failing = [a for a, b, c in legs if c == "fail"]
    return p.returncode, len(legs) - len(failing), failing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=61001)
    a = ap.parse_args()
    work = pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    base_txt = pathlib.Path(a.base).read_text()
    ref_txt = REF.read_text()
    ctl = {}
    (work / "noop0.py").write_text("import sys\nsys.exit(0)\n")
    (work / "always2.py").write_text("import sys\nsys.exit(2)\n")
    # forge: the base builder that also prints the target token before exiting
    forge = base_txt.replace("    sys.exit(main())", "    print('LEGS=20/20 C1=PASS')\n    sys.exit(main())")
    assert forge != base_txt
    (work / "forge.py").write_text(forge)
    naive = base_txt.replace("    rows = read_quotes(pathlib.Path(a.quotes))",
                             "    if out.exists() and any(out.iterdir()):\n        return 2\n    rows = read_quotes(pathlib.Path(a.quotes))")
    assert naive != base_txt
    (work / "naive.py").write_text(naive)
    rows = [("base", pathlib.Path(a.base), None), ("noop0", work / "noop0.py", None), ("always2", work / "always2.py", None),
            ("forge-token", work / "forge.py", None), ("naive-guard", work / "naive.py", None), ("reference", REF, [])]
    bad = 0
    for name, path, _ in rows:
        rc, n, failing = run(path, work, a.seed)
        want_pass = name == "reference"
        ok = (rc == 0 and n == 20) if want_pass else (n < 20 and rc == 1)
        bad += not ok
        print(f"{name:22s} rc={rc} legs={n}/20 failing={','.join(failing) or '-'} {'OK' if ok else 'UNEXPECTED'}")
    for name, edits, expect in MUT:
        t = ref_txt
        for anchor, rep in edits:
            assert t.count(anchor) == 1, (name, anchor, t.count(anchor))
            t = t.replace(anchor, rep)
        f = work / f"{name}.py"
        f.write_text(t)
        rc, n, failing = run(f, work, a.seed)
        killed = all(any(x.startswith(e) for x in failing) for e in expect) and rc == 1
        bad += not killed
        print(f"{name:22s} rc={rc} legs={n}/20 failing={','.join(failing) or '-'} expect={','.join(expect)} {'KILLED' if killed else 'SURVIVED'}")
    print(f"CONTROLS_UNEXPECTED={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

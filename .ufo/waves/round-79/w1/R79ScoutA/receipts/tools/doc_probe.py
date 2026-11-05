"""Does the re-emission preserve __doc__ (the battery's own argparse idiom is
`description=__doc__.splitlines()[0]`)?  And does a star-import of a re-emitted
module still resolve the names listed in its __all__?"""
import importlib.util, pathlib, shutil, subprocess, sys, tempfile

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

for name in ("h25_all_starimport.py", "h27_argparse_docstring.py"):
    src = pathlib.Path(sys.argv[2]) / name
    copy = bat.reemit(src, work)
    for label, target in (("original", src), ("copy", copy)):
        if label == "original":
            r = subprocess.run([sys.executable, "-B", str(target)], capture_output=True, text=True)
            print(f"{name} {label}: rc={r.returncode} out={r.stdout.strip()!r} "
                  f"err={(r.stderr.strip().splitlines() or [''])[-1]!r}")
        else:
            # star-import semantics: exec the copy's module and try to fetch __all__ names
            code = (
                "import importlib.util,sys;"
                "spec=importlib.util.spec_from_file_location('m', sys.argv[1]);"
                "m=importlib.util.module_from_spec(spec);"
                "spec.loader.exec_module(m);"
                "names=getattr(m,'__all__',None);"
                "print('DOC_IS_NONE', m.__doc__ is None);"
                "print('ALL', names);"
                "print('RESOLVE', [hasattr(m,n) for n in (names or [])])"
            )
            r = subprocess.run([sys.executable, "-B", "-c", code, str(target)],
                               capture_output=True, text=True)
            print(f"{name} {label}: {r.stdout.strip()!r} "
                  f"err={(r.stderr.strip().splitlines() or [''])[-1]!r}")
    shutil.rmtree(copy.parent, ignore_errors=True)

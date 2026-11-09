# Formal equivalence check for e1/e2 beyond "they're comments/docstrings":
# e1: appends "# equivalent mutant\n" after the __main__ block. The tail is "\nif __name__ == \"__main__\":\n    sys.exit(...)". Appending a comment line after: Python parses fine, no behavior change. Survives selftest (verified). Does it change verify CLI? No (comment). Truly equivalent.
# e2: docstring "sha256..." -> "SHA-256..." (digest's docstring, line 360). Docstrings are not computed. Equivalent.
# e3: verified exhaustively above. Equivalent.
# All three survive the F selftest (observed SURVIVED ok, rc=0). K2 not triggered.
# One gap: the battery's killed() for equivalents uses POSITIVE last line PASS_LINE (67/67). The base tool's equivalents print 48/48 and are scored KILLED FAIL in before receipt — correct, they fail POSITIVE eq check. Fine.
# Also check: could a 4th equivalent (e.g., whitespace change, reordering imports no-op) be killed? That would be K2 territory. Try a couple:
import subprocess, sys, shutil
src = open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py").read()
tests = {
    "ws-indent-comment": (src + "\n# extra trailing newline comment\n", "append comment at EOF"),
}
# import reorder no-op: swap two adjacent imports? `import argparse` ... `import contextlib` order change has no effect.
old_imports = "import argparse\nimport contextlib\nimport fnmatch\n"
if src.count(old_imports)==1:
    swapped = "import contextlib\nimport argparse\nimport fnmatch\n"
    open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/mut-importswap.py","w").write(src.replace(old_imports, swapped))
    p = subprocess.run([sys.executable,"-B","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/mut-importswap.py","--selftest"],capture_output=True,text=True)
    print("import-swap rc", p.returncode, p.stdout.splitlines()[-1] if p.stdout else "", "equiv_survives", p.returncode==0)
# blank line insertion in digest function
old_digest = "        digest(at_rev) != r[\"digest\"]"
print("digest line count", src.count(old_digest))

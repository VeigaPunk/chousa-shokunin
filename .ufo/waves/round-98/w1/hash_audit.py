# Q5: is the battery's hash-of-self oracle a faithful stand-in for R97 routed limit (g)?
# R97 limit (g) per battery docstring: "a self-test that detects mutants by hashing its own source passes every mutant-kill leg."
# The R98 battery's hash_of_self: inserts a sha256 check of its own file bytes (minus the _H line) at the TOP of selftest(),
# failing with FAIL cases=0/67 failed=setup on mismatch.
# Faithfulness checks:
# (a) Does the oracle mutant actually PASS the real selftest's POSITIVE check by itself? It should fail on any byte change, INCLUDING the mutant itself's bytes (since inserting the check changes the hash). Wait — how is the hash computed? body = src with HASH_CHECK inserted (containing {h} placeholder replaced by hash of stripped). The stripped version excludes only the "_H = " line. So the oracle's own bytes hash equals _H always (computed over its own final bytes). So the oracle PASSES its own check when unmutated. When a mutant is applied, bytes change -> hash differs from the baked _H -> oracle prints FAIL setup. So YES, like limit (g) description.
# (b) Does the battery reject it? Observed: oracle-hash-of-self battery_rc=1, EQUIVALENT_SURVIVED=0/3 (it kills the equivalents because any byte change triggers FAIL). Rejection leg = battery exit 1 AND "SELFTEST_CONTROLS_R98=FAIL". It got that.
# (c) BUT: hash-of-self as constructed checks __file__ bytes. When the battery runs the mutant self-test, it writes the mutant to work/oracle-hash-of-self.py and runs THAT. The check hashes __file__ = the mutant path. The baked hash was computed over the FULL FILE including everything. Any mutant that changes ANY byte (including in a comment, or in an unused function) triggers FAIL. That's exactly limit (g)'s "detects mutants by hashing its own source".
# (d) SUBTLE: the stripped computation excludes lines starting with "    _H = ". If a mutant changes ONLY the _H line itself... a mutant that replaced _H's value with a matching hash would pass. But no such mutant exists in the scored sets. The EQUIVALENT mutants (e1 trailing comment, e2 docstring) DO change bytes -> hash mismatch -> oracle kills them -> EQUIVALENT leg fails -> battery rejects. Faithful.
# (e) One more check: does the oracle's failure mode satisfy the battery's KILLED rule? It prints FAIL cases=0/67 failed=setup, rc=1, no traceback, setup in CASE_IDS set -> KILLED for every mutant. So it passes kill legs. The ONLY rejection comes from EQUIVALENT leg (0/3) + ... also POSITIVE? The oracle unmutated passes selftest POSITIVE (hash matches itself). Battery's sub-run tally: POSITIVE=1/1 KILL_REQUIRED=35/35 ... EQUIVALENT_SURVIVED=0/3 -> FAIL. Correct rejection path.
# Verify (e) by running the oracle directly.
import importlib.util, hashlib, subprocess, sys, os
spec_src = open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/corpus/evidence/round98/selftest-controls-r98.py").read()
# exec just the hash funcs
ns = {}
exec("import hashlib\nHASH_ANCHOR = \"    try:\\n        guard_ok, guard_detail = _guard_canary()\\n\"\nHASH_CHECK = ('    import hashlib as _h\\n' '    _s = \"\".join(ln for ln in open(__file__, encoding=\"utf-8\").readlines() if not ln.startswith(\"    _H = \"))\\n' '    _H = \"{h}\"\\n' '    if _h.sha256(_s.encode(\"utf-8\")).hexdigest() != _H:\\n' '        print(\"SEARCH_RERUN_SELFTEST: FAIL cases=0/{n} failed=setup\")\\n' '        return 1\\n')\nN_CASES = 67\ndef hash_of_self(src):\n    if src.count(HASH_ANCHOR) != 1:\n        return None\n    body = src.replace(HASH_ANCHOR, HASH_CHECK.replace(\"{n}\", str(N_CASES)) + HASH_ANCHOR)\n    stripped = \"\".join(ln for ln in body.splitlines(keepends=True) if not ln.startswith(\"    _H = \"))\n    return body.replace(\"{h}\", hashlib.sha256(stripped.encode(\"utf-8\")).hexdigest())\n", ns)
src = open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py").read()
hos = ns["hash_of_self"](src)
open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/oracle-hash.py","w").write(hos)
p = subprocess.run([sys.executable,"-B","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/oracle-hash.py","--selftest"],capture_output=True,text=True)
print("oracle rc", p.returncode, "last", p.stdout.splitlines()[-1] if p.stdout else "")
# apply e1 equivalent to oracle
e1_old = "\nif __name__ == \"__main__\":\n    sys.exit(main(sys.argv[1:]))\n"; e1_new = e1_old + "# equivalent mutant\n"
open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/oracle-hash-e1.py","w").write(hos.replace(e1_old, e1_new))
p2 = subprocess.run([sys.executable,"-B","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/oracle-hash-e1.py","--selftest"],capture_output=True,text=True)
print("oracle+e1 rc", p2.returncode, "last", p2.stdout.splitlines()[-1][:80] if p2.stdout else "")
# apply e2 (docstring)
e2_old = "    \"\"\"sha256 of the paths as bytes, byte-sorted,"; e2_new = "    \"\"\"SHA-256 of the paths as bytes, byte-sorted,"
open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/oracle-hash-e2.py","w").write(hos.replace(e2_old, e2_new))
p3 = subprocess.run([sys.executable,"-B","/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/oracle-hash-e2.py","--selftest"],capture_output=True,text=True)
print("oracle+e2 rc", p3.returncode, "last", p3.stdout.splitlines()[-1][:80] if p3.stdout else "")

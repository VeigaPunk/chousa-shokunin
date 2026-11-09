import importlib.util, sys, os, textwrap
src = open("/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py").read()
def run_mut(name, old, new):
    n = src.count(old)
    print(f"=== {name}: applies {n} times")
    if n != 1: return
    mp = f"/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/attack/mut-{name}.py"
    open(mp,"w").write(src.replace(old,new))
    import subprocess
    p = subprocess.run([sys.executable,"-B",mp,"--selftest"], capture_output=True, text=True)
    last = p.stdout.splitlines()[-1] if p.stdout.splitlines() else ""
    print(f" rc={p.returncode} last={last!r} traceback={'Traceback' in p.stderr}")
    # also print g00 line
    for ln in p.stdout.splitlines():
        if "g00" in ln: print(" ", ln)
# Canary holes: mutations that _collect/_summary get wrong but canary's fixed sets don't catch?
# 1. _collect: only counts setup raise as setup when it happens AFTER 3 cases? canary's failing set raises after 3 cases -> caught. What about raising on the FIRST case binding?
# 2. _summary: miscounts when n != 4 and n != 1 (e.g., counts k==n+1)? canary only checks n=4 fail, n=1 pass. A mutant that returns PASS when k == n OR n>5 would pass canary but fail real 67-case run? But real run passed. Need mutant that passes canary AND real run? Impossible if real run is correct. Wait: attack is canary passing while _collect/_summary broken in a way real run exposes. Real run exposes breaking by FAILing the real selftest... but canary passes -> g00 ok, then _collect runs real cases brokenly -> summary maybe still PASS? If _summary is broken to always PASS, canary fails (fail_set expects FAIL). So summary-always-pass is caught. What about _summary that miscounts duplicate ids? Real cases have no dup ids except canary? Hmm.
# Try: _collect mutation that drops the LAST case result (results[:-1] return). Canary fail set has 4 results; dropping last (setup) would make _summary count 3/3? Let's see exact behavior.
run_mut("drop-last", "    return results\n\n\ndef _summary", "    return results[:-1]\n\n\ndef _summary")
# Try: _collect that appends ("setup", True) instead of False -> canary expect FAIL cases=1/4 failed=..., but mutant would give cases=2/4? caught?
run_mut("setup-true", '        results.append(("setup", False))', '        results.append(("setup", True))')
# Try: _summary that treats "setup" id specially (excludes from bad) -> canary expects setup in failed list, would fail -> caught
run_mut("summary-exclude-setup", "    bad = [cid for cid, ok in results if not ok]", "    bad = [cid for cid, ok in results if not ok and cid != 'setup']")
# Try: _summary that swaps k and n in print but keeps verdict? canary checks exact lines, would be caught
# Try: exception guard catches only ValueError in cases? canary-raise is ValueError -> would pass canary but RuntimeError in real case escapes to outer guard... but real cases raising RuntimeError? Check: are any real cases raising non-ValueError? r30 raises Setup caught inside. Hmm x mutants raise RuntimeError in setup, not inside a case. canary set-up raise is RuntimeError caught by outer guard. So narrowing inner except to ValueError: canary-raise (ValueError) still caught -> canary passes. Real case raising RuntimeError inside a case would escape inner guard, hit outer guard, become setup FAIL (not case FAIL) -> still FAIL, still non-zero. So selftest still fails real breakage, just mislabels? But kill rule needs named case or setup in failed=... setup counts, so still killed. Interesting: canary passes, real behavior differs (setup vs case id) but verdict same. Not a hole for kill rule but for diagnosis.
run_mut("inner-valueerror-only", "        except Exception as exc:  # a crash inside a case is that case's failure", "        except ValueError as exc:  # a crash inside a case is that case's failure")
# Try: _collect swallows exception and returns ok=True for raising case but canary-raise expects FAIL -> caught. What about _collect that returns bool(ok) but ok is tuple detail? already covered.
# Try: canary itself mutated: _guard_canary returns (True, ...) always -> canary passes trivially. Is that reachable? That IS the guard-blind oracle. Battery rejects it because real mutants g01..g05 then survive? Check: guard-blind mutant still runs real cases; g01 (case always true) would then be masked? Real cases still PASS -> g01 survives -> KILL_REQUIRED drops. So battery catches it, but the claim says canary checks _collect/_summary. A mutant that makes _guard_canary lie is itself a canary bypass. Does canary check itself? No. The battery's guard-blind oracle covers it.
run_mut("canary-returns-true", "    return all(seen), f\"fail_set={'ok' if seen[0] else 'WRONG'} pass_set={'ok' if seen[1] else 'WRONG'}\"", "    return True, 'fail_set=ok pass_set=ok'")

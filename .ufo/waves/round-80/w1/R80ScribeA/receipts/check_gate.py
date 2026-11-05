import re, subprocess, sys
ROOT = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
REC = re.compile(r'^GATE-RECORD (S\d{3}) rev=([0-9a-f]{40}) path=(\S+) line=(\d+) words=(\d+) quote=(.*)$')
def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True)
fails = 0
for raw in open(sys.argv[1], encoding="utf-8"):
    ln = raw.rstrip("\n")
    if not ln:
        continue
    m = REC.match(ln)
    if not m:
        print("FORMAT-FAIL", ln[:100]); fails += 1; continue
    sid, rev, path, n, w, quote = m.groups()
    n = int(n); w = int(w)
    r1 = git("cat-file", "-e", rev + "^{commit}").returncode == 0
    blob = git("show", f"{rev}:{path}")
    r2 = blob.returncode == 0
    text = blob.stdout.decode("utf-8").split("\n") if r2 else []
    r3 = r2 and 1 <= n <= len(text) and quote in text[n - 1]
    wc = len(quote.split())
    r4 = (wc == w) and wc <= 25
    ok = r1 and r2 and r3 and r4
    fails += (not ok)
    print(f"{sid} R1={'ok' if r1 else 'FAIL'} R2={'ok' if r2 else 'FAIL'} R3={'ok' if r3 else 'FAIL'} "
          f"R4={'ok' if r4 else 'FAIL'} words_recorded={w} words_measured={wc} "
          f"line_n={n} line_len_chars={len(text[n-1]) if r3 else 'NA'} {'PASS' if ok else 'FAIL'}")
print("GATE_RECORDS_CHECK=" + ("PASS" if fails == 0 else "FAIL") + f" failures={fails}")
sys.exit(1 if fails else 0)

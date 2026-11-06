import re, sys, subprocess, pathlib
root = pathlib.Path(sys.argv[1]); LANE = sys.argv[2]
PATTERNS = [
 ("aws_access_key_id",  re.compile(r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b')),
 ("github_token",       re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}')),
 ("slack_token",        re.compile(r'\bxox[abposr]-[A-Za-z0-9-]{10,}')),
 ("google_api_key",     re.compile(r'\bAIza[0-9A-Za-z_\-]{35}\b')),
 ("openai_sk",          re.compile(r'\bsk-[A-Za-z0-9]{20,}')),
 ("jwt",                re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.')),
 ("private_key_block",  re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
 ("authorization_hdr",  re.compile(r'(?i)\bauthorization\s*:\s*\S+')),
 ("bearer",             re.compile(r'(?i)\bbearer\s+[A-Za-z0-9._\-]{12,}')),
 ("cookie_hdr",         re.compile(r'(?i)\b(?:set-)?cookie\s*:\s*\S+')),
 ("url_userinfo",       re.compile(r'[a-zA-Z][a-zA-Z0-9+.-]*://[^/\s:@]+:[^/\s@]+@')),
 ("password_assign",    re.compile(r'(?i)\b(?:password|passwd|pwd)\s*[:=]\s*\S+')),
 ("apikey_assign",      re.compile(r'(?i)\b(?:api[_-]?key|apikey|access[_-]?token|auth[_-]?token|secret[_-]?key|client[_-]?secret)\s*[:=]\s*\S+')),
 ("email",              re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b')),
]
CRED = {p for p,_ in PATTERNS if p != "email"}
def scan(text):
    lines = text.splitlines(); out = {}
    for cls, pat in PATTERNS:
        hits = [i+1 for i in range(len(lines)) if pat.search(lines[i])]
        if hits: out[cls] = hits
    return out
def report(label, text):
    r = scan(text)
    if not r:
        print(f"  {label}: NO MATCH (0/14 classes)"); return 0
    for cls, hits in r.items():
        print(f"  {label}: {cls} count={len(hits)} lines={hits[:10]}")
    return sum(len(v) for k,v in r.items() if k in CRED)

creds = 0
print("### A. committed diff 378fda82..7e2da96 — added lines only")
diff = subprocess.run(["git","-C",LANE,"diff","378fda82dc2cbcc555a0565052cc408121813cef",
                       "7e2da96a0541946e796384d42fea18e09ede9e9f"], capture_output=True, text=True).stdout
added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
print(f"  added_lines={len(added.splitlines())}")
creds += report("diff", added)

KEYS = ["f2489455cc311a4de981e926","c52a1f15884a78028febcf43","371c55117727d526805f030d",
        "f221c90f69188f775e32cd34","43a45b49723f7677d6446c92"]
print("\n### B. five new 2026-11-06 captures, .txt form (the counter's grounding surface)")
for k in KEYS:
    p = root/'corpus/captures'/f"{k}.txt"
    creds += report(f"{k}.txt", p.read_text(errors='replace'))

print("\n### C. five new 2026-11-06 captures, .raw form (binary decoded latin-1)")
for k in KEYS:
    p = root/'corpus/captures'/f"{k}.raw"
    creds += report(f"{k}.raw", p.read_bytes().decode('latin-1', errors='replace'))

print(f"\nCREDENTIAL_SHAPED_HITS_TOTAL={creds}")
print("VERDICT_CLASS=" + ("FOUND" if creds else "NONE"))

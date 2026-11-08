import re, os, sys
# Replicate exactly the functions from gate-records-r89.py lines 624-681 for independent probing
ROWS_203=3
def probe_re(ROWSPIN=3):
    def rederive(name, detail, tool_present=True):
        d = detail.strip()
        m = re.fullmatch(r"(\d+)/(\d+)/(\d+) pin(\d+)", d)
        if m:
            a,b,c,pin=(int(g) for g in m.groups())
            return a==b==c==pin, (a,b,c,pin)
        m = re.fullmatch(r"derived=(\d+) killed=(\d+)", d)
        if m:
            dv,kv=int(m.group(1)),int(m.group(2))
            return dv==1 and kv==1, (dv,kv)
        m = re.fullmatch(r"tool present", d)
        if m:
            return tool_present, ()
        m = re.match(r"(\d+)/(\d+)", d)
        if m:
            a,b=int(m.group(1)),int(m.group(2))
            return a==b, (a,b)
        return None, None
    return rederive

rederive=probe_re()
cases=[
  ("3/3/3 pin3", True),        # width pass
  ("3/3/1 pin3", False),       # E7c
  ("3/3/3 pin9", False),       # wrong pin (also pin!=ROWS_203)
  ("3/3/3 pin9x", None),      # unparseable -> falls to n/m? tests fallback
  ("3/3", True),               # n/m pass
  ("2/3", False),              # n/m fail
  ("3/3 and more", True),      # prefix match! n/m via re.match not fullmatch
  ("derived=1 killed=1", True),
  ("derived=0 killed=0", False),
  ("derived=1 killed=0", False),
  ("derived=0 killed=1", False),
  ("tool present", True),      # depends on tool_present
  ("garbage", None),
  ("1/1", True),
  ("0/1", False),
  ("1/1 evil", True),          # n/m prefix
]
for detail, exp in cases:
    ok,nums=rederive("X", detail)
    print(f"rederive({detail!r}) -> ok={ok} nums={nums} exp={exp} {'MATCH' if ok==exp else 'DIFF'}")

# TOOL with absent
print("tool present + absent tool ->", rederive("TOOL","tool present", tool_present=False))
# Does any detail return None (unreconciled path)? DERIVE_NEG detail "1/1" -> n/m branch, ok
print("DERIVE_NEG 1/1 ->", rederive("DERIVE_NEG","1/1"))
print("DERIVE_NEG 0/1 ->", rederive("DERIVE_NEG","0/1"))
# SUMMARY detail "15/15" -> n/m
print("SUMMARY 15/15 ->", rederive("SUMMARY","15/15"))
print("SUMMARY 14/14 ->", rederive("SUMMARY","14/14"))  # rederived True but receipt False -> UNRECONCILED
# FRESH detail with error suffix?
print("FRESH '5/5' ->", rederive("FRESH","5/5"))
print("FRESH '5/5 FRESH_BUILD=FAILED' ->", rederive("FRESH","5/5 FRESH_BUILD=FAILED"))  # re.match prefix!
print("FRESH '0/5 FRESH_BUILD=FAILED' ->", rederive("FRESH","0/5 FRESH_BUILD=FAILED"))

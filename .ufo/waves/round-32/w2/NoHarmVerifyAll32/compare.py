#!/usr/bin/env python3
import os, re, sys, json, hashlib

S = "/fast/scratch/hyaku/chousa-r32/w2/NoHarmVerifyAll32"
FX = os.path.join(S, "out", "fx")
MASK = re.compile(rb'"gate_sha256":"[0-9a-f]{64}"')

def mask(b):
    return MASK.sub(b'"gate_sha256":"<GATE>"', b)

def read(p):
    try:
        with open(p, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

def manifest_state(mf):
    if not os.path.exists(mf):
        return None
    if os.path.isdir(mf):
        return b"<DIR>"
    os.chmod(mf, 0o600)
    return read(mf)

def shape(obj):
    # recursively collect key structure and value types / tally keys
    if isinstance(obj, dict):
        return {k: shape(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [shape(x) for x in obj]
    return type(obj).__name__

rows = []
for rec in "ABCDE":
    states = ["absent","empty","term","unterm","nul","cr"]
    if rec == "A":
        states += ["wore","dir"]
    for st in states:
        d = lambda g: os.path.join(FX, f"{g}-{rec}-{st}")
        b, l = d("base"), d("landed")
        bm = manifest_state(os.path.join(b, "manifest.jsonl"))
        lm = manifest_state(os.path.join(l, "manifest.jsonl"))
        sorig_b = read(os.path.join(b, "stdout")) or b""
        sorig_l = read(os.path.join(l, "stdout")) or b""
        eorig_b = read(os.path.join(b, "stderr")) or b""
        eorig_l = read(os.path.join(l, "stderr")) or b""
        # rc recorded in matrix.tsv
        rc = {}
        for line in open(os.path.join(S, "out", "matrix.tsv"), "rb").read().decode().splitlines():
            f = line.split("\t")
            if len(f) >= 7 and f[0] in ("base","landed") and f[1] == rec and f[2] == st:
                rc[f[0]] = int(f[5])
        rows.append(dict(rec=rec, state=st, rc_b=rc.get("base"), rc_l=rc.get("landed"),
                         stdout_eq=sorig_b == sorig_l, stderr_eq=eorig_b == eorig_l,
                         man_eq=(mask(bm) == mask(lm) if bm is not None and lm is not None else (bm is None and lm is None)),
                         bm=bm, lm=lm, sb=sorig_b, sl=sorig_l, eb=eorig_b, el=eorig_l))

print("rec state    rc_b rc_l  stdout stderr manifest_masked")
bad = []
for r in rows:
    ok = (r["rc_b"] == r["rc_l"] and r["stdout_eq"] and r["stderr_eq"] and r["man_eq"])
    print(f'{r["rec"]}   {r["state"]:<8} {r["rc_b"]}    {r["rc_l"]}    '
          f'{"eq" if r["stdout_eq"] else "DIFF":<6} {"eq" if r["stderr_eq"] else "DIFF":<6} '
          f'{"eq" if r["man_eq"] else "DIFF"}')
    if not ok:
        bad.append(r)

print(f"\nCASES={len(rows)} DIVERGENT={len(bad)}")
for r in bad:
    print(f'\n=== {r["rec"]}/{r["state"]} rc {r["rc_b"]} vs {r["rc_l"]}')
    if r["sb"] != r["sl"]:
        import difflib
        a = r["sb"].decode(errors="replace").splitlines()
        b = r["sl"].decode(errors="replace").splitlines()
        print("\n".join(difflib.unified_diff(a, b, "base", "landed", lineterm="")))
    for who, e1, e2 in (("stderr", r["eb"], r["el"]),):
        if e1 != e2:
            print(f"{who} base={e1!r}\n{who} land={e2!r}")
    if not r["man_eq"]:
        if r["bm"] is not None and r["lm"] is not None:
            a = mask(r["bm"]).decode(errors="replace").splitlines()
            b = mask(r["lm"]).decode(errors="replace").splitlines()
            import difflib
            print("\n".join(difflib.unified_diff(a, b, "base-man", "landed-man", lineterm="")))
        else:
            print("manifest presence base=", r["bm"] is not None, "landed=", r["lm"] is not None)

# schema of appended line, per record (terminated state)
print("\nSCHEMA (appended object keys, terminated state):")
for rec in "ABCDE":
    objs = {}
    for g in ("base", "landed"):
        mf = os.path.join(FX, f"{g}-{rec}-term", "manifest.jsonl")
        raw = manifest_state(mf)
        lines = [ln for ln in raw.split(b"\n") if ln.strip()]
        obj = json.loads(lines[-1])
        objs[g] = shape(obj)
    print(f'{rec}: schema_shapes_equal={objs["base"] == objs["landed"]}')
    if objs["base"] != objs["landed"]:
        print(" base:", json.dumps(objs["base"], sort_keys=True)[:1500])
        print(" land:", json.dumps(objs["landed"], sort_keys=True)[:1500])

import re
# crosscheck replicas
def make(tool_present=True, summ=None, ROWS_203=3):
    summ=summ or {}
    def _ints(key):
        v=summ.get(key)
        if v is None: return None
        out=[]
        for part in v.split("/"):
            try: out.append(int(part))
            except ValueError: return None
        return out
    def crosscheck(name, nums):
        if name=="TOOL":
            want="present" if tool_present else "absent"
            return summ.get("TOOL")==want, f"TOOL={summ.get('TOOL','-')} want={want}"
        if name in ("D1_WIDTH","D2_WIDTH"):
            a,b,c,pin=nums
            key="D1_FORGES" if name=="D1_WIDTH" else "D2_FORGES"
            ok=(_ints(key)==[a] and _ints("D1_EXPECTED")==[b] and _ints("DIV3")==[c] and pin==ROWS_203)
            return ok, f"{key}={summ.get(key,'-')} D1_EXPECTED={summ.get('D1_EXPECTED','-')} DIV3={summ.get('DIV3','-')} pin={pin}/{ROWS_203}"
        if name in ("MUT_ADMIT","MUT_UNREACH"):
            dv,kv=nums
            ok=(_ints(name+"_DERIVED")==[dv] and _ints(name+"_KILLED")==[kv])
            return ok, f"{name}_DERIVED={summ.get(name+'_DERIVED','-')} {name}_KILLED={summ.get(name+'_KILLED','-')}"
        if name=="DERIVE_NEG":
            return (nums[0]==nums[1] and _ints("DERIVE_NEG")==[nums[0]], f"DERIVE_NEG={summ.get('DERIVE_NEG','-')}")
        key={"POSITIVE":"POSITIVE","FRESH":"FRESH_POSITIVE","FORGED":"FORGED_REFUSED","CODES":"EXPECTED_CODE","EMPTY":"EMPTY_REFUSED","RC":"RC","SETUP":"SETUP","D1_REFUSED":"D1_REFUSED","D2_REFUSED":"D2_REFUSED"}[name]
        return _ints(key)==[nums[0],nums[1]], f"{key}={summ.get(key,'-')}"
    return crosscheck

# Good summary
good={"TOOL":"present","POSITIVE":"15/15","FRESH_POSITIVE":"5/5","FORGED_REFUSED":"362/362","EXPECTED_CODE":"362/362","EMPTY_REFUSED":"1/1","RC":"4/4","SETUP":"1/1","D1_EXPECTED":"3","D1_FORGES":"3","DIV3":"3","D1_REFUSED":"3/3","D2_FORGES":"3","D2_REFUSED":"3/3","MUT_ADMIT_DERIVED":"1","MUT_ADMIT_KILLED":"1","MUT_UNREACH_DERIVED":"1","MUT_UNREACH_KILLED":"1","DERIVE_NEG":"1"}
cc=make(summ=good)
tests=[
 ("TOOL",(),True),
 ("POSITIVE",(15,15),True),
 ("FRESH",(5,5),True),
 ("FORGED",(362,362),True),
 ("CODES",(362,362),True),
 ("EMPTY",(1,1),True),
 ("RC",(4,4),True),
 ("SETUP",(1,1),True),
 ("D1_WIDTH",(3,3,3,3),True),
 ("D1_REFUSED",(3,3),True),
 ("D2_WIDTH",(3,3,3,3),True),
 ("D2_REFUSED",(3,3),True),
 ("MUT_ADMIT",(1,1),True),
 ("MUT_UNREACH",(1,1),True),
 ("DERIVE_NEG",(1,1),True),
]
for n,nums,exp in tests:
    ok,note=cc(n,nums)
    print(f"{n}: ok={ok} exp={exp} {'MATCH' if ok==exp else 'DIFF'} note={note}")

# Vacuity probes: mutate summary fields, see which go unchecked
print("\n--- vacuity: change one summary field at a time ---")
for k,v in list(good.items()):
    bad=dict(good); 
    if "/" in v: a,b=v.split("/"); bad[k]=f"{int(a)+1}/{b}"
    else: bad[k]=str(int(v)+1)
    cc2=make(summ=bad)
    # find which leg catches it
    caught=[]
    for n,nums,_ in tests:
        ok,_=cc2(n,nums)
        if not ok: caught.append(n)
    print(f"change {k} -> caught by {caught}")

print("\n--- vacuity: FOREIGN summary fields (LEGS_MEASURED, DIV3-in-D2 etc) ---")
# LEGS_MEASURED is NOT in crosscheck map at all
print("LEGS_MEASURED in crosscheck keys?", "LEGS_MEASURED" in good)  # not compared anywhere
# DIV3 is compared, but twice (WIDTH legs both read DIV3) - changing DIV3 catches BOTH width legs
# What about 'TOOL' mismatch? handled. What about EXTRA fields not in map? e.g. FORGED vs CODES both exist.
# Which printed summary fields are NEVER read by crosscheck?
keys_read=set()
cc_code=open("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round89/gate-records-r89.py").read()
print("summ.get usages:", sorted(set(re.findall(r"summ\.get\(\"([A-Z_0-9]+)\"",cc_code))))
print("_ints usages:", sorted(set(re.findall(r"_ints\(\"([A-Z_0-9]+)\"\)",cc_code)) + re.findall(r'_ints\("([^"]+)"',cc_code)))
# also derived keys
print("name+_DERIVED etc are dynamic")
# List all summary fields
print("ALL summary fields:", sorted(good.keys()))
read=set(re.findall(r'summ\.get\(\"([A-Z_0-9]+)\"',cc_code)) | set(re.findall(r'_ints\(\"([A-Z_0-9]+)\"',cc_code))
# MUT_ dynamic: MUT_ADMIT_DERIVED etc use name+"_DERIVED"
print("READ set:", sorted(read))
print("UNREAD:", sorted(set(good.keys())-read-{"MUT_ADMIT_DERIVED","MUT_ADMIT_KILLED","MUT_UNREACH_DERIVED","MUT_UNREACH_KILLED"}))
# D1_FORGES/D2_FORGES/D1_EXPECTED/DIV3 read explicitly, printed?
# Check: is DIV3 compared in D2_WIDTH too (same cell)? yes both legs read it.
# Is any leg compared to itself? DERIVE_NEG: nums=(1,1) from detail "1/1", compares _ints("DERIVE_NEG")==[nums[0]] where nums[0]==nums[1] checked.
# TOOL: nums=() so crosscheck(name,()) - TOOL branch ignores nums entirely!
print("\nTOOL branch uses tool_present, not nums. DERIVE_NEG: nums=(a,b) with a==b AND summary==a. Width: nums=(a,b,c,pin), checks a==FORGES etc but NOT pin==c? Pin checked vs ROWS only.")
# Width pin: rederive requires a==b==c==pin, crosscheck requires pin==ROWS_203 but does NOT re-check a==b==c? It checks a==FORGES, b==EXPECTED, c==DIV3 separately. If detail had a!=b, rederive False -> UNRECONCILED, but crosscheck might still pass if summary matches a,b,c individually? But nums from failed rederive still passed to crosscheck!

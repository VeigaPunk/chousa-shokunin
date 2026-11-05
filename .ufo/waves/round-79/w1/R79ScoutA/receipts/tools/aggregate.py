"""Aggregate structure-identity recovery over the 13 subjects: what a normalizer that
unmarshals the payload and canonicalises the fresh identifier table recovers."""
import ast, base64, importlib.util, marshal, pathlib, shutil, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SUBJ = [("successor-counter", LANE + "/corpus/evidence/round74/correction-count.py"),
        ("ref-counter", LANE + "/corpus/evidence/round75/ref-counter.py")]
for n, f in [("constant-pass","forge-constant-pass.py"),("constant-fail","forge-constant-fail.py"),
             ("order-twelve","forge-order-twelve.py"),("diff-only","forge-diff-only.py"),
             ("naive-grep","forge-naive-grep.py"),("subject-map","forge-subject-map.py"),
             ("tree-identity","forge-tree-identity.py"),("size-map","forge-size-map.py"),
             ("harness-source","forge-harness-source.py"),("seed-leak","forge-seed-leak.py"),
             ("hang","forge-hang.py")]:
    SUBJ.append((n, LANE + "/corpus/evidence/round76/forgers/" + f))

def payload_of(p):
    for n in ast.walk(ast.parse(p.read_text())):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "b85decode":
            return n.args[0].value

def consts(code, acc):
    for c in code.co_consts:
        acc.append(c)
        if hasattr(c, "co_code"): consts(c, acc)
    return acc

def names(code, acc):
    acc.extend(code.co_names)
    for c in code.co_consts:
        if hasattr(c, "co_code"): names(c, acc)
    return acc

tot_s = tot_sr = tot_n = tot_nf = 0
print("subject | string literals recovered | identifier names in payload that are FRESH | original names surviving")
for name, src in SUBJ:
    src = pathlib.Path(src)
    copy = bat.reemit(src, work)
    code = marshal.loads(base64.b85decode(payload_of(copy)))
    strs = {c for c in consts(code, []) if isinstance(c, str)}
    nm = names(code, [])
    t = ast.parse(src.read_text())
    orig_strs = {n.value for n in ast.walk(t)
                  if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    orig_names = set()
    for nd in ast.walk(t):
        if isinstance(nd, ast.Name): orig_names.add(nd.id)
        elif isinstance(nd, ast.arg): orig_names.add(nd.arg)
        elif isinstance(nd, (ast.FunctionDef, ast.ClassDef)): orig_names.add(nd.name)
    rec = sum(1 for s in orig_strs if s in strs)
    fresh = sum(1 for n in set(nm) if n.startswith("_") and len(n) == 9)
    kept = sorted(n for n in set(nm) & orig_names if not n.startswith("_"))
    print(f"{name}: {rec}/{len(orig_strs)} | {fresh}/{len(set(nm))} | {kept}")
    tot_s += len(orig_strs); tot_sr += rec; tot_n += len(set(nm)); tot_nf += fresh
    shutil.rmtree(copy.parent, ignore_errors=True)
print(f"TOTAL strings {tot_sr}/{tot_s} = {tot_sr/tot_s:.1%} | fresh names {tot_nf}/{tot_n} = {tot_nf/tot_n:.1%}")

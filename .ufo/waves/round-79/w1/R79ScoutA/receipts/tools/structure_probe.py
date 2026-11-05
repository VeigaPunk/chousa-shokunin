"""STRUCTURE-IDENTITY RESIDUAL RISK: the copy is base85(marshal(code)) plus a fixed
wrapper. Unmarshal it and measure what a normalizer recovers: identifier names vs
string literals (which in these subjects carry the semantic contract)."""
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

def strings_of(p):
    t = ast.parse(pathlib.Path(p).read_text())
    return {n.value for n in ast.walk(t)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}

def payload_of(copy_path):
    tree = ast.parse(copy_path.read_text())
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "b85decode":
            return n.args[0].value
    return None

def all_consts(code, acc):
    for c in code.co_consts:
        acc.append(c)
        if hasattr(c, "co_code"):
            all_consts(c, acc)
    return acc

def all_names(code, acc):
    acc.extend(code.co_names)
    for c in code.co_consts:
        if hasattr(c, "co_code"):
            all_names(c, acc)
    return acc

print("name | string_literals_recovered | names_in_payload_fresh | names_matching_original")
for name, src in SUBJ:
    src = pathlib.Path(src)
    copy = bat.reemit(src, work)
    code = marshal.loads(base64.b85decode(payload_of(copy)))
    strs = {c for c in all_consts(code, []) if isinstance(c, str)}
    names = all_names(code, [])
    orig = strings_of(src)
    recovered = sum(1 for s in orig if s in strs)
    fresh = sum(1 for n in set(names) if n.startswith("_") and len(n) == 9)
    orig_names = set()
    t = ast.parse(src.read_text())
    for nd in ast.walk(t):
        if isinstance(nd, ast.Name): orig_names.add(nd.id)
        elif isinstance(nd, ast.arg): orig_names.add(nd.arg)
        elif isinstance(nd, (ast.FunctionDef, ast.ClassDef)): orig_names.add(nd.name)
    kept = sorted(n for n in set(names) & orig_names if not n.startswith("_"))
    print(f"{name}: {recovered}/{len(orig)} | fresh={fresh}/{len(set(names))} | kept_original_names={kept}")
    shutil.rmtree(copy.parent, ignore_errors=True)

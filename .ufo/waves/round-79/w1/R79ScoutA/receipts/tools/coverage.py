"""Per subject: which bound identifiers SURVIVE the battery's rename (i.e. are not
fresh), and which are excluded only because their spelling is a keyword-argument name."""
import ast, builtins, pathlib, sys

root = pathlib.Path(sys.argv[1])
tot_b = tot_r = tot_s = 0
for p in sorted(root.glob("*.py")):
    tree = ast.parse(p.read_text())
    ex = set(dir(builtins)); kw = set(); imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names: imported.add(a.asname or a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names: imported.add(a.asname or a.name)
        elif isinstance(node, ast.keyword) and node.arg: kw.add(node.arg)
    ex |= imported | kw
    bound = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name): bound.setdefault(node.id, []).append(node.lineno)
        elif isinstance(node, ast.arg): bound.setdefault(node.arg, []).append(node.lineno)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.setdefault(node.name, []).append(node.lineno)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.setdefault(node.name, []).append(node.lineno)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            for n in node.names: bound.setdefault(n, []).append(node.lineno)
    survivors = sorted(n for n in bound if n in ex and not n.startswith("__"))
    kw_only = sorted(n for n in survivors if n in kw and n not in imported)
    renamable = sorted(n for n in bound if n not in ex and not n.startswith("__"))
    tot_b += len(bound); tot_r += len(renamable); tot_s += len(kw_only)
    print(f"{p.name}:")
    print(f"   bound={len(bound)} renamed={len(renamable)} "
          f"survivors(excluded,non-dunder)={survivors}")
    print(f"   survivors attributable to a KEYWORD-ARGUMENT name: {kw_only}")
print(f"TOTAL bound={tot_b} renamed={tot_r} kwarg-spelled survivors={tot_s}")

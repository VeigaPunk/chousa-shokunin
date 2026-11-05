"""Scan the 13 subjects for the residual-risk classes the battery does NOT cover:
 (a) ast.Attribute.attr naming a module-local binding  (method/attribute access to a
     renamed def/class breaks: def names are renamed, attribute names are not);
 (b) a keyword-argument name that equals a parameter of a module-local def
     (the exclusion is module-global, so it is safe — verify);
 (c) **kwargs splat into a module-local def (string key, not an ast.keyword).
"""
import ast, builtins, pathlib, sys

root = pathlib.Path(sys.argv[1])
for p in sorted(root.glob("*.py")):
    tree = ast.parse(p.read_text())
    # module-local bindings (def/class names and module-level assignment targets)
    local_defs = {n.name for n in ast.walk(tree)
                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    hit = sorted(attrs & local_defs)
    # keyword args vs local-def parameters
    kwnames = {k.arg for n in ast.walk(tree) if isinstance(n, ast.Call) for k in n.keywords if k.arg}
    params = {}
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params[n.name] = [a.arg for a in n.args.args + n.args.kwonlyargs]
    collide = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            nm = getattr(n.func, "id", None)
            if nm in params:
                for k in n.keywords:
                    if k.arg and k.arg in params[nm]:
                        collide.append(f"{nm}({k.arg}=...) -> param {params[nm]}")
    splat = [f"{getattr(n.func,'id',None)}(**" for n in ast.walk(tree)
             if isinstance(n, ast.Call) and any(k.arg is None for k in n.keywords)]
    print(f"{p.name}:")
    print(f"   (a) attribute-name referring to a module-local def/attr: {hit or 'NONE'}")
    print(f"   (b) kwarg==local-param collisions: {collide or 'NONE'}")
    print(f"   (c) **-splat calls into local defs: {splat or 'NONE'}")

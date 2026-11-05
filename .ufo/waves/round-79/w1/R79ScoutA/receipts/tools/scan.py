"""AST sweep of the 13 round-79 battery subjects for string-keyed rename hazards.

Mirrors matrix-battery-v6.py's _rename() exclusion rules so that the set of
"renamable" identifiers is computed the same way the battery computes it.
"""
import ast, builtins, pathlib, sys

def excluded_set(tree):
    ex = set(dir(builtins))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                ex.add(a.asname or a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                ex.add(a.asname or a.name)
        elif isinstance(node, ast.keyword) and node.arg:
            ex.add(node.arg)
    return ex

def renamable(tree):
    """Names the battery would rename (i.e. bound identifiers not in the excluded set)."""
    ex = excluded_set(tree)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            names.update(node.names)
    return {n for n in names if n not in ex and not n.startswith("__")}, ex

def report(path):
    tree = ast.parse(path.read_text())
    ren, ex = renamable(tree)
    findings = []
    for node in ast.walk(tree):
        ln = getattr(node, "lineno", 0)
        if isinstance(node, ast.Call):
            fn = node.func
            fname = getattr(fn, "id", None) or getattr(fn, "attr", None)
            if fname in ("getattr", "setattr", "hasattr", "delattr", "globals",
                         "locals", "vars", "eval", "exec", "compile"):
                args = [getattr(a, "value", None) for a in node.args]
                findings.append((ln, f"call:{fname}", f"string args={args!r}"))
            if fname in ("import_module", "spec_from_file_location", "module_from_spec"):
                findings.append((ln, f"call:{fname}", "importlib name lookup"))
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            if v in ren:
                findings.append((ln, "string==renamable", repr(v)))
            if v in {"__all__"} or v == "__all__":
                findings.append((ln, "__all__ literal", repr(v)))
        if isinstance(node, ast.JoinedStr):
            # f-string debug specifier: Constant ending with '=' immediately before a FormattedValue
            for i, part in enumerate(node.values):
                if isinstance(part, ast.Constant) and isinstance(part.value, str) \
                   and part.value.endswith("=") and i + 1 < len(node.values) \
                   and isinstance(node.values[i + 1], ast.FormattedValue):
                    findings.append((ln, "f-string debug '='", repr(part.value)))
        if isinstance(node, (ast.Match, ast.MatchAs, ast.MatchStar, ast.MatchMapping,
                             ast.MatchClass, ast.MatchValue)):
            findings.append((ln, f"match:{type(node).__name__}", ast.dump(node)[:120]))
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            findings.append((ln, f"{type(node).__name__}", repr(node.names)))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for d in node.decorator_list:
                findings.append((ln, "decorator", ast.dump(d)[:120]))
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            findings.append((ln, "__future__", node.module))
    # keyword-argument names that collide with a renamable parameter of a local def
    params = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params[node.name] = [a.arg for a in node.args.args + node.args.kwonlyargs]
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            nm = getattr(f, "id", None)
            if nm in params:
                for k in node.keywords:
                    if k.arg and k.arg in params[nm] and k.arg in ren:
                        findings.append((getattr(node, "lineno", 0),
                                         "kwarg==local param", f"{nm}(... {k.arg}=...)"))
    return ren, ex, findings

def main():
    root = pathlib.Path(sys.argv[1])
    for p in sorted(root.glob("*.py")):
        ren, ex, f = report(p)
        print(f"### {p.name}  renamable={len(ren)} excluded={len(ex)} findings={len(f)}")
        for ln, kind, detail in sorted(f):
            print(f"  {p.name}:{ln}: {kind}: {detail}")

main()

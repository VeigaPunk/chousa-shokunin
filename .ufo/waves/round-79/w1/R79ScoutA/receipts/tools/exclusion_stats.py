"""Per subject: how many bound identifiers does the battery rename, and which ones
escape renaming ONLY because their spelling is used as a keyword-argument name?"""
import ast, builtins, pathlib, sys

root = pathlib.Path(sys.argv[1])
for p in sorted(root.glob("*.py")):
    tree = ast.parse(p.read_text())
    ex = set(dir(builtins))
    kw_names = set()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported.add(a.asname or a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                imported.add(a.asname or a.name)
        elif isinstance(node, ast.keyword) and node.arg:
            kw_names.add(node.arg)
    ex |= imported | kw_names
    bound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            bound.add(node.id)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            bound.update(node.names)
    renamable = {n for n in bound if n not in ex and not n.startswith("__")}
    escaped = {n for n in bound if n in kw_names and not n.startswith("__")}
    # escaped names that are also MODULE-LEVEL bindings (the visible surface)
    module_level = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    module_level.add(t.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            module_level.add(node.name)
    esc_mod = sorted(n for n in escaped if n in module_level)
    print(f"{p.name}: bound={len(bound)} renamed={len(renamable)} "
          f"kwarg_excluded={sorted(escaped)} kwarg_excluded_module_level={esc_mod}")

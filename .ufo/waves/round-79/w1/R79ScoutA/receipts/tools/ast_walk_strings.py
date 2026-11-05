import ast, pathlib, sys
def strings_of(p):
    t = ast.parse(pathlib.Path(p).read_text())
    out = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.add(n.value)
    return out

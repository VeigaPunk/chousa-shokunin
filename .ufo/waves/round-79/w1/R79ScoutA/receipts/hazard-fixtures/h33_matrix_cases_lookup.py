import importlib.util, sys
CASES = [("c", 0, frozenset())]
def load(path):
    spec = importlib.util.spec_from_file_location("h", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "CASES", [])
if __name__ == "__main__":
    print(load(sys.argv[1]))

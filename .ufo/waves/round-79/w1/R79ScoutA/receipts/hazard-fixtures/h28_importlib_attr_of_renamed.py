import importlib
mod = importlib.import_module("json")
if __name__ == "__main__":
    print(mod.dumps([1]))

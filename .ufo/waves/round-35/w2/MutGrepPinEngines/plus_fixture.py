import importlib.util, sys
spec = importlib.util.spec_from_file_location("c1", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round35/c1-count.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.make_fixture(sys.argv[1]))

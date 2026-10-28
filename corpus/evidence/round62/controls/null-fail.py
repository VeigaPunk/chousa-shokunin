#!/usr/bin/env python3
import importlib.util, pathlib, sys
s = importlib.util.spec_from_file_location("nc", pathlib.Path(__file__).resolve().with_name("null-counter.py"))
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
sys.exit(m.main("fail"))

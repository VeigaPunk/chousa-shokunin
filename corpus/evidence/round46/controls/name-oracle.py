#!/usr/bin/env python3
import sys, pathlib
name = pathlib.Path(sys.argv[sys.argv.index("--entry") + 1]).name
raise SystemExit(0 if name.startswith("positive-") else 1)

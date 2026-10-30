"""Isolated G02 markdown-escaped underscore probe; execute from any cwd with python3."""
import argparse
import importlib.util
import pathlib
import tempfile

candidate = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py")
root = pathlib.Path("/fast/scratch/hyaku/chousa-r64/G02Probe09/fixture")
(root / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
(root / "corpus/knowledge/foo_bar.md").write_text("fixture\n", encoding="utf-8")
(root / "corpus/README.md").write_text("Knowledge entry: foo\\_bar.md\n", encoding="utf-8")
spec = importlib.util.spec_from_file_location("candidate", candidate)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
args = argparse.Namespace()
with tempfile.TemporaryDirectory(prefix="g02-probe-") as work:
    result = module.g02(root, args, {}, pathlib.Path(work))
print("fixture: knowledge/foo_bar.md; README token: foo\\_bar.md")
print(f"observed: {result[0]} {result[1]}")
print("exit: " + ("0" if result[0] == "PASS" else "1"))
raise SystemExit(0 if result[0] == "PASS" else 1)

#!/usr/bin/env python3
"""R75Critic probe: rebuild the frozen matrix's fixture bytes in the seat's own
scratch and dump the case identity signatures a metadata-reading candidate can
see (tree id, blob ids, byte sizes, commit subject).

The frozen instrument is imported as a module, so FILES/CASES/mutate are the
instrument's own bytes, never a transcription. A second build is compared
against the first to prove the signatures are run-independent.

Writes only under the seat scratch root and prints one JSON document.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import importlib.util

MATRIX = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py"
SCRATCH = pathlib.Path("/fast/scratch/hyaku/chousa-r75/R75Critic")


def load_matrix():
    spec = importlib.util.spec_from_file_location("loader_matrix_v2", MATRIX)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip()[:400])
    return p.stdout.strip()


def build(m, order):
    """One fixture repo, commits in `order`; returns per-case signature dict."""
    root = pathlib.Path(tempfile.mkdtemp(prefix="harvest-", dir=SCRATCH))
    git(root, "init", "-q")
    top = git(root, "rev-parse", "--show-toplevel")
    if pathlib.Path(top).resolve() != root.resolve() or root.parent != SCRATCH:
        raise RuntimeError(f"fixture root mismatch: {top}")
    if not str(root).startswith(str(SCRATCH) + "/"):
        raise RuntimeError(f"fixture outside scratch: {root}")
    for path, text in m.FILES.items():
        t = root / path
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(text)
    paths = list(m.FILES)
    git(root, "add", "--", *paths)
    ident = ("-c", "user.name=fixture", "-c", "user.email=fixture@invalid")
    git(root, *ident, "commit", "-qm", "base")
    base = git(root, "rev-parse", "HEAD")
    out = {"root": str(root), "base": base,
           "base_sizes": {p: (root / p).stat().st_size for p in paths},
           "base_tree": git(root, "rev-parse", "HEAD^{tree}"), "cases": {}}
    for name, path, operation, rc, failed in order:
        for key, value in m.FILES.items():
            (root / key).write_text(value)
        if path:
            (root / path).write_text(m.mutate(m.FILES[path], operation))
        git(root, "add", "--", *paths)
        git(root, *ident, "commit", "--allow-empty", "-qm", name)
        rev = git(root, "rev-parse", "HEAD")
        out["cases"][name] = {
            "rev": rev,
            "tree": git(root, "rev-parse", "HEAD^{tree}"),
            "sizes": {p: (root / p).stat().st_size for p in paths},
            "blobs": {p: git(root, "rev-parse", f"HEAD:{p}") for p in paths},
            "subject": git(root, "log", "-1", "--format=%s", rev),
            "depth": int(git(root, "rev-list", "--count", f"{base}..{rev}")),
            "expected_rc": rc,
            "expected_failed": sorted(failed),
        }
    return out


def main() -> int:
    m = load_matrix()
    declared = [tuple(row[:5]) for row in m.CASES]
    first = build(m, declared)
    second = build(m, list(reversed(declared)))
    stable = {n: first["cases"][n]["tree"] == second["cases"][n]["tree"]
              and first["cases"][n]["sizes"] == second["cases"][n]["sizes"]
              and first["cases"][n]["blobs"] == second["cases"][n]["blobs"]
              for n in first["cases"]}
    distinct_trees = len({v["tree"] for v in first["cases"].values()})
    distinct_sizes = len({json.dumps(v["sizes"], sort_keys=True) for v in first["cases"].values()})
    distinct_subj = len({v["subject"] for v in first["cases"].values()})
    doc = {
        "matrix_sha256": __import__("hashlib").sha256(pathlib.Path(MATRIX).read_bytes()).hexdigest(),
        "n_cases": len(declared),
        "base": first["base"], "base_sizes": first["base_sizes"],
        "base_tree": first["base_tree"],
        "same_root": first["root"] == second["root"],
        "trees_stable_across_orderings": stable,
        "distinct_trees": distinct_trees,
        "distinct_size_vectors": distinct_sizes,
        "distinct_subjects": distinct_subj,
        "cases": first["cases"],
    }
    print(json.dumps(doc, indent=1, sort_keys=True))
    shutil.rmtree(first["root"], ignore_errors=True)
    shutil.rmtree(second["root"], ignore_errors=True)
    return 0 if all(stable.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

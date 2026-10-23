#!/usr/bin/env python3
"""receipt-binding.py — E4 measurement-binding census.

Walks a directory of JSON receipts, reads each receipt's ``gate_sha256`` (and the
gate path it names), and reports every receipt whose gate hash matches no
*committed* blob in the lane repository.

Committed-blob set (E4 repair):
  * every committed blob of ``tools/research-gate.sh`` across
    ``git -C <repo> rev-list --all`` (i.e. every revision of the lane gate), plus
  * every committed ``*.sh`` blob under ``.ufo/waves/`` (controls, mutants,
    mask gates, scratch gate copies that were committed).

A receipt whose ``gate_sha256`` is in that set is *bound*: it names bytes that
exist in the repository history.  A receipt whose hash is absent is *unbound*:
it was measured on bytes that were never committed (a scratch/worktree state),
so it cannot be cited as evidence for a landed claim.

Output (stdout), one line per finding:

    UNBOUND <receipt-path-relative-to-repo-root> <gate_sha256>

followed by totals.  Exit status:

    0  no unbound receipt carries a landed/final label
    1  at least one unbound receipt carries a landed/final label
       (path under ``measure/``, or file name containing ``landed``/``final``)

Read-only: the tool never writes to the repository and never runs the gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

HEX = set("0123456789abcdef")


def _git(repo: str, *args: str) -> bytes:
    return subprocess.run(
        ("git", "-C", repo) + args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def _blob_sha256s(repo: str, blob_ids: set[str]) -> dict[str, str]:
    """sha256 (content hash, not the git object id) for each blob id."""
    if not blob_ids:
        return {}
    ids = sorted(blob_ids)
    proc = subprocess.run(
        ("git", "-C", repo, "cat-file", "--batch"),
        input=("\n".join(ids) + "\n").encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = proc.stdout
    result: dict[str, str] = {}
    pos = 0
    for oid in ids:
        nl = out.find(b"\n", pos)
        if nl < 0:
            break
        header = out[pos:nl].decode()
        pos = nl + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            continue
        size = int(parts[2])
        data = out[pos:pos + size]
        pos += size + 1  # trailing newline after the payload
        result[oid] = hashlib.sha256(data).hexdigest()
    return result


def committed_gate_blobs(repo: str, gate_path: str) -> set[str]:
    """Blob ids of ``gate_path`` across every commit reachable from any ref."""
    commits = _git(repo, "rev-list", "--all").decode().split()
    blobs: set[str] = set()
    # `git ls-tree` per commit is slow; ask git for the path's blob directly.
    for c in commits:
        r = subprocess.run(
            ("git", "-C", repo, "rev-parse", "--verify", "-q", f"{c}:{gate_path}"),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if r.returncode == 0:
            oid = r.stdout.decode().strip()
            if oid:
                blobs.add(oid)
    return blobs


def committed_wave_shell_blobs(repo: str, waves_prefix: str) -> set[str]:
    """Blob ids of every committed ``*.sh`` under ``waves_prefix``."""
    raw = _git(repo, "rev-list", "--all", "--objects", "--", waves_prefix).decode()
    blobs: set[str] = set()
    for line in raw.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        if path.endswith(".sh"):
            blobs.add(oid)
    return blobs


def is_hex64(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(c in HEX for c in value)
    )


def landed_final_label(rel_path: str) -> bool:
    """Landed/final labelling used by the E4 exit rule."""
    parts = rel_path.split("/")
    if "measure" in parts[:-1]:
        return True
    name = parts[-1]
    return ("landed" in name) or ("final" in name)


def walk_receipts(root: str) -> list[str]:
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if name.endswith(".json"):
                out.append(os.path.join(dirpath, name))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("repo", help="lane repository root (read-only)")
    ap.add_argument("receipts", help="directory tree of JSON receipts to census")
    ap.add_argument("--gate-path", default="tools/research-gate.sh",
                    help="lane gate path inside the repository")
    ap.add_argument("--waves-prefix", default=".ufo/waves/",
                    help="prefix holding committed control/mutant shell scripts")
    ap.add_argument("--json-out", default=None,
                    help="write the census result as JSON to this path")
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    receipts_root = os.path.abspath(args.receipts)

    gate_blobs = committed_gate_blobs(repo, args.gate_path)
    wave_blobs = committed_wave_shell_blobs(repo, args.waves_prefix)
    hashes = _blob_sha256s(repo, gate_blobs | wave_blobs)
    bound_hashes = set(hashes.values())

    n_receipts = 0
    n_hash = 0
    n_bound = 0
    n_unbound = 0
    n_nohash = 0
    n_badjson = 0
    unbound_labelled: list[tuple[str, str]] = []
    unbound_other: list[tuple[str, str]] = []

    for path in walk_receipts(receipts_root):
        rel = os.path.relpath(path, repo)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                doc = json.load(fh)
        except Exception:
            n_badjson += 1
            continue
        n_receipts += 1
        if not isinstance(doc, dict):
            n_nohash += 1
            continue
        gate_hash = doc.get("gate_sha256")
        if is_hex64(gate_hash):
            candidates = [gate_hash]
        else:
            # Some receipts record only the pre/post gate digests of the run
            # (gate_sha256_before / gate_sha256_after).  Fall back to those so
            # the census has no blind spot.
            candidates = [
                h for h in (doc.get("gate_sha256_before"),
                            doc.get("gate_sha256_after"))
                if is_hex64(h)
            ]
            if not candidates:
                n_nohash += 1
                continue
        n_hash += 1
        unbound_here = [h for h in candidates if h not in bound_hashes]
        if not unbound_here:
            n_bound += 1
            continue
        gate_hash = unbound_here[0]
        n_unbound += 1
        gate_path = doc.get("gate")
        if not isinstance(gate_path, str):
            gate_path = ""
        if landed_final_label(rel):
            unbound_labelled.append((rel, gate_hash, gate_path))
        else:
            unbound_other.append((rel, gate_hash, gate_path))

    print(f"REPO {repo}")
    print(f"RECEIPTS_ROOT {receipts_root}")
    print(f"COMMITTED_GATE_BLOBS {len(gate_blobs)}")
    print(f"COMMITTED_WAVE_SH_BLOBS {len(wave_blobs)}")
    print(f"COMMITTED_BLOB_HASHES {len(bound_hashes)}")
    for rel, gate_hash, _gate_path in unbound_labelled + unbound_other:
        print(f"UNBOUND {rel} {gate_hash}")
    print(f"TOTAL_RECEIPTS {n_receipts}")
    print(f"TOTAL_WITH_GATE_HASH {n_hash}")
    print(f"TOTAL_BOUND {n_bound}")
    print(f"TOTAL_UNBOUND {n_unbound}")
    print(f"TOTAL_UNBOUND_LANDED_FINAL {len(unbound_labelled)}")
    print(f"TOTAL_UNBOUND_OTHER {len(unbound_other)}")
    print(f"TOTAL_NO_GATE_HASH {n_nohash}")
    print(f"TOTAL_UNPARSEABLE_JSON {n_badjson}")

    if args.json_out:
        result = {
            "repo": repo,
            "receipts_root": receipts_root,
            "committed_gate_blobs": len(gate_blobs),
            "committed_wave_sh_blobs": len(wave_blobs),
            "committed_blob_hashes": len(bound_hashes),
            "totals": {
                "receipts": n_receipts,
                "with_gate_hash": n_hash,
                "bound": n_bound,
                "unbound": n_unbound,
                "unbound_landed_final": len(unbound_labelled),
                "unbound_other": len(unbound_other),
                "no_gate_hash": n_nohash,
                "unparseable_json": n_badjson,
            },
            "unbound": [
                {"path": rel, "gate_sha256": h, "gate": gp,
                 "landed_final_label": landed_final_label(rel)}
                for rel, h, gp in unbound_labelled + unbound_other
            ],
            "exit_code": 1 if unbound_labelled else 0,
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
            fh.write("\n")

    if unbound_labelled:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

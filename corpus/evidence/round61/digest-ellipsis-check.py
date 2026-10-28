#!/usr/bin/env python3
"""R61 check — an abbreviated digest in a claims or lesson file must match a real file.

Finds every `<8 hex>…<5 to 8 hex>` token (prefix, ellipsis, suffix of a sha256) in FILE and looks for a
file under the lane (git-tracked or not, skipping .git) whose sha256 starts with the prefix and ends with
the suffix. Prints `DIGEST_ELLIPSIS tokens=n matched=m mismatched=k` and one `MISMATCH token` line per
miss; exit 0 iff k == 0 and n > 0, 1 otherwise, 2 usage. QUALITY 122: round 61's claims file carries two
such tokens that no file matches (`controls`' runner and `c1-count.py` tails mistyped by the L1).
Usage: python3 corpus/evidence/round61/digest-ellipsis-check.py FILE [--root LANE]
"""
import hashlib, os, pathlib, re, sys

LANE = pathlib.Path(__file__).resolve().parents[3]
TOKEN = re.compile(r"\b([0-9a-f]{8})…([0-9a-f]{5,8})\b")


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    root = LANE
    if "--root" in sys.argv:
        root = pathlib.Path(sys.argv[sys.argv.index("--root") + 1])
    toks = sorted(set(TOKEN.findall(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))))
    pending = set(toks)
    hits = set()
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git", "__pycache__", ".jj")]
        for n in fns:
            if not pending:
                break
            p = pathlib.Path(dp) / n
            try:
                if p.stat().st_size > 20 << 20:
                    continue
                h = hashlib.sha256(p.read_bytes()).hexdigest()
            except OSError:
                continue
            for pre, suf in list(pending):
                if h.startswith(pre) and h.endswith(suf):
                    hits.add((pre, suf))
                    pending.discard((pre, suf))
    miss = sorted(set(toks) - hits)
    for pre, suf in miss:
        print(f"MISMATCH {pre}…{suf}")
    print(f"DIGEST_ELLIPSIS tokens={len(toks)} matched={len(hits)} mismatched={len(miss)}")
    return 0 if toks and not miss else 1


if __name__ == "__main__":
    sys.exit(main())

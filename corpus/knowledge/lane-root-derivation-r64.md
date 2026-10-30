source: S150 — /usr/lib/python3.14/pathlib/__init__.py lines 49–72, 392–396, 932–938; S151 — /usr/share/man/man1/realpath.1.gz DESCRIPTION -e; S152 — corpus/evidence/round64/c3-count.py lines 34–39, 85–93
verified-at: 2026-10-30; installed Python 3.14.8 and GNU coreutils 9.12; round64 source opening
recheck: on-release; re-open named sections and run python3 corpus/evidence/round64/c3-count.py --work <fresh-scratch-dir>

# Derived roots name locations, not intentions

## Question

What can this lane establish before a counter reads a file relative to its own location?

## Located evidence

- S150, PurePath.parents docstring, lines 392–393: “A sequence of this path's logical parents.” Its sequence implementation slices `_tail[:-idx - 1]` (lines 63–72).
- S150, Path.resolve docstring, lines 932–935: “Make the path absolute, resolving all symlinks on the way and also normalizing it.” Line 938 delegates to `os.path.realpath(self, strict=strict)`.
- S151, DESCRIPTION, `-e, --canonicalize-existing`: “all components of the path must exist”. This is the realpath command's contract, not a claim that Path.resolve defaults to strict existence checking.
- S152, c3-count.py lines 35–39: the counter derives `LANE = HERE.parents[2]`, checks `corpus/SOURCES.md`, and prints `MISSING_LANE_FILE:` before raising SystemExit(2) if it is missing.

## Claims

1. Parent indexing in the installed pathlib implementation is positional: the slice removes idx+1 components. Neither the docstring nor that slice identifies a Git repository or an intended lane. **Inference from S150**, not a promise of repository detection.
2. The local resolve docstring describes normalization and symlink resolution. It does not promise to validate this lane's intended root. The code defaults `strict=False`; the existence check must not be inferred from the word resolve. **Observation from S150**.
3. The realpath command exposes an explicit existing-components mode. Treating existence as an explicit requirement, rather than a property of a normalized string, is supported by S151's `-e` distinction.
4. Checking the exact file at its derived location catches a missing-file instance before measurement. It does not catch a wrong but populated root. **Inference from S152's conditional**, restricted to the branch it implements.

## The round's counter is not an oracle

The frozen relocation counter has its own expected-path expression at line 91 (`mirror.parent / needs[0]`). That expression must be compared to the copied instrument's actual parents arithmetic; the mere presence of the startup assertion does not validate the counter's expectation. The round records the observed verdict separately rather than treating this entry as a passing measurement.

## Rejection and limits

S153 (the candidate preflight docstring) is rejected as evidence that the implementation meets its index contract: a contract description is not an execution. Root assertions prove neither file provenance nor content, cannot disambiguate two populated trees, and do not remove time-of-check/time-of-use races. No external source was fetched. General filesystem tooling and testing methods remain adjacent; this entry concerns the lane's own research instruments.

# CritNoFetch

Seat: leaf critic. Attacked surface: the no-fetch claim on `tools/absent-split.py` and the three round-43 counters. Axes: operability, calibration, depth. Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (working tree clean for those four files plus `tools/quarantine-check.py`). No network. No production edit. Bound not retuned.

## Assigned grep

Tokens: `urllib`, `requests`, `curl`, `wget`, `socket`.

Hits in the four named files: **none**.

Grep tool, each file separately, same pattern:

```text
No non-sensitive matches found
```

returned for:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c3-count.py`

Line-numbered rescan (case-sensitive, then casefold-only):

```text
ASSIGNED_GREP_BEGIN
FILE /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py lines=145
FILE /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py lines=103
FILE /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py lines=141
FILE /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c3-count.py lines=72
ASSIGNED_HITS=0
ASSIGNED_GREP_END
CASEFOLD_BEGIN
CASEFOLD_ONLY_HITS=0
CASEFOLD_END
GATE_TOKEN_BEGIN
GATE_TOKEN_HITS=0
GATE_TOKEN_END
```

`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD` and a porcelain check of the five sources printed only:

```text
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
```

## Counterexample

The five-token list is an incomplete egress probe. It does not name the only calls that could still reach the network:

- `c1-count.py:26` imports `subprocess`. `c1-count.py:45-48` runs `[sys.executable, str(tool)]` with `shell=False` and no env override. Default `tool` is `tools/absent-split.py`.
- `absent-split.py:72-76` and `c2-count.py:62-66` `exec_module` `tools/quarantine-check.py` under the name `quarantine_check`, so the gate's `if __name__ == "__main__"` block (`quarantine-check.py:416-417`) does not run. The functions that do run are `parse_register` and `cache_doc`.

If either callee opened a socket, `ASSIGNED_HITS=0` would be a false clean. That is the strongest counterexample the token list allows. It does not instantiate.

A second, false counterexample must not be laundered in. A directory grep of `corpus/evidence/round43` for the same tokens matches a file this seat was not assigned:

```text
chousa-shokunin/corpus/evidence/round43/receipts/census-end.txt:2:chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
```

That line is a census note about a duplicate URL. It is not an import and not a fetch. Reporting it as a hit of this seat's four files would be false provenance.

## Evidence the executed path does not fetch

`quarantine-check.py` imports only `__future__`, `argparse`, `hashlib`, `pathlib`, `re`, `sys`, `unicodedata` (lines 31-38). No `urllib`, `requests`, `curl`, `wget`, `socket`, `http.client`, `urlopen`, `httpx`, `aiohttp`, `ftplib`, or `subprocess` (content grep of those names: no match).

`cache_doc` (`quarantine-check.py:244-258`) hashes the URL to a local path, reads `key.txt` if it exists, and otherwise returns `(None, None, "missing")`. A missing capture is not fetched. `absent-split.py:130-133` then exits 1. `c2-count.py:83-85` skips that row, so `expected.get(rid)` is missing and agreement fails. Both fail closed.

The only near-miss in the executed module is a class-label test, not a call:

```text
quarantine-check.py:209:    return ("could not be fetched" in low or "named no locator" in low
```

The assigned tokens do not match that line (`GATE_TOKEN_HITS=0`). A broader `fetch` grep must not be scored as egress.

`c3-count.py:30` embeds `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`. Lines 56-62 use that string as a `SOURCES.md` substring and as `sha256(URL)[:24]` into the local `.qcache`. If the capture file is absent, `located` stays false and the counter prints `C3=FAIL` and exits 1 (`c3-count.py:60-68`). The URL literal is an identity key, not a re-open. Claims line 91: "No network re-open is part of this predicate." The code matches that sentence.

Imports of the four files, for the record: `absent-split.py` stdlib only (lines 28-36); `c2-count.py` stdlib only including `importlib.util` (lines 21-28); `c3-count.py` stdlib only (lines 16-22); `c1-count.py` adds `subprocess` (line 26) and nothing else network-shaped.

## Impacted axes

No axis fails on this attack.

- Operability: C1 executes a local interpreter on a local script. The script reads a local table, a local register, and a local cache. A missing capture exits 1. It does not become operable by fetching. Do not reject C1 for `subprocess` being outside the token list.
- Calibration: `ASSIGNED_HITS=0` is the right count for the four files. It is miscalibrated only if widened to the round-43 directory (`census-end.txt:2`) or if "no token" is treated as proof without the callee. The callee was read. The frozen sentence "No external fetch" (`claims.md:99`) still holds for this surface. Do not retune R43-SPLIT; the bound is not an egress parameter.
- Depth: C3's located-quote check is a local substring of the committed capture. The open fetch-scope ruling is respected by not re-opening. A URL in the counter is not an unreopened source. Do not reject the S078 adoption for the URL literal.

This is a tradeoff of the probe (five tokens, four files), not a fixable defect in the split or the adoption. The L1's per-axis verdicts must not reject the round on it.

## Smallest safe correction

None. Do not edit the counters, `absent-split.py`, the split table, the claims, or the bound.

If a later proof sentence is written, name the four files and the executed gate `tools/quarantine-check.py`, and exclude `corpus/evidence/round43/receipts/census-end.txt`. Do not add a network sandbox; that would be a new predicate, and it could harm the local cache read that C1 and C3 require.

## Not done

The three counters were not re-run here (other seats own those reruns). An unrun counter is not cited as PASS. Pacman was not touched. No tool was installed.

Report: .ufo/waves/round-43/w1/CritNoFetch.md

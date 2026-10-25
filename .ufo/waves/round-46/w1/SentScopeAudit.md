# SentScopeAudit — round 46 wave 1: scope and egress of the round's new code

item: audit `tools/inference-ground.py`, `corpus/evidence/round46/{c1,c2,c3}-count.py`
for egress and for writes outside declared scope; verify no new round-46 file writes
into `/home/vgpnk/Projects/shokuknow` or the fleet repo; judge whether the fixture
`spans.tsv` bogus digest can be mistaken for a real capture digest.
lane commit audited: `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`
scratch: `/tmp/chousa-r46-SentScopeAudit` (deleted at end). No lane file was modified.
No tool installed (nothing needed). No network call made.

## Verdict

- **Egress: none.** No socket/urllib/http/httpx/curl/wget in any of the five files or in
  `build-spans.py`. Imports are stdlib only: `argparse, json, pathlib, re, sys` (tool),
  `+ subprocess` (c1), `+ hashlib` (c3, build-spans).
- **Declared write scopes hold, with one exception:** the tool writes when given `--json`
  (F4). `c2`/`c3` are read-only; `c1` writes nothing and spawns only the tool (6 Popen,
  verified). `build-spans.py` writes only `corpus/evidence/round46/`.
- **Write boundary holds:** no round-46 file writes into shokuknow or the fleet repo.
- **Fixture digest is inert, not mistakable** once three checks are made (below), but
  nothing in-tree declares it bogus, so each reader must make them.
- **Two real gate forges found in the C1 counter** (F1, F2): `C1=PASS` is reachable with a
  tool that does nothing. These are the sharpest findings; neither is a scope/egress breach.
- **Post-audit state (observed 07:44, uncommitted):** `MutC1Junk` changed `c1-count.py:61` to
  `run(...) == 1` on the junk leg, closing F1 and F2 in the working tree. Re-verified against
  the working-tree file: deleted junk fixtures + always-exit-0 stub now score
  `JUNK_KILLED=0/3 C1=FAIL exit=1`. F3–F7 stand on unchanged bytes. Findings below are stated
  against the audited commit `c2f0e9d`.

## Hits, one row each

| file:line | hit | can egress? | can write outside scope? |
|---|---|---|---|
| `tools/inference-ground.py:225` | `Path(a.json).write_text(...)` | no | **yes** — arbitrary `--json` path, mode `w` (F4); unreached by c1 |
| `tools/inference-ground.py:216` | `(spans.parent / span_file).resolve()` then `read` | no | read-only, but **escapes the spans dir** (F3) |
| `corpus/evidence/round46/c1-count.py:26,39` | `import subprocess`; `subprocess.run([sys.executable, str(tool), ...])` | no (no socket) | no writes; exec target = `--tool` or `<root>/tools/inference-ground.py` |
| `…/c1-count.py:36-38` | `return 127` when a fixture is missing | no | no — but **127 scores as a kill** (F1) |
| `…/c1-count.py:61` | `sum(run(...) != 0 ...)` on junk | no | no — **any nonzero scores as a kill** (F2) |
| `…/c2-count.py:40` | `NAMED = (tools|corpus)/…\.(py|sh)` + `is_file()` | no | stat only, but path may escape root (F7) |
| `…/c3-count.py:39` | `CACHE = /home/vgpnk/Projects/shokuknow/.../.qcache` | no | read-only (`read_bytes`/`read_text`) |
| `…/c3-count.py:110-116` | `ev / span_file` then `read_text` | no | read-only, escapes via absolute span_file (F5) |
| `…/c3-count.py:120` | `int(offset)` unguarded | no | no — traceback exit 1 (F6) |
| `…/build-spans.py:113-116` | `mkdir` + `write_text` under `HERE` | no | **no** — `HERE` = `corpus/evidence/round46`; `--check` writes nothing |
| `.ufo/waves/round-46/gen-w1-spec.py:12,180` | writes `w1-spec.json` | no | no — lane `.ufo`, not the fleet `.ufo/state` |

## Findings

**F1 — medium — a deleted junk fixture scores as a kill (`c1-count.py:36-38`, `:61`).**
Exploit: `rm corpus/fixtures/inference-ground-r46/junk-*.md` + a 2-line always-exit-0 tool.
Evidence (fixtures copied to /tmp, lane files untouched):
```
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS   exit=0
```
Impact: claim C1's own kill rule ("a fixture set changed after this freeze fails the claim")
is enforced nowhere in code; the score survives with zero tool behaviour. Smallest fix:
`returncode == 1` required on the junk leg and 127/negative exit treated as an error leg, plus
a pinned fixture-set digest (current: `ebaf802a8dfc0c2b9afe155e59ec6e96fa5500d6433f16f946b6ba5da5800064`
over the 6 fixtures + `spans.tsv` + `counts.json` + 2 span files).

**F2 — medium — the junk leg accepts any nonzero exit (`c1-count.py:61`).**
The frozen predicate says junk fixtures must exit **1**. A stub exiting `0` on positives and
`2` otherwise scores `JUNK_KILLED=3/3 C1=PASS exit=0`. Same fix as F1 (`== 1`).

**F3 — medium — `span_file` path traversal makes the gate a read oracle (`inference-ground.py:216`).**
`spans.parent / "/abs/path"` is the absolute path; `..` likewise escapes. Evidence: a fixture
manifest row with `span_file=/tmp/chousa-r46-SentScopeAudit/outside.txt` holding the bullet's
quoted phrase → `GROUND: PASS exit=0` (unknown-to-fixture file grounds the claim). Read-only, so
the harm is a false PASS plus disclosure of any file the operator can read. Fix: refuse
absolute or `..` span_file and require `resolve()` under `spans.parent`.

**F4 — low — the tool writes an arbitrary path via `--json` (`:225`), against "tool: read-only".**
Evidence: audit hook `WRITE-OPEN /tmp/chousa-r46-SentScopeAudit/toolwrite.json w`; file created.
`c1-count.py:39-43` never passes `--json`, so the counter's use is write-free. Fix: delete the
flag, or restrict it under `root`.

**F5 — low — same traversal in `c3-count.py:110`** (`ev / span_file`, absolute wins:
`Path('/lane/corpus/evidence/round46') / '/etc/hostname'` → `'/etc/hostname'`). Read-only.

**F6 — low — malformed `offset` crashes instead of failing as usage (`c3-count.py:120`).**
Evidence (default mode, fake root, `offset=abc`): `ValueError: invalid literal for int()`,
exit 1, no `C3=` line printed. An exit-code-only wrapper reads a malformed manifest as
`C3=FAIL`. Fix: `try/except ValueError` → `return 2`.

**F7 — info — `c2` entry points are not confined to the repo (`c2-count.py:40,65`).** A claims
line naming `corpus/../outside.py` (existing file) yields `UNREGISTERED_PATH corpus/../outside.py`.
Stat-only; it makes the gate stricter, not weaker. No fix needed; worth naming. Related cosmetic:
`LANE = parents[3]` at import (`c1-count.py:29`) makes a relocated copy of the counter die with
`IndexError: 3`, so controls must run the lane copy with `--root`.

## Required checks

**No round-46 file writes into shokuknow or the fleet repo — holds.**
Audit-hook runs of `c2`, `c3 --lane-only`, `c3` (default, cache-reading) emitted **no**
`WRITE-OPEN` and **no** `EGRESS-OR-EXEC`; `c1` emitted exactly 6 `subprocess.Popen`, all
`/usr/bin/python3 <lane>/tools/inference-ground.py`. `build-spans.py` target is `HERE`
(`corpus/evidence/round46`); `gen-w1-spec.py` target is `<lane>/.ufo/waves/round-46/w1-spec.json`.
Grep of every round-46 file for `Projects/shokunin/` excluding the lane: **no match**.
External trees, read-only evidence:
- `.qcache` files newer than 2026-10-25 00:00: **0**; `5a631adb…` mtime 2026-10-23 20:36.
- shokuknow `MANIFEST.json` mtime 2026-10-24 23:33 (before round start 07:10 today). Its many
  `M` entries are campaign tooling drift, none dated today.
- fleet `.ufo/state/chousa.report-baseline` mtime 2026-10-25 07:10 = the hyaku runner; no
  round-46 script names that path.

**Fixture `spans.tsv` bogus digest — cannot be mistaken, if the reader checks three things.**
The digest is 64 zeros on all three rows, IDs `S901/S902`, URLs `https://example.invalid/…`.
A reader must:
1. know `0*64` is not the sha256 of any file (`sha256("") = e3b0c442…`), and the span files hash
   to `7c2aa3214d94…` / `c2184ca73ce4…`, not to zeros;
2. compute `sha256(url)[:24]` for the two URLs → `19917f015256597e63e5a09e`,
   `8bee599ab20f7ed3abaca472`; **neither exists in `.qcache`**, and `example.invalid` is RFC 2606
   reserved, so the digest is unverifiable by construction;
3. know that no verifier reads that column: `inference-ground.py:213` unpacks it as `_sha` and
   `c1-count.py` only passes the path, while `c3-count.py` reads a different manifest
   (`corpus/evidence/round46/spans.tsv`) — so the zeros are inert.
The real manifest is distinct on every axis: 11 rows, five distinct 64-hex digests, each equal to
`sha256` of its live cache file (S085 `e18eeb26…`, S086 `c508913a…`, S087 `dfc3e0f5…`, S088
`603f9b42…`, S089 `35bdf1c1…` — all matched). The zero digest occurs in no file under
`corpus/evidence/round46`. **Residual gap:** nothing in-tree (no fixture README, no docstring
line, no claims sentence) says the fixture digest is deliberately bogus; each reader must run
1–3 themselves. Smallest fix: one sentence in the fixture dir (e.g. `corpus/fixtures/inference-ground-r46/README.md`)
stating that `capture_sha256` is a placeholder and the URLs are `.invalid`.

## Observed, not findings

- `c2-count.py` at audit time: `ENTRY_POINTS=72 (tools=8 counters=50 named=70) REGISTERED=55/72
  UNREGISTERED=17` — the new tool is the 8th entry point, consistent with before=71.
- `c3-count.py` at audit time: `ENTRIES=2/2 CITES_BOUND=0/5 … CAPTURE_BOUND=11/11 C3=FAIL`,
  `REF_BOUND=2/2`; in-flight (registry/entry scribes still running), not judged here.

## Commands (decisive output only)

```
$ python3 c1-count.py --root /tmp/…/fake   # always-exit-0 stub, fixtures intact
TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=0/3 C1=FAIL   exit=1
$ python3 c1-count.py --root /tmp/…/fake   # same stub, junk-*.md deleted
TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS   exit=0
$ python3 c1-count.py --root /tmp/…/fake2  # stub: 0 on positive-*, 2 otherwise
TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS   exit=0
$ python3 tools/inference-ground.py --entry …/positive-a.md --spans …/spans.tsv …  # abs span_file
GROUND entry=… section=1 bullets=1 tokens=1 grounded=1 / GROUND: PASS   exit=0
$ python3 c3-count.py --root /tmp/…/fake4          # offset=abc
ValueError: invalid literal for int() with base 10: 'abc'            exit=1 (no C3= line)
$ python3 c2-count.py --root /tmp/…/fake5 --list   # claims names corpus/../outside.py
UNREGISTERED_PATH corpus/../outside.py / ENTRY_POINTS=2 (tools=1 counters=0 named=1)
$ sha256sum $CACHE/{5a63…,1c15…,7800…,b73f…,7876…}.txt   → equals the 11-row manifest digests
$ grep -rn 0{64} <lane>   → only corpus/fixtures/inference-ground-r46/spans.tsv (:2-4)
```
Nothing fetched; every read was an on-disk capture or a committed lane file.

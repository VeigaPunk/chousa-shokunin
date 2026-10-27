# R58ReviewToolingPolicy — C1 tool-install review (round 58, chousa lane)

Seat question: does the proposed C1 change (build-spans hazard battery,
`corpus/evidence/round58/c1-count.py` + hardened `tools/build-spans.py`) require
any tool install? Answer: **NO — no install is required.** Evidence below.

## 1. Policy read (required before any install; none performed)

Read `/home/vgpnk/.omp/agent/RULES.md` (operator tooling directive, 2026-10-19).
Exact operative lines:

- "Any agent — main session or subagent, any lane, any wave — installs or updates
  any tool that helps its task or is a strict upgrade, with full privilege,
  without asking first."
- Channel order: `sudo pacman -S --needed --noconfirm <pkg>` → `uv tool install
  <pkg>` → official release binary into `~/.local/bin` → `cargo install` / `npm -g`.
  Official sources only; never pipe an unverified remote script into a shell.
- "Record every install or update — tool, version, channel, reason — in your
  report or handoff."

Seat-brief overlay: pacman is paused host-wide (no pacman transactions), so if an
install were ever needed the first channel is unavailable and the fallback is
uv/npx/official binary, or an L0 file note. The RULES.md pre-install/read-and-record
gate therefore holds for this lane as: read RULES.md first, then install via
fallback channel, then record. **No step of this gate is triggered: zero installs
and zero updates were performed by this seat.**

## 2. Tool-surface inventory of the C1 change (all reads, frozen bytes)

Counter `corpus/evidence/round58/c1-count.py` (frozen, 406 lines):

```
$ grep -n '^import ' corpus/evidence/round58/c1-count.py
# lines 21-30: argparse hashlib os pathlib random shutil subprocess sys tempfile
```
All stdlib. Its only external processes (exact invocations, lines 95-102, 337,
364, 376):
- `[python, "-B", <builder>, --quotes .. --out .. --cache ..]` via `subprocess.run`
- `[sys.executable, "-B", .../c1-count.py, --builder <control>, ...]` (controls)
- optional `[args.python, "-B", tools/capture-text.py, corpus/captures/6dc68f….raw]`
Interpreter choice: line 166 `ap.add_argument("--python", default=sys.executable)`
— the same CPython running the counter; no interpreter download path exists.

Candidate `tools/build-spans.py` (lines 32-39):
`argparse hashlib importlib.util pathlib re sys` — stdlib only; the importlib use
loads lane `tools/capture-text.py` dynamically (lines 57-58). No subprocess, no pip.

Pinned r55 control `corpus/evidence/round58/controls/build-spans-r55.py`
(lines 34-39): same stdlib import set as the candidate.

`tools/capture-text.py` (lines 62-72): `argparse bisect posixpath urllib.parse
sys struct zipfile zlib xml.etree.ElementTree` — stdlib only; it parses the
committed capture itself (`struct`/`zipfile`/`zlib`). `urllib.parse` is URL
parsing, not fetching.

Controls generator `corpus/evidence/round58/controls/build-c1-controls.py`
(lines 3-4): `pathlib`, `subprocess` — stdlib only.

Network check (all five files):
```
$ grep -n 'urllib.request\|requests\|http.client\|socket' <counter> \
    tools/build-spans.py tools/capture-text.py \
    corpus/evidence/round58/controls/{build-spans-r55,build-c1-controls}.py
no network modules
```
No live fetch is possible from any C1 component — consistent with the lane's
no-fetch rule; nothing needs to be installed to keep it that way.

## 3. Host prerequisites — already satisfied

```
$ command -v python3 && python3 --version
/usr/bin/python3
Python 3.14.8
```
Language floor: `from __future__ import annotations` + builtin generics in
annotations (`dict[str, bytes]`, `list[tuple[str,str,str,str]]`) need CPython
≥ 3.9; 3.14.8 satisfies with headroom. Fixture legs needing FIFOs/devices/64 MiB
files use stdlib `os`/`pathlib`/`shutil` inside the `--work` scratch; subprocess
timeouts are in-process (`timeout=`), so no coreutils `timeout` dependency.
`uv` (`~/.local/bin/uv`) and `npx` exist on the host but are not referenced by
any C1 byte.

## 4. Pin integrity (presence, not fetch)

```
$ python3 -c "import hashlib,pathlib; b=pathlib.Path( \
  'corpus/evidence/round58/controls/build-spans-r55.py').read_bytes(); \
  print(hashlib.sha256(b).hexdigest())"
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
```
Equals frozen `R55_BUILDER_SHA` in the counter exactly. The control that must
FAIL the FOREIGN leg is committed in-lane; no download, hence no install surface.

## 5. Tooling risks considered and rejected (no-install status)

- OCR/`.doc` converter (antiword/libreoffice/`catdoc`): NOT required — the
  defined form is made by stdlib `capture-text.py` from the committed raw capture
  (`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`); no C1 leg touches a live .doc.
- `sha256sum`/`mkfifo`/`mknod` shell utilities: NOT required — hashing via
  `hashlib`, FIFOs via stdlib in-process.
- Newer Python: NOT required (≥3.9 floor met by 3.14.8).
- pacman transaction: NOT required by C1 and prohibited host-wide this round.

## 6. Not run / scope limits

- The counter itself was NOT executed by this seat (executor work); the no-install
  conclusion rests on static import/invocation analysis of the frozen bytes plus
  host `python3 --version`, all quoted above. An import-error at run time would
  be a defect finding, not an install need, since every import is stdlib.
- No scratch dir was created (no runnable probe needed); nothing to remove.
- No writes outside this report file; lane and fleet untouched; no git/jj mutation.

VERDICT: no-install — the proposed C1 change runs entirely on the host CPython
3.14.8 + stdlib with the committed r55 pin (sha verified); no prerequisite is
missing and RULES.md's install gate never triggers; survives.

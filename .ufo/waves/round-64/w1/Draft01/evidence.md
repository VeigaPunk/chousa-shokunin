# Draft01 local documentation evidence

Access date: 2026-10-30. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

## Executed commands and outcomes

1. Command (initial requested cwd `/fast/scratch/hyaku/chousa-r64/Draft01`):
   `mkdir -p /fast/scratch/hyaku/chousa-r64/Draft01 && cd /fast/scratch/hyaku/chousa-r64/Draft01 && python3 -VV; echo "rc_version=$?"; python3 -c 'import sys, pathlib; print("exe:", sys.executable); print("pathlib_file:", pathlib.__file__); print("resolve_doc_repr:", repr(pathlib.Path.resolve.__doc__))'; echo "rc_probe=$?"`
   Tool rejected before execution: `Working directory does not exist: /fast/scratch/hyaku/chousa-r64/Draft01`. No process exit code.
2. Initial pydoc command in the same absent cwd was also rejected before execution; no documentation output and no process exit code. Its proposed shell text was `python3 -m pydoc pathlib.Path.resolve 2>&1; echo "rc_resolve_pydoc=$?"; python3 -m pydoc pathlib.Path.parents 2>&1; echo "rc_parents_pydoc=$?"`.
3. Corrected command, cwd `/home/vgpnk/Projects/shokunin`:
   `mkdir -p /fast/scratch/hyaku/chousa-r64/Draft01 && cd /fast/scratch/hyaku/chousa-r64/Draft01 && python3 -VV && echo "rc_version=$?" && python3 -c 'import sys, pathlib; print("exe:", sys.executable); print("pathlib_file:", pathlib.__file__); print("version_info:", sys.version_info)'; echo "rc_probe=$?"`
   Output:
   ```text
   Python 3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]
   rc_version=0
   exe: /usr/bin/python3
   pathlib_file: /usr/lib/python3.14/pathlib/__init__.py
   version_info: sys.version_info(major=3, minor=14, micro=8, releaselevel='final', serial=0)
   rc_probe=0
   ```
4. A concurrent pydoc attempt, including `head -30`, was rejected because cwd validation raced the scratch creation. It did not run; no process exit code. Command: `python3 -m pydoc pathlib.Path.resolve 2>&1 | head -30; echo "rc_resolve_pydoc=${PIPESTATUS[0]}"; python3 -m pydoc pathlib.Path.parents 2>&1 | head -30; echo "rc_parents_pydoc=${PIPESTATUS[0]}"`.
5. Successful documentation command, cwd `/fast/scratch/hyaku/chousa-r64/Draft01`:
   `python3 -m pydoc pathlib.Path.resolve && python3 -m pydoc pathlib.Path.parents`
   Successful tool result (no explicit numeric exit printed); output:
   ```text
   Help on function resolve in pathlib.Path:

   pathlib.Path.resolve = resolve(self, strict=False)
       Make the path absolute, resolving all symlinks on the way and also
       normalizing it.

   Help on property in pathlib.Path:

   pathlib.Path.parents
       A sequence of this path's logical parents.
   ```

## Exact source locations opened with read

`/usr/lib/python3.14/pathlib/__init__.py:49-72,392-396,932-938`:

- Line 393: `"""A sequence of this path's logical parents."""` — quotation is 7 whitespace-delimited words.
- Lines 934–935: `Make the path absolute, resolving all symlinks on the way and also` / `normalizing it.` — quotation is 14 words; rendering joins the source newline with a space.
- Lines 71–72: `return self._path._from_parsed_parts(self._drv, self._root,` / `self._tail[:-idx - 1])`.
- Line 932: `def resolve(self, strict=False):`.
- Line 938: `return self.with_segments(os.path.realpath(self, strict=strict))`.

These are installed implementation docstrings and code, not a fetched HTML reference manual. No reference-manual installation was established. No behavior probe or claim counter was run.

## Context opened read-only

- `/home/vgpnk/.omp/agent/RULES.md`.
- Frozen round64 `corpus/evidence/round64/claims.md` (assignment pins freeze `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`; this seat read the working-tree file, not an independently extracted commit blob).
- Existing `corpus/knowledge/lane-root-derivation-r64.md`.
- `corpus/SOURCES.md` rows S150–S153: S150 already registers this installed source, with the same version and locators.

No tool installation/update, network access, clone, git/jj mutation, or production edit occurred.

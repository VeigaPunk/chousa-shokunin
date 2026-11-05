# R79ScoutA — the re-emission mechanism's behavioural risk surface

Seat: R79ScoutA (scout, leaf). Lane: chousa round 79, wave 1.
Scope: read-only reconnaissance of `corpus/evidence/round79/matrix-battery-v6.py`'s
copy mechanism. No production edits, no lane/fleet git or jj mutation, no commits.

Frozen predicate set read first: `corpus/evidence/round79/claims.md` (C1 operability,
C2 calibration). Frozen revision (controls commit) `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`;
base revision `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`. Frozen instruments were read only;
every mutation was done on copies under scratch.

All receipts cited below are copied into `.ufo/waves/round-79/w1/R79ScoutA/receipts/`.
Scratch was `$HYAKU_SCRATCH/chousa-r79/R79ScoutA` (`HYAKU_SCRATCH` unset →
`/fast/scratch/hyaku`), deleted before this report was written.

No frozen artefact was amended. One byproduct was created and removed: importing the
frozen battery through `importlib.util.spec_from_file_location` (as
`derivative-check.py` does) caused CPython to write
`corpus/evidence/round79/__pycache__/matrix-battery-v6.cpython-314.pyc` into the frozen
directory. It was a regenerable, `.gitignore`d bytecode cache (not a frozen artefact and
not a tracked file), and it was deleted immediately after the last probe; the frozen
directory is byte-identical to how it was found. The other `__pycache__` directories under
`corpus/evidence/round35`, `round47`, `round51` and `round52` predate this seat
(mtimes 2026-10-25/26) and were left alone.

Tooling: no tool was installed, upgraded or removed. Everything ran on the host's
`/usr/bin/python3` (CPython 3.14.8) and `git`; no `pacman`, `uv tool`, `npx` or
`~/.local/bin` transaction was made, so there is no tool/version/channel/reason row to
record. The pacman host-wide pause was therefore not engaged.

---

## 1. What the mechanism does (the surface under test)

`matrix-battery-v6.py:256-282` (`reemit`) never writes subject text. It:

1. `ast.parse`s the source (`:263`);
2. `_drop_docstrings(tree)` (`:265`, defined `:184-193`) removes every module/class/function
   docstring;
3. `_rename(tree)` (`:266`, defined `:203-253`) renames every bound identifier through a
   fresh per-copy table — `ast.Name`, `ast.arg`, `ast.FunctionDef`/`AsyncFunctionDef`/
   `ClassDef` names, `ExceptHandler.name`, `Global`/`Nonlocal` names, `MatchAs`/`MatchStar`
   names and `MatchMapping.rest` (`:234-252`);
4. inserts one random-named integer assignment at a random top-level position after the
   last `__future__` import (`:267-274`);
5. compiles the tree under a random file name (`:276`), marshals and base85-encodes it
   (`:277`);
6. writes a fixed 3-line wrapper (`:124-127`) into a fresh random directory under a
   random file name `subject.py` (`:278-281`).

The wrapper's whole body is:

```
exec(_m.loads(_b.b85decode({payload!r})), {{"__name__": "__main__", "__file__": __file__}})
```

Three properties of that line drive every finding below:

* the payload runs in a **fresh globals dict**, not in the wrapper module's namespace;
* the dict supplies exactly `__name__` and `__file__` — nothing else;
* `__name__` is hard-coded to `"__main__"`.

The rename exclusions are: builtins (`dir(builtins)`, `:211`), imported names
(`:213-218`) and **keyword-argument names** (`:219-220`). Dunders are exempt via
`old.startswith("__")` (`:226`). Nothing else is exempt.

---

## 2. The sweep

Subjects are the battery's own `POSITIVES` (`:83-84`) and `FORGERS` (`:86-96`) lists:
`corpus/evidence/round74/correction-count.py`, `corpus/evidence/round75/ref-counter.py`,
and the eleven `corpus/evidence/round76/forgers/forge-*.py`. Copies were made under
scratch and swept there.

Sweep commands (verbatim, also in `receipts/sweep-commands.sh`, transcript in
`receipts/sweep-transcript.txt`):

```sh
grep -nE '\b(getattr|setattr|hasattr|delattr|globals|locals|vars|eval|exec)\s*\(' *.py
grep -nE '^\s*(match|case)\b' *.py
grep -nE '__all__' *.py
grep -nE '\b(importlib|__import__)\b' *.py
grep -nE '^\s*(global|nonlocal)\b' *.py
grep -nE '__name__\s*==\s*["'"'"']__main__["'"'"']' *.py
grep -nE '^\s*@[A-Za-z_]' *.py
grep -nE '^\s*from\s+[A-Za-z0-9_.]+\s+import\s+\*' *.py
grep -nE '\*\*' *.py
grep -nE '__file__|sys\.argv' *.py
grep -nE '^\s*class\s|\bself\.' *.py
grep -nE '__doc__' *.py
```

The f-string `=` debug field needs an AST test, not a grep — `{expr=}` is a
`Constant` ending in `=` immediately followed by a `FormattedValue` whose `conversion`
is 114 (`repr`). The script in `receipts/sweep-commands.sh` runs exactly that; it
returns **zero** hits across all thirteen subjects. (A naive `grep -nE 'f"[^"]*\{[^}]*='`
produces false positives on ordinary f-strings such as
`f"C2=FAIL checks=6/7 rev={...}"` — the `=` is inside the literal text, not a debug
specifier. `receipts/hazard-run.txt` shows that false-positive class explicitly.)

---

## 3. Construct table

| Construct | file:line | covered by the battery's exclusions? | residual risk |
|---|---|---|---|
| `getattr(mod, "CASES", [])` — string-keyed lookup of a **module-level** name in an imported module | `corpus/evidence/round76/forgers/forge-harness-source.py:43` | **No.** The exclusion set (`:211-220`) covers builtins, import aliases and keyword-argument spellings. A string literal is none of those; `_rename` never rewrites `ast.Constant`. | **Live and material.** The key `"CASES"` names `loader-matrix-v3.py`'s module-level `CASES`, which `_rename` **does** rename (measured: `MODULE_LEVEL_ASSIGNMENTS after_rename = ['_01bc3590', …]` — `'CASES'` is gone, `receipts/cases-probe.txt`). If the matrix under test is itself re-emitted, F05's lookup returns `[]` instead of the table. Measured consequence below. |
| `importlib.util.spec_from_file_location` / `module_from_spec` / `exec_module` — importlib name lookup | `forge-harness-source.py:40-42` | Partly: `importlib` and `util` are import-alias exclusions (`:213-218`), so the *spelling* survives; but the imported module's own contents are re-emitted. | **Live.** Same coupling as the row above. |
| `__import__('os')` — string-keyed module import | `forge-harness-source.py:20` | No (it is a string literal, not an `ast.Import` node). | **None.** `os` is a stdlib module, not a subject binding; the rename cannot touch it. Measured: `harness-source` copy behaves identically (`receipts/subject-diff.txt`). |
| `match`/`case` bindings | **none in the 13 subjects** (sweep 2: `NO MATCH`) | n/a — but note `_rename` *does* handle `MatchAs`/`MatchStar`/`MatchMapping.rest` (`:245-252`). | **Low, but the handler is incomplete.** `MatchClass` keyword attributes are **not** renamed, so `case Point(x=1)` silently stops matching when `x` is a renamed class attribute. Measured on fixture `h34_matchclass_attr.py`: original prints `hit`, copy prints `miss` (`receipts/hazard-run5.txt`). A silent wrong answer, not an error. Not reachable from the 13 subjects. |
| f-string `=` debug field (`{expr=}`) | **none in the 13 subjects** (AST scan: zero hits) | n/a | **Low.** The debug text is a compile-time `Constant` and is **not** rewritten, so the copy still prints the *original* name: `COPY_CONSTANTS = ['__main__', 'v=']` (`receipts/fstring-leak.txt`). Behaviour is preserved (fixture `h17`: both print `v=3`), but the copy leaks the original identifier text into the payload — a fingerprint channel, not a behaviour change. |
| `__all__` string list | **none in the 13 subjects** (sweep 4: `NO MATCH`) | n/a | **Medium, if ever introduced.** `__all__` is a dunder so its *name* survives, but its *string contents* are constants and are not rewritten, while the functions they name are renamed. Measured: `star_probe` — original `STAR_NAMES = ['bar','foo']`; the re-emitted copy raises `AttributeError: module 'allmod_copy' has no attribute '__all__'` (`receipts/star-probe.txt`). |
| decorators resolved by name | **none in the 13 subjects** (sweep 8: `NO MATCH`) | n/a | **None at module level.** A decorator that is a plain module-level name is renamed *consistently* with its definition (both go through `name_for`), so `@deco` still binds (fixture `h08`: `SAME`, prints `42`). |
| `global` / `nonlocal` statements | **none in the 13 subjects** (sweep 6: `NO MATCH`) | n/a — `_rename` handles both (`:243-244`) | **None.** Fixtures `h06`/`h12`: `SAME`. |
| keyword argument whose name equals a renamed parameter | **none in the 13 subjects** (`receipts/attr-scan.txt` (b): `NONE` for all thirteen) | **Yes, by construction.** `_rename` excludes every `ast.keyword.arg` spelling (`:219-220`), and the exclusion is *module-global*, so a parameter spelled `count` is never renamed while `f(count=…)` is also never renamed. | **None for the 13 subjects.** The exclusion is global rather than per-call, which is over-broad but safe. Two residual hazards the exclusion does **not** cover: `**kwargs` splat (`h14`/`h36`: `TypeError: _c817218f() got an unexpected keyword argument 'count'` — the *dict key* is a runtime string, invisible to the AST) and a caller in a *different* module. Neither is reachable from the 13 subjects. |
| `if __name__ == "__main__"` | **all 13 subjects**: `correction-count.py:204`, `ref-counter.py:98`, `forge-constant-fail.py:21`, `forge-constant-pass.py:21`, `forge-diff-only.py:47`, `forge-hang.py:24`, `forge-harness-source.py:60`, `forge-naive-grep.py:41`, `forge-order-twelve.py:41`, `forge-seed-leak.py:47`, `forge-size-map.py:46`, `forge-subject-map.py:43`, `forge-tree-identity.py:36` | **Yes, decisively.** The wrapper hard-codes `{"__name__": "__main__"}` (`:126`), so the guard **fires in the copy exactly as in the source**. This is what makes the copy runnable at all. | **None for the 13 subjects — measured.** Differential run of all thirteen subjects, original vs re-emitted copy, same fixture lane, same argv: **14/14 identical** stdout and exit code, `SUMMARY same=14 differ=0` (`receipts/subject-diff.txt`). The `hang` forger timed out identically in both. |
| `__file__` / `sys.argv` | **none in the 13 subjects** (sweep 11: `NO MATCH`) | n/a | **None for the 13 subjects**, but the mechanism rebinds them anyway: the copy's `__file__` is the *wrapper's* path (`…/<hex>/subject.py`), not the source's (`receipts/deep-probe.txt` PROBE 3). The three ORACLE matrices *do* use `__file__` (`forge-order-matrix.py:30,34,45`; `-table.py:41,45,56`; `-block.py:42,46,57`) — see §4. |
| `__doc__` | **none in the 13 subjects** (sweep 13: `NO MATCH`) | n/a | **Medium for any re-emitted program that reads `__doc__`.** `_drop_docstrings` (`:265`) removes the docstring *and* the wrapper's globals dict has no `__doc__` key, so `__doc__` resolves to `builtins.__doc__` — measured: `DOC_IS_BUILTINS = True`, `IN_GLOBALS = False` (`receipts/doc-clean.txt`). A program using the battery's own idiom `description=__doc__.splitlines()[0]` (`matrix-battery-v6.py:328`, `loader-matrix-v3.py:192`) gets a *different description string*, not an error. Fixture `h27`: original raises `AttributeError: 'NoneType' object has no attribute 'splitlines'`, the copy **succeeds** (`Namespace(x='1')`) — `receipts/hazard-run3.txt`. |
| `globals()` / `locals()` / `eval()` / `exec()` with a string key | **none in the 13 subjects** (sweep 1 returns only `forge-harness-source.py:43`) | n/a | **High as a class, unreachable here.** The rename moves the binding out from under the string: `h02` `globals()["x"]` → `KeyError: 'x'`; `h13` `locals()["loc"]` → `KeyError: 'loc'`; `h09` `eval("val + 1")` → `NameError: name 'val' is not defined` (`receipts/hazard-run.txt`, `hazard-run2.txt`). Also `getattr(sys.modules[__name__], "VALUE")` → `AttributeError` (`h01`, `h19`), because the payload's globals are a *different* dict from `sys.modules["__main__"]` (`h29`: original `42`, copy `ABSENT` — a *silent* wrong value). |
| class attribute / method access on a renamed class | **none in the 13 subjects** (sweep 12: `NO MATCH`) | n/a | **High as a class, unreachable here.** `_rename` renames `ast.FunctionDef`/`ClassDef` names (`:239-240`) but **not** `ast.Attribute.attr`. So `Holder().show()` breaks: `h15`/`h26` → `AttributeError: '_4d30659c' object has no attribute 'show'`; `h30` (`@classmethod` + `C.make(count=4)`) → `AttributeError: type object '_64090227' has no attribute 'make'`; `h38` (dataclass field) → `AttributeError: '_2dd9f28c' object has no attribute 'count'` (`receipts/hazard-run2.txt`, `hazard-run3.txt`, `hazard-run5.txt`). Note `h38` also shows the keyword-argument exclusion cannot save a dataclass field. |
| `**kwargs` splat into a renamed parameter | **none in the 13 subjects** (sweep 10: `NO MATCH`) | **No** — a dict key is a runtime string. | **High as a class, unreachable here.** `h14`/`h36` → `TypeError: … got an unexpected keyword argument 'count'`. |
| `setattr`/`getattr` on an *instance* attribute | **none in the 13 subjects** | n/a | **None.** `h10`/`h31`: `SAME` — instance attribute names are not bound identifiers, so the rename cannot touch them. |
| `importlib.import_module("json")` (module name, not subject binding) | **none in the 13 subjects** | n/a | **None.** `h11`/`h28`: `SAME`. |
| `from X import *` | **none in the 13 subjects** (sweep 9: `NO MATCH`) | n/a | **High as a class, unreachable here.** `h22` → `NameError: name '_86a81c14' is not defined`: a star-imported name is an `ast.Name` with no `ast.Import` node to exclude it, so it is renamed and its binding is not. |
| `except E as e` handler name | n/a (no subject has one) | Handled by `_rename` (`:241-242`) | **None.** `h23`: `SAME`. |
| `from __future__ import annotations` | `correction-count.py:46` only | Handled: the random integer assignment is placed after the last `__future__` import (`:269-274`). | **None.** `correction-count.py` with `--selftest` and with `--lane/--rev/--base`: identical output both ways (`receipts/subject-diff.txt`). |

### Identifier-coverage statistics (`receipts/coverage.txt`, `receipts/exclusion-stats.txt`)

Across the 13 subjects: **347 bound identifiers, 226 renamed (65 %), 2 survivors whose only
reason for surviving is that their spelling is a keyword-argument name** — `text` in
`forge-naive-grep.py` and in `correction-count.py`, both from `subprocess.run(..., text=True)`.
Both are module-*local* variables, not module-level bindings, so their survival is
invisible in the payload's module namespace.

### The one live coupling, measured end to end

F05 `forge-harness-source.py` is the only subject with a string-keyed lookup. Its channel
has **two** halves and re-emission breaks **both** when it is applied to the matrix:

* **name half** — `forge-harness-source.py:25` selects the matrix by the substring
  `"matrix"` in the file name of the parent's cmdline. A re-emitted copy is named
  `subject.py`, so the substring is gone. Measured:
  `NAME-COUPLING original-name: MATRIX_FOUND = loader-matrix-v3.py` /
  `NAME-COUPLING re-emitted-name: MATRIX_FOUND = None` (`receipts/name-coupled.txt`).
* **string-key half** — `forge-harness-source.py:43` reads the matrix's module-level
  `CASES` by string. `_rename` renames that binding, so the key no longer resolves.
  Measured: `GETATTR_CASES -> []` for the re-emitted module
  (`receipts/name-coupled.txt`, `receipts/cases-probe.txt`).
* a third, structural consequence: importing a re-emitted module **executes its
  `__main__` guard**, because the wrapper hard-codes `__name__="__main__"`. So an
  importer of a re-emitted matrix gets the matrix's *output*, not its table:
  `IMPORT_RAISED_SystemExit 2` (`receipts/cases-probe.txt`,
  `receipts/systemexit-probe.txt`).

Observed behavioural consequence, run against the frozen battery (`receipts/matrix-leg-detail.txt`,
`receipts/f05-answers.txt`): with the **committed** matrix F05 answers each of the
twelve cases with a *mixture* of `actual_rc=0/1` and `failed=C2-1,…` — it is reading the
matrix's real case table and replaying it in declared order, so the per-run shuffle
desynchronises it. With the **re-emitted** matrix F05 answers **all twelve cases
`actual_rc=0 failed=none`** — it finds no matrix at all and degenerates into a
constant-PASS forger. The battery's own verdict is unchanged
(`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`, exit 0, in both
legs) because the *content* leg independently refuses a constant-PASS counter — but the
**marks** differ (`harness-source` marks 1/12 committed vs 4/12 re-emitted), so F05's
discrimination power against the *shuffled-order* leg is lost when the matrix is
re-emitted.

**This is a measured limit of the mechanism, not a falsification of C1.** C1's target
sentence is about the *textual* channel (no 40-byte window shared with the committed
source); the claims file already records the structure-identity channel as a separate,
wave-measured limit. This is a *third* channel: the re-emission also destroys
**name-coupled and string-key-coupled** discovery between a subject and its matrix. It is
reachable only if a battery re-emits the matrix under test; round 79's battery re-emits
the *subjects* (`:265-266` of the battery, in `reemit`) and the *oracles*
(`matrix-battery-v6.py:97-100` → `reemit(source, run)`), but runs the **legitimate**
matrix from its committed path (`:365`, `matrix = pathlib.Path(a.matrix)`). The
legitimate matrix is therefore never re-emitted in the round-79 battery, and F05's
coupling survives in the committed configuration — confirmed by the battery receipt
`receipts/battery-run_receipt.txt`, which shows `harness-source REJECTED` with
`marks=2/12` against the committed matrix.

### The `__file__` channel and the oracle state file

The three oracle matrices *do* use `__file__` (`forge-order-matrix.py:30,34,45` etc.) to
(a) refuse to run inside a git worktree and (b) place their `.state` file beside
themselves. Under re-emission `__file__` is rebound to the wrapper path, so both change:

* the in-worktree refusal **no longer fires** — measured: committed oracle exits 2 with
  `refusing to run inside the git worktree`, the re-emitted copy exits 0 and prints
  `LOADER_MATRIX=12/12 MATRIX=PASS`;
* the state file moves from `forgers/` to the copy's own directory, named
  `subject.state` instead of `forge-order-matrix.state` — measured in
  `receipts/oracle-state.txt`.

This is *why* the round-79 battery's oracle legs score as they do (the re-emitted oracle
runs where the committed one would refuse), and it is a **second**, independent
behavioural difference introduced by the mechanism. It does not affect the committed
leg, where the oracles are re-emitted into the battery's work directory anyway
(`matrix-battery-v6.py:392-394`).

### Structure-identity residual risk (the channel claims.md already names)

The copy is `base85(marshal(code))`, so a normalizer that unmarshals the payload and
canonicalises the fresh identifier table recovers the module's *structure*. Measured over
the 13 subjects (`receipts/structure-probe.txt`, `receipts/aggregate.txt`):

* **75.2 %** of each subject's original string literals (327/435) are present verbatim
  in the payload — these carry the semantic contract (check ids `C2-1`…, headings,
  file paths, the answer-key literals);
* only **18.1 %** of the identifier names in the payload are fresh (65/360); the rest are
  builtins, imported names and the kwarg-spelled survivors.

So the structure-identity channel recovers the contract even though the identifier table
is fresh — exactly the limit claims.md records as "measured by the wave".

The **textual** channel is closed: `python3 -B corpus/evidence/round79/derivative-check.py
--battery corpus/evidence/round79/matrix-battery-v6.py` prints
`DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` exit 0 (`receipts/deriv_receipt-v6.txt`); the
superseded v5 battery prints `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096` exit 1
(`receipts/deriv5_receipt-v5.txt`).

---

## 4. Instruments re-measured at the frozen revision (read-only, scratch work dirs)

| Command | Observed | Exit |
|---|---|---|
| `python3 -B corpus/evidence/round79/matrix-battery-v6.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work <scratch> --runs 1` | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`; `RECEIPT_LINES=113` (`receipts/battery-run_receipt.txt`) | 0 |
| `python3 -B corpus/evidence/round79/forge-battery.py --battery corpus/evidence/round79/matrix-battery-v6.py --work <scratch>` | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`; all six REFUSED/DETECTED, positive ACCEPTED (`receipts/forge-run_receipt.txt`) | 0 |
| `python3 -B corpus/evidence/round79/derivative-check.py --battery corpus/evidence/round79/matrix-battery-v6.py` | `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` (`receipts/deriv_receipt-v6.txt`) | 0 |
| `python3 -B corpus/evidence/round79/derivative-check.py --battery corpus/evidence/round78/matrix-battery-v5.py` | `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096` (`receipts/deriv5_receipt-v5.txt`) | 1 |

The battery's own SHA-256 read from the forge receipt is
`bb91406e9130d9a1960d99226c69380435fc933385db79e0e6ea6b5542a61e1d`, matching the
digest table in `claims.md`.

---

## 5. Findings, ranked

1. **The 13 subjects are behaviourally safe under re-emission.** All thirteen use
   `if __name__ == "__main__"`, the wrapper hard-codes `__name__="__main__"`, and the
   differential run over all thirteen (14 argv sets) is **14/14 identical** in stdout and
   exit code. No subject reads `__file__`, `sys.argv`, `__doc__`, `globals()`, `locals()`,
   `eval()`, `__all__`, `match`/`case`, `global`/`nonlocal`, a decorator, a star import,
   a `**` splat, or a class. The construct sweep found exactly one string-keyed lookup
   (`forge-harness-source.py:43`) and it reaches *across* modules into the matrix, not
   into the subject's own namespace.
   *Confidence: high — measured, not inferred.*

2. **The mechanism is not behaviour-preserving in general, in three specific ways.**
   (a) `ast.Attribute.attr` is not renamed while `FunctionDef`/`ClassDef` names are, so
   any method or class-attribute access breaks (`h15`, `h26`, `h30`, `h38`);
   (b) `globals()`/`locals()`/`eval()`/`exec()` string keys and `**kwargs` splat keys
   are invisible to the AST, so the binding moves out from under the string (`h02`,
   `h09`, `h13`, `h14`, `h36`) — and `h29` shows the `getattr(sys.modules[__name__], …)`
   variant fails *silently* to a wrong value rather than raising;
   (c) `__doc__` is dropped and then resolves to `builtins.__doc__` (`h27`,
   `doc-clean.txt`).
   *None of these is reachable from the 13 subjects.* They are the residual risk surface
   any future subject would enter, and they are the reason "re-emission preserves
   behaviour" is a claim about *these* thirteen, not about the mechanism.

3. **A third, previously unnamed channel: name-coupled and string-key-coupled discovery
   between a subject and its matrix is destroyed by re-emitting the matrix.** F05's
   two halves both break (`name-coupled.txt`), F05 degenerates from a mixed-answer forger
   to a constant-PASS forger, and the per-case marks move from 1/12 to 4/12
   (`f05-answers.txt`). The battery's overall verdict is unchanged (the content leg
   independently refuses a constant-PASS counter), so this is a **measured limit**, not a
   falsification of C1's textual sentence. It is unreachable in the committed round-79
   configuration because the legitimate matrix is run from its committed path, never
   re-emitted. *Confidence: high — measured with the frozen battery.*

4. **The oracle `__file__` channel changes under re-emission**: the in-worktree refusal
   stops firing and the state file relocates and is renamed (`subject.state`).
   *Confidence: high — measured.*

5. **The structure-identity channel recovers 75.2 % of the subjects' string literals
   verbatim**, including the semantic contract, while only 18.1 % of payload identifier
   names are fresh. This quantifies the limit claims.md already records for the wave.
   *Confidence: high — measured.*

6. **Two fingerprint channels that do not change behaviour but do leak the original
   identifier text**: the f-string `=` debug constant (`COPY_CONSTANTS = ['__main__',
   'v=']`) and the kwarg-spelled survivors `text` in two subjects. Neither is reachable
   from the 13 subjects' behaviour; both are visible in the payload.
   *Confidence: high — measured.*

---

## 6. Unresolved / not established

* Whether the name-coupled and string-key-coupled discovery channel (finding 3) is
  *intended* to be closed is not decidable from the frozen instruments: the round-79
  battery never re-emits the legitimate matrix, so the channel is exercised only in my
  synthetic leg. This is a **report**, not a repaired predicate — no frozen artefact was
  touched.
* The per-case `marks` differences in finding 3 are observed on single runs
  (`--runs 1`) against a per-run random permutation; the *direction* of the change
  (mixed answers → all-`actual_rc=0`) is deterministic from the mechanism, but the exact
  mark counts are seed-dependent.
* `lsp` was not available in this environment (`xd://lsp` → `No such tool`; the mounted
  device list contains no language-server device), so all symbol tracing here is
  literal `grep` plus Python `ast` inspection against the frozen sources, and every
  `file:line` above was confirmed by direct read of the file. No semantic claim in this
  report rests on grep output alone.
* Whether any *other* round-79 subject or oracle depends on the re-emitted copy's file
  name is not established beyond the two matrices named in §3 and §4; the 13 subjects were
  swept exhaustively for `__file__`/`sys.argv` and use neither.

---

## 7. Receipt index (all under `.ufo/waves/round-79/w1/R79ScoutA/receipts/`)

| File | What it shows |
|---|---|
| `sweep-commands.sh` | the sweep commands, verbatim |
| `sweep-transcript.txt` | their output over the 13 subjects |
| `subject-diff.txt` | original vs re-emitted for all 13 subjects: **14/14 identical** |
| `coverage.txt`, `exclusion-stats.txt` | identifier rename coverage per subject |
| `attr-scan.txt` | attribute-name / kwarg-collision / `**`-splat scan per subject |
| `hazard-run.txt` … `hazard-run5.txt` | 39 constructed fixtures, each run original vs re-emitted |
| `hazard-fixtures/` | those 39 fixtures |
| `deep-probe.txt` | `__doc__`, `__file__`, `sys.argv[0]` rebinding in the copy |
| `doc-clean.txt`, `doc-probe.txt` | `__doc__` → `builtins.__doc__` |
| `import-probe.txt`, `final-probe.txt`, `systemexit-probe.txt` | importing a re-emitted module fires its `__main__` guard |
| `name-coupled.txt` | F05's name half and string-key half, broken by re-emission |
| `cases-probe.txt` | `CASES` renamed away; the module-level table is gone |
| `f05-answers.txt` | F05's twelve per-case answers under each matrix |
| `matrix-leg-detail.txt` | the frozen battery run against committed vs re-emitted matrix |
| `matrix-reemit.txt` | matrix-side re-emission probe |
| `oracle-state.txt` | the oracle `__file__` / state-file / worktree-refusal channel |
| `structure-probe.txt`, `aggregate.txt` | structure-identity recovery: 75.2 % of strings, 18.1 % fresh names |
| `fstring-leak.txt` | the f-string `=` debug constant leak |
| `star-probe.txt` | `__all__` / star-import breakage |
| `ns-empty.txt` | the copy's module namespace is empty (`['_b','_m']`) |
| `battery-run_receipt.txt` | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| `forge-run_receipt.txt` | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` |
| `deriv_receipt-v6.txt`, `deriv5_receipt-v5.txt` | `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` vs `13/13 MAX_WINDOW=4096` |
| `tools/` | every script that produced the above |

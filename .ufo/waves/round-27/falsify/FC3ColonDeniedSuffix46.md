# FC3ColonDeniedSuffix46 — attack on C3 control `colon-denied-suffix`

- Target: `dd72641e574679c4f7882dd43de072b4c8892d6f` (lane `chousa-shokunin`, master).
- Sandbox: `/tmp/chousa-r27-falsify-FC3ColonDeniedSuffix46` (git archive of the target; no lane/git/jj edits).
- Gate under attack: `tools/research-gate.sh`, sandbox sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches assignment).
- Control: `corpus/evidence/round27-regressions.py:168-172`, fixture `<root>/synthetic:fixture.env`,
  expected rc2, `metadata registry refused: denylist`, zero lines matching `^RESEARCH_GATE: `.
- Production sites: `:595-617` (`is_denylist_path_value`, `is_denylist_fs_path`, `is_denylist_path`),
  `:2394/:2397/:2401` (registry `$path`/`$canon`/`$fdcanon`), `:1139/:1166` (claims), `:2609/:2616` (entry).
  Contract: `corpus/evidence/round27-claims.md:15`; design note `corpus/lessons/round-27.md:40` (R27-M6:
  "separate raw-filesystem predicate and citation wrapper").
- Environment per run: `CHOUSA_STRICT=0 LC_ALL=C`, cwd = fixture root, `timeout 30`; no installs.
- Command template: `bash <gate> verify-metadata <fx>/corpus/knowledge/entry.md --root <fx> --registry <path>`
  (claims/entry variants: `verify-claims <jsonl> --root <fx>`; `verify-metadata <entry-file> --root <fx>`).

## Verdict

The named control **HOLDS**: its core expectation is contract-grounded, it fails at base and fails under a
semantic revert of the targeted fix for the intended reason, and it is not vacuous. **But C3 as claimed is
FALSIFIED on its "not citation-anchor prefixes" clause** by same-class inputs where the landed gate refuses
clean complete paths, and the C3 control family is not fully contract-independent: one new control
(`legacy-env-anchor-refusal`) pins inherited prefix behavior that contradicts the claim's own wording.

## 1. Is the expectation derived from the declared contract, independent of gate code?

For the core assertion, yes. C3 says "no reading a denylisted synthetic path when a colon occurs earlier";
the complete path ends `.env`, which the *inherited* denylist already denies on colon-free names
(base gate refuses `plain.env`). The base gate on the exact fixture returns rc0 with one verdict, so the
expectation discriminates old from new behavior without reading the new code (table in §2). Exit 2 is
declared by the gate's own public contract (`Exit: 2 setup/usage`), and the diagnostic text is the refusal
string already present in the base gate (r26 D-controls). Those are conventions, not new-code circularity.

The independence failure is in the same C3 denylist block, not in the named control:

- `legacy-env-anchor-refusal` (`<root>/synthetic.env:1`, `round27-regressions.py:170`) **passes on the
  unmodified base gate** (rc2 denylist) and therefore is not a regression detector at all; it is a fence.
- A contract-faithful full-path predicate fails it (see §2), while still passing `colon-denied-suffix`,
  `colon-denied-component`, and every r26 D-class denial. So the C3 denylist expectations are jointly
  satisfiable only by keeping prefix matching for filesystem arguments — i.e. by contradicting the clause
  "inspect complete filesystem paths, not citation-anchor prefixes". This is implementation-derived, not
  contract-derived. The new gate selftest `metadata-colon-anchor-denylist-compat`
  (`tools/research-gate.sh:6492-6494`, file `metadata.env:1.md`) was introduced at the same commit and pins
  the same union; no such case exists at base (`git show 64eec5d:tools/research-gate.sh | grep 'env:1'` → none).

## 2. Mutation of the targeted production fix

Mutants (sandbox copies; only the named change differs):

| gate | sha256 | change |
|---|---|---|
| target | `ca39d14d…` | none |
| `gate-prefixonly.sh` | `c2124705…` | `is_denylist_fs_path` body reverted to `is_denylist_path_value "$(ptr_file_part "$f")"` (the pre-fix semantics) |
| `gate-fullonly.sh` | `28568bf0…` | `is_denylist_fs_path` = `is_denylist_path_value "$f"` (strict "complete path" reading) |
| `gate-rawsite.sh` | `532c5330…` | only registry `$path` arm reverted to `is_denylist_path "$path"`; `$canon`/`$fdcanon` unchanged |
| `base-gate.sh` | `c2c813f1…` | `git show 64eec5d:tools/research-gate.sh` |
| `base-fullpath.sh` | — | base gate with r26-M2 predicate (`f=$(norm_ptr "$1")`) |

Observe-style evaluation of the named control (exit==2, message present, `^RESEARCH_GATE: ` count==0):

- `gate-prefixonly.sh`: **FAIL** — `exit 0 != 2`; `missing 'metadata registry refused: denylist'`;
  `count '^RESEARCH_GATE: ': 1 != 0`. The fixture table is parsed and a CLEAN verdict is emitted: the
  intended reason, not a parse/setup error.
- `base-gate.sh`: **FAIL** identically (rc0, one verdict). The control is therefore discriminating.
- `gate-rawsite.sh`: **PASS** (the `$canon` / `/proc/$$/fd` arms still inspect the full path). The control
  asserts the outcome, not per-site defense in depth; the source-mechanism probe
  (`round27-mechanisms.py`) reports `C3_pointer_predicate_on_registry_path: 1` here.
- `round27-mechanisms.py gate-prefixonly.sh` reports **C3=0** even though the defect behavior returned:
  the mechanism probe is syntactic and misses a semantic revert inside the helper; the behavioral control
  is the only detector for this regression. (Consistent with the probe's own "not a verdict" disclaimer.)
- `gate-fullonly.sh`: named control **PASS**, `colon-denied-component` **PASS**; only
  `legacy-env-anchor-refusal` **FAIL** (`exit 0 != 2`, message missing, count 1 != 0).

Conclusion: the control does detect reversion of the specific production fix, for the right reason, and it
does not require the prefix arm that the strict contract reading removes.

## 3. Nearby same-class inputs where the landed gate is wrong

All fixtures are regular files with valid content; each complete path contains no denylist token. The
suffix after the colon is `notes.md`, not a citation anchor.

| surface | input (complete path) | target `ca39d14d…` | `gate-fullonly.sh` (strict contract) |
|---|---|---|---|
| registry | `<root>/reg.env:notes.md` (valid table) | rc2 `refused: denylist` | rc0 `RESEARCH_GATE: CLEAN` |
| entry | `<root>/e.env:notes.md` (valid entry) | rc1 `META_ENTRY_REFUSED … reason=denylist` | rc0 `verdict=clean` |
| claims | `<root>/src.env:notes.md` (contains the span) | rc1 `CLAIM_SOURCE_SESSION … path=…/src.env denied (not opened)`, `refused=1` | rc0 `supported=1` |

Denial at the landed gate comes solely from the prefix before the first colon ending in `.env`
(`tools/research-gate.sh:611` calls the prefix arm inside the filesystem predicate), while the complete
path is clean. Under the contract sentence and the anchor-aware reading of "preserve existing citation-pointer
semantics" (`x.env:1` may be a pointer; `x.env:notes.md` is not), these three refusals are wrong, across all
three surfaces the C3 fix touched. `base-fullpath.sh` (r26 M2) reproduces the same three accepts.

The union is also the *only* source of these refusals: with `gate-fullonly.sh`, every r26 D-class denial is
preserved (`op.env`, `secret.env`, `a:secret.env`, `server.token.md`, `b/Cookies`, `b/Login Data`,
`x/oauth/reg.md`, `x/credentials/reg.md`, `.config/reg.md`, `a:b/.config/reg.md`) plus both C3 colon
controls, and only `synthetic.env:1` and `synthetic.env:notes.md` flip to accept. No declared r26 denylist
case needs the prefix arm. Secondary asymmetry: `<root>/synthetic:secret.env:1` is read and yields a verdict
(rc0) while `<root>/synthetic.env:1` is refused — consistent with an anchor-aware rule, but proving the
landed predicate is not an "any `.env` component" check either; its boundary is first-colon position.

## Limits

- No `strace`/`/proc` inspection (bounds): "not opened" for the refusal path is inferred from control flow
  (`:2394-2397` denies before `exec {registry_fd}<"$canon"`), not observed.
- Only single gate invocations and sandbox mutants; the full `--selftest` and the 58-control regression
  script were not run (L1 owns those).
- Fixtures are synthetic temp files with fixed table/entry content; no host files, network, or live process.
- `en_US.UTF-8` locale availability not probed (not needed for this item); all runs used `LC_ALL=C`.

## Author-lane advice (not outside admission)

1. Split the filesystem predicate per R27-M6: `is_denylist_fs_path` should match the complete path only;
   keep prefix/pointer matching in `is_denylist_path`. If `path:line` pointer arguments must be refused for
   `--registry`/entry/claims sources, validate the anchor shape (`:<digits>`) explicitly before applying
   the pointer arm, so a real filename `x.env:notes.md` is read.
2. Add three independent controls: `clean-complete-path-after-env-prefix` expecting accept for registry,
   entry, and claims-source `x.env:notes.md`; `anchor-suffix-pointer-refusal` retaining denial for
   `x.env:1`; `non-anchor-suffix-after-env-prefix` accepting the same file. Cite the contract sentence in
   each, not the gate's current output.
3. Reclassify `legacy-env-anchor-refusal` and the `metadata-colon-anchor-denylist-compat` selftest: either
   cite the inherited-behavior clause they encode, or drop them; as written they force the union that C3
   says to remove, and the "58 independent controls" claim overstates independence.
4. Report the `.env`-prefix over-denial as inherited residual (base also refuses `x.env:notes.md`) rather
   than as repaired; the C3 sentence claims the opposite.

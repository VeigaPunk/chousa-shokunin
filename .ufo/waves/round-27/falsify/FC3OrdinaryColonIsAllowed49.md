# FC3 falsify — `ordinary-colon-is-allowed` (round27 attempt1)

Item: C3 control `ordinary-colon-is-allowed`, `corpus/evidence/round27-regressions.py:180-184`
(registry `ROOT/synthetic:ordinary.md`, well-formed table, expect exit 0 and exactly one
`^RESEARCH_GATE: ` line).

- Target: `dd72641e574679c4f7882dd43de072b4c8892d6f`; sandbox `git archive` at
  `/tmp/chousa-r27-falsify-OrdinaryColon`. Gate sha256
  `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (verified in the sandbox),
  regressions.py sha256 `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df`.
- Base for mutation comparison: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, gate sha256
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` (`git show` to a temp file,
  read-only; it is the same blob the r26 falsifier pinned).
- Tools: GNU bash 5.3.20, coreutils. No installs or updates. No full selftest and no full
  regressions.py run (L1 owns those); every result below is one gate command in the sandbox.

## Verdict

- **The control's assertion HOLDS**: no input was found where the landed gate refuses
  `ROOT/synthetic:ordinary.md` (rc 0, one verdict on landed, base and every mutant tried).
- **The control as C3 repair evidence is FALSIFIED (non-discriminating).** It passes on the base
  gate, on a mutant that reverts every `is_denylist_fs_path` call site to the pre-fix predicate,
  and on the literal full-path-only implementation of the C3 clause. It fails only for an
  over-broad "any colon is denied" implementation. It also cannot distinguish "the colon registry
  was read" from "the registry argument was ignored". The three sibling deny controls, not this
  one, carry the repair's discrimination.
- **A same-class input shows the landed gate still applies the citation-anchor-prefix arm to
  filesystem paths**, which C3 clause 1 disclaims: `--registry ROOT/notes.env:registry/table.md`
  (complete path clean, well-formed table) is refused `metadata registry refused: denylist`, and a
  claims source `corpus/notes.env:registry/f.md` (existing file, span present, complete path clean)
  gets a crit `CLAIM_SOURCE_SESSION` refusal. This is fail-closed over-refusal, not a read of
  protected bytes.
- **The control set and the C3 wording cannot both hold.** A full-path-only implementation of
  "inspect complete filesystem paths, not citation-anchor prefixes" keeps this control and the
  three deny controls green, but makes `legacy-env-anchor-refusal` (regressions.py:170) and the
  selftest case `metadata-colon-anchor-denylist-compat` (gate:6490-6493) fail.

## (1) Is the expectation derived from the declared contract, independent of gate code?

Partly. It is derived from the denylist *classes* (`*.env`, `.config/`, `.omp/`, …) plus the usage
interface (exit 2 for refusal, one `RESEARCH_GATE:` line per run): `synthetic:ordinary.md` contains
none of those classes, so a path-only denylist must accept it. It does not copy the changed
predicate, so it is independent of the repair's code shape.

But it is not independent of the *repair's input domain*, and it does not discriminate the
contract's actual question. The fixture sits exactly in the intersection of "allowed before the
fix" and "allowed after the fix": `ptr_file_part` yields `…/synthetic`, which misses every denylist
class, so both the base predicate and the landed predicate accept it (measured below). The
contract's operative clause is "filesystem-path denylist checks must inspect complete filesystem
paths, not citation-anchor prefixes"; the control exercises only the case where the complete path
*and* the pre-colon prefix are both clean, so it cannot distinguish "complete path inspected" from
"prefix inspected". Its comment "A colon in a normal pathname is not itself forbidden" is true
narrowly, but whether the colon path is accepted is decided by the pre-colon prefix, not the colon.

## (2) Mutation of the targeted production fix

Harness (sandbox only): same fixture and invocation as the control —
`cd ROOT && CHOUSA_STRICT=0 LC_ALL=C bash GATE verify-metadata corpus/knowledge/entry.md --root ROOT --registry ROOT/<path>`,
`ROOT=…/fx`, entry `source: S001`, `verified-at: 2026-01-02 checked synthetic fixture`,
`recheck: 90d`; registry `| id | status | used-by |` / `|---|---|---|` /
`| S001 | mined | corpus/knowledge/entry.md |`. Control passes iff rc 0 and exactly one
`^RESEARCH_GATE: ` line.

| gate | change | control `synthetic:ordinary.md` | `synthetic:fixture.env` | `synthetic:fixture/.config/registry.md` | `clean-alias.md -> .config` |
|---|---|---|---|---|---|
| landed `ca39d14d…` | — | rc 0, 1 verdict **PASS** | rc 2 denylist | rc 2 denylist | rc 2 denylist |
| base `c2c813f1…` | pre-fix | rc 0, 1 verdict **PASS** | rc 0 CLEAN | rc 0 CLEAN | rc 0 CLEAN |
| `mut/revert.sh` `251f272b…` | all 7 `is_denylist_fs_path` call sites (gate:646,1139,1166,2394,2401,2609,2616) → `is_denylist_path`; function body unused | rc 0, 1 verdict **PASS** | rc 0 CLEAN | rc 0 CLEAN | rc 0 CLEAN |
| `mut/fullonly.sh` `ad201501…` | `is_denylist_fs_path` = complete value only (`is_denylist_path_value "$(norm_ptr "$f")"`), prefix arm deleted — literal clause 1 | rc 0, 1 verdict **PASS** | rc 2 denylist | rc 2 denylist | rc 2 denylist |
| `mut/overbroad.sh` `727a528e…` | `is_denylist_path_value` denies any value containing `:` | rc 2 denylist **FAIL** | rc 2 | rc 2 | rc 2 |
| `mut/ignorerows.sh` `a34bbd39…` | `metadata_registry_check_source` returns 0 immediately (rows parsed but never consulted) | rc 0, 1 verdict **PASS** | rc 2 | rc 2 | rc 2 |

Answers:

- **Reverting the targeted fix does not make this control fail.** `mut/revert.sh` is behaviorally
  identical to base on nine fixtures (including this control and the three deny shapes) and the
  control still passes. The control is therefore not a regression guard for the C3 fs-path repair.
- The only mutation that fails it is the over-broad implementation, and it fails **for the intended
  reason**: rc 2 with `research-gate: metadata registry refused: denylist` and zero verdicts, not a
  parse or setup error. So the control is a genuine anti-over-reach guard, but that over-reach
  never existed at base.
- `mut/fullonly.sh` passes this control while breaking `legacy-env-anchor-refusal` (it returns
  rc 0 CLEAN where regressions.py:170 expects rc 2) and the selftest compat case
  (`metadata.env:1.md` becomes `verdict=clean` where gate:6492 expects `META_ENTRY_REFUSED`).
  The suite therefore *requires* the prefix arm on a filesystem path, i.e. it contradicts the
  literal C3 wording — while remaining blind to whether that arm exists at all.
- For contrast, the repair is discriminated by its siblings: `synthetic:fixture.env`,
  `synthetic:fixture/.config/registry.md` and the canonical alias all flip base rc 0 CLEAN →
  landed rc 2 denylist. My measurements agree with the shipped expectations for those three.

## (3) Nearby same-class inputs: where the gate is wrong, and where the control is vacuous

All fixtures synthetic under `/tmp/chousa-r27-falsify-OrdinaryColon/fx`; same invocation.

**(a) Complete path clean, pre-colon prefix denylisted — refused anyway.**

| input | landed | base | note |
|---|---|---|---|
| `--registry ROOT/notes.env:registry/table.md` (directory `notes.env:registry`, valid table) | rc 2 `metadata registry refused: denylist` | rc 2 denylist | complete path contains no denylist component/suffix; only the text before the first `:` ends in `.env` |
| `--registry ROOT/synthetic.env:notes` (regular file, valid table; `:notes` is not a line/heading anchor) | rc 2 denylist | rc 2 denylist | same arm |
| `--registry ROOT/synthetic.env-notes/table.md` (same bytes, no colon) | rc 0 CLEAN | rc 0 CLEAN | the colon is the only difference |

**(b) Same class on the claims surface — a false crit secrecy finding.**

- `{"id":"C1","source":"corpus/notes.env:registry/f.md","span":"alpha synthetic line","expect":"supported"}`,
  file exists in root with that content:
  landed rc 1, `FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims obs=id=C1 source=corpus/notes.env:registry/f.md obs=path=corpus/notes.env denied (not opened)`, DRIFT.
  Identical bytes at `corpus/notes.env-registry/f.md`: rc 0, `observed=supported … verdict=match`.
- Base gives the same refusal, so this is inherited prefix semantics, not introduced by r27. It is
  nonetheless the behavior C3 clause 1 says must not happen for filesystem paths, and it is a
  crit-labelled finding on a path that names nothing protected. Sibling reports
  `FC3ColonDeniedComponent45.md` and `FC3ClaimsLegacyEnvAnchorR57.md` already record the same
  over-refusal tradeoff for `ordinary.env:notes/registry.md` and `notes.env:2026.md`; this item
  adds the registry-directory case and the `:notes` non-anchor case.

**(c) The control is satisfied by a run that never consults the registry.** The assertion set is
rc 0 + one verdict. A run with **no** `--registry` at all produces exactly
`RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` (rc 0, one verdict), and
`mut/ignorerows.sh` passes the control unchanged. A queued row through the same colon path
(`| S001 | queued | - |`) does prove reading — landed rc 1
`FINDING META_SOURCE_NOT_MINED … source_id=S001` — and `ignorerows` turns that twin into rc 0
CLEAN. So a two-line companion control would close this gap; the shipped one does not.

**(d) Internal contradiction, measured.** Under `mut/fullonly.sh` (the literal clause-1 fix):
`legacy-env-anchor-refusal` input `ROOT/synthetic.env:1` → rc 0, 1 verdict CLEAN (shipped
expectation rc 2 + `metadata registry refused: denylist`), and entry `ROOT/metadata.env:1.md` →
rc 0 `verdict=clean` (shipped gate selftest expects `META_ENTRY_REFUSED`). So the control set is a
preservation guard for the prefix arm on fs paths, while C3 says fs-path checks use complete paths
"not citation-anchor prefixes". Either the claim text must be narrowed ("in addition to"), or the
prefix arm must move to the pointer surfaces and those two expectations must flip.

**(e) New refusal introduced by the landed full-path check (low, fail-closed).**
`--registry ROOT/a:b/.config/../reg.md` (canonical target `ROOT/a:b/reg.md`, clean, exists):
landed rc 2 denylist, base rc 0 CLEAN. The raw complete path names `.config/` before `..`, so
clause 1 read literally supports the refusal; canon-first reading does not. Recorded as a behavior
change, not as a defect.

No input was found where the landed gate *reads* a denylisted path by way of this control's class;
the raw/canon denylist check at gate:2394 precedes the open at gate:2396, and the claims refusal
checks at gate:1139/1166 precede their open. I did not use strace (forbidden here), so "not read"
is structural + message-based, not syscall-observed.

## Author-lane advice (not outside admission)

1. Do not cite `ordinary-colon-is-allowed` as evidence that the C3 fs-path repair is live; it
   passes at base and under a full revert of the repair. Keep it only as the anti-over-reach guard
   it actually is, or make it discriminating: a queued-row twin
   (`synthetic:ordinary.md` with `| S001 | queued | - |`, expect rc 1 `META_SOURCE_NOT_MINED`)
   proves the colon registry was read and costs two lines.
2. Resolve the wording conflict: either C3 says fs-path checks inspect the complete path **in
   addition to** retaining the legacy `path:line` prefix refusal, or `is_denylist_fs_path` drops
   its second arm and `legacy-env-anchor-refusal` plus `metadata-colon-anchor-denylist-compat` move
   to the pointer surfaces (`is_denylist_path`). As landed, the claim text and the control set
   cannot both be true, and the clause-1-only implementation fails the suite (measured above).
3. If the prefix arm is kept, expect over-refusal of clean complete paths whose pre-colon text ends
   in `.env` (`notes.env:registry/table.md`, claim source `corpus/notes.env:registry/f.md` →
   crit `CLAIM_SOURCE_SESSION`), and say so in the claim instead of "not citation-anchor prefixes".

## Limits

- Scoped to one control and the registry/entry/claims `--registry`/source surfaces. Chain, sweep
  and citation-pointer call sites were not exercised; other seats hold them.
- The `lsp` device was not available to this seat; symbol locations come from literal `grep` plus
  range reads of the cited lines, so they are text-located, not semantic proof.
- No strace/live-process inspection, no network, no host secrets; only synthetic fixtures under
  `/tmp`, and no lane production file was edited (report only).
- No full `--selftest`, no full regressions.py run, no build/lint. All mutants are sandbox copies,
  `bash -n` clean, and were exercised with single gate commands (each well under 120 s).

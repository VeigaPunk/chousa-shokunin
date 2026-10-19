# Root-slash boundary dead-arm (round 15)

source: tools/research-gate.sh (in_root helper ~:612; claim_source_path :1044-1075; ptr_resolves_meta :546-551; sweep_path_guarded :1750-1756); receipts: corpus/evidence/root-r15-20261019T152000Z-{demo,selftest,battery,drift}.log; queue entry closed: mount-alias-r14.md "Latent" bullet
verified-at: 2026-10-19 (round 15, landed; selftest PASS (110 cases, 0 skipped); gate sha dd0951d7…)
recheck: `bash tools/research-gate.sh --selftest` (cases 107–110 pin the healed arm); `CHOUSA_ROOT=/ bash tools/research-gate.sh verify-claims <abs-source>.jsonl`

## The dead arm

The gate decides "inside an allowed root?" by string-joining the resolved
root with a literal slash and a glob:

    root_r=$(cd -- "$ROOT" 2>/dev/null && pwd -P || …)   # "/" at --root /
    case "$canon" in "$root_r"/*) …                      # or [[ == "$root_r"/* ]]

At `--root /` the quoted `"$root_r"` contributes `/`, the literal `/` another,
and the unquoted `*` is the glob: the PATTERN STRING renders `//*`. A `*`
matches any string including `/`, but the two leading slashes are literal, and
every canonical path arrives single-slashed (`readlink -f` collapses `//x` →
`/x`). Every source falls to the else branch: `CLAIM_SOURCE_OUT_OF_CORPUS`
crit. The boundary never opens.

## Four outcomes at --root / (pre-fix, all measured)

| citation | outcome pre-fix |
|---|---|
| absolute, existing (`/etc/hostname`) | `OUT_OF_CORPUS` crit — false refusal |
| root-relative, existing (`etc/hostname`) | same refusal — `readlink -f` collapses the `//ROOT/$src` join to single-slash |
| absolute, absent (`/research/ghost.md`) | `OUT_OF_CORPUS` (mislabeled: should be MISSING) |
| relative, absent (`research/ghost.md`) | `MISSING` warn — the `//`-prefixed fallback canon accidentally matches `//*` |

Under `--root /` the gate degrades to lane-only resolution. The one surviving
MISSING arm is an artifact of the bug itself.

## The in_root contract (landed form)

    in_root() { local c=$1 r=${2%/}; [[ $c == "$r" || $c == "$r"/* ]]; }

- `${r%/}` strips `/`'s trailing slash to the empty string; `""/*` renders
  `/*`, which matches `/` itself (`*` matches empty) and every descendant.
  For any root ≠ `/` the strip is a no-op — behavior byte-identical.
- A materialized helper/local is mandatory: **inline `case "$canon" in
  "${root_r%/}"/*)` is still dead at root_r=/** (measured, bash 5.3.15 — a
  quoted `${var%/}` expansion that strips to empty quashes the trailing
  unquoted glob). The `[[ == ]]` inline form works, but the helper is the
  uniform landing.
- `src_root` keeps the ORIGINAL root (`/`): the device probe stats the
  declared root, per the r14 contract.
- The `== "$r"` arm is required so a source that canonically IS the root
  hits the boundary and then fails `-f` → `MISSING`, not `OUT_OF_CORPUS`.

## Three sites, one class

| site | form | pre-fix at root=/ |
|---|---|---|
| `claim_source_path` (~:1051-1055) | `[[ == "$root_r"/* ]]` + lane twin | every in-/ absolute source refused `OUT_OF_CORPUS` crit |
| `ptr_resolves_meta` (:546-551) | `case "$f" in "$root_r"/*)` | absolute verify pointers never resolve → `POINTER_UNRESOLVED` |
| `sweep_path_guarded` (:1741-1743) | `case … "$root_r"\|"$root_r"/*\|…)` | bare `/` arm admits only canon==`/`; every subdir glob refused |

The fix lands in all three via the same `in_root` helper.

## Named limits

- The inline-strip quirk is measured on bash 5.3.15 only; the assign-first
  helper is version-independent by construction.
- `--root //`: `cd //` + `pwd -P` prints `//`; `${root_r%/}` strips to `/` —
  normalized matching also repairs the double-slash spelling.
- With `root_r=/` the sweeps guard is vacuous by declaration (the whole
  filesystem is in-corpus); `sweep_glob_matches` can expand `/proc/*`-class
  globs unboundedly — a declared-root property, not a bug.
- TOCTOU, unmeasurable-stat, same-device binds, overlay roots: unchanged
  (mount-alias-r14.md); this round's class is the pattern arm only.
- `/etc/hostname` measured `9 1 31` (stat %s %h %d, content `plazir27`) on
  this host; selftest case 108 derives its span from the file's first line
  at case-build time.

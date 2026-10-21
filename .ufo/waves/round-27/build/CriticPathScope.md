# CriticPathScope — C3 complete-filesystem-path denylist (round 27 attempt 1)

Seat: `ChousaR27.CriticPathScope` (critic, leaf). Author-lane advice only; not a judge or admission.
Mode: read-only static analysis of base `64eec5d` `tools/research-gate.sh`. No gate, selftest,
build, lint, strace or /proc probe was run. No installs. When this was written, no executor patch
existed: `.ufo/waves/round-27/work/ExecRegistry` showed a clean `git status` at `64eec5d`, and
`patches/` was absent. So the attacks below target the fix shape that the claim and the r26 receipt
imply. They must be rechecked against the real patch.

Axes: calibration (primary), operability (refusal exit/message identity), freshness (none touched).

## Assigned item

C3 says: "Filesystem-path denylist checks must inspect complete filesystem paths, not citation-anchor
prefixes; preserve existing citation-pointer semantics" (`corpus/evidence/round27-claims.md:15`).
The receipt is `.ufo/waves/round-26/falsify/FRegistryRegistryDeny.md` (B1–B6, FRRD-2, M2).

## Code under attack (base 64eec5d)

- `:573-576` `ptr_file_part`: `${p%%:*}` after `norm_ptr` (`:567-571`) strips one leading and one
  trailing backtick. `:595-606` `is_denylist_path` globs against that prefix.
- Filesystem-path call sites, where the string is a real path that gets opened:
  - registry raw/canon at `:2375` and fdcanon at `:2382`;
  - entry raw/canon at `:2584` and fdcanon at `:2591`;
  - pointer canonical target at `:636` (`canon` = `readlink -f` output);
  - claim source at `:1129` (the whole `src` becomes `cand` at `:1146-1153` and is read).
- Citation-pointer call sites, where anchor semantics are correct: `:621`, `:650`, `:1598`.

## Counterexamples to the likely fix

### CX1 — a naive full-path swap weakens existing refusals (crit, hidden regression)

The suffix-anchored patterns `*op.env|*.env` (`:598`) are *not* monotone under full-path matching.
Take a synthetic registry file literally named `w/k.env:1` that holds a valid table:
- at base it is refused, because `ptr_file_part` gives `w/k.env`, which matches `*.env`;
- after a fix that only replaces `ptr_file_part` with the full path, `w/k.env:1` does not match
  `*.env`, so the file is opened, parsed and reports CLEAN.

The same applies to `w/a.env:x/reg.md` and to entries named `e.env:1.md` (the full path ends in
`.md`, while the base prefix `e.env` matched). This turns a refusal into a read. It breaks "never
disable a safeguard", and no existing selftest or r26 control would notice.
**Correction:** at every filesystem site, deny on the union of both checks:
`is_denylist_fs_path "$x" || is_denylist_path "$x"`. Refusal stays a superset of base.

### CX2 — fixing only the raw arm leaves the canon arm open (crit)

B4 from the r26 receipt is a symlink `plain.md -> a:b/.config/reg.md`. The raw path is clean, and
the canon `/…/a:b/.config/reg.md` is truncated to `/…/a`. Root-colon variant: the fixture root is
`$T/x:y/`, with `plain.md -> .config/reg.md` inside it. Its canon `$T/x:y/.config/reg.md` is
truncated to `$T/x`, so it bypasses even though no colon appears in the user-supplied path.
**Correction:** all three arms (raw, canon, fdcanon) need the full-path union, in the registry
*and* in the entries.

### CX3 — fixing the registry only leaves the entry reader open (crit, inherited FRRD-2)

`:2584/:2591` use the same helper. Entry `$T/a:b/.config/e.md` is parsed CLEAN at base (FRRD-2).
The claim sentence is gate-wide ("filesystem-path denylist checks"), so a registry-only patch claims
more than it fixes. The six arms are textually identical, so this costs 2 extra lines.

### CX4 — the pointer canonical arm (`:636`) truncates a filesystem path (warn, calibration)

Root `$T/r:1`, record pointer `lib/l.md`, with `lib/l.md -> ../.config/t.md` (in-root):
- `:621` checks the citation `lib/l.md`, which is clean;
- `:636` checks the canon `$T/r:1/.config/t.md`, truncated to `$T/r`, which is clean;
- `in_root` and `-f` both pass, so the pointer *resolves* and no `POINTER_UNRESOLVED` is emitted.

The r21 comment at `:615-616` promises the denylist "applies to the canonical target too". This is
existence only; no bytes are read.
**Correction:** at `:636`, use the union on `$canon`, and keep `:621` as the citation wrapper.

### CX5 — the claim source is a complete path but is checked as a citation (crit if in scope)

`claim_source_path` uses the whole `src` as the path (`:1146-1155`); it does not strip `:line`.
Its denylist check at `:1129` still truncates. A synthetic claims line
`{"source":"a:b/.config/t.md",…}` with `ROOT/a:b/.config/t.md` present passes `:1129` (prefix `a`),
is in-root and is read. This is exactly the claim's "reading a denylisted synthetic path when a colon
occurs earlier". The same applies to the verify-all declared claims file (`:2921`).

A second, separate, inherited gap: `claim_source_path` never checks `canon` against the denylist.
A symlink `lib/ok.md -> ../.config/t.md` (in-root) is read. Two authorities therefore disagree:
`ptr_resolves_meta` denies canonical targets, but the claim, chain and verify-all reader does not.

**Correction (smallest):** at `:1129`, use the union on `$src`, and add a union check on `$canon`
after `:1155`. Both should report `CLAIM_SOURCE_SESSION`.

Chain semantics stay intact. `chain_ref_file` (`:1596-1602`) strips anchors before calling, and
passes denylisted refs such as `x.env:12` through raw. The union keeps those refused as SESSION.
A full-path-only check would downgrade them to `CLAIM_SOURCE_MISSING` warn, which is CX1 again.

If L1 scopes CX5 out, the report must say so explicitly. It must not claim gate-wide complete-path
denial.

### CX6 — a global swap breaks citation semantics (crit if attempted)

The r26 diagnostic M2 (`norm_ptr` in place of `ptr_file_part` at `:596`) is not a fix. Pointer
`lib/x.md:op.env` (an anchor whose text looks like a file) would become `SESSION_READ` crit through
`:650`, where today it resolves to `lib/x.md`. The wrapper `is_denylist_path` MUST keep
`norm_ptr` + `${p%%:*}` for `:621/:650/:1598`.

## Identity and provenance hazards in the fix

- **Leave `fdcanon` unchanged.** It is also the used-by identity: it feeds
  `metadata_registry_entry_path` at `:2694`. Normalising it (stripping backticks, `norm_ptr`,
  trimming) would change used-by matching.
- **Do not run `norm_ptr` inside the filesystem helper.** It strips backticks, so the checked string
  would differ from the opened path. The union already covers the wrapper's behaviour.
- **Keep refusal identity.** Messages must stay exactly as they are:
  - registry: `metadata registry refused: denylist`, exit 2;
  - entries: `META_ENTRY_REFUSED … reason=denylist unparsed`;
  - claims: `CLAIM_SOURCE_SESSION` crit.

  Keep the `-e/-r/-f` order at `:2370-2372`, so an absent registry still reports `not found` (D17).
  The existence oracle is inherited FRRD-5; do not "fix" it here.
- **Engineering.** The new helper should take `$1` directly with no command substitution. The
  current `f=$(ptr_file_part …)` forks a subshell per call, and the fix should not add a second one.

## Suggested shape (author advice; not applied)

```bash
is_denylist_fs_path() { # complete filesystem path; no anchor or backtick stripping
  case "$1" in
    *op.env|*.env|*server.token*|*credentials/*|*/oauth/*) return 0 ;;
  esac
  [[ $1 == *chrome-profile* || $1 == *Cookies* || $1 == *"Login Data"* ]] && return 0
  [[ $1 == *'/.omp/'* || $1 == *'/.config/'* || $1 == *'/.local/state/'* ]] && return 0
  [[ $1 == '.omp/'* || $1 == '.config/'* || $1 == '.local/state/'* ]] && return 0
  return 1
}
is_denylist_path() { is_denylist_fs_path "$(ptr_file_part "$1")"; }  # citation pointers
deny_fs() { is_denylist_fs_path "$1" || is_denylist_path "$1"; }      # monotone vs base
```

Use `deny_fs` at `:2375` (both operands), `:2382`, `:2584` (both), `:2591`, `:636`, `:1129`, and at
a new canon check after `:1155`. One pattern list stays the single authority, so there is no
duplicate list.

## Synthetic controls to persist (temp dirs only; no strace or /proc reads by the harness)

The refusal message is set before `exec` for the raw and canon arms (`:2375-2377`, `:2584-2586`).
So `exit 2` + `refused: denylist`, with no `has no table` and no `RESEARCH_GATE:` line, proves the
file was not parsed. Pair each refusal with a non-table body; a read would then show up as
`has no table`.

1. Registry `a:b/.config/reg.md` → refused (B1).
2. Registry `a:secret.env` → refused (B2).
3. Registry `plain.md -> a:b/.config/reg.md` → refused (B4, canon arm).
4. Root `$T/x:y/`, registry `plain.md -> .config/reg.md` → refused (CX2, root-colon canon).
5. **Monotone guard:** registry `w/k.env:1` → still refused (CX1; it kills a full-path-only fix).
6. Entries `a:b/.config/e.md` and `alias.md -> a:b/.config/private.md` →
   `META_ENTRY_REFUSED reason=denylist` (CX3).
7. Pointer under root `$T/r:1`, `lib/l.md -> ../.config/t.md` → `POINTER_UNRESOLVED` (CX4).
8. Claims `source:"a:b/.config/t.md"` → `CLAIM_SOURCE_SESSION`; claims `source:"lib/ok.md"` with an
   in-root symlink to `.config/t.md` → `CLAIM_SOURCE_SESSION` (CX5, if in scope).
9. Citation preservation:
   - pointer `lib/x.md:12` still resolves;
   - pointer `lib/x.md:op.env` still resolves, not SESSION (CX6);
   - chain ref `x.env:12` is still CHAIN_SOURCE_SESSION;
   - a positive registry `reg.md` is CLEAN (P0).
10. Negative, do not invent: `a:.config/reg.md` (the directory is named `a:.config`, not `.config`)
    is **not** a denylist hit at base or after the fix. Expecting refusal would be an invented
    control.

### Mutation adequacy

Controls 1–4 and 6 kill a raw-only, registry-only or canon-less patch. Control 5 kills a
full-path-only patch. No black-box control isolates the fdcanon arm: raw and canon would need to be
clean while the opened fd's path is denylisted, which needs an open-time race. That arm can be
verified only by static review. It is a residual; do not claim it as tested.

## Inherited limits to report, not claim fixed

- FRRD-4: credential files outside the pattern list (`.ssh`, `.aws`, `.netrc`, …) are read. The
  denylist is pattern-scoped and not a protection of host secrets.
- FRRD-5: the existence oracle.
- Open-time races and bind/namespace aliases.
- `readlink` ` (deleted)` suffixes defeat `*.env` on fdcanon.
- Sweeps (`:2030-2066`) have no denylist arm; they list in-root names without reading content.

## Unrun checks (for L1)

None of the following was run by this seat:
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` (base + final);
- `bash tools/research-gate.sh --selftest` (`metadata-denylist-alias`, `ptr-deny-symlink`, cases
  129–132 and `metadata-stat-*` must stay green);
- `corpus/evidence/round26-registry-differential.sh` on an isolated copy.

Tools installed: none.

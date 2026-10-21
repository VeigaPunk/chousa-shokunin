# FC3EntryColonDeniedCanoni51 — `entry-colon-denied-canonical-alias`

Target: dd72641e574679c4f7882dd43de072b4c8892d6f, gate sha256 ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84 (re-hashed in sandbox: match).
Sandbox: /tmp/chousa-r27-falsify-FC3EntryColonDeniedCanoni51 (git archive of target). No installs. No full selftest or full regression run.

## Verdict

**HOLDS for the landed gate. The control is PARTIALLY VACUOUS against its own fix.**

- The landed gate refused every same-class input I tried: 15 refusal variants, all `reason=denylist`. It also allowed all 4 ordinary-colon inputs.
- The control fails for the intended reason only when both halves of the entry-reader fix are reverted, or when the shared helper is reverted. It still passes when either half is reverted alone.
- The post-open `fdcanon` half (gate line 2616) has a surviving mutant. With a deterministic swap between canonicalization and open, that mutant reads the denylisted colon path and reports CLEAN. The persisted control does not catch this, and I found no selftest that does either.
- Impacted axis: calibration, which is control strength, not the landed gate's behavior.

## (1) Is the expectation independent of the gate code?

Yes. The fixture is built independently: `entry-alias.md` is a symlink to `<tmp>/synthetic:fixture/.config/entry.md`. The expected results are exit 1, `META_ENTRY_REFUSED`, `source=refused`, and exactly one `^RESEARCH_GATE: ` record. These follow from two parts of the contract:

- C3: "no reading a denylisted synthetic path when a colon occurs earlier" and "inspect complete filesystem paths, not citation-anchor prefixes".
- The preserved r25 entry-refusal semantics (gate header line 35).

The control does not import gate predicates or code sets. It uses only the gate's public finding vocabulary.

Precision weakness: the control never asserts `reason=denylist`. All six refusal reasons emit both required strings: denylist, unreadable, stat, multilink, size, and nul/read. A refusal for the wrong reason would therefore pass. The selftest analogue (`metadata-entry-colon-denylist`, line 6485) does pin the full `reason=denylist` finding line.

## (2) Mutation evidence

I wrote a single-case replica of the control in `probe.py` in the sandbox. It uses the same environment (`CHOUSA_*` stripped, `CHOUSA_STRICT=0`, `LC_ALL=C`), the same entry text, the same fixture, and the same assertions. Each command was `timeout 120 python3 probe.py <gate>`, and each exited 0.

| mutant | change (sandbox copy only) | control |
|---|---|---|
| landed | — | PASS: rc=1, reason=denylist |
| M1 | line 2609: `is_denylist_fs_path` → `is_denylist_path` (file and canon) | **PASS (survives)**: the `fdcanon` check backstops it |
| M2 | line 2616: `fdcanon` check → `is_denylist_path` | **PASS (survives)**: the line-2609 canon check backstops it |
| M3 | M1 and M2 together (base-equivalent entry reader) | FAIL: `exit 0!=1; missing META_ENTRY_REFUSED; missing source=refused`. This is the intended semantic failure, not a setup error. The entry was parsed: `source=present ... verdict=clean`. |
| M5 | helper `is_denylist_fs_path` reduced to the `ptr_file_part` check only | FAIL, for the same intended reason as M3 |
| M4 | overbroad: also refuse any canonical path containing `:` | **PASS (survives the control)** |

M4 is killed only by the selftest case `metadata-ordinary-colon-allowed` (line 6498). In my replica, `raw:ordinary.md` gives rc=1 reason=denylist under M4. The regression script's only ordinary-colon positive case is on the registry side (`ordinary-colon-is-allowed`). Every regression-script entry path is colon-free. [INFERENCE] M4 would therefore pass all 58 regression controls; I did not run the whole script, per the bounds.

### Minimal counterexample: M2 survives, and the landed gate is correct

`race.sh` adds a PATH shim for `readlink`, following the same pattern as the selftest's `stat` shims at lines 5926 and 5956.

- For the alias argument only, the shim prints a clean canonical name, `<w>/clean-name.md`. That name is itself a symlink to `<w>/synthetic:fixture/.config/entry.md`.
- Every other call goes to the real `readlink`, including the gate's `/proc/$$/fd` lookup.

This deterministically simulates a swap between the canon `readlink` and the open.

Each command was `timeout 120 bash race.sh <gate>`:

```
landed  rc=1  FINDING META_ENTRY_REFUSED ... obs=entry=entry-alias.md reason=denylist unparsed
M1      rc=1  ... reason=denylist unparsed
M2      rc=0  META entry=entry-alias.md source=present verified_at=dated recheck=scheduled verdict=clean
              RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
M3      rc=0  ... verdict=clean / RESEARCH_GATE: CLEAN
```

Under M2, the gate reads and parses a denylisted path that has a colon earlier in it. That is exactly the C3 prohibition, and `entry-colon-denied-canonical-alias` still passes under M2.

On coverage elsewhere: a grep of the selftest finds only the `stat`-swap race (`metadata-stable-object`). That race fires after the `fdcanon` check, so it tests snapshot binding, and it uses a colon-free `credentials/` path. So I found no selftest pinning the colon-class `fdcanon` change. [INFERENCE] I did not run the full selftest.

M1 is effectively equivalent. Without a race, the `fdcanon` check sees the same object. Preflight (`-f`/`-r` on the user path, lines 2570–2591) blocks the FIFO and mode-000 targets that would make an early open observable.

## (3) Same-class probes against the landed gate (`probe.py`)

Every canonical target below has a colon before a denied component. All gave rc=1 with `reason=denylist`:

- the exact replica
- relative symlink
- two-hop symlink chain
- symlinked directory component (`cfglink` → `synthetic:fixture/.config`)
- directory mode (`verify-metadata DIR` containing the alias)
- `synthetic:fixture/{credentials,.omp,.local/state,oauth,chrome-profile}/entry.md`
- `synthetic:fixture/op.env` and `synthetic:fixture.env` as non-`.md` targets behind a `.md` alias
- `synthetic:a/b:c/.config/entry.md` (multiple colons)
- a component containing a newline before the colon (`synthetic\n:fixture/.config/entry.md`)

Allowed, with rc=0 and verdict=clean, as the contract requires:

- an alias to `synthetic:ordinary/entry.md`
- a colon in the alias name pointing at a plain target (`a:b.md`)
- a raw `raw:ordinary.md`
- an alias to `synthetic:fixture/.config-adjacent/entry.md`

An alias to `x:.config/entry.md` was also allowed. I first marked this "deny", but that was my mistake: the component is literally `x:.config`, not `.config`. Under complete-filesystem-path semantics, allowing it is correct and consistent with the base behavior, so it is not a counterexample.

No landed-gate counterexample was found.

## Smallest safe correction (advice to the author lane)

1. Add a regression control in the colon class that pins the `fdcanon` half, for example the `race.sh` readlink-shim fixture. Expect rc=1 and `reason=denylist unparsed`. It fails under M2 and passes on the landed gate.
2. Make this control require `reason=denylist`, not just `META_ENTRY_REFUSED` and `source=refused`.
3. Optionally, add an entry-side ordinary-colon positive control so the regression suite catches M4 by itself rather than relying only on the selftest.

None of these change the gate.

## Limits

- Leaf-local synthetic fixtures only.
- The race is simulated with a PATH shim, not a real concurrent swap.
- The full selftest and the full regression script were not run, per the bounds; claims about their coverage are grep-based [INFERENCE].
- The gate's own `/proc/$$/fd` use was exercised only indirectly; I did not inspect `/proc` directly.
- No installs.

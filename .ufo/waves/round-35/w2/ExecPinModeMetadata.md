# ExecPinModeMetadata — round-35 w2, `verify-metadata` under the grep pin

Lane: chousa. Wave: round-35 v2 (`chousa-r35-w2`). Seat: executor (leaf, no
subagents). Axes: operability, calibration.

## Verdict (one line)

`verify-metadata --registry corpus/SOURCES.md --as-of 2026-10-23` behaves
**identically under all four pin environments** (exit 1, byte-identical stdout,
tripwire empty, refusals exit 2 with empty stdout) — the pin covers this mode
correctly — **but the pin's own third resolution step is dead code**, so on a
host whose GNU grep is not at `/usr/bin/grep` or `/bin/grep` the landed gate
refuses to run at all where the pre-pin base gate ran fine. That is a real
operability regression introduced by the C1 repair, and it is invisible to the
C1 counter.

---

## 1. What was measured, and against what

Gate under test (sha256, full):

```
1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
  /tmp/hyaku/chousa-r35/w2/ExecPinModeMetadata/clone/tools/research-gate.sh
```

The clone is at wave base revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`
(`git -C clone rev-parse HEAD` → `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`),
so the clone's gate is byte-identical to the landed gate.

Registries used (both read-only, never edited):

| registry | sha256 | where |
|---|---|---|
| committed at wave base | `3281259a49ffd2dd3e95b1924d494db4229fb499d90991ff7aaea10ea08c18ab` | `clone/corpus/SOURCES.md` (= `git show HEAD:corpus/SOURCES.md`, identical) |
| live worktree | `54bf6cc800ad3d958cfa4bf274aa852991be69e17d3095594c2337d4b19f0bf2` | `/home/.../chousa-shokunin/corpus/SOURCES.md` |

**Caveat, stated because it affects any receipt taken now:** the live
`corpus/SOURCES.md` changed *during* this wave (mtime 17:00, worktree copy
`54bf6cc8…` vs committed `3281259a…`; `git status` shows ` M corpus/SOURCES.md`
and 2 extra `corpus/knowledge/*.md` files: `grep-pin-r35.md`,
`keyed-engine-output-equivalence-r35.md`, `bash-local-expansion-r35.md`). The
C1 counter (`corpus/evidence/round35/c1-count.py`) pins the **gate** sha but not
the registry/metadata bytes, so metadata-mode counts are only reproducible
against a stated registry sha. All numbers below name their registry sha.

Command form used throughout (root = the tree owning the registry):

```
bash tools/research-gate.sh verify-metadata corpus/knowledge \
     --root <ROOT> --registry <REGISTRY> --as-of 2026-10-23
```

`corpus/knowledge` is the metadata population (41 `.md` files at wave base,
44 in the live worktree). Harness: `/tmp/hyaku/chousa-r35/w2/ExecPinModeMetadata/harness{,2,3,4,5,6,7}.sh`;
receipts in `/tmp/hyaku/chousa-r35/w2/ExecPinModeMetadata/out/`.

---

## 2. The four environments (wave base clone, registry `3281259a…`)

`harness5.sh`, output verbatim:

```
PINNED RECEIPTS (gate=1f2fb4f522d9a670  registry=3281259a49ffd2dd  rev=e87c5d7ea2dbf3730b36a3961de3f06261d015e4)
clean            rc=1   trip_path=0   trip_fn=0   stdout_bytes=12638  META_lines=41  verdict_lines=1  METADATA_COMPLETE=37/41 | RESEARCH_GATE: DRIFT (entries=41 complete=37 findings=61 drift=6)
shim             rc=1   trip_path=0   trip_fn=0   stdout_bytes=12638  META_lines=41  verdict_lines=1  METADATA_COMPLETE=37/41 | RESEARCH_GATE: DRIFT (entries=41 complete=37 findings=61 drift=6)
override         rc=1   trip_path=0   trip_fn=0   stdout_bytes=12638  META_lines=41  verdict_lines=1  METADATA_COMPLETE=37/41 | RESEARCH_GATE: DRIFT (entries=41 complete=37 findings=61 drift=6)
echo             rc=1   trip_path=0   trip_fn=0   stdout_bytes=12638  META_lines=41  verdict_lines=1  METADATA_COMPLETE=37/41 | RESEARCH_GATE: DRIFT (entries=41 complete=37 findings=61 drift=6)
bashenv          rc=1   trip_path=0   trip_fn=0   stdout_bytes=12638  META_lines=41  verdict_lines=1  METADATA_COMPLETE=37/41 | RESEARCH_GATE: DRIFT (entries=41 complete=37 findings=61 drift=6)
```

Environments: (a) clean `PATH=/usr/local/bin:/usr/bin:/bin`; (b) a logging
`grep` shim first on `PATH`; (c) `RESEARCH_GATE_GREP=/usr/bin/grep` **plus** the
shim; (d) `CHOUSA_GREP_PIN_ECHO=1`. A fifth, `BASH_ENV` function shim, was added
because it is the other interception vector the round-34 closure measured.

* **Exit**: 1 (DRIFT) in all five. 1 is the mode's own verdict on this
  population, not a pin artifact — `META_RECHECK_ABSENT` ×4 and
  `META_VERIFIED_AT_ABSENT` ×1 are warn-severity and always drift.
* **Counts**: `METADATA_COMPLETE=37/41`; `RESEARCH_GATE: DRIFT (entries=41
  complete=37 findings=61 drift=6)`; 41 `META entry=` lines (37 `verdict=clean`,
  4 `verdict=drift`); exactly 1 `RESEARCH_GATE:` verdict line. Finding census
  (clean): `META_RECHECK_ABSENT` 4, `META_RECHECK_ROOT_PARENT` 9,
  `META_RECHECK_UNSCHEDULED` 21, `META_SOURCE_ABSENT` 1,
  `META_SOURCE_NO_ROW_ID` 25, `META_VERIFIED_AT_ABSENT` 1.
* **Tripwire**: **empty in every environment** (`trip_path=0`, `trip_fn=0`).
* **stdout identity**: `IDENTICAL(normalized) clean vs shim`, `clean vs
  override`, `clean vs echo`, `clean vs bashenv`. Normalization strips only the
  `ts=` field of the banner line; stdout is otherwise byte-identical
  (12638 bytes each). The `CHOUSA_GREP_PIN_ECHO=1` run adds exactly one stderr
  line and nothing to stdout: `GATE_GREP: path=/usr/bin/grep source=default
  version="grep (GNU grep) 3.12-modified"`.
* **Live worktree cross-check** (`harness final.sh`, registry `54bf6cc8…`,
  44 entries): all four environments give `rc=1`, `METADATA_COMPLETE=37/44`,
  `RESEARCH_GATE: DRIFT (entries=44 complete=37 findings=73 drift=15)`, tripwire
  empty. Same conclusion on the moving tree.

### Refusals (all three classes)

```
refuse-rel       rc=2  stdout_bytes=0  stderr: research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)
refuse-nongnu    rc=2  stdout_bytes=0  stderr: research-gate: GREP_PROVENANCE refused: override does not report GNU grep: <no version> (candidate=…/out/stub-grep)
refuse-missing   rc=2  stdout_bytes=0  stderr: research-gate: GREP_PROVENANCE refused: override is not a regular file (candidate=…/out/absent-grep)
```

stdout is **0 bytes** in every refusal case (no `META entry=` line, no
`RESEARCH_GATE:` line): the refusal happens before any record is read, as
claimed. Refusal text matches the claimed form
`research-gate: GREP_PROVENANCE refused: …`.

---

## 3. Scope: does this mode even use grep?

Yes, but only through one call site, and only with `--registry`:

* With `--registry`, the mode makes **81 grep calls through the pinned binary**
  (`census.sh`, logging override wrapper): 41 × `-oE [[:alnum:]_]+` and 40 × `-xE
  S[0-9]{3,}`. These are the registry source-id scanner in
  `metadata_registry_check_source` (`tools/research-gate.sh:3144` and `:3146`).
* **Without `--registry`, the mode makes 0 grep calls** (`A2-no-registry
  rc=1 pinned_calls=0`, same `METADATA_COMPLETE=37/44`). The header screen
  (`source:` / `verified-at:` / `recheck:`) is pure bash. So the pin's reach in
  this mode is exactly the registry scanner, and nothing else. Any claim that
  the pin covers "the metadata mode" must be read as "the metadata mode's
  registry scanner".

---

## 4. Before/after control: the base gate IS intercepted, and it is invisible

Same live tree, same registry `54bf6cc8…`, base gate
`.ufo/waves/round-35/repairs/base-gate.sh`
(`a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`):

```
B-shim      rc=1  trip_path=1392  METADATA_COMPLETE=37/44 | RESEARCH_GATE: DRIFT (entries=44 complete=37 findings=73 drift=15)
              shim log: 44 × "-oE [[:alnum:]_]+", 40 × "-xE S[0-9]{3,}"
B-bashenv   rc=1  trip_fn=1644    METADATA_COMPLETE=37/44 | RESEARCH_GATE: DRIFT (entries=44 complete=37 findings=73 drift=15)
```

The base gate **executes the PATH shim 84 times** and the `BASH_ENV` function
84 times, and its stdout is **byte-identical** to the landed gate's clean run
(verified by `diff` on the ts-normalized streams: `IDENTICAL`). The
substitution is invisible to output alone — exactly the round-34 finding, now
reproduced on the metadata mode. The landed gate's tripwire is empty in the
same environments. That is the pin doing its job.

Second before/after contrast, same clone and registry `3281259a…`: with a
`PATH` that contains 38 tools but **no grep at all**,

```
D1-landed-nogrep  rc=1  METADATA_COMPLETE=37/41 | DRIFT (entries=41 complete=37 findings=61 drift=6)
D2-base-nogrep    rc=1  METADATA_COMPLETE=37/41 | DRIFT (entries=41 complete=37 findings=77 drift=47)
                   + 84× "base-gate.sh: line 3069: grep: command not found"
                   finding census: META_SOURCE_SCAN_FAILED 41 (crit)
```

So on this mode the pre-pin gate produced 41 `META_SOURCE_SCAN_FAILED` crit
findings (registry relationships unknown) where the landed gate produces the
real registry verdict (25 `META_SOURCE_NO_ROW_ID`). The pin is not cosmetic
here.

---

## 5. FINDING — the pin's third resolution step is dead code (operability regression)

`tools/research-gate.sh:384-393`:

```bash
    for c in /usr/bin/grep /bin/grep; do
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    if [[ -z $cand ]]; then
      c=$(command -v grep 2>/dev/null || true)
      case "$c" in
        /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
      esac
    fi
    [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
```

The gate defines a shell **function** named `grep` at line 351
(`grep() { command "$GREP_BIN" "$@"; }`) before `grep_pin_init` runs. Inside
that shell, `command -v grep` reports the **function**, not a path:

```
$ bash -c 'grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep 2>/dev/null || true); printf "[%s]\n" "$c"'
[grep]
```

`"grep"` does not match `/*)`, so the third candidate is **always dropped**.
The step is unreachable, not merely rare. (`type -P grep` returns
`/usr/bin/grep` in the same shell — the correct incantation.)

### Proof, on the UNPATCHED landed gate

`harness6.sh` / `harness7.sh`: a user+mount namespace in which `/bin/false` is
bind-mounted over `/usr/bin/grep` (so `/usr/bin/grep` and `/bin/grep`, which are
the **same inode** on this host — `stat` → `32:18679` for both — both fail
verification), while a genuine `grep (GNU grep) 3.12-modified` sits on `PATH`
at a non-standard location `$ALTPATH/grep`:

```
  /usr/bin/grep now: false (GNU coreutils) 9.12
  which grep on PATH: /tmp/.../altgrep/grep
  alt grep version: grep (GNU grep) 3.12-modified
  --- A: LANDED gate (unpatched) ---
  rc=2  stdout: NONE
  stderr: research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)
  --- B: CONTROL copy, wrapper fn removed (only edit) ---
  rc=1  stdout: METADATA_COMPLETE=37/41
```

Control B is the **landed gate with exactly one line changed** — the
`grep() { … }` wrapper removed (`ctl-nowrapper-only.sh`, sha256
`c63e26df74ec348d090e74cc2f1718e09c9d64b04de58671f383f82fbcc814d2`). With the
wrapper gone, `command -v grep` sees the PATH file and the gate runs. That
isolates the cause to the wrapper/lookup interaction, with no other variable
changed.

The **base (pre-pin) gate runs fine in that same namespace**:

```
  env: /usr/bin/grep broken; PATH grep = …/altgrep/grep
  --- BASE gate (pre-pin, sha a6307edf) in this namespace ---
  rc=1  stdout: METADATA_COMPLETE=37/41
```

So: **the landed gate refuses where the base gate worked.** The regression is
silent about its own cause — the refusal message says "…**or on PATH**", but the
gate never successfully consults `PATH`.

### Minimal fix, validated

`ctl-fix-typeP.sh` = landed gate with exactly one substitution,
`command -v grep` → `type -P grep` (sha256
`939cfbc511335dece3e8054f4f99b4e312ca23eb98d94b01f893489b13d6dcbc`). Same
namespace:

```
  tools/research-gate.sh      -> rc=2  research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)
  ctl-fix-typeP.sh            -> rc=1  METADATA_COMPLETE=37/41
```

`type -P` reports the PATH-resolved file, ignoring functions — the lookup the
code already intends. (Alternative: `hash -p`/`command -v` with the function
unset for the lookup only. `type -P` is the smaller diff.)

### Why the C1 counter cannot see this

The C1 counter's S3 scenario ("grep absent from PATH") only removes grep from
`PATH`; `/usr/bin/grep` still exists on disk, so the **first** candidate always
wins and the broken third step is never reached. No scenario in
`c1-count.py` breaks `/usr/bin/grep` and `/bin/grep` themselves. Hence
`GREP_PIN_MATCH=9/9` can hold while the third resolution step is dead. This is
a **gap in the frozen predicate's coverage**, not a falsification of it — the
predicate is still met on this host — but the *claim prose* in
`corpus/knowledge/grep-pin-r35.md:39-40` ("Otherwise the gate tries
`/usr/bin/grep`, then `/bin/grep`, then an absolute `command -v grep` result —
each through the same check") describes behaviour that does not exist.

**Impact** [INFERENCE, prevalence not measured here]: on any host whose GNU
grep is not at `/usr/bin/grep` or `/bin/grep` (BSD/macOS/Homebrew, Nix,
a musl/Alpine image with `grep` only under `/usr/local`, a distro that moves
`grep` out of `/usr/bin`), the gate **cannot run at all** — every mode, exit 2.
That is a hard operability loss against the pre-pin gate, which resolved bare
`grep` through `PATH` and ran. Operability is the lowest-scored axis (3/10).
The fix is one word.

**Second-order note:** on this host `/usr/bin/grep` and `/bin/grep` are the same
inode, so the "two absolute candidates" are really one; the whole default
resolution is a single file plus one dead branch.

---

## 6. FINDING — the self-reported-provenance limit is reachable *in this mode* (calibration)

`claims.md` states the limit ("a binary that lies about its version is out of
this check's reach"). Confirmed here, with a concrete number: an override that
prints `grep (GNU grep) 3.12-modified` on `--version` but never matches
(`ctl-lying-grep`) passes the pin check, and the registry scanner then silently
reports **41** `META_SOURCE_NO_ROW_ID` instead of **25** — i.e. the registry
relationship screen is degraded without any error:

```
C1-clone-clean        25 FINDING META_SOURCE_NO_ROW_ID  (+4 RECHECK_ABSENT, 9 ROOT_PARENT, 21 UNSCHEDULED, 1 SOURCE_ABSENT, 1 VERIFIED_AT_ABSENT)  findings=61 drift=6
F1-lying-override     41 FINDING META_SOURCE_NO_ROW_ID  (same other ids)                                                              findings=77 drift=6
META_SOURCE_SCAN_FAILED present in lying run? 0
```

`drift` stays 6 (the extra 16 findings are `info` severity, so they do not
drift) — a wrong-but-plausible registry verdict, with **no** drift signal. The
gate's own answer to "is the registry relationship trustworthy?" is therefore
only as trustworthy as the binary's self-report. This is the documented limit,
now quantified for the metadata mode; it is a bound on C1's operability claim,
not a refutation of it.

---

## 7. Limits of this report

* Coverage is `verify-metadata` only. `verify`, `verify-claims`,
  `verify-chain`, `verify-sweeps`, `verify-integrity`, `verify-all`, `--pin`,
  `--drift`, `--selftest` are other seats' items; the dead-fallback defect
  (§5) is in `grep_pin_init` and so is **mode-independent** — every mode on such
  a host refuses with exit 2 before reading anything.
* The registry was **not** edited. The live `corpus/SOURCES.md` /
  `corpus/knowledge/*` differences (`54bf6cc8…`, +3 knowledge files) are other
  seats' concurrent edits, observed but not caused by this seat. This seat wrote
  only `.ufo/waves/round-35/w2/ExecPinModeMetadata.md` and files under
  `/tmp/hyaku/chousa-r35/w2/ExecPinModeMetadata/`.
* No `pacman`/package install, no network, no git/jj write commands. The clone
  was made with `git clone` + `git checkout` of the frozen base revision
  (read-only git).
* The mount-namespace experiments used `unshare --user --map-root-user --mount`
  with a bind-mount over `/usr/bin/grep` **inside the namespace only**; the
  host's `/usr/bin/grep` was not modified (`sha256sum /usr/bin/grep` unchanged,
  and the namespace exits with it).
* §5's host-prevalence claim is [INFERENCE]; the *unreachability of the branch*
  and the *regression vs the base gate* are measured.

## 8. Files

* Report: `.ufo/waves/round-35/w2/ExecPinModeMetadata.md` (this file).
* Harnesses + receipts (scratch, `/tmp/hyaku/chousa-r35/w2/ExecPinModeMetadata/`):
  `harness.sh` … `harness7.sh`, `final.sh`, `census.sh`, `ns-test*.sh`;
  `out/` (600 KiB) holds every stdout/stderr receipt named above; controls
  `ctl-nowrapper-only.sh` (`c63e26df…`), `ctl-fix-typeP.sh` (`939cfbc5…`),
  `ctl-lying-grep`, `ctl-patch-nofallback-gate.sh`,
  `ctl-patch-nofallback-nowrapper.sh`; clone at `clone/` (rev `e87c5d7`).

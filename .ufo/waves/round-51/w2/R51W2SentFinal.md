# R51W2SentFinal — FINAL hazard sweep, round 51 wave 2

Scope: the five assigned hazards over what the round adds (`9ec1751…4436e27`, plus `4436e27…72566c8` where relevant). No production byte written; no network; no install/upgrade needed. All runs from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, counters `env -u ASSIMILATE_CITES`, scratch `/dev/shm/chousa-r51-R51W2SentFinal/` (deleted at end).

## H1 — credential / private-URL material: NONE (holds)

```
$ git -C …/chousa-shokunin diff 9ec1751a… 4436e279… --stat | tail -1
 173 files changed, 12642 insertions(+), 56 deletions(-)
$ git diff 9ec1751a… 4436e279… -U0 > added.diff          # 13810 diff lines, 11133 added
$ grep -E '^\+[^+]' added.diff | grep -icE 'op://|api[_-]?key|token=|password|secret|session'
94
$ per-pattern, added lines: op:// 0 · api[_-]?key 0 · token= 40 · password 0 · secret 2 · session 52
```

All 94 classified by shape (values never printed; long runs masked `<REDACTED:len>`): `session` (52) = 49 × `w1-results.json` note “delivered to the orchestrator session”, `R51ExecFixturePerturb.md` “the session shell's builtin `grep`”, 3 × Sinomed capture paths holding the **public site's** `jsessionid=…` (a foreign session, not ours); `token=` (40) = `R51ExecInfStaged.md`/`R51ReviewProvince.md` finding lines `token='<quote under test>'`; `secret` (2) = `secrets.token_hex(...)`, a stdlib call quoted in `R51ConnCrossClaim.md`.

Zero over the same lines: `ghp_/gho_/ghs_/sk-…/xox…/AKIA…/glpat-/npm_…` prefixes, basic-auth `scheme://user:pass@`, `Bearer <blob>`, `-----BEGIN` PEM, private IPv4 (`10./192.168./172.16-31.`), `localhost|127.0.0.1:port`, and `.env|.pem|id_rsa|credential|.netrc|.npmrc|kubeconfig|.p12|.key` filenames (0 of the 173 changed paths). High-entropy hits are only 40/64-hex commit ids and `.qcache` `sha256[:24]`. The 26 URL hosts are all public (slarc.org.cn, jstage.jst.go.jp, jahbs.info, jaohfa.com, sinomed.ac.cn, doc.sinomed.ac.cn, c2h.niph.go.jp, lifescience.co.jp, prisma-statement.org, schemas.openxmlformats.org, medsci.cn, cochrane.org, jmla.pitt.edu, toho-shoten.co.jp, library.um.edu.mo, chinagp.net, web.archive.org, gcpunion.org, m.cnpharm.com + synthetic `example.test`/`{host}`). Wave-2 range scanned separately: 4 hits, all the literal pattern inside this seat's own `w2-spec.json`/`w2-dispatch.json`/`gen-w2-spec.py` (self reference). Absolute paths do appear (274 lines cite `/home/vgpnk/Projects/shokuknow`, e.g. `c2-count.py:53` `CACHE`, `claims.md:10`; 440 cite `shokunin`) — the C2 on-disk-capture contract, a portability property, not secrecy.

## H2 — fleet-root misroot: no chousa/round-51 artefact (holds; two strays noted)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | wc -l            22
$ git status --porcelain -uall | grep '^??' | cut -c4-                      155 files
$ for f in <155>; do grep -qiE 'chousa|round[ -]?51' "$f" && echo HIT; done
 14 HIT — every one under .tower/comms/** (M11/M12/M13 missions, r100 survey summaries, reviews,
 state.json, kaika quarantine READMEs); 1-7 × `chousa`, 0 × `round 51`
```

A strict `R51|round-51|round 51` scan over all 155 untracked files returns **no file**. Two strays were created inside the wave-1 window (claims.md 19:55:07 → tip 20:56:49), flagged and left untouched: `demo-cwd.txt`, 30 B, mtime `20:54:49`, content exactly `/home/vgpnk/Projects/shokunin` — a seat's cwd probe landing at the fleet root, the closest instance of the misroot hazard, though its content names neither `chousa` nor `round 51`; and `.ufo/waves/round-41/w1/ExecQuarantineSlice.md`, mtime `19:58:53`, header “seat report (w1, round 41)”, `STATUS: in progress` — another lane's wave, not chousa content.

## H3 — lane hygiene: no production file dirty; bytecode and jj state ARE written into the lane

```
$ git status --porcelain
 M .ufo/waves/round-51/w1/R51DraftSkillGates.md
?? .ufo/waves/round-51/w2.ready
?? .ufo/waves/round-51/w2.ready.dispatched
?? .ufo/waves/round-51/w2/
```

The only dirty tracked file is a **wave-1 seat report** appending “Post-draft tip movement (appended after the lane advanced under this seat)” (+11/−1) — its own report path, so not a breach, but uncommitted post-tip state the integrator must commit or revert. The exact item (3) `find … -newer claims.md …` returns 301 files, classified: 189 `.jj/repo`, 86 `corpus/evidence`, 5 `corpus/fixtures`, 3 `corpus/knowledge`, 2 `tools/__pycache__`, 2 `.jj/working_copy`, 1 each `tools/assimilate-rows.py`, `corpus/lessons`, `corpus/SOURCES.md`, `corpus/README.md` — the `cf642c6`/`4436e27` checkout writes plus jj/pycache. That command is **not trustworthy alone**: 6 tree files carry impossible future mtimes (`.ufo/waves/round-33/w2/ReviewD1Repair/keep-s9001/root/f2f67df2dff.md` = `2026-12-25 03:59:20`), so `-newer` matches them regardless; the authoritative test used instead was `git status` (content) plus pyc mtimes. Zero-byte: exactly 2 in the round dirs — `w1-run.err`, `w2-run.err`, both empty captured-stderr logs (legitimate); `w1-run.err` is the only zero-byte file the diff adds. No symlink added (`git diff --raw` mode `120000`: none), no mode drift beyond `100644`/`100755`, no `.pyc` committed.

**`__pycache__` is written into the lane during wave 2 by the counters:** `corpus/evidence/round51/__pycache__/{c1-count,c1-supplement,c2-count,c3-count,build-spans}.cpython-314.pyc`, mtimes 20:57:22 → 21:16:05, plus `tools/__pycache__/assimilate-rows.cpython-314.pyc` 21:08:38. Cause proven: `c1-supplement.py:43` loads the frozen counter via `importlib.util.spec_from_file_location`; importing a copy of the counter in scratch produced `importtest/__pycache__/c1-count.cpython-314.pyc`. Gitignored (`.gitignore:3 corpus/**/__pycache__/`), so `git status` stays clean — invisible to every content gate.

**Adjacent, sharpest finding — jj state written at 21:14:50:**

```
$ stat -c %y .jj/working_copy/tree_state                  2026-10-25 21:14:14
$ ls -t .jj/repo/op_store/operations/ | head -1            3834b7dd…   (stat: 21:14:50)
$ strings <op file> | head
  snapshot working copy"
  args "jj log --no-graph -r ::@ --limit 48
$ grep -rn 'jj log --no-graph' .ufo/waves/round-51/        (no output, 21:18)
```

A `jj log` inside the lane snapshotted the working copy — this is how the dirty w1 report entered jj state. No wave-2 report claims that command, so authorship is **unattributed**: orchestrator dispatch tooling, or a seat that did not log it. If a seat, it is a breach (boundary: never write jj state). I ran no jj; the only read was `ls`/`stat`/`strings` on the op file.

## H4 — /tmp leaks: present and growing during this sweep (breach by seats, not counters)

```
$ ls /tmp | grep -i chousa-r51      # 21:09:33 → 21:18:45, monotonic 7 → 15
 15 × /tmp/chousa-r51-c1-*          (14 empty; 1 in flight, 90 entries, 21:18:45)
  1 × /tmp/chousa-r51-sup-queb00b9  (160 entries, abandoned 21:14:31)
```

Attribution measured, not assumed:

```
$ TMPDIR=<scratch> env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py
  LEGS=5/5 C1=PASS RC=0 ; ls -a <scratch> → . ..
$ TMPDIR=<scratch> PYTHONDONTWRITEBYTECODE=1 … python3 corpus/evidence/round51/c1-supplement.py
  SUPPLEMENT_LEGS=6/6 C1_SUPPLEMENT=PASS RC=0 ; scratch empty after
```

Both use `tempfile.mkdtemp(prefix=…)` with no `dir=` (`c1-count.py:119`, `c1-supplement.py:170`) and remove it in `finally` (`:209`, `:177`); with `TMPDIR` unset they use `/tmp`, and killed runs (or mutant copies) leave the dir behind — wave 1 logged the hard-kill variant (`R51ExecSeedRuns.md:92`, `R51SentScope.md:33`). Empty dirs, no data leak; the defect is peers running counters under `/tmp` against the `/dev/shm` boundary. I deleted nothing: one dir was in active use at snapshot time and removing a live peer's scratch would corrupt its run. Host fix: `TMPDIR=/dev/shm/…` in the dispatch wrapper.

## H5 — builders and counters write only to scratch (holds)

```
$ git status --porcelain > st.before
$ TMPDIR=<scratch> env -u ASSIMILATE_CITES python3 corpus/evidence/round51/controls/build-c3-controls.py
  RC=0
$ git status --porcelain > st.after ; diff st.before st.after        (no output)
$ ls -a <scratch>                                                   . ..
```

Controls, red expectations met: `BLANKET` DANGLING=5 `C3=FAIL` exit=1 · `DELETED` DANGLING=0 `C3=FAIL` exit=1 · `EMPTY` DANGLING=5 `C3=FAIL` exit=1 · `DOTPATH` DANGLING=0 `C3=PASS` exit=0 · pre-erratum `DOTPATH` DANGLING=4 incl. `ufo/waves/round-51/gen-w1-spec.py`, `C3=FAIL` exit=1. Both counters likewise left `git status` unchanged.

Residual gap (low, no live write path): `scratch()` symlinks every lane top-level entry and the `EMPTY` control skips pointers whose first segment is a symlinked lane entry (`build-c3-controls.py:44-48,63-72`) — the guard against the wave-1 zero-byte-through-symlink write. All five base dangling pointers are top-level names that **do not exist** at the lane root (`measure/final/`, `measure-l1/c1-s36361.json`, `c1-supplement.py`, `round25-meta-differential.log`; root = `AGENTS.md LOG.md MINT.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md considerthese corpus scratch tools` + `.ufo .jj`), so no control ever writes under a symlinked segment: the guard is dead code today and only a future `corpus/…`/`tools/…`/`.ufo/…` dangling pointer exercises it. Smallest remediation: a sixth control appending a `corpus/…/nonexistent` pointer, asserting `C3=FAIL` *and* an unchanged lane file count.

## What holds

No credential, token, PEM, basic-auth URL, private host or private-IP material in any added line; all hosts public; no secret-shaped filename added. No symlink or mode hazard added; no `.pyc` committed. No production lane file is dirty and no seat wrote outside its own report. The c3 builder, `c1-count` and `c1-supplement` leave the lane byte-identical with TMPDIR on scratch. The fleet root carries no chousa/round-51 file.

## Residual risks, ranked

1. **jj state written 21:14:50** by an unattributed `jj log` — snapshotted a dirty w1 report.
2. **`__pycache__` written into the lane** by `importlib` loading of the counters — invisible to `git status` and every content gate (a read-only checkout also changes the failure mode; cf. `R51W2ExecReplayAll` F4). Fix: `sys.dont_write_bytecode = True` in `c1-supplement.py` before line 43.
3. **/tmp scratch growth** under the round's boundary (seats, not counters; 15 dirs at 21:18:45).
4. **`demo-cwd.txt` at the fleet root** (20:54:49) — misroot near-miss, harmless content.
5. **Uncommitted w1 report edit** at sweep time — commit or revert before freeze.

VERDICT: attacked all five assigned surfaces (fresh-credential grep over 11 133 added lines and both commit ranges, fleet-root untracked-content scan, lane status/zero-byte/pycache/mode/symlink audit, /tmp inventory with isolated-TMPDIR replays, builder-and-counter before/after status diffs) — **no credential, private-URL, misrooted chousa artefact, symlink or committed-bytecode hazard holds**; four real hygiene defects do: an unattributed jj working-copy snapshot at 21:14:50, counter-driven `__pycache__` writes inside the lane, 15 abandoned `/tmp/chousa-r51-*` dirs, and an uncommitted wave-1 report edit.

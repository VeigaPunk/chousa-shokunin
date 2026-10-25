# R46 wave 2 — sentinel: span-path boundary, `--json` write scope, Gates-row accuracy

seat `L1Chousa46.SentC1Path` · body chousa · 2026-10-25 · scratch `/tmp/chousa-r46w2-SentC1Path` (deleted)

Bytes, pinned (the lane moved twice while I worked, so every claim names its revision): landing tool `d09fc8e:tools/inference-ground.py` = `819f83ebdc6c…`; landing `span_texts` = `3e325f5a9ac9…`; current worktree tool = `0c8f7ba96cda…` (uncommitted; HEAD blob `7736688b`) and its `span_texts` is **byte-identical** (`3e325f5a9ac9…`), so one result covers all revisions; landing c1 counter `819287e2…` (no canary), current counter `8473abf6…` (canary).

**Verdict.** All four probes hold: (a) absolute, (b) `../`, (c) escaping symlink, (d) directory each exit 1 and no outside file content is ever opened. C1 is **not** harmed on this surface. Four defects: S2/S3 informational, S4 low ×2 plus one cosmetic, S5 low. The row's read-only sentence is accurate about *what* is written, inaccurate about the exit codes around a failed write.

## Harness and positive control

Entry: one `#### Inference` bullet, `- The pool matched \`ZQX9 SECRETTOKEN\` in S085 and nothing else is claimed here.`; `counts.json = {}`; no `--registry`; the token exists only in `outside/secret.txt`. Manifests placed inside `spansdir/` (base = manifest's parent). Discriminating control, both revisions: in-dir span holding the token → **exit 0**; the same file without it → **exit 1**.

## The four requested probes (cell → exit; strace over `%file`)

| case | `span_file` cell | landing | worktree | syscalls naming the outside path |
|---|---|---|---|---|
| (a) absolute | `/tmp/…/outside/secret.txt` | 1 | 1 | **0** — refused before any touch |
| (b) `../` | `../outside/secret.txt` | 1 | 1 | **0** — refused before any touch |
| (c) file symlink → outside | `link.txt` → `../outside/secret.txt` | 1 | 1 | 3: `readlink`, 2× `newfstatat`; **no `openat`** |
| (c2) intermediate dir symlink | `sub_out/secret.txt`, `sub_out/` → `../outside` | 1 | 1 | 3: same shape, metadata only |
| (d) directory | `adir` (a directory inside the base) | 1 | 1 | **0** |

Case (c), verbatim: `readlink("…/spansdir/link.txt", "../outside/secret.txt", 4096) = 21` · `newfstatat(…, "…/outside", {st_mode=S_IFDIR|0755…}, AT_SYMLINK_NOFOLLOW) = 0` · `newfstatat(…, "…/outside/secret.txt", {st_mode=S_IFREG|0644, st_size=39…}, AT_SYMLINK_NOFOLLOW) = 0`. No `openat` of an outside path in any run. Refusal is silent about the bad row and blames the bullet (`FINDING INF_TOKEN_NOT_IN_SPAN`) — a misdiagnosis a reader will chase, not a security defect.

Guard is not over-broad (exit 0, both revisions): nested in-dir `sub/nested.txt`, in-dir symlink `oklink.txt` → `../spansdir/real.txt`, `./sub/nested.txt`. Clean exit 1, no traceback, for a self-symlink loop and a 5 005-byte filename (`ENAMETOOLONG`).

**Row clause "span files named in the manifest must stay inside the manifest's directory": true for read content**, at the landing and at current bytes.

## S2 — info — path-inside / inode-outside (named limit, no fix)

A hardlink to the outside file placed inside the base is accepted and its content read: cell `hard.txt` → **exit 0**, token grounded, trace `openat(…, "…/spansdir/hard.txt", O_RDONLY|O_CLOEXEC) = 3`. Same class: a pre-existing bind mount (untested — needs root). The guard is path-based; inode identity is not compared (`st_dev`/`st_ino` would close it). Impact nil under the stated threat model — the cell is untrusted, the directory is trusted, and whoever can drop a hardlink there can rewrite the manifest. Named so a later reader does not take "inside the directory" as inode containment.

## S3 — info — `resolve()` touches outside metadata

Cases (c), (c2), (d2) `readlink` + `lstat` the outside target before refusing. Nothing is opened and nothing outside reaches stdout/stderr/JSON; findings only ever quote the bullet's own tokens. The clause is true of content, not of stat metadata (existence, mode, size).

## S4 — `--json /etc/…` and whether the declared scope is accurate

Grounded entry (`GROUND: PASS`), landing and worktree identical:

| `--json` target | rc | stdout | stderr last | effect |
|---|---|---|---|---|
| `/etc/chousa-r46-probe.json` | **1** | `GROUND: PASS` | `PermissionError: [Errno 13]` | nothing written (path verified absent) |
| `<dir>/nodir/out.json` | **1** | `GROUND: PASS` | `FileNotFoundError` | nothing written |
| a directory | **1** | `GROUND: PASS` | `IsADirectoryError` | nothing written |
| `…/elsewhere/out.json` (writable, outside manifest dir) | **0** | `GROUND: PASS` | — | file written, 104 B |

**S4.1 — low — exit 1 is not exclusively "findings".** The row's exit-1 cell says `findings, one FINDING line per bullet`; a failed `--json` write yields exit 1 with **zero** `FINDING` lines and `GROUND: PASS` on stdout, plus a traceback. A wrapper reading exit 1 as "claim refused" reports a false refusal for a grounded entry. Smallest fix: `try: write… except OSError: print(…, file=sys.stderr); return 2` (exit 2 already means usage and is already documented).

**S4.2 — low — documented exit 2 is wrong for unreadable input.** A present-but-unreadable (`mode 000`) entry → **rc 1, empty stdout**, `PermissionError` (both revisions), while the row says `exit 2 usage or unreadable entry` and the landing docstring said `2 usage or unreadable input`. The current docstring adds `an unreadable --spans/--counts/--registry reads as empty, fail-closed` — that is **false**: a `mode 000` span file inside the directory → **rc 1, empty stdout, no FINDING** (`read()` raises on an `is_file()`-true path; only *missing* reads as empty). Fix: catch `OSError` in `read()` and `return 2`, or correct both sentences to "a crash exits 1".

**S4.3 — cosmetic.** The landing row read `[--registry corpus/SOURCES.md]`; the current row reads it unbracketed while the code keeps `default=None`. Bracket it or make it required.

**Answer.** `read-only (no network); --json OUT writes exactly the named path` is **accurate about writes** — only the named `OUT`, no temp files, no `__pycache__` (verified), no network, and the path is not confined to any root (`elsewhere/out.json`, rc 0); the sentence carries that carve-out. It is **not accurate as a whole** for the adjacent exit contract, per S4.1/S4.2: "read-only" is true, "exit 1 = findings" is not.

## S5 — low — the C1 kill leg accepts a death, not only a refusal

`c1-count` requires `returncode == 1` on junk and says "a crash (2) or a missing file (127) is not a kill". Python's uncaught-exception exit code **is 1**, and the tool has a reachable path of exactly that shape (S4.2). One-line mutant of the current tool (`if findings: raise SystemExit(1/0)` before the print block; junk stdout becomes `''`, stderr `ZeroDivisionError`):

```
landing counter (819287e2, no canary): JUNK_KILLED=3/3 C1=PASS  rc=0
current counter (8473abf6, canary):    JUNK_KILLED=3/3 CANARY=pass C1=PASS  rc=0
```
The mutant emits no `FINDING` and no `GROUND: FAIL` on any junk fixture — the legs establish "died with 1", not "refused with a finding". The canary closes filename-keyed forgeries only (my name-keyed forge failed it; the content-keyed mutant passes). C1 **as declared** is unaffected (its predicate is exit codes, and its docstring says so). Fix: in `run()` also require `"GROUND: FAIL" in stdout and "FINDING" in stdout` on junk, `"GROUND: PASS" in stdout` on positives — the real tool already emits both.

## S6 — record state (reported, untouched; I wrote only this report)

- HEAD moved `d09fc8e` → `3807537` → `e50b388` during the audit, and `tools/inference-ground.py` is dirty (`0c8f7ba9` vs HEAD `7736688b`; 47+/33−, none in `span_texts`). Verdicts must name bytes.
- Uncommitted at snapshot: `tools/inference-ground.py`, five `w2/*.md`, two `swarm-registry.json` (rounds 40/41), and `corpus/evidence/round41/receipts/cells/cells.json` (`1f5c0afa…` vs HEAD `226b8907…` — an earlier round's receipt). Counter and both controls are now committed (`8473abf6…`, `60209699…`, `b1dac74c…`).
- Wave-1 `SentScopeAudit` F3 cites `inference-ground.py:216` and reports `GROUND: PASS` on an absolute `span_file`. At `d09fc8e` line 216 is `ap.add_argument("--counts"…)` and that probe returns exit 1 at every revision; the guard is already in the landing, commented "round-46 sentinel F3". F3's evidence is **not reproducible against the landing bytes** — a stale line citation from a pre-guard revision, or a false positive. Do not re-assert it as open.

## Not re-tested (out of my surface)

`c3-count.py` span traversal (wave-1 F5), C2 registry scope, C3 spans. The pinned fixture set is what the counter reads (`C1=PASS`, `CANARY=pass`, digests unchanged).

## Commands (verbatim, trimmed)

```
$ git show d09fc8e:tools/inference-ground.py | sha256sum              → 819f83ebdc6c…  (worktree 0c8f7ba9…)
$ sed -n '/^def span_texts/,/^def /p' LANDING  | sha256sum            → 3e325f5a9ac9…
$ sed -n '/^def span_texts/,/^def /p' WORKTREE | sha256sum            → 3e325f5a9ac9…  identical
$ strace -f -qq -e trace=%file TOOL --spans m-c.tsv                  → readlink + 2×newfstatat outside, 0 openat; rc=1
$ strace -f -qq -e trace=%file TOOL --spans m-a.tsv                  → 0 syscalls naming the outside path; rc=1
$ TOOL --entry entry.md --spans m-unreadable.tsv …                   → rc=1, stdout '', PermissionError
$ TOOL --entry entry-locked.md --spans m-pos.tsv …                   → rc=1, stdout '', PermissionError
$ TOOL --spans m-pos.tsv --json /etc/chousa-r46-probe.json            → GROUND: PASS, rc=1, PermissionError
$ python3 c1-count.py --root LANE --tool tool-silent-crash.py         → POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass C1=PASS  rc=0
$ for f in junk-uncited junk-ungrounded junk-borrowed positive-a/b/c; do TOOL …; done → 1 1 1 / 0 0 0, GROUND: FAIL/PASS
```

Scratch deleted; no lane file written except this report; no install needed.

# R55CritForgeHook — C1 audit-hook falsifiers

Axes: operability (C1), depth (scope of capability boundary); calibration unchanged. Frozen claim read first: `corpus/evidence/round55/claims.md:47-96` specifies the hook's stated events and allowed paths. Hook source: `corpus/evidence/round55/c1-count.py:81-108`.

## Probe

Probe command: `python3 -X dev "$S/probe.py"` (in seat scratch; probe installed an audit hook that prints `event, args`, then attempted posix_spawn(`/bin/true`), `io.FileIO('/etc/hostname','r')`, chdir(`/`), symlink(`/etc/hostname`, scratch link), kill(self,0), and zipimporter on a non-zip Python directory). Selected observed output:

```text
os.posix_spawn ('/bin/true', ['true'], environ(...))
open ('/etc/hostname', 'r', 524288)
os.chdir ('/',)
os.symlink ('/etc/hostname', '<scratch>/probe/link', -1)
os.kill (<pid>, 0)
ERROR zipimport ZipImportError not a Zip file
```

`os.openpty` was attempted in the same probe; no `os.openpty` event appeared. Hook `BAD` has `os.posix_spawn` but not `os.openpty`, `os.chdir`, `os.symlink`, or `os.kill`; `PATHS` tests only `open`, `os.listdir`, `os.scandir` (`c1-count.py:84-105`). Thus posix_spawn is denied; open/FileIO is denied when the path is outside ALLOW; chdir, symlink, kill, and openpty are not stopped by this hook. Audit events are emitted for the latter operations but are not matched by either event list. Probe imports/extensions generated incidental Python import/open events; these are not a bypass if their paths fall in Python-prefix ALLOW.

## Consequence and counterexample

The decisive potential bypass is `os.chdir('/')` followed by an ordinary relative open: audit event `open` carries the unresolved relative name, while `allowed()` resolves it against the process's *current* cwd (`realpath`, lines 91-100). The relevant allowed run directory is also a prefix, so a tool can chdir from its run directory into that allowed directory and open a relative path there without denial; more importantly, it may use a relative path that resolves externally if it can arrange the cwd or `dir_fd` context. `dir_fd`-relative `os.open` can access an outside directory while its audit event's first argument is only a relative name; `allowed()` has no dir_fd-aware resolution. Therefore the stated confinement is not established by this hook. A symlink placed within an allowed run directory and then opened is also resolved by realpath and should be denied if it points outside, but this does not close dir_fd/cwd-relative access.

A bypass alone does not demonstrate a C1 leg can pass: the judge compares each span with the counter-derived exact defined text form (`claims.md:58-66`, and `c1-count.py:238-279`). Delegating to LibreOffice would only pass if output spans remain exact slices of that form, and spawning via `os.posix_spawn` is itself caught as `os.posix_spawn`. No successful leg-pass bypass was demonstrated in this probe; report this as a hook-boundary defect, not a falsified observed leg.

Smallest safe correction: make path checks descriptor-aware and cwd-independent (reject relative opens, or resolve against and validate the effective dir_fd/cwd), and deny `os.chdir`, `os.openpty`, `os.symlink`, and `os.kill` if these capabilities are outside the frozen operational contract. The frozen claim must not be edited; this is a counter finding for adjudication, not a patch proposal to the predicate.

VERDICT: C1 hook falsified as a complete filesystem/process capability boundary; posix_spawn is caught, but cwd/dir_fd-relative access and several unlisted audited operations remain unblocked; no passing-leg exploit demonstrated.

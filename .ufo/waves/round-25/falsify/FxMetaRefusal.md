# FxMetaRefusal — round 25 operability

Tested only in `/tmp/chousa-r25-FxMetaRefusal`, switched to the full pin
`e93ac711f885a10d44fdd80a1734997419595b5a`. Clone initially observed at
`d8c8cff3923f10481ac9ced66d0af7c41d38130c`; gate SHA-256 was
`63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2` at d8
and e93. Packaging corrections preserved: at 0fc037e the gate was the old
version (observed old-file SHA-256 `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`);
d8 added the gate but omitted the evidence-index landing; e93 is the full pin.

LSP status was unavailable: `xd://mcp__lsp_status` returned “No such tool” and
the mounted-device list had no LSP device. No semantic LSP checks were possible.

## Finding

- **MEDIUM — exact-cap metadata entry has a severe latency cliff (operability).**
  The valid exact-8-MiB single-line-body fixture completed CLEAN but took
  `real 3m40.934s` (`user 6m32.928s`, `sys 0m55.997s`). Exact timed command:
  ```
  TIMEFORMAT='ELAPSED_SECONDS=%3R'; time env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=/tmp/chousa-r25-FxMetaRefusal/fxmeta-refusal-probe/root CHOUSA_NOW_EPOCH=1792531200 bash /tmp/chousa-r25-FxMetaRefusal/tools/research-gate.sh verify-metadata /tmp/chousa-r25-FxMetaRefusal/fxmeta-refusal-probe/root/exact8mib.md --root /tmp/chousa-r25-FxMetaRefusal/fxmeta-refusal-probe/root
  ```
  Exact output: `research-gate v2 — ts=2026-10-20T21:20:00Z — mode=verify-metadata — path=/tmp/chousa-r25-FxMetaRefusal/fxmeta-refusal-probe/root/exact8mib.md — root=/tmp/chousa-r25-FxMetaRefusal/fxmeta-refusal-probe/root`; `META entry=exact8mib.md source=present verified_at=dated recheck=scheduled verdict=clean`; `METADATA_COMPLETE=1/1`; `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`; exit 0. Bash timing: `real 3m40.934s`, `user 6m32.928s`, `sys 0m55.997s`.
  Code accepts exactly 8,388,608 bytes (`tools/research-gate.sh:265-269`, `2333`) then reads lines into a Bash array (`2343-2347`). The observed latency is actionable for an input explicitly admitted by the inclusive cap; cause attribution beyond the measured run is inference.

## Refusal checks and specification status

- Full five-case exact commands and outputs are saved in the private clone at
  `fxmeta-refusal-probe/metadata-refusal-transcript.txt` (SHA-256
  `fcfc44edc84459ee72c50c3f097310b29375cfccdb728778ea62478f64b9b6af`).
- Sizes: clean 122 B; symlink target 95 B; over-cap 8,388,704 B; exact cap
  8,388,608 B; NUL case 82 B. Clean control: exit 0, `verdict=clean`.
- Benign `meta-alias/benign.md` symlink to the synthetic private
  `home/.config/private.md`: exit 1, `reason=denylist unparsed`; marker absent,
  and no metadata-key findings. Over-cap entry: exit 1, `reason=size unparsed`;
  marker absent, and no metadata-key findings. The gate checks canonical
  denylist then size before the content parser and continues on refusal
  (`tools/research-gate.sh:2329-2347`).
- Exact 8 MiB: exit 0, clean. NUL entry: exit 1,
  `reason=nul unparsed`; output contains no `unread`. NUL is probed by the
  `tr`/`wc` scan before refusal (`2335-2341`), not parsed as metadata.
- **Classification:** spec v1 (`round25-claims.md:20-42`) does not define
  denylist/size/NUL refusal or latency, so those cases are unspecified there,
  not a demonstrated spec divergence. Observed classifications match the
  disclosed post-registration hardening (`metadata-screen-r25.md:41-46`);
  exact-cap acceptance matches the gate's inclusive-boundary comment. No
  refusal-path functional divergence found.

Probe artifacts written in the private clone (SHA-256):
- `fxmeta-refusal-probe/metadata-refusal-transcript.txt` — `fcfc44edc84459ee72c50c3f097310b29375cfccdb728778ea62478f64b9b6af`
- `fxmeta-refusal-probe/root/clean.md` — `d06970eba525dbf9671225d12a6329ea68c8987f63fa0e84ee2bc0af88786a05`
- `fxmeta-refusal-probe/root/home/.config/private.md` — `ffab609f85d1d55ab608aa0abc293f9f15f45e21d210a1ea00e67eec5986d86d`
- `fxmeta-refusal-probe/root/meta-alias/benign.md` symlink-text — `877718473030439adb27ee50ac12dd98639ab54f3e3a576d8601f798166a1995`
- `fxmeta-refusal-probe/root/oversize.md` — `34cde0b8935811555eaa8c2ed552450e9ef26b7317c4e10aecd4db6d8bc4d105`
- `fxmeta-refusal-probe/root/exact8mib.md` — `f98c3b24009157292a84413815b421d3de8d6d07431f0ad4ff64b3870feb2728`
- `fxmeta-refusal-probe/root/nul.md` — `3e9c6c2e33d1a9ce1c00d9aa220c61a09e61b58e8acee7c6fdae77be44f48bb6`

No installs. No selftest/full-suite run; no production edits.
VERDICT: Refusal behavior matched the disclosed hardening; recommend resolving the measured 220.934-second exact-cap latency before treating this input boundary as operationally safe.
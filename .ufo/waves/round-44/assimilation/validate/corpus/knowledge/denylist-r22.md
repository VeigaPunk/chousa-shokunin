# Denylist path-start bypass (round 22)

source: tools/research-gate.sh (is_denylist_path :581-592; norm_ptr :553-562; ptr_file_part :563-578; call sites :603, :632, :1111, :1564); receipts: corpus/evidence/deny-r22-20261019T190000Z-{demo,selftest,battery,drift}.log; round-20 named debt closed
verified-at: 2026-10-19 (round 22, landed; selftest PASS (132 cases, 0 skipped); gate sha dfb798b4…)
recheck: `bash tools/research-gate.sh --selftest` (cases 129–132 pin the path-start class); the demo record in `evidence/deny-r22-…-demo.log`

## The bypass

`is_denylist_path` uses `*/.config/*`, `*/.omp/*`, `*/.local/state/*` — the
`*/X/*` pattern requires a leading path component before the denied
directory. A citation `.config/foo` (no `./` prefix) doesn't match and
passes CLEAN, while `./.config/foo` IS refused `CLAIM_SOURCE_SESSION` crit.
`norm_ptr` strips backticks but not `./` — the two forms reach the denylist
differently.

## The fix

`is_denylist_path` gains bare-start alternatives:
`'.config/'*`, `'.omp/'*`, `'.local/state/'*` — checked after the existing
`*/X/*` forms. A citation starting with the denied directory at path start
now refuses identically to the `./`-prefixed form.

## Named limits

- The canonical-target check (r21) covers symlink indirection but not the
  raw path-start form — the two checks complement each other.
- `.config-adjacent/file.md` is NOT a denylist hit (the `'/` after the
  directory name prevents over-refusal) — case 132 pins this.
- Other denylist patterns (`*.env`, `*server.token*`, `*credentials/*`,
  `*/oauth/*`, `*chrome-profile*`, `*Cookies*`, `*Login Data*`) use `*` not
  `*/X/*` — they already match bare-start forms.

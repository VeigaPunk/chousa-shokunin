source: S075 (`/usr/share/man/man1/mktemp.1.gz`), S076 (`/usr/share/man/man1/sed.1.gz` + `/usr/share/info/sed.info.gz`), S067 (exec PATH resolution), S071/S072 (prior pin/env-export sources); instrumentation run recorded in `corpus/evidence/round41/claims.md`
verified-at: 2026-10-24 — counter `corpus/evidence/round41/c1-count.py` prints `CAPTURE_PIN_MATCH=12/12` on the round-41 landed gate
recheck: re-run `python3 corpus/evidence/round41/c1-count.py` after any edit to `tools/research-gate.sh`; `on-release` for the pinned tool versions

# Canonical capture invocation pinning (round 41)

## What was measured

Before this round the gate pinned `grep`, `env`, `bash`, and `sha256sum`
(r35–r39) but resolved every other external name through the caller's PATH.
An instrumentation run on 2026-10-24 — every candidate tool name trapped
through a logging PATH shim — counted **20 PATH-resolved calls in one
`--pin` + one `--drift` run and 728 in a single `--pin`**: parent-side
`mktemp`, `mkdir`, `cat`, `sed` (the volatile-field normalizer), `rm`, `sort`,
plus startup `readlink`, `dirname`, `date`; and inside the captured
`verify-all` child a much wider set (`tr` 428, `sed` 482, `date`, `readlink`,
`dirname`, `head`, `od`, `wc`, `stat`, `cat`). Each bare name is a documented
interposition point: S067 establishes that a bare command name is sought in
the colon-separated PATH list, so the first shim wins.

## Delivery mechanisms

The pin uses the r35 grep-pin pattern, generalized:

1. **Pin table** — `CAPTOOL_NAMES=(mktemp sed mkdir cat rm sort readlink
   dirname date tr wc od head stat)`; each resolves to ONE absolute binary
   (`/usr/bin/<name>` or `/bin/<name>`, first to pass), verified GNU-reporting
   by a timeout-bounded `--version` probe (`GNU coreutils` for all but `sed`,
   which must report `GNU sed`). `RESEARCH_GATE_<NAME>` overrides must be
   absolute paths and pass the same check; anything else exits 2
   `<NAME>_PROVENANCE` before any record is read.
2. **Function wrappers** — `name() { "$PINNED" "$@"; }` is `eval`-defined at
   init, so all ~263 bare call sites (parsers, selftest, capture) keep their
   spelling and resolve the pinned path. Same mechanism as `grep_pin_define`.
3. **Child PATH** — the captured `verify-all` child runs with
   `PATH=/usr/bin:/bin` (escape hatch `RESEARCH_GATE_CAPTURE_PATH`,
   caller-chosen, not provenance-checked) via the pinned `env` binary; its own
   tools resolve the same pinned table because the child re-runs init.
4. **Loader scrub** — `-u LD_PRELOAD -u LD_LIBRARY_PATH` added to the child
   `env` line (round-38 Erratum-1 class demonstrated live in r37/r38).

## Kill record (frozen scenario table, `claims.md`)

| cell | vector | base gate | landed gate |
|---|---|---|---|
| S2 trap-inventory | logging shim dir on PATH | >0 capture-attributable marks | 0 marks |
| S3 sed-suppress | normalization unmasked | FAIL (volatile tokens drift) | `GATE_DRIFT: none`, shim unread |
| S4 mktemp-preseed | planted capture dir | `fixture-write-failed` / influenced | real dir, shim unread |
| S5 cat-poison | appended JSONL line | manifest-lines mismatch | clean, shim unread |
| S6 rm-suppress | fixture residue | leftover dirs ≥1 | 0 leftovers |
| S7 sort-reverse | non-canonical token order | reversed drift tokens | `sort -u` order, shim unread |
| S8 mkdir-suppress | fixture absent | `fixture-write-failed` | clean |
| S9/S10 override | relative / non-GNU pin overrides | n/a (mechanism absent) | exit 2 `<NAME>_PROVENANCE` |
| S11 child-tr | poisoned child `tr` | child marks present | 0 child marks, identical capture |
| S12 loader-env | inherited `LD_PRELOAD` | 10 child marks saw it | 0 non-empty child `LD=` marks |

Do-nothing control (`controls/base-gate-r41.sh` = pre-round bytes):
`CAPTURE_PIN_MATCH=1/12` — only S1 (base-clean) holds; every attack cell
fails. Landed gate: `12/12`.

## Named limits

- Exported-function delivery (`BASH_FUNC_sed%%` etc.) still reaches the child
  through the r38/S072 channel; the pin covers binary resolution, not
  function delivery.
- `SHELLOPTS=noexec` disables the gate body before pins run (r37 residual).
- The trap-inventory measures the 2026-10-24 observed surface; a tool name
  never invoked in the measured run is outside the claim.
- `RESEARCH_GATE_CAPTURE_PATH` is a caller escape hatch by design.
- `stat` is pinned because the selftest's PATH-shim "stat unavailable" case
  predates the pin; the case now simulates unavailability through
  `RESEARCH_GATE_STAT` with a GNU-reporting stub (the pin honors overrides).

## Cross-round readings

- Correct scope (r39 rule): the surface is the *invocation path* of the
  canonical capture, not the archive-export observable — the 3/10 legacy
  score is unmoved by design.
- Related prior pins: `env-pin-capture-r38.md` (env + `-u` scrubs),
  `capture-bash-pin-r39.md` (grandchild bash), `receipt-binding-r38.md`
  (expectation digests). This note closes the remaining PATH channels in the
  same call tree.

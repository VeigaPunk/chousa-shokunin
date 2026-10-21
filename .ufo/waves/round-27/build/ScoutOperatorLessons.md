# ScoutOperatorLessons — operator teaching and previous verifier lesson existence

Round 27, attempt 1. Base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`. Static
read-only check; no test, selftest, build, fixture or runtime execution.
Axes: **calibration** (record accuracy; no invented absence), **operability**
(the round lesson's intake statement is correct as worded). **Freshness is not
advanced** — this item measures no date behavior; its own dates are the base
commit date (2026-10-21) and the observed working-tree files of the same day.

Paths are relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless
prefixed `fleet:` (`/home/vgpnk/Projects/shokunin`).

## Observed — what "operator teaching" means here

`fleet:LEARNING.md:50-53` defines the artifact: “Operator teaching outranks
every other source. A teaching lands verbatim as
`corpus/lessons/operator-<YYYY-MM-DD>-<slug>.md`”. The same paragraph requires
the next round to reflect it in `QUALITY.md` or `SKILL.md` with the lesson
cited, or report why not. So the existence question has an exact glob:
`corpus/lessons/operator-*`.

## Observed — lane operator teaching file: none at the contract slot

| scope | command | result |
|---|---|---|
| working tree | `compgen -G 'corpus/lessons/operator-*'` | no match |
| base tree | `git ls-tree --name-only 64eec5d corpus/lessons/ \| grep -i operator` | no row; 16 tracked entries (15 `.md` + `.gitkeep`) |
| all refs/history | `git log --all --oneline -- 'corpus/lessons/operator-*'` | 0 commits |
| lane tree (excluding executor clones) | `find . -path ./.git -prune -o -path './.ufo/waves/round-27/work' -prune -o -name 'operator-*' -print` | no match |
| all fleet lanes | per-lane `compgen -G '<lane>/corpus/lessons/operator-*'` under `fleet:` | no match in any lane |

No `corpus/lessons/operator-*` file is staged, untracked, deleted in history,
or present in another lane's lesson directory. `SKILL.md`, `corpus/QUALITY.md`
and `corpus/README.md` contain no `teaching` reference that would imply a
landed-but-hidden teaching (`grep -n -i teaching` → no hits).

Related artifacts are **not** this artifact class:

- `considerthese/2026-10-19.md`, `...-20.md`, `...-21.md` self-identify as
  “daily reflection (chousa-shokunin)” (`considerthese/2026-10-21.md:1`) with
  “Self-improvement proposals (not acted on)” (`:47`). Convention precedent in
  another lane labels the same filename “a reflection, not an operator
  teaching” and separately records no `operator-*.md` (`fleet:.ufo/reports/round-17/mado.md:46-47`;
  that is mado's lane, cited only as wording precedent, not chousa evidence).
- `fleet:.ufo/scopes/*/operator-demand.md` files are mint demands
  (`fleet:.ufo/scopes/shokunin-12h-20261014/operator-demand.md`), not the
  `corpus/lessons/` landing slot.
- The round's claim text (`corpus/evidence/round27-claims.md`, untracked) and
  the operator report quoted in the round lesson are directives/reports, not
  operator teachings.

Consequence, scoped: **no operator-teaching file exists**, so no
`LEARNING.md:50-53` reflection obligation is triggered for round 27 by a file.
This is an absence of the artifact, not evidence that no teaching was ever
spoken outside this slot.

## Observed — previous verifier lesson

A verifier lesson **does exist for round 24**:
`corpus/lessons/round-24-verifier-spotcheck.md` (sha256
`4533b490…c465b4`; tracked at base). Its opening line is “round-24 — non-author
verification and spot-check (orchestrator, kaika)” and `:3` says “Written by
the integrator, not the lane”. Its spot-check table records 4/4 admit and
3/3 reject agreement (`:8-13`). `corpus/lessons/round-25.md:6-9` records it as
reused, `:12-14` names it the “Previous outside check”, and `:102-107` says
round 25's own outside sample was “not performed by this lane”.

No verifier lesson exists for rounds 25 or 26:

- `git ls-tree -r --name-only 64eec5d | grep -i verifier` → only
  `corpus/lessons/round-24-verifier-spotcheck.md` (plus the unrelated
  `.ufo/waves/round-25/build/ConnectorSpotcheckMap.md`).
- `git log --all --oneline -- 'corpus/lessons/round-25-verifier*'
  'corpus/lessons/round-26-verifier*'` → 0 commits.
- working-tree `compgen -G 'corpus/lessons/*verifier*'` → only the round-24
  file.

The reason is recorded outside the lane, so the absence is documented rather
than inferred: `fleet:MANIFEST.json:9873` (`rounds[395]`,
`verification.spotcheck`) says “lane/report writes forbidden by assignment, so
no lane verifier lesson created”; `fleet:MANIFEST.json:11131` (`rounds[414]`,
`verification.scope`) says “Explicit closure bounds forbid lane/report edits:
findings retained in this durable row, no lane verifier lesson.” This matches
`corpus/lessons/round-26.md:12-14` (“No separate round25 verifier lesson
exists (the closure assignment forbade lane writes)”) and leaves round 26's
outside slot to the orchestrator (`round-26.md:64-68`).

## Check of the round-27 lesson's own intake claim

`corpus/lessons/round-27.md:19-20` (currently **untracked**, sha256
`d8da2b16…7680e7b`) states: “No separate round26-verifier-spotcheck lesson or
operator-* teaching was present in the lane glob at opening.” Both halves hold
at the base for their named scopes. One calibration caveat: a generalized
statement “no verifier lesson exists” would be false, because the round-24
verifier lesson is tracked at base. The round-qualified wording must be kept.

## Inference and unknowns

- **Observed:** all existence checks above. **Inference:** with no teaching
  file, the round-27 lesson incurs no reflection duty; if the operator did
  deliver a teaching outside the slot, this check cannot see it and the
  teaching would need to land at the contract path.
- **Not searched (out of scope):** `.ufo/interactive-sessions` transcripts,
  parked-agent transcripts, operator chat, external hosts, and any location
  outside the lane tree and `fleet:*/corpus/lessons/`. Absence is therefore
  claimed only for the named globs and trees; it is not a statement about the
  operator's intent or speech.
- **Tooling limit:** no `lsp` device is mounted (checked `xd://lsp` → “No such
  tool”); this is a filesystem-existence question, answered by literal
  `git ls-tree`, `git log`, `find` and `compgen`. Literal output is not
  presented as semantic proof of file contents.

## Advisory for L1 (no production change required)

- Keep the round-qualified wording at `corpus/lessons/round-27.md:19-20`. If a
  grounded pointer is wanted, append `fleet:MANIFEST.json:9873` and `:11131` as
  the recorded reasons no round25/26 verifier lesson exists.
- Do not create `corpus/lessons/operator-*.md` to satisfy this item; a
  fabricated teaching file would violate the verbatim-landing contract. If a
  teaching is intended this round, it must be supplied by the operator and
  reflected in `QUALITY.md` or `SKILL.md` by the next round.

## Unrun checks and installs

- Not run: `tools/research-gate.sh` (any mode), `--selftest`, fixtures,
  builds, linters, formatters, and the round regression scripts.
- No network, `/proc`, strace, mount, namespace, debugger, live-process or
  host-secret probe. No production edits; this file is the only write.
- Installs/updates: none.

Confidence: **high** for lane file existence and history (direct Git object
inspection); **high** for the fleet-wide `corpus/lessons/operator-*` glob;
**limited** by design to the searched scopes for any claim about operator
teaching outside the contract slot.

## Erratum (same seat, same attempt; prior text preserved)

In “Observed — previous verifier lesson”, the parenthetical “plus the
unrelated `.ufo/waves/round-25/build/ConnectorSpotcheckMap.md`” belongs to the
earlier combined `operator|verifier|spotcheck` pattern, not to the verifier-only
command shown in that bullet. Exact receipt: `git ls-tree -r --name-only
64eec5d | grep -i verifier` returns exactly one path,
`corpus/lessons/round-24-verifier-spotcheck.md`. No finding changes.

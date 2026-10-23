# MutC3Bypass — C3 do-nothing / junk-control attack (round-34 a2, wave 2)

Seat: mutation-tester. Target: C3 (self-audit calibration), not C2. Read-only on lane:
all runs in `/fast/scratch/hyaku/chousa-r34-a2/w2/MutC3Bypass-9/` on a clone checked out
at the frozen tip `707da8184a0fc4d10ab3f17271556cdf364f0af5`.
Pins: gate `a6307edf687ac0fb…` (`sha256sum lane/tools/research-gate.sh` agrees);
`self-audit.py` `22a6822c…091f`, `audit-set.json` `01f6c4b4…9f5c`, dispositions
`e3b0c442…b855` (0 bytes) — each equals `git show 707da81:<path> | sha256sum`. The lane
working tree (`fe3db76`) is byte-identical to 707da81 for `corpus/ tools/ SCORECARD.md
LOG.md SKILL.md` (`git diff --stat 707da81 -- …` empty, exit 0).

## Re-derivation of the committed count (P3)

`timeout 900 python3 corpus/evidence/round34/self-audit.py --lane <clone>` → exit 0,
43 `AUDIT id=… ok` lines + 2 totals = 45 lines, sha256
`b709781c949b5f63371783b93f3b99958f6b48b413a96899de1209646af06452`; the committed
receipt `.ufo/waves/round-34/measure-a2/audit-first-run.txt` is exactly that blob
(1851 bytes, same sha). Second run byte-identical (`cmp` clean). `git status --porcelain`
in the clone = 0 lines after both runs: the tool writes nothing. **K=0, J=0 reproduced
verbatim; C3's P3 holds as specified.**

## (1) Do-nothing control cannot reach the after-state — enumerated

At the attempt-1 base `bf7c931a`, `git cat-file -e` says ABSENT for all five artifacts:
`self-audit.py` (6188 B), `audit-set.json` (5009 B), `audit-dispositions.md` (0 B),
`measure-a2/audit-first-run.txt` (1851 B), `measure-a2/audit-negative-control.txt` (494 B).
`git ls-tree bf7c931a .ufo/waves/round-34/measure-a2/` is empty. All five enter at
`0af0844` only (`git log --diff-filter=A -- …` → one commit). A no-op round therefore
leaves uncommitted/absent: the tool (nothing to run), the 43-check set, the dispositions
file, and the K/J receipt; the SCORECARD row (`SCORECARD.md:1957`) and LOG entry
(`LOG.md:1292`) assert numbers no artifact would support.

Reachability boundary, measured: with the tool but no set,
`--set <missing>.json` → exit 1, **0 stdout lines**, `FileNotFoundError` (no count, no
receipt). With the committed set but a **nonexistent** dispositions path the tool still
prints `SELF_AUDIT_MISMATCHES=0 / SELF_AUDIT_UNDISPOSITIONED=0`, byte-identical to the
receipt (`committed-set-nodisp.txt` sha `b709781c…`). So at K=0 the dispositions file is
*not* load-bearing — the claim's "unreachable without the tool, the set and the
dispositions" is one term too strong; unreachable without tool+set+receipt is shown.

## (2) Junk audit vs real re-derivation

`junk-audit.sh` (in artifact dir) is 6 lines: a heredoc printing `SELF_AUDIT_MISMATCHES=0`
and `SELF_AUDIT_UNDISPOSITIONED=0`, opening nothing. Output `junk-output.txt`.

- Against a 2-lie scratch set (`lie-set.json`: prefix `deadbeef`, gate digest `0*64`):
  real tool → `SELF_AUDIT_MISMATCHES=2`, `SELF_AUDIT_UNDISPOSITIONED=2`, exit 0, with
  `commit-b8053900 MISMATCH git_commit` and `gate-head-digest MISMATCH sha256` lines.
  Junk → 0/0. **Lies hidden.**
- Against a repo-state lie: appended one byte to the scratch clone's `c2-count.py`
  (before `8c0def4d…2173`, after `5ab774aa…199c`); real tool → K=1 (c2-counter-digest),
  junk still 0/0. Restored by `cp`; after-hash equals before exactly; `git status` clean.
- Junk cannot impersonate the receipt: `diff junk-output audit-first-run.txt` = 44
  changed lines (43 AUDIT lines + totals vs 2 lines), `junk-vs-receipt.diff`.

Verdict: the junk-tool mutant **survives** any output-only check and is **killed** by the
frozen re-derivation (same command, real tool, committed set): the count moves to 2 on
set lies and to 1 on repo lies. Exclusion argument in claims-a2 C3 holds.

## (3) Disposition matching rule — can a line cover an unnamed id?

Observed rule (`corpus/evidence/round34/self-audit.py:72-74,129`): a line counts iff it
contains `|` and does not start with `#`; key = `line.split("|",1)[0].strip()`, value =
remainder stripped; coverage = exact dict-key membership `m not in dispositions`. No
regex, glob, prefix, substring or wildcard. Value is never validated or parsed.
Matrix (2 mismatches: `commit-b8053900`, `gate-head-digest`; `matrix.txt`):

| disposition lhs | J | notes |
|---|---|---|
| `*` / `commit-*` / `gate-.*` / `gate-head` | 2 | no unnamed coverage |
| `Xgate-head-digest` / `gate-head-digestX` / `gate-head-digest extra` | 2 | not prefix/substring |
| `gate-head-digest` (padded / no spaces / tab / CRLF) | 1 | `.strip()`, exact name |
| `\| accepted` (empty lhs), `\|---\|---\|`, ZWSP after id | 2 | empty key / invisible byte |
| `\| gate-head-digest \| accepted \|` (markdown table row) | 2 | lhs before first `\|` is empty — format trap |
| `gate-head-digest \|` (empty value), `… \| rejected`, `… \| ZZZ` | 1 | any value counts; printed in mismatch line |
| duplicate key, last line `rejected` | 1 | last wins, reason displayed as `rejected` |

**Answer: no.** A disposition covers an id only by naming it exactly (one id per line,
lhs = id, modulo outer whitespace); it can never zero K (J only), so it cannot fabricate
P3's number. The committed negative control re-derives exactly: 2 lies + disposition
`commit-b8053900` → K=2/J=1 (`d22`); without it J=2; with both named J=0 (`d21`).

Full-bypass probe: a *lying set* of 43 tautological `path README.md` checks makes the real
tool print 0/0, exit 0 (`taut-set.json`) — identical numbers to the junk script, because
the tool trusts its set. The receipt does not record the set's digest, no check pins
`audit-set.json`, and `01f6c4b4…` is cited nowhere in the tree. **Coverage finding:** C3's
after-state binds tool and receipts but not the audit set's bytes; re-derivation must
hash `audit-set.json` at the tip independently. Also at K=0 the J machinery is vacuous
(tool includes no evidence that a real K>0 would land dispositioned).

## Verdict

C3 as frozen (P3) **holds**: K=0/J=0 reproduced twice, byte-identical to the committed
receipt, at pinned tip bytes. Do-nothing unreachable; junk tool killed by re-derivation;
disposition wildcard killed (exact-name only). Surviving coverage findings (not contract
changes): dispositions inert/optional at K=0; set bytes unpinned; any exact-named id is
dispositioned with an unvalidated free-text (even empty) reason; markdown table-row
dispositions silently fail. Limits: C2 not touched; no network; sibling files untouched;
lane jj/git untouched (scratch clone only). Artifacts:
`.ufo/waves/round-34/w2a2/MutC3Bypass/` (12 files, 52 KB) — `rerun-707.txt`/`committed-set-nodisp.txt` `b709781c…`, `lie-set-run.txt` `426ab836…`, `repolie-run.txt` `6dc4facc…`, `taut-set-run.txt` `f5bd3cbe…`, `matrix.txt` `ba82aae6…`, `junk-vs-receipt.diff` `39dc7666…`.

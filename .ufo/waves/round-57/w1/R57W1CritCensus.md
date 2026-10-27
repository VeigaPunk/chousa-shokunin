# R57W1CritCensus — census-gate attack (sources-census.sh validate)

Scope: attack the fleet census gate the round's registry hygiene relies on. All mutations in scratch
fixtures only; the real lane was only read. Gate: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(read-only, runs against `--file`). Tools: bash 5.3.20, gawk 5.4.1 (system, nothing installed).
Scratch `/fast/scratch/hyaku/chousa-r57/R57W1CritCensus/` (deleted at exit; corpus copies 66M each).

## Fixture construction

`cp -a corpus` per fixture under `$S/fix-<name>/corpus/`; rows injected after line 140 (last registry
row S130, before `## Paths` at line 142) via `sed -i '140r inj.txt'`. Registry = lines 11–140,
130 rows, ids S001–S130. Lesson learned the hard way: `validate --file` resolves `used-by` against
the parent of the file's dir (`resolve_targets`, script:546-550), i.e. the lane ROOT — a corpus-only
copy false-positives `E11 S077 missing used-by tools/quarantine-check.py` (S077 legitimately cites
the lane tool; it exists). Symlinking the lane's `tools/` into each fixture root makes the baseline
byte-comparable to the real registry. Any seat copying only `corpus/` and running validate will hit
this spurious E11.

## Baseline (pristine copy, tools/ linked) — exit 0

```
file  W04  S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file  W04  S053 duplicate url docs.python.org/3/library/socket.html across scopes
file  W04  S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file  W04  S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file  W04  S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file  ok   .../fix-base/corpus/SOURCES.md
```
(5 pre-existing W04 warnings; exit=0.) The same run against the REAL registry
`validate --file /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md` prints the identical
5 W04s + `file ok`, exit=0: the live registry is census-clean today.

## The four attacks — each flagged

Common preamble (all runs): the same 5 W04 lines as baseline. Finding lines and exit codes:

(a) 12-cell row injected (`| S901 | … | EXTRA |`, NF=14 vs required NF=13):
```
file  E01  S901 fields=12        exit=1
```
(b) duplicate id (`| S001 | https://example.invalid/dup | …`):
```
file  E03  S001 duplicate id     file  W03  S001 mined but unused     exit=1
```
(c) mined row, dangling used-by (`| S902 | … | corpus/knowledge/no-such-entry-r57.md |`):
```
file  E11  S902 missing used-by corpus/knowledge/no-such-entry-r57.md     exit=1
```
(d) indented duplicate: column-zero `| S999 | …` + 2-space `  | S999 | …` (cat -A-verified 2 leading
spaces), injected as the last two registry rows:
```
file  W03  S999 mined but unused
file  E03  S999 duplicate id
file  W03  S999 mined but unused     exit=1
```
The double W03 proves BOTH S999 rows entered the table — the 2-space row was parsed. Parse proof on
the mutated copy with the round-prompt §10 pattern itself:
```
guarded '^ {0,3}\|…' : S999 count=2 (total ids 132)
column0 '^\|…'       : S999 count=1 (total ids 131)
```

## §10 pattern against the real registry

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,]' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort
```
Result: 130 ids, head `S001 S002 S003`, tail `S128 S129 S130`; column-zero pattern also 130; zero
indented-only ids; zero duplicate ids (`uniq -d` → 0). New ids S131+ are free on the registry side.

## Extra critic probe: the documented 4-space blind spot

A 4-space indented `    | S002 | …` duplicate row (cat -A-verified) passes clean:
`validate` → `file ok`, exit=0, and the §10 guarded pattern still extracts S002 only once. The script
header documents this ("4 or more spaces are indented code and ignored"), and the same blind spot
serves both the validator and the §10 collision check — so a 4-space injected row evades census and
id-collision detection together. Disclosed design tradeoff, not a gate failure; but any seat proving
"no indented rows exist" should say "no 0–3-space indented rows" (4-space rows are invisible to both tools).

## Calibration notes

1. `--file` used-by resolution is lane-root-relative: corpus-only fixture copies false-positive
   `E11 S077` on `tools/quarantine-check.py`. Not a registry defect — the real registry validates clean.
2. The 5 W04 warnings are pre-existing and lane-accepted (exit stays 0); they are not introduced by
   any injection here.
3. Census gate verdicts are per-registry-file; the fleet-wide `census` mode was not exercised (out of scope).

VERDICT — attacked the sources-census.sh gate with four scratch-fixture injections: 12-column row (E01),
duplicate id (E03), dangling mined used-by (E11) and a 2-space indented `  | S999 |` duplicate (E03, with
double-W03 + guarded-pattern differential proving the indented row parsed) — all four flagged, gate survives;
§10 pattern on the real registry gives 130 collision-free ids S001–S130; residual exposure named: 4-space
indented rows are silently ignored by both the validator and the §10 pattern (documented tradeoff).

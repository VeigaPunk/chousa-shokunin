# CritC2Probe: critic of candidate-git-revision-probe.py and its output

Scope: `corpus/evidence/round63/controls/candidate-git-revision-probe.py` (sha256 ccd702f4…) and `candidate-git-revision-probe.txt` (sha256 48aa21f4…). Read-only on the lane; scratch `/fast/scratch/hyaku/chousa-r63/CritC2Probe/` (deleted before yield). No tool installed. No network. No git mutation.

## Findings first

1. **Reproducible.** Two runs, `--work .../p1` and `.../p2`, both exit 0, `diff run1.txt run2.txt` empty, and both match the frozen `.txt` byte-for-byte (`diff` empty). `PROBE_FACTS=14/14`.
2. **Host-varying lines: only the two HEADERs** (`HEADER git=git version 2.56.0`, `HEADER python=3.14.8`). No commit ids are printed; every PROBE line is boolean or a length, so the rest is host-stable.
3. **Five expectations have no sentence in the rendered pages that predicts them** (P02, P06, P07, P10, P13). Two of those are not labelled INFERENCE (P07 and the "moves" half of P06). Another three have a mis-cited or over-cautious comment (P03, P05, P13). Details in the table.
4. **Four probes cannot fail as a git check** (P01, P02, P07, P08). P02 cannot even produce `DIFFERENT`: a sha256-refusing git makes the probe exit 2, not report a fact.
5. **Broken path in the registry rows.** S144 (`candidate-git-rows.txt` line 3), `c2-positive-entry.md` (Q8, Q9, "Claims" cite), and the probe's own usage line name `corpus/evidence/round63/git-revision-probe.{py,txt}`. Neither file exists (`ls` → No such file). The real files are under `controls/candidate-…`.
6. **Docstring list mismatch.** Docstring lines 14-15 list INFERENCE facts as "P02, P05, P06, P13"; the code's `# cite` comments also mark P10 as INFERENCE. The list omits P10.
7. **P13 "small repository" is the wrong mechanism.** The default abbreviation is computed from the *packed*-object count (git-config(1), line 1553 of the rendered page; not in the S142/S143 registry). The fixture has zero packs, which is why 7 holds, not object count. Measured below.

## Per-probe source check

Rendered pages: `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` (S142) and `…/man7/gitrevisions.7.gz` (S143); line numbers are from that output.

| id | expectation | source sentence that predicts it | verdict |
|---|---|---|---|
| P01 | sha1 name = 40 | S143 l.22 "The full SHA-1 object name (40-byte hexadecimal string)" | sourced; **cannot fail** (fixed by `--object-format=sha1`) |
| P02 | sha256 name = 64 | none. Comment says INFERENCE | **no source**, label correct; cannot produce DIFFERENT (see mutant m1) |
| P03 | `v1` id ≠ commit id | cited l.115 ("describes the corresponding commit object") does **not** predict inequality. Predicting sentences are l.117 "because a tag is already an object" and l.119 "<rev>^{tag} can be used to ensure that <rev> identifies an existing tag object" | sourced, **mis-cited**; can fail (mutant m2) |
| P04 | `v1^{commit}` = commit id | S143 l.115; S142 l.64 | sourced; can fail only on git regression |
| P05 | lightweight `lw` id = commit id | l.28 "<refname> … means the commit object referenced by refs/heads/…" plus rule 3, l.34 "refs/tags/<refname> if it exists" predicts it | **labelled INFERENCE but sourced**; label over-cautious, cite should be l.28/l.34 |
| P06 | branch moves after new commit | l.28 gives name → commit the ref holds; that a new commit *advances* the ref is not stated in either page | **no source for the "moves" half**; label INFERENCE correct, cite comment quotes a sentence that predicts only the first half |
| P07 | unchanged file's blob id equal across commits | l.131 says `<rev>:<path>` "names the blob"; it does not say blob id is equal across commits (content addressing is outside both pages) | **no source, not labelled INFERENCE**; **cannot fail** (fixture leaves a.txt unchanged; any git hashes equal bytes equally) |
| P08 | unique 4-digit prefix resolves | S143 l.22 "dae86e … name the same commit object if there is no other object … starts with dae86e" | sourced; fixture-determined, **cannot fail as a git check** (see §Fixtures) |
| P09 | prefix resolves, then ambiguous | S143 l.22 ("unique within the repository") | sourced; can fail |
| P10 | stderr contains "ambiguous" | none (page gives no wording). Comment says INFERENCE | **no source**, label correct; docstring list omits it; fragile wording check, duplicates P09's `returncode != 0` |
| P11 | `--disambiguate` lists both objects | S142 l.119 "Show every object whose name begins with the given prefix" | sourced; can fail |
| P12 | `--short=2` gives 4 | S142 l.75 "The minimum length is 4" | sourced; can fail (mutant m3b) |
| P13 | default `--short` = 7 | none in S142/S143. Comment says INFERENCE, "for a small repository" (wrong mechanism, see §Fixtures) | **no source**, label correct, comment mechanism wrong |
| P14 | `0…0^{object}` fails verify | S142 l.64 "to make sure $VAR names an existing object of any type, … `$VAR^{object}` can be used" | sourced; can fail only on regression |

Count of expectations with no predicting sentence: **k = 5** (P02, P06, P07, P10, P13). If P06 were counted as sourced on the "name → ref's commit" half, k would be 4; the "moves" half is not in the pages, so 5 is reported.

Cannot-fail (n): **P01, P02, P07, P08** = 4. P02 is strict: any sha256-capable git yields 64; a git without sha256 makes `init` raise, so the probe exits 2 and never prints DIFFERENT.

## Mutant runs (wrappers in scratch only, on PATH for the probe's own `git` calls)

- m1, refuse `--object-format=sha256`: probe exit **2**, `RuntimeError: git init -q --object-format=sha256 -b main failed`. No DIFFERENT line. Shows P02 cannot be a DIFFERENT fact.
- m2, `rev-parse --verify v1` peels to commit: exit **1**, `PROBE P03 … observed=False expected=True DIFFERENT`, `PROBE_FACTS=13/14`. P03 can fail.
- m3b, `--short=2` truncated to 2 chars: exit **1**, `PROBE P12 … observed=2 expected=4 DIFFERENT`, `PROBE_FACTS=13/14`. P12 can fail.
(An earlier m3 wrapper was mis-written, observed=7 without truncation; discarded, not reported as a result.)

## Fixtures

- **4-digit collision loop.** Replicated the loop with the probe's env and content: `n=199`, `pref=6a1c`, not a prefix of any of the 7 pre-loop objects; after the second object, `--disambiguate=6a1c` lists exactly `6a1cb632…`, `6a1cd0c8…`; `--verify` stderr `error: short object ID 6a1c is ambiguous` (rc 128). The 6000 bound is safe (birthday tail for 6000 draws in 65536 is ~e^-275). A third colliding object would show as P11 DIFFERENT (detected, not silent). Deterministic for a given hash function.
- **P08 prefix `c1b[:4]` = `8a19`**: exactly one object (`8a19e3e8…`). Fixed content, so it cannot vary by git.
- **Default abbrev 7 under `GIT_CONFIG_GLOBAL=/dev/null`.** Measured:
  - 7 objects, no packs: `--short` = 7. Host `git config --global --get core.abbrev` → unset (rc 1), so the null global is protective, not load-bearing, here.
  - 205 objects at P09 time, no packs: 7.
  - +20,000 loose blobs, no packs: 7 (count-objects `count: 20206 | in-pack: 0 | packs: 0`).
  - After packing all ~20.2k objects (`pack-objects --all`): **8** (`in-pack: 20213 | packs: 2`).
  So the value tracks *packed* count, not loose count or "small repository". The probe's 7 holds because the fixture has zero packs; the comment's "small repository" is the wrong reason. The mechanism sentence is git-config(1) l.1553 ("computed based on the approximate number of packed objects"); that page is not in the registry, so P13 stays unsourced under S142/S143.

## Registry and path defects (for L1)

- S144 row, `candidate-git-rows.txt` l.3: names `corpus/evidence/round63/git-revision-probe.{txt,py}`; absent. Real: `controls/candidate-git-revision-probe.{txt,py}`.
- `c2-positive-entry.md` Q8 and Q9 quote lines of that absent output; the entry's `recheck` path has the same defect.
- Probe usage line (docstring l.6) names `corpus/evidence/round63/git-revision-probe.py`; the file is `controls/candidate-git-revision-probe.py`.

## Smallest corrections (not applied; frozen tree)

1. P03 cite → S143 l.117 and l.119 (drop l.115).
2. P05 comment → cite l.28 and rule 3 (l.34), or keep INFERENCE and say the rule is the basis.
3. P07 → relabel INFERENCE (content addressing, outside both pages) and make it discriminating: a fixture where a.txt changes must give DIFFERENT, or drop it. As written it cannot fail.
4. P01, P02 → label as format checks; P02 cannot fail as written.
5. P10 → add to the docstring INFERENCE list; drop or keep as a single wording check (duplicates P09's rc).
6. P13 → cite git-config(1) l.1553 with a new registry row, or keep INFERENCE and change "small repository" to "no packs".
7. Fix the S144 / entry / usage paths.

`PROBE_FACTS=14/14` measures agreement with author-typed expectations, not an independent measurement (the probe's own docstring says so).

Runs: `python3 -B candidate-git-revision-probe.py --work …/p1` and `…/p2` (both exit 0, identical, equal to frozen `.txt`); mutants m1, m2, m3b as above; replica fixture and pack test by a Python driver (`git hash-object`, `cat-file --batch-all-objects`, `repack`, `pack-objects --all`, `count-objects -v`); man renders via `MANWIDTH=1000 man -l … | col -bx`.

VERDICT: PROBES_WITHOUT_SOURCE_SENTENCE=5/14 cannot_fail=4

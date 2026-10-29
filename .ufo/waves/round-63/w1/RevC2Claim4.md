# RevC2Claim4 — entailment review of Claim 4, candidate entry

Scope: Claim 4 only, of `corpus/evidence/round63/controls/c2-positive-entry.md` (sha256 prefix 93ad2c681783b6ce).
Frozen instruments and controls read, not edited. No network. Scratch removed before yield.

## The claim as written

> Claim 4. The shortest abbreviation the tool will print is four digits and its default comes from configuration, so an abbreviation printed on another machine may be longer or shorter than the one a citation shows. [Q5, Q1]

## Re-opened quotes (rendered `MANWIDTH=1000 man -l FILE | col -bx`, git 2.56.0)

Q5, git-rev-parse(1), rendered output lines 74-75:

> `--short[=<length>]` Same as --verify but shortens the object name to a unique prefix with at least length characters. The minimum length is 4, the default is the effective value of the core.abbrev configuration variable (see git-config(1)).

The entry's Q5 matches these words exactly, cut before "(see git-config(1))". The page's entry is for `git rev-parse --short` only.

Q1, git-rev-parse(1) line 202 and gitrevisions(7) line 22 (same wording in both):

> The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository.

The entry's Q1 matches.

Probe, `controls/candidate-git-revision-probe.txt` (rerun by me: `python3 -B .../candidate-git-revision-probe.py --work <scratch>/p`, exit 0, `PROBE_FACTS=14/14`):

- `PROBE P12 short-length-minimum-is-four observed=4 expected=4 ok` (source line 140: the probe calls `--short=2`)
- `PROBE P13 default-short-length-small-repository observed=7 expected=7 ok` (source lines 143-145; the P13 cite is `INFERENCE`: "the page names core.abbrev as the default but not its value")
- Source header: "no global or system git configuration". The committed probe never sets `core.abbrev`.

## Verdict reasoning

The quotes support three things:

1. For `git rev-parse --short`, a requested length has minimum 4 (Q5).
2. The default length is the effective value of `core.abbrev` (Q5), so configuration sets it.
3. An abbreviation is a prefix that is unique within the repository, so its printed length depends on repository contents (Q1), and is "at least length characters" (Q5 line 75).

From these, "the length of an abbreviation depends on configuration" follows. Claim 4 is not a misreading. It **overreaches** in three places, each stating more than the quotes and the probe support:

- **"the tool"**: the claim names no tool. The only quoted source is the `--short` entry of `git-rev-parse(1)`. Read as "git" or "any abbreviation git prints", it reaches `git log --abbrev-commit` and other commands that Q5 does not cover. Limits does not scope it either: Limits covers git versions and hosting services only.
- **"four digits"**: Q5 says "at least length characters" and "the minimum length is 4" for the requested length. "digits" is a paraphrase (object names are hexadecimal) that a stranger checking the page will not find. Minor.
- **"on another machine"**: no quote mentions machines, hosts or where configuration lives; git-config(1) scope is not quoted. This is `[INFERENCE]` and is not marked as such in the entry. This is the main overreach.

The claim also leans on configuration being varied, and the lane's own probe does not vary it. The probe runs with no global or system configuration, and P13 is the default on one small repository. So the configuration dependence is quoted (Q5), not observed by the probe. The entry's Limits does not say this. That is a calibration gap.

Not overreach: "may be longer or shorter" is hedged, and the direction follows from a variable default. The minimum-4 part is observed for the argument (P12: `--short=2` → 4 characters) and is consistent with Q5.

## Own observation (not committed to the lane; reproducible)

Fixture: `D=$(mktemp -d --tmpdir=/fast/scratch/hyaku/chousa-r63/RevC2Claim4 fx.XXXX)`, `git -C "$D" init -q`, one commit with `-c user.name=probe -c user.email=probe@invalid`. Toplevel check: `git -C "$D" rev-parse --show-toplevel` printed `$D` (TOPLEVEL_OK). Commit hashes differ between my runs (commit time), so the hash strings below are from the final run.

```
git --version                                             -> git version 2.56.0
git -C "$D" rev-parse --short HEAD                        -> 7 chars  a5d17c6
git -C "$D" -c core.abbrev=4  rev-parse --short HEAD      -> 4 chars  0cea
git -C "$D" -c core.abbrev=12 rev-parse --short HEAD      -> 12 chars 0ceaf100dee9
git -C "$D" -c core.abbrev=no rev-parse --short HEAD      -> 40 chars (full)
git -C "$D" -c core.abbrev=3  rev-parse --short HEAD      -> rc=128
    "error: abbrev length out of range: 3"
    "fatal: unable to parse 'core.abbrev' from command-line config"
git -C "$D" -c core.abbrev=12 rev-parse --short=2 HEAD    -> 4 chars  a5d1
git -C "$D" -c core.abbrev=4  rev-parse --short=2 HEAD    -> 4 chars  a5d1
git -C "$D" rev-parse --short=1 HEAD                      -> 4 chars  a5d1
git -C "$D" rev-parse --short=40 HEAD                     -> 40 chars
```

What this adds:

- The explicit length overrides the configured default, and is clamped to 4 (`--short=1`, `--short=2` → 4 chars). Consistent with Q5.
- A configured `core.abbrev` below 4 is a fatal error (rc 128), not a shorter abbreviation and not a clamp. Not in any quote; observed once here. Consistent with "the shortest the tool will print is 4", but it means the minimum is enforced differently for configuration and for the argument. The entry should state this if the claim keeps the minimum.
- Configuration changes the default (7 → 4 or 12 with `core.abbrev`). Observed here, not in the lane probe.

## Rewritten Claim 4 (checkable by a stranger)

> Claim 4. `git rev-parse --short` takes its default length from the effective value of the `core.abbrev` configuration variable [Q5], and a requested length is at least four characters [Q5; probe P12 prints 4 characters for `--short=2`]. An abbreviation is at least the requested length and grows past it when the prefix is not unique in the repository [Q5 "at least length characters"; Q1 "unique within the repository"]. So the length of an abbreviation depends on configuration and on repository contents, and an abbreviation of one object printed under one `core.abbrev` setting may be longer or shorter than the abbreviation of the same object printed under another [INFERENCE from Q5 and Q1; the setting is not observed in the lane probe]. That the two settings sit on different machines is [INFERENCE]: the quotes name a configuration variable and cite no scope.

Stranger's check for this rewrite:

- Q5: `grep -n 'minimum length is 4' ` on the rendered `git-rev-parse(1)` (line 75).
- Q1: rendered line 202.
- P12: `candidate-git-revision-probe.txt` line 14.
- Config effect: the `git -C "$D" -c core.abbrev=... rev-parse --short HEAD` runs above (not committed; a stranger reruns them in a fixture).

Suggested additions to the entry's Limits (only if the rewrite is adopted):

- "The committed probe sets no `core.abbrev` value; the configuration effect on the default is from Q5 and from the fixture runs noted in the review, not from `candidate-git-revision-probe.txt`."
- "A configured `core.abbrev` below 4 is refused with `abbrev length out of range`; the minimum of 4 is not applied to configuration."

Note: the rewrite drops "the tool" in favour of `git rev-parse --short`, drops "digits", and marks "another machine" as `[INFERENCE]`.

## Verification gaps

- Versions other than git 2.56.0 are not checked.
- Entailment is my reading, not a machine check. `c2-count.py` does not check entailment.
- I did not run `c2-count.py` or `c1-battery.py`; they are outside this item.

VERDICT: CLAIM4=overreach rewrite_needed=yes

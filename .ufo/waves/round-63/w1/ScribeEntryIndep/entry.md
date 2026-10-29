# Pinning a citation to a git revision (r63, independent entry)

source: S142 (git-rev-parse(1), git 2.56.0-1 page), S143 (gitrevisions(7), same package), S144 (lane probe output corpus/evidence/round63/git-revision-probe.txt)
verified-at: 2026-10-28
recheck: on-release

## Located quotes

- Q1 | S142 | Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1 | --verify
- Q2 | S142 | If you want to make sure that the output actually names an object in your object database | --verify
- Q3 | S142 | and/or can be used as a specific type of object you require, you can add the ^{type} peeling operator to the parameter | --verify
- Q4 | S142 | The minimum length is 4, the default is the effective value of the core.abbrev configuration variable | --short
- Q5 | S142 | Same as --verify but shortens the object name to a unique prefix with at least length characters | --short
- Q6 | S142 | Show every object whose name begins with the given prefix | --disambiguate
- Q7 | S142 | The <prefix> must be at least 4 hexadecimal digits long to avoid listing each and every object in the repository by mistake | --disambiguate
- Q8 | S143 | The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository | <sha1>
- Q9 | S143 | A symbolic ref name. E.g. master typically means the commit object referenced by refs/heads/master | <refname>
- Q10 | S143 | If you happen to have both heads/master and tags/master, you can explicitly say heads/master to tell Git which one you mean | <refname>
- Q11 | S143 | dereference the object at <rev> recursively until an object of type <type> is found or the object cannot be dereferenced anymore | <rev>^{<type>}
- Q12 | S143 | A suffix : followed by a path names the blob or tree at the given path in the tree-ish object | <rev>:<path>
- Q13 | S144 | PROBE P03 annotated-tag-id-differs-from-commit-id observed=True expected=True ok | P03
- Q14 | S144 | PROBE P07 unchanged-file-blob-id-same-across-commits observed=True expected=True ok | P07
- Q15 | S144 | PROBE P09 prefix-resolves-then-ambiguous-after-second-object observed=(True, True) expected=(True, True) ok | P09

## Claims

Claim 1. `git rev-parse --verify` accepts exactly one name, turns it into a raw 20-byte SHA-1 object name, and checks that the output names an object; a `^{type}` suffix also requires the object to be of a given type. [Q1, Q2, Q3]
Claim 2. `--short` abbreviates an object name only as far as it stays unique, never below four characters; the fallback length is whatever core.abbrev configures, and `--disambiguate=<prefix>` lists every object whose name starts with the prefix, which must carry at least four hexadecimal digits. [Q4, Q5, Q6, Q7]
Claim 3. A revision spelled as the full 40-byte hexadecimal name, or as any leading substring that stays unique in the repository, names one object; a refname such as master typically means refs/heads/master, and when both heads/master and tags/master exist, writing heads/master tells git which one is meant. [Q8, Q9, Q10]
Claim 4. `<rev>^{<type>}` keeps dereferencing the object at `<rev>` until one of the given type turns up or nothing more can be dereferenced; `<rev>:<path>` picks out the blob or tree at a path in a tree-ish object. [Q11, Q12]
Claim 5. On this host git 2.56.0 gives an annotated tag an object id that differs from its commit's id, keeps a file's blob id the same across commits while the file is unchanged, and makes a short prefix ambiguous once a second object shares it (probe P03, P07, P09). [Q13, Q14, Q15]

## Limits

- The live `git --version` line on the checking host is `git version 2.56.0`; the quotes are from the git 2.56.0-1 pages rendered on that host. Other git versions are not claimed.
- The S144 probe covers one host, one git version and 14 cases in throwaway repositories; it says nothing about hosting services or other object formats.
- [INFERENCE] Whether each claim follows from its quotes is judged by reading, not by the counter; the counter checks quote location, structure and a word-echo screen only.
- The pages describe object names in SHA-1 form (a 40-byte string, a 20-byte raw name). The sha256 object format is only named in rev-parse (`--output-object-format`) and is not quoted here.

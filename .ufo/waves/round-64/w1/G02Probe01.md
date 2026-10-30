# G02 prefix/suffix boundary probe

Scope: isolated fixture calls to candidate `corpus/evidence/round64/controls/ref-preflight-v3.py`'s G02 function; candidate was not modified. Frozen contract read from `corpus/evidence/round64/claims.md` lines 52–61: indexing regex uses `(?<![\w.-])(?:knowledge/)?NAME(?![\w-])`, where NAME includes the `.md` suffix.

## Fixture recipe and command

Recipe: `/fast/scratch/hyaku/chousa-r64/G02Probe01/probe.py`. It loads the candidate by absolute path, creates a fresh temporary minimal `corpus/knowledge/alpha.md` plus `corpus/README.md` for each case, and calls `g02` directly. Command:

```sh
python3 /fast/scratch/hyaku/chousa-r64/G02Probe01/probe.py
```

Exit: 0. Exact output:

```text
whole-token bare: PASS | 1 entries indexed
left word boundary rejected: FAIL | 1 not named in corpus/README.md: alpha.md
left dot boundary rejected: FAIL | 1 not named in corpus/README.md: alpha.md
left hyphen boundary allowed: FAIL | 1 not named in corpus/README.md: alpha.md
right word boundary rejected: FAIL | 1 not named in corpus/README.md: alpha.md
right hyphen boundary rejected: FAIL | 1 not named in corpus/README.md: alpha.md
right dot boundary allowed: PASS | 1 entries indexed
prefixed whole token: PASS | 1 entries indexed
```

## Comparison

For the frozen regex, `alpha.md` is an exact whole token. A preceding word/dot/hyphen character blocks a match; a preceding ordinary delimiter allows one. A following word or hyphen character blocks a match; a following dot is allowed. Bare and prefixed forms pass, as expected. The case labelled “left hyphen boundary allowed” was misnamed in the initial recipe: the frozen contract explicitly excludes hyphen on the left, so its observed FAIL is correct; ordinary delimiter behavior was not tested.

The candidate diverges from the exact frozen pattern: its index-side code matches the file stem `alpha`, not `alpha.md` (candidate lines 131–135). The probe independently demonstrates an important observable edge: README `alphaX` fails to index `alpha.md`, while `alpha.md.` passes. However this does not establish exact conformance for every suffix shape because the probe did not include a token where the `.md` suffix is followed by a letter/punctuation boundary, nor did it exercise false-positive stem tokens. Treat any claim of full regex equivalence as unproven by this probe. Candidate outputs above are the measured evidence; no production edits or tool installs were made.

Scratch recipe is under `/fast/scratch/hyaku/chousa-r64/G02Probe01/` and must be removed at exit.
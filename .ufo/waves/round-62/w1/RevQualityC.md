# RevQualityC — QUALITY 124 draft (freeze-file digests and control counts)

Scope: one new QUALITY.md criterion, drafted and attacked. No lane file written; the checker lived in
scratch (deleted). Revision read: `388d153519a36a4c3f34d56d034870f032865a70` (freeze commit; `git cat-file -t` → commit).

## Findings

1. **Criterion 122 is a partial duplicate, and its own Check cannot pass a compliant file.** The ellipsis
   clause is 122's. Run: `python3 -B corpus/evidence/round61/digest-ellipsis-check.py corpus/evidence/round62/claims.md`
   → `DIGEST_ELLIPSIS tokens=0 matched=0 mismatched=0`, rc=1, because the tool returns 0 only when `toks and not miss`.
   Round 62's claims follow 122's advice (no ellipsis) and 122's Check reports FAIL. Calibration defect in 122;
   L1 should fix that tool's zero-token branch in a later round (I did not edit it).
2. **Criterion 74 covers `<n> located quotes` only in four prose files, digit forms only.**
   `corpus/evidence/round50/stale-count-check.py:18` `PROSE = (QUALITY.md, README.md, LOG.md, lessons/round-49.md)`;
   `corpus/evidence/round61/claims.md` is not scanned, and `ten`/`fourteen`-style words are not matched.
   So round 61's `8 located quotes` (claims.md:81) escaped 74. 74's own check is red on the working tree:
   `python3 -B corpus/evidence/round50/stale-count-check.py --root <lane>` → `STALE_COUNT=FAIL`, 14 unresolved hits
   (e.g. `corpus/QUALITY.md:935 says 49, receipt 31`). Extending 74's scope inherits that red state until those
   lines are corrected.
3. **The 16-hex prefix form is invisible to existing tools.** `tools/freeze-check.py` `DIGEST_STRAY` reads only
   64-hex tokens (`HEX64` at line 47); 122 reads only `8hex…5-8hex`. Round 62's `sha256 prefix <16 hex>` convention
   has no checker.
4. **Round 62 claims pass the draft digest clause** (rev `388d1535`, 3 prefix tokens, 2 paired, 0 fails, rc 0).
   Round 61 claims fail it with 9 abbreviation hits (8 unique tokens; 6 of them match real files, which 122
   accepts). Per the criterion text, a matching abbreviation still fails: the form is refused, not only the mismatch.

## Draft criterion text (for L1; number 124 unused — last criterion is 123)

124. **A frozen claims file writes each digest as a 16-hex prefix that `sha256sum` reproduces, and every stated
    count of controls or quotes equals the number its named receipt prints.** A digest written `prefix…suffix`, or as
    a 64-hex token, cannot be checked against its file; a count stated as `8 located quotes` over a receipt printing
    `QUOTES=10/10` is a false claim frozen before any seat ran. — `corpus/lessons/round-61-verifier-spotcheck.md`
    defect (a); `corpus/evidence/round61/claims.md` `…` tokens at lines 38, 48, 123–124 and `8 located quotes` at 81.
    Check, from the lane root, against the freeze revision: `python3 -B corpus/evidence/round62/digest-prefix-check.py
    corpus/evidence/round62/claims.md <freeze-rev>` exits 0 with `fails=0`: no `…`-abbreviated or 64-hex digest; each
    `sha256 prefix` token is the prefix of a blob at that revision; each backticked path followed by a prefix token
    reproduces it (`sha256sum PATH | cut -c1-16`). Count clause, one named command per count:
    `grep -cE '^CONTROL X(0[1-8]|1[02])-' corpus/evidence/round62/controls/c1v2-controls.txt` must print `ten`'s 10.
    Shown able to fail (ran): round-61 `claims.md` → `fails=9`, rc 1; round-62 claims with `b7016fba…91b03460` → rc 1
    `ABBREV_OR_64HEX`; round-62 claims with the owner path swapped to `tools/build-spans.py` → rc 1
    `PAIR_MISMATCH tools/build-spans.py b7016fba91b03460`; round-61 `8 located quotes` vs
    `grep -oE 'QUOTES=[0-9]+/[0-9]+' corpus/evidence/round61/c2-measure-after.txt` = `QUOTES=10/10` → mismatch.
    Named limits: the pairing regex reads a path at most 100 characters before its token (round-62 `817d5fc0b94e9fc8`,
    wrapped at claims.md:113, is existence-checked only); the count set is named by the author, so the command can
    be wrong about the sentence; the check binds to blobs at the named revision, not to the working tree.

Relationship: 124 is an amendment, not a new rule. Its ellipsis clause restates 122 (fold into 122 and repair 122's
zero-token exit); its count clause is 74's scope and grammar extended (claims files; word numbers). A new number
adds a second checker for the same failure.

## Checker (scratch draft; the L1 commits it if the criterion is taken)

```python
import re, subprocess, sys, hashlib, pathlib
f, rev = pathlib.Path(sys.argv[1]), sys.argv[2]
lane = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin"); G = ["git", "-C", str(lane)]
t = f.read_text(encoding="utf-8"); fails = []
for m in re.finditer(r"[0-9a-f]{8}…[0-9a-f]{5,8}|\b[0-9a-f]{64}\b", t):
    fails.append(("ABBREV_OR_64HEX", m.group()))
ls = subprocess.run(G + ["ls-tree", "-r", "-z", rev], capture_output=True, check=True).stdout.split(b"\0")
blobs = {}
for rec in ls:
    if rec:
        meta, path = rec.split(b"\t", 1); blobs[path.decode()] = meta.split()[2].decode()
data = subprocess.run(G + ["cat-file", "--batch"], input="\n".join(blobs.values()).encode() + b"\n",
                      capture_output=True, check=True).stdout
prefixes, i = set(), 0
while i < len(data):
    nl = data.index(b"\n", i); hdr = data[i:nl].split()
    if hdr[1:2] != [b"blob"]: break
    n = int(hdr[2]); prefixes.add(hashlib.sha256(data[nl+1:nl+1+n]).hexdigest()[:16]); i = nl + 2 + n
toks = re.findall(r"sha256\s+prefix\s+`([0-9a-f]{16})`", t); pairs = 0
for tok in sorted(set(toks)):
    if tok not in prefixes: fails.append(("NO_BLOB_AT_REV", tok))
for m in re.finditer(r"`([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)`[^`]{0,100}?sha256\s+prefix\s+`([0-9a-f]{16})`", t, re.S):
    pairs += 1; path, tok = m.group(1), m.group(2)
    if path not in blobs: fails.append(("PATH_NOT_AT_REV", path)); continue
    body = subprocess.run(G + ["cat-file", "blob", blobs[path]], capture_output=True, check=True).stdout
    if hashlib.sha256(body).hexdigest()[:16] != tok: fails.append(("PAIR_MISMATCH", path, tok))
print(f"DIGEST124 rev={rev[:8]} prefix_tokens={len(toks)} paired={pairs} fails={len(fails)}")
for x in fails: print("FAIL", *x)
sys.exit(1 if fails else 0)
```

## Runs (rev `388d153519a36a4c3f34d56d034870f032865a70`, `python3 -B`, all read-only)

- `check124 round62/claims.md` → `DIGEST124 rev=388d1535 prefix_tokens=3 paired=2 fails=0`, rc 0.
- `check124 round61/claims.md` at `2edacaf` → nine `ABBREV_OR_64HEX` lines, `fails=9`, rc 1.
- `check124` on round-62 with `b7016fba…91b03460` → `ABBREV_OR_64HEX`, rc 1.
- `check124` on round-62 with `tools/build-spans.py` as owner of `b7016fba91b03460` → `PAIR_MISMATCH`, rc 1
  (existence-only would pass it: the token is a real prefix of `corpus/evidence/round62/c1v2-count.py`).
- Count clause (commands run by hand, comparison by eye, not scripted):
  - `grep -cE '^CONTROL X(0[1-8]|1[02])-' corpus/evidence/round62/controls/c1v2-controls.txt` → `10` (claim: ten).
  - `grep -E ' C2=FAIL OK$' …/c2v2-controls.txt | grep -vcE '^(absent|no-entry-rows) '` → `18` (claim: 18 variants).
  - `grep -oE 'M[0-9]{2}' corpus/evidence/round61/controls/c1-controls.txt | sort -u | wc -l` → `14` (claim: 14).
  - `grep -oE 'QUOTES=[0-9]+/[0-9]+' corpus/evidence/round61/c2-measure-after.txt` → `QUOTES=10/10` (claim: 8) — mismatch.
- `git -C <lane> show 388d153…:corpus/evidence/round62/claims.md | sha256sum | cut -c1-16` → `a3193ebd328919e2`,
  equal to the frozen prefix; the file's full digest was not written in the claim (frozen digest is a3193ebd…866bc).

## Attack results

- A1 existence-only check passes a wrong-owner token (path swapped): the pair clause is necessary. Shown (above).
- A2 pairing is a heuristic over backticked paths; an unpaired token is only existence-checked. Named limit.
- A3 counts are author-named: the checker cannot tell which set a sentence means. The round-62 command regexes
  were written after reading the claims, so they agree with the claims by construction. Not blind; limit stated.
- A4 `…` in a 64-hex or 16-hex context: a token of 16 hex with `…` is caught by the first regex (8hex…5-8hex).
  A token written with a space instead of `…` is not caught (`b7016fba 91b03460`); a limit, not run.
- A5 rev binding: the check reads blobs at the freeze revision, so a later working-tree edit to a named file cannot
  change its verdict; a claim about a file absent at the revision fails `PATH_NOT_AT_REV`.

## Named gaps for L1

- 122: the zero-token branch of `digest-ellipsis-check.py` returns 1 on a clean file (Finding 1).
- 74: scope excludes claims files and number words; its own check is red on the working tree (Finding 2).
- No checker covers 16-hex prefixes; `freeze-check.py` `DIGEST_STRAY` is 64-hex only (Finding 3).

Tools: none installed or updated. Scratch `/fast/scratch/hyaku/chousa-r62/RevQualityC/` removed.

VERDICT: CRITERION_CHECK_CAN_FAIL=yes duplicate_of=122 text_ready=yes

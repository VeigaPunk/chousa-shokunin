# R100SentinelC1 — C1 bypass and side-effect audit at F

Seat: sentinel, wave w1, round 100, lane `chousa`.
Attacked tree: `6d4e8487ee6a16823c24a8e085c6559b92b9fec8` (freeze F), cloned read-only at
`/fast/scratch/hyaku/chousa-r100/R100SentinelC1/repo`. Base: `929c784c63a1fd17961d21742101b2b109b7b8ff`.
Scope: C1 (`C1-GATE-REVCAP-R100`) — the identity rule in `tools/gate-records.py` and its battery. C2 was
spot-checked only (its four counting commands plus an independent quote-location pass), because this seat's
assignment is the C1 bypass/side-effect audit.

Tools used, all preinstalled: `git 2.56.0`, `python3 3.14.8`, `strace` (util-linux), GNU `grep 3.12`.
No package was installed or upgraded in this seat.

## Verdict summary

**C1 fired.** The frozen sentence says the tool fails a rev-form record whose blob "has the object id of a
`corpus/captures/<24 hex>.txt` or `.raw` entry of that rev's tree, and that capture's text — for a `.raw`
entry, its sibling `.txt` at that rev when one exists — is a challenge page". The instrument does not enforce
that sentence: it binds each object id to **one** path, and when two capture entries share an object id it
consults the *other* entry's sibling. A rev record on an honest challenge `.raw` is then **admitted (OK,
exit 0)** after a forger adds one byte-identical file. This is an uncovered admission: none of the five named
limits (a)–(e) covers it, and it is a soundness gap in the tool, not a gap in the battery's oracles.

A second, independent defect: `--repo` pointing at a **subdirectory** of the worktree silently empties the
capture set, so *no* rev record is ever judged (the whole rule goes dark, not just one capture). Also
uncovered by (a)–(e).

Everything else I could throw at the identity rule held: path-spelling bypasses, byte-variant copies,
LFS pointers, symlinks, trees, gitlinks, tag/tree revs, and colon/absolute paths are all refused or fall
under a named limit. Full matrix in `R100SentinelC1-edge-cases.txt`.

---

## F-1 (high) — duplicate-OID cross-wiring admits a challenge capture

### Mechanism

`tools/gate-records.py:249-256` builds the capture set as a map keyed by **object id**:

```python
if parts[2] not in m or path.endswith(".txt"):
    m[parts[2]] = path
```

One object id maps to one path. `rev_capture_text` (`:261-271`) then looks the record's blob id up in that
map and, if the mapped path ends `.raw`, reads **that path's** sibling `.txt`:

```python
name = capture_oids(repo, rev).get(p.stdout.strip())
if name is None:
    return None
if name.endswith(".raw"):
    sib = git_blob(repo, rev, name[:-4] + ".txt")
    if sib is not None:
        blob = sib
```

So the sibling consulted is the sibling of *whichever* capture path happens to own the id, not of the
capture path the record names. When a forger adds a byte-identical copy of an honest challenge `.raw` under a
**lexicographically earlier** capture key, the map's `.txt`-wins/last-writer rule binds that id to the
forger's path, whose `.txt` sibling is benign — and the honest capture's own challenge-page sibling is never
read.

### Reproduction (real lane bytes)

Honest capture: `corpus/captures/b5b8d050eea0c638e95ba674.txt` (S230) at base `929c784c` — 23 words, marker
"checking your browser" → `is_challenge` True. Its `.raw` is the same page's HTML, 620 words → not a challenge
by itself, which is exactly why the `.raw`→sibling rule exists.

```
$ python3 $S/final_evidence.py
```

| tree | `map[oid(S230.raw)]` | rev record on honest `…b5b8d050….raw` | rev record on honest `…b5b8d050….txt` |
|---|---|---|---|
| A honest tree only | `…/b5b8d050….raw` | **rc=1 FAIL CHALLENGE** | rc=1 FAIL CHALLENGE |
| B forger adds 1 file `…/000000000000000000000000.raw` = byte-copy | `…/000000000000000000000000.raw` | **rc=0 OK  ← ADMISSION** | rc=1 FAIL CHALLENGE |
| C forger adds 1 file `…/ffffffffffffffffffffffff.txt` = byte-copy | `…/ffffffffffffffffffffffff.txt` | **rc=0 OK  ← ADMISSION** | rc=1 FAIL CHALLENGE |
| D forger adds `0000….raw` + benign `0000….txt` | `…/000000000000000000000000.raw` | **rc=0 OK  ← ADMISSION** | rc=1 FAIL CHALLENGE |

Base (round-99) tool on the same row-A record: rc=0 OK. So the forger's file **restores** the round-99
behaviour on an honest capture — the round-100 repair is undone by one committed file.

Receipt: `R100SentinelC1-oid-collision-evidence.txt` (script `final_evidence.py` and its stdout, both under
`/fast/scratch/hyaku/chousa-r100/R100SentinelC1/`).

### Why no named limit covers it

- **(a)** the CHALLENGE rule itself is unchanged; the defect is *which* capture's sibling is read.
- **(b)** byte identity — the blob is byte-**identical** to a capture; it is judged, against the wrong sibling.
- **(c)** the capture set is read at the correct rev; the OID→PATH binding inside it is lossy.
- **(d)** covers a `.raw` with *no* sibling; the honest `.raw` here *has* a sibling (the challenge page) and
  the tool never looks at it.
- **(e)** the twelve oracles mutate the *rule*; none mutates the OID→PATH binding. This is a tool soundness
  gap, not an oracle-coverage gap.

### Lane exposure today

The lane's own capture set at F already contains **14 duplicate-OID groups** (e.g. oid `92135f157e…` is both
`corpus/captures/6fe041acddaa1f4e6f6e9775.raw` and `corpus/captures/a42feae4448612f949cc715f.raw`), so the
binding is already lossy on live data. It does not change any verdict *today* because in every one of those
14 groups the colliding siblings carry the same challenge status (measured: 0 groups diverge). The exposure is
latent, and the forger only needs one added file to open it.

### Smallest remediation

Make the OID→path map preserve *all* colliding paths and pick the sibling of the capture path the record
actually names, e.g. resolve the sibling from `path` (the record's own capture path) after confirming that
`path` itself is a capture path, rather than from the map's arbitrary winner. Equivalently: keep the map
`oid -> [paths]` and choose the path equal to the record's own capture path when it is among them. Failing
that, at minimum refuse (CHALLENGE) when *any* capture entry sharing the blob's object id has a challenge-page
sibling.

---

## F-2 (medium) — `--repo` at a worktree subdirectory silently disables the identity rule

`tools/gate-records.py:249` runs

```python
p = subprocess.run(["git", "-C", repo, "ls-tree", "-z", rev, "--", "corpus/captures/"], capture_output=True)
```

`git ls-tree … -- <pathspec>` interprets the pathspec **relative to the current directory**, while
`git cat-file blob <rev>:<path>` (`:232`, `:235`) is **root-relative**. With `--repo` = a subdirectory of the
worktree the pathspec matches nothing, the capture set comes back empty, and `capture_oids(...).get(oid)`
returns `None` for every record — so `rev_capture_text` returns `None` and **no rev record is ever judged**,
by any capture.

Measured on the lane clone with a rev record pointing at the honest S230 challenge capture:

```
  --repo <lane>            -> rc=1  FAIL CHALLENGE
  --repo <lane>/.git       -> rc=1  FAIL CHALLENGE
  --repo <lane>/corpus      -> rc=0  OK      <-- ADMISSION (capture set silently EMPTY)
```

```
$ git -C $FX      ls-tree <rev> -- corpus/captures/   # 4 entries
$ git -C $FX/sub  ls-tree <rev> -- corpus/captures/   # 0 entries
$ git -C $FX/sub  ls-tree --full-name <rev> -- ':(top)corpus/captures/'   # 4 entries
$ git -C $FX/sub  cat-file -t <rev>:corpus/captures/<key>.txt             # blob (root-relative, still resolves)
```

Receipt: `R100SentinelC1-repo-subdir-evidence.txt`.

Not covered by (a)–(e) either. The tool's own `--repo` contract (`main()` at `:377` rejects a non-git
`--repo` with exit 2) is not the issue — a subdirectory *is* inside a git repository, so it passes that check.

Reachability: every lane call site passes `--repo` = the **worktree root** (`--repo @ROOT@` in
`corpus/evidence/round8{9,90,91,92,93,94}/controls/expected.tsv`), so the lane is not currently exposed.
The exposure is a caller passing a subdirectory, or the lane root itself being a subdirectory of its git
worktree — which is the *lane's own* layout: `/home/vgpnk/Projects/shokunin/chousa-shokunin` is a worktree
root of its own repo today, but `git -C /home/vgpnk/Projects/shokunin rev-parse --show-toplevel` returns
`/home/vgpnk/Projects/shokunin`, i.e. the fleet root is a *different, enclosing* repository. Any future
re-layout that makes the lane root a subdirectory of a larger worktree would silently disable the whole C1
rule for every rev record — with no error, exit 0, and "OK" on challenge captures.

### Smallest remediation

Anchor the pathspec to the repository root, exactly as the fix probe shows:
`git -C repo ls-tree -z --full-name <rev> -- ':(top)corpus/captures/'`. Then assert the capture set is
non-empty when the tree contains `corpus/captures/`, so an empty set is a loud setup error rather than a
silent pass.

---

## Checks that passed (no finding)

- **Battery at F.** `python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work <scratch>` →
  `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27
  BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS`, exit 0 — the frozen
  predicate line exactly. Receipt `R100SentinelC1-battery-at-F.txt`.
- **Before control reproduced.** Base tool through the same battery with `--no-oracles` → `REV=3/11 PROD=4/6
  CHALLENGE_CONTROLS_R100=FAIL`, exit 1, matching the shipped `corpus/evidence/round100/before/c1-base.txt`.
  Receipt `R100SentinelC1-before-base-tool.txt`.
- **No lane verdict moved.** `verify` over all 27 lane GATE-RECORD files (207 records) produces **byte-identical**
  stdout for base and F (`diff` empty); both exit 1 on the same single pre-existing lane failure. Base 0.20 s
  vs F 0.22 s over three runs each.
- **Subprocess cost is bounded.** 60 rev records: base 180 `cat-file` + 1 `rev-parse`; F 180 `cat-file` +
  61 `rev-parse` + 1 `ls-tree`. F adds exactly one `rev-parse` per rev record and one `ls-tree` per
  `(repo, rev)` — `capture_oids` caches on `(repo, rev)` (191 entries at F, 0.001 s first call, 0.0000 s second).
  The claim's "one `git ls-tree` once per (repo, rev)" holds.
- **Side effects: none outside `--work`.** `strace -f -e trace=file,network,process` over the whole battery:
  **0 sockets/connects**; 2662 writes, all under `--work` (13 fixture git repos + the lab lanes), 1880 to
  `/dev/null`, **0** under `/home/vgpnk` and **0** outside `--work`. The battery reads the lane and never
  writes to it. Receipt `R100SentinelC1-perf-robustness.txt`.
- **`--repo` non-git dir** → exit 2, `GATE_RECORDS_ERROR not a git repo: …` (the round-85 repair is intact).
- **Path-spelling bypasses all refused**: `./`, `//`, `/./`, `../`, trailing-slash and copy-at-another-path
  spellings of a challenge capture → `FAIL CHALLENGE`. 147 path spellings fuzzed for `cat-file` vs
  `rev-parse` resolution divergence: **0 divergences**.
- **Non-blob capture paths refused**: capture path that is a tree, a gitlink (submodule), or a symlink; a
  capture holding a git-lfs pointer; a rev that is a tag object or a tree. All fail `REV`/`LINE`, never `OK`.
- **Byte-variant copies** (BOM, CRLF, NBSP-in-marker, ZWSP-in-marker) are admitted — exactly named limit
  (b) ("a rev blob that differs from every capture of that rev by one byte is not judged, whatever its
  text"). Not a finding against this claim. (NBSP and CRLF normalize back to the marker; ZWSP does not,
  because `is_challenge` splits on U+200B.)

## C2 spot-check (bounded, no finding)

`corpus/knowledge/quotation-error-update-r100.md` at F: `gate-records.py verify` → `records=17 ok=17 fail=0`
(exit 0); `research-gate.sh verify-metadata` → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN` (exit 0);
`search-rerun.py verify` → `rev_match=3/3`, `SEARCH_RERUN: CLEAN` (exit 0); `entry-controls-r100.py` →
the frozen line exactly, `ENTRY_CONTROLS_R100=PASS` (exit 0). Harm legs: the r99 entry still
`records=25 ok=25 fail=0` and `ENTRY_CONTROLS_R99=PASS`.

Independent of the shipped controls, I re-located every quote: the S238 capture parses as JSON
(`resultList.result[0]`); `U0` is in `result["title"]`, `U1`–`U13` are each in `result["abstractText"]`
(14 U-quotes), `J1`/`J2` are in S236's `abstractText` — 16 quotes, matching "14 located quotes (U0-U13) plus
J1/J2". The S238 registry row's tier cell is `B`, and the capture carries `pmid 40696441`, `pmcid PMC12285159`,
`pubYear 2025`, `doi 10.1186/s41073-025-00173-z`, `authorString Baethge C, Jergas H.`, journal *Research
integrity and peer review* — matching "Baethge & Jergas, Research Integrity and Peer Review 2025, pmid
40696441" and "tier B". The decision table has exactly 8 rows and every Do-cell numeral is a substring of that
row's own warrant quotes; all eight Never cells read "(none stated by the sources)", so `NEVER=8/8` is
trivially true. The r99 entry's `## Update` section names the new entry and S238, and the update's own
wording ("the two rates pool different study sets and their gap is not a trend") matches named limit (c).

One wording note, not a finding: the entry prints `0.253,` (trailing comma) in the "journal's standing" row's
Do cell while the warrant quote U11 reads `-0.253` — a token-level mismatch that the shipped `NUMBERS`
check passes anyway; the numeric *value* and sign are identical, and named limit (b) ("the controls check
numerals as tokens; spelled-out quantities … are not checked") covers the class. It cannot make the row
overreach, because the sign and value both agree.

Receipt: `R100SentinelC1-c2-spotcheck.txt`.

---

## Files written by this seat

- `.ufo/waves/round-100/w1/R100SentinelC1.md` (this report)
- `.ufo/waves/round-100/w1/R100SentinelC1-battery-at-F.txt`
- `.ufo/waves/round-100/w1/R100SentinelC1-before-base-tool.txt`
- `.ufo/waves/round-100/w1/R100SentinelC1-oid-collision-evidence.txt`
- `.ufo/waves/round-100/w1/R100SentinelC1-repo-subdir-evidence.txt`
- `.ufo/waves/round-100/w1/R100SentinelC1-edge-cases.txt`
- `.ufo/waves/round-100/w1/R100SentinelC1-perf-robustness.txt`
- `.ufo/waves/round-100/w1/R100SentinelC1-c2-spotcheck.txt`

Scratch (deleted before yield): `/fast/scratch/hyaku/chousa-r100/R100SentinelC1/`.

VERDICT: R100SentinelC1 C1 fired — the frozen sentence's per-capture sibling rule is not what the tool enforces (one added byte-identical capture file makes the tool admit an honest challenge `.raw`, rc=0 OK), and `--repo` at a worktree subdirectory empties the capture set so no rev record is judged at all; neither is covered by named limits (a)–(e).
VERDICT: R100SentinelC1 C2 held — all five counting commands reproduce the frozen lines at F, and an independent pass located every one of the 16 quotes in the field the entry names, with tier B and pmid 40696441 confirmed in the capture.

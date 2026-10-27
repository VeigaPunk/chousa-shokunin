# RegistryGuard — round 60 registry- and freeze-integrity guard

Seat: `RegistryGuard` (executor). Judged on: operability, depth.
Frozen input: `corpus/evidence/round60-claims.md` (assignment SHA-256
`09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`).
Scope actually executed: the registry/identity surface of the two frozen claims — the
claim-freeze identity, the `corpus/SOURCES.md` registry, the registry↔entry↔counter
bindings the C2 predicate depends on, and the two freeze-side assertions the claims make
(`Round-58 bytes remain frozen`; the `R59Executor09.md` forge pointer). Read-only against
lane, source package and prior committed evidence. No external fetch, no writes outside
this report, no git/jj mutation, no subagent dispatch (one `labrat` was permitted; none was
needed — every probe below is a direct read or a run of the lane's own counter against a
scratch root).

Scratch used and removed before yield: `/fast/scratch/hyaku/chousa-r60/RegistryGuard`
(created fresh; removed at close, verified absent).

---

## 0. Verdict in one paragraph

The **registry is healthy but the freeze identity and the C2 measurement binding are not.**
`corpus/SOURCES.md` passes the canonical census at exit 0 (133 rows, ids unique S001–S133,
the five W04 duplicate-URL warnings are the pre-existing, already-dispositioned set), and
the S101 row's registry anchor is verifiable against the committed raw capture (6/6
character offsets land in the sections the row claims). But the frozen claims file on disk
hashes to `65721569…` and is not the `09d8053f…` artifact the dispatch pins, no file in the
round-60 evidence tree reproduces that digest, and the file is untracked and absent at the
declared base — so **the freeze is not auditable from any retained byte**. Worse for
admission, the C2 counter as committed **passes on the untouched base** (`C2=PASS`, exit 0)
because its subject is the already-committed round-37 entry
`corpus/knowledge/citation-count-semantics-r37.md`, not any round-60 note; it reads no
registry, no SCORECARD, and takes its pinned form from the script checkout rather than
`--root`. Under the frozen predicate's own clauses (`Base must fail because no round-60
entry exists`; `verify its S101 citation and metadata`; `require the scorecard's declared
disposition`) the counter does not measure the claim: **C2 is not admissible as frozen**,
and the negative result is measured, not asserted.

---

## 1. Freeze identity (claims file)

### F1 — the assigned immutable digest is not the artifact on disk  *(blocker)*

```sh
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
$ git status --porcelain corpus/evidence/round60-claims.md
?? corpus/evidence/round60-claims.md
$ git cat-file -e b379919a873e7080a31ef92c7002f55f5374e2c6:corpus/evidence/round60-claims.md; echo $?
128
```

- Assigned: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`
  (`.ufo/waves/round-60/w1-dispatch.json`, recorded verbatim in every seat prompt).
- Observed: `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`, 3355 bytes.
- The path is untracked and absent at the declared base `b379919` — there is no committed
  copy and no history to compare against.

Derived-form sweep (no common normalisation reproduces the assignment digest):

```sh
$ python3 - <<'EOF'
import hashlib, pathlib
b = pathlib.Path('corpus/evidence/round60-claims.md').read_bytes()
for k,v in {'raw':b,'no_trailing_nl':b.rstrip(b'\n'),'crlf':b.replace(b'\n',b'\r\n'),
            'no_final_byte':b[:-1]}.items():
    print(k, hashlib.sha256(v).hexdigest())
EOF
raw             65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
no_trailing_nl  cae804faeb016bf18d8183355e3885b7269e3fbce0a70d790cd688e5bb7175be
crlf            dbb847b81e834ecff97ca54bc2fe149a1fcdd2f8d2aa90aa50ac4c079778ba54
no_final_byte   cae804faeb016bf18d8183355e3885b7269e3fbce0a70d790cd688e5bb7175be
```

Whole-tree digest search over the round-60 evidence and `corpus/evidence/` (files ≤2 MiB)
for the assigned digest returned no match:

```sh
$ find .ufo/waves/round-60 corpus/evidence -type f -size -2M -print0 \
  | xargs -0 sha256sum | grep -c '^09d8053f'
0
```

Chronology (mtime, -03), which bounds the explanation:

| artifact | mtime |
|---|---|
| `corpus/evidence/round60-claims.md` | 2026-10-27 17:51:18 |
| `.ufo/waves/round-60/c1-before.txt` | 17:51:47 |
| `corpus/evidence/round60/c2-count.py` | 17:52:14 |
| `.ufo/waves/round-60/w1-spec.json` | 17:55:15 |
| `.ufo/waves/round-60/w1-dispatch.json` | 17:55:19 |
| `.ufo/waves/round-60/w1.ready` | 17:55:21 |

The claims file was last written **before** the spec, dispatch and ready marker, so the
dispatched digest is not the digest of the present bytes and was not produced by a
post-dispatch edit of this path. Either the digest was computed over an earlier version of
this file that was overwritten without retention, or it was computed over a different
serialisation that is nowhere recorded. Both are unrecoverable from lane bytes: the freeze
receipt (digest ⨯ artifact) does not exist. **Every verdict this round is therefore rendered
against the bytes present, and no seat may claim the frozen-claim identity is verified.**

### P1 — the claims' own `Round-58 bytes remain frozen` assertion holds  *(positive)*

```sh
$ sha256sum corpus/evidence/round58/c1-count.py
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f
$ git show b379919a873e7080a31ef92c7002f55f5374e2c6:corpus/evidence/round58/c1-count.py | sha256sum
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  -
$ git log --oneline -- corpus/evidence/round58/c1-count.py
9e73a03 round-58: freeze claims and before controls
```

Worktree bytes equal base bytes, and the only commit touching the file is its own freeze
commit. The C1 claim's "Round-58 bytes remain frozen" is true as written.

### P2 — the claims' `R59Executor09.md` forge pointer is accurate  *(positive)*

`.ufo/waves/round-59/w1/R59Executor09.md` is present and states exactly what C1's
before→after relies on: an honest candidate emits `REFUSE=0/7` … `C1=FAIL` (`:51`, `:88`),
and the echoing/spoofing candidate reaches `SUMMARY … REFUSE=7/7 … C1=PASS` / `EXIT=0`
while the hazard is realised (`:140-157`, `SYMLINK_OUT=pass(refused)(target-dir-written!)`,
`BEFORE_FOREIGN=deleted`; §6 "Correction — `C1=PASS` is reachable on the frozen bytes by
echoing the needle"). The claim's "C1=PASS with all seven hazards failing" is a fair
summary of that receipt; the pointer resolves.

---

## 2. Registry (`corpus/SOURCES.md`)

### P3 — canonical census passes; id space is clean  *(positive)*

```sh
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
```

- Exit 0; the five W04 rows are exactly the pre-existing, already-dispositioned set
  (`SCORECARD.md` round 41: `W04_DISPOSITIONED=5/5`), and identical to the round-start
  receipt `.ufo/waves/round-60/census-start.txt` — no round-60 drift.
- Independent id census: 133 data rows, 133 unique ids, `S001`–`S133`, zero duplicates:

```sh
$ python3 - <<'EOF'
import re, pathlib, collections
ids = re.findall(r'^ {0,3}\|\s*(S\d{3,})\s*\|', pathlib.Path('corpus/SOURCES.md').read_text(), re.M)
c = collections.Counter(ids)
print('rows', len(ids), 'unique', len(c), 'dups', {k:v for k,v in c.items() if v>1}, min(ids), max(ids))
EOF
rows 133 unique 133 dups {} S001 S133
```

- `corpus/SOURCES.md` is unchanged against the claim base (`git diff --stat b379919 --
  corpus/SOURCES.md` empty), so nothing was silently appended to serve the round.

### S101 row: cells, linkage and anchor verification  *(positive, with one binding gap)*

The row parses to the contract's 11 columns and is internally consistent with the entry it
serves:

| # | cell | observed |
|---|---|---|
| 1 | id | `S101` |
| 2 | source | `…数据规范（修订本）— copy hosted by 哈尔滨工业大学 — https://jc.hit.edu.cn/_upload/article/files/f7/54/…/1f6f2731-….doc` |
| 3–4 | kind / tier | `docs` / `B` |
| 5 | scope | bibliographic/data-specification scope only |
| 6 | anchor | sections 11, 14.1/14.4, 15.7 table; "located quotes char 11170, 11205, 11993, 12161, 13247, 34374" |
| 7 | teaches | reference-record elements incl. `文献类型及载体类型标志` |
| 8–10 | status/opened/recheck | `mined` / `2026-10-25` / `180d` |
| 11 | used-by | `corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md, corpus/lessons/round-59.md` |

Linkage is closed: the r37 entry is the only `corpus/knowledge/` file citing `S101`
(`grep -rln S101 corpus/knowledge/` → one path), and that path is listed in `used-by`; the
entry's `verified-at: 2026-10-25` / `recheck: 180d` agree with the row's `opened` /
`recheck`.

Anchor verification against the committed capture
(`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, decodes as UTF-16LE, sha256
`6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, committed and equal at
base) — all six registered offsets land in the section the row names:

| offset | raw-capture text at offset | row claim |
|---:|---|---|
| 11170 | `…为便于文献的统计和期刊评价…标识一个文献标志码` | §11 |
| 11205 | `…应根据其内容性质标识一个文献标志码…` | §11.6 |
| 11993 | `…本规范推荐采用GB/T 7714中规定的顺序编码制…` | §14.1 |
| 12161 | `…c. 文献类型及载体类型标志；…` | §14.2 |
| 13247 | `…参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束` | §14.4 |
| 34374 | `15.7参考文献格式，参照ISO 690，采用1位字母…` | §15.7 table |

**Gap (registry↔measurement):** these six registered offsets are the row's claim, and none
of them is exercised by the C2 counter — the counter binds one line of a *derived form*
(`FORM_SHA`), not the registry anchor (see F4e). Registry cells are correct; the frozen
predicate's "quote locations" clause has no measurement behind it.

### Collision / id-space guard receipts are reproducible  *(positive)*

The committed receipts `.ufo/waves/round-60/{reg-ids,staged-ids,collisions}` re-derive
byte-identically under the census-compatible 0–3-space pattern against the read-only source
package:

```sh
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > coll/reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > coll/staged-ids
$ comm -12 coll/reg-ids coll/staged-ids > coll/collisions
133 reg-ids / 114 staged-ids / 52 collisions
$ cmp coll/reg-ids .ufo/waves/round-60/reg-ids        # identical
$ cmp coll/staged-ids .ufo/waves/round-60/staged-ids  # identical
$ cmp coll/collisions .ufo/waves/round-60/collisions  # identical
```

52 of 114 staged ids (`S082`–`S133`) collide with the live registry, so package adoption
stays closed — consistent with the frozen claims, which adopt nothing from the package this
round. No source-tree write occurred.

---

## 3. C2 measured against its own frozen predicate

Predicate clauses (claims file, C2): the counter "must establish source digest and quote
locations from committed S101 raw capture using the pinned capture-text form, verify the new
entry's exact observation and no overreach against those source bytes, verify its S101
citation and metadata, and require the scorecard's declared disposition. Base must fail
because no round-60 entry exists."

Counter under test: `corpus/evidence/round60/c2-count.py` (untracked:
`git status --porcelain` → `?? corpus/evidence/round60/c2-count.py`).

### F2 — do-nothing control meets the target: `C2=PASS` on the untouched base  *(blocker)*

```sh
$ python3 -B corpus/evidence/round60/c2-count.py \
    --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --work /fast/scratch/hyaku/chousa-r60/RegistryGuard/work
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

Cause is the subject binding, not a subtle pass: `ENTRY` is
`corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8`, `:13`) — a round-37/49
entry that is **already committed at base** (worktree bytes equal base bytes,
`sha256 bb80627b…`). The counter has no round-60 identity anywhere except a directory name
in the form path (`grep -n 60 c2-count.py` → `:2` docstring, `:7` form path, `:10`
`RAW_SHA` hex constant, `:13` form path). The entry is the counter's only entry-side input;
removing it flips the verdict:

```sh
$ mv <scratch-root>/corpus/knowledge/citation-count-semantics-r37.md /tmp/r37.hold
$ python3 -B corpus/evidence/round60/c2-count.py --root <scratch-root> --work ... 
C2=ERROR FileNotFoundError: …/corpus/knowledge/citation-count-semantics-r37.md
exit=2
```

Per the round contract's claim-sizing rule (a do-nothing control must not reach the target),
this alone blocks C2 as frozen: either the counter is measuring the wrong artifact, or the
claim is already satisfied at base. The committed base receipt `.ufo/waves/round-60/c2-before.txt`
("Baseline must fail by missing round-60 source gate; C2 not admitted") does not reproduce:
the counter it names prints PASS on that same state.

The predicate's target text is also already present at base — the entry's `#### Unknown`
line 79 is verbatim `- Whether the specification copy (S101) is the version in force, …`,
which is the exact sentence `scoped` requires (`c2-count.py:18`), so a "new note" would
duplicate committed text.

### F3 — no registry read: the "S101 citation" clause is a literal prefix  *(blocker)*

```sh
$ grep -nE 'SOURCES|registry|used-by' corpus/evidence/round60/c2-count.py
NO_REGISTRY_READ
```

With `--root` pointing at a copy that contains **no `corpus/SOURCES.md` at all**, the counter
still prints `C2=PASS` (same run shape as F2; `RAW_PIN=1 FORM_PIN=1 QUOTE=1 METADATA=1
LIMIT=1`). So no registry row, status, id, URL equality or `used-by` membership is consulted.
`metadata` (`:17`) is four substring tests; a forged note with a truncated, non-matching URL
and a fabricated observation passes end to end. Exact reproduction (scratch only; the lane
counter was never edited):

```sh
S=/fast/scratch/hyaku/chousa-r60/RegistryGuard/root        # lane copy: corpus/{captures,evidence,knowledge}
cp corpus/evidence/round60/c2-count.py "$S/corpus/evidence/round60/c2-count-forged.py"
# in that scratch copy only, change the single ENTRY literal on line 8 to
#   ENTRY=ROOT/'corpus/knowledge/citation-count-semantics-r60-forged.md'
# no other byte changes; the lane counter at corpus/evidence/round60/c2-count.py stays untouched
mkdir -p "$S/.ufo/waves/round-60"; cp .ufo/waves/round-60/s101-open.txt "$S/.ufo/waves/round-60/"
cat > "$S/corpus/knowledge/citation-count-semantics-r60-forged.md" <<'EOF'

# Forged round-60 note
source: S101 — https://jc.hit.edu.cn/ — (no located quote)
verified-at: 2026-10-27
recheck: 180d
#### Observation
- The specification requires authors to cite in MLA style with parentheses. (fabricated)
#### Unknown
Whether the specification copy (S101) is the version in force today is unknown.
EOF
$ python3 -B "$S/corpus/evidence/round60/c2-count-forged.py" --root "$S" --work <work>
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

The forged note's `source:` URL is the bare host prefix with no document path, its observation
contradicts the capture, and it carries no located quote — and the counter credits it.

The quote leg (`QUOTE`, `LINE`) is computed over the **form**, not over the entry
(`:15`: `at=[i for i,l in enumerate(lines,1) if EXPECTED in l]` where `lines` come from the
form bytes). Nothing binds what the entry asserts to any source line, so "exact observation
and no overreach" is unmeasured — the fabricated-MLA mutant shows it.

### F4 — `<lane-copy>` isolation is broken; `--work` is dead  *(operability)*

- `FORM` is `ROOT/'.ufo/waves/round-60/s101-open.txt'` (`:7`) and in `main` is again
  `form=ROOT/'.ufo/…'` (`:13`), where `ROOT = pathlib.Path(__file__).resolve().parents[3]`
  (`:5`) — the **script checkout**, never `--root`. Measured: running the lane counter with
  `--root` at a scratch root that has **no `.ufo/` directory** still prints `FORM_PIN=1`,
  i.e. the pinned form was read from the lane checkout, not from the root under test.
- `--work` is declared and never referenced (`grep -n work` → `:13` only), so the predicate's
  `<fresh-absolute-dir>` argument has no effect.
- Consequence for the frozen predicate: `--root <lane-copy>` can mix one tree's raw capture
  and entry with another tree's form, and a PASS cannot be attributed to the lane copy.

### F5 — the "scorecard's declared disposition" clause has nothing to bind  *(blocker, claim-side)*

- `grep -nE 'SCORECARD|scorecard' corpus/evidence/round60/c2-count.py` → `NO_SCORECARD_READ`.
- `SCORECARD.md` (2922 lines) has **no round-60 section and no round-59/60 planned row**;
  the last headings are `## Capabilities (round-57 addition)` :2883,
  `## Planned — round 58` :2889, `## Round 58 verdict …` :2902.
So the predicate names an artifact state that does not exist, and the counter would not read
it if it did. As frozen, the clause is vacuous; as a claim, a PASS cannot be attributed to a
declared disposition.

### P4 — form provenance is recoverable and byte-identical to a committed twin  *(positive)*

```sh
$ python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > form-regen.txt
$ sha256sum form-regen.txt .ufo/waves/round-60/s101-open.txt corpus/evidence/round59/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  form-regen.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  corpus/evidence/round59/s101-open.txt
```

`FORM_SHA` therefore pins bytes that (i) regenerate from the committed raw capture with the
lane's own `tools/capture-text.py` and (ii) equal a committed round-59 artifact — the gap is
*where the counter reads them from* (F4), not whether they are derivable.

---

## 4. C2 verdict

**Not admissible as frozen; measured, not asserted.**

- Base does not fail — the counter prints `C2=PASS` on the untouched committed state (F2),
  so the claim's own before/after has no measurable delta, and the target is reachable by a
  do-nothing control.
- Two of the predicate's clauses have no measurement at all: the S101 registry citation
  (F3) and the scorecard disposition (F5), and the entry-to-source quote binding is absent
  (F3), while the six registered anchor offsets are never exercised (§2).
- One clause is miswired rather than missing: `--root <lane-copy>` cannot isolate the form
  (F4).
- None of this disputes the *source* work the round can legitimately do — the S101 row is
  well-formed, its anchors verify against the committed capture, and the form regenerates.
  It disputes only that the frozen counter, as written, measures the claim.

**Smallest safe corrections (advisory — not applied; I hold no write scope beyond this
report):**
1. Bind `ENTRY` to the round-60 note path named in the claims/SCORECARD, and require a
   non-empty diff of that path against the base (`git show <base>:<path>` absent or
   different) — this restores "base must fail".
2. Resolve `S101` through `corpus/SOURCES.md` inside `--root`: id present, `status` =
   `mined`, entry path in `used-by`, and the entry's declared URL equal to the row's URL —
   not a prefix.
3. Derive `FORM` from `root` (not module `ROOT`), assert the regenerated bytes against
   `tools/capture-text.py` on the `root`'s raw capture, and exercise the row's registered
   character offsets instead of one form line.
4. Require the SCORECARD round-60 C2 disposition row, or drop the clause from the predicate
   before the next freeze.
5. Freeze with a retained artifact: commit the claims file (or its digest receipt) in the
   same act that publishes the digest, so no seat has to render verdicts against an
   unreconcilable identity (F1).

---

## 5. Claims-file summary the integrator must carry forward

| item | verdict | evidence |
|---|---|---|
| assigned claims digest vs on-disk bytes | **mismatch, unreconcilable** | F1 (four derivations, whole-tree scan, mtime order) |
| claims file committed at base | **no** — untracked, absent at `b379919` | F1 |
| `Round-58 bytes remain frozen` | **holds** | P1 (`65da18bb…`, single commit `9e73a03`) |
| `R59Executor09.md` forge pointer | **holds** | P2 (`:51`, `:140-157`, §6) |
| registry census | **exit 0**, five pre-existing W04 | P3 |
| registry ids | 133 rows, unique `S001`–`S133` | P3 |
| S101 row cells / used-by closure | **consistent** | §2 table |
| S101 anchor char offsets vs committed capture | **6/6 land in claimed sections** | §2 table |
| staged-package collision receipts | **byte-identical on recompute** (52 collisions) | §2 last block |
| round-60 C1/C2 counters committed | **no** — both untracked | `git status` |
| C2 counter on base | **`C2=PASS`, exit 0 (do-nothing meets target)** | F2 |
| C2 registry/citation leg | **absent** (no SOURCES read; forged URL passes) | F3 |
| C2 lane-copy isolation | **broken** (`FORM` from script `ROOT`; `--work` dead) | F4 |
| C2 SCORECARD disposition leg | **absent**, and no round-60 section exists | F5 |
| pinned form provenance | **recoverable**, equals committed round-59 twin | P4 |

Risks carried: (i) any closure that cites the assigned `09d8053f…` as a verified identity
would be unfounded; (ii) a C2 verdict of `PASS` from the current counter would credit work
that already existed at base; (iii) the counters are untracked, so no verdict this round is
against committed bytes until the lane commits them.

Open L0 items unchanged; I added none (the freeze-identity defect is resolvable inside the
lane by correction 5, and C2's clauses are the frozen claim's own, which this seat may not
rewrite).

---

## 6. Discipline

- Reads only: lane repo (working tree + read-only `git show/log/diff/ls-files`),
  `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` (read, never run/write).
- Scratch: `/fast/scratch/hyaku/chousa-r60/RegistryGuard` — created for the copy-root
  mutants, all receipts reproduced inline above, directory removed before yield.
- No external fetch, no network, no commits, no jj/git mutation, no fleet-root or sibling
  writes, no subagent dispatch, no `agent://all`.
- Tool installs: none needed.

# Scout — independent id-collision recheck (round 46, wave 1)

seat: `L1Chousa46.ScoutCollisionRecheck` · date 2026-10-25T07:27-03:00 · leaf, no dispatch
item: re-run the id-collision check for this round's append; confirm S084 is the lane's
highest id so the next five are S085–S089; check staged-vs-lane URL equality (E04 class)
for the five adopted documents; verify the amendment's prose ids by document.
inputs (read-only): `corpus/SOURCES.md` sha256 `1b53080660abcc64b79c6421fb3280ef5b7acc2836c3804bb9db1ece1149d384`;
`merge/chousa/SOURCES.append.md` sha256 `a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696`.
No installs; no network; no lane writes except this file.

## Commands (decisive output only)

1. `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>` → `84`; `<append>` → `114`.
2. extract `S\d{3}`, `sort -u`, `comm -12`:
   `INTERSECTION_SIZE=3` · `INTERSECTION_MEMBERS=[S082,S083,S084]` · `LANE_MAX=S084`
   `STAGED_MIN=S082 STAGED_MAX=S195`
3. python row/URL census over both files (`^ {0,3}\|\s*(S\d{3,})\s*\|`, URL = `https?://[^\s|)\]>,]+`):
   `lane rows 84 first S001 last S084` · `app rows 114 first S082 last S195`
4. contiguity: `count 84 min 1 max 84 unique 84 gaps []` · `S085-089 present in lane? none`
5. five adopted URLs vs lane registry — lane side `NOT IN LANE REGISTRY` for all five.
6. intra-staged duplicate URLs: `https://fever.ai/dataset/fever.html ['S097','S120']` (plus 10
   other same-URL pairs inside the package).
7. staged URL also held by lane:
   `S140==S083 arxiv.org/html/2305.13117v3` · `S095==S081 current.ndl.go.jp/e2867`
   `S139==S082 raw…/AVeriTeC/main/README.md` · `S132==S084 raw…/AVeriTeC/main/data/train.json`
   `S094==S080 warp.ndl.go.jp/en/info/qanda` · `S123==S078 …/PMC6148622/fullTextXML`
   `S084==S079 www.rfc-editor.org/rfc/rfc7089.txt`
8. `git -C <lane> log --oneline -1` → `c2f0e9d round-46: freeze three claims …`

## Findings

**F1 — id intersection fires, size 3: S082, S083, S084. The three collide on ID and clash on
DOCUMENT.** Held (round 45) vs staged (corpus-expansion round 1):

| id | lane document | staged document |
|---|---|---|
| S082 | AVeriTeC dataset README | PRISMA-S (doi 10.1186/s13643-020-01542-z) |
| S083 | AVeriTeC corpus paper arXiv:2305.13117v3 | Cochrane Handbook ch. 4 |
| S084 | AVeriTeC train.json | RFC 7089 Memento |

Applying `SOURCES.append.md` verbatim re-defines three held ids → the check FAILS as staged.
Confidence: certain (byte-compared rows, `corpus/SOURCES.md:92-94` vs `SOURCES.append.md:7-9`).

**F2 — lane highest id is S084; S085–S089 are free.** 84 rows, contiguous S001–S084, no gaps,
no S085+ row. `S085–S089` is therefore the correct next block. Confidence: certain.

**F3 — census E04 (duplicate-URL) does not fire for any of the five adopted documents.**
None of the five URLs occurs anywhere in the lane registry:

| lane (new) | staged source row | URL | staged-vs-lane URL match |
|---|---|---|---|
| S085 | S120 | `https://fever.ai/dataset/fever.html` | none |
| S086 | S121 | `https://aclanthology.org/N18-1074.pdf` | none |
| S087 | S122 | `https://zenodo.org/api/records/4925954` | none |
| S088 | S127 | `https://fever.ai/dataset/averitec.html` | none |
| S089 | S128 | `https://arxiv.org/html/2505.17978v2` | none |

The staged→lane offsets are not uniform (S120→S085 = −35, S121→S086 = −35, S122→S087 = −35,
S127→S088 = −39, S128→S089 = −39), so no arithmetic rule reproduces the block; the binding is
by document only. Confidence: certain.

**F4 — one E04 event sits inside the incoming package and touches an adopted document.**
The FEVER dataset page is staged twice: `S097` (scope = support-test label set, used-by
`corpus/knowledge/claim-support-test-r37.md`) and `S120` (scope = verdict-to-evidence binding,
used-by the r39 entry). `S120`'s own scope cell declares the distinction ("**distinct from wave
2's FEVER dataset row**"). Under the campaign's own rule this is the surface-don't-reject case,
not a duplicate: `.ufo/waves/corpus-expansion-1/merge-plan.py:390-399` (sha256 `90a19108…`) —
"may already hold a row for the SAME page. That is not automatically a duplicate". Rejection
needs same URL **and** same tier **and** near-identical claim (`doctrine/poison-watch.md:2081-2098`).
Recorded so the operator sees that S085 (fever.ai/dataset/fever.html) is the second lane row for
that page if S097 is ever mirrored. Confidence: high (rule text read; no census script located —
`sources-census.sh` is absent from both trees, so "E04" is cited by its doctrine, not by a rule id).

**F5 — the amendment's prose ids bind by document, not by id; two of the three are dangling.**
Prose (`knowledge/…/evidence-pool-versioning-r39-amendment-2026-10-23.md:44-47`):
"RFC 7089's Memento and NDL's timestamp-in-URL capture scheme (round 1's `S071`, round 2's `S082`)"
and line 51 "The lane's `S095` amendment".

| prose token | does it exist in the stage? | lane reading | document it must name | correct lane id |
|---|---|---|---|---|
| `S071` | no — staged block starts at S082 (`lanes/chousa/SOURCES-PROPOSED.md:8`) | S071 = GNU coreutils `env(1)` (`SOURCES.md:81`) | RFC 7089 Memento | **S079** (`SOURCES.md:89`) |
| `S082` | yes, but = PRISMA-S | S082 = AVeriTeC README (`SOURCES.md:92`) | NDL timestamp-in-URL (E2867) | **S081** (`SOURCES.md:91`) |
| `S095` | yes, = NDL E2867 | no lane row S095 | NDL E2867 note | **S081** (`SOURCES.md:91`) |

By-document anchors: RFC 7089 = lane `S079` = staged `S084`; NDL E2867 = lane `S081` = staged
`S095`; the *other* WARP document (FAQ, staged `S094`) is lane `S080` and is **not** the
timestamp-in-URL note. Both prose ids are wrong under every reading (stage and lane); rewriting
them to `S079`/`S081` is the only binding that survives. Confidence: certain for the ids;
the sentence's content claim ("its own pin fixes bytes and not time") also appears in the lane
entry at `corpus/knowledge/evidence-pool-versioning-r39.md:20`, so the referent is the lane's
own sha256 pin, consistent with `S081`.

**F6 — the merge report's collision table is stale by three rows.** `MERGE-REPORT.md:9` states
"lane registry currently holds **81** rows; first staged id is **S082**"; the lane holds 84
(`S082–S084` landed in round 45, after packaging). Its "Rows whose source the lane's registry
already holds" table lists only `S084/S079, S094/S080, S095/S081, S123/S078`; the actual set is
seven — `S132/S084`, `S139/S082`, `S140/S083` are missing because those lane rows did not exist
at packaging time. Consequence: those three staged rows are second rows for the three documents
round 45 just mined, and must not be appended as new ids.

**F7 — the in-flight lane entries already carry the correct binding** (read, not mine; untracked):
`corpus/knowledge/evidence-pool-versioning-r39.md:3-5` = S085/S086/S087 on the three URLs;
`…-amendment-2026-10-23.md:3-4` = S088/S089; both cite RFC 7089 as `S079` and the NDL note as
`S081` (r39 line 22, amendment line 21). This matches F3/F5 exactly. The registry mirror has not
landed: `corpus/SOURCES.md` still ends at S084, so the five URLs are absent from it as of this read.

## Verdict

- ID collision for the append **as staged**: FAILS — intersection 3 (`S082`,`S083`,`S084`), and
  all three clash on document.
- ID collision for the **round's five-row adopt**: CLEAN — S085–S089 free (lane max S084,
  contiguous, no gaps) and no held URL duplicated.
- E04 for the five documents: **0/5 matches** in the lane registry; one declared same-URL pair
  (`S097`/`S120`) exists inside the package and is documented as a distinct scope.
- Prose-id binding: staged `S071` names nothing (block starts S082); lane `S071` is coreutils
  `env(1)`. RFC 7089 → `S079`; NDL E2867 → `S081`. `S082`/`S095` prose tokens are dangling in
  both readings and must be rewritten by document.

## Residual unknowns

- The census rule id `E04` could not be resolved to a script: no `sources-census.sh` under
  `/home/vgpnk/Projects/shokuknow/scripts` or the lane. The class is identified here from
  `MERGE-REPORT.md` §"Rows whose source the lane's registry already holds" and
  `doctrine/poison-watch.md:2081-2098`. If the id is owned by a harness I cannot see, its wording
  is unverified.
- `corpus/SOURCES.md` is moving (registrar seat in flight); counts above are the state at
  07:27:21-03:00 with the lane at `c2f0e9d`.
